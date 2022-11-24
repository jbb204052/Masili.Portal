from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from apps.authentication import models


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "form-control"
            }
        ))


    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')


class OTPEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
            }
        )
    )


class OTPForm(forms.Form):
    otp = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control num_input",
                "placeholder": "OTP",
            }
        )
    )


class PasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))


class ChangeAccountType(ModelForm):
    class Meta:
        model = models.Profile
        fields = ['is_resident', 'is_admin', 'is_superadmin']
        widgets = {
            'is_resident': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'is_admin': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'is_superadmin': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }
