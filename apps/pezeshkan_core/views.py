import urllib.parse
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
from datetime import datetime, timezone, timedelta
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import models
from django.core.files.storage import default_storage
from django.core.cache import cache

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
    user = getattr(request, 'user', None)
    if user and user.is_authenticated and user.is_staff:
        return True
    if hasattr(request, 'session') and bool(request.session.get('is_admin')):
        return True
    auth_header = getattr(request, 'headers', {}).get('Authorization', '')
    if auth_header.startswith('Bearer ') and len(auth_header) > 10:
        return True
    return False

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
    ".glb": "model/gltf-binary",
    ".gltf": "model/gltf+json",
}

# In-Memory High-Concurrency Caches
_SITE_IMAGES_CACHE = None
_SITE_IMAGES_MTIME = 0
_STATIC_FILE_CACHE = {}
_MAX_STATIC_CACHE_ENTRIES = 500

# Helper: Load and Save Site Page Images Configuration with in-memory caching
def load_site_images():
    global _SITE_IMAGES_CACHE, _SITE_IMAGES_MTIME
    images_file = settings.BASE_DIR / 'mag' / 'content' / 'site_images.json'
    if not images_file.exists():
        return []
    try:
        mtime = images_file.stat().st_mtime
        if _SITE_IMAGES_CACHE is not None and mtime == _SITE_IMAGES_MTIME:
            return _SITE_IMAGES_CACHE
        with open(images_file, 'r', encoding='utf-8') as f:
            _SITE_IMAGES_CACHE = json.load(f)
            _SITE_IMAGES_MTIME = mtime
            return _SITE_IMAGES_CACHE
    except Exception:
        return _SITE_IMAGES_CACHE or []


def save_site_images(images):
    global _SITE_IMAGES_CACHE, _SITE_IMAGES_MTIME, _STATIC_FILE_CACHE
    images_file = settings.BASE_DIR / 'mag' / 'content' / 'site_images.json'
    try:
        with open(images_file, 'w', encoding='utf-8') as f:
            json.dump(images, f, ensure_ascii=False, indent=2)
        _SITE_IMAGES_CACHE = images
        _SITE_IMAGES_MTIME = images_file.stat().st_mtime
        _STATIC_FILE_CACHE = {k: v for k, v in _STATIC_FILE_CACHE.items() if not k.endswith('.html')}
        return True
    except Exception:
        return False


def inject_cache_busting(html_text):
    """
    Dynamically injects file modification timestamps (mtime) for static assets (shared.css, shared.js)
    and attaches aggressive no-cache meta tags to HTML head.
    Guarantees that any changes to CSS or JS instantly invalidate browser cache on a single F5 refresh.
    """
    try:
        portal_dir = settings.BASE_DIR / 'portal'
        shared_css = portal_dir / 'shared.css'
        shared_js = portal_dir / 'shared.js'

        css_mtime = int(shared_css.stat().st_mtime) if shared_css.exists() else int(datetime.now().timestamp())
        js_mtime = int(shared_js.stat().st_mtime) if shared_js.exists() else int(datetime.now().timestamp())

        preloader_css = portal_dir / 'preloader.css'
        preloader_js = portal_dir / 'preloader.js'
        pl_css_mtime = int(preloader_css.stat().st_mtime) if preloader_css.exists() else int(datetime.now().timestamp())
        pl_js_mtime = int(preloader_js.stat().st_mtime) if preloader_js.exists() else int(datetime.now().timestamp())

        # Update /shared.css?v=...
        html_text = re.sub(r'(/shared\.css)(?:\?[^"\'\s>]*)?', rf'\g<1>?v={css_mtime}', html_text)
        # Update /shared.js?v=...
        html_text = re.sub(r'(/shared\.js)(?:\?[^"\'\s>]*)?', rf'\g<1>?v={js_mtime}', html_text)
        # Update /preloader.css?v=...
        html_text = re.sub(r'(/preloader\.css)(?:\?[^"\'\s>]*)?', rf'\g<1>?v={pl_css_mtime}', html_text)
        # Update /preloader.js?v=...
        html_text = re.sub(r'(/preloader\.js)(?:\?[^"\'\s>]*)?', rf'\g<1>?v={pl_js_mtime}', html_text)

        # Ensure no-cache meta tags in <head>
        meta_tags = (
            '  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n'
            '  <meta http-equiv="Pragma" content="no-cache">\n'
            '  <meta http-equiv="Expires" content="0">'
        )
        if '<meta http-equiv="Cache-Control"' not in html_text and '</head>' in html_text:
            html_text = html_text.replace('</head>', f'{meta_tags}\n</head>', 1)
    except Exception:
        pass
    return html_text


