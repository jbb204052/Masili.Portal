# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('tinymce/', include('tinymce.urls')),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

    # HOTLINES
    path('hotlines/', views.hotlines, name='hotlines'),
    path('hotlines/add/', views.hotline_data, name='hotline_add'),
    path('hotlines/edit/<int:id>/', views.hotline_edit, name='hotline_edit'),
    path('hotlines/view/<int:id>/', views.hotline_view, name='hotline_view'),
    path('hotlines/delete/<int:id>/', views.hotline_delete, name='hotline_delete'),

    # ANNOUNCEMENT
    path('announcements/<str:opt>', views.announcements, name='announcements'),
    path('announcements/new/', views.announcement_data, name='announcement_add'),
    path('announcements/view/<int:id>/', views.announcement_view, name='announcement_view'),
    path('announcements/approve/<int:id>/', views.announcement_approve, name='announcement_approve'),

    # ORGANIZATIONS
    path('organizations/', views.organizations, name='organizations'),
    path('organizations/add/', views.organization_data, name='organization_add'),
    path('organizations/edit/<int:id>/', views.organization_edit, name='organization_edit'),

    # GALLERY
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/upload/', views.gallery_upload, name='gallery_upload'),
    path('dropzone-image/', views.dropzone_image, name='dropzone-image'),

    # ORDINANCES
    path('ordinances/', views.ordinances, name='ordinances'),
    path('ordinances/add/', views.ordinance_data, name='ordinance_add'),
    path('ordinances/view/<int:id>/', views.ordinance_view, name='ordinance_view'),
    path('ordinances/edit/<int:id>/', views.ordinance_edit, name='ordinance_edit'),

    # RESIDENTS
    path('residents/', views.residents, name='residents'),
    path('residents/add/', views.resident_data, name='resident_add'),
    path('residents/view/<int:id>/', views.resident_view, name='resident_view'),
    path('residents/edit/<int:id>/', views.resident_edit, name='resident_edit'),
    path('residents/forapproval/', views.residents_for_approval, name='residents_for_approval'),
    path('residents/approve/<int:id>/', views.resident_approve, name='resident_approve'),


    # OFFICIALS
    path('officials/', views.officials, name='officials'),
    path('officials/add', views.official_data, name='official_add'),
    path('officials/view/<int:id>/', views.official_view, name='official_view'),
    path('officials/update/<int:id>/', views.official_update, name='official_update'),

    # BLOTTERS
    path('blotters/', views.blotters, name='blotters'),
    path('blotters/add/', views.blotter_data, name='blotter_add'),
    path('blotters/view/<int:id>/', views.blotter_view, name='blotter_view'),
    path('blotters/print/<int:id>/', views.blotter_print, name='blotter_print'),

    # Hearing
    path('hearing/add/<int:id>/<str:blotter_no>/', views.hearing, name='hearing'),



    # CUSTOM URL
    path('index/', views.user_ui, name='user_ui'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about, name='about'),


    # SESSIONS
    path('brgy_sessions/', views.brgy_sessions, name='brgy_sessions'),
    path('brgy_sessions/add/', views.brgy_session_data, name='brgy_session_add'),
    path('brgy_sessions/view/<int:id>', views.brgy_session_view, name="brgy_session_view"),



    # CERTIFICATES AND PERMITS
    path('certificates/', views.certificates, name='certificates'),
    path('certificates/certificate_of_indigency/view', views.certificate_of_indigency_view, name="indigency"),
    path('certificate/add/certificate_of_indigency', views.certificate_of_indigency_data, name="indigency_add"),
    path('certificate/certificate_of_indigency/view/<int:id>', views.indigency_print, name="cert_indigency"),
    path('certificates/issued/<int:id>', views.issued_certificates, name='issued_certificates'),
    path('certificates/print/<int:id>', views.printed_certificate, name='printed_certificate'),

    path('certificates/request', views.request_certificates, name='request_certificates'),


    # NOTIFICATION
    path('notifications/read/<int:id>', views.notification, name='notification_read'),
    path('notifications/mark_all_as_read', views.notification_read_all, name='notification_read_all'),


    # NEWS
    path('news/', views.news, name='news'),
    path('news/add/', views.news_data, name='news_add'),
    path('news/view/<int:id>', views.news_view, name='news_view'),
    path('news/read/<int:id>/<str:title>', views.news_read, name='news_read'),
    path('news/update/<int:id>', views.news_update, name='news_update'),



    # BUSINESS PERMIT
    path('business_permit/', views.business_permit, name='business_permit'),
    path('business_permit/add/', views.business_permit_data, name='business_permit_add'),
    path('business_permit/view/<int:id>', views.business_permit_view, name='business_permit_view'),
    path('business_permit/print/<int:id>', views.business_permit_print, name='permit_print'),
    path('business_permit/issued/<int:id>', views.issued_business_permit, name='issued_business_permit'),

    path('business_permit/business_closure/add/', views.business_closure_data, name='business_closure_add'),

]
