from django.db import models
from django.contrib.auth.models import User
import os


class Purok(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BrgyOfficial(models.Model):
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50, blank=True)
    lname = models.CharField(max_length=50)
    ext_name = models.CharField(max_length=5, blank=True)
    position = models.CharField(max_length=50)
    start_term = models.DateField()
    end_term = models.DateField()
    photo = models.ImageField(upload_to='brgy_officials/', blank=True, default='brgy_officials/default.jpg')
    date_added = models.DateTimeField(auto_now_add=True)
    stat = (
        ['ACTIVE', 'ACTIVE'],
        ['INACTIVE', 'INACTIVE'],
    )
    status = models.CharField(max_length=10, choices=stat, default='active')

    def __str__(self):
        return self.fname + ' ' + self.lname

    def save(self, *args, **kwargs):
        self.fname = self.fname.upper()
        self.mname = self.mname.upper()
        self.lname = self.lname.upper()
        self.ext_name = self.ext_name.upper()
        self.position = self.position.upper()
        super(BrgyOfficial, self).save(*args, **kwargs)


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
    purok = models.ForeignKey(Purok, on_delete=models.CASCADE, blank=False, default=None)

    # Contact
    phone_no1 = models.CharField(max_length=11, blank=False, default=None)
    phone_no2 = models.CharField(max_length=11, blank=True)
    tel_no = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50, blank=True)

    # Other
    is_voter = models.BooleanField(default=False)
    is_household_head = models.BooleanField(default=False)

    def __str__(self):
        return self.fname + ' ' + self.lname

    def save(self, *args, **kwargs):
        self.fname = self.fname.upper()
        self.mname = self.mname.upper()
        self.lname = self.lname.upper()
        self.ext_name = self.ext_name.upper()
        self.religion = self.religion.upper()
        self.occupation = self.occupation.upper()
        self.address_line1 = self.address_line1.upper()
        if self.phone_no1[0:2] != '+63':
            self.phone_no1 = '+63' + self.phone_no1
        if self.phone_no2[0:2] != '+63':
            self.phone_no2 = '+63' + self.phone_no2
        super(Resident, self).save(*args, **kwargs)


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


class EmergencyContact(models.Model):
    res = models.ForeignKey(Resident, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50, blank=False)
    lname = models.CharField(max_length=50, blank=False)
    mname = models.CharField(max_length=50, blank=True)
    ext_name = models.CharField(max_length=5, blank=True)
    phone_no = models.CharField(max_length=11, blank=False, default=None)

    def __str__(self):
        return self.fname + ' ' + self.lname

    def save(self, *args, **kwargs):
        self.fname = self.fname.upper()
        self.mname = self.mname.upper()
        self.lname = self.lname.upper()
        self.ext_name = self.ext_name.upper()
        super(EmergencyContact, self).save(*args, **kwargs)


# BLOTTERS
class Blotter(models.Model):
    blotter_no = models.AutoField(primary_key=True)
    incident_type = models.CharField(max_length=50, blank=False)
    datetimeReported = models.DateTimeField(auto_now_add=True)
    dateOfIncident = models.DateField(blank=False)
    placeOfIncident = models.CharField(max_length=50, blank=False)
    hearingDate = models.DateField(blank=False)
    hearingTime = models.TimeField(blank=False)
    status = models.CharField(max_length=50, blank=False)
    narrative = models.TextField(blank=False)
    recordedBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.blotter_no

    def save(self, *args, **kwargs):
        self.incident_type = self.incident_type.upper()
        self.placeOfIncident = self.placeOfIncident.upper()
        self.status = self.status.upper()
        super(Blotter, self).save(*args, **kwargs)


class Complainant(models.Model):
    blotter_no = models.ForeignKey(Blotter, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50, blank=False)
    lname = models.CharField(max_length=50, blank=False)
    mname = models.CharField(max_length=50, blank=True)
    ext_name = models.CharField(max_length=5, blank=True)
    contact = models.CharField(max_length=11, blank=False)
    address = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.blotter_no

    def save(self, *args, **kwargs):
        self.fname = self.fname.upper()
        self.mname = self.mname.upper()
        self.lname = self.lname.upper()
        self.ext_name = self.ext_name.upper()
        self.address = self.address.upper()
        super(Complainant, self).save(*args, **kwargs)


class Respondent(models.Model):
    blotter_no = models.ForeignKey(Blotter, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50, blank=False)
    lname = models.CharField(max_length=50, blank=False)
    mname = models.CharField(max_length=50, blank=True)
    ext_name = models.CharField(max_length=5, blank=True)
    contact = models.CharField(max_length=11, blank=False)
    address = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.blotter_no

    def save(self, *args, **kwargs):
        self.fname = self.fname.upper()
        self.mname = self.mname.upper()
        self.lname = self.lname.upper()
        self.ext_name = self.ext_name.upper()
        self.address = self.address.upper()
        super(Respondent, self).save(*args, **kwargs)


class Witness(models.Model):
    blotter_no = models.ForeignKey(Blotter, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50, blank=False)
    lname = models.CharField(max_length=50, blank=False)
    mname = models.CharField(max_length=50, blank=True)
    ext_name = models.CharField(max_length=5, blank=True)
    contact = models.CharField(max_length=11, blank=False)
    address = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.blotter_no

    def save(self, *args, **kwargs):
        self.fname = self.fname.upper()
        self.mname = self.mname.upper()
        self.lname = self.lname.upper()
        self.ext_name = self.ext_name.upper()
        self.address = self.address.upper()
        super(Witness, self).save(*args, **kwargs)


# ANNOUNCEMENTS
class Announcement(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    stat = (
        ['SENT', 'SENT'],
        ['PENDING', 'PENDING'],
    )
    status = models.CharField(max_length=50, choices=stat, default='PENDING')
    send_to = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.upper()
        user = User.objects.get(username=self.request.user)
        self.posted_by = user.first_name + ' ' + user.last_name
        super(Announcement, self).save(*args, **kwargs)



class Gallery(models.Model):
    caption = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='gallery/', blank=False)

    def __str__(self):
        return str(self.id)


    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'


