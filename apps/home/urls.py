# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

    # HOTLINES
    path('hotlines/', views.hotlines, name='hotlines'),
    path('hotlines/add/', views.hotline_data, name='hotline_add'),
    path('hotlines/edit/<int:id>/', views.hotline_edit, name='hotline_edit'),
    path('hotlines/view/<int:id>/', views.hotline_view, name='hotline_view'),
    path('hotlines/delete/<int:id>/', views.hotline_delete, name='hotline_delete'),

    # ANNOUNCEMENT
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/new/', views.announcement_data, name='announcement_add'),

    # ORGANIZATIONS
    path('organizations/', views.organizations, name='organizations'),
    path('organizations/add/', views.organization_data, name='organization_add'),
    path('organizations/edit/<int:id>/', views.organization_edit, name='organization_edit'),



    # GALLERY
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/upload/', views.gallery_upload, name='gallery_upload'),

    # OFFICIALS
    path('officials/', views.officials, name='officials'),
    path('officials/add/', views.official_data, name='official_add'),
    path('officials/edit/<int:id>/', views.official_edit, name='official_edit'),
    path('officials/view/<int:id>/', views.official_view, name='official_view'),


    path('user_ui/', views.user_ui, name='user_ui'),


    # ORDINANCES
    path('ordinances/', views.ordinances, name='ordinances'),
    path('ordinances/add/', views.ordinance_data, name='ordinance_add'),
    path('ordinances/view/<int:id>/', views.ordinance_view, name='ordinance_view'),

    # RESIDENTS
    path('residents/', views.residents, name='residents'),
    path('residents/add/', views.resident_data, name='resident_add'),
    path('residents/view/<int:id>/', views.resident_view, name='resident_view'),
    path('residents/edit/<int:id>/', views.resident_edit, name='resident_edit'),

]
