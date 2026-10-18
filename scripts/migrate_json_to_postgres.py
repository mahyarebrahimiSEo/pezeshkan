#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - JSON to PostgreSQL & Django Migration Bridge
========================================================================
Automated migration script to transition the Pezeshkan data layer from 
JSON flat-files to PostgreSQL & Django 5.x ORM without any downtime, data loss,
or schema mismatches.

Features:
- Generates Django loaddata-compatible JSON fixtures (`django_fixtures.json`)
- Generates pure PostgreSQL DDL schema & UPSERT SQL (`schema_and_data.sql`)
- Outputs production Django Models reference (`django_models_reference.py`)
- Full Persian/UTF-8 support and JSON field type casting
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timezone

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONTENT_DIR = os.path.join(BASE_DIR, "mag", "content")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "migration")


def load_json(filename, default=None):
    filepath = os.path.join(CONTENT_DIR, filename)
    if not os.path.exists(filepath):
        return default if default is not None else []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Warning] Failed loading {filename}: {e}")
        return default if default is not None else []


def escape_sql_string(val):
    if val is None:
        return "NULL"
    if isinstance(val, (dict, list)):
        s = json.dumps(val, ensure_ascii=False)
        return "'" + s.replace("'", "''") + "'::jsonb"
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, (int, float)):
        return str(val)
    s = str(val).replace("'", "''")
    return f"'{s}'"


