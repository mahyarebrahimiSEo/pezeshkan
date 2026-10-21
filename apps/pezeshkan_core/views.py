# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - Enterprise Django API & View Controllers
Production-grade controllers with 100% backward compatibility for all frontends.
"""

import os
import io
import re
import json
import base64
import secrets
import mimetypes
from pathlib import Path
from datetime import datetime, timezone
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import models
from django.core.files.storage import default_storage

from apps.pezeshkan_core.models import (
    Pillar, Doctor, Article, Appointment, MediaItem,
    Redirect, SiteSetting, UserAccount, Newsletter,
    Subscriber, Inquiry, CrmTutorial, SubscriptionPlan, ClinicLead
)

try:
    from PIL import Image, ImageOps
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


# Helper: JSON body reader
def read_json(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode('utf-8'))
    except Exception:
        return {}


# Helper: Auth check
def is_admin(request):
    if request.user and request.user.is_authenticated and request.user.is_staff:
        return True
    return bool(request.session.get('is_admin'))


MIME_MAP = {
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".ttf": "font/ttf",
    ".xml": "application/xml; charset=utf-8",
    ".webmanifest": "application/manifest+json; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".ico": "image/x-icon",
    ".html": "text/html; charset=utf-8",
}

# Helper: Serve file safely with exact MIME types
def serve_static_file(file_path):
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        return HttpResponseNotFound("Page Not Found")
    
    ext = path.suffix.lower()
    content_type = MIME_MAP.get(ext)
    if not content_type:
        content_type, _ = mimetypes.guess_type(str(path))
        content_type = content_type or "application/octet-stream"
        if content_type.startswith("text/") or content_type in ("application/javascript", "application/json"):
            content_type += "; charset=utf-8"

    try:
        with open(path, "rb") as f:
            content = f.read()
        response = HttpResponse(content, content_type=content_type)
        if ext in (".css", ".js", ".svg", ".png", ".jpg", ".webp", ".woff2", ".woff", ".ttf"):
            response["Cache-Control"] = "public, max-age=86400"
        return response
    except Exception as e:
        return HttpResponse(f"Error loading file: {e}", status=500)


def serve_static_asset(request, path):
    """
    Universal static asset resolver. Searches portal, mag, assets, and fonts folders.
    Guarantees that files like /shared.css, /shared.js, /pezeshkon-logo.svg, etc., always resolve.
    """
    clean_path = path.lstrip("/")
    base_name = Path(clean_path).name

    candidates = [
        settings.BASE_DIR / 'portal' / clean_path,
        settings.BASE_DIR / 'mag' / clean_path,
        settings.BASE_DIR / 'assets' / clean_path,
        settings.BASE_DIR / 'fonts' / clean_path,
        settings.BASE_DIR / 'portal' / 'fonts' / base_name,
        settings.BASE_DIR / 'mag' / 'fonts' / base_name,
        settings.BASE_DIR / 'fonts' / base_name,
        settings.BASE_DIR / 'mag' / 'uploads' / clean_path,
        settings.BASE_DIR / clean_path,
    ]

    for c in candidates:
        if c.exists() and c.is_file():
            return serve_static_file(c)

    return HttpResponseNotFound(f"Static Asset Not Found: {clean_path}")


# ==============================================================================
# 1. HTML Page Views
# ==============================================================================

PORTAL_PAGE_NAMES = {
    "product": "product.html",
    "features": "features.html",
    "packages": "packages.html",
    "start": "start.html",
    "services": "services.html",
    "about": "about.html",
    "contact": "contact.html",
    "tutorials": "tutorials.html",
    "download": "download.html",
    "appointments": "appointments.html",
    "404": "404.html",
}

def index_page(request):
    """Serves the portal landing page or root index.html."""
    candidate = settings.BASE_DIR / 'portal' / 'index.html'
    if candidate.exists():
        return serve_static_file(candidate)
    return serve_static_file(settings.BASE_DIR / 'index.html')


def portal_page(request, page_name="index"):
    """Serves portal HTML pages (/product, /features, /packages, etc.)."""
    clean = page_name.strip("/").replace(".html", "")
    if not clean or clean == "index":
        target = settings.BASE_DIR / 'portal' / 'index.html'
    elif clean in PORTAL_PAGE_NAMES:
        target = settings.BASE_DIR / 'portal' / PORTAL_PAGE_NAMES[clean]
    else:
        target = settings.BASE_DIR / 'portal' / f"{clean}.html"
        if not target.exists():
            target = settings.BASE_DIR / 'portal' / '404.html'
    return serve_static_file(target)


def magazine_page(request, path=""):
    """Serves magazine SPA and subpages with full SSR for clinical articles."""
    import urllib.parse
    from django.shortcuts import redirect
    from server import render_article_ssr

    clean = urllib.parse.unquote(path.strip("/"))
    
    # 1. 301 Canonical Redirect for legacy query parameter ?article=:slug
    article_param = request.GET.get('article')
    if article_param:
        clean_param = urllib.parse.unquote(article_param.strip())
        return redirect(f"/mag/{urllib.parse.quote(clean_param)}", permanent=True)

    if not clean:
        target = settings.BASE_DIR / 'mag' / 'index.html'
        return serve_static_file(target)
    elif clean == "newsletter":
        target = settings.BASE_DIR / 'mag' / 'newsletter.html'
        return serve_static_file(target)
    else:
        # Check if direct file exists (assets, css, js, etc.)
        target = settings.BASE_DIR / 'mag' / clean
        if target.exists() and target.is_file():
            return serve_static_file(target)
        if not clean.endswith(".html"):
            target_html = settings.BASE_DIR / 'mag' / f"{clean}.html"
            if target_html.exists() and target_html.is_file():
                return serve_static_file(target_html)
        
        # Check if requested slug is an article
        try:
            articles_path = settings.BASE_DIR / 'mag' / 'content' / 'articles.json'
            if articles_path.exists():
                with open(articles_path, 'r', encoding='utf-8') as af:
                    articles_data = json.load(af)
            else:
                articles_data = []

            found_article = None
            for a in articles_data:
                curr_slug = a.get("slug") or a.get("id")
                old_slugs = a.get("oldSlugs", [])
                if clean in old_slugs and curr_slug and curr_slug != clean:
                    return redirect(f"/mag/{urllib.parse.quote(curr_slug)}", permanent=True)
                if a.get("slug") == clean or str(a.get("id")) == clean:
                    found_article = a
                    break

            if found_article:
                mag_template_path = settings.BASE_DIR / 'mag' / 'index.html'
                with open(mag_template_path, 'r', encoding='utf-8') as tf:
                    template_html = tf.read()
                ssr_html = render_article_ssr(found_article, template_html)
                return HttpResponse(ssr_html, content_type="text/html; charset=utf-8")
        except Exception as ssr_err:
            import logging
            logging.getLogger(__name__).error(f"[SSR] Django magazine article render error for {clean}: {ssr_err}")

        # If slug not found and not a static file, fallback to index.html
        target = settings.BASE_DIR / 'mag' / 'index.html'
        return serve_static_file(target)


def admin_page(request):
    """Serves the unified CMS and Clinical Management Dashboard."""
    target = settings.BASE_DIR / 'admin.html'
    return serve_static_file(target)


def login_page(request):
    """Serves the login page."""
    target = settings.BASE_DIR / 'mag' / 'login.html'
    return serve_static_file(target)


def appointments_page(request):
    """Serves the public patient appointment booking and tracking portal."""
    target = settings.BASE_DIR / 'portal' / 'appointments.html'
    return serve_static_file(target)


# ==============================================================================
# 2. Authentication APIs
# ==============================================================================

@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    data = read_json(request)
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    admin_user = getattr(settings, "ADMIN_USERNAME", "mahyarebrahimi")
    admin_pass = getattr(settings, "ADMIN_PASSWORD", "mahyebi86")

    if username == admin_user and password == admin_pass:
        request.session['is_admin'] = True
        request.session['username'] = username
        request.session['role'] = 'administrator'
        return JsonResponse({
            "success": True,
            "message": "ورود موفقیت‌آمیز بود",
            "user": {"username": username, "role": "administrator"}
        })

    # Check DB UserAccount
    user = UserAccount.objects.filter(username=username).first()
    if user and user.password_hash == password:  # or argon2 verification
        request.session['is_admin'] = (user.role == 'administrator')
        request.session['username'] = user.username
        request.session['role'] = user.role
        return JsonResponse({
            "success": True,
            "message": "ورود موفقیت‌آمیز بود",
            "user": user.to_dict()
        })

    return JsonResponse({"success": False, "error": "نام کاربری یا کلمه عبور اشتباه است"}, status=401)


@csrf_exempt
def api_logout(request):
    request.session.flush()
    return JsonResponse({"success": True, "message": "خروج با موفقیت انجام شد"})


def api_me(request):
    if is_admin(request) or request.session.get('username'):
        return JsonResponse({
            "authenticated": True,
            "user": {
                "username": request.session.get('username', 'mahyarebrahimi'),
                "role": request.session.get('role', 'administrator'),
                "displayName": "مهیار ابراهیمی"
            }
        })
    return JsonResponse({"authenticated": False}, status=401)


# ==============================================================================
# 3. Clinical Data APIs (Pillars, Doctors, Articles)
# ==============================================================================

def api_pillars(request):
    pillars = Pillar.objects.all().order_by('id')
    return JsonResponse([p.to_dict() for p in pillars], safe=False)


@csrf_exempt
def api_doctors(request):
    if request.method == "GET":
        doctors = Doctor.objects.all().order_by('id')
        return JsonResponse([d.to_dict() for d in doctors], safe=False)

    elif request.method == "POST":
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)
        data = read_json(request)
        doc_id = str(data.get("id") or f"doc_{int(datetime.now().timestamp())}")
        
        doctor, created = Doctor.objects.update_or_create(
            custom_id=doc_id,
            defaults={
                "name": data.get("name", "پزشک متخصص"),
                "title": data.get("title", ""),
                "mc_number": data.get("mcNumber", ""),
                "dept": data.get("dept", ""),
                "pillar_slug": data.get("pillarSlug", ""),
                "rating": float(data.get("rating", 5.0) or 5.0),
                "reviews_count": int(data.get("reviewsCount", 0) or 0),
                "avatar": data.get("avatar", ""),
                "available": bool(data.get("available", True)),
                "work_hours": data.get("workHours", ""),
                "address": data.get("address", ""),
                "phone": data.get("phone", ""),
                "time_slots": data.get("timeSlots", []),
                "services": data.get("services", []),
            }
        )
        # Synchronize doctors to mag/content/doctors.json
        try:
            docs_json_path = settings.BASE_DIR / 'mag' / 'content' / 'doctors.json'
            all_docs = [d.to_dict() for d in Doctor.objects.all().order_by('id')]
            with open(docs_json_path, 'w', encoding='utf-8') as f:
                json.dump(all_docs, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        return JsonResponse({
            "success": True,
            "doctor": doctor.to_dict(),
            "doctors": [d.to_dict() for d in Doctor.objects.all().order_by('id')]
        })

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def api_articles(request, slug=None):
    if request.method == "GET":
        query_slug = slug or request.GET.get("slug")
        if query_slug:
            article = Article.objects.filter(slug=query_slug).first()
            if not article:
                return JsonResponse({"error": "Article not found"}, status=404)
            return JsonResponse(article.to_dict())

        articles = Article.objects.all().order_by('-id')
        return JsonResponse([a.to_dict() for a in articles], safe=False)

    elif request.method in ("POST", "PUT"):
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)
        data = read_json(request)
        art_id = str(data.get("id") or f"art_{int(datetime.now().timestamp())}")
        art_slug = data.get("slug") or f"article-{art_id}"

        article, created = Article.objects.update_or_create(
            slug=art_slug,
            defaults={
                "custom_id": art_id,
                "title": data.get("title", ""),
                "summary": data.get("summary", ""),
                "raw_html": data.get("rawHtml", ""),
                "content_html": data.get("contentHtml", ""),
                "image": data.get("image", ""),
                "image_alt": data.get("imageAlt", ""),
                "pillar_id": data.get("pillarId", ""),
                "category_name": data.get("categoryName", ""),
                "category_icon": data.get("categoryIcon", ""),
                "doctor_id": str(data.get("doctorId", "")),
                "author": data.get("author", "تیم تحریریه پزشکان"),
                "read_time": data.get("readTime", "۵ دقیقه"),
                "last_reviewed": data.get("lastReviewed", ""),
                "tag": data.get("tag", ""),
                "tag_class": data.get("tagClass", ""),
                "status": data.get("status", "published"),
                "meta_title": data.get("metaTitle", ""),
                "meta_description": data.get("metaDescription", ""),
                "focus_keyword": data.get("focusKeyword", ""),
                "faqs": data.get("faqs", []),
                "schema_type": data.get("schemaType", "MedicalWebPage"),
                "old_slugs": data.get("oldSlugs", []),
                "schema_data": data.get("schemaData", {}),
                "custom_schema_json": data.get("customSchemaJson", ""),
            }
        )
        all_articles = [a.to_dict() for a in Article.objects.all().order_by('-id')]
        return JsonResponse({"success": True, "article": article.to_dict(), "articles": all_articles})

    elif request.method == "DELETE":
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)
        art_id = request.GET.get("id") or slug
        Article.objects.filter(models.Q(custom_id=art_id) | models.Q(slug=art_id)).delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Method not allowed"}, status=405)


# ==============================================================================
# 4. Appointments & Booking APIs
# ==============================================================================

@csrf_exempt
def api_appointments(request):
    if request.method == "POST":
        data = read_json(request)
        doctor_id = str(data.get("doctorId", "")).strip()
        patient_name = data.get("patientName", "").strip()
        patient_phone = data.get("patientPhone", "").strip()
        date_label = data.get("dateLabel", "").strip()
        time_slot = data.get("timeSlot", "").strip()
        visit_type = data.get("visitType", "ویزیت حضوری مطب")
        notes = data.get("notes", "").strip()
        doctor_name = data.get("doctorName", "").strip()

        if not patient_name or not patient_phone or not date_label or not time_slot:
            return JsonResponse({"error": "تمامی فیلدهای الزامی نوبت‌دهی را تکمیل فرمایید"}, status=400)

        if not doctor_name and doctor_id:
            doc = Doctor.objects.filter(custom_id=doctor_id).first()
            if doc:
                doctor_name = doc.name

        # Concurrency / Double-booking prevention
        has_conflict = Appointment.objects.filter(
            doctor_id=doctor_id,
            date_label=date_label,
            time_slot=time_slot
        ).exclude(status__in=["cancelled", "لغو شده"]).exists()

        if has_conflict:
            return JsonResponse({
                "error": "این زمان نوبت قبلاً برای این پزشک رزرو شده است. لطفاً ساعت دیگری را انتخاب فرمایید."
            }, status=409)

        tracking_code = f"PZ-{secrets.randbelow(900000) + 100000}"
        apt = Appointment.objects.create(
            custom_id=f"apt-{int(datetime.now().timestamp() * 1000)}",
            tracking_code=tracking_code,
            doctor_id=doctor_id,
            doctor_name=doctor_name or "پزشک متخصص",
            patient_name=patient_name,
            patient_phone=patient_phone,
            national_id=data.get("nationalId", ""),
            visit_type=visit_type,
            date_label=date_label,
            time_slot=time_slot,
            notes=notes,
            status="confirmed"
        )
        return JsonResponse({
            "success": True,
            "ok": True,
            "trackingCode": tracking_code,
            "appointment": apt.to_dict()
        })

    elif request.method == "GET":
        tracking_code = request.GET.get("code", "").strip()
        phone = request.GET.get("phone", "").strip()

        if tracking_code or phone:
            q = models.Q()
            if tracking_code:
                q |= models.Q(tracking_code=tracking_code)
            if phone:
                q |= models.Q(patient_phone=phone)
            filtered = [a.to_dict() for a in Appointment.objects.filter(q).order_by('-id')]
            single_app = filtered[0] if filtered else None
            return JsonResponse({
                "success": True,
                "trackingCode": tracking_code,
                "appointment": single_app,
                "appointments": filtered
            })

        if is_admin(request):
            appointments = [a.to_dict() for a in Appointment.objects.all().order_by('-id')]
            return JsonResponse(appointments, safe=False)

        return JsonResponse({"error": "جهت استعلام نوبت، ارسال کد رهگیری یا شماره تماس الزامی است"}, status=400)

    elif request.method == "PUT":
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)
        data = read_json(request)
        apt_id = data.get("id") or data.get("trackingCode")
        apt = Appointment.objects.filter(models.Q(custom_id=apt_id) | models.Q(tracking_code=apt_id)).first()
        if not apt:
            return JsonResponse({"error": "Appointment not found"}, status=404)
        if "status" in data:
            apt.status = data["status"]
        if "notes" in data:
            apt.notes = data["notes"]
        apt.save()
        return JsonResponse({"success": True, "appointment": apt.to_dict()})

    elif request.method == "DELETE":
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)
        apt_id = request.GET.get("id") or request.GET.get("code")
        Appointment.objects.filter(models.Q(custom_id=apt_id) | models.Q(tracking_code=apt_id)).delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Method not allowed"}, status=405)


def api_admin_appointments(request):
    if not is_admin(request):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    appointments = [a.to_dict() for a in Appointment.objects.all().order_by('-id')]
    return JsonResponse(appointments, safe=False)


# ==============================================================================
# 5. Settings & Deep Merge API
# ==============================================================================

@csrf_exempt
def api_settings(request):
    setting, _ = SiteSetting.objects.get_or_create(id=1)
    if request.method == "GET":
        return JsonResponse(setting.to_dict())

    elif request.method == "PUT":
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)
        data = read_json(request)

        # Deep merge incoming keys so partial updates (e.g. SEO) do not wipe existing settings
        if "siteTitle" in data:
            setting.site_title = data["siteTitle"]
        if "siteSubtitle" in data:
            setting.site_subtitle = data["siteSubtitle"]
        if "editorialLeader" in data:
            setting.editorial_leader = data["editorialLeader"]
        if "announcementBanner" in data:
            setting.announcement_banner = data["announcementBanner"]
        if "contactPhone" in data:
            setting.contact_phone = data["contactPhone"]
        if "emergencyTriageEnabled" in data:
            setting.emergency_triage_enabled = bool(data["emergencyTriageEnabled"])

        if "seo" in data and isinstance(data["seo"], dict):
            current_seo = setting.seo or {}
            current_seo.update(data["seo"])
            setting.seo = current_seo

        setting.save()
        return JsonResponse({"success": True, "settings": setting.to_dict()})

    return JsonResponse({"error": "Method not allowed"}, status=405)


# ==============================================================================
# 6. Media Library & File Upload APIs
# ==============================================================================

@csrf_exempt
def api_upload(request):
    """
    Universal media upload endpoint for Pezeshkan Medical Ecosystem.
    Accepts multipart/form-data (file, image) and JSON base64 payloads.
    Optimizes images using Pillow (WebP/JPEG) and registers MediaItem.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    raw_bytes = None
    filename = None
    alt_text = ""
    caption = ""

    # 1. Check multipart/form-data
    if request.FILES:
        uploaded = request.FILES.get("file") or request.FILES.get("image")
        if uploaded:
            filename = uploaded.name
            raw_bytes = uploaded.read()
            alt_text = request.POST.get("alt", "").strip() or filename
            caption = request.POST.get("caption", "").strip()

    # 2. Check JSON payload with base64 data
    if not raw_bytes:
        data = read_json(request)
        if data and data.get("data"):
            filename = data.get("filename") or f"upload_{int(datetime.now().timestamp())}.webp"
            alt_text = data.get("alt", "").strip() or filename
            caption = data.get("caption", "").strip()
            b64_str = data.get("data")
            if "," in b64_str:
                b64_str = b64_str.split(",", 1)[1]
            try:
                raw_bytes = base64.b64decode(b64_str)
            except Exception as e:
                return JsonResponse({"error": f"Invalid base64 data: {e}"}, status=400)

    if not raw_bytes or not filename:
        return JsonResponse({"error": "هیچ فایلی ارسال نشده است"}, status=400)

    now = datetime.now()
    year_str = str(now.year)
    month_str = f"{now.month:02d}"

    # Route doctor photos to mag/uploads/doctors
    is_doctor_photo = any(k in filename.lower() for k in ['doctor', 'dr-', 'dr_', 'pezeshk', 'avatar'])
    if is_doctor_photo:
        target_dir = settings.BASE_DIR / 'mag' / 'uploads' / 'doctors'
        base_url_prefix = "/mag/uploads/doctors"
    else:
        target_dir = settings.BASE_DIR / 'mag' / 'uploads' / year_str / month_str
        base_url_prefix = f"/mag/uploads/{year_str}/{month_str}"

    os.makedirs(target_dir, exist_ok=True)

    clean_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)
    stem = Path(clean_name).stem
    ext = Path(clean_name).suffix.lower()
    if not ext:
        ext = ".webp"

    save_filename = f"{stem}_{int(now.timestamp())}{ext}"
    save_path = target_dir / save_filename

    # Optimize with Pillow if it's an image
    file_size = len(raw_bytes)
    fmt = ext.lstrip('.')
    if HAS_PILLOW:
        try:
            img = Image.open(io.BytesIO(raw_bytes))
            if ext == '.webp':
                out_io = io.BytesIO()
                img.save(out_io, 'WEBP', quality=88, method=6)
                raw_bytes = out_io.getvalue()
                file_size = len(raw_bytes)
            elif ext in ('.jpg', '.jpeg'):
                img = img.convert('RGB')
                out_io = io.BytesIO()
                img.save(out_io, 'JPEG', quality=88, optimize=True)
                raw_bytes = out_io.getvalue()
                file_size = len(raw_bytes)
        except Exception:
            pass

    with open(save_path, "wb") as f:
        f.write(raw_bytes)

    file_url = f"{base_url_prefix}/{save_filename}"

    # Save MediaItem in DB
    media_item = MediaItem.objects.create(
        custom_id=f"med_{int(now.timestamp())}",
        filename=save_filename,
        url=file_url,
        alt=alt_text,
        caption=caption,
        format=fmt,
        size=file_size,
        original_size=file_size,
        storage="local"
    )

    # Sync to mag/content/media.json
    try:
        media_json_path = settings.BASE_DIR / 'mag' / 'content' / 'media.json'
        if media_json_path.exists():
            with open(media_json_path, 'r', encoding='utf-8') as f:
                media_list = json.load(f)
        else:
            media_list = []
        media_list.insert(0, media_item.to_dict())
        with open(media_json_path, 'w', encoding='utf-8') as f:
            json.dump(media_list, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    return JsonResponse({
        "success": True,
        "url": file_url,
        "media": media_item.to_dict()
    })


@csrf_exempt
def api_media(request):
    if request.method == "GET":
        items = [m.to_dict() for m in MediaItem.objects.all().order_by('-id')]
        return JsonResponse(items, safe=False)

    elif request.method == "POST":
        return api_upload(request)

    return JsonResponse({"error": "Method not allowed"}, status=405)


# ==============================================================================
# 7. SEO Redirects APIs
# ==============================================================================

@csrf_exempt
def api_redirects(request):
    if request.method == "GET":
        rules = [r.to_dict() for r in Redirect.objects.all().order_by('-id')]
        return JsonResponse(rules, safe=False)

    elif request.method in ("POST", "PUT"):
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)
        data = read_json(request)
        rule_id = data.get("id") or f"red_{int(datetime.now().timestamp())}"

        rule, _ = Redirect.objects.update_or_create(
            source=data.get("source", "").strip(),
            defaults={
                "custom_id": str(rule_id),
                "target": data.get("target", "").strip(),
                "status_code": int(data.get("statusCode", 301) or 301),
                "match_type": data.get("matchType", "exact"),
                "preserve_query": bool(data.get("preserveQuery", True)),
                "is_active": bool(data.get("isActive", True)),
                "description": data.get("description", ""),
            }
        )
        all_rules = [r.to_dict() for r in Redirect.objects.all().order_by('-id')]
        return JsonResponse({"success": True, "rule": rule.to_dict(), "rules": all_rules})

    elif request.method == "DELETE":
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)
        rule_id = request.GET.get("id")
        Redirect.objects.filter(models.Q(custom_id=rule_id) | models.Q(id=rule_id if str(rule_id).isdigit() else 0)).delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Method not allowed"}, status=405)


