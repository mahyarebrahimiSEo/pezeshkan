# -*- coding: utf-8 -*-
"""
=================================================================================
🌟 پیشخوان و استودیوی مدیریت محتوای جامع (Universal Portable CMS Engine)
نسخه: 2.0 - فول‌استک، مستقل، بدون نیاز به نصب هیچ پکیج جانبی (Zero-Dependency)
=================================================================================

ویژگی‌ها و قابلیت‌های کلیدی:
1. کاملاً مستقل و قابل حمل: فقط کافیست این تک‌فایل را در هر پروژه‌ای قرار دهید و اجرا کنید.
2. دارای ویرایشگر قدرتمند با استانداردهای وردپرس:
   - پاک‌سازی خودکار استایل‌ها و فونت‌های نامربوط (MS Word, Telegram, Web) هنگام Paste
   - خروجی تمیز، یکدست و هماهنگ با تایپوگرافی سایت
3. سیستم هوش سئو و تحلیل زنده (Real-Time Live SEO Audit) با نمره‌دهی 0 تا 100
4. کتابخانه رسانه و آپلود پیشرفته (Media Library & Drag-and-Drop Uploader)
5. سیستم دوگانه تم روز و شب (Light / Dark Mode)
6. مدیریت راهنماها و آموزش‌های پایگاه دانش (CRM & Documentation Hub)
7. پایداری داده‌ها: ذخیره‌سازی خودکار در فایل‌های JSON و سازگار با دیتابیس‌ها
8. سیستم پشتیبان‌گیری کامل (خروجی و درون‌ریزی JSON با یک کلیک)
9. بدون هیچ ایموجی در رابط کاربری (100% آیکن‌های وکتور SVG خالص)
10. سازگاری دوگانه: هم به صورت سرور لوکال کار می‌کند و هم خروجی HTML مستقل برای هاست‌های استاتیک می‌دهد.

دستورات اجرا:
- اجرای مستقیم و بالا آمدن پیشخوان:
    python universal_cms.py
- تغییر پورت یا نام سایت:
    python universal_cms.py --port 8080 --name "نام وبسایت من" --color "#0ea5e9"
- فقط استخراج فایل HTML مستقل بدون اجرای سرور:
    python universal_cms.py --export
=================================================================================
"""

import os
import sys
import json
import time
import re
import base64
import zlib
import mimetypes
import threading
import urllib.parse
import webbrowser
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

# 1. Output encoding & MIME configurations
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("font/woff", ".woff")
mimetypes.add_type("font/ttf", ".ttf")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/png", ".png")
mimetypes.add_type("image/jpeg", ".jpg")
mimetypes.add_type("image/gif", ".gif")
mimetypes.add_type("application/json", ".json")

# 2. Concurrency Lock
FILE_LOCK = threading.Lock()

def atomic_write_json(filepath, data):
    """ذخیره اتمیک و امن فایل‌های داده برای جلوگیری از تداخل و خرابی"""
    with FILE_LOCK:
        dir_name = os.path.dirname(filepath)
        os.makedirs(dir_name, exist_ok=True)
        tmp_path = filepath + f".tmp.{int(time.time()*1000)}"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, filepath)
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

def load_json(filepath, default=None):
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

# 3. Default Dataset Seeders
DEFAULT_CONFIG = {
    "site_name": "پیشخوان مدیریت محتوا",
    "site_tagline": "استودیوی تحریریه، مدیریت مقالات و هوش سئو",
    "brand_color": "#0ea5e9",
    "accent_color": "#10b981",
    "port": 8000,
    "host": "127.0.0.1"
}

DEFAULT_CATEGORIES = [
    {"id": 1, "name": "آموزش و مقالات تخصصی", "slug": "tutorials", "icon": "book-open"},
    {"id": 2, "name": "اخبار و رویدادها", "slug": "news", "icon": "newspaper"},
    {"id": 3, "name": "راهنما و مستندات سیستم", "slug": "docs", "icon": "file-text"},
    {"id": 4, "name": "فناوری و توسعه وب", "slug": "tech", "icon": "code"}
]

