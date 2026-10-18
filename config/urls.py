# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - Master URL Configuration
Routes All Clinical APIs, Portal Pages, Magazine SPA, and Universal Static Assets
"""

from django.contrib import admin
from django.urls import path, include, re_path
from apps.pezeshkan_core import views

urlpatterns = [
    # 1. Django Admin
    path('django-admin/', admin.site.urls),

    # 2. Pezeshkan Core Application URLs (HTML pages + APIs)
    path('', include('apps.pezeshkan_core.urls')),

    # 3. Universal Direct Static & Asset Servicing (shared.css, shared.js, logos, fonts, uploads, etc.)
    re_path(r'^(?P<path>.+\.(css|js|svg|png|jpg|jpeg|webp|woff2|woff|ttf|xml|webmanifest|txt|ico|json))$', views.serve_static_asset, name='static_asset'),
]
