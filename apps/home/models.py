from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
import os

from notifications.models import notify_handler, Notification
from notifications.signals import notify

from tinymce.models import HTMLField

from auditlog.registry import auditlog


def file_path(path):
    def _func(instance, filename):
        return os.path.join(path + str(instance.id), filename)
    # return _func


def photo_path(path):
    def _func(instance, filename):
        return os.path.join(path, str(instance.id) + '.png')
    # return _func


class NotificationsCTA(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, blank=False, default=None)
    cta_link = models.CharField(max_length=255, blank=True, default=None)

    def __str__(self):
        return str(self.cta_link)


def notify_handler(*args, **kwargs):
    notifications = notify_handler(*args, **kwargs)
    cta_link = kwargs.get('cta_link', '')
    for notification in notifications:
        NotificationsCTA.objects.create(notification=notification, cta_link=cta_link)
    return notifications


notify.disconnect(notify_handler, dispatch_uid='notifications.models.notification')
notify.connect(notify_handler, dispatch_uid='notifications.models.notification')

# class Purok(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         self.name = self.name.upper()
#         super(Purok, self).save(*args, **kwargs)
#


Purok = (
    ['PUROK 1', 'PUROK 1'],
    ['PUROK 2', 'PUROK 2'],
    ['PUROK 3', 'PUROK 3'],
    ['PUROK 4', 'PUROK 4'],
    ['PUROK 5', 'PUROK 5'],
    ['PUROK 6', 'PUROK 6'],
)


class Hotline(models.Model):
    name = models.CharField(max_length=50, unique=True)
    phone_no1 = models.CharField(max_length=11, blank=False, default=None)
    phone_no2 = models.CharField(max_length=11, blank=True)
    tel_no = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.address = self.address.upper()
        super(Hotline, self).save(*args, **kwargs)


class Resident(models.Model):
    res_id = models.CharField(max_length=50, default='MASILI-RES-ID-000000')
    fname = models.CharField(max_length=50, blank=False)
    lname = models.CharField(max_length=50, blank=False)
    mname = models.CharField(max_length=50, blank=True)
    ext_name = models.CharField(max_length=5, blank=True)
    bdate = models.DateField(blank=False)
    genders = (
        ['MALE', 'MALE'],
        ['FEMALE', 'FEMALE']
    )
    gender = models.CharField(max_length=10, choices=genders, blank=False, default='MALE')
    stat = (
        ['SINGLE', 'SINGLE'],
        ['MARRIED', 'MARRIED'],
        ['WIDOWED', 'WIDOWED'],
        ['SEPARATED', 'SEPARATED'],
        ['DIVORCED', 'DIVORCED'],
    )
    civil_status = models.CharField(max_length=10, choices=stat, blank=False, default='SINGLE')
    religion = models.CharField(max_length=50, blank=False)
    occupation = models.CharField(max_length=50, blank=False, default=None)

    # Address
    address_line1 = models.CharField(max_length=50, blank=False, default=None)
    purok = models.CharField(max_length=50, choices=Purok, blank=False, default='PUROK 1')

    # Contact
    phone_no1 = models.CharField(max_length=11, blank=False, default=None)
    phone_no2 = models.CharField(max_length=11, blank=True)
    tel_no = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    photo = models.ImageField(upload_to=photo_path('residents'), blank=True, default='residents/avatar.png')
    resident_since = models.DateField(blank=False, default=None)
    date_added = models.DateTimeField(auto_now_add=True)

    stat_1 = (
        ['RESIDING', 'RESIDING'],
        ['MOVED OUT', 'MOVED OUT'],
    )
    status = models.CharField(max_length=10, choices=stat_1, default='RESIDING')
    fullname = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('fname', 'lname', 'mname', 'ext_name', 'bdate')

    def __str__(self):
        return self.fname + ' ' + self.mname + ' ' + self.lname + ' ' + self.ext_name

    def save(self, *args, **kwargs):
        self.fname = self.fname.upper()
        self.mname = self.mname.upper()
        self.lname = self.lname.upper()
        self.ext_name = self.ext_name.upper()
        self.religion = self.religion.upper()
        self.occupation = self.occupation.upper()
        self.address_line1 = self.address_line1.upper()
        self.fullname = self.fname + ' ' + self.mname + ' ' + self.lname + ' ' + self.ext_name
        if self.phone_no1[0:2] != '+63':
            self.phone_no1 = '+63' + self.phone_no1
        if self.phone_no2 != '':
            if self.phone_no2[0:2] != '+63':
                self.phone_no2 = '+63' + self.phone_no2
        super(Resident, self).save(*args, **kwargs)

    @property
    def get_fullname(self):
        return self.fname + ' ' + self.mname + ' ' + self.lname + ' ' + self.ext_name


