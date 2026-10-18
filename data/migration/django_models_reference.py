# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - Django Models Architecture
Direct 1:1 mapping with current Pezeshkan JSON databases & REST API endpoints.
Ensures zero frontend changes when transitioning backend to Django 5.x.
"""

from django.db import models


class Pillar(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام ستون")
    short_name = models.CharField(max_length=100, blank=True, verbose_name="نام کوتاه")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    icon = models.CharField(max_length=100, blank=True, verbose_name="آیکون")
    count_badge = models.CharField(max_length=50, blank=True)
    intent = models.CharField(max_length=100, blank=True)
    dept = models.CharField(max_length=100, blank=True)
    desc = models.TextField(blank=True, verbose_name="توضیحات")
    chips = models.JSONField(default=list, blank=True)
    branches = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "pezeshkan_pillars"
        verbose_name = "ستون تخصصی"
        verbose_name_plural = "ستون‌های تخصصی"

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام پزشک")
    title = models.CharField(max_length=255, verbose_name="عنوان و تخصص")
    mc_number = models.CharField(max_length=100, blank=True, verbose_name="شماره نظام پزشکی")
    dept = models.CharField(max_length=100, blank=True, verbose_name="بخش")
    pillar_slug = models.CharField(max_length=100, blank=True, verbose_name="اسلاگ ستون")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    reviews_count = models.IntegerField(default=0)
    avatar = models.TextField(blank=True, verbose_name="تصویر پزشک")
    available = models.BooleanField(default=True, verbose_name="در دسترس")
    work_hours = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True, verbose_name="آدرس مطب")
    phone = models.CharField(max_length=50, blank=True, verbose_name="تلفن تماس")
    time_slots = models.JSONField(default=list, blank=True)
    services = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "pezeshkan_doctors"
        verbose_name = "پزشک"
        verbose_name_plural = "پزشکان"

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = (
        ("published", "منتشر شده"),
        ("draft", "پیش‌نویس"),
        ("archived", "بایگانی"),
    )
    title = models.CharField(max_length=500, verbose_name="عنوان مقاله")
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    summary = models.TextField(blank=True, verbose_name="خلاصه")
    raw_html = models.TextField(blank=True)
    content_html = models.TextField(verbose_name="متن مقاله (HTML)")
    image = models.TextField(blank=True, verbose_name="تصویر شاخص")
    image_alt = models.CharField(max_length=500, blank=True)
    pillar_id = models.CharField(max_length=50, blank=True)
    category_name = models.CharField(max_length=100, blank=True)
    category_icon = models.CharField(max_length=100, blank=True)
    doctor_id = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=255, default="تیم تحریریه پزشکان")
    read_time = models.CharField(max_length=50, default="۵ دقیقه")
    last_reviewed = models.CharField(max_length=100, blank=True)
    tag = models.CharField(max_length=100, blank=True)
    tag_class = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="published")
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    focus_keyword = models.CharField(max_length=255, blank=True)
    faqs = models.JSONField(default=list, blank=True)
    schema_type = models.CharField(max_length=100, default="MedicalWebPage")
    old_slugs = models.JSONField(default=list, blank=True)
    schema_data = models.JSONField(default=dict, blank=True)
    custom_schema_json = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pezeshkan_articles"
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title


class Appointment(models.Model):
    STATUS_CHOICES = (
        ("pending", "در انتظار بررسی"),
        ("confirmed", "تایید شده"),
        ("cancelled", "لغو شده"),
        ("completed", "انجام شده"),
    )
    tracking_code = models.CharField(max_length=32, unique=True, verbose_name="کد رهگیری")
    doctor_id = models.CharField(max_length=50, verbose_name="شناسه پزشک")
    doctor_name = models.CharField(max_length=255, blank=True, verbose_name="نام پزشک")
    patient_name = models.CharField(max_length=255, verbose_name="نام بیمار")
    patient_phone = models.CharField(max_length=50, verbose_name="تلفن بیمار")
    national_id = models.CharField(max_length=50, blank=True, verbose_name="کد ملی")
    date_label = models.CharField(max_length=100, verbose_name="تاریخ نوبت")
    time_slot = models.CharField(max_length=100, verbose_name="ساعت نوبت")
    notes = models.TextField(blank=True, verbose_name="یادداشت")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pezeshkan_appointments"
        verbose_name = "نوبت پزشکی"
        verbose_name_plural = "نوبت‌های پزشکی"
        indexes = [
            models.Index(fields=["doctor_id", "date_label", "time_slot"]),
            models.Index(fields=["patient_phone"]),
        ]

    def __str__(self):
        return f"{self.tracking_code} - {self.patient_name} ({self.date_label} {self.time_slot})"


class MediaItem(models.Model):
    filename = models.CharField(max_length=255, verbose_name="نام فایل")
    url = models.TextField(verbose_name="آدرس فایل")
    variants = models.JSONField(default=dict, blank=True)
    dimensions = models.JSONField(default=dict, blank=True)
    format = models.CharField(max_length=20, default="webp")
    size = models.BigIntegerField(default=0)
    original_size = models.BigIntegerField(default=0)
    saved_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    storage = models.CharField(max_length=50, default="local")
    alt = models.CharField(max_length=500, blank=True)
    title = models.CharField(max_length=500, blank=True)
    caption = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pezeshkan_media"
        verbose_name = "فایل چندرسانه‌ای"
        verbose_name_plural = "کتابخانه رسانه‌ها"


class Redirect(models.Model):
    source = models.CharField(max_length=500, unique=True)
    target = models.CharField(max_length=500)
    status_code = models.IntegerField(default=301)
    match_type = models.CharField(max_length=50, default="exact")
    preserve_query = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    hit_count = models.BigIntegerField(default=0)
    last_hit = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pezeshkan_redirects"


class SiteSetting(models.Model):
    site_title = models.CharField(max_length=255, default="پزشکان - مجله جامع سلامت")
    site_subtitle = models.CharField(max_length=255, blank=True)
    editorial_leader = models.CharField(max_length=255, blank=True)
    announcement_banner = models.TextField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    emergency_triage_enabled = models.BooleanField(default=True)
    seo = models.JSONField(default=dict, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pezeshkan_settings"
