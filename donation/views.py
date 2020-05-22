from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView

from donation.forms import UserForm, LoginForm
from donation.models import Donation, Institution, Category
from donation.tokens import account_activation_token


class IndexPage(View):
    def get(self, request):
        quantity = Donation.objects.all().aggregate(Sum('quantity'))
        institution_count = Donation.objects.distinct('institution_id').count()

        foundations_list = Institution.objects.filter(type__exact='F')
        ngos = Institution.objects.filter(type__exact='OP')
        h2h_collections = Institution.objects.filter(type__exact='ZL')

        # paginator_f = Paginator(foundations_list, 4)  # TODO: do paginatora ale i tak nie działa
        # page = request.GET.get('page', 1)
        # foundations = paginator_f.get_page(page)

        return render(request, 'index.html', context={'quantity': quantity,
                                                      'institutions': institution_count,
                                                      'foundations': foundations_list,
                                                      # 'foundations': foundations,
                                                      'ngos': ngos,
                                                      'h2h_collections': h2h_collections})


class AddDonation(LoginRequiredMixin, View):
    def get_login_url(self):
        return f"{reverse('login')}#login"

    # def get_redirect_field_name(self):
    #     return f"{reverse('add_donation')}#steps-form"

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories,
                                             'institutions': institutions})

    def post(self, request):
        category_id_list = request.POST.getlist('category')
        bags_quantity = request.POST.get('bags')
        institution_id = request.POST.get('organization')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        more_info = request.POST.get('more_info')
        user_id = request.user.id
        donation = Donation.objects.create(quantity=bags_quantity,
                                           institution_id=institution_id,
                                           address=address,
                                           city=city,
                                           zip_code=postcode,
                                           phone_number=phone,
                                           pick_up_date=date,
                                           pick_up_time=time,
                                           pick_up_comment=more_info,
                                           user_id=user_id)
        donation.categories.add(*category_id_list)
        donation.save()
        return redirect('add_donation_confirmation')


class AddDonationConfirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html', {})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(username__iexact=email).exists():
                user = authenticate(request, username=email, password=password)
                if user is None:
                    msg = 'Niepoprawne hasło'
                    return render(request, 'login.html', {'form': form, 'msg': msg})
                elif user is not None:
                    login(request, user)
                    return redirect('index')
            else:
                return redirect(f'{reverse("register")}#register')
        else:
            return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class RegisterView(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['email']
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                password = form.cleaned_data['password']  # password is validated through form's "clean" method
                user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                last_name=last_name)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Aktywuj swoje konto'
                message = render_to_string('acc_activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email
                email_message = EmailMessage(mail_subject, message, to=[to_email])
                email_message.send()
                return render(request, 'register_confirmation.html', {})
                # return redirect(f"{reverse('login')}#login")
            except IntegrityError:
                msg = 'Podany email już istnieje w bazie danych'
                return render(request, 'register.html', {'form': form, 'msg': msg})
        else:
            return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Dziekujemy za potwierdzenie rejestracji. Możesz się teraz zalogować')
    else:
        return HttpResponse('Link do aktywcji jest nieważny')


class UserProfileView(LoginRequiredMixin, View):
    def get_login_url(self):
        return f"{reverse('login')}#login"

    def get(self, request):
        user_object = request.user
        is_taken = request.GET.get('is_taken')
        don_id = request.GET.get('don_id')
        if don_id is not None:
            Donation.objects.filter(pk=don_id).update(is_taken=is_taken)
        donations = Donation.objects.filter(user__email__iexact=user_object.email).order_by('is_taken',
                                                                                            'date_added',
                                                                                            'pick_up_date')
        return render(request, 'user_profile.html', context={'donations': donations,
                                                             'profile': user_object})


# class UserProfileView(LoginRequiredMixin, DetailView):
#     context_object_name = 'profile'
#     model = User
#     template_name = 'user_profile.html'
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['donations'] = Donation.objects.filter(user__email__iexact=self.object.email).order_by('is_taken',
#                                                                                                        'date_added',
#                                                                                                        'pick_up_date')
#         return context
#
#     def get_login_url(self):
#         return f"{reverse('login')}#login"

class UserSettingsView(LoginRequiredMixin, View):
    def get(self, request):

        return render(request, 'settings.html', context={'user_object': request.user})

    def post(self, request):
        user_object = request.user
        password = request.POST.get('password')
        submit_btn_value = request.POST.get('submit_button')

        msg = ""

        if not user_object.check_password(password):
            msg = "Hasło nieprawidłowe"
            return render(request, 'settings.html', context={'user_object': user_object, 'msg': msg})

        if submit_btn_value == 'change_settings':
            try:
                user_object.username = request.POST.get('email')
                user_object.email = request.POST.get('email')
                user_object.first_name = request.POST.get('first_name')
                user_object.last_name = request.POST.get('last_name')
                user_object.save()
                msg = "Ustawienia zakutalizowane"
            except IntegrityError:
                msg = 'Podany email już istnieje w bazie danych'

        elif submit_btn_value == 'change_password':
            new_password_1 = request.POST.get('new_password_1')
            new_password_2 = request.POST.get('new_password_2')
            if new_password_1 != new_password_2 and new_password_1 is not None:
                msg = 'Hasła nie są takie same'
            else:
                user_object.set_password(new_password_1)
                user_object.save()
                msg = 'Poprawnie zmieniono hasło'
        return render(request, 'settings.html', context={'user_object': request.user, 'msg': msg})

    def get_login_url(self):
        return f"{reverse('login')}#login"