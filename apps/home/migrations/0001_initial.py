# Generated by Django 4.1.3 on 2022-12-10 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.NOTIFICATIONS_NOTIFICATION_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[['APPROVED', 'APPROVED'], ['PENDING', 'PENDING']], default='PENDING', max_length=50)),
                ('send_to', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Blotter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blotter_no', models.CharField(default='MASILI-BLOTTER-000000', max_length=50)),
                ('incident_type', models.CharField(max_length=50)),
                ('datetimeReported', models.DateTimeField(auto_now_add=True)),
                ('dateOfIncident', models.DateTimeField()),
                ('placeOfIncident', models.CharField(max_length=50)),
                ('hearingDate', models.DateField()),
                ('hearingTime', models.TimeField()),
                ('status', models.CharField(choices=[['PENDING', 'PENDING'], ['RESOLVED', 'RESOLVED']], default='PENDING', max_length=50)),
                ('narrative', tinymce.models.HTMLField()),
                ('recordedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BrgyOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=50, unique=True)),
                ('org_description', models.CharField(max_length=100)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_number', models.CharField(max_length=50)),
                ('certificate_type', models.CharField(choices=[['INDIGENCY', 'INDIGENCY'], ['LIVE IN', 'LIVE IN']], default='INDIGENCY', max_length=50)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('date_printed', models.DateField(blank=True, null=True)),
                ('date_issued', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[['PENDING', 'PENDING'], ['PROCESSED', 'PROCESSED'], ['ISSUED', 'ISSUED']], default='PENDING', max_length=50)),
                ('attachment', models.FileField(blank=True, default=None, null=True, upload_to=None)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=50)),
                ('photo', models.ImageField(upload_to='gallery/')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Gallery',
                'verbose_name_plural': 'Gallery',
            },
        ),
        migrations.CreateModel(
            name='Hotline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('phone_no1', models.CharField(default=None, max_length=11)),
                ('phone_no2', models.CharField(blank=True, max_length=11)),
                ('tel_no', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ordinance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordinance_no', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=255)),
                ('provisions', tinymce.models.HTMLField()),
                ('presiding_officer', models.CharField(max_length=50)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.CharField(max_length=50)),
                ('files', models.FileField(blank=True, default=None, upload_to=None)),
                ('status', models.CharField(choices=[['ACTIVE', 'ACTIVE'], ['EXPIRED', 'EXPIRED']], default='ACTIVE', max_length=50)),
                ('attested_by', models.TextField(blank=True)),
                ('signed_ordinance', models.FileField(blank=True, default=None, null=True, upload_to=None)),
                ('active_chairman', models.CharField(blank=True, default=None, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_no', models.CharField(max_length=50)),
                ('session_date', models.DateField()),
                ('session_start', models.TimeField()),
                ('session_end', models.TimeField()),
                ('attendees', models.TextField()),
                ('other_attendees', models.TextField(blank=True)),
                ('agenda', models.TextField()),
                ('minutes_of_meeting', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='Respondent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('ext_name', models.CharField(blank=True, max_length=5)),
                ('contact', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=50)),
                ('blotter_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.blotter')),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_id', models.CharField(default='MASILI-RES-ID-000000', max_length=50)),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('mname', models.CharField(blank=True, max_length=50)),
                ('ext_name', models.CharField(blank=True, max_length=5)),
                ('bdate', models.DateField()),
                ('gender', models.CharField(choices=[['MALE', 'MALE'], ['FEMALE', 'FEMALE']], default='MALE', max_length=10)),
                ('civil_status', models.CharField(choices=[['SINGLE', 'SINGLE'], ['MARRIED', 'MARRIED'], ['WIDOWED', 'WIDOWED'], ['SEPARATED', 'SEPARATED'], ['DIVORCED', 'DIVORCED']], default='SINGLE', max_length=10)),
                ('religion', models.CharField(max_length=50)),
                ('occupation', models.CharField(default=None, max_length=50)),
                ('address_line1', models.CharField(default=None, max_length=50)),
                ('purok', models.CharField(choices=[['PUROK 1', 'PUROK 1'], ['PUROK 2', 'PUROK 2'], ['PUROK 3', 'PUROK 3'], ['PUROK 4', 'PUROK 4'], ['PUROK 5', 'PUROK 5'], ['PUROK 6', 'PUROK 6']], default='PUROK 1', max_length=50)),
                ('phone_no1', models.CharField(default=None, max_length=11)),
                ('phone_no2', models.CharField(blank=True, max_length=11)),
                ('tel_no', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('photo', models.ImageField(blank=True, default='residents/avatar.png', upload_to=None)),
                ('resident_since', models.DateField(default=None)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[['RESIDING', 'RESIDING'], ['MOVED OUT', 'MOVED OUT']], default='RESIDING', max_length=10)),
                ('fullname', models.CharField(blank=True, max_length=100, null=True)),
                ('is_approved', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('fname', 'lname', 'mname', 'ext_name', 'bdate')},
            },
        ),
        migrations.CreateModel(
            name='NotificationsCTA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cta_link', models.CharField(blank=True, default=None, max_length=255)),
                ('notification_type', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('notification', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.NOTIFICATIONS_NOTIFICATION_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hearing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(choices=[['PENDING', 'PENDING'], ['RESOLVED', 'RESOLVED']], default='PENDING', max_length=50)),
                ('remarks', tinymce.models.HTMLField(blank=True, max_length=50)),
                ('files', models.FileField(blank=True, upload_to='blotter_files/')),
                ('blotter_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.blotter')),
            ],
        ),
        migrations.CreateModel(
            name='Complainant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=50)),
                ('blotter_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.blotter')),
            ],
        ),
        migrations.CreateModel(
            name='CertificateRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_number', models.CharField(max_length=50)),
                ('certificate_type', models.CharField(choices=[['INDIGENCY', 'INDIGENCY'], ['LIVE IN', 'LIVE IN']], default='INDIGENCY', max_length=50)),
                ('purpose', models.CharField(max_length=50)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('date_printed', models.DateField(blank=True, null=True)),
                ('date_issued', models.DateField(blank=True, null=True)),
                ('requestor', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[['PENDING', 'PENDING'], ['PROCESSED', 'PROCESSED'], ['ISSUED', 'ISSUED']], default='PENDING', max_length=50)),
                ('signed_certificates', models.FileField(blank=True, default=None, null=True, upload_to=None)),
                ('request_method', models.CharField(choices=[['ONLINE', 'ONLINE'], ['WALK IN', 'WALK IN']], default='WALK IN', max_length=50)),
                ('full_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.resident')),
            ],
        ),
        migrations.CreateModel(
            name='certificate_of_indigency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(max_length=50, null=True)),
                ('requestor', models.CharField(max_length=50)),
                ('full_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.resident')),
                ('transaction_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.certificaterequest')),
            ],
        ),
        migrations.CreateModel(
            name='certfiticate_of_live_in',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship', models.CharField(max_length=50, null=True)),
                ('live_in_since', models.DateField()),
                ('name_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name_1', to='home.resident')),
                ('name_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name_2', to='home.resident')),
                ('transaction_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.certificaterequest')),
            ],
        ),
        migrations.CreateModel(
            name='OrgMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.resident')),
                ('org', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.brgyorganization')),
            ],
            options={
                'unique_together': {('org', 'member')},
            },
        ),
        migrations.CreateModel(
            name='BarangayOfficial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=50)),
                ('date_appointed', models.DateField()),
                ('end_term', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[['ACTIVE', 'ACTIVE'], ['INACTIVE', 'INACTIVE']], default='ACTIVE', max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('fullname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.resident')),
            ],
            options={
                'unique_together': {('fullname', 'position', 'date_appointed', 'end_term', 'status')},
            },
        ),
    ]