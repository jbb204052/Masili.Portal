import json
from datetime import datetime, timezone
from itertools import chain
from time import sleep

from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.template.defaultfilters import safe
from django.urls import reverse
from . import models
from . import forms
from . import sms_sender
from notifications.signals import notify
from apps.authentication import models as auth_models


Purok = ['PUROK 1', 'PUROK 2', 'PUROK 3', 'PUROK 4', 'PUROK 5', 'PUROK 6']
# Purok = (
#     ('PUROK 1', 'PUROK 1'),
#     ('PUROK 2', 'PUROK 2'),
#     ('PUROK 3', 'PUROK 3'),
#     ('PUROK 4', 'PUROK 4'),
#     ('PUROK 5', 'PUROK 5'),
#     ('PUROK 6', 'PUROK 6'),
# )



def index(request):
    population = models.Resident.objects.filter(status='RESIDING').count()
    officials_count = models.BarangayOfficial.objects.filter(status='ACTIVE').count()
    _pending_certificates = models.CertificateRequest.objects.filter(status='PENDING').count()
    gallery = models.Gallery.objects.all()
    purok_population = []
    for purok in Purok:
        purok_population.append([purok, models.Resident.objects.filter(purok=purok, status='RESIDING').count()])
    population_per_gender = []
    gender = ['MALE', 'FEMALE']
    for g in gender:
        population_per_gender.append([g, models.Resident.objects.filter(gender=g, status='RESIDING').count()])
    _account_forBackend = ['ADMIN', 'OFFICIAL', 'SECRETARY', 'CHAIRMAN']
    if request.user.is_authenticated:
        if request.user.profile.account_type in _account_forBackend:
            notifications = request.user.notifications.unread()
            captain = models.BarangayOfficial.objects.filter(position='BARANGAY CHAIRMAN', status='ACTIVE').first()
            officials = models.BarangayOfficial.objects.filter(status='ACTIVE').exclude(position='BARANGAY CHAIRMAN')
            _pending_blotters = models.Blotter.objects.filter(status='PENDING').count()
            context = {'segment': 'index', 'population': population, 'gallery': gallery,
                       'notifications': notifications, 'pending_certificates': _pending_certificates,
                       'officials_count': officials_count, 'purok_population': purok_population,
                       'population_per_gender': population_per_gender, 'captain': captain,
                       'officials': officials, 'pending_blotters': _pending_blotters}
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
    news = models.News.objects.filter(post_status='PUBLISHED').order_by('-date_posted')[0:3]
    context = {'segment': {'user_ui'}, 'residents': residents, 'gallery': get_three,
               'count': range(1, get_three.count() + 1), 'officials_count': officials_count, 'news_list': news}
    return render(request, 'index/index.html', context)


def about(request):
    # chairman = auth_models.User.objects.filter(profile__account_type='CHAIRMAN')
    # print(chairman)
    # for i in chairman:
    #     notify.send(sender=request.user, recipient=i, verb='Viewed the About Page', cta_link='/about')
    officials = models.BarangayOfficial.objects.filter(status='ACTIVE')
    _chairman = officials.filter(position='BARANGAY CHAIRMAN').first()
    _councilors = officials.filter(position__contains='BARANGAY').exclude(position='BARANGAY CHAIRMAN')
    _skchairman = officials.filter(position='SK CHAIRMAN').first()
    _skcouncilors = officials.filter(position__contains='SK').exclude(position='SK CHAIRMAN')
    _hotlines = models.Hotline.objects.all()
    context = {'segment': 'about', 'chairman': _chairman, 'councilors': _councilors, 'officials': officials, 'skchairman': _skchairman, 'skcouncilors': _skcouncilors, 'hotlines': _hotlines}
    html_template = loader.get_template('index/about.html')
    return HttpResponse(html_template.render(context, request))


def portfolio(request):
    gallery = models.Gallery.objects.all().order_by('-date_uploaded')
    context = {'segment': 'portfolio', 'gallery': gallery}
    return render(request, 'index/portfolio.html', context)


