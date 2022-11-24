from datetime import datetime, timezone
from time import sleep

from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from . import models
from . import forms
from . import sms_sender

from django.forms import formset_factory, modelformset_factory

from ..authentication.models import Profile


@login_required(login_url="/login/")
def index(request):
    population = models.Resident.objects.count()
    officials_count = models.BrgyOfficial.objects.count()
    gallery = models.Gallery.objects.all()
    context = {'segment': 'index', 'officials_count': officials_count, 'population': population, 'gallery': gallery}
    if request.user.profile.is_superadmin:
        html_template = loader.get_template('home/index.html')
    else:
        return HttpResponseRedirect('user_ui')
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


def hotlines(request):
    hotlines = models.Hotline.objects.all()
    context = {'segment': {'hotlines', 'brgy_info'}, 'hotlines': hotlines}
    html_template = loader.get_template('home/hotlines/hotlines_list.html')
    return HttpResponse(html_template.render(context, request))


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


def hotline_view(request, id=0):
    hotline = models.Hotline.objects.get(id=id)
    context = {'segment': {'hotlines', 'brgy_info', 'view'}, 'hotline': hotline}
    html_template = loader.get_template('home/hotlines/hotline_view.html')
    return HttpResponse(html_template.render(context, request))


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


# BRGY OFFICIALS
def officials(request):
    officials = models.BrgyOfficial.objects.all()
    context = {'segment': {'officials'}, 'officials': officials}
    html_template = loader.get_template('home/officials/officials_list.html')
    return HttpResponse(html_template.render(context, request))


def official_data(request):
    if request.method == 'POST':
        official_form = forms.BrgyOfficialForm(request.POST)
        if official_form.is_valid():
            start_term = official_form.cleaned_data['start_term']
            end_term = official_form.cleaned_data['end_term']

            if start_term.year > end_term.year:
                messages.error(request, 'Start term must be less than end term!')
            elif start_term.year > datetime.now().year:
                messages.error(request, 'Start term must be less than or equal the current year!')
            else:
                positions = ['captain', 'kapitan', 'chairman', 'chairwoman']
                position = official_form.cleaned_data['position'].lower()
                # check if position contains any of the positions in the list
                if any(x in position for x in positions):
                    if models.BrgyOfficial.objects.filter(position__icontains='captain', status='ACTIVE').exists():
                        messages.error(request, 'There can only have 1 active Barangay Captain!')
                    else:
                        try:
                            official_form.save()
                            messages.success(request, 'Official successfully added!')
                            return HttpResponseRedirect(reverse('officials'))
                        except:
                            messages.error(request, 'Official already exists!')
                else:
                    try:
                        official_form.save()
                        messages.success(request, 'Official successfully added!')
                        return HttpResponseRedirect(reverse('officials'))
                    except:
                        messages.error(request, 'Official already exists!')
        else:
            messages.error(request, 'Error adding official')
    else:
        official_form = forms.BrgyOfficialForm()
    context = {'segment': {'officials', 'add'}, 'form': official_form}
    html_template = loader.get_template('home/officials/official_data.html')
    return HttpResponse(html_template.render(context, request))


def official_edit(request, id=0):
    official = models.BrgyOfficial.objects.get(id=id)
    if request.method == 'POST':
        official_form = forms.BrgyOfficialForm(request.POST, instance=official)
        if official_form.is_valid():
            start_term = official_form.cleaned_data['start_term']
            end_term = official_form.cleaned_data['end_term']

            if start_term.year > end_term.year:
                messages.error(request, 'Start term must be less than end term!')
            elif start_term.year > datetime.now().year:
                messages.error(request, 'Start term must be less than or equal the current year!')
            else:
                try:
                    official_form.save()
                    messages.success(request, 'Official successfully updated!')
                    return HttpResponseRedirect(reverse('officials'))
                except:
                    messages.error(request, 'Error updating official')
        else:
            messages.error(request, 'Error updating official')
    else:
        official_form = forms.BrgyOfficialForm(instance=official)
    context = {'segment': {'officials', 'update'}, 'form': official_form, 'official': official}
    html_template = loader.get_template('home/officials/official_data.html')
    return HttpResponse(html_template.render(context, request))


def official_view(request, id=0):
    official = models.BrgyOfficial.objects.get(id=id)
    context = {'segment': {'officials', 'view'}, 'official': official}
    html_template = loader.get_template('home/officials/official_view.html')
    return HttpResponse(html_template.render(context, request))

def user_ui(request):
    gallery = models.Gallery.objects.all()
    context = {'segment': {'user_ui'}, 'photos': gallery}
    return render(request, 'user_ui/user_index.html', context)


def organizations(request):
    orgs = models.BrgyOrganization.objects.all()
    context = {'segment': {'org', 'brgy_info'}, 'orgs': orgs}
    html_template = loader.get_template('home/orgs/org_list.html')
    return HttpResponse(html_template.render(context, request))


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

def announcements(request):
    announcements = models.Announcement.objects.all()
    context = {'segment': {'announcements'}, 'announcements': announcements}
    html_template = loader.get_template('home/announcements/announcement_list.html')
    return HttpResponse(html_template.render(context, request))


