from time import sleep

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.template import loader

from . import helper
from .forms import *
from .models import Profile
from apps.home import models as home_models

from notifications.signals import notify

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            if User.objects.filter(email=email).exists():
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    get_user = User.objects.get(email=email)
                    if get_user.is_active:
                        login(request, user)
                        return redirect("home")
                    else:
                        msg = 'Your account has not been approved yet. We will send you an email notification once approved.'
                else:
                    msg = 'Invalid credentials.'
            else:
                msg = 'Email address is not associated with any account.'
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
                bdate = request.POST['bdate']
                __user = form.save(commit=False)
                __user.username = email
                __user.is_active = False
                __user.save()
                user = authenticate(email=email, password=raw_password)
                _user = User.objects.get(email=email)

                profile = Profile.objects.create(user=_user, birthdate=bdate)

                success = True
                _chairman = User.objects.get(profile__account_type='CHAIRMAN')
                # notify.send(request.user, recipient=_chairman, verb='has requested to join the Masili Portal.', cta_link='/accounts_management/pending_approval/approve/{}'.format(_user.id))


                request.session['message'] = 'Your account has been queued for approval. You will receive an email ' \
                                             'once your account has been approved. '
                request.session['flag'] = 'registration_success'
                return render(request, "accounts/redirecting_template.html", {'message': request.session['message']})
                sleep(3)
                return redirect("/login/")
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


def accounts(request):
    accounts = User.objects.filter(is_active=True)
    context = {'segment': {'accounts', 'account_type'}, 'accounts': accounts}
    html_template = loader.get_template('home/account_mgmt/accounts_list.html')
    return HttpResponse(html_template.render(context, request))


def account_update(request, id):
    account = User.objects.get(id=id)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save(commit=False)
            _account_type = form.cleaned_data.get('account_type')
            profile = Profile.objects.get(user=account)
            profile.account_type = _account_type
            profile.save()
            form.save()
            messages.success(request, 'Account updated successfully.')
            return redirect('accounts')
    form = AccountForm(instance=account)
    context = {'segment': {'accounts', 'update', 'account_type'}, 'account': account, 'form': form}
    html_template = loader.get_template('home/account_mgmt/account_data.html')
    return HttpResponse(html_template.render(context, request))


def approve_credentials(request, id):
    account = User.objects.get(id=id)
    try:
        resident = home_models.Resident.objects.get(fname__iexact=account.first_name, lname__iexact=account.last_name)
    except home_models.Resident.DoesNotExist:
        resident = None
    if request.method == 'POST':
        account.is_active = True
        account.save()
        helper.send_email(account.email, 'Approved', 'Your Masili Portal account has been approved. You can now '
                                                     'logged in and access the services module on your portal',
                          account.first_name, "")
        messages.success(request, 'Account approved successfully.')
        return redirect('accounts')

    context = {'segment': {'accounts', 'acc_forApproval'}, 'account': account, 'resident': resident}
    print(context)
    html_template = loader.get_template('home/account_mgmt/account_data.html')
    return HttpResponse(html_template.render(context, request))


def account_forApproval(request):
    accounts = User.objects.filter(is_active=False)
    context = {'segment': {'accounts', 'acc_forApproval'}, 'accounts': accounts}
    html_template = loader.get_template('home/account_mgmt/accounts_list.html')
    return HttpResponse(html_template.render(context, request))