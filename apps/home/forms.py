from django.forms import *
from . import models


class HotlineForm(ModelForm):
    class Meta:
        model = models.Hotline
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Directory Name'}),
            'phone_no1': TextInput(attrs={'class': 'form-control mob_no', 'placeholder': 'Phone Number 1'}),
            'phone_no2': TextInput(attrs={'class': 'form-control mob_no', 'placeholder': 'Phone Number 2'}),
            'tel_no': TextInput(attrs={'class': 'form-control', 'placeholder': 'Telephone Number'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        }


class BrgyOfficialForm(ModelForm):
    class Meta:
        model = models.BrgyOfficial
        fields = '__all__'
        widgets = {
            'fname': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'First Name'}),
            'mname': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Middle Name'}),
            'lname': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Last Name'}),
            'ext_name': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Ext'}),
            'position': TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'start_term': DateInput(attrs={'class': 'form-control', 'placeholder': 'Start Term', 'type': 'date'}),
            'end_term': DateInput(attrs={'class': 'form-control', 'placeholder': 'End Term', 'type': 'date'}),
            'photo': FileInput(attrs={'class': 'w-25', 'id':'official_photo_input', 'placeholder': 'Photo', 'style': 'display: none;'}),
        }


class OrganizationForm(ModelForm):
    class Meta:
        model = models.BrgyOrganization
        fields = '__all__'
        widgets = {
            'org_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),
            'org_description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


class OrgMemberForm(ModelForm):
    class Meta:
        model = models.OrgMember
        fields = ['member']
        widgets = {
            'member': Select(attrs={'class': 'form-control', 'placeholder': 'Member'}),
        }


class AnnouncementForm(ModelForm):
    class Meta:
        model = models.Announcement
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'content': Textarea(attrs={'class': 'form-control', 'placeholder': 'Content'}),
        }


class GalleryForm(ModelForm):
    class Meta:
        model = models.Gallery
        fields = '__all__'
        widgets = {
            'caption': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'photo': FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),
        }