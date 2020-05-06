from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from donation.forms import UserForm, LoginForm
from donation.models import Donation, Institution, Category


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
        username = None
        if request.user.is_authenticated:
            username = request.user.id
        donation = Donation.objects.create(quantity=bags_quantity,
                                           institution_id=institution_id,
                                           address=address,
                                           city=city,
                                           zip_code=postcode,
                                           phone_number=phone,
                                           pick_up_date=date,
                                           pick_up_time=time,
                                           pick_up_comment=more_info,
                                           user_id=username)
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
                user.save()
                return redirect(f"{reverse('login')}#login")
            except IntegrityError:
                msg = 'Podany email już istnieje w bazie danych'
                return render(request, 'register.html', {'form': form, 'msg': msg})
        else:
            return render(request, 'register.html', {'form': form})
