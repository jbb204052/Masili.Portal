from datetime import datetime, timezone
from time import sleep

from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from . import models
from . import forms
from . import sms_sender
from notifications.signals import notify
from apps.authentication import models as auth_models


def index(request):
    population = models.Resident.objects.filter(status='RESIDING').count()
    officials_count = models.BarangayOfficial.objects.filter(status='ACTIVE').count()
    _pending_certificates = models.CertificateRequest.objects.filter(status='PENDING').count()
    gallery = models.Gallery.objects.all()

    _account_forBackend = ['ADMIN', 'OFFICIAL', 'SECRETARY', 'CHAIRMAN']

    if request.user.is_authenticated:
        if request.user.profile.account_type in _account_forBackend:
            notifications = request.user.notifications.unread()
            context = {'segment': 'index', 'population': population, 'gallery': gallery,
                       'notifications': notifications, 'pending_certificates': _pending_certificates, 'officials': officials_count}
            html_template = loader.get_template('home/index.html')
        else:
            return HttpResponseRedirect('index')
    else:
        return HttpResponseRedirect('index')
        # html_template = loader.get_template('home/page-404.html')

    return HttpResponse(html_template.render(context, request))


def user_ui(request):
    get_three = models.Gallery.objects.order_by('-date_uploaded')[:3]
    residents = models.Resident.objects.count()
    officials_count = models.BarangayOfficial.objects.count()
    context = {'segment': {'user_ui'}, 'residents': residents, 'gallery': get_three,
               'count': range(1, get_three.count() + 1), 'officials_count': officials_count}
    return render(request, 'index/index.html', context)


