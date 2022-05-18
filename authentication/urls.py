from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('register', views.register, name="register"),
    path('resend-otp', views.resend_otp, name="resend-otp"),
]