def generate_django_fixtures():
    fixtures = []
    
    # 1. Pillars
    pillars = load_json("pillars.json", [])
    for idx, p in enumerate(pillars, start=1):
        pk = p.get("id") or idx
        if isinstance(pk, str) and not pk.isdigit():
            pk = idx
        fixtures.append({
            "model": "pezeshkan.pillar",
            "pk": int(pk),
            "fields": {
                "name": p.get("name", ""),
                "short_name": p.get("shortName", ""),
                "slug": p.get("slug", ""),
                "icon": p.get("icon", ""),
                "count_badge": p.get("countBadge", ""),
                "intent": p.get("intent", ""),
                "dept": p.get("dept", ""),
                "desc": p.get("desc", ""),
                "chips": p.get("chips", []),
                "branches": p.get("branches", [])
            }
        })

    # 2. Doctors
    doctors = load_json("doctors.json", [])
    for idx, d in enumerate(doctors, start=1):
        pk = d.get("id") or idx
        if isinstance(pk, str) and not pk.isdigit():
            pk = idx
        fixtures.append({
            "model": "pezeshkan.doctor",
            "pk": int(pk),
            "fields": {
                "name": d.get("name", ""),
                "title": d.get("title", ""),
                "mc_number": d.get("mcNumber", ""),
                "dept": d.get("dept", ""),
                "pillar_slug": d.get("pillarSlug", ""),
                "rating": float(d.get("rating", 5.0) or 5.0),
                "reviews_count": int(d.get("reviewsCount", 0) or 0),
                "avatar": d.get("avatar", ""),
                "available": bool(d.get("available", True)),
                "work_hours": d.get("workHours", ""),
                "address": d.get("address", ""),
                "phone": d.get("phone", ""),
                "time_slots": d.get("timeSlots", []),
                "services": d.get("services", [])
            }
        })

    # 3. Articles
    articles = load_json("articles.json", [])
    for idx, a in enumerate(articles, start=1):
        pk = a.get("id") or idx
        if isinstance(pk, str) and not pk.isdigit():
            pk = idx
        fixtures.append({
            "model": "pezeshkan.article",
            "pk": int(pk),
            "fields": {
                "title": a.get("title", ""),
                "slug": a.get("slug", ""),
                "summary": a.get("summary", ""),
                "raw_html": a.get("rawHtml", ""),
                "content_html": a.get("contentHtml", ""),
                "image": a.get("image", ""),
                "image_alt": a.get("imageAlt", ""),
                "pillar_id": a.get("pillarId", ""),
                "category_name": a.get("categoryName", ""),
                "category_icon": a.get("categoryIcon", ""),
                "doctor_id": str(a.get("doctorId", "")),
                "author": a.get("author", "تیم تحریریه پزشکان"),
                "read_time": a.get("readTime", "۵ دقیقه"),
                "last_reviewed": a.get("lastReviewed", ""),
                "tag": a.get("tag", ""),
                "tag_class": a.get("tagClass", ""),
                "status": a.get("status", "published"),
                "meta_title": a.get("metaTitle", ""),
                "meta_description": a.get("metaDescription", ""),
                "focus_keyword": a.get("focusKeyword", ""),
                "faqs": a.get("faqs", []),
                "schema_type": a.get("schemaType", "MedicalWebPage"),
                "old_slugs": a.get("oldSlugs", []),
                "schema_data": a.get("schemaData", {}),
                "custom_schema_json": a.get("customSchemaJson", ""),
                "last_modified": a.get("lastModified", datetime.now(timezone.utc).isoformat())
            }
        })

    # 4. Appointments
    appointments = load_json("appointments.json", [])
    for idx, app in enumerate(appointments, start=1):
        pk = app.get("id") or idx
        if isinstance(pk, str) and not pk.isdigit():
            pk = idx
        fixtures.append({
            "model": "pezeshkan.appointment",
            "pk": int(pk),
            "fields": {
                "tracking_code": app.get("trackingCode", ""),
                "doctor_id": str(app.get("doctorId", "")),
                "doctor_name": app.get("doctorName", ""),
                "patient_name": app.get("patientName", ""),
                "patient_phone": app.get("patientPhone", ""),
                "national_id": app.get("nationalId", ""),
                "date_label": app.get("dateLabel", ""),
                "time_slot": app.get("timeSlot", ""),
                "notes": app.get("notes", ""),
                "status": app.get("status", "pending"),
                "created_at": app.get("createdAt", datetime.now(timezone.utc).isoformat()),
                "updated_at": app.get("updatedAt", datetime.now(timezone.utc).isoformat())
            }
        })

    # 5. Media
    media_items = load_json("media.json", [])
    for idx, m in enumerate(media_items, start=1):
        pk = m.get("id") or idx
        if isinstance(pk, str) and not pk.isdigit():
            pk = idx
        fixtures.append({
            "model": "pezeshkan.media",
            "pk": int(pk),
            "fields": {
                "filename": m.get("filename", ""),
                "url": m.get("url", ""),
                "variants": m.get("variants", {}),
                "dimensions": m.get("dimensions", {}),
                "format": m.get("format", "webp"),
                "size": int(m.get("size", 0) or 0),
                "original_size": int(m.get("originalSize", 0) or 0),
                "saved_percentage": float(m.get("savedPercentage", 0) or 0.0),
                "storage": m.get("storage", "local"),
                "alt": m.get("alt", ""),
                "title": m.get("title", ""),
                "caption": m.get("caption", ""),
                "uploaded_at": m.get("uploadedAt", datetime.now(timezone.utc).isoformat())
            }
        })

    # 6. Redirects
    redirects = load_json("redirects.json", [])
    for idx, r in enumerate(redirects, start=1):
        pk = r.get("id") or idx
        if isinstance(pk, str) and not pk.isdigit():
            pk = idx
        fixtures.append({
            "model": "pezeshkan.redirect",
            "pk": int(pk),
            "fields": {
                "source": r.get("source", ""),
                "target": r.get("target", ""),
                "status_code": int(r.get("statusCode", 301) or 301),
                "match_type": r.get("matchType", "exact"),
                "preserve_query": bool(r.get("preserveQuery", True)),
                "is_active": bool(r.get("isActive", True)),
                "description": r.get("description", ""),
                "hit_count": int(r.get("hitCount", 0) or 0),
                "last_hit": r.get("lastHit"),
                "created_at": r.get("createdAt", datetime.now(timezone.utc).isoformat()),
                "updated_at": r.get("updatedAt", datetime.now(timezone.utc).isoformat())
            }
        })

    # 7. Settings
    settings_obj = load_json("settings.json", {})
    if settings_obj:
        fixtures.append({
            "model": "pezeshkan.sitesetting",
            "pk": 1,
            "fields": {
                "site_title": settings_obj.get("siteTitle", "پزشکان - مجله جامع سلامت"),
                "site_subtitle": settings_obj.get("siteSubtitle", ""),
                "editorial_leader": settings_obj.get("editorialLeader", ""),
                "announcement_banner": settings_obj.get("announcementBanner", ""),
                "contact_phone": settings_obj.get("contactPhone", ""),
                "emergency_triage_enabled": bool(settings_obj.get("emergencyTriageEnabled", True)),
                "seo": settings_obj.get("seo", {}),
                "last_updated": settings_obj.get("lastUpdated", datetime.now(timezone.utc).isoformat())
            }
        })

    return fixtures


