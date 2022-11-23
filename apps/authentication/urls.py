# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('social_login/', include('allauth.urls')),

    path('password_reset/email/', otp_email_view, name="password_reset"),
    path('password_reset/otp/', verify_OTP, name="otp"),
    path('password_reset/new_password/', new_password, name="new_password"),

    path('redirecting/', redirecting, name="redirecting"),
]
