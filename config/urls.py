# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - Master URL Configuration
"""

import os
from pathlib import Path
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponseNotFound

BASE_DIR = settings.BASE_DIR

def serve_any_static(request, path):
    # Try different static locations
    search_dirs = [
        BASE_DIR / 'mag' / 'uploads',
        BASE_DIR / 'assets',
        BASE_DIR / 'fonts',
        BASE_DIR / 'mag',
        BASE_DIR / 'portal',
        BASE_DIR,
    ]
    for d in search_dirs:
        candidate = d / path
        if candidate.exists() and candidate.is_file():
            return serve(request, path, document_root=str(d))
    return HttpResponseNotFound("Asset Not Found")

urlpatterns = [
    # 1. Django Admin
    path('django-admin/', admin.site.urls),

    # 2. Pezeshkan Core Application URLs (HTML pages + APIs)
    path('', include('apps.pezeshkan_core.urls')),

    # 3. Direct Static & Media File Servicing
    re_path(r'^uploads/(?P<path>.*)$', serve, {'document_root': str(settings.MEDIA_ROOT)}),
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': str(BASE_DIR / 'assets')}),
    re_path(r'^fonts/(?P<path>.*)$', serve, {'document_root': str(BASE_DIR / 'fonts')}),
    re_path(r'^(?P<path>(css|js|images)/.*)$', serve_any_static),
]