def announcement_data(request):
    orgs = models.BrgyOrganization.objects.all()
    if request.method == 'POST':
        announcement_form = forms.AnnouncementForm(request.POST)
        if announcement_form.is_valid():
            _data = announcement_form.save(commit=False)
            send_to = request.POST['recipient']
            print(send_to)

            message = request.POST['content']
            numbers = None
            if(send_to == 'ALL'):
                numbers = models.Resident.objects.values_list('phone_no1', flat=True)
            else:
                org_id = models.BrgyOrganization.objects.get(org_name=send_to).id
                numbers = models.OrgMember.objects.filter(org_id=org_id).values_list('member__phone_no1', flat=True)

            message += '\n\n' + '- Sent by ' + request.user.first_name + ' ' + request.user.last_name + ' via Barangay Masili Portal'
            if numbers.count() > 0:
                for number in numbers:
                    sms_sender.send_sms(number, message)
                sleep(3)
                _data.status = 'SENT'
                messages.success(request, 'Announcement has been delivered!')
            else:
                messages.error(request, 'No recipients found!')

            _data.send_to = send_to
            _data.posted_by = request.user.first_name + ' ' + request.user.last_name
            _data.save()
            return HttpResponseRedirect(reverse('announcements'))
        else:
            messages.error(request, 'Error adding announcement!')

    announcement_form = forms.AnnouncementForm()
    context = {'segment': {'announcements', 'add'}, 'form': announcement_form, 'organization': orgs}
    html_template = loader.get_template('home/announcements/announcement_data.html')
    return HttpResponse(html_template.render(context, request))


def gallery(request):
    gallery = models.Gallery.objects.all()
    context = {'segment': {'gallery'}, 'gallery': gallery}
    html_template = loader.get_template('home/gallery/gallery.html')
    return HttpResponse(html_template.render(context, request))


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


def ordinances(request):
    ordinances = models.Ordinance.objects.all()
    context = {'segment': {'ordinances'}, 'ordinances': ordinances}
    html_template = loader.get_template('home/ordinances/ordinances_list.html')
    return HttpResponse(html_template.render(context, request))


def ordinance_data(request):
    officials = models.BrgyOfficial.objects.all()
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

            files = request.FILES.getlist('files')
            for file in files:
                _data.files = file
                _data.save()

            _data.save()

            messages.success(request, 'Ordinance successfully added!')
            return HttpResponseRedirect(reverse('ordinances'))
        else:
            messages.error(request, 'Error adding ordinance!')
    context = {'segment': {'ordinances', 'add'}, 'form': forms.OrdinanceForm, 'ordinance_no': ordinance_no, 'officials': officials}
    html_template = loader.get_template('home/ordinances/ordinance_data.html')
    return HttpResponse(html_template.render(context, request))


def ordinance_view(request, id=0):
    ordinance = models.Ordinance.objects.get(id=id)
    attest_by = ordinance.attested_by.split(',')

    year = ordinance.date_posted.year

    context = {'segment': {'ordinances', 'view'}, 'ordinance': ordinance, 'year': year, 'attest_by': attest_by}
    html_template = loader.get_template('home/ordinances/ordinance_view.html')
    return HttpResponse(html_template.render(context, request))


def residents(request):
    residents = models.Resident.objects.all()
    puroks = models.Purok.objects.all()


    # get the number or residents per purok
    purok_residents = []
    for purok in puroks:
        purok_residents.append(models.Resident.objects.filter(purok=purok).count())
    count = residents.count()
    context = {'segment': {'residents'}, 'residents': residents, 'count': count, 'puroks': puroks, 'purok_residents': purok_residents}
    html_template = loader.get_template('home/residents/residents_list.html')
    return HttpResponse(html_template.render(context, request))


def resident_view(request, id):
    resident = models.Resident.objects.get(id=id)
    emergency = models.EmergencyContact.objects.filter(resident=resident)
    print(emergency)
    context = {'segment': {'residents', 'view'}, 'resident': resident, 'emergency': emergency}
    html_template = loader.get_template('home/residents/resident_view.html')
    return HttpResponse(html_template.render(context, request))


def resident_data(request):
    residents = models.Resident.objects.all()
    resident_count = residents.count()
    if resident_count == 0:
        resident_no = 'MASILI-RES-0001'
    else:
        last_resident = residents.last()
        resident_no = last_resident.resident_no
        resident_no = resident_no.split('-')
        resident_no = 'MASILI-RES-' + str(int(resident_no[1]) + 1).zfill(4)

    if request.method == 'POST':
        resident_form = forms.ResidentForm(request.POST, request.FILES)
        emergency_form = forms.EmergencyContactForm(request.POST)
        if resident_form.is_valid():
            _data = resident_form.save(commit=False)
            _data.resident_no = resident_no
            resident_form.save()

            _emergency = emergency_form.save(commit=False)
            _emergency.resident = _data
            emergency_form.save()
            messages.success(request, 'Resident successfully added!')
            return HttpResponseRedirect(reverse('residents'))
        else:
            messages.error(request, 'Error adding resident!')

    form = forms.ResidentForm()
    context = {'segment': {'residents', 'add'}, 'form': form, 'resident_no': resident_no, 'emergency_form': forms.EmergencyContactForm}
    html_template = loader.get_template('home/residents/resident_data.html')
    return HttpResponse(html_template.render(context, request))


def resident_edit(request, id):
    resident = models.Resident.objects.get(id=id)
    emergency = models.EmergencyContact.objects.filter(resident=resident)
    if request.method == 'POST':
        resident_form = forms.ResidentForm(request.POST, request.FILES, instance=resident)
        emergency_form = forms.EmergencyContactForm(request.POST, instance=emergency[0])
        if resident_form.is_valid():
            resident_form.save()
            emergency_form.save()
            messages.success(request, 'Resident successfully updated!')
            return HttpResponseRedirect(reverse('residents'))
        else:
            messages.error(request, 'Error updating resident!')

    context = {'segment': {'residents', 'edit'}, 'form': forms.ResidentForm(instance=resident), 'resident': resident, 'emergency_form': forms.EmergencyContactForm(instance=emergency[0])}
    html_template = loader.get_template('home/residents/resident_edit.html')
    return HttpResponse(html_template.render(context, request))