DEFAULT_AUTHORS = [
    {"id": "author-admin", "name": "مدیر سیستم", "title": "سردبیر و مدیر ارشد محتوا", "mcNumber": ""}
]

DEFAULT_ARTICLES = [
    {
        "id": "welcome-to-universal-cms",
        "title": "راهنمای کار با پیشخوان مدیریت محتوا و استودیوی هوشمند تحریریه",
        "slug": "guide-to-universal-cms-studio",
        "pillarId": 1,
        "pillarSlug": "tutorials",
        "categoryName": "آموزش و مقالات تخصصی",
        "categoryIcon": "book-open",
        "doctorId": "author-admin",
        "author": {
            "name": "مدیر سیستم",
            "title": "سردبیر و مدیر ارشد محتوا"
        },
        "status": "published",
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "lastModified": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": "پیشخوان مدیریت محتوا با قابلیت پاک‌سازی هوشمند متون کپی‌شده، تحلیل زنده سئو، کتابخانه رسانه و تم اختصاصی روز و شب آماده بهره‌برداری است.",
        "featuredImage": {
            "url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80",
            "alt": "میز کار و ابزارهای نویسندگی استودیوی محتوا"
        },
        "contentHtml": """
<h2>۱. خوش آمدید به استودیوی تحریریه و مدیریت محتوا</h2>
<p>این سامانه به عنوان یک پلتفرم مستقل، سریع و بدون نقص برای انتشار استاندارد مقالات و مستندات در تمامی وب‌سایت‌ها طراحی شده است. از ویژگی‌های بارز این پنل، حذف کامل وابستگی‌های سنگین و تمرکز بر سرعت و کیفیت محتواست.</p>

<h2>۲. پاک‌سازی هوشمند متن کپی‌شده (Universal Paste Sanitization)</h2>
<p>یکی از بزرگ‌ترین چالش‌های مدیران سایت، کپی کردن مطالب از نرم‌افزار <strong>Microsoft Word</strong>، کانال‌های تلگرام یا سایر وب‌سایت‌هاست که موجب ورود فونت‌ها، رنگ‌ها و اندازه‌های ناهمگون به صفحه می‌شود. در این استودیو، به هنگام فشردن کلیدهای Ctrl+V تمامی استایل‌های مخرب حذف شده و متن به صورت پاک، استاندارد و هماهنگ با تایپوگرافی سایت نمایش داده می‌شود.</p>

<blockquote>«تایپوگرافی یکدست و تمیز، اعتماد کاربر به محتوای شما را تا ۴ برابر افزایش می‌دهد.»</blockquote>

<h2>۳. هوش سئو و ارزیابی بلادرنگ (Live SEO Engine)</h2>
<p>در حین نگارش مقاله، سیستم به طور خودکار فاکتورهای کلیدی سئو را بررسی می‌کند:</p>
<ul>
  <li>طول عنوان مقاله و ساختار بهینه برای موتورهای جستجو</li>
  <li>فرمت استاندارد پیوند یکتا (Slug)</li>
  <li>چگالی کلمه کلیدی هدف در بدنه و تیترها</li>
  <li>وجود تیترهای سطح دوم (H2) و پاراگراف‌بندی خوانا</li>
  <li>تخمین دقیق زمان مطالعه بر اساس تعداد واژگان</li>
</ul>

<h2>۴. امکانات رسانه‌ای و پشتیبان‌گیری</h2>
<p>شما می‌توانید تصاویر خود را با کشیدن و رها کردن در بخش کتابخانه رسانه بارگذاری کنید. همچنین با استفاده از دکمه «پشتیبان (JSON)» در نوار بالایی، در هر لحظه یک خروجی کامل از تمام مقالات و پایگاه داده خود به صورت آفلاین دریافت فرمایید.</p>
""",
        "seo": {
            "focusKeyword": "مدیریت محتوا",
            "metaTitle": "راهنمای کار با پیشخوان مدیریت محتوا و سئو",
            "metaDescription": "آموزش گام به گام امکانات استودیوی مدیریت محتوا شامل پاک‌سازی متن، هوش سئو، کتابخانه تصاویر و پشتیبان‌گیری.",
            "canonicalUrl": "",
            "readingTimeMinutes": 3
        }
    }
]

