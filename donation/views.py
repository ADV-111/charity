from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from donation.forms import UserForm
from donation.models import Donation, Institution


class IndexPage(View):
    def get(self, request):
        quantity = Donation.objects.all().aggregate(Sum('quantity'))
        institution_count = Donation.objects.distinct('institution_id').count()

        foundations_list = Institution.objects.filter(type__exact='F')
        ngos = Institution.objects.filter(type__exact='OP')
        h2h_collections = Institution.objects.filter(type__exact='ZL')

        # paginator_f = Paginator(foundations_list, 4) #TODO: do paginatora ale i tak nie działa
        # page = request.GET.get('page', 1)
        # foundations = paginator_f.get_page(page)

        return render(request, 'index.html', context={'quantity': quantity,
                                                      'institutions': institution_count,
                                                      'foundations': foundations_list,
                                                      'ngos': ngos,
                                                      'h2h_collections': h2h_collections})


class AddDonation(TemplateView):
    template_name = 'form.html'


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})


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
                password = form.cleaned_data['password'] # password is validated through form's "clean" method
                user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                return redirect(f"{reverse('login')}#login")
            except IntegrityError:
                msg = 'Podany email już istnieje w bazie danych'
                return render(request, 'register.html', {'form': form, 'msg': msg})
        else:
            return render(request, 'register.html', {'form': form})
