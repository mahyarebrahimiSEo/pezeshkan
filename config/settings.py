# -*- coding: utf-8 -*-
"""
Django Settings for Pezeshkan Medical Ecosystem
Production-Grade Enterprise Clinical Architecture
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Load .env file if present
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    try:
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception as e:
        print(f"[Warning] Could not load .env: {e}")

# 2. Security & Environment
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development").lower()
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-pezeshkan-2026-medical-hardened-key-99x")
DEBUG = os.environ.get("DEBUG", "").lower() in ("true", "1") or ENVIRONMENT != "production"

ALLOWED_HOSTS_RAW = os.environ.get("ALLOWED_HOSTS", "*")
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS_RAW.split(",") if h.strip()]
if "*" not in ALLOWED_HOSTS and DEBUG:
    ALLOWED_HOSTS.extend(["localhost", "127.0.0.1", "0.0.0.0"])

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "mahyarebrahimi")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "mahyebi86")
APPOINTMENT_SYSTEM_URL = os.environ.get("APPOINTMENT_SYSTEM_URL", "").strip().rstrip("/")

# 3. Application Definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'apps.pezeshkan_core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'apps.pezeshkan_core.middleware.RedirectAndSecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR,
            BASE_DIR / 'mag',
            BASE_DIR / 'portal',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# 4. Database Configuration: PostgreSQL with seamless fallback to SQLite3
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
DATABASE_URL = os.environ.get("DATABASE_URL", "")

if DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://"):
    import urllib.parse
    parsed = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path.lstrip('/'),
            'USER': parsed.username,
            'PASSWORD': parsed.password or '',
            'HOST': parsed.hostname or 'localhost',
            'PORT': parsed.port or 5432,
            'CONN_MAX_AGE': 600,
        }
    }
elif POSTGRES_DB and POSTGRES_USER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': POSTGRES_DB,
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': POSTGRES_HOST,
            'PORT': POSTGRES_PORT,
            'CONN_MAX_AGE': 600,
        }
    }
else:
    # Zero-config high-performance SQLite fallback
    DATA_DIR = BASE_DIR / 'data'
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DATA_DIR / 'pezeshkan.sqlite3',
            'OPTIONS': {
                'timeout': 30,
            },
        }
    }

# 4.1. High-Performance In-Memory Cache for Concurrency
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'pezeshkan-high-concurrency-cache',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
            'CULL_FREQUENCY': 3,
        }
    }
}

# 5. Password Hashing (Argon2id + PBKDF2)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# 6. Internationalization
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# 7. Static and Media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'assets',
    BASE_DIR / 'fonts',
]

MEDIA_URL = '/uploads/'
MEDIA_ROOT = BASE_DIR / 'mag' / 'uploads'
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 8. CORS & CSRF
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
DATA_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024  # 25 MB max payload for clinical media
FILE_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024
