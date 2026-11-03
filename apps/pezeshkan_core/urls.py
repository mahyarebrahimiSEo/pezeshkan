# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - Complete URL Routing Specification
"""

from django.urls import path, re_path
from apps.pezeshkan_core import views

urlpatterns = [
    # 1. Root Homepage
    path('', views.index_page, name='index'),

    # 2. Portal Pages (Clean Canonical URLs - supports with/without trailing slash and optional .html)
    re_path(r'^product(?:\.html)?/?$', views.portal_page, {'page_name': 'product'}, name='product'),
    re_path(r'^features(?:\.html)?/?$', views.portal_page, {'page_name': 'features'}, name='features'),
    re_path(r'^packages(?:\.html)?/?$', views.portal_page, {'page_name': 'packages'}, name='packages'),
    re_path(r'^start(?:\.html)?/?$', views.portal_page, {'page_name': 'start'}, name='start'),
    re_path(r'^services(?:\.html)?/?$', views.portal_page, {'page_name': 'services'}, name='services'),
    re_path(r'^about(?:\.html)?/?$', views.portal_page, {'page_name': 'about'}, name='about'),
    re_path(r'^contact(?:\.html)?/?$', views.portal_page, {'page_name': 'contact'}, name='contact'),
    re_path(r'^tutorials(?:\.html)?/?$', views.portal_page, {'page_name': 'tutorials'}, name='tutorials'),
    re_path(r'^download(?:\.html)?/?$', views.portal_page, {'page_name': 'download'}, name='download'),
    re_path(r'^appointments(?:\.html)?/?$', views.appointments_page, name='appointments_portal'),
    re_path(r'^portal/appointments(?:\.html)?/?$', views.appointments_page, name='portal_appointments_html'),
    re_path(r'^service-appointments(?:\.html)?/?$', views.portal_page, {'page_name': 'service-appointments'}, name='service_appointments'),
    re_path(r'^service-emr(?:\.html)?/?$', views.portal_page, {'page_name': 'service-emr'}, name='service_emr'),
    re_path(r'^service-physio(?:\.html)?/?$', views.portal_page, {'page_name': 'service-physio'}, name='service_physio'),
    re_path(r'^service-sms-crm(?:\.html)?/?$', views.portal_page, {'page_name': 'service-sms-crm'}, name='service_sms_crm'),
    re_path(r'^service-accounting(?:\.html)?/?$', views.portal_page, {'page_name': 'service-accounting'}, name='service_accounting'),
    re_path(r'^portal/(?P<page_name>[a-zA-Z0-9_\-]+)(?:\.html)?/?$', views.portal_page, name='portal_page_html'),
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
    path('api/newsletter-doctors', views.api_newsletter_doctors, name='api_newsletter_doctors'),
    path('api/newsletter-doctors/', views.api_newsletter_doctors, name='api_newsletter_doctors_slash'),
    path('api/newsletter-doctors/<str:doc_id>', views.api_newsletter_doctors, name='api_newsletter_doctor_detail'),
    path('api/newsletter-doctors/<str:doc_id>/', views.api_newsletter_doctors, name='api_newsletter_doctor_detail_slash'),
    path('api/articles', views.api_articles, name='api_articles'),
    path('api/articles/<str:slug>', views.api_articles, name='api_article_detail'),

    # 6. Appointments & Booking APIs
    path('api/appointments', views.api_appointments, name='api_appointments'),
    path('api/admin/appointments', views.api_admin_appointments, name='api_admin_appointments'),

    # 7. Settings, Media, Redirects APIs
    path('api/settings', views.api_settings, name='api_settings'),
    path('api/site-images', views.api_site_images, name='api_site_images'),
    path('api/site-images/', views.api_site_images, name='api_site_images_slash'),
    path('api/media', views.api_media, name='api_media'),
    path('api/media/upload', views.api_upload, name='api_media_upload'),
    path('api/upload', views.api_upload, name='api_upload'),
    path('api/upload/', views.api_upload, name='api_upload_slash'),
    path('api/redirects', views.api_redirects, name='api_redirects'),

    # 8. Newsletters, Subscribers, Schemas, CRM APIs
    path('api/newsletters', views.api_newsletters, name='api_newsletters'),
    path('api/subscribers', views.api_subscribers, name='api_subscribers'),
    path('api/schemas', views.api_schemas, name='api_schemas'),
    path('api/admin/schemas/validate', views.api_schema_validate, name='api_schema_validate'),
    path('api/crm-tutorials', views.api_crm_tutorials, name='api_crm_tutorials'),

    # 9. Blueprint 2.2.0 Integration Routes
    # FLOW_01: Doctor Directory & Quick Booking Bridge
    path('api/v1/clinic/public/directory/', views.api_clinic_directory, name='api_v1_clinic_directory'),
    path('api/v1/clinic/public/directory', views.api_clinic_directory, name='api_v1_clinic_directory_noslash'),
    path('api/directory', views.api_clinic_directory, name='api_directory'),

    # FLOW_02: Subscription Plans
    path('api/v1/platform/public/plans/', views.api_platform_plans, name='api_v1_platform_plans'),
    path('api/v1/platform/public/plans', views.api_platform_plans, name='api_v1_platform_plans_noslash'),
    path('api/packages', views.api_platform_plans, name='api_packages'),

    # FLOW_03: Clinic Onboarding Leads (/start)
    path('api/v1/leads/start/', views.api_leads_start, name='api_v1_leads_start'),
    path('api/v1/leads/start', views.api_leads_start, name='api_v1_leads_start_noslash'),
    path('api/start-lead', views.api_leads_start, name='api_start_lead'),
    path('api/admin/leads', views.api_admin_leads, name='api_admin_leads'),

    # 10. SEO Watchdog, Site Structure, Robots, LLMs, Users
    path('api/admin/seo-audit', views.api_seo_audit, name='api_seo_audit'),
    path('api/admin/site-structure', views.api_site_structure, name='api_site_structure'),
    path('api/admin/site-structure/analyze', views.api_site_structure, name='api_site_structure_analyze'),
    path('sitemap.xml', views.sitemap_xml_view, name='sitemap_xml'),
    path('api/admin/sitemap', views.api_sitemap, name='api_admin_sitemap'),
    path('api/admin/sitemap/', views.api_sitemap, name='api_admin_sitemap_slash'),
    path('api/admin/sitemap/generate', views.api_sitemap, name='api_admin_sitemap_generate'),
    path('api/admin/robots', views.api_robots, name='api_robots'),
    path('api/admin/robots/analyze', views.api_robots, name='api_robots_analyze'),
    path('api/admin/llms', views.api_llms, name='api_llms'),
    path('api/admin/llms/preview', views.api_llms_preview, name='api_llms_preview'),
    path('api/admin/users', views.api_users, name='api_users'),
]

