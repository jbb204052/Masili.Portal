from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from . import models
from . import forms

from django.forms import formset_factory


@login_required(login_url="/login/")
def index(request):
    officials_count = models.BrgyOfficial.objects.count()
    context = {'segment': 'index', 'officials_count': officials_count}
    if request.user.profile.is_superadmin:
        html_template = loader.get_template('home/index.html')
    else:
        html_template = loader.get_template('user_ui/userindex.html')
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
            official_form.save()
            messages.success(request, 'Official successfully added!')
            return HttpResponseRedirect(reverse('officials'))
        else:
            messages.error(request, 'Official already exists!')
    else:
        official_form = forms.BrgyOfficialForm()
    context = {'segment': {'officials', 'add'}, 'form': official_form}
    html_template = loader.get_template('home/officials/official_data.html')
    return HttpResponse(html_template.render(context, request))


def official_edit(request):
    return None


def official_view(request):
    return None

# Residents
def hotline_view1(request):
    context = {'segment': {'user_ui'}}
    # html_template = loader.get_template('home/user_ui/userindex')
    # return HttpResponse(html_template.render(context, request))
    return render(request, 'home/user_ui/userindex')


def user_ui(request):
    return None