# ==============================================================================
# 8. Auxiliary APIs (Newsletters, Subscribers, Schemas, CRM)
# ==============================================================================

def api_newsletters(request):
    news = [n.to_dict() for n in Newsletter.objects.all().order_by('-id')]
    return JsonResponse(news, safe=False)


@csrf_exempt
def api_subscribers(request):
    if request.method == "POST":
        data = read_json(request)
        email = data.get("email", "").strip()
        if not email or "@" not in email:
            return JsonResponse({"error": "ایمیل نامعتبر است"}, status=400)
        sub, _ = Subscriber.objects.get_or_create(
            email=email,
            defaults={"name": data.get("name", ""), "category": data.get("category", "عمومی")}
        )
        return JsonResponse({"success": True, "message": "عضویت با موفقیت ثبت شد"})
    return JsonResponse({"error": "Method not allowed"}, status=405)


def api_schemas(request):
    schema_file = settings.BASE_DIR / 'mag' / 'content' / 'schemas.json'
    if schema_file.exists():
        with open(schema_file, 'r', encoding='utf-8') as f:
            return JsonResponse(json.load(f), safe=False)
    return JsonResponse([], safe=False)


@csrf_exempt
def api_schema_validate(request):
    data = read_json(request)
    json_ld = data.get("jsonLd") or data.get("schema")
    if not json_ld:
        return JsonResponse({"valid": False, "errors": ["محتوای اسکیما ارسال نشده است"]}, status=400)
    try:
        if isinstance(json_ld, str):
            json.loads(json_ld)
        return JsonResponse({"valid": True, "message": "ساختار JSON-LD کاملاً معتبر است"})
    except Exception as e:
        return JsonResponse({"valid": False, "errors": [f"خطای سینتکس JSON: {e}"]}, status=400)