@login_required(login_url='/login/')
def request_certificates(request):
    _certificates = models.CertificateRequest.objects.count();
    if _certificates == 0:
        transaction_no = f'IND-{datetime.now().year}-0001'
    else:
        transaction_no = f'IND-{datetime.now().year}-{str(int(_certificates) + 1).zfill(4)}'

    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        res = models.Resident.objects.filter(lname=request.user.last_name, fname=request.user.first_name, bdate=request.user.profile.birthdate).first()
        print(res)
        cert_type = 'INDIGENCY'
        requestor = res.fullname
        chairman = models.BarangayOfficial.objects.filter(position='BARANGAY CHAIRMAN', status='ACTIVE').first()
        createCertificate = models.CertificateRequest.objects.create(transaction_number=transaction_no, purpose=purpose, full_name=res, certificate_type=cert_type, requestor=requestor, status='PENDING', chairman=chairman.fullname.fullname)
        createCertificate.save()
        messages.success(request, 'Your request has been sent to the Barangay Officials. Please wait for their response.')
        return HttpResponseRedirect('user_ui')
    context = {'segment': 'request_certificates'}
    return render(request, 'index/certificate_request.html', context)



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
    recipients = None
    if arg == 'ALL':
        recipients = models.Resident.objects.filter(status='RESIDING').values_list('phone_no1', flat=True)
    elif arg in orgs.values_list('org_name', flat=True):
        recipients = models.OrgMember.objects.filter(org__org_name=arg).values_list('member__phone_no1', flat=True)
    elif arg in Purok:
        recipients = models.Resident.objects.filter(purok=arg, status='RESIDING').values_list('phone_no1', flat=True)
    print(recipients)
    return recipients


@login_required(login_url="/login/")
def announcement_data(request):
    orgs = models.BrgyOrganization.objects.all()
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
    context = {'segment': {'announcements', 'add', 'all'}, 'form': announcement_form, 'organization': orgs, 'puroks': Purok}
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


# @login_required(login_url="/login/")
# def gallery_upload(request):
#     if request.method == 'POST':
#         gallery_form = forms.GalleryForm(request.POST, request.FILES)
#         if gallery_form.is_valid():
#             gallery_form.save()
#             messages.success(request, 'Photo successfully added!')
#             return HttpResponseRedirect(reverse('gallery'))
#         else:
#             messages.error(request, 'Error adding photo!')
#
#     form = forms.GalleryForm()
#     context = {'segment': 'gallery', 'form': form}
#     return render(request, 'home/gallery/upload.html', context)


def gallery_upload(request):
    context = {'segment': 'gallery'}
    return render(request, 'home/gallery/upload.html', context)


def dropzone_image(request):
    if request.method == "POST":
        image = request.FILES.get('file')
        print(image)
        img = models.Gallery.objects.create(photo=image)
        messages.success(request, 'Photo successfully added!')
        return JsonResponse({'success': True, 'image': img.photo.url})
        # return HttpResponseRedirect(reverse('gallery'))

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
            chairman = models.BarangayOfficial.objects.get(position='BARANGAY CHAIRMAN', status='ACTIVE')
            _data.active_chairman = chairman.fullname

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
    puroks = Purok
    purok_residents = []
    for purok in puroks:
        purok_residents.append(models.Resident.objects.filter(purok=purok, is_approved=True).count())
    count = residents.count()
    context = {'segment': {'residents', 'app_residents'}, 'residents': residents, 'count': count, 'puroks': puroks,
               'purok_residents': purok_residents}
    html_template = loader.get_template('home/residents/residents_list.html')
    return HttpResponse(html_template.render(context, request))


