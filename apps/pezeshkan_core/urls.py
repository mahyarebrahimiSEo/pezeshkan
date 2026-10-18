# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - Complete URL Routing Specification
"""

from django.urls import path, re_path
from apps.pezeshkan_core import views

urlpatterns = [
    # 1. Root Homepage
    path('', views.index_page, name='index'),

    # 2. Portal Pages (Clean Canonical URLs)
    path('product', views.portal_page, {'page_name': 'product'}, name='product'),
    path('features', views.portal_page, {'page_name': 'features'}, name='features'),
    path('packages', views.portal_page, {'page_name': 'packages'}, name='packages'),
    path('start', views.portal_page, {'page_name': 'start'}, name='start'),
    path('services', views.portal_page, {'page_name': 'services'}, name='services'),
    path('about', views.portal_page, {'page_name': 'about'}, name='about'),
    path('contact', views.portal_page, {'page_name': 'contact'}, name='contact'),
    path('tutorials', views.portal_page, {'page_name': 'tutorials'}, name='tutorials'),
    path('download', views.portal_page, {'page_name': 'download'}, name='download'),
    path('appointments', views.appointments_page, name='appointments_portal'),
    path('portal/appointments.html', views.appointments_page, name='portal_appointments_html'),
    path('portal/', views.portal_page, name='portal_index'),
    path('portal/<path:path>', views.portal_page, name='portal_subpage'),

    # 3. Magazine SPA & Administration Pages
    path('mag', views.magazine_page, name='magazine_root'),
    path('mag/', views.magazine_page, name='magazine_index'),
    path('mag/newsletter', views.magazine_page, {'path': 'newsletter'}, name='mag_newsletter'),
    path('mag/<path:path>', views.magazine_page, name='magazine_subpage'),
    path('admin', views.admin_page, name='admin_root'),
    path('admin/', views.admin_page, name='admin_slash'),
    path('admin.html', views.admin_page, name='admin_panel'),
    path('mag/admin.html', views.admin_page, name='mag_admin_panel'),
    path('login', views.login_page, name='login'),
    path('login/', views.login_page, name='login_slash'),
    path('mag/login', views.login_page, name='mag_login'),
    path('mag/login.html', views.login_page, name='mag_login_html'),

    # 4. Authentication APIs
    path('api/login', views.api_login, name='api_login'),
    path('api/logout', views.api_logout, name='api_logout'),
    path('api/me', views.api_me, name='api_me'),

    # 5. Clinical Data APIs
    path('api/pillars', views.api_pillars, name='api_pillars'),
    path('api/doctors', views.api_doctors, name='api_doctors'),
    path('api/articles', views.api_articles, name='api_articles'),
    path('api/articles/<str:slug>', views.api_articles, name='api_article_detail'),

    # 6. Appointments & Booking APIs
    path('api/appointments', views.api_appointments, name='api_appointments'),
    path('api/admin/appointments', views.api_admin_appointments, name='api_admin_appointments'),

    # 7. Settings, Media, Redirects APIs
    path('api/settings', views.api_settings, name='api_settings'),
    path('api/media', views.api_media, name='api_media'),
    path('api/media/upload', views.api_media, name='api_media_upload'),
    path('api/redirects', views.api_redirects, name='api_redirects'),

    # 8. Newsletters, Subscribers, Schemas, CRM APIs
    path('api/newsletters', views.api_newsletters, name='api_newsletters'),
    path('api/subscribers', views.api_subscribers, name='api_subscribers'),
    path('api/schemas', views.api_schemas, name='api_schemas'),
    path('api/admin/schemas/validate', views.api_schema_validate, name='api_schema_validate'),
    path('api/crm-tutorials', views.api_crm_tutorials, name='api_crm_tutorials'),
]