DEFAULT_CRM_TUTORIALS = [
    {
        "id": "crm-content-workflow",
        "title": "فرآیند تولید، بازبینی و انتشار محتوا در استودیو",
        "category": "تحریریه و نویسندگان",
        "role": "author",
        "duration": "۵ دقیقه",
        "views": "۳۵۰",
        "level": "مقدماتی",
        "summary": "راهنمای جامع مراحل نگارش مقاله، تنظیم پیوند یکتا، بررسی چک‌لیست سئو و دریافت تأییدیه انتشار.",
        "html": "<h3>مراحل ایجاد مقاله استاندارد</h3><p>۱. عنوان واضح و جذاب انتخاب کنید.<br>۲. کلمه کلیدی اصلی را در بخش سئو مشخص نمایید.<br>۳. متن را تایپ یا جای‌گذاری کنید؛ سیستم فونت و رنگ را استاندارد می‌کند.<br>۴. دکمه انتشار یا ذخیره پیش‌نویس را بزنید.</p>"
    },
    {
        "id": "crm-media-guidelines",
        "title": "استانداردسازی تصاویر، سایزها و متن جایگزین (Alt)",
        "category": "مدیریت رسانه",
        "role": "admin",
        "duration": "۴ دقیقه",
        "views": "۲۴۰",
        "level": "مهم",
        "summary": "نکات کلیدی برای کاهش حجم تصاویر، افزایش سرعت لود سایت و بهینه‌سازی تگ‌های سئو تصاویر.",
        "html": "<h3>نکات کلیدی تصاویر</h3><p>برای دریافت بالاترین رتبه در گوگل، همیشه متن Alt را متناسب با موضوع تصویر تکمیل فرمایید و از تصاویر با نسبت استاندارد ۱۶:۹ استفاده کنید.</p>"
    }
]

DEFAULT_SETTINGS = {
    "siteTitle": "پیشخوان مدیریت محتوا",
    "titleTemplate": "%title% | پیشخوان مدیریت",
    "defaultMetaDesc": "سامانه مدیریت محتوای هوشمند با نگارش استاندارد و ارزیابی سئوی بلادرنگ.",
    "defaultKeywords": "آموزش, مقالات, سئو, تولید محتوا",
    "robotsIndex": True,
    "robotsFollow": True
}

# 4. Embedded Compressed HTML Template (Standard Base64 ZLib)
EMBEDDED_TEMPLATE_B64 = "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"

def get_base_html():
    raw_bytes = zlib.decompress(base64.b64decode(EMBEDDED_TEMPLATE_B64))
    return raw_bytes.decode('utf-8')

# 5. Core Environment & Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "cms_data")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

CONFIG_PATH = os.path.join(DATA_DIR, "config.json")
ARTICLES_PATH = os.path.join(DATA_DIR, "articles.json")
CATEGORIES_PATH = os.path.join(DATA_DIR, "categories.json")
AUTHORS_PATH = os.path.join(DATA_DIR, "authors.json")
MEDIA_PATH = os.path.join(DATA_DIR, "media.json")
CRM_PATH = os.path.join(DATA_DIR, "crm_tutorials.json")
SETTINGS_PATH = os.path.join(DATA_DIR, "settings.json")

def init_workspace(custom_name=None, custom_color=None):
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)

    config = load_json(CONFIG_PATH, DEFAULT_CONFIG)
    if custom_name:
        config["site_name"] = custom_name
    if custom_color:
        config["brand_color"] = custom_color
    atomic_write_json(CONFIG_PATH, config)

    if not os.path.exists(ARTICLES_PATH):
        atomic_write_json(ARTICLES_PATH, DEFAULT_ARTICLES)
    if not os.path.exists(CATEGORIES_PATH):
        atomic_write_json(CATEGORIES_PATH, DEFAULT_CATEGORIES)
    if not os.path.exists(AUTHORS_PATH):
        atomic_write_json(AUTHORS_PATH, DEFAULT_AUTHORS)
    if not os.path.exists(MEDIA_PATH):
        atomic_write_json(MEDIA_PATH, [])
    if not os.path.exists(CRM_PATH):
        atomic_write_json(CRM_PATH, DEFAULT_CRM_TUTORIALS)
    if not os.path.exists(SETTINGS_PATH):
        atomic_write_json(SETTINGS_PATH, DEFAULT_SETTINGS)
    return config