def about(request):
    chairman = auth_models.User.objects.filter(profile__account_type='CHAIRMAN')
    print(chairman)
    for i in chairman:
        notify.send(sender=request.user, recipient=i, verb='Viewed the About Page', cta_link='/about')
    officials = models.BarangayOfficial.objects.filter(status='ACTIVE')
    _chairman = officials.filter(position='BARANGAY CHAIRMAN').first()
    _councilors = officials.filter(position='BARANGAY COUNCILOR')
    context = {'segment': 'about', 'chairman': _chairman, 'councilors': _councilors}
    html_template = loader.get_template('index/about.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def hotlines(request):
    hotlines = models.Hotline.objects.all()
    context = {'segment': {'hotlines', 'brgy_info'}, 'hotlines': hotlines}
    html_template = loader.get_template('home/hotlines/hotlines_list.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def hotline_data(request):
    if request.method == 'POST':
        hotline_form = forms.HotlineForm(request.POST)
        if hotline_form.is_valid():
            hotline_form.save()
            messages.success(request, 'Hotline successfully added!')
            return HttpResponseRedirect(reverse('hotlines'))
        else:
            messages.error(request, 'Hotline already exists!')
    else:
        hotline_form = forms.HotlineForm()
    context = {'segment': {'hotlines', 'brgy_info', 'add'}, 'form': hotline_form}
    html_template = loader.get_template('home/hotlines/hotline_data.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def hotline_edit(request, id=0):
    hotline = models.Hotline.objects.get(id=id)
    if request.method == 'POST':
        hotline_form = forms.HotlineForm(request.POST, instance=hotline)
        if hotline_form.is_valid():
            hotline_form.save()
            messages.success(request, 'Hotline successfully updated!')
            return HttpResponseRedirect(reverse('hotlines'))
        else:
            messages.error(request, 'Error updating hotline')
    else:
        hotline_form = forms.HotlineForm(instance=hotline)
    context = {'segment': {'hotlines', 'brgy_info', 'update'}, 'form': hotline_form, 'hotline': hotline}
    html_template = loader.get_template('home/hotlines/hotline_data.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def hotline_view(request, id=0):
    hotline = models.Hotline.objects.get(id=id)
    context = {'segment': {'hotlines', 'brgy_info', 'view'}, 'hotline': hotline}
    html_template = loader.get_template('home/hotlines/hotline_view.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def hotline_delete(request, id=0):
    hotline = models.Hotline.objects.get(id=id)
    if request.method == 'POST':
        hotline.delete()
        messages.success(request, 'Hotline successfully deleted!')
        return HttpResponseRedirect(reverse('hotlines'))
    else:
        messages.info(request, 'Deletion cancelled!')
    context = {'segment': {'hotlines', 'brgy_info'}, 'hotline': hotline}
    html_template = loader.get_template('home/hotlines/hotline_delete.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def organizations(request):
    orgs = models.BrgyOrganization.objects.all()
    context = {'segment': {'org', 'brgy_info'}, 'orgs': orgs}
    html_template = loader.get_template('home/orgs/org_list.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def organization_data(request):
    if request.method == 'POST':
        org_form = forms.OrganizationForm(request.POST)
        if org_form.is_valid():
            org_form.save()
            messages.success(request, 'Organization successfully added!')
            return HttpResponseRedirect(reverse('organizations'))
        else:
            messages.error(request, 'Organization already exists!')
    context = {'segment': {'org', 'brgy_info', 'add'}, 'form': forms.OrganizationForm}
    html_template = loader.get_template('home/orgs/org_data.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def organization_edit(request, id=0):
    org = models.BrgyOrganization.objects.get(id=id)
    if request.method == 'POST':
        org_form = forms.OrganizationForm(request.POST, instance=org)
        if org_form.is_valid():
            org_form.save()
            messages.success(request, 'Organization successfully updated!')
            return HttpResponseRedirect(reverse('organizations'))
        else:
            messages.error(request, 'Error updating organization')
    context = {'segment': {'org', 'brgy_info', 'update'}, 'form': forms.OrganizationForm(instance=org), 'org': org}
    html_template = loader.get_template('home/orgs/org_data.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def announcements(request, opt):
    announcements = None
    if opt == 'all':
        announcements = models.Announcement.objects.all()
    elif opt == 'pending':
        announcements = models.Announcement.objects.filter(status='PENDING')

    context = {'segment': {'announcements', opt}, 'announcements': announcements}
    html_template = loader.get_template('home/announcements/announcement_list.html')
    return HttpResponse(html_template.render(context, request))


def getRecipientList(arg):
    orgs = models.BrgyOrganization.objects.all()
    puroks = models.Purok.objects.all()
    recipients = None
    if arg == 'ALL':
        recipients = models.Resident.objects.filter(status='RESIDING').values_list('phone_no1', flat=True)
    elif arg in orgs.values_list('org_name', flat=True):
        recipients = models.OrgMember.objects.filter(org__org_name=arg).values_list('member__phone_no1', flat=True)
    elif arg in puroks.values_list('name', flat=True):
        recipients = models.Resident.objects.filter(purok__name=arg, status='RESIDING').values_list('phone_no1', flat=True)
    print(recipients)
    return recipients


@login_required(login_url="/login/")
def announcement_data(request):
    orgs = models.BrgyOrganization.objects.all()
    puroks = models.Purok.objects.all()
    if request.method == 'POST':
        announcement_form = forms.AnnouncementForm(request.POST)
        if announcement_form.is_valid():
            _data = announcement_form.save(commit=False)
            send_to = request.POST['recipient']
            print(send_to)

            message = request.POST['content']
            numbers = getRecipientList(send_to)
            if numbers.count() > 0:
                if request.user.profile.account_type == 'CHAIRMAN':
                    if numbers.count() > 0:
                        for number in numbers:
                            sms_sender.send_sms(number,  announcement_form.cleaned_data.get('title') + '\n\n ' + message + '\n\n - sent via Masili Online Portal')
                        sleep(3)
                        _data.status = 'APPROVED'
                        messages.success(request, 'Announcement has been delivered!')

                _data.send_to = send_to
                _data.posted_by = request.user.first_name + ' ' + request.user.last_name
                _data.save()
                messages.success(request, 'Announcement successfully added!')
                return HttpResponseRedirect(reverse('announcements', kwargs={'opt': 'all'}))
            else:
                messages.error(request, 'No recipients found!')
        else:
            messages.error(request, 'Error adding announcement!')

    announcement_form = forms.AnnouncementForm()
    context = {'segment': {'announcements', 'add', 'all'}, 'form': announcement_form, 'organization': orgs, 'puroks': puroks}
    html_template = loader.get_template('home/announcements/announcement_data.html')
    return HttpResponse(html_template.render(context, request))


def announcement_view(request, id=0):
    announcement = models.Announcement.objects.get(id=id)
    form = forms.AnnouncementForm(instance=announcement)
    context = {'segment': {'announcements', 'view', 'for_approval'}, 'announcement': announcement, 'form': form}
    html_template = loader.get_template('home/announcements/announcement_data.html')
    return HttpResponse(html_template.render(context, request))


def announcement_approve(request, id=0):
    announcement = models.Announcement.objects.get(id=id)
    announcement.status = 'APPROVED'
    announcement.save()
    for number in getRecipientList(announcement.send_to):
        sms_sender.send_sms(number, announcement.title + '\n\n ' + announcement.content + '\n\n - sent via Masili Online Portal')
        sleep(1)
    messages.success(request, f'Announcement has been delivered to {getRecipientList(announcement.send_to).count()} recipients!')
    context = {'segment': {'announcements', 'view', 'for_approval', 'pending'}, 'announcement': announcement}
    return HttpResponseRedirect(reverse('announcements', kwargs={'opt': 'pending'}), context)


@login_required(login_url="/login/")
def gallery(request):
    # gallery = models.Gallery.objects.all()
    # get photo from the gallery sort by date_uploaded
    gallery = models.Gallery.objects.all().order_by('-date_uploaded')
    context = {'segment': {'gallery'}, 'gallery': gallery}
    html_template = loader.get_template('home/gallery/gallery.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def gallery_upload(request):
    if request.method == 'POST':
        gallery_form = forms.GalleryForm(request.POST, request.FILES)
        if gallery_form.is_valid():
            gallery_form.save()
            messages.success(request, 'Photo successfully added!')
            return HttpResponseRedirect(reverse('gallery'))
        else:
            messages.error(request, 'Error adding photo!')

    form = forms.GalleryForm()
    context = {'segment': 'gallery', 'form': form}
    return render(request, 'home/gallery/upload.html', context)


@login_required(login_url="/login/")
def ordinances(request):
    ordinances = models.Ordinance.objects.all()
    context = {'segment': {'ordinances'}, 'ordinances': ordinances}
    html_template = loader.get_template('home/ordinances/ordinances_list.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def ordinance_data(request):
    officials = models.BarangayOfficial.objects.filter(status='ACTIVE')
    ordinances = models.Ordinance.objects.all()
    ordinance_count = ordinances.count()
    if ordinance_count == 0:
        ordinance_no = 'ORD-' + str(datetime.now().year) + '-0001'
    else:
        last_ordinance = ordinances.last()
        ordinance_no = last_ordinance.ordinance_no
        ordinance_no = ordinance_no.split('-')
        ordinance_no = 'ORD-' + str(datetime.now().year) + '-' + str(int(ordinance_no[2]) + 1).zfill(4)

    if request.method == 'POST':
        ordinance_form = forms.OrdinanceForm(request.POST, request.FILES)
        if ordinance_form.is_valid():
            _data = ordinance_form.save(commit=False)
            _data.ordinance_no = ordinance_no
            _data.posted_by = request.user.first_name + ' ' + request.user.last_name

            _presiding = request.POST['presiding']
            _data.presiding_officer = _presiding
            # get the active brgy chairman
            chairman = models.BrgyOfficial.objects.get(position='BARANGAY CHAIRMAN')
            _data.active_chairman = chairman

            files = request.FILES.getlist('files')
            for file in files:
                _data.files = file
                _data.save()

            _data.save()

            messages.success(request, 'Ordinance successfully added!')
            return HttpResponseRedirect(reverse('ordinances'))
        else:
            messages.error(request, 'Error adding ordinance!')
    context = {'segment': {'ordinances', 'add'}, 'form': forms.OrdinanceForm, 'ordinance_no': ordinance_no,
               'officials': officials}
    html_template = loader.get_template('home/ordinances/ordinance_data.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def ordinance_view(request, id=0):
    ordinance = models.Ordinance.objects.get(id=id)
    attest_by = ordinance.attested_by.split(',')

    year = ordinance.date_posted.year

    context = {'segment': {'ordinances', 'view'}, 'ordinance': ordinance, 'year': year, 'attest_by': attest_by}
    html_template = loader.get_template('home/ordinances/ordinance_view.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def ordinance_edit(request, id=0):
    ordinance = models.Ordinance.objects.get(id=id)
    officials = models.BarangayOfficial.objects.filter(status='ACTIVE')
    attest_by = ordinance.attested_by.split(',')

    if request.method == 'POST':
        ordinance_form = forms.OrdinanceForm(request.POST, request.FILES, instance=ordinance)
        if ordinance_form.is_valid():
            _data = ordinance_form.save(commit=False)
            _data.posted_by = request.user.first_name + ' ' + request.user.last_name

            _presiding = request.POST['presiding']
            _data.presiding_officer = _presiding

            files = request.FILES.getlist('files')
            for file in files:
                _data.files = file
                _data.save()

            _data.save()

            messages.success(request, 'Ordinance successfully updated!')
            return HttpResponseRedirect(reverse('ordinances'))
        else:
            messages.error(request, 'Error updating ordinance!')

    context = {'segment': {'ordinances', 'edit'}, 'form': forms.OrdinanceForm(instance=ordinance),
               'ordinance': ordinance, 'officials': officials, 'attest_by': attest_by}
    html_template = loader.get_template('home/ordinances/ordinance_data.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def residents(request):
    residents = models.Resident.objects.filter(is_approved=True)
    puroks = models.Purok.objects.all()

    # get the number or residents per purok
    purok_residents = []
    for purok in puroks:
        purok_residents.append(models.Resident.objects.filter(purok=purok, is_approved=True).count())
    count = residents.count()
    context = {'segment': {'residents'}, 'residents': residents, 'count': count, 'puroks': puroks,
               'purok_residents': purok_residents}
    html_template = loader.get_template('home/residents/residents_list.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def resident_view(request, id):
    resident = models.Resident.objects.get(id=id)
    # emergency = models.EmergencyContact.objects.filter(resident=resident)
    context = {'segment': {'residents', 'view'}, 'resident': resident}
    html_template = loader.get_template('home/residents/resident_view.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def resident_data(request):
    residents = models.Resident.objects.all()
    resident_count = residents.count()
    if resident_count == 0:
        resident_no = 'MASILI-RES-0001'
    else:
        resident_no = 'MASILI-RES-' + str(int(resident_count) + 1).zfill(4)

    if request.method == 'POST':
        resident_form = forms.ResidentForm(request.POST, request.FILES)
        # emergency_form = forms.EmergencyContactForm(request.POST)
        if resident_form.is_valid():
            try:
                _data = resident_form.save(commit=False)
                _data.res_id = resident_no
                if request.user.profile.account_type == 'CHAIRMAN':
                    _data.is_approved = True
                _data.save()
                #
                # _emergency = emergency_form.save(commit=False)
                # _emergency.resident = _data
                # emergency_form.save()
                messages.success(request, 'Resident successfully added!')
                return HttpResponseRedirect(reverse('residents'))
            except IntegrityError as e:
                messages.error(request, e)
        else:
            messages.error(request, 'Error adding resident!')

    form = forms.ResidentForm()
    context = {'segment': {'residents', 'add'}, 'form': form, 'resident_no': resident_no}
    html_template = loader.get_template('home/residents/resident_data.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def resident_edit(request, id):
    resident = models.Resident.objects.get(id=id)

    if request.method == 'POST':
        resident_form = forms.ResidentForm(request.POST, request.FILES, instance=resident)
        if resident_form.is_valid():
            _data = resident_form.save(commit=False)
            if request.user.profile.account_type == 'CHAIRMAN':
                _data.is_approved = True
            _data.save()

            messages.success(request, 'Resident successfully updated!')
            return HttpResponseRedirect(reverse('residents'))
        else:
            messages.error(request, 'Error updating resident information!')

    form = forms.ResidentForm(instance=resident)
    context = {'segment': {'residents', 'edit'}, 'form': form, 'resident': resident}
    html_template = loader.get_template('home/residents/resident_data.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def blotters(request):
    blotters = models.Blotter.objects.all()
    count = blotters.count()
    context = {'segment': {'blotters'}, 'blotters': blotters, 'count': count}
    html_template = loader.get_template('home/blotters/blotters_list.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def blotter_data(request):
    blotters = models.Blotter.objects.all()
    blotter_count = blotters.count()
    if blotter_count == 0:
        blotter_no = f'MASILI-BLOTTER-0001'
    else:
        blotter_no = f'MASILI-BLOTTER-' + str(int(blotter_count) + 1).zfill(4)

    if request.method == 'POST':
        blotter_form = forms.BlotterForm(request.POST)
        complainant_form = forms.ComplainantForm(request.POST)
        respondent_form = forms.RespondentForm(request.POST)
        if blotter_form.is_valid():
            _data = blotter_form.save(commit=False)
            _data.blotter_no = blotter_no
            _data.posted_by = request.user.first_name + ' ' + request.user.last_name
            _data.recordedBy = request.user
            _data.save()
            _data1 = complainant_form.save(commit=False)
            _data1.blotter_no = _data
            _data1.save()
            _data2 = respondent_form.save(commit=False)
            _data2.blotter_no = _data
            _data2.save()
            messages.success(request, 'Blotter successfully added!')
            return HttpResponseRedirect(reverse('blotters'))
        else:
            messages.error(request, 'Error adding blotter!')

    form = forms.BlotterForm()
    complainant_form = forms.ComplainantForm()
    respondent_form = forms.RespondentForm()
    context = {'segment': {'blotters', 'add'}, 'form': form, 'blotter_no': blotter_no,
               'complainant_form': complainant_form, 'respondent_form': respondent_form}
    html_template = loader.get_template('home/blotters/blotter_data.html')
    return HttpResponse(html_template.render(context, request))


def portfolio(request):
    context = {'segment': 'portfolio'}
    html_template = loader.get_template('user_ui/portfolio.html')
    return HttpResponse(html_template.render(context, request))


def brgy_sessions(request):
    sessions = models.Session.objects.all()
    context = {'segment': 'sessions', 'sessions': sessions}
    html_template = loader.get_template('home/sessions/sessions_list.html')
    return HttpResponse(html_template.render(context, request))


def brgy_session_data(request):
    sessions = models.Session.objects.filter(session_date__month=datetime.now().month)
    session_count = sessions.count()
    positions = ['BARANGAY CHAIRMAN', 'BARANGAY COUNCILOR', 'SK CHAIRMAN', 'BARANGAY SECRETARY', 'BARANGAY TREASURER']
    officials = models.BarangayOfficial.objects.filter(position__in=positions, status='ACTIVE')
    if session_count == 0:
        session_no = f'Y{datetime.now().year}-M{datetime.now().month}-S01'
    else:
        session_no = f'Y{datetime.now().year}-M{datetime.now().month}-S' + str(int(session_count) + 1).zfill(2)

    if request.method == 'POST':
        session_form = forms.SessionForm(request.POST)
        if session_form.is_valid():
            _data = session_form.save(commit=False)
            _data.session_no = session_no
            _data.save()
            messages.success(request, 'Session successfully added!')
            return HttpResponseRedirect(reverse('brgy_sessions'))
        else:
            messages.error(request, 'Error adding session!')

    context = {'segment': 'sessions', 'session_no': session_no, 'form': forms.SessionForm, 'officials': officials}
    html_template = loader.get_template('home/sessions/session_data.html')
    return HttpResponse(html_template.render(context, request))


def brgy_session_view(request, id):
    session = models.Session.objects.get(id=id)
    session_date = session.session_date.strftime('%B %d, %Y').upper()
    session_time = session.session_start.strftime('%I:%M %P').upper()
    presents = session.attendees.split(',')

    officials = models.BarangayOfficial.objects.filter(id__in=presents)
    secretary = officials.filter(position='BARANGAY SECRETARY').first()

    context = {'segment': 'sessions', 'session': session, 'officials': officials, 'secretary': secretary,
               'session_date': session_date, 'session_time': session_time}
    html_template = loader.get_template('home/sessions/session_view.html')
    return HttpResponse(html_template.render(context, request))


def certificate_of_indigency_view(request):
    chairman = models.BarangayOfficial.objects.filter(position='BARANGAY CHAIRMAN', status='ACTIVE').first()
    chairman_fullname = chairman.fname + ' ' + chairman.mname[0] + '. ' + chairman.lname

    context = {'segment': {'certificates', 'indigency', 'view'}, 'brgy_chairman': chairman_fullname}
    html_template = loader.get_template('home/certificates/indigency.html')
    return HttpResponse(html_template.render(context, request))


def certificates(request):
    _certificates = models.CertificateRequest.objects.all()
    _issued = models.CertificateRequest.objects.filter(status='ISSUED').count()
    _indigency = models.CertificateRequest.objects.filter(certificate_type='INDIGENCY').count()
    _livein = models.CertificateRequest.objects.filter(certificate_type='LIVE IN').count()
    _pending = models.CertificateRequest.objects.filter(status='PENDING').count()
    context = {'segment': 'certificates', 'certificates': _certificates, 'issued': _issued, 'indigency': _indigency,
               'livein': _livein, 'pending': _pending}
    html_template = loader.get_template('home/certificates/certificates_list.html')
    return HttpResponse(html_template.render(context, request))


def certificate_of_indigency_data(request):
    _certificates = models.CertificateRequest.objects.count();
    form = forms.CertificateRequestForm()
    if _certificates == 0:
        transaction_no = f'IND-{datetime.now().year}-0001'
    else:
        transaction_no = f'IND-{datetime.now().year}-{str(int(_certificates) + 1).zfill(4)}'

    if request.method == 'POST':
        form = forms.CertificateRequestForm(request.POST)
        if form.is_valid():
            fullname = request.POST['fullname']
            res = models.Resident.objects.filter(fullname=fullname).first()
            cert = form.save(commit=False)
            cert.full_name = res
            cert.transaction_number = transaction_no
            cert.certificate_type = "INDIGENCY"
            cert.request_method = 'WALK IN'
            cert.save()
            messages.success(request, 'Certificate successfully added!')



            _resident = models.Resident.objects.get(fullname=fullname)
            certificate = models.CertificateRequest.objects.get(transaction_number=transaction_no)
            _chairman = models.BrgyOfficial.objects.filter(position='BARANGAY CHAIRMAN', status='ACTIVE').first()
            _age = datetime.now().year - _resident.bdate.year
            return render(request, 'home/certificates/indigency.html', {'resident': _resident, 'certificate': certificate, 'chairman': _chairman, 'age': _age})
        else:
            messages.error(request, 'Error adding certificate!')
            form = forms.CertificateRequestForm(request.POST)

    residents = models.Resident.objects.all()
    context = {'segment': {'certificates', 'indigency'}, 'type_of_certificate': 'Indigency', 'residents': residents,
               'transaction_no': transaction_no, 'form': form}
    html_template = loader.get_template('home/certificates/certificate_data.html')
    return HttpResponse(html_template.render(context, request))


def issued_certificates(request, id):
    _certificate = models.CertificateRequest.objects.get(id=id)
    _certificate.status = 'ISSUED'
    _certificate.save()
    messages.success(request, f'{_certificate.transaction_number} has been issued!')
    return HttpResponseRedirect(reverse('certificates'))

def indigency_print(request, id):
    certificate = models.CertificateRequest.objects.get(id=id)
    res = models.Resident.objects.get(fullname=certificate.full_name)

    aux = lambda x: 'Mr.' if res.gender == 'MALE' else 'Ms.'
    age = datetime.now().year - res.bdate.year
    is_samePerson = res.fullname == certificate.requestor
    chairman = models.BarangayOfficial.objects.filter(position='BARANGAY CHAIRMAN', status='ACTIVE').first()
    print(res.fullname)
    print(certificate.requestor)
    print(is_samePerson)

    context = {'segment': {'certificates', 'indigency'}, 'aux': aux, 'age': age, 'resident': res,
               'certificate': certificate, 'type_of_certificate': 'Indigency', 'is_samePerson': is_samePerson, 'chairman': chairman}
    html_template = loader.get_template('home/certificates/indigency.html')
    return HttpResponse(html_template.render(context, request))


def certificate_add(request, cert_type):
    _certificates = models.CertificateRequest.objects.count()
    if _certificates == 0:
        transaction_no = f'{cert_type}-{datetime.now().year}-0001'
    else:
        transaction_no = f'{cert_type}-{datetime.now().year}-{str(int(_certificates) + 1).zfill(4)}'

    if cert_type == 'IND':
        form = forms.CertificateRequestForm()
    elif cert_type == 'LIV':
        form = forms.LiveInForm()

    # if request.method == 'POST':


def officials(request):
    _officials = models.BarangayOfficial.objects.all().order_by('date_added')
    context = {'segment': 'officials', 'officials': _officials}
    html_template = loader.get_template('home/officials/officials_list.html')
    return HttpResponse(html_template.render(context, request))


def official_data(request):
    residents = models.Resident.objects.filter(status='RESIDING')
    if request.method == 'POST':
        form = forms.OfficialForm(request.POST)
        if form.is_valid():
            _fullname = request.POST['fullname']
            _res = models.Resident.objects.get(fullname=_fullname)
            print(_res)
            _position = form.cleaned_data['position']
            _date_appointed = form.cleaned_data['date_appointed']
            _end_term = form.cleaned_data['end_term']
            _status = form.cleaned_data['status']
            try:
                _data = form.save(commit=False)
                _data.fullname = _res
                _data.save()
                messages.success(request, 'Official successfully added!')
                return redirect('officials')
            except IntegrityError:
                messages.error(request, 'Official already exists!')
                form = forms.OfficialForm(request.POST)
        else:
            messages.error(request, 'Error adding official!')
            form = forms.OfficialForm(request.POST)
    else:
        form = forms.OfficialForm()

    context = {'segment': {'officials', 'add'}, 'form': form, 'residents': residents}
    html_template = loader.get_template('home/officials/official_data.html')
    return HttpResponse(html_template.render(context, request))


def official_update(request, id):
    _official = models.BarangayOfficial.objects.get(id=id)
    residents = models.Resident.objects.filter(status='RESIDING')
    if request.method == 'POST':
        form = forms.OfficialForm(request.POST, instance=_official)
        if form.is_valid():
            form.save()
            messages.success(request, 'Official successfully updated!')
            return redirect('officials')
        else:
            messages.error(request, 'Error updating official!')
            form = forms.OfficialForm(request.POST, instance=_official)
    else:
        form = forms.OfficialForm(instance=_official)

    context = {'segment': {'officials', 'update'}, 'form': form, 'official': _official, 'residents': residents}
    html_template = loader.get_template('home/officials/official_data.html')
    return HttpResponse(html_template.render(context, request))


def official_view(request, id):
    _official = models.BarangayOfficial.objects.get(id=id)

    history = models.BarangayOfficial.objects.filter(fullname=_official.fullname)

    context = {'segment': {'officials', 'view'}, 'official': _official, 'history': history}
    html_template = loader.get_template('home/officials/official_view.html')
    return HttpResponse(html_template.render(context, request))


def notification(request, id):
    _notification = get_object_or_404(models.Notification, id=id, recipient=request.user)
    _notification.mark_as_read()
    return redirect(_notification.notificationscta.cta_link)


def notification_read_all(request):
    _notifications = models.Notification.objects.filter(unread=True)
    for _notification in _notifications:
        _notification.unread = False
        _notification.save()
    return redirect('notifications')