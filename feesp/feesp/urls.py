"""feesp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from login.admin import ac_site
from feedbck.admin import ac_site
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from examfee import views as eview



logurl='login.urls'

urlpatterns = [
    path('',include(logurl)),
    path('admin/', ac_site.urls),
    path('register',include(logurl)),
    path('log_in', include(logurl)),
    path('index',include(logurl)),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('log_out', include(logurl)), 
    path('payexam',include('examfee.urls')),
    path('savestud',eview.savestud,name="savestud"),
    path('exform',eview.exprintform,name="exprintform"), 
    path('homepage',TemplateView.as_view(template_name='home.html')),
    path('ajax-test-view', eview.myajaxtestview, name='myajaxtestview'),


    path('feedback',include('feedbck.urls')),    
]