def api_crm_tutorials(request):
    tuts = [t.to_dict() for t in CrmTutorial.objects.all()]
    return JsonResponse(tuts, safe=False)


# ==============================================================================
# 9. Blueprint 2.2.0 Integration Flows (Directory, Plans, Leads)
# ==============================================================================

def api_clinic_directory(request):
    """
    FLOW_01_PATIENT_QUICK_BOOKING: Public directory endpoint returning doctors
    with clinic slugs and external Quick Booking bridge URLs.
    """
    doctors = Doctor.objects.all().order_by('id')
    results = []
    for doc in doctors:
        slug = doc.clinic_slug or doc.custom_id or f"doc-{doc.id}"
        results.append({
            "slug": slug,
            "name": f"کلینیک {doc.name}",
            "doctor_name": doc.name,
            "specialty": doc.pillar_slug or "general",
            "title": doc.title,
            "mc_number": doc.mc_number,
            "dept": doc.dept,
            "phone": doc.phone,
            "address": doc.address,
            "center_type": doc.center_type or "solo",
            "rating": float(doc.rating) if doc.rating else 5.0,
            "reviews_count": doc.reviews_count,
            "quick_booking_url": doc.quick_booking_url,
        })
    return JsonResponse({
        "count": len(results),
        "results": results
    })


