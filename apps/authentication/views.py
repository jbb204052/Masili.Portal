from time import sleep

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from . import helper
from .forms import *
from .models import Profile


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")

            # check if email is already registered
            if User.objects.filter(email=email).exists():
                msg = 'Email address is already registered.'
            else:
                form.save()
                user = authenticate(email=email, password=raw_password)

                # save the user to Profile
                profile = Profile(user=user)
                profile.is_resident = True
                profile.save()

                request.session['message'] = 'Registration successful. Redirecting to login page...'
                request.session['flag'] = 'registration_success'
                return redirect("/redirecting/")

                sleep(3)

                return redirect("/login/")
                success = True
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



def otp_email_view(request):
    msg = None
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            otp = helper.generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email
            helper.send_email(email, 'Reset Password', 'You requested to reset your password on your Masili Portal account. To proceed, please enter the OTP in the website, and we\'ll give you the option to change your password.', user.first_name, otp)
            return redirect("/password_reset/otp/")

        else:
            msg = 'Email address is not associated with any account.'

    return render(request, "otp/OTPEmailForm.html", {'form': OTPEmailForm(), 'msg': msg})


def verify_OTP(request):
    msg = None
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            if otp == request.session['otp']:
                return redirect("/password_reset/new_password/")
            else:
                msg = 'Invalid OTP'
        else:
            msg = 'Invalid input'
    else:
        form = OTPForm()

    return render(request, "otp/OTPForm.html", {'form': form, 'msg': msg, 'email': request.session['email']})


def new_password(request):
    msg = None
    success = False

    if request.method == "POST":
        form = PasswordResetForm(request.user, request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            if password == password2:
                user = User.objects.get(email=request.session['email'])
                user.set_password(password)
                user.save()

                request.session['message'] = 'Password changed successfully. Redirecting to login page...'
                request.session['flag'] = 'password_changed_success'

                sleep(3)

                success = True
                return redirect("/redirecting/")
            else:
                msg = 'Passwords do not match.'

        else:
            msg = 'Form is not valid'
    else:
        form = PasswordResetForm(request.user)

    return render(request, "accounts/password_reset.html", {"form": form, "msg": msg})


def redirecting(request):
    context = {'message': request.session['message'], 'flag': request.session['flag']}
    return render(request, "accounts/redirecting_template.html", context)