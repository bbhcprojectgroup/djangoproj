from django.urls import path
from . import views



urlpatterns=[
    path('',views.home, name="home"),
    path('register',views.register, name="register"),
    path('log_in',views.log_in, name="log_in"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('log_out',views.log_out, name="log_out"),
    path('index',views.about_us,name="about_us"),
    
]