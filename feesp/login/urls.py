from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name="home"),
    path('register',views.register, name="register"),
    path('log_in',views.log_in, name="log_in"),
    path("password_reset", views.password_reset_request, name="password_reset")
]