def api_platform_plans(request):
    """
    FLOW_02_PACKAGES_AND_PLANS: Public plans endpoint returning active subscription packages.
    """
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('order', 'id')
    return JsonResponse([p.to_dict() for p in plans], safe=False)


@csrf_exempt
def api_leads_start(request):
    """
    FLOW_03_CLINIC_ONBOARDING_LEADS: Captures clinic onboarding leads from /start wizard,
    stores them in marketing DB, and returns redirect_url to live interactive demo.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = read_json(request)
    doctor_name = (data.get("doctorName") or data.get("doctor_name") or data.get("name") or "").strip()
    mobile = (data.get("mobile") or data.get("phone") or "").strip()

    if not doctor_name or not mobile:
        return JsonResponse({
            "success": False,
            "error": "نام پزشک و شماره همراه الزامی است"
        }, status=400)

    # Extract client IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    specialty = data.get("specialty") or ""
    patients_volume = data.get("patientsVolume") or data.get("patients_volume") or ""
    challenges = data.get("challenges") or []
    if isinstance(challenges, str):
        challenges = [challenges]
    clinic_address = data.get("clinicAddress") or data.get("clinic_address") or data.get("address") or ""
    chosen_plan = data.get("chosenPlan") or data.get("chosen_plan") or data.get("plan") or ""

    lead = ClinicLead.objects.create(
        doctor_name=doctor_name,
        mobile=mobile,
        specialty=specialty,
        patients_volume=patients_volume,
        challenges=challenges,
        clinic_address=clinic_address,
        chosen_plan=chosen_plan,
        status="new",
        ip=ip
    )

    return JsonResponse({
        "success": True,
        "message": "درخواست دمو و شروع همکاری با موفقیت ثبت شد",
        "lead": lead.to_dict(),
        "redirect_url": "https://app.pezeshk-on.ir/demo/doctor"
    }, status=201)


def api_admin_leads(request):
    """
    Admin endpoint to view captured clinic onboarding leads.
    """
    if not is_admin(request):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    leads = [lead.to_dict() for lead in ClinicLead.objects.all().order_by('-created_at')]
    return JsonResponse(leads, safe=False)

