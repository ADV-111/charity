from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

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


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'
