import math, random

import requests
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from core import settings


def send_email(email, subject, message, user_name, otp):
    subject = f'Masili Portal | {subject}'
    html_message = render_to_string('otp/mail_template.html', {'user_name': user_name, 'otp': otp, 'message': message})
    plain_message = strip_tags(html_message)
    mail_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, plain_message, mail_from, recipient_list, html_message=html_message, fail_silently=False)


###########################################################
# OTP Generator
###########################################################
def generate_otp():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name