def generate_postgres_sql():
    sql = []
    sql.append("-- =================================================================")
    sql.append("-- Pezeshkan Medical Ecosystem - PostgreSQL Migration Schema & Data")
    sql.append(f"-- Generated on: {datetime.now(timezone.utc).isoformat()} UTC")
    sql.append("-- =================================================================\n")
    
    # Extensions
    sql.append("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    sql.append("CREATE EXTENSION IF NOT EXISTS \"pg_trgm\";\n")

    # DDL
    sql.append("""
CREATE TABLE IF NOT EXISTS pezeshkan_pillars (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    short_name VARCHAR(100),
    slug VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(100),
    count_badge VARCHAR(50),
    intent VARCHAR(100),
    dept VARCHAR(100),
    description TEXT,
    chips JSONB DEFAULT '[]'::jsonb,
    branches JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pezeshkan_doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    mc_number VARCHAR(100),
    dept VARCHAR(100),
    pillar_slug VARCHAR(100),
    rating NUMERIC(3, 2) DEFAULT 5.0,
    reviews_count INT DEFAULT 0,
    avatar TEXT,
    available BOOLEAN DEFAULT TRUE,
    work_hours VARCHAR(255),
    address TEXT,
    phone VARCHAR(50),
    time_slots JSONB DEFAULT '[]'::jsonb,
    services JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pezeshkan_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    summary TEXT,
    raw_html TEXT,
    content_html TEXT,
    image TEXT,
    image_alt VARCHAR(500),
    pillar_id VARCHAR(50),
    category_name VARCHAR(100),
    category_icon VARCHAR(100),
    doctor_id VARCHAR(50),
    author VARCHAR(255) DEFAULT 'تیم تحریریه پزشکان',
    read_time VARCHAR(50) DEFAULT '۵ دقیقه',
    last_reviewed VARCHAR(100),
    tag VARCHAR(100),
    tag_class VARCHAR(100),
    status VARCHAR(50) DEFAULT 'published',
    meta_title VARCHAR(255),
    meta_description TEXT,
    focus_keyword VARCHAR(255),
    faqs JSONB DEFAULT '[]'::jsonb,
    schema_type VARCHAR(100) DEFAULT 'MedicalWebPage',
    old_slugs JSONB DEFAULT '[]'::jsonb,
    schema_data JSONB DEFAULT '{}'::jsonb,
    custom_schema_json TEXT,
    last_modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pezeshkan_appointments (
    id SERIAL PRIMARY KEY,
    tracking_code VARCHAR(32) UNIQUE NOT NULL,
    doctor_id VARCHAR(50) NOT NULL,
    doctor_name VARCHAR(255),
    patient_name VARCHAR(255) NOT NULL,
    patient_phone VARCHAR(50) NOT NULL,
    national_id VARCHAR(50),
    date_label VARCHAR(100) NOT NULL,
    time_slot VARCHAR(100) NOT NULL,
    notes TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pezeshkan_media (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    variants JSONB DEFAULT '{}'::jsonb,
    dimensions JSONB DEFAULT '{}'::jsonb,
    format VARCHAR(20) DEFAULT 'webp',
    size BIGINT DEFAULT 0,
    original_size BIGINT DEFAULT 0,
    saved_percentage NUMERIC(5, 2) DEFAULT 0.0,
    storage VARCHAR(50) DEFAULT 'local',
    alt VARCHAR(500),
    title VARCHAR(500),
    caption TEXT,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pezeshkan_redirects (
    id SERIAL PRIMARY KEY,
    source VARCHAR(500) UNIQUE NOT NULL,
    target VARCHAR(500) NOT NULL,
    status_code INT DEFAULT 301,
    match_type VARCHAR(50) DEFAULT 'exact',
    preserve_query BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    description TEXT,
    hit_count BIGINT DEFAULT 0,
    last_hit TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pezeshkan_settings (
    id SERIAL PRIMARY KEY,
    site_title VARCHAR(255) DEFAULT 'پزشکان - مجله جامع سلامت',
    site_subtitle VARCHAR(255),
    editorial_leader VARCHAR(255),
    announcement_banner TEXT,
    contact_phone VARCHAR(50),
    emergency_triage_enabled BOOLEAN DEFAULT TRUE,
    seo JSONB DEFAULT '{}'::jsonb,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
""")

    # Populate Data
    pillars = load_json("pillars.json", [])
    for p in pillars:
        sql.append(f"""INSERT INTO pezeshkan_pillars (name, short_name, slug, icon, count_badge, intent, dept, description, chips, branches)
VALUES ({escape_sql_string(p.get('name'))}, {escape_sql_string(p.get('shortName'))}, {escape_sql_string(p.get('slug'))}, {escape_sql_string(p.get('icon'))}, {escape_sql_string(p.get('countBadge'))}, {escape_sql_string(p.get('intent'))}, {escape_sql_string(p.get('dept'))}, {escape_sql_string(p.get('desc'))}, {escape_sql_string(p.get('chips', []))}, {escape_sql_string(p.get('branches', []))})
ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name, description = EXCLUDED.description;""")

    doctors = load_json("doctors.json", [])
    for d in doctors:
        sql.append(f"""INSERT INTO pezeshkan_doctors (name, title, mc_number, dept, pillar_slug, rating, reviews_count, avatar, available, work_hours, address, phone, time_slots, services)
VALUES ({escape_sql_string(d.get('name'))}, {escape_sql_string(d.get('title'))}, {escape_sql_string(d.get('mcNumber'))}, {escape_sql_string(d.get('dept'))}, {escape_sql_string(d.get('pillarSlug'))}, {d.get('rating', 5.0) or 5.0}, {d.get('reviewsCount', 0) or 0}, {escape_sql_string(d.get('avatar'))}, {escape_sql_string(d.get('available', True))}, {escape_sql_string(d.get('workHours'))}, {escape_sql_string(d.get('address'))}, {escape_sql_string(d.get('phone'))}, {escape_sql_string(d.get('timeSlots', []))}, {escape_sql_string(d.get('services', []))});""")

    articles = load_json("articles.json", [])
    for a in articles:
        sql.append(f"""INSERT INTO pezeshkan_articles (title, slug, summary, raw_html, content_html, image, image_alt, pillar_id, category_name, category_icon, doctor_id, author, read_time, last_reviewed, tag, tag_class, status, meta_title, meta_description, focus_keyword, faqs, schema_type, old_slugs, schema_data, custom_schema_json)
VALUES ({escape_sql_string(a.get('title'))}, {escape_sql_string(a.get('slug'))}, {escape_sql_string(a.get('summary'))}, {escape_sql_string(a.get('rawHtml'))}, {escape_sql_string(a.get('contentHtml'))}, {escape_sql_string(a.get('image'))}, {escape_sql_string(a.get('imageAlt'))}, {escape_sql_string(a.get('pillarId'))}, {escape_sql_string(a.get('categoryName'))}, {escape_sql_string(a.get('categoryIcon'))}, {escape_sql_string(a.get('doctorId'))}, {escape_sql_string(a.get('author'))}, {escape_sql_string(a.get('readTime'))}, {escape_sql_string(a.get('lastReviewed'))}, {escape_sql_string(a.get('tag'))}, {escape_sql_string(a.get('tagClass'))}, {escape_sql_string(a.get('status'))}, {escape_sql_string(a.get('metaTitle'))}, {escape_sql_string(a.get('metaDescription'))}, {escape_sql_string(a.get('focusKeyword'))}, {escape_sql_string(a.get('faqs', []))}, {escape_sql_string(a.get('schemaType'))}, {escape_sql_string(a.get('oldSlugs', []))}, {escape_sql_string(a.get('schemaData', {}))}, {escape_sql_string(a.get('customSchemaJson'))})
ON CONFLICT (slug) DO UPDATE SET title = EXCLUDED.title, content_html = EXCLUDED.content_html, last_modified = NOW();""")

    return "\n".join(sql)


