from datetime import datetime

from django.forms import *
from . import models
from tinymce.widgets import TinyMCE


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
            'provisions': TinyMCE(attrs={'class': 'form-control', 'placeholder': 'Content', 'cols': 30, 'rows': 10}),
            'files': ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Files', 'multiple': True}),
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'attested_by': Textarea(attrs={'class': 'form-control', 'placeholder': 'Attested By', 'rows': 3}),
        }


class ResidentForm(ModelForm):
    class Meta:
        model = models.Resident
        fields = ['fname', 'lname', 'mname', 'ext_name', 'bdate', 'gender', 'civil_status', 'religion', 'occupation', 'address_line1', 'purok', 'phone_no1', 'phone_no2', 'tel_no', 'email', 'photo', 'resident_since', 'status']
        widgets = {
            'fname': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'First Name'}),
            'lname': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Last Name'}),
            'mname': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Middle Name'}),
            'ext_name': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Ext'}),
            'bdate': DateInput(attrs={'class': 'form-control', 'placeholder': 'Birth Date', 'type': 'date'}),
            'gender': Select(attrs={'class': 'form-control', 'placeholder': 'Gender'}),
            'civil_status': Select(attrs={'class': 'form-control', 'placeholder': 'Civil Status'}),
            'religion': TextInput(attrs={'class': 'form-control', 'placeholder': 'Religion'}),
            'occupation': TextInput(attrs={'class': 'form-control', 'placeholder': 'Occupation'}),
            'address_line1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'purok': Select(attrs={'class': 'form-control', 'placeholder': 'Purok'}),
            'phone_no1': TextInput(attrs={'class': 'form-control mob_no', 'placeholder': 'Phone Number 1'}),
            'phone_no2': TextInput(attrs={'class': 'form-control mob_no', 'placeholder': 'Phone Number 2'}),
            'tel_no': TextInput(attrs={'class': 'form-control tel_no', 'placeholder': 'Telephone Number'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'photo': FileInput(attrs={'class': 'w-25', 'id':'resident_photo_input', 'placeholder': 'Photo', 'hidden': 'true'}),
            'resident_since': DateInput(attrs={'class': 'form-control', 'placeholder': 'Resident Since', 'type': 'date'}),
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Residency Status'}),
        }


# class EmergencyContactForm(ModelForm):
#     class Meta:
#         model = models.EmergencyContact
#         fields = ['name', 'relationship', 'phone_no', 'address']
#         widgets = {
#             'name': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Name'}),
#             'relationship': TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship'}),
#             'phone_no': TextInput(attrs={'class': 'form-control mob_no', 'placeholder': 'Phone Number'}),
#             'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
#         }
#

class BlotterForm(ModelForm):
    class Meta:
        model = models.Blotter
        fields = ['incident_type', 'dateOfIncident', 'placeOfIncident', 'hearingDate', 'hearingTime', 'status', 'narrative']
        widgets = {
            'incident_type': TextInput(attrs={'class': 'form-control', 'placeholder': 'Incident Type'}),
            'dateOfIncident': DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Date of Incident', 'type': 'datetime-local'}),
            'placeOfIncident': TextInput(attrs={'class': 'form-control', 'placeholder': 'Place of Incident'}),
            'hearingDate': DateInput(attrs={'class': 'form-control', 'placeholder': 'Hearing Date', 'type': 'date'}),
            'hearingTime': TimeInput(attrs={'class': 'form-control', 'placeholder': 'Hearing Time', 'type': 'time'}),
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'narrative': TinyMCE(attrs={'class': 'form-control', 'placeholder': 'Narrative'}),
        }


class ComplainantForm(ModelForm):
    class Meta:
        model = models.Complainant
        fields = ['full_name', 'contact', 'address']
        widgets = {
            'full_name': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Fullname'}),
            'contact': TextInput(attrs={'class': 'form-control mob_no', 'placeholder': 'Contact'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        }


class RespondentForm(ModelForm):
    class Meta:
        model = models.Respondent
        fields = ['full_name', 'contact', 'address']
        widgets = {
            'full_name': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Fullname'}),
            'contact': TextInput(attrs={'class': 'form-control mob_no', 'placeholder': 'Contact'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        }


class SessionForm(ModelForm):
    class Meta:
        model = models.Session
        fields = ['session_date', 'session_start', 'session_end', 'attendees', 'other_attendees', 'minutes_of_meeting', 'agenda']
        widgets = {
            'session_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Session Date', 'type': 'date', 'id': 'sessionDate'}),
            'session_start': TimeInput(attrs={'class': 'form-control', 'placeholder': 'Session Start', 'type': 'time'}),
            'session_end': TimeInput(attrs={'class': 'form-control', 'placeholder': 'Session End', 'type': 'time'}),
            'attendees': TextInput(attrs={'class': 'form-control', 'placeholder': 'Attendees', 'id': 'attendees', 'readonly': 'readonly', 'hidden': 'true'}),
            'other_attendees': TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Attendees'}),
            'minutes_of_meeting': TinyMCE(attrs={'class': 'form-control', 'placeholder': 'Minutes of Meeting'}),
            'agenda': TextInput(attrs={'class': 'form-control', 'placeholder': 'Agenda'}),
        }


class CertificateRequestForm(ModelForm):
    class Meta:
        model = models.CertificateRequest
        fields = ['purpose', 'requestor', 'status']
        widgets = {
            # 'full_name': TextInput(attrs={'class': 'form-control text_input', 'placeholder': 'Fullname', 'id': 'fullname', "list":"cert_fullname_list", 'autocomplete':'off'}),
            'purpose': TextInput(attrs={'class': 'form-control', 'placeholder': 'Purpose'}),
            'requestor': TextInput(attrs={'class': 'form-control', 'placeholder': 'Requestor', 'id':'requestor'}),
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
        }


class OfficialForm(ModelForm):
    class Meta:
        model = models.BarangayOfficial
        fields = ['position', 'date_appointed', 'end_term', 'status']
        widgets = {
            'position': TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'date_appointed': DateInput(attrs={'class': 'form-control', 'placeholder': 'Date Appointed', 'type': 'date'}),
            'end_term': DateInput(attrs={'class': 'form-control', 'placeholder': 'End Term', 'type': 'date'}),
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
        }



