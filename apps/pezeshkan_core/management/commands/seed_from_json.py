# -*- coding: utf-8 -*-
"""
Django Management Command: seed_from_json
Migrates and populates the database from existing mag/content/*.json databases.
"""

import os
import json
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.pezeshkan_core.models import (
    Pillar, Doctor, Article, Appointment, MediaItem,
    Redirect, SiteSetting, UserAccount, Newsletter,
    Subscriber, Inquiry, CrmTutorial
)

CONTENT_DIR = settings.BASE_DIR / 'mag' / 'content'


def read_json_file(filename, default=None):
    path = CONTENT_DIR / filename
    if not path.exists():
        return default if default is not None else []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return default if default is not None else []


class Command(BaseCommand):
    help = "Seed database from existing JSON files in mag/content/"

    def handle(self, *args, **options):
        self.stdout.write("[Pezeshkan] Starting automated database seeding from JSON...")

        # 1. Pillars
        pillars_data = read_json_file("pillars.json", [])
        p_count = 0
        for p in pillars_data:
            Pillar.objects.update_or_create(
                slug=p.get("slug"),
                defaults={
                    "name": p.get("name", ""),
                    "short_name": p.get("shortName", ""),
                    "icon": p.get("icon", ""),
                    "count_badge": p.get("countBadge", ""),
                    "intent": p.get("intent", ""),
                    "dept": p.get("dept", ""),
                    "desc": p.get("desc", ""),
                    "chips": p.get("chips", []),
                    "branches": p.get("branches", [])
                }
            )
            p_count += 1
        self.stdout.write(f"  [OK] Seeded {p_count} Pillars/Departments")

        # 2. Doctors
        doctors_data = read_json_file("doctors.json", [])
        d_count = 0
        for d in doctors_data:
            doc_id = str(d.get("id") or f"doc_{d_count+1}")
            Doctor.objects.update_or_create(
                custom_id=doc_id,
                defaults={
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
            )
            d_count += 1
        self.stdout.write(f"  [OK] Seeded {d_count} Doctors")

        # 3. Articles
        articles_data = read_json_file("articles.json", [])
        a_count = 0
        for a in articles_data:
            art_id = str(a.get("id") or f"art_{a_count+1}")
            art_slug = a.get("slug") or f"article-{art_id}"
            Article.objects.update_or_create(
                slug=art_slug,
                defaults={
                    "custom_id": art_id,
                    "title": a.get("title", ""),
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
                }
            )
            a_count += 1
        self.stdout.write(f"  [OK] Seeded {a_count} Articles")

        # 4. Appointments
        appointments_data = read_json_file("appointments.json", [])
        apt_count = 0
        for apt in appointments_data:
            code = apt.get("trackingCode") or f"PZ-{apt_count+100000}"
            Appointment.objects.update_or_create(
                tracking_code=code,
                defaults={
                    "custom_id": str(apt.get("id", f"apt-{apt_count+1}")),
                    "doctor_id": str(apt.get("doctorId", "")),
                    "doctor_name": apt.get("doctorName", "پزشک متخصص"),
                    "patient_name": apt.get("patientName", ""),
                    "patient_phone": apt.get("patientPhone", ""),
                    "national_id": apt.get("nationalId", ""),
                    "visit_type": apt.get("visitType", "ویزیت حضوری مطب"),
                    "date_label": apt.get("dateLabel", ""),
                    "time_slot": apt.get("timeSlot", ""),
                    "notes": apt.get("notes", ""),
                    "status": apt.get("status", "confirmed")
                }
            )
            apt_count += 1
        self.stdout.write(f"  [OK] Seeded {apt_count} Appointments")

        # 5. Media
        media_data = read_json_file("media.json", [])
        m_count = 0
        for m in media_data:
            m_id = str(m.get("id") or f"med_{m_count+1}")
            MediaItem.objects.update_or_create(
                custom_id=m_id,
                defaults={
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
                    "caption": m.get("caption", "")
                }
            )
            m_count += 1
        self.stdout.write(f"  [OK] Seeded {m_count} Media Items")

        # 6. Redirects
        redirects_data = read_json_file("redirects.json", [])
        r_count = 0
        for r in redirects_data:
            Redirect.objects.update_or_create(
                source=r.get("source", "").strip(),
                defaults={
                    "custom_id": str(r.get("id", f"red_{r_count+1}")),
                    "target": r.get("target", "").strip(),
                    "status_code": int(r.get("statusCode", 301) or 301),
                    "match_type": r.get("matchType", "exact"),
                    "preserve_query": bool(r.get("preserveQuery", True)),
                    "is_active": bool(r.get("isActive", True)),
                    "description": r.get("description", ""),
                    "hit_count": int(r.get("hitCount", 0) or 0)
                }
            )
            r_count += 1
        self.stdout.write(f"  [OK] Seeded {r_count} SEO Redirects")

        # 7. Settings
        settings_data = read_json_file("settings.json", {})
        if settings_data:
            SiteSetting.objects.update_or_create(
                id=1,
                defaults={
                    "site_title": settings_data.get("siteTitle", "پزشکان - مجله جامع سلامت"),
                    "site_subtitle": settings_data.get("siteSubtitle", ""),
                    "editorial_leader": settings_data.get("editorialLeader", ""),
                    "announcement_banner": settings_data.get("announcementBanner", ""),
                    "contact_phone": settings_data.get("contactPhone", ""),
                    "emergency_triage_enabled": bool(settings_data.get("emergencyTriageEnabled", True)),
                    "seo": settings_data.get("seo", {})
                }
            )
            self.stdout.write("  [OK] Seeded Site Settings")

        # 8. Users
        users_data = read_json_file("users.json", [])
        u_count = 0
        for u in users_data:
            UserAccount.objects.update_or_create(
                username=u.get("username"),
                defaults={
                    "custom_id": str(u.get("id", f"user_{u_count+1}")),
                    "display_name": u.get("displayName", ""),
                    "first_name": u.get("firstName", ""),
                    "last_name": u.get("lastName", ""),
                    "nickname": u.get("nickname", ""),
                    "email": u.get("email", ""),
                    "website": u.get("website", ""),
                    "role": u.get("role", "administrator"),
                    "bio": u.get("bio", ""),
                    "avatar": u.get("avatar", ""),
                    "specialty": u.get("specialty", ""),
                    "medical_council": u.get("medicalCouncil", ""),
                    "status": u.get("status", "active"),
                    "password_salt": u.get("passwordSalt", ""),
                    "password_hash": u.get("passwordHash", "")
                }
            )
            u_count += 1
        self.stdout.write(f"  [OK] Seeded {u_count} Clinical Users")

        # 9. Newsletters
        newsletters_data = read_json_file("newsletters.json", [])
        n_count = 0
        for n in newsletters_data:
            n_slug = n.get("slug") or f"newsletter-{n_count+1}"
            Newsletter.objects.update_or_create(
                slug=n_slug,
                defaults={
                    "custom_id": str(n.get("id", f"news_{n_count+1}")),
                    "title": n.get("title", ""),
                    "date": n.get("date", ""),
                    "read_time": n.get("readTime", "۴ دقیقه"),
                    "excerpt": n.get("excerpt", ""),
                    "content_html": n.get("contentHtml", ""),
                    "tags": n.get("tags", []),
                    "metrics": n.get("metrics", {}),
                    "status": n.get("status", "published")
                }
            )
            n_count += 1
        self.stdout.write(f"  [OK] Seeded {n_count} Newsletters")

        self.stdout.write(self.style.SUCCESS("[SUCCESS] Database successfully seeded with all Pezeshkan clinical data!"))
