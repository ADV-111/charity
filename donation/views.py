from django.views.generic import TemplateView


class IndexPage(TemplateView):
    template_name = "index.html"


class AddDonation(TemplateView):
    template_name = 'form.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'