# class EmergencyContact(models.Model):
#     resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     relationship = models.CharField(max_length=50)
#     phone_no = models.CharField(max_length=11, blank=False, default=None)
#     address = models.CharField(max_length=255, blank=False)
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         self.name = self.name.upper()
#         self.relationship = self.relationship.upper()
#         self.address = self.address.upper()
#         super(EmergencyContact, self).save(*args, **kwargs)


# RECOGNIZED ORGANIZATIONS
class BrgyOrganization(models.Model):
    org_name = models.CharField(max_length=50, blank=False, unique=True)
    org_description = models.CharField(max_length=100, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.org_name

    def save(self, *args, **kwargs):
        self.org_name = self.org_name.upper()
        self.org_description = self.org_description.upper()
        super(BrgyOrganization, self).save(*args, **kwargs)


class OrgMember(models.Model):
    org = models.ForeignKey(BrgyOrganization, on_delete=models.CASCADE, blank=False, default=None)
    member = models.ForeignKey(Resident, on_delete=models.CASCADE, blank=False, default=None)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.org.org_name + ' - ' + self.member.fname + ' ' + self.member.lname

    class Meta:
        unique_together = ('org', 'member')


# BLOTTERS
class Blotter(models.Model):
    blotter_no = models.CharField(max_length=50, default='MASILI-BLOTTER-000000')
    incident_type = models.CharField(max_length=50, blank=False)
    datetimeReported = models.DateTimeField(auto_now_add=True)
    dateOfIncident = models.DateTimeField(blank=False)
    placeOfIncident = models.CharField(max_length=50, blank=False)
    hearingDate = models.DateField(blank=False)
    hearingTime = models.TimeField(blank=False)
    _stat = (
        ['PENDING', 'PENDING'],
        ['RESOLVED', 'RESOLVED'],
    )
    status = models.CharField(max_length=50, choices=_stat, default='PENDING')
    narrative = HTMLField(blank=False)
    recordedBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.blotter_no

    def save(self, *args, **kwargs):
        self.incident_type = self.incident_type.upper()
        self.placeOfIncident = self.placeOfIncident.upper()
        self.status = self.status.upper()
        super(Blotter, self).save(*args, **kwargs)


class Complainant(models.Model):
    blotter = models.ForeignKey(Blotter, on_delete=models.CASCADE, blank=False, default=None)
    full_name = models.CharField(max_length=50, blank=False)
    contact = models.CharField(max_length=11, blank=False)
    address = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return str(self.blotter)

    def save(self, *args, **kwargs):
        self.full_name = self.full_name.upper()
        self.address = self.address.upper()
        super(Complainant, self).save(*args, **kwargs)


class Respondent(models.Model):
    blotter = models.ForeignKey(Blotter, on_delete=models.CASCADE, blank=False, default=None)
    full_name = models.CharField(max_length=50, blank=False)
    contact = models.CharField(max_length=11, blank=False)
    address = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return str(self.blotter)

    def save(self, *args, **kwargs):
        self.full_name = self.full_name.upper()
        self.address = self.address.upper()
        super(Respondent, self).save(*args, **kwargs)


class Hearing(models.Model):
    blotter = models.ForeignKey(Blotter, on_delete=models.CASCADE, blank=False, default=None)
    hearing_no = models.CharField(max_length=50, default='1')
    date = models.DateTimeField(blank=False, auto_now_add=True)
    _stat = (
        ['PENDING', 'PENDING'],
        ['RESOLVED', 'RESOLVED'],
    )
    status = models.CharField(max_length=50, choices=_stat, default='PENDING')
    remarks = HTMLField(blank=False)
    files = models.FileField(upload_to='blotter_files/', blank=True, null=True)

    def __str__(self):
        return str(self.blotter) + ' | ' + self.hearing_no

    def save(self, *args, **kwargs):
        self.status = self.status.upper()
        super(Hearing, self).save(*args, **kwargs)


# ANNOUNCEMENTS
class Announcement(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.CharField(max_length=50, blank=False)
    stat = (
        ['APPROVED', 'APPROVED'],
        ['PENDING', 'PENDING'],
    )
    status = models.CharField(max_length=50, choices=stat, default='PENDING')
    send_to = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.upper()
        super(Announcement, self).save(*args, **kwargs)


class Gallery(models.Model):
    photo = models.ImageField(upload_to='gallery/', blank=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'


class Ordinance(models.Model):
    ordinance_no = models.CharField(max_length=50, blank=False)
    title = models.CharField(max_length=255, blank=False)
    provisions = HTMLField(blank=False)
    presiding_officer = models.CharField(max_length=50, blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.CharField(max_length=50, blank=False)
    files = models.FileField(upload_to=file_path('ordinances/'), blank=True, default=None)
    stat = (
        ['ACTIVE', 'ACTIVE'],
        ['EXPIRED', 'EXPIRED'],
    )
    status = models.CharField(max_length=50, choices=stat, default='ACTIVE')
    attested_by = models.TextField(blank=True)
    signed_ordinance = models.FileField(upload_to=file_path('ordinances/'), blank=True, default=None, null=True)
    active_chairman = models.CharField(max_length=50, blank=True, default=None, null=True)

    def __str__(self):
        return self.ordinance_no

    def save(self, *args, **kwargs):
        self.ordinance_no = self.ordinance_no.upper()
        self.title = self.title.upper()
        super(Ordinance, self).save(*args, **kwargs)


# SESSIONS
class Session(models.Model):
    session_no = models.CharField(max_length=50, blank=False)
    session_date = models.DateField(blank=False)
    session_start = models.TimeField(blank=False)
    session_end = models.TimeField(blank=False)
    attendees = models.TextField(blank=False)
    other_attendees = models.TextField(blank=True)
    agenda = models.TextField(blank=False)
    minutes_of_meeting = HTMLField(blank=False)

    def __str__(self):
        return self.session_no


class CertificateRequest(models.Model):
    transaction_number = models.CharField(max_length=50)
    certs = (
        ['INDIGENCY', 'INDIGENCY'],
        ['LIVE IN', 'LIVE IN'],
    )
    certificate_type = models.CharField(max_length=50, choices=certs, default='INDIGENCY')
    full_name = models.ForeignKey(Resident, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=50)
    request_date = models.DateTimeField(auto_now_add=True)
    date_printed = models.DateField(blank=True, null=True)
    date_issued = models.DateField(blank=True, null=True)
    requestor = models.CharField(max_length=50)
    stat = (
        ['PENDING', 'PENDING'],
        ['PROCESSED', 'PROCESSED'],
        ['ISSUED', 'ISSUED'],
    )
    status = models.CharField(max_length=50, choices=stat, default='PENDING')
    signed_certificates = models.FileField(upload_to=file_path('certificates/'), blank=True, default=None, null=True)
    method = (
        ['ONLINE', 'ONLINE'],
        ['WALK IN', 'WALK IN']
    )
    request_method = models.CharField(max_length=50, choices=method, default='WALK IN')
    chairman = models.CharField(max_length=50, blank=True, default=None, null=True)

    def __str__(self):
        return self.transaction_number


class Certificate(models.Model):
    transaction_number = models.CharField(max_length=50)
    certs = (
        ['INDIGENCY', 'INDIGENCY'],
        ['LIVE IN', 'LIVE IN'],
    )
    certificate_type = models.CharField(max_length=50, choices=certs, default='INDIGENCY')
    request_date = models.DateTimeField(auto_now_add=True)
    date_printed = models.DateField(blank=True, null=True)
    date_issued = models.DateField(blank=True, null=True)
    stat = (
        ['PENDING', 'PENDING'],
        ['PRINTED', 'PRINTED'],
        ['ISSUED', 'ISSUED'],
    )
    status = models.CharField(max_length=50, choices=stat, default='PENDING')
    attachment = models.FileField(upload_to=file_path('certificates/'), blank=True, default=None, null=True)

    def __str__(self):
        return self.transaction_number


class certificate_of_indigency(models.Model):
    transaction_number = models.ForeignKey(CertificateRequest, on_delete=models.CASCADE)
    full_name = models.ForeignKey(Resident, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=50, null=True)
    requestor = models.CharField(max_length=50)

    def __str__(self):
        return self.transaction_number.transaction_number


class certfiticate_of_live_in(models.Model):
    transaction_number = models.ForeignKey(CertificateRequest, on_delete=models.CASCADE)
    name_1 = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='name_1')
    name_2 = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='name_2')
    relationship = models.CharField(max_length=50, null=True)
    live_in_since = models.DateField(null=False)

    def __str__(self):
        return self.transaction_number.transaction_number


class BarangayOfficial(models.Model):
    fullname = models.ForeignKey(Resident, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    date_appointed = models.DateField(blank=False)
    end_term = models.DateField(blank=True, null=True)
    stat = (
        ['ACTIVE', 'ACTIVE'],
        ['INACTIVE', 'INACTIVE'],
    )
    status = models.CharField(max_length=50, choices=stat, default='ACTIVE')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('fullname', 'position', 'date_appointed', 'end_term', 'status')

    def __str__(self):
        return self.fullname.fullname

    def save(self, *args, **kwargs):
        self.position = self.position.upper()
        super(BarangayOfficial, self).save(*args, **kwargs)


class News(models.Model):
    title = models.CharField(max_length=50)
    front_image = models.ImageField(upload_to=file_path('news/'), blank=True, default=None, null=True)
    content = HTMLField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    posted_by = models.CharField(max_length=50)
    status = (
        ['PUBLISHED', 'PUBLISHED'],
        ['DRAFT', 'DRAFT'],
    )
    post_status = models.CharField(max_length=50, choices=status, default='DRAFT')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.upper()
        super(News, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'News'


class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_for = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class BusinessPermit(models.Model):
    business_no = models.CharField(max_length=50, blank=False)
    business_name = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50, blank=False)
    classification = models.CharField(max_length=50, blank=False)
    owner = models.CharField(max_length=50, blank=False)
    residence_certificate_number = models.CharField(max_length=50, blank=False)
    date_issued = models.DateField(auto_now_add=True)
    capital_investment = models.CharField(max_length=50, blank=False)
    gross_sales_or_receipts = models.CharField(max_length=50, blank=False)

    previous_OR_number = models.CharField(max_length=50, blank=False)
    date_issued1 = models.DateField()
    amount_to_collect = models.CharField(max_length=50, blank=False)
    paid_OR_number = models.CharField(max_length=50, blank=False)
    date_issued2 = models.DateField()
    amount_collected = models.CharField(max_length=50, blank=False)
    chairman = models.CharField(max_length=50)
    stat = (
        ['PENDING', 'PENDING'],
        ['PRINTED', 'PRINTED'],
        ['ISSUED', 'ISSUED'],
    )
    status = models.CharField(max_length=50, choices=stat, default='PENDING')
    signed_permits = models.FileField(upload_to=file_path('business_permit/'), blank=True, default=None, null=True)
    type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.business_name)


class BusinessClosure(models.Model):
    transaction_no = models.CharField(max_length=50, blank=False)
    business_name = models.ForeignKey(BusinessPermit, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50)
    date_closed = models.DateField(blank=False)
    date_issued = models.DateField(auto_now_add=True)
    stat = (
        ['PENDING', 'PENDING'],
        ['PRINTED', 'PRINTED'],
        ['ISSUED', 'ISSUED'],
    )
    status = models.CharField(max_length=50, choices=stat, default='CLOSED')
    chairman = models.CharField(max_length=50)
    signed_permits = models.FileField(upload_to=file_path('business_closure/'), blank=True, default=None, null=True)
    type = models.CharField(max_length=50)

    def __str__(self):
        return str(self.business_name)
