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

    # OFFICIALS
    path('officials/', views.officials, name='officials'),
    path('officials/add/', views.official_data, name='official_add'),
    path('officials/edit/<int:id>/', views.official_edit, name='official_edit'),
    path('officials/view/<int:id>/', views.official_view, name='official_view'),


    # RESIDENTS
    path('user_ui/', views.user_ui, name='user_ui')
]
