from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from donation.models import Donation, Institution


class IndexPage(View):
    def get(self, request):
        quantity = Donation.objects.all().aggregate(Sum('quantity'))
        institution_count = Institution.objects.count()
        return render(request, 'index.html', context={'quantity': quantity,
                                                      'institutions': institution_count})


class AddDonation(TemplateView):
    template_name = 'form.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'