def render_admin_html(config=None):
    if not config:
        config = load_json(CONFIG_PATH, DEFAULT_CONFIG)

    articles = load_json(ARTICLES_PATH, DEFAULT_ARTICLES)
    categories = load_json(CATEGORIES_PATH, DEFAULT_CATEGORIES)
    authors = load_json(AUTHORS_PATH, DEFAULT_AUTHORS)
    media = load_json(MEDIA_PATH, [])
    crm = load_json(CRM_PATH, DEFAULT_CRM_TUTORIALS)
    settings = load_json(SETTINGS_PATH, DEFAULT_SETTINGS)

    html = get_base_html()
    html = html.replace("__SITE_NAME__", config.get("site_name", "پیشخوان مدیریت محتوا"))
    html = html.replace("__SITE_TAGLINE__", config.get("site_tagline", "استودیوی تحریریه، مدیریت مقالات و سئو"))
    html = html.replace("__BRAND_COLOR__", config.get("brand_color", "#0ea5e9"))

    html = html.replace("__ARTICLES_JSON__", json.dumps(articles, ensure_ascii=False))
    html = html.replace("__CATEGORIES_JSON__", json.dumps(categories, ensure_ascii=False))
    html = html.replace("__AUTHORS_JSON__", json.dumps(authors, ensure_ascii=False))
    html = html.replace("__SETTINGS_JSON__", json.dumps(settings, ensure_ascii=False))
    html = html.replace("__MEDIA_JSON__", json.dumps(media, ensure_ascii=False))
    html = html.replace("__CRM_JSON__", json.dumps(crm, ensure_ascii=False))
    return html

