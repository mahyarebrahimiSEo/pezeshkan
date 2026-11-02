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

    # 3. Universal Direct Static & Asset Servicing (shared.css, shared.js, logos, fonts, 3D glb models, uploads, etc.)
    re_path(r'^(?P<path>.+\.(css|js|svg|png|jpg|jpeg|webp|woff2|woff|ttf|xml|webmanifest|txt|ico|json|glb|gltf|bin))$', views.serve_static_asset, name='static_asset'),

    # 4. Universal Catch-All 404 Route (handles all unmatched English, Persian, and API URLs gracefully)
    re_path(r'^(?P<unmatched_path>.*)$', views.custom_404_view, name='catch_all_404'),
]

# Custom HTTP error handlers
handler404 = 'apps.pezeshkan_core.views.custom_404_view'
handler500 = 'apps.pezeshkan_core.views.custom_500_view'