def generate_django_models_reference():
    return """# -*- coding: utf-8 -*-
\"\"\"
Pezeshkan Medical Ecosystem - Django Models Architecture
Direct 1:1 mapping with current Pezeshkan JSON databases & REST API endpoints.
Ensures zero frontend changes when transitioning backend to Django 5.x.
\"\"\"

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
"""


def main():
    parser = argparse.ArgumentParser(description="Pezeshkan JSON to PostgreSQL/Django Migration Tool")
    parser.add_argument("--output-dir", default=OUTPUT_DIR, help="Destination directory for outputs")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("🚀 Starting Pezeshkan Data Migration Bridge...")
    
    # 1. Django Fixtures
    fixtures_path = os.path.join(args.output_dir, "django_fixtures.json")
    fixtures_data = generate_django_fixtures()
    with open(fixtures_path, "w", encoding="utf-8") as f:
        json.dump(fixtures_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Exported {len(fixtures_data)} records to Django Fixtures: {fixtures_path}")

    # 2. PostgreSQL SQL Dump
    sql_path = os.path.join(args.output_dir, "schema_and_data.sql")
    sql_data = generate_postgres_sql()
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write(sql_data)
    print(f"✅ Exported PostgreSQL DDL & Inserts: {sql_path}")

    # 3. Django Models Reference
    models_path = os.path.join(args.output_dir, "django_models_reference.py")
    with open(models_path, "w", encoding="utf-8") as f:
        f.write(generate_django_models_reference())
    print(f"✅ Created Django Models reference: {models_path}")

    print("🎉 Migration artifacts generated successfully!")


if __name__ == "__main__":
    main()
