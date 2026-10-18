# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - URL Routing Specification
"""

from django.urls import path, re_path
from apps.pezeshkan_core import views

urlpatterns = [
    # 1. Root & Main Landing
    path('', views.index_page, name='index'),

    # 2. Magazine & Portal HTML Pages
    path('mag/', views.magazine_page, name='magazine_index'),
    path('mag/<path:path>', views.magazine_page, name='magazine_subpage'),
    path('admin.html', views.admin_page, name='admin_panel'),
    path('mag/admin.html', views.admin_page, name='mag_admin_panel'),
    path('appointments', views.appointments_page, name='appointments_portal'),
    path('portal/appointments.html', views.appointments_page, name='portal_appointments_html'),
    path('portal/', views.portal_page, name='portal_index'),
    path('portal/<path:path>', views.portal_page, name='portal_subpage'),

    # 3. Authentication APIs
    path('api/login', views.api_login, name='api_login'),
    path('api/logout', views.api_logout, name='api_logout'),
    path('api/me', views.api_me, name='api_me'),

    # 4. Clinical Data APIs
    path('api/pillars', views.api_pillars, name='api_pillars'),
    path('api/doctors', views.api_doctors, name='api_doctors'),
    path('api/articles', views.api_articles, name='api_articles'),
    path('api/articles/<str:slug>', views.api_articles, name='api_article_detail'),

    # 5. Appointments & Booking APIs
    path('api/appointments', views.api_appointments, name='api_appointments'),
    path('api/admin/appointments', views.api_admin_appointments, name='api_admin_appointments'),

    # 6. Settings, Media, Redirects APIs
    path('api/settings', views.api_settings, name='api_settings'),
    path('api/media', views.api_media, name='api_media'),
    path('api/media/upload', views.api_media, name='api_media_upload'),
    path('api/redirects', views.api_redirects, name='api_redirects'),

    # 7. Newsletters, Subscribers, Schemas, CRM APIs
    path('api/newsletters', views.api_newsletters, name='api_newsletters'),
    path('api/subscribers', views.api_subscribers, name='api_subscribers'),
    path('api/schemas', views.api_schemas, name='api_schemas'),
    path('api/admin/schemas/validate', views.api_schema_validate, name='api_schema_validate'),
    path('api/crm-tutorials', views.api_crm_tutorials, name='api_crm_tutorials'),
]