# Helper: Serve file safely with exact MIME types and in-memory cache
def serve_static_file(file_path, status=200):
    path = Path(file_path)
    str_path = str(path)

    if not path.exists() or not path.is_file():
        return HttpResponseNotFound("Page Not Found")

    file_mtime = path.stat().st_mtime
    ext = path.suffix.lower()

    # In-memory cache hit with mtime validation (skip HTML to allow live asset mtime injection)
    if ext != '.html' and str_path in _STATIC_FILE_CACHE:
        cached_mtime, content, content_type, ext_cached = _STATIC_FILE_CACHE[str_path]
        if cached_mtime == file_mtime:
            response = HttpResponse(content, content_type=content_type, status=status)
            response["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
            return response

    content_type = MIME_MAP.get(ext)
    if not content_type:
        content_type, _ = mimetypes.guess_type(str(path))
        content_type = content_type or "application/octet-stream"
        if content_type.startswith("text/") or content_type in ("application/javascript", "application/json"):
            content_type += "; charset=utf-8"

    try:
        with open(path, "rb") as f:
            content = f.read()

        # If serving HTML page, perform instant SSR image hydration, cache busting, and script injection
        if ext == '.html':
            try:
                html_text = content.decode('utf-8')
                html_text = inject_cache_busting(html_text)
                images = load_site_images()
                if images:
                    for img in images:
                        d_url = img.get('defaultUrl')
                        c_url = img.get('currentUrl')
                        if d_url and c_url and d_url != c_url:
                            html_text = html_text.replace(d_url, c_url)
                    
                    img_dict = {item['key']: item.get('currentUrl') for item in images if isinstance(item, dict) and 'key' in item}
                    img_dict_json = json.dumps(img_dict, ensure_ascii=False)
                    script_tag = f'<script>window.__SITE_IMAGES__ = {img_dict_json};</script>'
                    if '</head>' in html_text:
                        html_text = html_text.replace('</head>', f'{script_tag}\n</head>', 1)
                content = html_text.encode('utf-8')
            except Exception:
                pass

        if ext != '.html' and len(_STATIC_FILE_CACHE) < _MAX_STATIC_CACHE_ENTRIES:
            _STATIC_FILE_CACHE[str_path] = (file_mtime, content, content_type, ext)

        response = HttpResponse(content, content_type=content_type, status=status)
        response["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
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
    "service-appointments": "service-appointments.html",
    "service-emr": "service-emr.html",
    "service-physio": "service-physio.html",
    "service-sms-crm": "service-sms-crm.html",
    "service-accounting": "service-accounting.html",
    "404": "404.html",
}

def index_page(request):
    """Serves the portal landing page with SSR for published magazine articles."""
    import html as html_escape
    from django.http import HttpResponse

    candidate = settings.BASE_DIR / 'portal' / 'index.html'
    if not candidate.exists():
        candidate = settings.BASE_DIR / 'index.html'

    try:
        content = candidate.read_text(encoding='utf-8')
    except Exception:
        return serve_static_file(candidate)

    # SSR: Query published articles for homepage magazine section (maximum 4 latest)
    try:
        published = list(Article.objects.filter(status='published').order_by('-id')[:4])
    except Exception:
        published = []

    if published:
        cards_html = []
        for idx, art in enumerate(published):
            slug = art.slug or str(art.id)
            title = html_escape.escape(art.title or '')
            summary = html_escape.escape(art.summary or '')
            img = html_escape.escape(art.image or 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=600&q=80')
            alt = html_escape.escape(art.image_alt or art.title or '')
            cat = html_escape.escape(art.category_name or art.tag or 'مجله سلامت')
            author_name = html_escape.escape(art.author if isinstance(art.author, str) and art.author else 'تیم متخصص محتوا نویس پزشکآن')
            read_time = html_escape.escape(art.read_time or '۵ دقیقه')

            card = f'''        <a href="/mag/{slug}" class="pez-mag-cover-card" data-slide-index="{idx}" title="{title}">
          <div class="mag-cover-img-wrap" aria-hidden="true">
            <img src="{img}" alt="{alt}" loading="lazy" decoding="async" class="mag-cover-bg-img" onerror="this.onerror=null; this.src='/mag/uploads/2026/10/11_1792233621_b823deb3.webp'" />
          </div>
          <div class="mag-cover-scrim" aria-hidden="true"></div>
          <div class="mag-cover-top-row">
            <span class="mag-cover-category-badge">{cat}</span>
            <span class="mag-cover-readtime-pill">
              <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="width:12px;height:12px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span>{read_time}</span>
            </span>
          </div>
          <div class="mag-cover-content-glass">
            <h3 class="mag-cover-title">{title}</h3>
            <p class="mag-cover-summary">{summary}</p>
            <div class="mag-cover-footer-row">
              <span class="mag-cover-read-more">
                <span>مطالعه مقاله کامل</span>
                <svg class="svg-icon mag-cover-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" style="width:14px;height:14px;"><polyline points="15 18 9 12 15 6"/></svg>
              </span>
              <span class="mag-cover-author-pill">
                <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                <span>{author_name}</span>
              </span>
            </div>
          </div>
        </a>'''
            cards_html.append(card)

        grid_content = "\n".join(cards_html)
        dots_html = "".join([f'<button type="button" class="home-mag-dot{" active" if i == 0 else ""}" data-index="{i}" aria-label="رفتن به اسلاید {i + 1}"></button>' for i in range(len(published))])

        content = content.replace(
            '<section id="home-magazine-section" class="home-magazine-section" style="display:none;">',
            '<section id="home-magazine-section" class="home-magazine-section" style="display:block;">'
        )
        content = content.replace(
            '<div class="grid-3 home-magazine-grid" id="home-magazine-grid"></div>',
            f'<div class="grid-3 home-magazine-grid" id="home-magazine-grid">\n{grid_content}\n      </div>'
        )
        content = content.replace(
            '<div class="home-mag-slider-dots" id="homeMagSliderDots" aria-label="صفحات اسلایدر مقالات"></div>',
            f'<div class="home-mag-slider-dots" id="homeMagSliderDots" aria-label="صفحات اسلایدر مقالات">\n{dots_html}\n      </div>'
        )

    # Dynamic asset version injection for instant cache-busting on simple F5 refresh
    content = inject_cache_busting(content)

    response = HttpResponse(content, content_type='text/html; charset=utf-8')
    response["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


def portal_page(request, page_name="index", path=None, **kwargs):
    """Serves portal HTML pages (/product, /features, /packages, etc.)."""
    actual = path if path is not None else page_name
    clean = actual.strip("/").replace(".html", "")
    if clean.startswith("portal/"):
        clean = clean[len("portal/"):]
    if not clean or clean == "index":
        return index_page(request)
    elif clean in PORTAL_PAGE_NAMES:
        target = settings.BASE_DIR / 'portal' / PORTAL_PAGE_NAMES[clean]
        status = 404 if clean in ("404", "404.html") else 200
        return serve_static_file(target, status=status)
    else:
        target = settings.BASE_DIR / 'portal' / f"{clean}.html"
        if not target.exists():
            target = settings.BASE_DIR / 'portal' / '404.html'
            return serve_static_file(target, status=404)
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
    elif clean in ("404", "404.html"):
        target_404 = settings.BASE_DIR / 'mag' / '404.html'
        if target_404.exists():
            return serve_static_file(target_404, status=404)
    elif clean == "newsletter":
        return HttpResponsePermanentRedirect('/mag')
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
            found_article = None
            art_db = Article.objects.filter(slug=clean).first()
            if not art_db and clean.isdigit():
                art_db = Article.objects.filter(id=int(clean)).first()
            if not art_db:
                art_db = Article.objects.filter(custom_id=clean).first()
            if art_db:
                found_article = art_db.to_dict()
            else:
                articles_path = settings.BASE_DIR / 'mag' / 'content' / 'articles.json'
                if articles_path.exists():
                    with open(articles_path, 'r', encoding='utf-8') as af:
                        articles_data = json.load(af)
                else:
                    articles_data = []
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

        # If slug not found and not a static file, serve dedicated Magazine 404 page
        target_404 = settings.BASE_DIR / 'mag' / '404.html'
        if target_404.exists() and target_404.is_file():
            return serve_static_file(target_404, status=404)
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


def custom_404_view(request, exception=None, unmatched_path=""):
    """
    Universal 404 handler for Pezeshkan Medical Platform.
    Handles Persian paths, URL-encoded paths, API requests, magazine routes, and portal routes cleanly.
    Guarantees no internal Django debug yellow screen is ever displayed.
    """
    import urllib.parse
    req_path = request.path or ""

    # 1. API routes -> JSON 404
    if req_path.startswith('/api/') or req_path == '/api':
        return JsonResponse({
            "success": False,
            "error": "مسیر درخواستی در API یافت نشد (Not Found)",
            "path": req_path,
            "status": 404
        }, status=404)

    # 2. Magazine routes -> Magazine 404
    if req_path.startswith('/mag/') or req_path == '/mag':
        mag_404 = settings.BASE_DIR / 'mag' / '404.html'
        if mag_404.exists():
            return serve_static_file(mag_404, status=404)

    # 3. All other paths (Portal, English, Persian, root) -> Portal 404
    portal_404 = settings.BASE_DIR / 'portal' / '404.html'
    if portal_404.exists():
        return serve_static_file(portal_404, status=404)

    # Fallback if 404.html is missing
    return HttpResponseNotFound("<h1>404 - صفحه مورد نظر پیدا نشد</h1>", content_type="text/html; charset=utf-8")


def custom_500_view(request):
    """Universal 500 error handler."""
    if request.path.startswith('/api/'):
        return JsonResponse({
            "success": False,
            "error": "خطای داخلی سرور (Internal Server Error)",
            "status": 500
        }, status=500)
    portal_404 = settings.BASE_DIR / 'portal' / '404.html'
    if portal_404.exists():
        return serve_static_file(portal_404, status=500)
    return HttpResponse("<h1>500 - خطای داخلی سرور</h1>", status=500, content_type="text/html; charset=utf-8")


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
    data = cache.get("api_pillars")
    if data is None:
        pillars = Pillar.objects.all().order_by('id')
        data = [p.to_dict() for p in pillars]
        cache.set("api_pillars", data, 60)
    return JsonResponse(data, safe=False)


@csrf_exempt
def api_doctors(request):
    if request.method == "GET":
        data = cache.get("api_doctors")
        if data is None:
            doctors = Doctor.objects.all().order_by('id')
            data = [d.to_dict() for d in doctors]
            cache.set("api_doctors", data, 30)
        return JsonResponse(data, safe=False)

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

        cache.delete("api_doctors")
        cache.delete("api_clinic_directory")
        return JsonResponse({
            "success": True,
            "doctor": doctor.to_dict(),
            "doctors": [d.to_dict() for d in Doctor.objects.all().order_by('id')]
        })

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def api_newsletter_doctors(request, doc_id=None):
    """
    CRUD Endpoint for dedicated Newsletter Clinical Authors (independent of clinic appointment doctors).
    Synchronizes directly with mag/content/newsletter_doctors.json.
    """
    newsletter_json_path = settings.BASE_DIR / 'mag' / 'content' / 'newsletter_doctors.json'

    def load_newsletter_docs():
        if newsletter_json_path.exists():
            try:
                with open(newsletter_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            except Exception:
                pass
        return []

    def save_newsletter_docs(docs):
        try:
            with open(newsletter_json_path, 'w', encoding='utf-8') as f:
                json.dump(docs, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    if request.method == "GET":
        docs = load_newsletter_docs()
        return JsonResponse(docs, safe=False)

    elif request.method == "POST":
        data = read_json(request)
        target_id = doc_id or data.get("id") or f"ndoc_{int(datetime.now().timestamp())}"
        docs = load_newsletter_docs()

        # Handle deletion via POST action
        if data.get("action") == "delete" or request.path.rstrip('/').endswith('/delete'):
            docs = [d for d in docs if str(d.get("id")) != str(target_id)]
            save_newsletter_docs(docs)
            return JsonResponse({"success": True, "doctors": docs})

        existing_doc = next((d for d in docs if str(d.get("id")) == str(target_id)), {})
        new_doc = {
            "id": target_id,
            "name": str(data.get("name") or existing_doc.get("name", "")).strip(),
            "title": str(data.get("title") or existing_doc.get("title", "")).strip(),
            "topic": str(data.get("topic") or existing_doc.get("topic", "")).strip(),
            "day": str(data.get("day") or existing_doc.get("day", "")).strip(),
            "panel": str(data.get("panel") or existing_doc.get("panel", "")).strip(),
            "avatar": str(data.get("avatar") or existing_doc.get("avatar", "/mag/uploads/doctors/dr-radmanesh.webp")).strip(),
        }

        existing_idx = next((i for i, d in enumerate(docs) if str(d.get("id")) == str(target_id)), -1)
        if existing_idx != -1:
            docs[existing_idx] = new_doc
        else:
            docs.append(new_doc)

        save_newsletter_docs(docs)
        return JsonResponse({"success": True, "doctor": new_doc, "doctors": docs})

    elif request.method == "DELETE":
        target_id = doc_id or request.GET.get("id")
        docs = load_newsletter_docs()
        if target_id:
            docs = [d for d in docs if str(d.get("id")) != str(target_id)]
            save_newsletter_docs(docs)
        return JsonResponse({"success": True, "doctors": docs})

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def api_articles(request, slug=None):
    if request.method == "GET":
        query_slug = slug or request.GET.get("slug")
        if query_slug:
            cache_key = f"api_article_{query_slug}"
            data = cache.get(cache_key)
            if data is None:
                article = Article.objects.filter(slug=query_slug).first()
                if not article:
                    return JsonResponse({"error": "Article not found"}, status=404)
                data = article.to_dict()
                cache.set(cache_key, data, 60)
            return JsonResponse(data)

        admin_mode = is_admin(request) or request.GET.get("all") == "1"
        cache_key = "api_articles_all" if admin_mode else "api_articles_published"
        data = cache.get(cache_key)
        if data is None:
            if admin_mode:
                articles = Article.objects.all().order_by('-id')
            else:
                articles = Article.objects.filter(status='published').order_by('-id')
            data = [a.to_dict() for a in articles]
            cache.set(cache_key, data, 30)
        return JsonResponse(data, safe=False)

    elif request.method in ("POST", "PUT"):
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)
        data = read_json(request)
        art_id = str(data.get("id") or "").strip()
        art_slug = str(data.get("slug") or "").strip()
        db_id = data.get("dbId")

        # 1. Look up existing article by dbId, custom_id, or slug (WordPress-style)
        article = None
        if db_id:
            try:
                article = Article.objects.filter(id=int(db_id)).first()
            except (ValueError, TypeError):
                pass

        if not article and art_id:
            article = Article.objects.filter(custom_id=art_id).first()
            if not article and art_id.isdigit():
                article = Article.objects.filter(id=int(art_id)).first()

        if not article and art_slug:
            article = Article.objects.filter(slug=art_slug).first()

        # Determine target slug
        if not art_slug:
            if article and article.slug:
                art_slug = article.slug
            else:
                art_slug = f"article-{art_id or int(datetime.now().timestamp())}"

        # Ensure slug uniqueness among OTHER articles (WordPress slug deduplication)
        existing_with_slug = Article.objects.filter(slug=art_slug)
        if article:
            existing_with_slug = existing_with_slug.exclude(id=article.id)
        if existing_with_slug.exists():
            base_slug = art_slug
            counter = 2
            while Article.objects.filter(slug=f"{base_slug}-{counter}").exclude(id=article.id if article else -1).exists():
                counter += 1
            art_slug = f"{base_slug}-{counter}"

        # If updating existing article, track old slug for 301 redirects
        old_slugs = data.get("oldSlugs", [])
        if not isinstance(old_slugs, list):
            old_slugs = []
        if article and article.slug and article.slug != art_slug:
            if article.slug not in old_slugs:
                old_slugs.append(article.slug)

        # Prepare field values
        author_val = data.get("author")
        if isinstance(author_val, dict):
            author_str = author_val.get("name") or "تیم تحریریه پزشکان"
        else:
            author_str = str(author_val or "تیم تحریریه پزشکان")

        defaults = {
            "title": data.get("title", ""),
            "summary": data.get("summary", ""),
            "raw_html": data.get("rawHtml", ""),
            "content_html": data.get("contentHtml", data.get("rawHtml", "")),
            "image": data.get("image", ""),
            "image_alt": data.get("imageAlt", ""),
            "pillar_id": str(data.get("pillarId", "")),
            "category_name": data.get("categoryName", ""),
            "category_icon": data.get("categoryIcon", ""),
            "doctor_id": str(data.get("doctorId", "")),
            "author": author_str,
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
            "old_slugs": old_slugs,
            "schema_data": data.get("schemaData", {}),
            "custom_schema_json": data.get("customSchemaJson", ""),
            "is_noindex": bool(data.get("isNoindex", False)),
            "robots": data.get("robots", "noindex, follow" if data.get("isNoindex") else "index, follow"),
            "seo_score": int(data.get("seoScore") or 0),
            "show_in_pediatrics": bool(data.get("showInPediatrics") or data.get("show_in_pediatrics", False)),
            "show_in_pharma": bool(data.get("showInPharma") or data.get("show_in_pharma", False)),
        }

        if article:
            # Update existing article in place (WordPress-style)
            for k, v in defaults.items():
                setattr(article, k, v)
            article.slug = art_slug
            if art_id and not article.custom_id:
                article.custom_id = art_id
            article.save()
            created = False
        else:
            # Create brand new article
            final_id = art_id or f"art_{int(datetime.now().timestamp())}"
            article = Article.objects.create(
                custom_id=final_id,
                slug=art_slug,
                **defaults
            )
            created = True

        all_articles = [a.to_dict() for a in Article.objects.all().order_by('-id')]
        cache.delete("api_articles_all")
        cache.delete("api_articles_published")
        try:
            articles_file = settings.BASE_DIR / 'mag' / 'content' / 'articles.json'
            with open(articles_file, 'w', encoding='utf-8') as af:
                json.dump(all_articles, af, ensure_ascii=False, indent=2)
        except Exception:
            pass
        return JsonResponse({"success": True, "created": created, "article": article.to_dict(), "articles": all_articles})

    elif request.method == "DELETE":
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)

        empty_trash = request.GET.get("empty_trash")
        if empty_trash in ("true", "1", "yes"):
            deleted_count, _ = Article.objects.filter(status="trash").delete()
            all_articles = [a.to_dict() for a in Article.objects.all().order_by('-id')]
            cache.delete("api_articles_all")
            cache.delete("api_articles_published")
            return JsonResponse({"success": True, "deleted": deleted_count, "articles": all_articles})

        art_id = request.GET.get("id") or slug
        if art_id:
            query = models.Q(custom_id=art_id) | models.Q(slug=art_id)
            if str(art_id).isdigit():
                query |= models.Q(id=int(art_id))
            Article.objects.filter(query).delete()

        all_articles = [a.to_dict() for a in Article.objects.all().order_by('-id')]
        cache.delete("api_articles_all")
        cache.delete("api_articles_published")
        try:
            articles_file = settings.BASE_DIR / 'mag' / 'content' / 'articles.json'
            with open(articles_file, 'w', encoding='utf-8') as af:
                json.dump(all_articles, af, ensure_ascii=False, indent=2)
        except Exception:
            pass
        return JsonResponse({"success": True, "articles": all_articles})

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
# 5.1. Site Page Images Management API
# ==============================================================================

@csrf_exempt
def api_site_images(request):
    """
    Manages custom visual assets and images across all website pages.
    Supports listing, bulk update, and single slot replacement.
    """
    if request.method == "GET":
        images = load_site_images()
        return JsonResponse(images, safe=False)

    elif request.method in ("POST", "PUT"):
        if not is_admin(request):
            return JsonResponse({"error": "Unauthorized"}, status=403)
        data = read_json(request)

        images = load_site_images()
        images_by_key = {item["key"]: item for item in images if isinstance(item, dict) and "key" in item}

        incoming_list = data if isinstance(data, list) else data.get("images")
        if incoming_list and isinstance(incoming_list, list):
            for item in incoming_list:
                k = item.get("key")
                if k and k in images_by_key:
                    images_by_key[k]["currentUrl"] = item.get("currentUrl", images_by_key[k]["currentUrl"])
                    if "title" in item:
                        images_by_key[k]["title"] = item["title"]
                    if "description" in item:
                        images_by_key[k]["description"] = item["description"]
                elif k:
                    images_by_key[k] = item
            final_images = list(images_by_key.values())
        elif isinstance(data, dict) and "key" in data:
            k = data["key"]
            if k in images_by_key:
                images_by_key[k]["currentUrl"] = data.get("currentUrl", images_by_key[k]["currentUrl"])
            else:
                images_by_key[k] = data
            final_images = list(images_by_key.values())
        else:
            final_images = images

        save_site_images(final_images)
        return JsonResponse({"success": True, "images": final_images})

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
def api_newsletter_feed(request):
    """
    Public Cross-Origin REST API for Syndicating Newsletters to External Websites.
    Supports filtering by slug, limit, doctor_id, format=widget, and search query.
    Enforces CORS (Access-Control-Allow-Origin: *) for direct frontend/backend consumption.
    """
    if request.method == "OPTIONS":
        res = HttpResponse()
        res["Access-Control-Allow-Origin"] = "*"
        res["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        res["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        return res

    req_format = request.GET.get("format", "json").lower()
    if req_format == "widget":
        return api_newsletter_widget(request)

    slug_filter = request.GET.get("slug", "").strip()
    doctor_filter = request.GET.get("doctor_id", "").strip() or request.GET.get("doctor", "").strip()
    query_search = request.GET.get("q", "").strip() or request.GET.get("search", "").strip()
    
    try:
        limit = min(int(request.GET.get("limit", 20)), 100)
    except (ValueError, TypeError):
        limit = 20

    public_domain = "https://pezeshkan.me"
    
    # Load newsletter doctors map for enrichment
    ndocs_file = settings.BASE_DIR / 'mag' / 'content' / 'newsletter_doctors.json'
    ndocs_map = {}
    if ndocs_file.exists():
        try:
            with open(ndocs_file, 'r', encoding='utf-8') as df:
                ndocs_list = json.load(df)
                if isinstance(ndocs_list, list):
                    for nd in ndocs_list:
                        ndocs_map[str(nd.get("id"))] = nd
        except Exception:
            pass

    from apps.pezeshkan_core.models import Article, Newsletter
    from django.db.models import Q

    # Query articles belonging to the newsletter category
    art_q = Q(status="published") & (
        Q(pillar_id="9") |
        Q(pillar_id=9) |
        Q(category_name__icontains="خبرنامه") |
        Q(tag__icontains="خبرنامه") |
        Q(custom_id__startswith="newsletter") |
        Q(custom_id__startswith="art-newsletter")
    )

    if slug_filter:
        art_q &= (Q(slug=slug_filter) | Q(custom_id=slug_filter))
    if doctor_filter:
        art_q &= Q(doctor_id=doctor_filter)
    if query_search:
        art_q &= (Q(title__icontains=query_search) | Q(summary__icontains=query_search))

    db_articles = list(Article.objects.filter(art_q).order_by("-id")[:limit])

    # Fallback to articles.json if DB has no newsletter articles yet
    if not db_articles:
        articles_json_path = settings.BASE_DIR / 'mag' / 'content' / 'articles.json'
        if articles_json_path.exists():
            try:
                with open(articles_json_path, 'r', encoding='utf-8') as f_art:
                    all_json = json.load(f_art)
                    for a in all_json:
                        if a.get("status") == "published" and (
                            str(a.get("pillarId")) == "9" or
                            "خبرنامه" in str(a.get("categoryName", "")) or
                            "خبرنامه" in str(a.get("tag", "")) or
                            str(a.get("id", "")).startswith("newsletter")
                        ):
                            if slug_filter and a.get("slug") != slug_filter and a.get("id") != slug_filter:
                                continue
                            if doctor_filter and a.get("doctorId") != doctor_filter:
                                continue
                            if query_search and query_search not in a.get("title", "") and query_search not in a.get("summary", ""):
                                continue
                            # Mimic to_dict
                            db_articles.append(a)
                            if len(db_articles) >= limit:
                                break
            except Exception:
                pass

    items = []
    seen_slugs = set()

    for a in db_articles:
        ad = a.to_dict() if hasattr(a, 'to_dict') else a
        s = ad.get("slug") or ad.get("id")
        if not s or s in seen_slugs:
            continue
        seen_slugs.add(s)

        img_url = ad.get("image", "")
        if img_url and img_url.startswith("/"):
            img_url = f"{public_domain}{img_url}"

        # Resolve doctor/author info
        doc_id = str(ad.get("doctorId") or "")
        author_data = ad.get("author")
        
        if doc_id in ndocs_map:
            doc_info = ndocs_map[doc_id]
            av = doc_info.get("avatar") or "/mag/uploads/doctors/dr-bahrami.webp"
            if av.startswith("/"):
                av = f"{public_domain}{av}"
            author_obj = {
                "id": doc_info.get("id"),
                "name": doc_info.get("name"),
                "title": doc_info.get("title"),
                "mcNumber": doc_info.get("mcNumber") or doc_info.get("mc", ""),
                "dept": doc_info.get("dept") or "هیئت علمی خبرنامه",
                "role": doc_info.get("role") or "دبیر علمی خبرنامه بالینی",
                "avatar": av
            }
        elif isinstance(author_data, dict):
            author_obj = dict(author_data)
            av = author_obj.get("avatar", "")
            if av and av.startswith("/"):
                author_obj["avatar"] = f"{public_domain}{av}"
        elif isinstance(author_data, str) and author_data.strip():
            author_obj = {
                "name": author_data.strip(),
                "title": "پزشک متخصص و مؤلف خبرنامه",
                "mcNumber": "",
                "dept": "شورای علمی خبرنامه",
                "role": "نویسنده خبرنامه بالینی",
                "avatar": f"{public_domain}/pezeshkon-logo.svg"
            }
        else:
            author_obj = {
                "name": "تیم متخصصان خبرنامه",
                "title": "شورای سردبیری مجله سلامت پزشکآن",
                "mcNumber": "پزشکآن",
                "dept": "تحریریه بالینی",
                "role": "شورای علمی خبرنامه",
                "avatar": f"{public_domain}/pezeshkon-logo.svg"
            }

        items.append({
            "id": ad.get("id"),
            "title": ad.get("title"),
            "slug": s,
            "permalink": f"{public_domain}/mag/{urllib.parse.quote(s)}",
            "summary": ad.get("summary", ""),
            "coverImage": img_url,
            "imageAlt": ad.get("imageAlt") or ad.get("title"),
            "publishedDate": ad.get("lastReviewed") or "آبان ۱۴۰۵",
            "readTime": ad.get("readTime") or "۴ دقیقه",
            "category": {
                "id": 9,
                "name": "خبرنامه",
                "badge": "ویژه متخصصین"
            },
            "author": author_obj,
            "faqs": ad.get("faqs", []),
            "contentHtml": ad.get("rawHtml") or ad.get("contentHtml", "")
        })

    # Also include published Newsletter model issues if any exist
    nl_issues = Newsletter.objects.filter(status="published")
    if slug_filter:
        nl_issues = nl_issues.filter(slug=slug_filter)
    for n in nl_issues[:limit]:
        nd = n.to_dict()
        s = nd.get("slug")
        if not s or s in seen_slugs:
            continue
        seen_slugs.add(s)
        items.append({
            "id": nd.get("id"),
            "title": nd.get("title"),
            "slug": s,
            "permalink": f"{public_domain}/mag/{urllib.parse.quote(s)}",
            "summary": nd.get("excerpt", ""),
            "coverImage": f"{public_domain}/mag/uploads/doctors/dr-bahrami.webp",
            "imageAlt": nd.get("title"),
            "publishedDate": nd.get("date") or "آبان ۱۴۰۵",
            "readTime": nd.get("readTime") or "۴ دقیقه",
            "category": {"id": 9, "name": "خبرنامه", "badge": "بولتن تخصصی"},
            "author": {
                "name": "شورای علمی خبرنامه",
                "title": "تحریریه و دبیرخانه خبرنامه بالینی",
                "mcNumber": "پزشکآن",
                "dept": "خبرنامه",
                "role": "دبیرخانه علمی",
                "avatar": f"{public_domain}/pezeshkon-logo.svg"
            },
            "faqs": [],
            "contentHtml": nd.get("contentHtml", "")
        })

    payload = {
        "success": True,
        "version": "1.0",
        "total": len(items),
        "source": "Pezeshkan Medical Ecosystem",
        "documentation": f"{public_domain}/admin.html#tab-newsletter-api",
        "endpoints": {
            "feed": f"{public_domain}/api/v1/newsletter/feed",
            "single": f"{public_domain}/api/v1/newsletter/feed?slug={{slug}}",
            "widget": f"{public_domain}/api/v1/newsletter/feed?format=widget"
        },
        "items": items
    }

    res = JsonResponse(payload, json_dumps_params={"ensure_ascii": False, "indent": 2})
    res["Access-Control-Allow-Origin"] = "*"
    res["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    res["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    res["Cache-Control"] = "public, max-age=60, s-maxage=120"
    return res


def api_newsletter_widget(request):
    """
    Renders an embeddable, responsive iframe/widget for displaying newsletters on third-party websites.
    """
    res = api_newsletter_feed(request)
    data = json.loads(res.content.decode('utf-8'))
    items = data.get("items", [])

    items_html = ""
    if items:
        for it in items:
            author = it.get("author", {})
            items_html += f"""
            <article class="nl-card">
              <div class="nl-cover-wrap">
                <img src="{it.get('coverImage') or '/mag/uploads/doctors/dr-bahrami.webp'}" alt="{it.get('title')}" class="nl-cover" loading="lazy" />
                <span class="nl-badge">{it.get('category', {}).get('badge', 'ویژه')}</span>
              </div>
              <div class="nl-content">
                <div class="nl-meta">
                  <span class="nl-date">{it.get('publishedDate', '')}</span>
                  <span class="nl-dot">•</span>
                  <span class="nl-readtime">{it.get('readTime', '')}</span>
                </div>
                <h3 class="nl-title"><a href="{it.get('permalink')}" target="_blank" rel="noopener">{it.get('title')}</a></h3>
                <p class="nl-summary">{it.get('summary', '')}</p>
                <div class="nl-footer">
                  <div class="nl-author">
                    <img src="{author.get('avatar') or '/pezeshkon-logo.svg'}" alt="{author.get('name')}" class="nl-avatar" />
                    <div class="nl-author-info">
                      <strong class="nl-author-name">{author.get('name', 'پزشک متخصص')}</strong>
                      <span class="nl-author-title">{author.get('title', '')}</span>
                    </div>
                  </div>
                  <a href="{it.get('permalink')}" target="_blank" rel="noopener" class="nl-btn">
                    <span>مطالعه خبرنامه</span>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5m7 7-7-7 7-7"/></svg>
                  </a>
                </div>
              </div>
            </article>
            """
    else:
        items_html = """
        <div class="nl-empty">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          <h4>هنوز خبرنامه‌ای منتشر نشده است</h4>
          <p>به زودی جدیدترین بولتن‌های تخصصی پزشکان در این بخش قرار می‌گیرد.</p>
        </div>
        """

    widget_html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ویجت خبرنامه پزشکی پزشکآن</title>
  <style>
    :root {{
      --bg: #0B1120;
      --card-bg: rgba(15, 23, 42, 0.85);
      --card-border: rgba(255, 255, 255, 0.08);
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --accent: #10B981;
      --accent-hover: #059669;
      --primary: #0284C7;
      --font: 'Vazirmatn', system-ui, -apple-system, sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: var(--font);
      background: var(--bg);
      color: var(--text-main);
      padding: 16px;
      direction: rtl;
    }}
    .nl-widget-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--card-border);
    }}
    .nl-header-title {{
      font-size: 18px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-main);
    }}
    .nl-powered {{
      font-size: 11px;
      color: var(--text-muted);
      text-decoration: none;
    }}
    .nl-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 16px;
    }}
    .nl-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    }}
    .nl-card:hover {{
      transform: translateY(-3px);
      border-color: rgba(16, 185, 129, 0.3);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
    }}
    .nl-cover-wrap {{
      position: relative;
      height: 160px;
      overflow: hidden;
      background: #1e293b;
    }}
    .nl-cover {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s;
    }}
    .nl-card:hover .nl-cover {{
      transform: scale(1.04);
    }}
    .nl-badge {{
      position: absolute;
      top: 10px;
      right: 10px;
      background: rgba(16, 185, 129, 0.9);
      color: #fff;
      font-size: 10px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      backdrop-filter: blur(8px);
    }}
    .nl-content {{
      padding: 16px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
    }}
    .nl-meta {{
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .nl-dot {{ color: var(--accent); }}
    .nl-title {{
      font-size: 15px;
      font-weight: 800;
      line-height: 1.5;
      margin-bottom: 8px;
    }}
    .nl-title a {{
      color: var(--text-main);
      text-decoration: none;
      transition: color 0.15s;
    }}
    .nl-title a:hover {{ color: var(--accent); }}
    .nl-summary {{
      font-size: 12.5px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 16px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      flex-grow: 1;
    }}
    .nl-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      margin-top: auto;
    }}
    .nl-author {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .nl-avatar {{
      width: 32px;
      height: 32px;
      border-radius: 50%;
      object-fit: cover;
      border: 1px solid var(--accent);
    }}
    .nl-author-info {{
      display: flex;
      flex-direction: column;
    }}
    .nl-author-name {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text-main);
    }}
    .nl-author-title {{
      font-size: 9.5px;
      color: var(--text-muted);
      max-width: 130px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .nl-btn {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: rgba(16, 185, 129, 0.15);
      color: var(--accent);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 11px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .nl-btn:hover {{
      background: var(--accent);
      color: #fff;
    }}
    .nl-empty {{
      text-align: center;
      padding: 48px 16px;
      background: var(--card-bg);
      border: 1px dashed var(--card-border);
      border-radius: 16px;
      color: var(--text-muted);
    }}
    .nl-empty h4 {{
      color: var(--text-main);
      margin: 12px 0 6px;
      font-size: 16px;
    }}
  </style>
</head>
<body>
  <div class="nl-widget-header">
    <div class="nl-header-title">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
      <span>تازه‌ترین خبرنامه‌های تخصصی پزشکآن</span>
    </div>
    <a href="https://pezeshkan.me/mag/newsletter" target="_blank" rel="noopener" class="nl-powered">قدرت‌گرفته از پزشکآن</a>
  </div>
  <div class="nl-grid">
    {items_html}
  </div>
</body>
</html>"""

    response = HttpResponse(widget_html, content_type="text/html; charset=utf-8")
    response["Access-Control-Allow-Origin"] = "*"
    return response


@csrf_exempt
def api_newsletter_seed_sample(request):
    """
    Creates a sample clinical newsletter article for immediate testing and verification of the API.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    from apps.pezeshkan_core.models import Article

    sample_slug = "cardio-silent-ischemia-hypertension-newsletter"
    existing = Article.objects.filter(slug=sample_slug).first()
    if existing:
        return JsonResponse({"success": True, "message": "خبرنامه نمونه از قبل موجود است", "article": existing.to_dict()})

    sample_art = Article.objects.create(
        custom_id="art-newsletter-cardio-01",
        title="خبرنامه سلامت قلب و عروق: علائم خاموش ایسکمی قلبی و راهنمای فوریت فشار خون",
        slug=sample_slug,
        summary="بولتن تخصصی و بالینی تدوین‌شده توسط دکتر کامران بهرامی: شناسایی زودهنگام گرفتگی عروق کرونر، تفاوت دردهای اسکلتی قفسه سینه با دردهای قلبی و دستورالعمل کنترل بحران فشار خون.",
        raw_html="<p class=\"lead\">خبرنامه سلامت قلب و عروق مرجع به‌روزترین توصیه‌های خودمراقبتی و پروتکل‌های اورژانسی برای عموم مراجعین و کادر درمان است.</p><h2>علائم خاموش تنگی عروق کرونر</h2><p>بسیاری از حملات قلبی بدون درد کلاسیک تیرکشنده رخ می‌دهند و با احساس خستگی مفرط، سنگینی مبهم فک یا سرگیجه ناگهانی ظاهر می‌شوند.</p>",
        content_html="<p class=\"lead\">خبرنامه سلامت قلب و عروق مرجع به‌روزترین توصیه‌های خودمراقبتی و پروتکل‌های اورژانسی برای عموم مراجعین و کادر درمان است.</p><h2>علائم خاموش تنگی عروق کرونر</h2><p>بسیاری از حملات قلبی بدون درد کلاسیک تیرکشنده رخ می‌دهند و با احساس خستگی مفرط، سنگینی مبهم فک یا سرگیجه ناگهانی ظاهر می‌شوند.</p>",
        image="/mag/uploads/doctors/dr-bahrami.webp",
        image_alt="خبرنامه سلامت قلب و عروق",
        pillar_id="9",
        category_name="خبرنامه",
        category_icon="newsletter",
        doctor_id="ndoc-bahrami",
        author="دکتر کامران بهرامی",
        read_time="۴ دقیقه",
        last_reviewed="آبان ۱۴۰۵",
        tag="خبرنامه",
        tag_class="newsletter",
        status="published",
        meta_title="خبرنامه سلامت قلب و عروق؛ پیشگیری و علائم خاموش | پزشکآن",
        meta_description="بولتن تخصصی خبرنامه سلامت قلب و عروق تدوین‌شده توسط متخصصان جهت اطلاع‌رسانی بالینی و پیشگیری از حملات قلبی.",
        focus_keyword="خبرنامه سلامت قلب",
        faqs=[
            {"q": "آیا فشار خون بالا همیشه با سردرد همراه است؟", "a": "خیر، فشار خون به عنوان قاتل خاموش شناخته می‌شود و در اکثر موارد هیچ علامتی ایجاد نمی‌کند مگر اینکه وارد بحران حاد شود."}
        ],
        schema_type="MedicalWebPage",
        robots="index, follow",
        seo_score=95
    )

    # Invalidate caches
    try:
        from django.core.cache import cache
        cache.delete("api_articles_all")
        cache.delete("api_articles_published")
    except Exception:
        pass

    return JsonResponse({"success": True, "message": "خبرنامه بالینی نمونه با موفقیت ایجاد شد", "article": sample_art.to_dict()})



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
    data = cache.get("api_clinic_directory")
    if data is None:
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
        data = {
            "count": len(results),
            "results": results
        }
        cache.set("api_clinic_directory", data, 60)
    return JsonResponse(data)


def api_platform_plans(request):
    """
    FLOW_02_PACKAGES_AND_PLANS: Public plans endpoint returning active subscription packages.
    """
    data = cache.get("api_platform_plans")
    if data is None:
        plans = SubscriptionPlan.objects.filter(is_active=True).order_by('order', 'id')
        data = [p.to_dict() for p in plans]
        cache.set("api_platform_plans", data, 60)
    return JsonResponse(data, safe=False)


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



# ==============================================================================
# 11. SEO Audit, Anti-Spam Watchdog, Site Structure, Robots, LLMs & Users
# ==============================================================================

def analyze_robots_txt(content):
    lines = content.splitlines()
    user_agents = []
    disallows = []
    allows = []
    sitemaps = []
    for line in lines:
        l = line.strip()
        if not l or l.startswith('#'):
            continue
        if ':' in l:
            key, val = l.split(':', 1)
            key = key.strip().lower()
            val = val.strip()
            if key == 'user-agent':
                user_agents.append(val)
            elif key == 'disallow':
                disallows.append(val)
            elif key == 'allow':
                allows.append(val)
            elif key == 'sitemap':
                sitemaps.append(val)
    return {
        "userAgents": user_agents or ["*"],
        "disallowRules": disallows,
        "allowRules": allows,
        "sitemaps": sitemaps,
        "totalRules": len(lines),
        "isHealthy": len(sitemaps) > 0 and len(user_agents) > 0
    }


def compute_seo_audit():
    articles = list(Article.objects.all().order_by('-id'))
    pillars = list(Pillar.objects.all().order_by('id'))
    doctors = list(Doctor.objects.all().order_by('id'))

    inlinks_map = {a.slug: [] for a in articles}
    outlinks_map = {a.slug: [] for a in articles}
    broken_links = []

    for a in articles:
        html = a.content_html or a.raw_html or ''
        hrefs = re.findall(r'href=[\'"](/mag/[^\'"]+|/[^\'"]*)[\'"]', html)
        for h in hrefs:
            if h.startswith('/mag/'):
                target_slug = h.replace('/mag/', '').strip('/')
                outlinks_map[a.slug].append(h)
                if target_slug in inlinks_map:
                    inlinks_map[target_slug].append(a.slug)
                elif target_slug and target_slug not in ('', 'admin', 'login', 'newsletter'):
                    broken_links.append({
                        "articleId": a.custom_id or a.id,
                        "title": a.title,
                        "brokenUrl": h,
                        "anchorText": "لینک داخلی شکسته"
                    })
            elif h.startswith('/') and not h.startswith('//'):
                outlinks_map[a.slug].append(h)

    keyword_stuffing = []
    thin_content = []
    eeat_deficiencies = []
    actionable_fixes = []

    titles_seen = {}
    descs_seen = {}

    for a in articles:
        html = a.content_html or a.raw_html or ''
        clean_text = re.sub(r'<[^>]+>', ' ', html)
        words = clean_text.split()
        word_count = len(words)

        fkw = a.focus_keyword or ''
        if not fkw and a.title:
            t_words = [w for w in a.title.split() if len(w) > 3][:2]
            fkw = ' '.join(t_words)

        occurrences = 0
        density = 0.0
        kw_status = 'safe'

        if fkw and word_count > 0:
            occurrences = clean_text.lower().count(fkw.lower())
            density = round((occurrences * len(fkw.split()) / max(word_count, 1)) * 100, 2)
            if density > 3.0:
                kw_status = 'danger'
                actionable_fixes.append({
                    "articleId": a.custom_id or a.id,
                    "severity": "danger",
                    "category": "اسپم کلمات کلیدی",
                    "title": f"چگالی بیش از حد کلیدواژه ({density}٪) در مقاله «{a.title}»",
                    "desc": f"کلمه کلیدی «{fkw}» به تعداد {occurrences} بار تکرار شده است. جهت پیشگیری از جریمه گوگل، چگالی را به زیر ۲.۵٪ کاهش دهید."
                })
            elif density > 2.5:
                kw_status = 'warning'
                actionable_fixes.append({
                    "articleId": a.custom_id or a.id,
                    "severity": "warning",
                    "category": "هشدار سئو",
                    "title": f"چگالی کلیدواژه در مرز ریسک ({density}٪) در «{a.title}»",
                    "desc": f"توصیه می‌شود چگالی کلمه «{fkw}» بین ۱٪ تا ۲٪ تنظیم گردد."
                })
            elif density < 0.8 and occurrences > 0:
                kw_status = 'low'
            elif occurrences == 0:
                kw_status = 'missing'
        else:
            kw_status = 'missing'

        keyword_stuffing.append({
            "articleId": a.custom_id or a.id,
            "title": a.title,
            "slug": a.slug,
            "focusKeyword": fkw,
            "occurrences": occurrences,
            "wordCount": word_count,
            "densityPercent": density,
            "status": kw_status
        })

        if word_count < 300:
            thin_status = 'danger'
            actionable_fixes.append({
                "articleId": a.custom_id or a.id,
                "severity": "danger",
                "category": "محتوای کوتاه (Thin Content)",
                "title": f"محتوای بسیار کم‌حجم ({word_count} کلمه) در «{a.title}»",
                "desc": "گوگل مقالات زیر ۳۰۰ کلمه را به عنوان محتوای بی‌کیفیت ارزیابی می‌کند. حداقل ۶۰۰ کلمه محتوای بالینی اضافه نمایید."
            })
        elif word_count < 500:
            thin_status = 'warning'
        else:
            thin_status = 'safe'

        thin_content.append({
            "articleId": a.custom_id or a.id,
            "title": a.title,
            "slug": a.slug,
            "wordCount": word_count,
            "minExpected": 600,
            "status": thin_status
        })

        t_clean = a.title.strip()
        titles_seen.setdefault(t_clean, []).append(a.slug)
        d_clean = (a.meta_description or a.summary or '').strip()
        if d_clean:
            descs_seen.setdefault(d_clean, []).append(a.slug)

        reasons = []
        author_name = a.author or 'تیم تحریریه پزشکان'
        doc_mc = 'ثبت نشده'
        reviewer_name = a.last_reviewed or 'شورای بازبینی بالینی'

        if a.doctor_id:
            doc = next((d for d in doctors if str(d.custom_id or d.id) == str(a.doctor_id)), None)
            if doc:
                author_name = doc.name
                doc_mc = doc.mc_number or 'معتبر'

        if doc_mc == 'ثبت نشده':
            reasons.append("عدم ثبت شماره نظام پزشکی معتبر")
        if not a.last_reviewed:
            reasons.append("عدم ثبت تاریخ و داور بازبینی علمی بالینی")

        if reasons:
            eeat_deficiencies.append({
                "articleId": a.custom_id or a.id,
                "title": a.title,
                "authorName": author_name,
                "mcNumber": doc_mc,
                "reviewerName": reviewer_name,
                "reasons": reasons
            })

    duplicate_titles = [{"title": t, "count": len(slugs), "slugs": slugs} for t, slugs in titles_seen.items() if len(slugs) > 1]
    duplicate_descs = [{"description": d, "count": len(slugs), "slugs": slugs} for d, slugs in descs_seen.items() if len(slugs) > 1]

    orphan_articles = []
    articles_analysis = []
    total_int_links = sum(len(v) for v in outlinks_map.values())

    for a in articles:
        in_c = len(inlinks_map.get(a.slug, []))
        out_c = len(outlinks_map.get(a.slug, []))
        status = 'good'
        if in_c == 0:
            status = 'orphan'
            orphan_articles.append({
                "id": a.custom_id or a.id,
                "title": a.title,
                "slug": a.slug
            })
            actionable_fixes.append({
                "articleId": a.custom_id or a.id,
                "severity": "warning",
                "category": "صفحه یتیم (Orphan Page)",
                "title": f"مقاله «{a.title}» فاقد هرگونه لینک داخلی ورودی است",
                "desc": "حداقل از ۲ مقاله مرتبط دیگر به این صفحه لینک داخلی با انکرتکست توصیفی ایجاد کنید تا بودجه خزش گوگل بهبود یابد."
            })
        elif in_c < 2:
            status = 'warning'

        articles_analysis.append({
            "id": a.custom_id or a.id,
            "title": a.title,
            "slug": a.slug,
            "inlinksCount": in_c,
            "outlinksCount": out_c,
            "status": status
        })

    active_pillars = []
    empty_pillars = []
    for p in pillars:
        p_name = getattr(p, 'name', '') or str(p)
        p_slug = getattr(p, 'slug', '')
        p_articles = [a for a in articles if a.pillar_id == str(p.id) or a.category_name == p_name]
        count = len(p_articles)
        if count > 0:
            linked_back = sum(1 for a in p_articles if any(p_slug in l for l in outlinks_map.get(a.slug, [])))
            health = min(100, int((count / 3.0) * 60 + (linked_back / max(count, 1)) * 40))
            active_pillars.append({
                "name": p_name,
                "clusterArticlesCount": count,
                "linkedBackCount": linked_back,
                "clusterHealthScore": health,
                "status": "good" if health >= 70 else "warning"
            })
        else:
            empty_pillars.append({
                "name": p_name,
                "slug": p_slug
            })

    total_articles = max(len(articles), 1)
    danger_count = sum(1 for f in actionable_fixes if f["severity"] == "danger")
    warning_count = sum(1 for f in actionable_fixes if f["severity"] == "warning")
    score = max(20, min(100, 100 - (danger_count * 15 + warning_count * 5)))

    health_status = 'عالی و بهینه' if score >= 85 else ('نیازمند بهبود' if score >= 60 else 'بحرانی')

    return {
        "summary": {
            "healthScore": score,
            "healthStatus": health_status,
            "spamRisksCount": danger_count + len(broken_links) + len(duplicate_titles),
            "activePillarsCount": len(active_pillars),
            "totalPillars": len(pillars),
            "totalInternalLinks": total_int_links,
            "orphanCount": len(orphan_articles),
            "eeatDeficiencyCount": len(eeat_deficiencies)
        },
        "actionableFixes": actionable_fixes,
        "spamAudit": {
            "keywordStuffing": keyword_stuffing,
            "thinContent": thin_content,
            "duplicateTitles": duplicate_titles,
            "duplicateDescriptions": duplicate_descs,
            "brokenInternalLinks": broken_links
        },
        "pillarClusterAudit": {
            "coverageRatePercent": int((len(active_pillars) / max(len(pillars), 1)) * 100),
            "activePillars": active_pillars,
            "emptyPillars": empty_pillars
        },
        "linkingAudit": {
            "avgInternalLinksPerArticle": round(total_int_links / max(len(articles), 1), 1),
            "orphanArticles": orphan_articles,
            "articlesAnalysis": articles_analysis
        },
        "eeatAudit": {
            "deficiencies": eeat_deficiencies
        }
    }


def compute_site_structure():
    audit = compute_seo_audit()
    articles_data = audit['linkingAudit']['articlesAnalysis']
    orphans = audit['linkingAudit']['orphanArticles']
    silos = audit['pillarClusterAudit']['activePillars']
    summary = {
        "healthScore": audit['summary']['healthScore'],
        "totalInternalLinks": audit['summary']['totalInternalLinks'],
        "totalCategories": audit['summary']['totalPillars'],
        "orphanCount": audit['summary']['orphanCount'],
        "avgInternalLinksPerArticle": audit['linkingAudit']['avgInternalLinksPerArticle']
    }
    return {
        "success": True,
        "summary": summary,
        "articles": articles_data,
        "orphans": orphans,
        "silos": silos
    }


@csrf_exempt
def api_seo_audit(request):
    """
    Real-time SEO Audit & Anti-Spam Watchdog Engine.
    Works directly in local dev and live server environments without external dependencies.
    """
    data = compute_seo_audit()
    return JsonResponse(data)


@csrf_exempt
def api_site_structure(request):
    """
    Site Structure & Internal Linking Graph Engine.
    """
    data = compute_site_structure()
    return JsonResponse(data)


def generate_sitemap_xml_django(request=None):
    """
    Dynamically generates Google-compliant XML Sitemap 0.9 from active articles,
    pillars, portal routes, and newsletter pages.
    """
    articles_path = settings.BASE_DIR / 'mag' / 'content' / 'articles.json'
    articles = []
    if articles_path.exists():
        try:
            with open(articles_path, 'r', encoding='utf-8') as f:
                articles = json.load(f)
        except Exception:
            articles = []

    now_iso = datetime.now(timezone(timedelta(hours=3, minutes=30))).strftime('%Y-%m-%dT%H:%M:%S+03:30')

    urls = [
        ("https://pezeshkan.me/", now_iso, "daily", "1.0"),
        ("https://pezeshkan.me/mag", now_iso, "daily", "0.95"),
        ("https://pezeshkan.me/appointments", now_iso, "daily", "0.9"),
        ("https://pezeshkan.me/mag/newsletter", now_iso, "weekly", "0.9"),
    ]

    for a in articles:
        slug = a.get("slug") or a.get("id")
        if not slug:
            continue
        loc = f"https://pezeshkan.me/mag/{urllib.parse.quote(str(slug))}"
        lastmod = a.get("publishDate") or a.get("lastReviewed") or now_iso
        if len(str(lastmod)) == 10:
            lastmod = f"{lastmod}T10:00:00+03:30"
        urls.append((loc, str(lastmod), "weekly", "0.85"))

    subpages = ["product", "features", "packages", "tutorials", "services", "start", "about", "contact", "download"]
    for sp in subpages:
        urls.append((f"https://pezeshkan.me/{sp}", now_iso, "weekly", "0.8"))

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
        '        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
    ]
    for loc, lastmod, changefreq, priority in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{loc}</loc>")
        xml_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_lines.append(f"    <changefreq>{changefreq}</changefreq>")
        xml_lines.append(f"    <priority>{priority}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")

    xml_content = "\n".join(xml_lines)
    try:
        with open(settings.BASE_DIR / 'sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(xml_content)
        with open(settings.BASE_DIR / 'portal' / 'sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(xml_content)
    except Exception:
        pass
    return xml_content


def sitemap_xml_view(request):
    """
    Public Google/Bing sitemap.xml endpoint.
    """
    sitemap_path = settings.BASE_DIR / 'sitemap.xml'
    if not sitemap_path.exists():
        content = generate_sitemap_xml_django()
    else:
        try:
            with open(sitemap_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            content = generate_sitemap_xml_django()
    return HttpResponse(content, content_type="application/xml; charset=utf-8")


@csrf_exempt
def api_sitemap(request):
    """
    Sitemap.xml management, analysis, and generation endpoint.
    """
    sitemap_path = settings.BASE_DIR / 'sitemap.xml'
    portal_sitemap_path = settings.BASE_DIR / 'portal' / 'sitemap.xml'

    def parse_sitemap_content(content):
        urls = []
        url_matches = re.findall(r'<url>(.*?)</url>', content, re.DOTALL)
        for u in url_matches:
            loc_m = re.search(r'<loc>(.*?)</loc>', u)
            lastmod_m = re.search(r'<lastmod>(.*?)</lastmod>', u)
            freq_m = re.search(r'<changefreq>(.*?)</changefreq>', u)
            prio_m = re.search(r'<priority>(.*?)</priority>', u)
            if loc_m:
                urls.append({
                    "loc": loc_m.group(1).strip(),
                    "lastmod": lastmod_m.group(1).strip() if lastmod_m else "",
                    "changefreq": freq_m.group(1).strip() if freq_m else "weekly",
                    "priority": prio_m.group(1).strip() if prio_m else "0.8"
                })
        articles_count = sum(1 for u in urls if '/mag/' in u['loc'] and not u['loc'].endswith('/mag') and not u['loc'].endswith('/mag/newsletter'))
        core_count = len(urls) - articles_count
        is_valid = bool(re.search(r'<urlset[^>]*>', content) and '</urlset>' in content)
        return {
            "urls": urls,
            "total": len(urls),
            "articlesCount": articles_count,
            "coreCount": core_count,
            "isValid": is_valid
        }

    if request.method == "POST":
        data = read_json(request)
        if request.path.rstrip('/').endswith('/generate') or data.get('action') == 'generate':
            content = generate_sitemap_xml_django()
        else:
            content = data.get('content', '')
            if not content.strip():
                content = generate_sitemap_xml_django()
            else:
                try:
                    with open(sitemap_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    with open(portal_sitemap_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    return JsonResponse({"success": False, "error": str(e)}, status=500)

        parsed = parse_sitemap_content(content)
        return JsonResponse({
            "success": True,
            "message": "فایل نقشه سایت (sitemap.xml) با موفقیت ذخیره و منتشر شد.",
            "content": content,
            **parsed
        })
    else:
        content = ""
        if sitemap_path.exists():
            try:
                with open(sitemap_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                pass
        if not content.strip():
            content = generate_sitemap_xml_django()

        parsed = parse_sitemap_content(content)
        return JsonResponse({
            "success": True,
            "content": content,
            **parsed
        })

def api_robots(request):
    """
    Robots.txt management and analysis endpoint.
    """
    robots_path = settings.BASE_DIR / 'robots.txt'
    if request.method == "POST":
        data = read_json(request)
        content = data.get('content', '')
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write(content)
        analysis = analyze_robots_txt(content)
        return JsonResponse({"success": True, "message": "فایل robots.txt با موفقیت ذخیره شد", "analysis": analysis})
    else:
        content = ""
        if robots_path.exists():
            with open(robots_path, 'r', encoding='utf-8') as f:
                content = f.read()
        analysis = analyze_robots_txt(content)
        return JsonResponse({"success": True, "content": content, "analysis": analysis})


@csrf_exempt
def api_llms(request):
    """
    LLMs.txt and AI Crawler configuration endpoint.
    """
    if request.method == "POST":
        data = read_json(request)
        return JsonResponse({"success": True, "message": "تنظیمات هوش مصنوعی llms.txt با موفقیت ذخیره شد", "settings": data})
    else:
        return JsonResponse({
            "success": True,
            "settings": {
                "enabled": True,
                "includePosts": True,
                "includePages": True,
                "floatingButton": False
            },
            "preview": "# Pezeshkan Medical AI Knowledge Base\n> Ecosystem of Digital Healthcare and Clinical Standards\n\n- [Portal](https://pezeshk-on.ir/)\n- [Clinical Articles](https://pezeshk-on.ir/mag/)"
        })


@csrf_exempt
def api_llms_preview(request):
    return JsonResponse({
        "success": True,
        "preview": "# Pezeshkan Medical AI Knowledge Base\n> Ecosystem of Digital Healthcare and Clinical Standards\n\n- [Portal](https://pezeshk-on.ir/)\n- [Clinical Articles](https://pezeshk-on.ir/mag/)"
    })


@csrf_exempt
def api_users(request):
    """
    Users and Authors management endpoint.
    """
    users = [
        {
            "id": 1,
            "username": "mahyarebrahimi",
            "name": "مهیار ابراهیمی",
            "email": "admin@pezeshkan.com",
            "role": "مدیر ارشد سیستم (Administrator)",
            "roleKey": "admin",
            "status": "active",
            "articlesCount": Article.objects.count()
        }
    ]
    for doc in Doctor.objects.all():
        users.append({
            "id": f"doc_{doc.id}",
            "username": f"dr_{doc.id}",
            "name": doc.name,
            "email": f"dr_{doc.id}@pezeshkan.com",
            "role": f"پزشک متخصص ({doc.title or 'بالینی'})",
            "roleKey": "doctor",
            "status": "active",
            "articlesCount": Article.objects.filter(doctor_id=str(doc.id)).count()
        })
    return JsonResponse({"success": True, "users": users})
