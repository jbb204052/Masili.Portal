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
        fields = ['photo']

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


class HearingForm(ModelForm):
    class Meta:
        model = models.Hearing
        fields = ['remarks', 'status', 'files']
        widgets = {
            'remarks': TinyMCE(attrs={'class': 'form-control', 'placeholder': 'Remarks'}),
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'files': FileInput(attrs={'class': 'form-control', 'placeholder': 'Files'}),
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


class NewsForm(ModelForm):
    class Meta:
        model = models.News
        fields = ['title', 'content', 'front_image']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'content': TinyMCE(attrs={'class': 'form-control', 'placeholder': 'Content'}),
            'front_image': FileInput(attrs={'class': 'form-control', 'id': 'front_image', 'hidden': 'true'}),
        }


class BusinessPermitForm(ModelForm):
    class Meta:
        model = models.BusinessPermit
        fields = '__all__'
        exclude = ['date_issued', 'business_no', 'signed_permits', 'chairman', 'type']
        widgets = {
            'business_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}),
            'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'classification': TextInput(attrs={'class': 'form-control', 'placeholder': 'Classification'}),
            'owner': TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner'}),
            'residence_certificate_number': TextInput(attrs={'class': 'form-control', 'placeholder': 'Residence Certificate Number'}),
            'capital_investment': TextInput(attrs={'class': 'form-control', 'placeholder': 'Capital Investment'}),

            'gross_sales_or_receipts': TextInput(attrs={'class': 'form-control', 'placeholder': 'Gross Sales or Receipts'}),
            'previous_OR_number': TextInput(attrs={'class': 'form-control', 'placeholder': 'Previous OR Number'}),
            'date_issued1': DateInput(attrs={'class': 'form-control', 'placeholder': 'Date Issued', 'type': 'date'}),
            'amount_to_collect': TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount to Collect'}),
            'paid_OR_number': TextInput(attrs={'class': 'form-control', 'placeholder': 'Paid OR Number'}),
            'date_issued2': DateInput(attrs={'class': 'form-control', 'placeholder': 'Date Issued', 'type': 'date'}),
            'amount_collected': TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount Collected'}),
            'status': Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
        }


class BusinessClosureForm(ModelForm):
    class Meta:
        model = models.BusinessClosure
        fields = '__all__'
        exclude = ['date_issued', 'signed_permits', 'chairman', 'type', 'status', 'transaction_no']
        widgets = {
            'business_name': Select(attrs={'class': 'form-control', 'placeholder': 'Business Name', 'id': 'business_name'}),
            'date_closed': DateInput(attrs={'class': 'form-control', 'placeholder': 'Date Closed', 'type': 'date'}),
            'reason': TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason'}),
        }