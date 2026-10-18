# -*- coding: utf-8 -*-
"""
Django Admin Registration for Pezeshkan Medical Models
"""

from django.contrib import admin
from apps.pezeshkan_core.models import (
    Pillar, Doctor, Article, Appointment, MediaItem,
    Redirect, SiteSetting, UserAccount, Newsletter,
    Subscriber, Inquiry, CrmTutorial
)

@admin.register(Pillar)
class PillarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'short_name', 'dept')
    search_fields = ('name', 'slug', 'desc')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'mc_number', 'dept', 'rating', 'available')
    list_filter = ('available', 'dept')
    search_fields = ('name', 'title', 'mc_number', 'phone')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'author', 'category_name', 'status', 'last_modified')
    list_filter = ('status', 'category_name', 'schema_type')
    search_fields = ('title', 'slug', 'summary', 'focus_keyword')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'doctor_name', 'patient_name', 'patient_phone', 'date_label', 'time_slot', 'status', 'created_at')
    list_filter = ('status', 'date_label')
    search_fields = ('tracking_code', 'patient_name', 'patient_phone', 'doctor_name')


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'format', 'size', 'storage', 'uploaded_at')
    list_filter = ('format', 'storage')
    search_fields = ('filename', 'title', 'alt')


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'target', 'status_code', 'match_type', 'is_active', 'hit_count', 'last_hit')
    list_filter = ('status_code', 'match_type', 'is_active')
    search_fields = ('source', 'target', 'description')


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'site_title', 'contact_phone', 'emergency_triage_enabled', 'last_updated')


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'display_name', 'email', 'role', 'status')
    list_filter = ('role', 'status')
    search_fields = ('username', 'display_name', 'email')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'date', 'status')
    search_fields = ('title', 'slug')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'category', 'subscribed_at')
    search_fields = ('email', 'name')


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'phone', 'email', 'subject')


@admin.register(CrmTutorial)
class CrmTutorialAdmin(admin.ModelAdmin):
    list_display = ('custom_id', 'title', 'category', 'last_modified')
    search_fields = ('title', 'category')
