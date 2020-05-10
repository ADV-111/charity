"""charity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from donation.views import IndexPage, LoginView, RegisterView, AddDonation, LogoutView, AddDonationConfirmation, \
    UserProfileView, UserSettingsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexPage.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('add_donation/', AddDonation.as_view(), name='add_donation'),
    path('add_donation/confirmation/', AddDonationConfirmation.as_view(), name='add_donation_confirmation'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/settings/', UserSettingsView.as_view(), name='user_settings'),
]