def residents_for_approval(request):
    residents = models.Resident.objects.filter(is_approved=False)
    context = {'segment': {'residents', 'res_forApproval'}, 'residents': residents}
    html_template = loader.get_template('home/residents/residents_list.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def resident_view(request, id):
    resident = models.Resident.objects.get(id=id)
    official_data = models.BarangayOfficial.objects.filter(fullname_id=resident.id).order_by('-date_appointed')
    print(official_data)
    org_member = models.OrgMember.objects.filter(member__res_id=id)
    membership = []
    if official_data:
        for data in official_data:
            membership.append(f'{data.position} | {data.date_appointed.year}-{data.end_term.year}')
    if org_member:
        for data in org_member:
            membership.append(data.org.org_name)
    context = {'segment': {'residents', 'view'}, 'resident': resident, 'membership': membership}
    html_template = loader.get_template('home/residents/resident_view.html')
    return HttpResponse(html_template.render(context, request))


def resident_approve(request, id):
    resident = models.Resident.objects.get(id=id)
    resident.is_approved = True
    resident.save()
    messages.success(request, 'Resident successfully approved!')
    return HttpResponseRedirect(reverse('res_forApproval'))

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

            blotter = models.Blotter.objects.get(blotter_no=blotter_no)

            _complainant = complainant_form.save(commit=False)
            _complainant.blotter = blotter
            _complainant.save()

            _respondent = respondent_form.save(commit=False)
            _respondent.blotter = blotter
            _respondent.save()



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


def blotter_view(request, id):
    blotter = models.Blotter.objects.get(id=id)
    complainant = models.Complainant.objects.get(blotter=blotter)
    respondent = models.Respondent.objects.get(blotter=blotter)
    hearing = models.Hearing.objects.filter(blotter=blotter).order_by('-date')
    print(hearing)
    context = {'segment': {'blotters', 'view'}, 'blotter': blotter,
               'complainant': complainant, 'respondent': respondent, 'hearings': hearing}
    html_template = loader.get_template('home/blotters/blotter_view.html')
    return HttpResponse(html_template.render(context, request))


def blotter_print(request, id):
    blotter = models.Blotter.objects.get(id=id)
    complainant = models.Complainant.objects.get(blotter=blotter)
    respondent = models.Respondent.objects.get(blotter=blotter)
    import io
    from django.http import FileResponse
    from docxtpl import DocxTemplate

    doc = DocxTemplate("home/blotters/blotter_template.docx")
    context = {
        "blotter_no": blotter.blotter_no,
        "dateReported": blotter.datetimeReported,
        "incident_type": blotter.incident_type,
        "dateOfIncident": blotter.dateOfIncident,
        "placeOfIncident": blotter.placeOfIncident,
        "complainant_fullname": complainant.full_name,
        "complainant_contactNo": complainant.contact,
        "complainant_address": complainant.address,
        "respondent_fullname": respondent.full_name,
        "res_contactNo": respondent.contact,
        "res_address": respondent.address,
        "narrative": blotter.narrative|safe,
        "official_name": blotter.recordedBy.fullname,
        "position": blotter.recordedBy.position,
    }

    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    response = HttpResponse(doc_io.read())
    response['Content-Disposition'] = 'attachment; filename=blotter.docx'
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    return response
    # context = {'segment': {'blotters', 'view'}, 'blotter': blotter,
    #            'complainant': complainant, 'respondent': respondent, 'hearings': hearing}
    # html_template = loader.get_template('home/blotters/blotter_print.html')
    # return HttpResponse(html_template.render(context, request))

def hearing(request, id, blotter_no):
    blotter = models.Blotter.objects.get(id=id)
    complainant = models.Complainant.objects.get(blotter=blotter)
    respondent = models.Respondent.objects.get(blotter=blotter)
    hearing_count = models.Hearing.objects.filter(blotter=blotter).count()
    if hearing_count == 0:
        hearing_no = f'01'
    else:
        hearing_no = str(int(hearing_count) + 1).zfill(2)
    if request.method == 'POST':
        hearing_form = forms.HearingForm(request.POST, request.FILES)
        if hearing_form.is_valid():
            _data = hearing_form.save(commit=False)
            _data.blotter = blotter
            _data.hearing_no = hearing_no
            _data.save()
            # change the blotter status
            blotter.status = _data.status
            blotter.save()
            messages.success(request, 'Hearing successfully added!')
            return HttpResponseRedirect(reverse('blotter_view', kwargs={'id': id}))
        else:
            messages.error(request, 'Error adding hearing!')

    form = forms.HearingForm()
    context = {'segment': {'blotters', 'view'}, 'blotter': blotter,
               'complainant': complainant, 'respondent': respondent, 'form': form, 'hearing_no': hearing_no}
    html_template = loader.get_template('home/blotters/hearing.html')
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
    context = {'segment': {'certificates', 'indigency', 'view'}, 'brgy_chairman': chairman.fullname}
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
            _chairman = models.BarangayOfficial.objects.filter(position='BARANGAY CHAIRMAN', status='ACTIVE').first()
            print(_chairman)
            res = models.Resident.objects.filter(fullname=fullname).first()
            cert = form.save(commit=False)
            cert.full_name = res
            cert.chairman = _chairman.fullname
            cert.transaction_number = transaction_no
            cert.certificate_type = "INDIGENCY"
            cert.request_method = 'WALK IN'
            cert.save()
            messages.success(request, 'Certificate successfully added!')


            _resident = models.Resident.objects.get(fullname=fullname)
            certificate = models.CertificateRequest.objects.get(transaction_number=transaction_no)
            _age = datetime.now().year - _resident.bdate.year
            # return render(request, 'home/certificates/business.html', {'resident': _resident, 'certificate': certificate, 'chairman': _chairman, 'age': _age})
            return HttpResponseRedirect(reverse('indigency'))
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
    # _certificate.status = 'ISSUED'
    # _certificate.save()
    # messages.success(request, f'{_certificate.transaction_number} has been issued!')
    # return HttpResponseRedirect(reverse('certificates'))
    if request.method == 'POST':
        _certificate.status = 'ISSUED'
        _certificate.signed_certificates = request.FILES['attachment']
        _certificate.save()
        messages.success(request, f'{_certificate.transaction_number} has been issued!')
        return HttpResponseRedirect(reverse('certificates'))
    context = {'segment': 'certificates', 'certificate': _certificate}
    html_template = loader.get_template('home/certificates/certificate_attachment.html')
    return HttpResponse(html_template.render(context, request))

def indigency_print(request, id):
    certificate = models.CertificateRequest.objects.get(id=id)
    res = models.Resident.objects.get(fullname=certificate.full_name)

    aux = lambda x: 'Mr.' if res.gender == 'MALE' else 'Ms.'
    age = datetime.now().year - res.bdate.year
    is_samePerson = res.fullname == certificate.requestor
    chairman = certificate.chairman

    context = {'segment': {'certificates', 'indigency'}, 'aux': aux, 'age': age, 'resident': res,
               'certificate': certificate, 'type_of_certificate': 'Indigency', 'is_samePerson': is_samePerson, 'chairman': chairman}
    html_template = loader.get_template('home/certificates/indigency.html')
    return HttpResponse(html_template.render(context, request))


def printed_certificate(request, id):
    certificate = models.CertificateRequest.objects.get(id=id)
    certificate.status = 'PRINTED'
    certificate.save()
    messages.success(request, f'{certificate.transaction_number} has been printed!')
    return HttpResponseRedirect(reverse('certificates'))

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

    history = models.BarangayOfficial.objects.filter(fullname=_official.fullname).order_by('-date_appointed')
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


def news(request):
    _news = models.News.objects.all().order_by('-date_posted')
    context = {'segment': 'news', 'news_list': _news}
    html_template = loader.get_template('home/news/news_list.html')
    return HttpResponse(html_template.render(context, request))


def news_data(request):
    if request.method == 'POST':
        form = forms.NewsForm(request.POST, request.FILES)
        if form.is_valid():
            _data = form.save(commit=False)
            _data.posted_by = request.user
            if request.user.profile.account_type == 'CHAIRMAN':
                _data.status = 'PUBLISHED'
            _data.save()
            messages.success(request, 'News successfully added!')
            return redirect('news')
        else:
            messages.error(request, 'Error adding news!')
            form = forms.NewsForm(request.POST, request.FILES)
    else:
        form = forms.NewsForm()
    context = {'segment': {'news', 'add'}, 'form': form}
    html_template = loader.get_template('home/news/news_data.html')
    return HttpResponse(html_template.render(context, request))

def news_view(request, id):
    _news = models.News.objects.get(id=id)
    context = {'segment': {'news', 'view'}, 'news': _news}
    html_template = loader.get_template('home/news/news_view.html')
    return HttpResponse(html_template.render(context, request))


def news_read(request, id, title):
    _news = models.News.objects.get(id=id)
    other_news = models.News.objects.filter(post_status='PUBLISHED').exclude(id=id).order_by('-date_posted')[:5]
    html_template = loader.get_template('index/news_info.html')
    return HttpResponse(html_template.render({'news': _news, 'other_news': other_news}, request))


def news_update(request, id):
    _news = models.News.objects.get(id=id)
    if request.method == 'POST':
        form = forms.NewsForm(request.POST, request.FILES, instance=_news)
        if form.is_valid():
            _data = form.save(commit=False)
            if request.user.profile.account_type == 'CHAIRMAN':
                _data.status = 'PUBLISHED'
            _data.save()
            messages.success(request, 'News successfully updated!')
            return redirect('news')
        else:
            messages.error(request, 'Error updating news!')
            form = forms.NewsForm(request.POST, request.FILES, instance=_news)
    else:
        form = forms.NewsForm(instance=_news)
    context = {'segment': {'news', 'update'}, 'form': form, 'news': _news}
    html_template = loader.get_template('home/news/news_data.html')
    return HttpResponse(html_template.render(context, request))


def business_permit(request):
    _business_permit = models.BusinessPermit.objects.all().order_by('-date_issued')
    _business_closure = models.BusinessClosure.objects.all().order_by('-date_issued')
    _business_permit = list(chain(_business_permit, _business_closure))
    issued = models.BusinessPermit.objects.filter(status='ISSUED').count()
    p= ['PENDING', 'PRINTED']
    pending = models.BusinessPermit.objects.filter(status__in=p).count()
    context = {'segment': 'permits', 'business_permit_list': _business_permit, 'issued': issued, 'pending': pending}
    html_template = loader.get_template('home/permit/permit_list.html')
    return HttpResponse(html_template.render(context, request))


def business_permit_data(request):
    _businessPermits = models.BusinessPermit.objects.count()
    if _businessPermits == 0:
        _permit_no = f'BUS-{datetime.now().year}-0001'
    else:
        _permit_no = f'BUS-{datetime.now().year}-{str(int(_businessPermits) + 1).zfill(4)}'

    if request.method == 'POST':
        form = forms.BusinessPermitForm(request.POST)
        if form.is_valid():
            _data = form.save(commit=False)
            _data.business_no = _permit_no
            _data.issued_by = request.user
            _data.chairman = models.BarangayOfficial.objects.get(position='BARANGAY CHAIRMAN', status='ACTIVE').fullname
            _data.type = 'BUSINESS PERMIT'
            _data.save()
            messages.success(request, 'Business Permit successfully added!')
            return redirect('business_permit')
        else:
            messages.error(request, 'Error adding Business Permit!')
            form = forms.BusinessPermitForm(request.POST)
    else:
        form = forms.BusinessPermitForm()
    context = {'segment': {'permits', 'add'}, 'form': form}
    html_template = loader.get_template('home/permit/permit_data.html')
    return HttpResponse(html_template.render(context, request))


def business_permit_view(request, id):
    _business_permit = models.BusinessPermit.objects.get(id=id)
    context = {'segment': {'permits', 'view'}, 'permit': _business_permit}
    html_template = loader.get_template('home/permit/business.html')
    return HttpResponse(html_template.render(context, request))


def business_permit_print(request, id):
    _business_permit = models.BusinessPermit.objects.get(id=id)
    _business_permit.status = 'PRINTED'
    _business_permit.save()
    messages.success(request, f'{_business_permit.business_no} has been printed!')
    return HttpResponseRedirect(reverse('business_permit'))

def issued_business_permit(request, id):
    _business_permit = models.BusinessPermit.objects.get(id=id)

    if request.method == 'POST':
        _business_permit.status = 'ISSUED'
        _business_permit.signed_permits = request.FILES['attachment']
        _business_permit.save()
        messages.success(request, f'{_business_permit.business_no} has been issued!')
        return HttpResponseRedirect(reverse('business_permit'))
    context = {'segment': 'permits', 'permit': _business_permit}
    html_template = loader.get_template('home/permit/business_attachment.html')
    return HttpResponse(html_template.render(context, request))


def business_closure_data(request):
    _permit = models.BusinessClosure.objects.count() + models.BusinessPermit.objects.count()
    if _permit == 0:
        _permit_no = f'BUS-CL-{datetime.now().year}-0001'
    else:
        _permit_no = f'BUS-CL-{datetime.now().year}-{str(int(_permit) + 1).zfill(4)}'

    if request.method == 'POST':
        form = forms.BusinessClosureForm(request.POST)
        if form.is_valid():
            _data = form.save(commit=False)
            _data.transaction_no = _permit_no
            _data.chairman = models.BarangayOfficial.objects.get(position='BARANGAY CHAIRMAN', status='ACTIVE').fullname
            _data.type = 'BUSINESS CLOSURE'
            _data.transaction_no = _permit_no
            _data.status = 'PENDING'
            _data.save()
            messages.success(request, 'Business Closure successfully added!')
            return redirect('business_permit')
        else:
            messages.error(request, 'Error adding Business Closure!')
            form = forms.BusinessClosureForm(request.POST)
    else:
        form = forms.BusinessClosureForm()
    context = {'segment': {'permits', 'add'}, 'form': form, 'transaction_no': _permit_no}
    html_template = loader.get_template('home/permit/closure_data.html')
    return HttpResponse(html_template.render(context, request))