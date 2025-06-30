"""
URL configuration for ishowspeed project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from main_page.views import main_page,logout
from register.views import register_user,send_verification_code,verification_view,clear_registration_session


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main_page,name="main_page"),
    path('register/',register_user,name="reg"),
     path('verify/', verification_view, name="verify"),
    path('send-verification-code/', send_verification_code, name='send_verification_code'),
    path('accounts/',include("allauth.urls")),
    path('logout/',logout),
    path('clear-registration-session/', clear_registration_session, name='clear_registration_session'),
    path('profile',include("userprofile.urls"),name="profile")
]
