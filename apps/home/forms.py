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
            'position': TextInput(attrs={'class': 'form-control', 'placeholder': 'Position', 'name': 'position'}),
            'start_term': DateInput(attrs={'class': 'form-control', 'placeholder': 'Start Term', 'type': 'date', 'name': 'start_term'}),
            'end_term': DateInput(attrs={'class': 'form-control', 'placeholder': 'End Term', 'type': 'date', 'name': 'end_term'}),
            'photo': FileInput(attrs={'class': 'w-25', 'id':'official_photo_input', 'placeholder': 'Photo', 'style': 'display: none;'}),
            'status': Select(attrs={'class': 'form-control'}),
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
        fields = ['title', 'content']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'content': Textarea(attrs={'class': 'form-control', 'placeholder': 'Content'}),
            # 'send_to': Select(attrs={'class': 'form-control', 'placeholder': 'Send To'}),
        }


class GalleryForm(ModelForm):
    class Meta:
        model = models.Gallery
        fields = '__all__'
        widgets = {
            'caption': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'photo': FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),
        }


class OrdinanceForm(ModelForm):
    class Meta:
        model = models.Ordinance
        fields = ('title', 'provisions', 'files', 'status', 'attested_by')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'provisions': Textarea(attrs={'class': 'form-control', 'placeholder': 'Content'}),
            'files': ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Files', 'multiple': True}),
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'attested_by': Textarea(attrs={'class': 'form-control', 'placeholder': 'Attested By', 'rows': 3}),
        }


class Residents(ModelForm):
    class Meta:
        model = models.Resident
        fields = ['fname', 'lname', 'mname', 'ext_name', 'bdate', 'gender', 'civil_status', 'religion', 'occupation', 'address_line1', 'purok', 'phone_no1', 'phone_no2', 'tel_no', 'email', 'photo']
        widgets = {
            'fname': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'lname': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'mname': TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'ext_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ext'}),
            'bdate': DateInput(attrs={'class': 'form-control', 'placeholder': 'Birth Date', 'type': 'date'}),
            'gender': Select(attrs={'class': 'form-control', 'placeholder': 'Gender'}),
            'civil_status': Select(attrs={'class': 'form-control', 'placeholder': 'Civil Status'}),
            'religion': Select(attrs={'class': 'form-control', 'placeholder': 'Religion'}),
            'occupation': TextInput(attrs={'class': 'form-control', 'placeholder': 'Occupation'}),
            'address_line1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'purok': Select(attrs={'class': 'form-control', 'placeholder': 'Purok'}),
            'phone_no1': TextInput(attrs={'class': 'form-control mob_no', 'placeholder': 'Phone Number 1'}),
            'phone_no2': TextInput(attrs={'class': 'form-control mob_no', 'placeholder': 'Phone Number 2'}),
            'tel_no': TextInput(attrs={'class': 'form-control tel_no', 'placeholder': 'Telephone Number'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'photo': FileInput(attrs={'class': 'w-25', 'id':'resident_photo_input', 'placeholder': 'Photo' }),
        }