# 6. Hardened HTTP Request Handler
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class UniversalCMSHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def read_json_body(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                return {}
            body = self.rfile.read(length).decode('utf-8')
            return json.loads(body)
        except Exception:
            return {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Serve Admin Studio
        if path in ("/", "/admin", "/admin/", "/admin.html"):
            html = render_admin_html().encode('utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return

        # Serve Uploaded Assets
        if path.startswith("/uploads/"):
            filename = os.path.basename(path)
            file_path = os.path.join(UPLOADS_DIR, filename)
            if os.path.isfile(file_path):
                mime, _ = mimetypes.guess_type(file_path)
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime or "application/octet-stream")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            self.send_error(404, "File Not Found")
            return

        # REST API: Articles
        if path == "/api/articles":
            return self.send_json(load_json(ARTICLES_PATH, []))

        # REST API: Categories
        if path == "/api/categories":
            return self.send_json(load_json(CATEGORIES_PATH, []))

        # REST API: Authors
        if path == "/api/authors":
            return self.send_json(load_json(AUTHORS_PATH, []))

        # REST API: Media
        if path == "/api/media":
            return self.send_json({"success": True, "media": load_json(MEDIA_PATH, [])})

        # REST API: CRM Tutorials
        if path in ("/api/crm-tutorials", "/api/crm-tutorials/"):
            return self.send_json(load_json(CRM_PATH, []))

        # REST API: Settings
        if path == "/api/settings":
            return self.send_json(load_json(SETTINGS_PATH, DEFAULT_SETTINGS))

        # REST API: Full Backup Export
        if path == "/api/export":
            backup = {
                "exportedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "articles": load_json(ARTICLES_PATH, []),
                "categories": load_json(CATEGORIES_PATH, []),
                "authors": load_json(AUTHORS_PATH, []),
                "media": load_json(MEDIA_PATH, []),
                "crmTutorials": load_json(CRM_PATH, []),
                "settings": load_json(SETTINGS_PATH, DEFAULT_SETTINGS)
            }
            return self.send_json(backup)

        self.send_error(404, "Endpoint Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        data = self.read_json_body()

        # Create Article
        if path == "/api/articles":
            articles = load_json(ARTICLES_PATH, [])
            art_id = data.get("id") or f"art-{int(time.time()*1000)}"
            data["id"] = art_id
            data["createdAt"] = data.get("createdAt") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            data["lastModified"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            # Upsert
            idx = next((i for i, a in enumerate(articles) if a.get("id") == art_id), None)
            if idx is not None:
                articles[idx] = data
            else:
                articles.insert(0, data)
            atomic_write_json(ARTICLES_PATH, articles)
            return self.send_json({"success": True, "articles": articles})

        # Upload Media (Base64)
        if path == "/api/upload":
            filename = data.get("filename", "image.webp")
            b64_data = data.get("data", "")
            alt_text = data.get("alt", "")

            if "," in b64_data:
                b64_data = b64_data.split(",", 1)[1]

            try:
                raw_bytes = base64.b64decode(b64_data)
            except Exception:
                return self.send_json({"error": "فرمت داده تصویر نامعتبر است"}, 400)

            clean_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '', filename) or f"img_{int(time.time())}.webp"
            unique_name = f"{int(time.time())}_{clean_name}"
            file_path = os.path.join(UPLOADS_DIR, unique_name)

            with open(file_path, "wb") as f:
                f.write(raw_bytes)

            url = f"/uploads/{unique_name}"
            media_item = {
                "id": f"med-{int(time.time()*1000)}",
                "filename": unique_name,
                "url": url,
                "alt": alt_text or clean_name,
                "size": len(raw_bytes),
                "uploadedAt": time.strftime("%Y-%m-%d %H:%M", time.localtime())
            }

            media = load_json(MEDIA_PATH, [])
            media.insert(0, media_item)
            atomic_write_json(MEDIA_PATH, media)
            return self.send_json({"success": True, "url": url, "media": media_item})

        # Create/Update CRM Tutorial
        if path in ("/api/crm-tutorials", "/api/crm-tutorials/"):
            crm = load_json(CRM_PATH, [])
            tut_id = data.get("id") or f"crm-{int(time.time()*1000)}"
            data["id"] = tut_id
            data["lastModified"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            idx = next((i for i, t in enumerate(crm) if t.get("id") == tut_id), None)
            if idx is not None:
                crm[idx] = data
            else:
                crm.insert(0, data)
            atomic_write_json(CRM_PATH, crm)
            return self.send_json({"success": True, "tutorials": crm})

        # Restore from Full Backup
        if path == "/api/import":
            if data.get("articles"):
                atomic_write_json(ARTICLES_PATH, data["articles"])
            if data.get("categories"):
                atomic_write_json(CATEGORIES_PATH, data["categories"])
            if data.get("authors"):
                atomic_write_json(AUTHORS_PATH, data["authors"])
            if data.get("media"):
                atomic_write_json(MEDIA_PATH, data["media"])
            if data.get("crmTutorials"):
                atomic_write_json(CRM_PATH, data["crmTutorials"])
            if data.get("settings"):
                atomic_write_json(SETTINGS_PATH, data["settings"])
            return self.send_json({"success": True, "message": "پایگاه داده با موفقیت بازیابی شد"})

        self.send_error(404, "Endpoint Not Found")

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        data = self.read_json_body()

        if path == "/api/articles":
            articles = load_json(ARTICLES_PATH, [])
            art_id = data.get("id")
            if not art_id:
                return self.send_json({"error": "شناسه مقاله الزامی است"}, 400)
            data["lastModified"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            idx = next((i for i, a in enumerate(articles) if a.get("id") == art_id), None)
            if idx is not None:
                articles[idx] = data
            else:
                articles.insert(0, data)
            atomic_write_json(ARTICLES_PATH, articles)
            return self.send_json({"success": True, "articles": articles})

        if path == "/api/settings":
            atomic_write_json(SETTINGS_PATH, data)
            return self.send_json({"success": True, "settings": data})

        if path in ("/api/crm-tutorials", "/api/crm-tutorials/"):
            crm = load_json(CRM_PATH, [])
            tut_id = data.get("id")
            if not tut_id:
                return self.send_json({"error": "شناسه آموزش الزامی است"}, 400)
            idx = next((i for i, t in enumerate(crm) if t.get("id") == tut_id), None)
            if idx is not None:
                crm[idx] = data
            else:
                crm.insert(0, data)
            atomic_write_json(CRM_PATH, crm)
            return self.send_json({"success": True, "tutorials": crm})

        self.send_error(404, "Endpoint Not Found")

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        item_id = query.get("id", [None])[0]

        if not item_id:
            body = self.read_json_body()
            item_id = body.get("id")

        if path == "/api/articles":
            articles = load_json(ARTICLES_PATH, [])
            articles = [a for a in articles if str(a.get("id")) != str(item_id)]
            atomic_write_json(ARTICLES_PATH, articles)
            return self.send_json({"success": True, "articles": articles})

        if path == "/api/media":
            media = load_json(MEDIA_PATH, [])
            found = next((m for m in media if str(m.get("id")) == str(item_id)), None)
            if found and found.get("filename"):
                file_path = os.path.join(UPLOADS_DIR, found["filename"])
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
            media = [m for m in media if str(m.get("id")) != str(item_id)]
            atomic_write_json(MEDIA_PATH, media)
            return self.send_json({"success": True, "media": media})

        if path in ("/api/crm-tutorials", "/api/crm-tutorials/"):
            crm = load_json(CRM_PATH, [])
            crm = [t for t in crm if str(t.get("id")) != str(item_id)]
            atomic_write_json(CRM_PATH, crm)
            return self.send_json({"success": True, "tutorials": crm})

        self.send_error(404, "Endpoint Not Found")

    def log_message(self, format, *args):
        # Clean terminal logging
        sys.stderr.write(f"[%s] %s\n" % (self.log_date_time_string(), format % args))

# 7. Main Entry Point
def main():
    parser = argparse.ArgumentParser(description="Universal Portable CMS Engine")
    parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host IP (default: 127.0.0.1)")
    parser.add_argument("--name", type=str, default=None, help="Custom site title")
    parser.add_argument("--color", type=str, default=None, help="Custom brand accent color (e.g. #0ea5e9)")
    parser.add_argument("--export", action="store_true", help="Export standalone admin.html and exit")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    args = parser.parse_args()

    config = init_workspace(custom_name=args.name, custom_color=args.color)
    port = args.port or config.get("port", 8000)
    host = args.host or config.get("host", "127.0.0.1")

    # Generate or export admin.html
    rendered_html = render_admin_html(config)
    admin_file_path = os.path.join(BASE_DIR, "admin.html")
    with open(admin_file_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    if args.export:
        print(f"\n[✔] فایل پنل مدیریت مستقل با موفقیت ایجاد شد: {admin_file_path}")
        print(f"می‌توانید این فایل را در هر هاست، سرور یا به صورت محلی در مرورگر باز کنید.")
        return

    admin_url = f"http://{host}:{port}/admin"

    banner = f"""
======================================================================
  استودیوی تحریریه و پیشخوان مدیریت محتوا (Universal CMS Engine)
======================================================================
  وبسایت:      {config.get('site_name')}
  آدرس پنل:     {admin_url}
  پوشه داده‌ها:  {DATA_DIR}
  پوشه رسانه‌ها: {UPLOADS_DIR}
  فایل خروجی:   {admin_file_path}
======================================================================
  برای توقف سرور کلیدهای Ctrl + C را فشار دهید.
"""
    print(banner)

    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(admin_url)).start()

    server = ThreadedHTTPServer((host, port), UniversalCMSHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nدر حال خاموش‌سازی سرور پیشخوان...")
        server.server_close()
        print("سرور با موفقیت متوقف شد.")

if __name__ == "__main__":
    main()
