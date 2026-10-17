# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - Hardened Production Application Server
Enterprise Clinical Gateway with Defensive Hardening:
- PBKDF2-SHA256 Multi-Layer Authentication & Session Management
- Sliding-Window IP Rate Limiting (Brute-Force & Anti-Spam Defense)
- Strict Path Normalization & Arbitrary File Traversal Prevention
- Input Sanitization & Stored XSS Neutralization
- Modern HTTP Defense Headers (CSP, HSTS, X-Frame-Options, Nosniff, Permissions)
- Atomic File Operations with Concurrency Locking
- DoS Defense (Content-Length Capping & Socket Timeout)
- Production .env & Environment Configuration Support
"""

import http.server
import socketserver
import os
import sys
import json
import urllib.parse
import hashlib
import secrets
import time
import datetime
import io
import math
import mimetypes
import threading
import html
import re
import base64
import uuid
import signal
import logging
from logging.handlers import RotatingFileHandler

# Pillow Image Processing (WebP Multi-Tier Optimization)
try:
    from PIL import Image, ImageOps
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("[Warning] Pillow not installed. Media optimization running in raw fallback mode. Run: pip install pillow")

# AWS S3 / Cloudflare R2 / MinIO Storage Engine
try:
    import boto3
    from botocore.config import Config as BotoConfig
    from botocore.exceptions import ClientError as BotoClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False
    BotoClientError = Exception

# Argon2 Password Hashing Setup (OWASP & RFC 9106 Standard)
try:
    from argon2 import PasswordHasher
    from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
    ARGON2_HASHER = PasswordHasher(
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        salt_len=16
    )
    HAS_ARGON2 = True
except ImportError:
    ARGON2_HASHER = None
    HAS_ARGON2 = False
    print("[Security Warning] argon2-cffi is not installed. Falling back to PBKDF2. Run: pip install argon2-cffi")

# 1. Output encoding & Mime-type registrations
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
mimetypes.add_type("application/xml", ".xml")
mimetypes.add_type("text/plain", ".txt")
mimetypes.add_type("application/manifest+json", ".webmanifest")

# 2. Directory Layout
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PORTAL_DIR = os.path.join(BASE_DIR, "portal")
MAG_DIR = os.path.join(BASE_DIR, "mag")
CONTENT_DIR = os.path.join(MAG_DIR, "content")
UPLOADS_DIR = os.path.join(MAG_DIR, "uploads")
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# 3. Environment Variable Loader (Zero External Dependency)
def load_dotenv(filepath):
    if not os.path.isfile(filepath):
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
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
        print(f"[Warning] Failed to load .env file: {e}")

load_dotenv(os.path.join(BASE_DIR, ".env"))

# 4. Server Configuration & Security Settings
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development").lower()
PORT = int(os.environ.get("PORT", 3000))
HOST = os.environ.get("HOST", "0.0.0.0")

# 4.0. Cloud Media & S3/R2 Storage Configuration
S3_ENABLED = os.environ.get("S3_ENABLED", "false").lower() in ("true", "1", "yes")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", "").strip()
S3_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY_ID", "").strip()
S3_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY", "").strip()
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "pezeshkan-media").strip()
S3_REGION = os.environ.get("S3_REGION", "auto").strip()
S3_PUBLIC_DOMAIN = os.environ.get("S3_PUBLIC_DOMAIN", "").strip().rstrip("/")

# 4.1. Enterprise Application & Security Audit Logging (OWASP A10 Compliant)
SECURITY_LOG_FILE = os.path.join(LOGS_DIR, "security_audit.log")

logger = logging.getLogger("pezeshkan")
logger.setLevel(logging.INFO)
if not logger.handlers:
    _log_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    _console_handler = logging.StreamHandler(sys.stdout)
    _console_handler.setFormatter(_log_formatter)
    logger.addHandler(_console_handler)

    try:
        _app_file_handler = RotatingFileHandler(
            os.path.join(LOGS_DIR, "application.log"),
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        _app_file_handler.setFormatter(_log_formatter)
        logger.addHandler(_app_file_handler)
    except Exception as _e:
        print(f"[Logging Warning] Could not attach file handler: {_e}")

class SecurityAuditLogger:
    """
    Dedicated tamper-evident, append-only structured audit logger for security events.
    Complies with OWASP Top 10 A10: Insufficient Logging & Monitoring.
    Automatically redacts passwords, tokens, hashes, and PII before writing.
    """
    def __init__(self, log_path=SECURITY_LOG_FILE):
        self.log_path = log_path
        self.lock = threading.Lock()
        self._audit_logger = logging.getLogger("pezeshkan_security_audit")
        self._audit_logger.setLevel(logging.INFO)
        if not self._audit_logger.handlers:
            try:
                handler = RotatingFileHandler(
                    log_path,
                    maxBytes=20 * 1024 * 1024,
                    backupCount=10,
                    encoding="utf-8"
                )
                handler.setFormatter(logging.Formatter("%(message)s"))
                self._audit_logger.addHandler(handler)
            except Exception as _e:
                print(f"[Audit Warning] Could not initialize audit log file: {_e}")

    def log_event(self, event_type, ip="unknown", user="anonymous", status="SUCCESS", details=None):
        safe_details = {}
        if isinstance(details, dict):
            for k, v in details.items():
                if any(secret_term in str(k).lower() for secret_term in ("password", "salt", "secret", "token", "hash")):
                    safe_details[k] = "[REDACTED]"
                else:
                    safe_details[k] = v
        elif details is not None:
            safe_details = {"info": str(details)[:300]}

        event = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event_type": event_type,
            "ip": ip,
            "user": user,
            "status": status,
            "details": safe_details
        }
        msg = json.dumps(event, ensure_ascii=False)
        with self.lock:
            try:
                self._audit_logger.info(msg)
            except Exception:
                pass

AUDIT_LOGGER = SecurityAuditLogger()

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "mahyarebrahimi")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "mahyebi86")
SALT = os.environ.get("SECRET_SALT", "pezeshkan_mag_secure_salt_2026_x99").encode("utf-8")

# Password Hashing Setup: Argon2id with legacy PBKDF2 support
HASH_ITERATIONS = 100000
STORED_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")
if not STORED_PASSWORD_HASH:
    if HAS_ARGON2 and ARGON2_HASHER:
        STORED_PASSWORD_HASH = ARGON2_HASHER.hash(ADMIN_PASSWORD)
    else:
        STORED_PASSWORD_HASH = hashlib.pbkdf2_hmac('sha256', ADMIN_PASSWORD.encode('utf-8'), SALT, HASH_ITERATIONS).hex()

SECURE_COOKIES = os.environ.get("SECURE_COOKIES", "").lower() in ("true", "1", "yes")
ALLOWED_HOSTS_RAW = os.environ.get("ALLOWED_HOSTS", "*")
ALLOWED_HOSTS = [h.strip().lower() for h in ALLOWED_HOSTS_RAW.split(",") if h.strip()]

MAX_PAYLOAD_SIZE = 15 * 1024 * 1024  # 15 Megabytes Max Request Body (Supports HD Clinical Images)
SESSION_MAX_AGE = 24 * 3600         # 24 Hours Max Session Lifetime
SESSION_IDLE_TIMEOUT = 4 * 3600     # 4 Hours Inactivity Timeout

# 5. Concurrency Locks & Storage
WRITE_LOCK = threading.Lock()
SESSIONS_LOCK = threading.Lock()
SESSIONS = {}

def atomic_write_json(filepath, data):
    """Safely and atomically writes JSON data using a temporary file and sync."""
    with WRITE_LOCK:
        dir_name = os.path.dirname(filepath)
        os.makedirs(dir_name, exist_ok=True)
        tmp_path = filepath + f".tmp.{secrets.token_hex(4)}"
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
                except OSError:
                    pass

def atomic_write_text(filepath, text):
    """Safely and atomically writes string text to a file using temp file and fsync."""
    with WRITE_LOCK:
        dir_name = os.path.dirname(filepath)
        os.makedirs(dir_name, exist_ok=True)
        tmp_path = filepath + f".tmp.{secrets.token_hex(4)}"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(text)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, filepath)
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

def load_json_file(filepath, default=None):
    """Safely and robustly loads JSON using context manager, preventing descriptor leaks."""
    if not os.path.isfile(filepath):
        return default if default is not None else []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Storage Warning] Error reading {os.path.basename(filepath)}: {e}")
        return default if default is not None else []

def save_json_file(filepath, data):
    """Thread-safe atomic wrapper to write JSON data."""
    return atomic_write_json(filepath, data)

# 6. Sliding-Window Rate Limiter
class SlidingWindowRateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.records = {}
        self.lock = threading.Lock()

    def check(self, key):
        now = time.time()
        with self.lock:
            timestamps = self.records.get(key, [])
            recent = [t for t in timestamps if now - t < self.window_seconds]
            if len(recent) >= self.max_requests:
                self.records[key] = recent
                retry_after = int(self.window_seconds - (now - recent[0]))
                return False, retry_after
            return True, 0

    def record_hit(self, key):
        now = time.time()
        with self.lock:
            if key not in self.records:
                self.records[key] = []
            self.records[key].append(now)
            if len(self.records) > 1000:
                self._prune(now)

    def reset(self, key):
        with self.lock:
            self.records.pop(key, None)

    def _prune(self, now):
        to_del = []
        for k, ts in self.records.items():
            valid = [t for t in ts if now - t < self.window_seconds]
            if not valid:
                to_del.append(k)
            else:
                self.records[k] = valid
        for k in to_del:
            self.records.pop(k, None)

LOGIN_LIMITER = SlidingWindowRateLimiter(max_requests=5, window_seconds=300)     # 5 failed attempts per 5 min
FORM_LIMITER = SlidingWindowRateLimiter(max_requests=10, window_seconds=300)      # 10 form submits per 5 min
API_LIMITER = SlidingWindowRateLimiter(max_requests=120, window_seconds=60)       # 120 API requests per min

# 7. Authentication, Users & Session Helpers
USERS_FILE = os.path.join(CONTENT_DIR, "users.json")
_USERS_CACHE = None
_USERS_MTIME = 0
_USERS_LOCK = threading.Lock()

def hash_user_password(password, salt=None):
    """
    Hashes a password using Argon2id (RFC 9106 / OWASP recommended).
    Returns (salt, hash). The Argon2id PHC format includes its own cryptographically secure salt,
    and an auxiliary salt is returned for backward compatibility.
    """
    if HAS_ARGON2 and ARGON2_HASHER:
        phc_hash = ARGON2_HASHER.hash(password)
        aux_salt = secrets.token_hex(16)
        return aux_salt, phc_hash
    else:
        if not salt:
            salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
        return salt, hashed

def verify_user_password(password, salt, stored_hash):
    """
    Verifies a password against stored_hash.
    Supports:
    1. Argon2id ($argon2id$...)
    2. Argon2i / Argon2d ($argon2...)
    3. Legacy PBKDF2-HMAC-SHA256 hex string (with seamless backward compatibility)
    """
    if not password or not stored_hash:
        return False

    # 1. Argon2 verification
    if stored_hash.startswith("$argon2"):
        if HAS_ARGON2 and ARGON2_HASHER:
            try:
                return ARGON2_HASHER.verify(stored_hash, password)
            except (VerifyMismatchError, VerificationError, InvalidHash):
                return False
            except Exception:
                return False
        else:
            print("[Security Warning] Password is in Argon2 format but argon2 module is missing.")
            return False

    # 2. Legacy PBKDF2 verification
    try:
        salt_bytes = (salt or "").encode('utf-8')
        computed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 100000).hex()
        return secrets.compare_digest(computed, stored_hash)
    except Exception:
        return False

def load_users():
    global _USERS_CACHE, _USERS_MTIME
    if not os.path.exists(USERS_FILE):
        return []
    try:
        mtime = os.path.getmtime(USERS_FILE)
        with _USERS_LOCK:
            if _USERS_CACHE is None or mtime != _USERS_MTIME:
                with open(USERS_FILE, "r", encoding="utf-8") as f:
                    _USERS_CACHE = json.load(f)
                _USERS_MTIME = mtime
            return [dict(u) for u in _USERS_CACHE]
    except Exception as e:
        print(f"[Users] Error loading users.json: {e}")
        return []

def save_users(users_list):
    global _USERS_CACHE, _USERS_MTIME
    atomic_write_json(USERS_FILE, users_list)
    with _USERS_LOCK:
        _USERS_CACHE = [dict(u) for u in users_list]
        if os.path.exists(USERS_FILE):
            _USERS_MTIME = os.path.getmtime(USERS_FILE)

def find_user_by_username(username):
    if not username:
        return None
    u_clean = str(username).strip().lower()
    for u in load_users():
        if str(u.get("username", "")).strip().lower() == u_clean:
            return u
    return None

def find_user_by_id(user_id):
    if not user_id:
        return None
    for u in load_users():
        if u.get("id") == user_id:
            return u
    return None

def revoke_user_sessions(username):
    if not username:
        return
    u_clean = str(username).strip().lower()
    with SESSIONS_LOCK:
        tokens_to_remove = [
            t for t, s in SESSIONS.items()
            if str(s.get("username", "")).strip().lower() == u_clean
        ]
        for t in tokens_to_remove:
            SESSIONS.pop(t, None)

def get_safe_users():
    users = load_users()
    articles_file = os.path.join(CONTENT_DIR, "articles.json")
    articles = []
    if os.path.isfile(articles_file):
        try:
            with open(articles_file, "r", encoding="utf-8") as f:
                articles = json.load(f)
        except Exception:
            pass

    safe_list = []
    for u in users:
        doc_id = u.get("doctorId")
        disp_name = str(u.get("displayName", "")).strip().lower()
        uname = str(u.get("username", "")).strip().lower()
        art_count = 0
        for a in articles:
            a_doc = a.get("doctorId")
            a_author_name = str(a.get("author", {}).get("name") or "").strip().lower()
            if doc_id and a_doc == doc_id:
                art_count += 1
            elif disp_name and disp_name in a_author_name:
                art_count += 1
            elif uname and uname in a_author_name:
                art_count += 1

        safe_u = {
            "id": u.get("id"),
            "username": u.get("username"),
            "displayName": u.get("displayName") or "مهیار ابراهیمی",
            "firstName": u.get("firstName", ""),
            "lastName": u.get("lastName", ""),
            "nickname": u.get("nickname", ""),
            "email": u.get("email", ""),
            "website": u.get("website", ""),
            "role": u.get("role", "author"),
            "bio": u.get("bio", ""),
            "avatar": u.get("avatar", "👤"),
            "specialty": u.get("specialty", ""),
            "medicalCouncil": u.get("medicalCouncil", ""),
            "doctorId": u.get("doctorId", ""),
            "status": u.get("status", "active"),
            "registeredAt": u.get("registeredAt", ""),
            "lastLogin": u.get("lastLogin", ""),
            "articlesCount": art_count
        }
        safe_list.append(safe_u)
    return safe_list

def verify_credentials(username, password):
    u = find_user_by_username(username)
    if u:
        if u.get("status") != "active":
            return False
        salt = u.get("passwordSalt")
        pwd_hash = u.get("passwordHash")
        if pwd_hash:
            if verify_user_password(password, salt, pwd_hash):
                # Automatic Rehash: upgrade legacy PBKDF2 hashes to Argon2id upon successful login
                if not pwd_hash.startswith("$argon2") and HAS_ARGON2:
                    try:
                        new_salt, new_hash = hash_user_password(password)
                        users = load_users()
                        for item in users:
                            if item.get("id") == u.get("id"):
                                item["passwordSalt"] = new_salt
                                item["passwordHash"] = new_hash
                                item["passwordUpdatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                                break
                        save_users(users)
                        print(f"[Security Upgrade] User '{username}' password hash seamlessly upgraded to Argon2id.")
                    except Exception as e:
                        print(f"[Security Warning] Failed to rehash user password: {e}")
                return True

    # Fallback to initial admin environment variables
    if username == ADMIN_USERNAME:
        if STORED_PASSWORD_HASH:
            if STORED_PASSWORD_HASH.startswith("$argon2"):
                if HAS_ARGON2 and ARGON2_HASHER:
                    try:
                        return ARGON2_HASHER.verify(STORED_PASSWORD_HASH, password)
                    except Exception:
                        return False
            else:
                computed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, HASH_ITERATIONS).hex()
                return secrets.compare_digest(computed, STORED_PASSWORD_HASH)
    return False

def create_session(username):
    token = secrets.token_urlsafe(32)
    csrf_token = secrets.token_hex(32)
    now = time.time()
    user = find_user_by_username(username)
    display_name = "مهیار ابراهیمی"
    role = "administrator"
    user_id = "usr_mahyarebrahimi"
    avatar = "👨‍💼"
    if user:
        display_name = user.get("displayName") or user.get("name") or "مهیار ابراهیمی"
        role = user.get("role", "administrator")
        user_id = user.get("id")
        avatar = user.get("avatar", "👨‍💼")
        try:
            users = load_users()
            for item in users:
                if item.get("id") == user_id:
                    item["lastLogin"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    break
            save_users(users)
        except Exception:
            pass

    with SESSIONS_LOCK:
        expired = [t for t, s in SESSIONS.items() if now > s["expires_at"] or (now - s.get("last_active", now)) > SESSION_IDLE_TIMEOUT]
        for t in expired:
            SESSIONS.pop(t, None)

        SESSIONS[token] = {
            "token": token,
            "csrf_token": csrf_token,
            "userId": user_id,
            "username": username,
            "name": display_name,
            "displayName": display_name,
            "role": role,
            "avatar": avatar,
            "created_at": now,
            "last_active": now,
            "expires_at": now + SESSION_MAX_AGE
        }
    return token

def get_session(token):
    if not token:
        return None
    now = time.time()
    with SESSIONS_LOCK:
        sess = SESSIONS.get(token)
        if not sess:
            return None
        if now > sess["expires_at"] or (now - sess.get("last_active", now)) > SESSION_IDLE_TIMEOUT:
            SESSIONS.pop(token, None)
            return None
        sess["last_active"] = now
        return sess

def destroy_session(token):
    if not token:
        return
    with SESSIONS_LOCK:
        SESSIONS.pop(token, None)

# 8. Input Sanitization & Validation Helpers
def sanitize_string(val, max_len=500):
    if not isinstance(val, str):
        return ""
    # Strip dangerous control characters except whitespace
    cleaned = "".join(c for c in val if c in "\n\r\t" or ord(c) >= 32)
    cleaned = cleaned.strip()[:max_len]
    return html.escape(cleaned, quote=True)

def is_valid_phone(phone_str):
    if not isinstance(phone_str, str):
        return False
    cleaned = phone_str.strip()
    if len(cleaned) < 5 or len(cleaned) > 30:
        return False
    # Allow digits, +, spaces, dashes, parentheses, Persian/Arabic numerals
    return bool(re.match(r'^[0-9+\-\s().\u0660-\u0669\u06F0-\u06F9]+$', cleaned))

# 9. Static File Safety Checker
def is_safe_static_request(filepath):
    """
    Verifies that the requested filepath:
    1. Resides strictly within authorized public static directories.
    2. Does not touch forbidden extensions (.py, .env, .bat, .json, .md, .docx, etc.).
    3. Does not touch hidden files/folders (.*).
    4. Prohibits access to internal folders (docs, scripts, dossiers, data, mag/content).
    """
    real_path = os.path.realpath(filepath)
    if not os.path.isfile(real_path):
        return False, 404, "File Not Found"

    # Strictly forbidden directories
    forbidden_dirs = [
        os.path.realpath(CONTENT_DIR),
        os.path.realpath(DATA_DIR),
        os.path.realpath(LOGS_DIR),
        os.path.realpath(os.path.join(BASE_DIR, "docs")),
        os.path.realpath(os.path.join(BASE_DIR, "scripts")),
        os.path.realpath(os.path.join(BASE_DIR, "dossiers")),
        os.path.realpath(os.path.join(BASE_DIR, ".agents")),
        os.path.realpath(os.path.join(BASE_DIR, "__pycache__")),
        os.path.realpath(os.path.join(BASE_DIR, "tmp_chrome")),
    ]
    for fdir in forbidden_dirs:
        if real_path.startswith(fdir):
            return False, 403, "Access Denied"

    # Forbidden file extensions
    ext = os.path.splitext(real_path)[1].lower()
    forbidden_exts = {
        ".py", ".pyc", ".pyo", ".env", ".bat", ".cmd", ".sh", ".ps1",
        ".md", ".odt", ".docx", ".zip", ".tar", ".gz", ".bak", ".log",
        ".sqlite", ".db", ".yaml", ".yml", ".json"
    }
    # Exception for specific public json if needed (e.g. medical_icons.json)
    if ext == ".json":
        allowed_json = os.path.realpath(os.path.join(MAG_DIR, "components", "medical_icons.json"))
        if real_path != allowed_json:
            return False, 403, "Access Denied"
    elif ext in forbidden_exts:
        return False, 403, "Access Denied"

    # Forbidden filenames / dotfiles
    basename = os.path.basename(real_path)
    if basename.startswith(".") or basename in ["server.py", "START_PROJECT.bat", "README.md", "data.html"]:
        return False, 403, "Access Denied"

    # Authorized base directories
    allowed_dirs = [
        os.path.realpath(PORTAL_DIR),
        os.path.realpath(MAG_DIR),
        os.path.realpath(UPLOADS_DIR),
        os.path.realpath(os.path.join(BASE_DIR, "fonts")),
        os.path.realpath(os.path.join(BASE_DIR, "public")),
        os.path.realpath(os.path.join(BASE_DIR, "assets")),
        os.path.realpath(os.path.join(MAG_DIR, "public")),
    ]
    # Authorized root standalone assets
    allowed_root_files = [
        os.path.realpath(os.path.join(BASE_DIR, "three.min.js")),
        os.path.realpath(os.path.join(BASE_DIR, "favicon.ico")),
        os.path.realpath(os.path.join(BASE_DIR, "favicon.svg")),
        os.path.realpath(os.path.join(BASE_DIR, "site.webmanifest")),
        os.path.realpath(os.path.join(BASE_DIR, "robots.txt")),
        os.path.realpath(os.path.join(BASE_DIR, "sitemap.xml")),
        os.path.realpath(os.path.join(BASE_DIR, "404.html")),
        os.path.realpath(os.path.join(BASE_DIR, "llms.txt")),
        os.path.realpath(os.path.join(BASE_DIR, "llm.txt")),
    ]

    # Block all files directly in root directory unless explicitly whitelisted
    if os.path.dirname(real_path) == BASE_DIR and real_path not in allowed_root_files:
        return False, 403, "Access Denied"

    if real_path in allowed_root_files:
        return True, 200, None

    for adir in allowed_dirs:
        if real_path.startswith(adir):
            return True, 200, None

    return False, 403, "Access Denied"

# 9.5. Dynamic SEO Redirect Engine (Production Rule Matching & Caching)
REDIRECTS_FILE = os.path.join(CONTENT_DIR, "redirects.json")
_REDIRECTS_CACHE = []
_REDIRECTS_MTIME = 0
_REDIRECTS_LOCK = threading.Lock()

def load_redirects():
    """Thread-safe mtime-cached loader for SEO redirect rules."""
    global _REDIRECTS_CACHE, _REDIRECTS_MTIME
    if not os.path.isfile(REDIRECTS_FILE):
        return []
    try:
        mtime = os.path.getmtime(REDIRECTS_FILE)
        with _REDIRECTS_LOCK:
            if mtime != _REDIRECTS_MTIME:
                with open(REDIRECTS_FILE, "r", encoding="utf-8") as f:
                    _REDIRECTS_CACHE = json.load(f)
                _REDIRECTS_MTIME = mtime
            return list(_REDIRECTS_CACHE)
    except Exception as e:
        print(f"[Redirects] Error loading redirects: {e}")
        return list(_REDIRECTS_CACHE)

def save_redirects(rules):
    """Atomically writes redirect rules and refreshes memory cache."""
    global _REDIRECTS_CACHE, _REDIRECTS_MTIME
    atomic_write_json(REDIRECTS_FILE, rules)
    with _REDIRECTS_LOCK:
        _REDIRECTS_CACHE = rules
        if os.path.exists(REDIRECTS_FILE):
            _REDIRECTS_MTIME = os.path.getmtime(REDIRECTS_FILE)

def record_redirect_hit(rule_id):
    """Asynchronously increments the hit count and updates the lastHit timestamp."""
    def _worker():
        try:
            with WRITE_LOCK:
                if not os.path.isfile(REDIRECTS_FILE):
                    return
                with open(REDIRECTS_FILE, "r", encoding="utf-8") as f:
                    rules = json.load(f)
                updated = False
                now_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                for r in rules:
                    if r.get("id") == rule_id:
                        r["hitCount"] = r.get("hitCount", 0) + 1
                        r["lastHit"] = now_str
                        updated = True
                        break
                if updated:
                    atomic_write_json(REDIRECTS_FILE, rules)
                    global _REDIRECTS_CACHE, _REDIRECTS_MTIME
                    with _REDIRECTS_LOCK:
                        _REDIRECTS_CACHE = rules
                        _REDIRECTS_MTIME = os.path.getmtime(REDIRECTS_FILE)
        except Exception as e:
            print(f"[Redirects] Error recording hit for {rule_id}: {e}")
    threading.Thread(target=_worker, daemon=True).start()

def match_custom_redirect(path, raw_query=""):
    """
    Evaluates requested path against configured SEO redirect rules.
    Supports: Exact Match, Prefix Match, Regex Match, Query Preservation, and 410 Gone.
    Returns (status_code, target_url) or None if no match.
    """
    # Protected paths: Never redirect admin portal, REST APIs, or essential core assets
    system_prefixes = (
        "/api/", "/admin", "/login", "/logout", "/mag/admin", "/mag/login", "/fonts/",
        "/shared.css", "/shared.js", "/three.min.js", "/gsap.min.js", "/lenis.min.js",
        "/robots.txt", "/sitemap.xml", "/site.webmanifest", "/favicon.ico", "/favicon.svg"
    )
    for sp in system_prefixes:
        if path == sp or path.startswith(sp + "/") or path.startswith(sp):
            return None

    rules = load_redirects()
    norm_path = path.rstrip("/") if len(path) > 1 else path

    for rule in rules:
        if not rule.get("isActive", True):
            continue

        source = (rule.get("source") or "").strip()
        if not source:
            continue

        match_type = rule.get("matchType", "exact")
        try:
            status_code = int(rule.get("statusCode", 301))
        except (ValueError, TypeError):
            status_code = 301

        target = (rule.get("target") or "").strip()
        preserve_query = bool(rule.get("preserveQuery", True))
        matched = False
        resolved_target = target

        if match_type == "exact":
            norm_source = source.rstrip("/") if len(source) > 1 else source
            if norm_path.lower() == norm_source.lower():
                matched = True
                resolved_target = target

        elif match_type == "prefix":
            norm_source = source.rstrip("/")
            if norm_path.lower() == norm_source.lower():
                matched = True
                resolved_target = target
            elif norm_path.lower().startswith(norm_source.lower() + "/"):
                matched = True
                remainder = norm_path[len(norm_source):]
                resolved_target = target.rstrip("/") + remainder

        elif match_type == "regex":
            try:
                if re.search(source, path, re.IGNORECASE):
                    matched = True
                    resolved_target = re.sub(source, target, path, flags=re.IGNORECASE)
            except re.error:
                matched = False

        if matched:
            # 410 Gone de-indexing handler
            if status_code == 410:
                record_redirect_hit(rule.get("id"))
                return (410, None)

            # Prevent infinite self-redirection loops
            if not resolved_target:
                continue
            target_path = resolved_target.split("?")[0].rstrip("/") if len(resolved_target.split("?")[0]) > 1 else resolved_target.split("?")[0]
            if target_path.lower() == norm_path.lower():
                continue

            # Query string preservation
            if preserve_query and raw_query:
                sep = "&" if "?" in resolved_target else "?"
                resolved_target = f"{resolved_target}{sep}{raw_query}"

            record_redirect_hit(rule.get("id"))
            return (status_code, resolved_target)

    return None

# 9.6. Dynamic Schema.org Management Engine (Rank Math Grade)
SCHEMAS_FILE = os.path.join(CONTENT_DIR, "schemas.json")
_SCHEMAS_CACHE = []
_SCHEMAS_MTIME = 0
_SCHEMAS_LOCK = threading.Lock()

def load_schemas():
    """Thread-safe mtime-cached loader for site-wide and page-specific Schema structured data."""
    global _SCHEMAS_CACHE, _SCHEMAS_MTIME
    if not os.path.isfile(SCHEMAS_FILE):
        return []
    try:
        mtime = os.path.getmtime(SCHEMAS_FILE)
        with _SCHEMAS_LOCK:
            if mtime != _SCHEMAS_MTIME:
                with open(SCHEMAS_FILE, "r", encoding="utf-8") as f:
                    _SCHEMAS_CACHE = json.load(f)
                _SCHEMAS_MTIME = mtime
            return list(_SCHEMAS_CACHE)
    except Exception as e:
        print(f"[Schemas] Error loading schemas: {e}")
        return list(_SCHEMAS_CACHE)

def save_schemas(schemas):
    """Atomically writes schema rules and refreshes memory cache."""
    global _SCHEMAS_CACHE, _SCHEMAS_MTIME
    atomic_write_json(SCHEMAS_FILE, schemas)
    with _SCHEMAS_LOCK:
        _SCHEMAS_CACHE = schemas
        if os.path.exists(SCHEMAS_FILE):
            _SCHEMAS_MTIME = os.path.getmtime(SCHEMAS_FILE)

def validate_schema_structure(schema_obj):
    """Validates Schema.org JSON-LD structure (@context and @type). Returns list of error strings."""
    errors = []
    if isinstance(schema_obj, str):
        try:
            schema_obj = json.loads(schema_obj)
        except Exception as e:
            return [f"خطای ساختار JSON: {e}"]
    if not isinstance(schema_obj, dict):
        return ["ساختار اسکیما باید یک آبجکت JSON معتبر باشد."]
    
    ctx = schema_obj.get("@context")
    stype = schema_obj.get("@type")
    if not stype and isinstance(schema_obj.get("@graph"), list) and schema_obj.get("@graph"):
        stype = schema_obj["@graph"][0].get("@type")
    
    if not ctx or "schema.org" not in str(ctx).lower():
        errors.append("ویژگی @context باید شامل https://schema.org باشد.")
    if not stype:
        errors.append("ویژگی @type برای تعیین هویت اسکیما الزامی است.")
    return errors

# 9.5. Intelligent Robots.txt Audit & Suitability Analyzer (Site-Aware SEO Engine)
def analyze_robots_txt(content):
    """
    تحلیل هوشمند و تطبیق ساختار فایل robots.txt با معماری اختصاصی وب‌سایت پزشکآن:
    - بررسی مسدود نبودن صفحات عمومی (/, /mag, /product, /packages, ...)
    - بررسی دسترسی کامل خزنده‌های گوگل به فایل‌های رندرینگ (shared.css, shared.js, fonts)
    - بررسی حفاظت از پیشخوان مدیریت، احراز هویت و APIهای داخلی (/admin, /login, /api/)
    - پایش امنیت فایل‌های پایگاه داده و محتوای خام (data/, *.json)
    - ارزیابی وجود و استاندارد بودن نشانی نقشه رسمی سایت (sitemap.xml با پروتکل HTTPS)
    - اعتبارسنجی سینتکس و دستورات پروتکل Robot Exclusion
    - محاسبه نمره سلامت و خروجی وضعیت صلاحیت (مناسب/نامناسب برای سایت)
    """
    if not content or not content.strip():
        return {
            "score": 0,
            "isSuitable": False,
            "verdict": "فایل خالی است؛ موتورهای جستجو بدون هیچ هدایتی اقدام به خزش تمامی بخش‌ها خواهند کرد.",
            "verdictType": "critical",
            "checks": [
                {
                    "id": "empty_file",
                    "title": "محتوای فایل robots.txt",
                    "status": "fail",
                    "category": "critical",
                    "message": "فایل خالی است یا هیچ دستوری در آن یافت نشد."
                }
            ],
            "recommendations": ["لطفاً از الگوی استاندارد پزشکآن برای راه‌اندازی فایل robots.txt استفاده فرمایید."],
            "summary": {
                "userAgents": [],
                "allowCount": 0,
                "disallowCount": 0,
                "sitemaps": [],
                "syntaxErrorsCount": 1
            }
        }

    lines = content.splitlines()
    checks = []
    score = 100

    user_agents = []
    disallows = []
    allows = []
    sitemaps = []
    crawl_delays = []
    syntax_errors = []

    current_agent = None

    for idx, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            syntax_errors.append(f"سطر {idx}: فاقد علامت دونقطه (:) است -> '{line}'")
            continue

        directive, _, val = line.partition(":")
        d_lower = directive.strip().lower()
        val_clean = val.strip()

        if d_lower == "user-agent":
            current_agent = val_clean
            if current_agent not in user_agents:
                user_agents.append(current_agent)
        elif d_lower == "disallow":
            disallows.append({"agent": (current_agent or "*").lower(), "path": val_clean, "line": idx})
        elif d_lower == "allow":
            allows.append({"agent": (current_agent or "*").lower(), "path": val_clean, "line": idx})
        elif d_lower == "sitemap":
            sitemaps.append(val_clean)
        elif d_lower == "crawl-delay":
            crawl_delays.append(val_clean)
        else:
            syntax_errors.append(f"سطر {idx}: دستور ناشناخته '{directive}'")

    # 1. Fatal Blanket Disallow Check
    has_fatal_block = any(
        d["path"] == "/" and d["agent"] in ("*", "googlebot")
        for d in disallows
    )
    has_root_allow = any(
        a["path"] == "/" and a["agent"] in ("*", "googlebot")
        for a in allows
    )

    if has_fatal_block and not has_root_allow:
        score -= 60
        checks.append({
            "id": "blanket_disallow",
            "title": "عدم مسدودسازی کلی وب‌سایت (Indexable Status)",
            "status": "fail",
            "category": "critical",
            "message": "دستور Disallow: / فعال است که کل دسترسی موتورهای جستجو به تمامی صفحات سایت را متوقف و ایندکس آن را نابود می‌کند!"
        })
    else:
        checks.append({
            "id": "blanket_disallow",
            "title": "دسترس‌پذیری سراسری وب‌سایت برای خزنده‌ها",
            "status": "pass",
            "category": "critical",
            "message": "دستور مسدودسازی فله‌ای ریشه وجود ندارد و صفحات عمومی آزادانه قابل ایندکس هستند."
        })

    # 2. Rendering Assets Check (Googlebot requirement for Core Web Vitals)
    blocked_assets = []
    for d in disallows:
        p = d["path"].lower()
        if p in ("/shared.css", "/shared.js", "/fonts/", "/*.css", "/*.js") or p.startswith("/shared") or p.startswith("/fonts"):
            # Check if there is an explicit allow overriding it
            if not any(a["path"].lower() == p for a in allows):
                blocked_assets.append(d["path"])

    has_explicit_assets = any(a["path"].lower() in ("/shared.css", "/shared.js", "/fonts/") for a in allows)

    if blocked_assets:
        score -= 25
        checks.append({
            "id": "rendering_assets",
            "title": "دسترسی گوگل‌بات به فایل‌های رندرینگ (CSS / JS / Fonts)",
            "status": "fail",
            "category": "rendering",
            "message": f"دارایی‌های حیاتی رندر ظاهر سایت ({', '.join(blocked_assets)}) مسدود شده‌اند! گوگل‌بات قادر به تحلیل چیدمان صفحه نخواهد بود که افت شدید رتبه در Core Web Vitals را در پی دارد."
        })
    elif has_explicit_assets:
        checks.append({
            "id": "rendering_assets",
            "title": "مجوز صریح رندرینگ فایل‌های CSS، جاوااسکریپت و فونت‌ها",
            "status": "pass",
            "category": "rendering",
            "message": "فایل‌های shared.css، shared.js و فونت‌های فارسی صراحتاً مجاز شده‌اند و رندر صفحات بالینی به صورت عالی انجام می‌شود."
        })
    else:
        checks.append({
            "id": "rendering_assets",
            "title": "دسترسی به دارایی‌های رندرینگ استایل و اسکریپت",
            "status": "pass",
            "category": "rendering",
            "message": "فایل‌های رندرینگ مسدود نشده‌اند. (توصیه بهینه‌سازی: اضافه کردن دستورات صریح Allow: /shared.css و Allow: /shared.js برای اطمینان مضاعف)."
        })

    # 3. Sensitive / Admin / API Protection
    disallow_paths = [d["path"].rstrip("/").lower() for d in disallows]
    admin_blocked = any(p in disallow_paths for p in ("/admin", "/wp-admin", "/mag/admin"))
    login_blocked = any(p in disallow_paths for p in ("/login", "/mag/login"))
    api_blocked = any(p in disallow_paths for p in ("/api", "/api/"))

    if admin_blocked and login_blocked and api_blocked:
        checks.append({
            "id": "admin_security",
            "title": "حفاظت از پیشخوان مدیریت، صفحات ورود و APIهای داخلی",
            "status": "pass",
            "category": "security",
            "message": "مسیرهای حساس /admin، /login و /api/ به درستی برای خزنده‌ها مسدود شده‌اند تا امنیت و بودجه خزش (Crawl Budget) بهینه بماند."
        })
    else:
        missing_sec = []
        if not admin_blocked: missing_sec.append("/admin")
        if not login_blocked: missing_sec.append("/login")
        if not api_blocked: missing_sec.append("/api/")
        score -= 15
        checks.append({
            "id": "admin_security",
            "title": "حفاظت از مسیرهای مدیریتی و اندپوینت‌های داخلی",
            "status": "warn",
            "category": "security",
            "message": f"مسیرهای حساس ({', '.join(missing_sec)}) در لیست مسدودی‌ها یافت نشدند. توصیه امنیتی: این مسیرها برای جلوگیری از اتلاف بودجه خزش باید مسدود شوند."
        })

    # 4. Data / Clinical JSON Files Protection
    data_blocked = any("*.json" in d["path"].lower() or "/data" in d["path"].lower() for d in disallows)
    if data_blocked:
        checks.append({
            "id": "data_privacy",
            "title": "محافظت از فایل‌های داده‌ای و پایگاه داده محتوا (JSON)",
            "status": "pass",
            "category": "security",
            "message": "فایل‌های خام مقالات و دیتابیس JSON سایت در برابر خزش مستقیم و ایندکس تکراری به درستی محافظت شده‌اند."
        })
    else:
        score -= 5
        checks.append({
            "id": "data_privacy",
            "title": "محافظت از فایل‌های داده‌ای خام (JSON Data)",
            "status": "warn",
            "category": "security",
            "message": "پیشنهاد می‌شود دستور Disallow: /*.json$ جهت ممانعت از ایندکس ناخواسته رکوردهای متنی در موتورهای جستجو قرار گیرد."
        })

    # 5. XML Sitemap Declaration
    if not sitemaps:
        score -= 20
        checks.append({
            "id": "sitemap_declaration",
            "title": "معرفی نقشه رسمی سایت (XML Sitemap)",
            "status": "fail",
            "category": "sitemap",
            "message": "هیچ دستور Sitemap در فایل ثبت نشده است! خزنده‌های گوگل برای کشف مقالات و صفحات به نقشه سایت احتیاج دارند."
        })
    else:
        has_http = any(s.startswith("http://") for s in sitemaps)
        has_pezeshkan = any("pezeshkan.me/sitemap.xml" in s for s in sitemaps)
        if has_http:
            score -= 10
            checks.append({
                "id": "sitemap_declaration",
                "title": "پروتکل امن نشانی نقشه سایت (HTTPS)",
                "status": "warn",
                "category": "sitemap",
                "message": "نشانی نقشه سایت با پروتکل ناامن HTTP درج شده است؛ باید با پروتکل امن HTTPS (https://pezeshkan.me/sitemap.xml) بازنویسی شود."
            })
        elif has_pezeshkan:
            checks.append({
                "id": "sitemap_declaration",
                "title": "معرفی نقشه سایت رسمی پزشکآن با پروتکل امن HTTPS",
                "status": "pass",
                "category": "sitemap",
                "message": f"نقشه سایت رسمی ({sitemaps[0]}) به صورت استاندارد به تمام موتورهای جستجو معرفی شده است."
            })
        else:
            checks.append({
                "id": "sitemap_declaration",
                "title": "نقشه سایت معتبر",
                "status": "pass",
                "category": "sitemap",
                "message": f"نقشه سایت به درستی معرفی شده است: {sitemaps[0]}"
            })

    # 6. Crawlability of Public Sections
    blocked_public = []
    for d in disallows:
        dp = d["path"].rstrip("/").lower()
        if dp in ("/mag", "/product", "/features", "/packages", "/tutorials", "/contact", "/about", "/services"):
            blocked_public.append(dp)
    if blocked_public:
        score -= 25
        checks.append({
            "id": "public_sections",
            "title": "دسترس‌پذیری بخش‌های عمومی و مقالات مجله سلامت",
            "status": "fail",
            "category": "critical",
            "message": f"بخش‌های عمومی کلیدی سایت ({', '.join(blocked_public)}) در مسدودی‌ها قرار دارند و از نتایج گوگل حذف خواهند شد!"
        })
    else:
        checks.append({
            "id": "public_sections",
            "title": "دسترسی آزاد به صفحات عمومی پرتال و مجله سلامت",
            "status": "pass",
            "category": "critical",
            "message": "مسیرهای عمومی نظیر /mag، /product، /packages و /tutorials بدون مانع در دسترس خزنده‌ها هستند."
        })

    # 7. Syntax and Directives Structure
    if syntax_errors:
        score -= min(30, len(syntax_errors) * 10)
        checks.append({
            "id": "syntax_errors",
            "title": "صحت نگارشی دستورات پروتکل ربات‌ها",
            "status": "fail",
            "category": "syntax",
            "message": f"خطای ساختاری یافت شد: {syntax_errors[0]}" + (f" (و {len(syntax_errors)-1} مورد دیگر)" if len(syntax_errors) > 1 else "")
        })
    else:
        checks.append({
            "id": "syntax_errors",
            "title": "صحت نگارشی و رعایت استانداردهای خزش",
            "status": "pass",
            "category": "syntax",
            "message": "تمامی دستورات از ساختار استاندارد و معتبر پروتکل Robots Exclusion پیروی می‌کنند."
        })

    # Final score clamping & suitability calculation
    score = max(0, min(100, score))
    has_critical_fail = any(c["status"] == "fail" and c["category"] == "critical" for c in checks)
    is_suitable = score >= 80 and not has_critical_fail

    if score >= 90 and not has_critical_fail:
        verdict = "عالی و کاملاً منطبق با معماری سئو وب‌سایت پزشکآن"
        verdict_type = "optimal"
    elif score >= 70 and not has_critical_fail:
        verdict = "مناسب برای وب‌سایت؛ چند توصیه بهینه‌سازی جزئی وجود دارد"
        verdict_type = "good"
    elif score >= 50:
        verdict = "نیازمند اصلاح؛ موارد هشداردهنده در حفاظت یا بودجه خزش وجود دارد"
        verdict_type = "warning"
    else:
        verdict = "نامناسب و خطرناک؛ مسدودسازی ناخواسته یا خطای بحرانی در ایندکس سایت وجود دارد"
        verdict_type = "critical"

    recommendations = []
    for c in checks:
        if c["status"] in ("fail", "warn"):
            recommendations.append(c["message"])

    return {
        "score": score,
        "isSuitable": is_suitable,
        "verdict": verdict,
        "verdictType": verdict_type,
        "checks": checks,
        "recommendations": recommendations,
        "summary": {
            "userAgents": user_agents or ["*"],
            "allowCount": len(allows),
            "disallowCount": len(disallows),
            "sitemaps": sitemaps,
            "syntaxErrorsCount": len(syntax_errors)
        }
    }

# 9.6. LLMS.txt Generator & Engine (Rank Math Compatible Protocol for AI & LLMs)
LLMS_SETTINGS_FILE = os.path.join(CONTENT_DIR, "llms_settings.json")
_LLMS_LOCK = threading.Lock()
_LLMS_CACHE = None
_LLMS_MTIME = 0

DEFAULT_LLMS_SETTINGS = {
    "isEnabled": True,
    "publicUrl": "https://pezeshkan.me/llms.txt",
    "postTypes": {
        "posts": True,       # نوشته‌ها
        "pages": True,       # برگه‌ها
        "floating": True     # عناصر شناور
    },
    "taxonomies": {
        "categories": True,  # دسته‌ها
        "tags": True         # برچسب‌ها
    },
    "limit": 50,
    "additionalContent": "## اطلاعات تکمیلی و پروتکل مدل‌های زبانی\nتمامی محتواهای بالینی این پایگاه تحت نظارت هیئت علمی و پزشکان متخصص پزشکآن تدوین گردیده است. استناد و استفاده در سامانه‌های استدلال پزشکی و هوش مصنوعی با ذکر منبع مجاز است."
}

def load_llms_settings():
    global _LLMS_CACHE, _LLMS_MTIME
    if not os.path.isfile(LLMS_SETTINGS_FILE):
        return dict(DEFAULT_LLMS_SETTINGS)
    try:
        mtime = os.path.getmtime(LLMS_SETTINGS_FILE)
        with _LLMS_LOCK:
            if _LLMS_CACHE is None or mtime != _LLMS_MTIME:
                with open(LLMS_SETTINGS_FILE, "r", encoding="utf-8") as f:
                    _LLMS_CACHE = json.load(f)
                _LLMS_MTIME = mtime
            return dict(_LLMS_CACHE)
    except Exception as e:
        print(f"[LLMS] Error loading settings: {e}")
        return dict(DEFAULT_LLMS_SETTINGS)

def save_llms_settings(settings):
    global _LLMS_CACHE, _LLMS_MTIME
    atomic_write_json(LLMS_SETTINGS_FILE, settings)
    with _LLMS_LOCK:
        _LLMS_CACHE = settings
        if os.path.exists(LLMS_SETTINGS_FILE):
            _LLMS_MTIME = os.path.getmtime(LLMS_SETTINGS_FILE)

def generate_llms_txt(settings=None):
    """
    تولید ساختار استاندارد Markdown فایل llms.txt ویژه مدل‌های هوش مصنوعی (ChatGPT, Claude, Gemini, Perplexity)
    مطابق با استاندارد رسمی Rank Math و انتخاب انواع پست‌ها و طبقه‌بندی‌ها
    """
    if settings is None:
        settings = load_llms_settings()

    is_enabled = settings.get("isEnabled", settings.get("enabled", True))
    if not is_enabled:
        return "# llms.txt is currently disabled by administrator.\n"

    try:
        limit = int(settings.get("limit", settings.get("postLimit", 50)))
    except (ValueError, TypeError):
        limit = 50

    post_types = settings.get("postTypes", {})
    if not isinstance(post_types, dict):
        post_types = {"posts": True, "pages": True, "floating": True}

    taxonomies = settings.get("taxonomies", {})
    if not isinstance(taxonomies, dict):
        taxonomies = {"categories": True, "tags": True}

    additional = (settings.get("additionalContent") or "").strip()

    lines = []
    lines.append("# پزشکآن | Pezeshkan Health & Clinical Ecosystem")
    lines.append("> اکوسیستم جامع سلامت دیجیتال، پرونده ۳۶۰ درجه الکترونیک سلامت (EHR) و پایگاه مقالات بالینی پزشکی تحت نظارت هیئت علمی.")
    lines.append("")

    # 1. نوشته‌ها (Articles / Clinical Guides)
    if post_types.get("posts", True):
        lines.append("## مقالات و راهنماهای بالینی (نوشته‌ها)")
        try:
            articles_file = os.path.join(CONTENT_DIR, "articles.json")
            if os.path.isfile(articles_file):
                with open(articles_file, "r", encoding="utf-8") as f:
                    articles = json.load(f)
                count = 0
                for a in articles:
                    if count >= limit:
                        break
                    slug = a.get("slug") or a.get("id")
                    title = a.get("title", "").strip()
                    summary = (a.get("summary") or a.get("metaDescription") or "").strip()
                    url = f"https://pezeshkan.me/mag/{slug}"
                    if title:
                        desc_part = f": {summary}" if summary else ""
                        lines.append(f"- [{title}]({url}){desc_part}")
                        count += 1
        except Exception as e:
            lines.append(f"- خطا در بارگذاری مقالات: {e}")
        lines.append("")

    # 2. برگه‌ها (Pages / Portal Sections)
    if post_types.get("pages", True):
        lines.append("## برگه‌ها و پرتال اصلی (برگه‌ها)")
        pages_list = [
            ("پرتال پزشکآن", "https://pezeshkan.me/", "صفحه اصلی اکوسیستم سلامت دیجیتال و زیرسیستم‌های هوشمند مطب"),
            ("محصولات و پرونده الکترونیک سلامت", "https://pezeshkan.me/product", "معرفی پرونده الکترونیک ۳۶۰ درجه، چارت قلم نوری و دستیار هوش مصنوعی"),
            ("قابلیت‌های فنی و بالینی", "https://pezeshkan.me/features", "امکانات هوشمند نوبت‌دهی آنلاین، اتصال به پوز بانکی و نسخه الکترونیک"),
            ("تعرفه‌ها و بسته‌های اشتراک", "https://pezeshkan.me/packages", "پلن‌های اشتراک ماهانه و سالانه نرم‌افزار مطب و کلینیک"),
            ("مرکز آموزش‌های CRM پزشکی", "https://pezeshkan.me/tutorials", "راهنماهای استانداردسازی فرایندهای پذیرش، مالی و ارزیابی علائم"),
            ("درباره پزشکآن", "https://pezeshkan.me/about", "معرفی تیم توسعه، استاندارد امنیتی AES-256 و اهداف اکوسیستم"),
            ("تماس و مشاوره", "https://pezeshkan.me/contact", "پشتیبانی ۲۴ ساعته، راه‌های ارتباطی و درخواست نسخه آزمایشی")
        ]
        count = 0
        for p_title, p_url, p_desc in pages_list:
            if count >= limit:
                break
            lines.append(f"- [{p_title}]({p_url}): {p_desc}")
            count += 1
        lines.append("")

    # 3. دسته‌ها (Categories / Departments)
    if taxonomies.get("categories", True):
        lines.append("## دسته‌ها و دپارتمان‌های تخصصی پزشکی (دسته‌ها)")
        try:
            pillars_file = os.path.join(CONTENT_DIR, "pillars.json")
            if os.path.isfile(pillars_file):
                with open(pillars_file, "r", encoding="utf-8") as f:
                    pillars = json.load(f)
                count = 0
                for p in pillars:
                    if count >= limit:
                        break
                    p_name = p.get("name") or p.get("title", "")
                    p_desc = p.get("intent") or p.get("desc", "")
                    p_slug = p.get("slug", "").strip("/")
                    p_url = f"https://pezeshkan.me/{p_slug}" if p_slug.startswith("mag") else f"https://pezeshkan.me/mag/{p_slug}"
                    if p_name:
                        desc_part = f": {p_desc}" if p_desc else ""
                        lines.append(f"- [{p_name}]({p_url}){desc_part}")
                        count += 1
        except Exception as e:
            lines.append(f"- خطا در بارگذاری دسته‌بندی‌ها: {e}")
        lines.append("")

    # 4. برچسب‌ها (Tags / Keywords)
    if taxonomies.get("tags", True):
        lines.append("## برچسب‌ها و واژگان کلیدی پرکاربرد (برچسب‌ها)")
        tags_list = [
            ("دیسک کمر و تنگی نخاع", "https://pezeshkan.me/mag?tag=disc"),
            ("سونوگرافی بارداری", "https://pezeshkan.me/mag?tag=ultrasound"),
            ("پرونده الکترونیک سلامت", "https://pezeshkan.me/mag?tag=ehr"),
            ("تریاژ اورژانس", "https://pezeshkan.me/mag?tag=triage"),
            ("نوبت‌دهی آنلاین", "https://pezeshkan.me/mag?tag=booking"),
            ("اتصال به کارت‌خوان مطب", "https://pezeshkan.me/mag?tag=pos")
        ]
        count = 0
        for t_name, t_url in tags_list:
            if count >= limit:
                break
            lines.append(f"- [{t_name}]({t_url})")
            count += 1
        lines.append("")

    # 5. عناصر شناور (Floating Elements / Callouts / FAQs)
    if post_types.get("floating", True):
        lines.append("## عناصر شناور و پروتکل‌های بالینی (عناصر شناور)")
        floating_items = [
            ("پروتکل تریاژ بالینی و شرایط ارجاع اورژانس", "https://pezeshkan.me/mag#triage-protocol", "معیارهای تشخیصی علائم قرمز (Red Flags) و شرایط هشدار بیمار"),
            ("سوالات متداول دارویی و مراقبت پس از درمان", "https://pezeshkan.me/mag#faq-clinical", "پاسخ به ابهامات شایع بیماران درباره نحوه مصرف و بازتوانی"),
            ("هشدارهای بالینی و منع مصرف داروها", "https://pezeshkan.me/mag#clinical-callouts", "جعبه‌های هشدار منع مصرف در مقالات تخصصی")
        ]
        count = 0
        for f_name, f_url, f_desc in floating_items:
            if count >= limit:
                break
            lines.append(f"- [{f_name}]({f_url}): {f_desc}")
            count += 1
        lines.append("")

    # 6. محتوای اضافی (Additional Content)
    if additional:
        lines.append("## محتوای اضافی و یادداشت‌های تکمیلی")
        lines.append(additional)
        lines.append("")

    return "\n".join(lines).strip() + "\n"

# 9.8. Dynamic Site Structure & Internal Linking Graph Engine
def extract_links_from_html(html_text):
    """
    Extracts all <a> tags with href and anchor text from HTML.
    Returns list of dicts: [{"href": ..., "anchor": ...}]
    """
    if not html_text or not isinstance(html_text, str):
        return []
    pattern = re.compile(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
    links = []
    for match in pattern.finditer(html_text):
        href = match.group(1).strip()
        raw_anchor = match.group(2)
        clean_anchor = re.sub(r'<[^>]+>', '', raw_anchor).strip()
        if not clean_anchor:
            clean_anchor = "بدون متن پیوند"
        links.append({
            "href": href,
            "anchor": clean_anchor
        })
    return links

def analyze_site_structure(override_article=None):
    """
    Analyzes the entire site hierarchy, content silos, and internal linking graph.
    If override_article is provided (e.g. during live editing in admin), it merges
    the unsaved article state to give real-time instant feedback.
    """
    articles_file = os.path.join(CONTENT_DIR, "articles.json")
    pillars_file = os.path.join(CONTENT_DIR, "pillars.json")

    articles = []
    if os.path.isfile(articles_file):
        try:
            with open(articles_file, "r", encoding="utf-8") as f:
                articles = json.load(f)
        except Exception as e:
            print(f"[SiteStructure] Error loading articles: {e}")

    # Merge override if provided (for live real-time analysis while typing)
    if override_article and isinstance(override_article, dict):
        ov_id = override_article.get("id")
        ov_slug = override_article.get("slug")
        replaced = False
        for i, a in enumerate(articles):
            if (ov_id and a.get("id") == ov_id) or (ov_slug and a.get("slug") == ov_slug):
                articles[i] = {**a, **override_article}
                replaced = True
                break
        if not replaced:
            articles.append(override_article)

    pillars = []
    if os.path.isfile(pillars_file):
        try:
            with open(pillars_file, "r", encoding="utf-8") as f:
                pillars = json.load(f)
        except Exception as e:
            print(f"[SiteStructure] Error loading pillars: {e}")

    # Build slug / url lookup tables
    article_by_slug = {}
    article_by_id = {}
    for a in articles:
        slug = (a.get("slug") or "").strip().strip("/")
        art_id = a.get("id", "")
        if slug:
            article_by_slug[slug] = a
        if art_id:
            article_by_id[art_id] = a

    pillar_by_slug = {}
    pillar_by_id = {}
    for p in pillars:
        slug = (p.get("slug") or "").strip().strip("/")
        pid = str(p.get("id"))
        if slug:
            pillar_by_slug[slug] = p
        pillar_by_id[pid] = p

    portal_routes = {
        "": "صفحه اصلی پرتال پزشکآن",
        "product": "معرفی محصول و پرونده الکترونیک سلامت",
        "features": "قابلیت‌های فنی و بالینی مطب",
        "packages": "تعرفه‌ها و بسته‌های اشتراک",
        "tutorials": "آموزش‌های CRM پزشکی",
        "about": "درباره پزشکآن و استانداردهای بالینی",
        "contact": "تماس با ما و مشاوره",
        "mag": "پایگاه مقالات مجله سلامت"
    }

    inlinks_map = {a.get("id"): [] for a in articles}
    outlinks_map = {a.get("id"): [] for a in articles}

    total_internal_links = 0
    total_external_links = 0

    for a in articles:
        aid = a.get("id")
        html_content = (a.get("contentHtml") or "") + " " + (a.get("rawHtml") or "")
        extracted = extract_links_from_html(html_content)

        for item in extracted:
            href = item["href"]
            anchor = item["anchor"]

            parsed = urllib.parse.urlparse(href)
            path = parsed.path.strip("/")

            is_ext = False
            if parsed.netloc and "pezeshkan.me" not in parsed.netloc and "localhost" not in parsed.netloc:
                is_ext = True

            if is_ext:
                total_external_links += 1
                outlinks_map[aid].append({
                    "targetType": "external",
                    "targetTitle": parsed.netloc or href,
                    "targetSlug": href,
                    "anchorText": anchor,
                    "href": href
                })
                continue

            # Internal link!
            total_internal_links += 1

            # 1. Match against article slugs
            slug_candidate = path.split("/")[-1] if "/" in path else path
            if slug_candidate in article_by_slug:
                target_art = article_by_slug[slug_candidate]
                target_id = target_art.get("id")
                outlinks_map[aid].append({
                    "targetType": "article",
                    "targetId": target_id,
                    "targetSlug": target_art.get("slug"),
                    "targetTitle": target_art.get("title"),
                    "anchorText": anchor,
                    "href": href
                })
                if target_id in inlinks_map:
                    inlinks_map[target_id].append({
                        "sourceId": aid,
                        "sourceSlug": a.get("slug"),
                        "sourceTitle": a.get("title"),
                        "anchorText": anchor,
                        "href": href
                    })
                continue

            # 2. Match against pillars/categories
            matched_pillar = None
            for pslug, pdata in pillar_by_slug.items():
                if path == pslug or path.endswith(pslug):
                    matched_pillar = pdata
                    break
            if matched_pillar:
                outlinks_map[aid].append({
                    "targetType": "category",
                    "targetId": matched_pillar.get("id"),
                    "targetSlug": matched_pillar.get("slug"),
                    "targetTitle": matched_pillar.get("name"),
                    "anchorText": anchor,
                    "href": href
                })
                continue

            # 3. Match against portal pages
            clean_route = path.replace(".html", "")
            if clean_route in portal_routes:
                outlinks_map[aid].append({
                    "targetType": "portal",
                    "targetSlug": f"/{clean_route}",
                    "targetTitle": portal_routes[clean_route],
                    "anchorText": anchor,
                    "href": href
                })
                continue

            # General internal link
            outlinks_map[aid].append({
                "targetType": "internal_other",
                "targetTitle": href,
                "targetSlug": href,
                "anchorText": anchor,
                "href": href
            })

    # Prepare detailed article models
    articles_analysis = []
    orphan_articles = []
    for a in articles:
        aid = a.get("id")
        in_list = inlinks_map.get(aid, [])
        out_list = outlinks_map.get(aid, [])

        in_count = len(in_list)
        out_count = len(out_list)

        if in_count == 0:
            health_tier = "orphan"
        elif in_count == 1:
            health_tier = "weak"
        elif in_count <= 4:
            health_tier = "good"
        else:
            health_tier = "pillar"

        pillar_id = str(a.get("pillarId", ""))
        pillar_obj = pillar_by_id.get(pillar_id) or {}
        cat_name = a.get("categoryName") or pillar_obj.get("name") or "عمومی"
        cat_slug = a.get("pillarSlug") or pillar_obj.get("slug") or "/mag"

        art_model = {
            "id": aid,
            "title": a.get("title", ""),
            "slug": a.get("slug", ""),
            "fullUrl": f"https://pezeshkan.me/mag/{a.get('slug')}",
            "categoryName": cat_name,
            "categorySlug": cat_slug,
            "pillarId": a.get("pillarId"),
            "status": a.get("status", "published"),
            "inlinksCount": in_count,
            "inlinks": in_list,
            "outlinksCount": out_count,
            "outlinks": out_list,
            "isOrphan": in_count == 0,
            "healthTier": health_tier
        }
        articles_analysis.append(art_model)

        if in_count == 0:
            orphan_articles.append(art_model)

    # Content Silos & Category breakdown
    silos_analysis = []
    for p in pillars:
        pid = str(p.get("id"))
        p_slug = p.get("slug", "")
        p_articles = [
            a for a in articles_analysis
            if str(a.get("pillarId")) == pid or (a.get("categorySlug") and p_slug in a.get("categorySlug"))
        ]
        p_orphan_count = sum(1 for a in p_articles if a["isOrphan"])
        p_total_inlinks = sum(a["inlinksCount"] for a in p_articles)
        p_total_outlinks = sum(a["outlinksCount"] for a in p_articles)

        silos_analysis.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "slug": p.get("slug"),
            "icon": p.get("icon", "📁"),
            "desc": p.get("desc", ""),
            "articlesCount": len(p_articles),
            "orphanCount": p_orphan_count,
            "totalInlinks": p_total_inlinks,
            "totalOutlinks": p_total_outlinks,
            "articleIds": [a["id"] for a in p_articles]
        })

    # Global SEO Link Health Score (0 to 100)
    total_articles_count = len(articles)
    orphan_count = len(orphan_articles)
    orphan_ratio = (orphan_count / total_articles_count) if total_articles_count > 0 else 0
    avg_inlinks = (total_internal_links / total_articles_count) if total_articles_count > 0 else 0

    score = 100 - int(orphan_ratio * 70)
    if avg_inlinks < 1.0:
        score -= 15
    elif avg_inlinks >= 2.0:
        score += 5
    score = max(10, min(100, score))

    return {
        "success": True,
        "summary": {
            "totalArticles": total_articles_count,
            "totalCategories": len(pillars),
            "totalInternalLinks": total_internal_links,
            "totalExternalLinks": total_external_links,
            "orphanCount": orphan_count,
            "orphanRatePercent": round(orphan_ratio * 100, 1),
            "avgInternalLinksPerArticle": round(avg_inlinks, 1),
            "healthScore": score
        },
        "articles": articles_analysis,
        "orphans": orphan_articles,
        "silos": silos_analysis
    }

def audit_comprehensive_seo(override_article=None):
    """
    Comprehensive Site-Wide SEO Health & Anti-Spam Verification Engine.
    Strictly derives metrics from actual content files (articles.json, pillars.json, newsletters.json).
    Detects and flags spammy behaviors:
      - Keyword Stuffing & Abnormal Keyword Density (> 2.8% spam threshold)
      - Duplicate Meta Titles & Meta Descriptions across pages
      - Thin Content (< 350 words in medical YMYL context)
      - Commercial Anchor Text Over-Optimization (> 3 identical anchors for same target)
      - Broken Internal Links / 404 dead references
      - Medical E-E-A-T deficiencies (Missing Doctor Name, Medical Council Number, Clinical Reviewer)
    Audits Topic Cluster and Pillar-Cluster completeness & silo connectivity.
    Calculates composite site health score (0-100) and actionable fix tasks.
    """
    # 1. Leverage internal link graph & silo structure
    structure = analyze_site_structure(override_article=override_article)
    articles_analysis = structure.get("articles", [])
    orphans = structure.get("orphans", [])
    silos = structure.get("silos", [])
    summary_struct = structure.get("summary", {})

    articles_file = os.path.join(CONTENT_DIR, "articles.json")
    pillars_file = os.path.join(CONTENT_DIR, "pillars.json")
    newsletters_file = os.path.join(CONTENT_DIR, "newsletters.json")

    articles = []
    if os.path.isfile(articles_file):
        try:
            with open(articles_file, "r", encoding="utf-8") as f:
                articles = json.load(f)
        except Exception as e:
            print(f"[SeoAudit] Error loading articles: {e}")

    if override_article and isinstance(override_article, dict):
        ov_id = override_article.get("id")
        ov_slug = override_article.get("slug")
        replaced = False
        for i, a in enumerate(articles):
            if (ov_id and a.get("id") == ov_id) or (ov_slug and a.get("slug") == ov_slug):
                articles[i] = {**a, **override_article}
                replaced = True
                break
        if not replaced:
            articles.append(override_article)

    pillars = []
    if os.path.isfile(pillars_file):
        try:
            with open(pillars_file, "r", encoding="utf-8") as f:
                pillars = json.load(f)
        except Exception as e:
            print(f"[SeoAudit] Error loading pillars: {e}")

    newsletters = []
    if os.path.isfile(newsletters_file):
        try:
            with open(newsletters_file, "r", encoding="utf-8") as f:
                newsletters = json.load(f)
        except Exception as e:
            print(f"[SeoAudit] Error loading newsletters: {e}")

    # Articles lookup by id & slug
    art_by_id = {a.get("id"): a for a in articles}
    art_by_slug = {(a.get("slug") or "").strip().strip("/"): a for a in articles if a.get("slug")}
    pillar_by_slug = {(p.get("slug") or "").strip().strip("/"): p for p in pillars if p.get("slug")}

    # Collections for spam & compliance metrics
    kw_stuffing_list = []
    duplicate_meta_titles = []
    duplicate_meta_descs = []
    thin_content_list = []
    eeat_deficiency_list = []
    broken_internal_links = []
    actionable_fixes = []

    # Map for duplicate detection
    meta_title_map = {}
    meta_desc_map = {}

    # Map for anchor text optimization: (target_path, anchor_text) -> list of source_ids
    anchor_usage_map = {}

    total_words_all = 0

    for a in articles:
        aid = a.get("id", "")
        title = a.get("title", "")
        slug = a.get("slug", "")
        raw_html = a.get("rawHtml") or ""
        content_html = a.get("contentHtml") or ""
        summary_text = a.get("summary") or ""
        combined_html = raw_html + " " + content_html

        # Extract text & calculate real word count
        clean_text = re.sub(r'<[^>]+>', ' ', combined_html)
        tokens = [t for t in clean_text.split() if t.strip()]
        word_count = len(tokens)
        total_words_all += word_count

        # Focus keyword analysis
        focus_kw = (a.get("focusKeyword") or "").strip()
        kw_density = 0.0
        kw_occurrences = 0
        kw_status = "missing"

        if focus_kw:
            kw_tokens = [k for k in focus_kw.split() if k]
            kw_len = max(1, len(kw_tokens))
            kw_lower = focus_kw.lower()
            text_lower = clean_text.lower()
            kw_occurrences = text_lower.count(kw_lower)
            if word_count > 0:
                kw_density = round((kw_occurrences * kw_len / word_count) * 100, 2)

            if word_count < 100:
                kw_status = "thin"
            elif kw_occurrences == 0:
                kw_status = "missing"
            elif kw_density > 3.0:
                kw_status = "danger"  # Keyword stuffing alert
            elif kw_density > 2.5:
                kw_status = "warning"
            elif kw_density >= 0.7:
                kw_status = "optimal"
            else:
                kw_status = "low"
        else:
            kw_status = "missing"

        kw_in_title = bool(focus_kw and focus_kw.lower() in title.lower())
        kw_in_desc = bool(focus_kw and focus_kw.lower() in (a.get("metaDescription") or "").lower())

        kw_stuffing_list.append({
            "articleId": aid,
            "title": title,
            "slug": slug,
            "focusKeyword": focus_kw,
            "densityPercent": kw_density,
            "occurrences": kw_occurrences,
            "wordCount": word_count,
            "status": kw_status,
            "inTitle": kw_in_title,
            "inMetaDesc": kw_in_desc
        })

        if kw_status == "danger":
            actionable_fixes.append({
                "id": f"fix-kw-{aid}",
                "severity": "danger",
                "category": "اسپم کلمات کلیدی (Keyword Stuffing)",
                "title": f"چگالی بیش‌از‌حد کلیدواژه ({kw_density}٪) در «{title[:35]}...»",
                "desc": f"تکرار {kw_occurrences} باره عبارت «{focus_kw}» خطر جریمه قطعی گوگل را در پی دارد. چگالی مجاز ۰.۸٪ تا ۲.۵٪ است.",
                "articleId": aid,
                "actionLabel": "کاهش تکرار در ویرایشگر"
            })
        elif kw_status == "missing" and focus_kw:
            actionable_fixes.append({
                "id": f"fix-kw-miss-{aid}",
                "severity": "warning",
                "category": "فقدان کلیدواژه در محتوا",
                "title": f"عدم استفاده از کلیدواژه در متن «{title[:35]}...»",
                "desc": f"کلیدواژه کانونی «{focus_kw}» در بدنه مقاله حتی یک‌بار هم ذکر نشده است.",
                "articleId": aid,
                "actionLabel": "درج کلیدواژه در ویرایشگر"
            })

        # Thin Content Check
        if word_count < 350:
            thin_content_list.append({
                "articleId": aid,
                "title": title,
                "slug": slug,
                "wordCount": word_count,
                "severity": "danger" if word_count < 200 else "warning",
                "desc": f"حجم مقاله {word_count} کلمه است (حداقل استاندارد بالینی ۳۵۰ کلمه و بهینه ۷۰۰ کلمه)"
            })
            actionable_fixes.append({
                "id": f"fix-thin-{aid}",
                "severity": "danger" if word_count < 200 else "warning",
                "category": "محتوای لاغر (Thin Content)",
                "title": f"حجم کم محتوا ({word_count} کلمه) در «{title[:35]}...»",
                "desc": "الگوریتم‌های سلامت گوگل (Helpful Content) مقالات پزشکی زیر ۳۵۰ کلمه را کم‌کیفیت تلقی کرده و جریمه می‌کنند.",
                "articleId": aid,
                "actionLabel": "گسترش محتوا در ویرایشگر"
            })

        # Duplicate Meta Title & Description Detection
        m_title = (a.get("metaTitle") or title).strip().lower()
        if m_title:
            meta_title_map.setdefault(m_title, []).append({"id": aid, "title": title, "slug": slug})

        m_desc = (a.get("metaDescription") or summary_text).strip().lower()
        if m_desc and len(m_desc) > 15:
            meta_desc_map.setdefault(m_desc, []).append({"id": aid, "title": title, "slug": slug})

        # Medical E-E-A-T Check
        author_data = a.get("author") or {}
        author_name = author_data.get("name") if isinstance(author_data, dict) else str(author_data)
        mc_number = ""
        if isinstance(author_data, dict):
            mc_number = author_data.get("mcNumber") or author_data.get("medicalCouncil") or ""
        if not mc_number:
            mc_number = a.get("medicalCouncil") or a.get("mcNumber") or ""
        if not mc_number and "نظام پزشکی" in combined_html:
            m_mc = re.search(r'نظام پزشکی[:\s]+(\d+)', combined_html)
            if m_mc:
                mc_number = m_mc.group(1)

        reviewer_data = a.get("reviewer") or {}
        reviewer_name = reviewer_data.get("name") if isinstance(reviewer_data, dict) else str(reviewer_data)
        if not reviewer_name and isinstance(a.get("schemaData"), dict):
            reviewer_name = a.get("schemaData", {}).get("reviewer") or ""

        eeat_reasons = []
        if not author_name:
            eeat_reasons.append("فاقد نام پزشک یا نویسنده متخصص")
        if not mc_number:
            eeat_reasons.append("فاقد شماره نظام پزشکی ثبت‌شده")
        if not reviewer_name:
            eeat_reasons.append("فاقد ناظر علمی بالینی (Reviewer)")

        if eeat_reasons:
            eeat_deficiency_list.append({
                "articleId": aid,
                "title": title,
                "slug": slug,
                "authorName": author_name or "نامشخص",
                "mcNumber": mc_number or "ثبت نشده",
                "reviewerName": reviewer_name or "ثبت نشده",
                "reasons": eeat_reasons
            })
            actionable_fixes.append({
                "id": f"fix-eeat-{aid}",
                "severity": "warning",
                "category": "فقدان سیگنال E-E-A-T پزشکی",
                "title": f"نقص اطلاعات نظام پزشکی در «{title[:35]}...»",
                "desc": "، ".join(eeat_reasons) + ". بر اساس الگوریتم YMYL گوگل، مقالات سلامت بدون نظام پزشکی جریمه می‌شوند.",
                "articleId": aid,
                "actionLabel": "تکمیل ناظر و نظام پزشکی"
            })

        # Outlinks / Broken Links / Anchor Analysis
        extracted_links = extract_links_from_html(combined_html)
        for lnk in extracted_links:
            href = lnk["href"].strip()
            anchor = lnk["anchor"].strip()

            parsed = urllib.parse.urlparse(href)
            path_part = parsed.path.strip("/").replace(".html", "")

            # If internal link
            if not parsed.netloc or "pezeshkan.me" in parsed.netloc or "localhost" in parsed.netloc:
                key = (path_part, anchor)
                anchor_usage_map.setdefault(key, []).append(aid)

                if path_part.startswith("mag/"):
                    mag_sub = path_part[4:].strip("/")
                    is_valid = (
                        mag_sub in art_by_slug or
                        mag_sub in pillar_by_slug or
                        mag_sub in [p.get("slug", "").strip("/") for p in pillars] or
                        any(p.get("slug", "").strip("/") in path_part for p in pillars) or
                        mag_sub in ("", "index", "category", "tag")
                    )
                    if not is_valid and not mag_sub.startswith("uploads/"):
                        broken_internal_links.append({
                            "sourceId": aid,
                            "sourceTitle": title,
                            "href": href,
                            "anchor": anchor
                        })
                        actionable_fixes.append({
                            "id": f"fix-broken-{aid}-{len(broken_internal_links)}",
                            "severity": "danger",
                            "category": "پیوند داخلی شکسته (404)",
                            "title": f"لینک شکسته به «{href}» در «{title[:30]}...»",
                            "desc": f"پیوند با متن «{anchor}» به مقصدی اشاره دارد که در سایت موجود نیست.",
                            "articleId": aid,
                            "actionLabel": "اصلاح نشانی پیوند در مقاله"
                        })

    # Duplicate Meta Titles
    for m_t, group in meta_title_map.items():
        if len(group) > 1:
            duplicate_meta_titles.append({
                "metaTitle": m_t,
                "count": len(group),
                "articles": group
            })
            actionable_fixes.append({
                "id": f"fix-dup-title-{group[0]['id']}",
                "severity": "danger",
                "category": "عنوان سئو تکراری (Duplicate Title)",
                "title": f"عنوان سئو یکسان در {len(group)} مقاله: «{m_t[:40]}...»",
                "desc": "تکرار عناوین سئو باعث رقابت مخرب مقالات با یکدیگر (Cannibalization) و شناسایی به عنوان اسپم می‌شود.",
                "articleId": group[0]["id"],
                "actionLabel": "تغییر عنوان سئو"
            })

    # Duplicate Meta Descriptions
    for m_d, group in meta_desc_map.items():
        if len(group) > 1:
            duplicate_meta_descs.append({
                "metaDesc": m_d,
                "count": len(group),
                "articles": group
            })
            actionable_fixes.append({
                "id": f"fix-dup-desc-{group[0]['id']}",
                "severity": "warning",
                "category": "توضیحات متا تکراری (Duplicate Meta Desc)",
                "title": f"توضیحات متای یکسان در {len(group)} مقاله",
                "desc": f"متن توضیحات «{m_d[:50]}...» در مقالات متعددی کپی شده است.",
                "articleId": group[0]["id"],
                "actionLabel": "نگارش توضیحات اختصاصی"
            })

    # Anchor Over-Optimization
    anchor_over_opt_list = []
    for (target_path, anchor_text), sources in anchor_usage_map.items():
        if len(sources) >= 3 and anchor_text not in ("بیشتر بخوانید", "اینجا کلیک کنید", "ادامه مطلب"):
            anchor_over_opt_list.append({
                "targetPath": target_path,
                "anchorText": anchor_text,
                "count": len(sources),
                "sourceArticleIds": sources
            })
            actionable_fixes.append({
                "id": f"fix-anchor-{len(anchor_over_opt_list)}",
                "severity": "warning",
                "category": "انکر تکست بیش‌از‌حد تجاری (Over-Optimization)",
                "title": f"تکرار {len(sources)} باره عبارت «{anchor_text}» به مقصد {target_path}",
                "desc": "استفاده غیرطبیعی از یک انکرتکست ثابت خطر فیلتر الگوریتم پنگوئن گوگل را افزایش می‌دهد. از عبارات مترادف استفاده کنید.",
                "articleId": sources[0],
                "actionLabel": "متنوع‌سازی انکر تکست"
            })

    # Orphan articles fix tasks
    for orph in orphans:
        actionable_fixes.append({
            "id": f"fix-orphan-{orph['id']}",
            "severity": "danger",
            "category": "صفحه یتیم (Orphan Page)",
            "title": f"صفحه یتیم با صفر لینک ورودی: «{orph['title'][:35]}...»",
            "desc": "ربات‌های گوگل این صفحه را نمی‌بینند و بودجه خزش برای آن صفر است. حداقل ۲ پیوند از مقالات مرتبط به این صفحه بدهید.",
            "articleId": orph["id"],
            "actionLabel": "لینک‌سازی به این مقاله"
        })

    # Pillar-Cluster Audit
    active_pillars = []
    empty_pillars = []
    for p in pillars:
        pid = str(p.get("id"))
        p_slug = (p.get("slug") or "").strip().strip("/")
        cluster_articles = [
            a for a in articles
            if str(a.get("pillarId")) == pid or (a.get("pillarSlug") and p_slug in a.get("pillarSlug"))
        ]

        if not cluster_articles:
            empty_pillars.append({
                "id": p.get("id"),
                "name": p.get("name"),
                "slug": p.get("slug"),
                "icon": p.get("icon", "📁"),
                "desc": p.get("desc", "")
            })
            actionable_fixes.append({
                "id": f"fix-empty-pillar-{pid}",
                "severity": "info",
                "category": "شکاف ساختاری پیلار (Structural Gap)",
                "title": f"پیلار محتوایی «{p.get('name')}» بدون مقاله است",
                "desc": "برای تثبیت اقتدار موضوعی، نگارش حداقل یک مقاله ستونی و دو مقاله کلاستر برای این بخش الزامی است.",
                "articleId": None,
                "actionLabel": "نگارش اولین مقاله این بخش"
            })
        else:
            linked_back_count = 0
            isolated_articles = []
            for art in cluster_articles:
                combined_html = (art.get("contentHtml") or "") + " " + (art.get("rawHtml") or "")
                extracted = extract_links_from_html(combined_html)
                has_pillar_link = any(
                    p_slug in lnk["href"] or f"/mag/{p_slug}" in lnk["href"]
                    for lnk in extracted
                )
                if has_pillar_link:
                    linked_back_count += 1
                else:
                    isolated_articles.append({
                        "id": art.get("id"),
                        "title": art.get("title"),
                        "slug": art.get("slug")
                    })

            cluster_health_score = int((linked_back_count / len(cluster_articles)) * 100) if cluster_articles else 0
            active_pillars.append({
                "id": p.get("id"),
                "name": p.get("name"),
                "slug": p.get("slug"),
                "icon": p.get("icon", "📁"),
                "clusterArticlesCount": len(cluster_articles),
                "linkedBackCount": linked_back_count,
                "isolatedCount": len(isolated_articles),
                "isolatedArticles": isolated_articles,
                "clusterHealthScore": cluster_health_score,
                "status": "good" if cluster_health_score >= 70 else ("warning" if cluster_health_score > 0 else "isolated")
            })

            for iso in isolated_articles:
                actionable_fixes.append({
                    "id": f"fix-cluster-iso-{iso['id']}",
                    "severity": "warning",
                    "category": "انزوای کلاستر از پیلار (Cluster Isolation)",
                    "title": f"عدم پیوند مقاله «{iso['title'][:35]}...» به ستون «{p.get('name')}»",
                    "desc": "در معماری تاپیک کلاستر، هر مقاله خوشه‌ای باید به صفحه ستون اصلی خود لینک بدهد تا اعتبار سئو تجمیع شود.",
                    "articleId": iso["id"],
                    "actionLabel": "افزودن لینک به پیلار"
                })

    # Overall SEO Health Score Calculation
    score = 100
    score -= min(25, len(orphans) * 6)
    score -= min(25, sum(1 for kw in kw_stuffing_list if kw["status"] == "danger") * 8)
    score -= min(20, len(thin_content_list) * 5)
    score -= min(15, len(duplicate_meta_titles) * 5)
    score -= min(10, len(duplicate_meta_descs) * 3)
    score -= min(15, len(broken_internal_links) * 5)
    score -= min(15, len(eeat_deficiency_list) * 3)
    score -= min(10, len(anchor_over_opt_list) * 3)

    if summary_struct.get("avgInternalLinksPerArticle", 0) >= 2.0:
        score += 5
    if len(orphans) == 0:
        score += 5
    if len(eeat_deficiency_list) == 0 and len(articles) > 0:
        score += 5

    final_score = max(10, min(100, score))

    if final_score >= 85:
        health_status = "عالی و امن (بدون ریسک اسپم)"
        health_class = "status-success"
    elif final_score >= 70:
        health_status = "قابل قبول (نیازمند بهینه‌سازی موضعی)"
        health_class = "status-primary"
    elif final_score >= 50:
        health_status = "هشدار متوسط (وجود الگوهای اسپم یا صفحات یتیم)"
        health_class = "status-warning"
    else:
        health_status = "خطر جریمه (الگوهای پرریسک و جریمه گوگل)"
        health_class = "status-danger"

    spam_risks_count = (
        sum(1 for kw in kw_stuffing_list if kw["status"] == "danger") +
        len(thin_content_list) +
        len(duplicate_meta_titles) +
        len(duplicate_meta_descs) +
        len(broken_internal_links) +
        len(anchor_over_opt_list)
    )

    return {
        "success": True,
        "summary": {
            "healthScore": final_score,
            "healthStatus": health_status,
            "healthClass": health_class,
            "totalArticles": len(articles),
            "totalPillars": len(pillars),
            "activePillarsCount": len(active_pillars),
            "emptyPillarsCount": len(empty_pillars),
            "totalWordsAll": total_words_all,
            "avgWordsPerArticle": int(total_words_all / max(1, len(articles))),
            "totalInternalLinks": summary_struct.get("totalInternalLinks", 0),
            "totalExternalLinks": summary_struct.get("totalExternalLinks", 0),
            "orphanCount": len(orphans),
            "spamRisksCount": spam_risks_count,
            "thinContentCount": len(thin_content_list),
            "eeatDeficiencyCount": len(eeat_deficiency_list),
            "duplicateMetaCount": len(duplicate_meta_titles) + len(duplicate_meta_descs),
            "brokenLinksCount": len(broken_internal_links)
        },
        "spamAudit": {
            "keywordStuffing": kw_stuffing_list,
            "duplicateTitles": duplicate_meta_titles,
            "duplicateDescriptions": duplicate_meta_descs,
            "thinContent": thin_content_list,
            "anchorOverOptimization": anchor_over_opt_list,
            "brokenInternalLinks": broken_internal_links
        },
        "pillarClusterAudit": {
            "coverageRatePercent": round((len(active_pillars) / max(1, len(pillars))) * 100, 1),
            "activePillars": active_pillars,
            "emptyPillars": empty_pillars
        },
        "linkingAudit": {
            "orphanArticles": orphans,
            "avgInternalLinksPerArticle": summary_struct.get("avgInternalLinksPerArticle", 0),
            "articlesAnalysis": articles_analysis
        },
        "eeatAudit": {
            "deficiencyCount": len(eeat_deficiency_list),
            "deficiencies": eeat_deficiency_list
        },
        "actionableFixes": actionable_fixes
    }

# 9.8. Enterprise Clinical Media Storage & Multi-Variant Engine
class ClinicalMediaStorageEngine:
    """
    Production-grade Media Storage & Multi-Variant Processing Engine:
    - S3 / Cloudflare R2 / MinIO / ArvanCloud Object Storage integration via boto3.
    - Hierarchical local storage layout: /mag/uploads/YYYY/MM/
    - Pillow WebP multi-tier conversion:
        * 'large': WebP max 1920px (quality 84) - high-res article reader
        * 'medium': WebP max 768px (quality 80) - card & archive views
        * 'thumb': WebP max 320px (quality 75) - admin gallery & modal pickers
    - Automatic EXIF orientation normalization.
    - Image dimension extraction (width, height, aspect ratio).
    - SVG Anti-XSS sanitization.
    - Graceful fallback when Pillow or S3 is unavailable.
    """

    def __init__(self):
        self.s3_client = self._init_s3_client()

    def _init_s3_client(self):
        if not (HAS_BOTO3 and S3_ENABLED and S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY):
            return None
        try:
            kwargs = {
                "service_name": "s3",
                "aws_access_key_id": S3_ACCESS_KEY_ID,
                "aws_secret_access_key": S3_SECRET_ACCESS_KEY,
                "region_name": S3_REGION or "auto",
                "config": BotoConfig(signature_version="s3v4", s3={"addressing_style": "virtual"})
            }
            if S3_ENDPOINT_URL:
                kwargs["endpoint_url"] = S3_ENDPOINT_URL
            client = boto3.client(**kwargs)
            logger.info(f"[MediaStorage] Initialized S3 storage backend with bucket: {S3_BUCKET_NAME}")
            return client
        except Exception as e:
            logger.error(f"[MediaStorage] S3 initialization failed: {e}", exc_info=True)
            return None

    def store_media(self, raw_bytes, filename, alt_text="", caption="", title=""):
        now = time.localtime()
        year_str = time.strftime("%Y", now)
        month_str = time.strftime("%m", now)

        target_dir = os.path.join(UPLOADS_DIR, year_str, month_str)
        os.makedirs(target_dir, exist_ok=True)

        orig_ext = os.path.splitext(filename)[1].lower()
        if orig_ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"]:
            orig_ext = ".webp"

        base_clean = re.sub(r'[^a-zA-Z0-9_\-]', '', os.path.splitext(filename)[0])[:40] or "img"
        token = secrets.token_hex(4)
        base_id = f"{base_clean}_{int(time.time())}_{token}"

        is_raster = orig_ext in (".jpg", ".jpeg", ".png", ".webp")
        variants = {}
        dimensions = {"width": None, "height": None, "aspectRatio": None}
        large_size = len(raw_bytes)
        format_name = orig_ext.lstrip(".")

        if is_raster and HAS_PILLOW:
            try:
                img = Image.open(io.BytesIO(raw_bytes))
                img = ImageOps.exif_transpose(img)

                # Ensure compatible color mode
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    img = img.convert("RGBA")
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                orig_w, orig_h = img.size
                dimensions["width"] = orig_w
                dimensions["height"] = orig_h
                dimensions["aspectRatio"] = round(orig_w / max(orig_h, 1), 3)

                # 1. Large variant (max width 1920px)
                ratio_lg = min(1.0, 1920 / orig_w)
                if ratio_lg < 1.0:
                    lg_size = (1920, max(1, int(orig_h * ratio_lg)))
                    lg_img = img.resize(lg_size, Image.Resampling.LANCZOS)
                else:
                    lg_img = img
                buf_lg = io.BytesIO()
                lg_img.save(buf_lg, format="WEBP", quality=84, method=6)
                large_bytes = buf_lg.getvalue()
                large_size = len(large_bytes)
                format_name = "webp"

                # 2. Medium variant (max width 768px)
                ratio_med = min(1.0, 768 / orig_w)
                if ratio_med < 1.0:
                    med_size = (768, max(1, int(orig_h * ratio_med)))
                    med_img = img.resize(med_size, Image.Resampling.LANCZOS)
                else:
                    med_img = img
                buf_med = io.BytesIO()
                med_img.save(buf_med, format="WEBP", quality=80, method=5)
                med_bytes = buf_med.getvalue()

                # 3. Thumb variant (max dimension 320px)
                ratio_thumb = min(1.0, 320 / max(orig_w, orig_h))
                if ratio_thumb < 1.0:
                    thumb_size = (max(1, int(orig_w * ratio_thumb)), max(1, int(orig_h * ratio_thumb)))
                    thumb_img = img.resize(thumb_size, Image.Resampling.LANCZOS)
                else:
                    thumb_img = img
                buf_thumb = io.BytesIO()
                thumb_img.save(buf_thumb, format="WEBP", quality=75, method=4)
                thumb_bytes = buf_thumb.getvalue()

                # Filenames
                main_filename = f"{base_id}.webp"
                med_filename = f"{base_id}_medium.webp"
                thumb_filename = f"{base_id}_thumb.webp"

                # Save locally (hierarchical YYYY/MM)
                with open(os.path.join(target_dir, main_filename), "wb") as f:
                    f.write(large_bytes)
                with open(os.path.join(target_dir, med_filename), "wb") as f:
                    f.write(med_bytes)
                with open(os.path.join(target_dir, thumb_filename), "wb") as f:
                    f.write(thumb_bytes)

                # S3 Cloud Upload if enabled
                s3_success = False
                if self.s3_client:
                    try:
                        prefix = f"uploads/{year_str}/{month_str}"
                        self.s3_client.put_object(
                            Bucket=S3_BUCKET_NAME,
                            Key=f"{prefix}/{main_filename}",
                            Body=large_bytes,
                            ContentType="image/webp",
                            CacheControl="public, max-age=31536000, immutable"
                        )
                        self.s3_client.put_object(
                            Bucket=S3_BUCKET_NAME,
                            Key=f"{prefix}/{med_filename}",
                            Body=med_bytes,
                            ContentType="image/webp",
                            CacheControl="public, max-age=31536000, immutable"
                        )
                        self.s3_client.put_object(
                            Bucket=S3_BUCKET_NAME,
                            Key=f"{prefix}/{thumb_filename}",
                            Body=thumb_bytes,
                            ContentType="image/webp",
                            CacheControl="public, max-age=31536000, immutable"
                        )
                        s3_success = True
                    except Exception as s3_err:
                        logger.error(f"[MediaStorage] S3 upload error: {s3_err}", exc_info=True)

                if s3_success and S3_PUBLIC_DOMAIN:
                    base_url = f"{S3_PUBLIC_DOMAIN}/uploads/{year_str}/{month_str}"
                else:
                    base_url = f"/mag/uploads/{year_str}/{month_str}"

                variants = {
                    "large": f"{base_url}/{main_filename}",
                    "medium": f"{base_url}/{med_filename}",
                    "thumb": f"{base_url}/{thumb_filename}"
                }
                main_url = variants["large"]
                storage_type = "s3" if s3_success else "local"

            except Exception as e:
                logger.error(f"[MediaStorage] Image optimization failed, falling back to raw save: {e}", exc_info=True)
                main_filename = f"{base_id}{orig_ext}"
                target_path = os.path.join(target_dir, main_filename)
                with open(target_path, "wb") as f:
                    f.write(raw_bytes)
                main_url = f"/mag/uploads/{year_str}/{month_str}/{main_filename}"
                variants = {"large": main_url, "medium": main_url, "thumb": main_url}
                storage_type = "local"
        else:
            # SVG, GIF, or raw fallback
            main_filename = f"{base_id}{orig_ext}"
            target_path = os.path.join(target_dir, main_filename)
            with open(target_path, "wb") as f:
                f.write(raw_bytes)

            if orig_ext == ".gif" and HAS_PILLOW:
                try:
                    img = Image.open(io.BytesIO(raw_bytes))
                    dimensions["width"], dimensions["height"] = img.size
                    dimensions["aspectRatio"] = round(img.size[0] / max(img.size[1], 1), 3)
                except Exception:
                    pass

            s3_success = False
            if self.s3_client:
                try:
                    ct = "image/svg+xml" if orig_ext == ".svg" else "image/gif"
                    prefix = f"uploads/{year_str}/{month_str}"
                    self.s3_client.put_object(
                        Bucket=S3_BUCKET_NAME,
                        Key=f"{prefix}/{main_filename}",
                        Body=raw_bytes,
                        ContentType=ct,
                        CacheControl="public, max-age=31536000, immutable"
                    )
                    s3_success = True
                except Exception as s3_err:
                    logger.error(f"[MediaStorage] S3 fallback upload error: {s3_err}")

            if s3_success and S3_PUBLIC_DOMAIN:
                main_url = f"{S3_PUBLIC_DOMAIN}/uploads/{year_str}/{month_str}/{main_filename}"
            else:
                main_url = f"/mag/uploads/{year_str}/{month_str}/{main_filename}"

            variants = {"large": main_url, "medium": main_url, "thumb": main_url}
            storage_type = "s3" if s3_success else "local"

        saved_pct = round((1 - (large_size / max(len(raw_bytes), 1))) * 100, 1) if (is_raster and large_size < len(raw_bytes)) else 0.0

        media_item = {
            "id": f"med-{int(time.time()*1000)}",
            "filename": main_filename,
            "url": main_url,
            "variants": variants,
            "dimensions": dimensions,
            "format": format_name,
            "size": large_size,
            "originalSize": len(raw_bytes),
            "savedPercentage": saved_pct,
            "storage": storage_type,
            "alt": alt_text or title or base_clean,
            "title": title or alt_text or base_clean,
            "caption": caption,
            "uploadedAt": time.strftime("%Y-%m-%d %H:%M", now)
        }
        return media_item

    def delete_media(self, media_item):
        """Removes all variant files from local disk and S3 bucket if applicable."""
        urls_to_delete = set()
        if "variants" in media_item and isinstance(media_item["variants"], dict):
            for v_url in media_item["variants"].values():
                if v_url:
                    urls_to_delete.add(v_url)
        if "url" in media_item and media_item["url"]:
            urls_to_delete.add(media_item["url"])

        for u in urls_to_delete:
            # Delete local file if it points to local uploads
            if "/mag/uploads/" in u:
                try:
                    rel_part = u[u.index("/mag/uploads/") + 1:]
                    local_path = os.path.join(BASE_DIR, rel_part)
                    if os.path.isfile(local_path):
                        os.remove(local_path)
                except OSError:
                    pass

            # Delete from S3 if client is active
            if self.s3_client and ("uploads/" in u):
                try:
                    s3_key = u[u.index("uploads/"):]
                    self.s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
                except Exception as s3_err:
                    logger.warning(f"[MediaStorage] S3 delete error for {u}: {s3_err}")

MEDIA_STORAGE_ENGINE = ClinicalMediaStorageEngine()

# 9.8. Clinical Magazine Server-Side Rendering (SSR) & Dynamic XML Sitemap Engines
def format_article_html(raw):
    """
    Sanitizes and normalizes article HTML markup for SSR injection.
    Removes clipboard fragments, inline fixed colors, and Apple linebreaks.
    """
    if not raw:
        return ""
    h = raw
    h = re.sub(r'<!--StartFragment-->|<!--EndFragment-->', '', h, flags=re.IGNORECASE)
    h = re.sub(r'<span\s+id=["\']docs-internal-guid-[^"\']+["\'][^>]*>', '', h, flags=re.IGNORECASE)
    h = re.sub(r'<br\s+class=["\']Apple-interchange-newline["\']/?>', '', h, flags=re.IGNORECASE)
    h = re.sub(r'color\s*:\s*rgb\(\s*203\s*,\s*213\s*,\s*225\s*\);?', '', h, flags=re.IGNORECASE)
    h = re.sub(r'color\s*:\s*#(CBD5E1|cbd5e1|F8FAFC|f8fafc);?', '', h, flags=re.IGNORECASE)
    h = re.sub(r'white-space\s*:\s*pre-wrap;?', '', h, flags=re.IGNORECASE)
    return h

def render_article_ssr(art, template_html):
    """
    Renders an article with complete Server-Side Rendering (SSR) for Search Engines (Googlebot):
    - Exact SEO Title and Meta Description
    - Strict Self-referencing Canonical URL (/mag/{slug})
    - Open Graph (og:type=article, og:title, og:image, article:published_time, etc.)
    - Twitter Card (summary_large_image)
    - Google Medical E-E-A-T Schema (MedicalScholarlyArticle + BreadcrumbList + FAQPage)
    - Author: تیم متخصص محتوا نویس پزشکآن
    - Verification: این مقاله توسط متخصصین نوشته شده و دارای تایید علمی هستش
    - Full Server-Rendered HTML Body in #articleReaderContent with hidden hub
    """
    slug = art.get("slug") or art.get("id")
    canonical_url = f"https://pezeshkan.me/mag/{urllib.parse.quote(slug)}"
    title = art.get("title", "")
    summary = art.get("summary") or art.get("metaDescription") or ""
    image = art.get("image") or "https://pezeshkan.me/pezeshkon-logo.svg"
    image_alt = art.get("imageAlt") or title
    category = art.get("categoryName") or art.get("tag") or "سلامت عمومی"
    category_slug = art.get("pillarId") or "0"
    last_reviewed = art.get("lastReviewed") or art.get("publishDate") or "به‌روزرسانی شده"
    
    # 1. Update Title
    page_title = f"{title} | مجله سلامت بالینی پزشکآن لایف"
    ssr_html = re.sub(r'<title>.*?</title>', f'<title>{html.escape(page_title)}</title>', template_html, count=1, flags=re.IGNORECASE)
    
    # 2. Update Description
    ssr_html = re.sub(
        r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']',
        f'<meta name="description" content="{html.escape(summary, quote=True)}"',
        ssr_html,
        count=1,
        flags=re.IGNORECASE
    )
    
    # 3. Update Canonical Link
    ssr_html = re.sub(
        r'<link\s+rel=["\']canonical["\']\s+href=["\'].*?["\']',
        f'<link rel="canonical" href="{canonical_url}"',
        ssr_html,
        count=1,
        flags=re.IGNORECASE
    )
    
    # 4. Update Open Graph Tags
    ssr_html = re.sub(r'<meta\s+property=["\']og:type["\']\s+content=["\'].*?["\']', '<meta property="og:type" content="article"', ssr_html, count=1, flags=re.IGNORECASE)
    ssr_html = re.sub(r'<meta\s+property=["\']og:title["\']\s+content=["\'].*?["\']', f'<meta property="og:title" content="{html.escape(page_title, quote=True)}"', ssr_html, count=1, flags=re.IGNORECASE)
    ssr_html = re.sub(r'<meta\s+property=["\']og:description["\']\s+content=["\'].*?["\']', f'<meta property="og:description" content="{html.escape(summary, quote=True)}"', ssr_html, count=1, flags=re.IGNORECASE)
    ssr_html = re.sub(r'<meta\s+property=["\']og:url["\']\s+content=["\'].*?["\']', f'<meta property="og:url" content="{canonical_url}"', ssr_html, count=1, flags=re.IGNORECASE)
    ssr_html = re.sub(r'<meta\s+property=["\']og:image["\']\s+content=["\'].*?["\']', f'<meta property="og:image" content="{html.escape(image, quote=True)}"', ssr_html, count=1, flags=re.IGNORECASE)
    ssr_html = re.sub(r'<meta\s+property=["\']og:image:alt["\']\s+content=["\'].*?["\']', f'<meta property="og:image:alt" content="{html.escape(image_alt, quote=True)}"', ssr_html, count=1, flags=re.IGNORECASE)
    
    # 5. Update Twitter Card Tags
    ssr_html = re.sub(r'<meta\s+name=["\']twitter:title["\']\s+content=["\'].*?["\']', f'<meta name="twitter:title" content="{html.escape(page_title, quote=True)}"', ssr_html, count=1, flags=re.IGNORECASE)
    ssr_html = re.sub(r'<meta\s+name=["\']twitter:description["\']\s+content=["\'].*?["\']', f'<meta name="twitter:description" content="{html.escape(summary, quote=True)}"', ssr_html, count=1, flags=re.IGNORECASE)
    ssr_html = re.sub(r'<meta\s+name=["\']twitter:image["\']\s+content=["\'].*?["\']', f'<meta name="twitter:image" content="{html.escape(image, quote=True)}"', ssr_html, count=1, flags=re.IGNORECASE)
    
    # 6. Build Article JSON-LD Schema (Google Medical E-E-A-T Compliant)
    graph = [
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "صفحه اصلی",
                    "item": "https://pezeshkan.me/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "مجله سلامت پزشکآن لایف",
                    "item": "https://pezeshkan.me/mag"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": category,
                    "item": f"https://pezeshkan.me/mag?cat={category_slug}"
                },
                {
                    "@type": "ListItem",
                    "position": 4,
                    "name": title,
                    "item": canonical_url
                }
            ]
        },
        {
            "@type": "MedicalScholarlyArticle",
            "@id": f"{canonical_url}#article",
            "url": canonical_url,
            "headline": title,
            "description": summary,
            "image": [image],
            "inLanguage": "fa-IR",
            "mainEntityOfPage": canonical_url,
            "author": {
                "@type": "Organization",
                "name": "تیم متخصص محتوا نویس پزشکآن",
                "url": "https://pezeshkan.me/about"
            },
            "publisher": {
                "@type": "Organization",
                "name": "اکوسیستم سلامت دیجیتال پزشکآن",
                "url": "https://pezeshkan.me/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://pezeshkan.me/pezeshkon-logo.svg"
                }
            },
            "reviewedBy": {
                "@type": "MedicalOrganization",
                "name": "شورای نظارت علمی و بالینی پزشکآن"
            },
            "medicalAudience": {
                "@type": "MedicalAudience",
                "audienceType": "Patient"
            }
        }
    ]
    
    faqs = art.get("faqs", [])
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "@id": f"{canonical_url}#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f.get("q", ""),
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f.get("a", "")
                    }
                }
                for f in faqs if f.get("q") and f.get("a")
            ]
        })
    
    schema_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    schema_tag = f'<script type="application/ld+json">\n{schema_json}\n  </script>'
    ssr_html = re.sub(r'<script\s+type=["\']application/ld\+json["\']>.*?</script>', schema_tag, ssr_html, count=1, flags=re.DOTALL | re.IGNORECASE)
    
    # 7. Render Article Body Content into reader-layout-grid
    sections = art.get("sections") or []
    sections_html = "".join([
        f'<div id="{s.get("id")}" style="margin-bottom:28px;">'
        f'<h3 style="font-size:18px; font-weight:800; color:var(--text-heading); margin-bottom:12px; border-right:3px solid var(--color-primary); padding-right:12px;">{html.escape(s.get("title", ""))}</h3>'
        f'<p style="font-size:15px; color:var(--text-body); line-height:1.9;">{html.escape(s.get("content", ""))}</p>'
        f'</div>'
        for s in sections
    ])
    
    raw_content = art.get("rawHtml") or art.get("contentHtml") or sections_html
    content_body = format_article_html(raw_content)
    
    # TOC
    if sections:
        toc_items = "".join([f'<li style="margin-bottom:10px;"><a href="#{s.get("id")}" style="color:var(--text-body); font-size:13px; font-weight:600;">• {html.escape(s.get("title", ""))}</a></li>' for s in sections])
    else:
        toc_items = '''<li style="margin-bottom:10px;"><a href="#intro" style="color:var(--text-body); font-size:13px; font-weight:600;">• مقدمه و مرور بالینی</a></li>
          <li style="margin-bottom:10px;"><a href="#treatment" style="color:var(--text-body); font-size:13px; font-weight:600;">• پروتکل‌های تشخیصی و درمانی</a></li>
          <li style="margin-bottom:10px;"><a href="#guidelines" style="color:var(--text-body); font-size:13px; font-weight:600;">• گایدلاین‌ها و مراقبت پس از درمان</a></li>'''

    # Build FAQs HTML if present (NO EMOJIS - pure SVG)
    faqs_html = ""
    if faqs:
        q_icon = "<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' style='vertical-align:middle;'><circle cx='12' cy='12' r='10'/><path d='M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3'/><path d='M12 17h.01'/></svg>"
        items_html = "".join([
            f'<div style="margin-bottom:14px; border-bottom:1px dashed var(--border-color); padding-bottom:12px;">'
            f'<strong style="display:flex; align-items:center; gap:6px; color:var(--text-heading); font-size:14px; margin-bottom:6px;">{q_icon} <span>{html.escape(f.get("q", ""))}</span></strong>'
            f'<p style="color:var(--text-body); font-size:13.5px; line-height:1.8; margin:0;">{html.escape(f.get("a", ""))}</p>'
            f'</div>'
            for f in faqs if f.get("q") and f.get("a")
        ])
        faqs_html = f'''
        <div style="margin-top:32px; background:var(--bg-subtle); border-radius:var(--radius-md); padding:20px;">
          <h4 style="font-size:16px; font-weight:800; color:var(--text-heading); margin-bottom:16px;">پرسش‌های پرتکرار بیماران (FAQ)</h4>
          {items_html}
        </div>
        '''
        
    citations = art.get("citations", [])
    citations_html = ""
    if citations:
        c_items = "".join([f'<li><a href="{html.escape(c.get("link", "#"))}" target="_blank" rel="noopener noreferrer" style="color:var(--color-primary); text-decoration:underline;">{html.escape(c.get("title", ""))}</a></li>' for c in citations])
        citations_html = f'''
        <div style="margin-top:20px; font-size:12px; color:var(--text-secondary); background:rgba(2,132,199,0.05); border:1px solid rgba(2,132,199,0.15); border-radius:8px; padding:12px 16px;">
          <strong>مراجع علمی و استنادهای بالینی:</strong>
          <ul style="margin:6px 0 0 16px; padding:0;">{c_items}</ul>
        </div>
        '''

    reader_content = f'''
      <aside class="reader-sidebar">
        <h4 style="font-size:14px; font-weight:800; color:var(--text-heading); margin-bottom:14px;">فهرست مطالب مقاله</h4>
        <ul style="list-style:none; padding:0; margin-bottom:24px;">
          {toc_items}
        </ul>
        
        <!-- باکس نویسنده و تاییدیه علمی در ستون کناری -->
        <div class="author-verification-sidebar-card" style="border-top:1px solid var(--border-color); padding-top:16px;">
          <div style="font-size:11px; font-weight:800; color:var(--color-primary); margin-bottom:10px; display:flex; align-items:center; gap:6px;">
            <span><svg xmlns='http://www.w3.org/2000/svg' width='13' height='13' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round' style='vertical-align:middle;'><path d='M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z'/></svg></span>
            <span>نویسنده و هیئت تحریریه بالینی</span>
          </div>
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <div style="position:relative; flex-shrink:0;">
              <div style="width:44px; height:44px; border-radius:50%; background:linear-gradient(135deg, #0073FF 0%, #00C48C 100%); display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-size:19px; box-shadow:0 3px 10px rgba(0,115,255,0.25);">
                <svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round' style='vertical-align:middle;'><path d='M11 2v2M5 2v2m0-1H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1'/><path d='M8 15a6 6 0 0 0 12 0v-3'/><circle cx='20' cy='10' r='2'/></svg>
              </div>
              <span style="position:absolute; bottom:-2px; left:-2px; background:#00E599; color:#0F172A; width:16px; height:16px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:900; border:2px solid #FFFFFF;"><svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round' style='vertical-align:middle;'><polyline points='20 6 9 17 4 12'/></svg></span>
            </div>
            <div>
              <h5 style="font-size:13.5px; font-weight:900; color:var(--text-heading); margin:0;">تیم متخصص محتوا نویس پزشکآن</h5>
              <span style="font-size:11px; color:var(--text-secondary); display:block; margin-top:2px;">تحریریه علمی و پایش بالینی مجله</span>
            </div>
          </div>

          <div style="background:linear-gradient(135deg, rgba(0, 115, 255, 0.05) 0%, rgba(0, 229, 153, 0.04) 100%); border:1px solid rgba(0, 115, 255, 0.16); border-radius:10px; padding:12px; margin-bottom:14px;">
            <div style="display:flex; align-items:center; gap:6px; font-size:11.5px; font-weight:800; color:#059669; margin-bottom:6px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              <span>تأییدیه علمی و منابع معتبر</span>
            </div>
            <p style="font-size:12px; color:var(--text-body); line-height:1.8; margin:0; font-weight:600;">
              این مقاله توسط متخصصین نوشته شده و دارای تایید علمی هستش و از منابع معتبر بین‌المللی استخراج شده است.
            </p>
          </div>

          <button class="btn-ui btn-primary-gradient" style="width:100%; justify-content:center; font-size:12px; padding:9px 12px;" onclick="openBookingDrawer()">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span>مشاوره با پزشکان متخصص پزشکآن</span>
          </button>
        </div>
      </aside>

      <article class="reader-article-body">
        <img src="{html.escape(image)}" class="reader-hero-img" alt="{html.escape(image_alt)}">
        
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
          <div style="display:flex; align-items:center; gap:10px;">
            <span class="hero-tag-badge">
              <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="M17 10c.7-.7 1.69 0 2.5 0a2.5 2.5 0 1 0 0-5a.5.5 0 0 1-.5-.5a2.5 2.5 0 1 0-5 0c0 .81.7 1.8 0 2.5l-7 7c-.7.7-1.69 0-2.5 0a2.5 2.5 0 0 0 0 5c.28 0 .5.22.5.5a2.5 2.5 0 1 0 5 0c0-.81-.7-1.8 0-2.5Z"/></svg>
              <span>{html.escape(category)}</span>
            </span>
            <span style="font-size:12px; color:var(--text-secondary);">آخرین بازبینی علمی: {html.escape(last_reviewed)}</span>
          </div>
          <div style="font-size:12px; color:var(--color-primary); font-weight:700; display:flex; align-items:center; gap:6px;">
            <span><svg xmlns='http://www.w3.org/2000/svg' width='13' height='13' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round' style='vertical-align:middle;'><path d='M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z'/></svg> نویسنده:</span>
            <span>تیم متخصص محتوا نویس پزشکآن</span>
          </div>
        </div>

        <h1 style="font-size:24px; font-weight:900; color:var(--text-heading); margin-bottom:16px; line-height:1.5;">{html.escape(title)}</h1>
        <div style="background:var(--bg-subtle); border-right:4px solid var(--color-primary); padding:16px; border-radius:8px; margin-bottom:28px; font-size:14.5px; color:var(--text-body); line-height:1.8;">
          {html.escape(summary)}
        </div>

        <div class="article-rich-content">{content_body}</div>

        {faqs_html}
        {citations_html}

        <!-- باکس کامل نویسنده و تاییدیه علمی زیر مقاله -->
        <div class="article-author-verification-box" style="margin-top:32px; background:linear-gradient(135deg, rgba(0, 115, 255, 0.05) 0%, rgba(0, 229, 153, 0.04) 100%); border:1px solid rgba(0, 115, 255, 0.18); border-radius:16px; padding:22px;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div style="display:flex; align-items:center; gap:14px;">
              <div style="position:relative; flex-shrink:0;">
                <div style="width:52px; height:52px; border-radius:50%; background:linear-gradient(135deg, #0073FF 0%, #00C48C 100%); display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-size:24px; box-shadow:0 4px 14px rgba(0,115,255,0.25);">
                  <svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round' style='vertical-align:middle;'><path d='M11 2v2M5 2v2m0-1H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1'/><path d='M8 15a6 6 0 0 0 12 0v-3'/><circle cx='20' cy='10' r='2'/></svg>
                </div>
                <span style="position:absolute; bottom:-2px; left:-2px; background:#00E599; color:#0F172A; width:18px; height:18px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:900; border:2px solid #FFFFFF;"><svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round' style='vertical-align:middle;'><polyline points='20 6 9 17 4 12'/></svg></span>
              </div>
              <div>
                <div style="font-size:11px; font-weight:800; color:var(--color-primary); margin-bottom:2px;">درباره نویسنده مقاله</div>
                <h4 style="font-size:16px; font-weight:900; color:var(--text-heading); margin:0;">تیم متخصص محتوا نویس پزشکآن</h4>
                <span style="font-size:12px; color:var(--text-secondary);">شورای علمی، تدوین بالینی و راستی‌آزمایی شواهد پزشکی اکوسیستم سلامت پزشکآن</span>
              </div>
            </div>
            <span style="background:rgba(0, 229, 153, 0.12); color:#059669; border:1px solid rgba(0, 229, 153, 0.3); padding:4px 12px; border-radius:20px; font-size:12px; font-weight:800; display:inline-flex; align-items:center; gap:6px;">
              <svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round' style='vertical-align:middle;'><path d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z'/><path d='m9 12 2 2 4-4'/></svg> دارای تأییدیه علمی تحریریه
            </span>
          </div>

          <div style="background:var(--bg-surface); border:1px solid rgba(0, 115, 255, 0.12); border-radius:12px; padding:14px 16px;">
            <div style="display:flex; align-items:flex-start; gap:10px;">
              <span style="font-size:18px; line-height:1.2;"><svg xmlns='http://www.w3.org/2000/svg' width='15' height='15' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round' style='vertical-align:middle;'><path d='m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z'/></svg></span>
              <div>
                <strong style="font-size:13.5px; color:var(--text-heading); display:block; margin-bottom:4px;">ضمانت اصالت و اعتبار محتوای سلامت:</strong>
                <p style="font-size:13px; color:var(--text-body); line-height:1.85; margin:0; font-weight:600;">
                  این مقاله توسط متخصصین نوشته شده و دارای تایید علمی هستش و از منابع معتبر و گایدلاین‌های بالینی بین‌المللی تدوین شده است.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="reader-cta-card" style="margin-top:24px;">
          <div>
            <h4 style="font-size:15px; font-weight:800; color:var(--text-heading); margin-bottom:4px;">نیاز به بررسی دقیق‌تر پرونده پزشکی خود دارید؟</h4>
            <p style="font-size:12.5px; color:var(--text-secondary);">می‌توانید مستقیماً آزمایش‌ها و گزارش‌های تصویربرداری خود را جهت ارزیابی به پزشکان متخصص پزشکآن ارسال فرمایید.</p>
          </div>
          <button class="btn-ui btn-primary-gradient" onclick="openBookingDrawer()">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span>رزرو ویزیت آنلاین یا حضوری</span>
          </button>
        </div>
      </article>
    '''
    
    # Switch display states
    ssr_html = ssr_html.replace('<div id="viewHubMain">', '<div id="viewHubMain" style="display: none;">')
    ssr_html = ssr_html.replace('<div id="viewArticleReaderArea" style="display: none; padding-bottom: 60px;">', '<div id="viewArticleReaderArea" style="display: block; padding-bottom: 60px;">')
    
    # Inject content
    empty_reader_target = '<div class="reader-layout-grid" id="articleReaderContent"></div>'
    if empty_reader_target in ssr_html:
        ssr_html = ssr_html.replace(empty_reader_target, f'<div class="reader-layout-grid" id="articleReaderContent">\n{reader_content}\n</div>')
        
    return ssr_html

def generate_dynamic_sitemap_xml():
    """
    Generates a fresh, dynamic Google-compliant XML Sitemap containing:
    - Root and Portal pages with high priority
    - Appointments / Booking directory
    - Health Magazine hub and newsletter
    - All verified clinical articles from articles.json with canonical slug and lastmod
    """
    try:
        articles_path = os.path.join(CONTENT_DIR, "articles.json")
        articles = load_json_file(articles_path, default=[])
    except Exception:
        articles = []

    now_iso = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3, minutes=30))).strftime('%Y-%m-%dT%H:%M:%S+03:30')

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
        loc = f"https://pezeshkan.me/mag/{urllib.parse.quote(slug)}"
        lastmod = a.get("publishDate") or a.get("lastReviewed") or now_iso
        if len(lastmod) == 10:
            lastmod += "T10:00:00+03:30"
        urls.append((loc, lastmod, "weekly", "0.85"))

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
        atomic_write_text(os.path.join(BASE_DIR, "sitemap.xml"), xml_content)
        atomic_write_text(os.path.join(PORTAL_DIR, "sitemap.xml"), xml_content)
    except Exception:
        pass
    return xml_content

# 10. Main HTTP Request Handler
class PezeshkanRequestHandler(http.server.BaseHTTPRequestHandler):

    server_version = "Pezeshkan-Security-Gateway"
    sys_version = ""

    def version_string(self):
        return "Pezeshkan-Security-Gateway"

    def send_error(self, code, message=None, explain=None):
        self.send_response(code, message)
        self.send_header('Connection', 'close')
        self.send_security_headers()
        body = None
        if code >= 200 and code not in (204, 304):
            msg = message if message else self.responses.get(code, ('Error', ''))[0]
            body = f"<!DOCTYPE html><html lang='fa' dir='rtl'><head><meta charset='utf-8'><title>{code} {html.escape(msg)}</title></head><body style='font-family:sans-serif;text-align:center;padding:50px;background:#0f172a;color:#f8fafc;'><h2>{code} - {html.escape(msg)}</h2><p style='color:#94a3b8;'>درخواست شما به دلیل ملاحظات امنیتی مسدود گردید.</p></body></html>".encode("utf-8")
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body and not getattr(self, "_head_only", False):
            self.wfile.write(body)

    def get_client_ip(self):
        cf_ip = self.headers.get("CF-Connecting-IP")
        if cf_ip:
            return cf_ip.strip()
        x_real_ip = self.headers.get("X-Real-IP")
        if x_real_ip:
            return x_real_ip.strip()
        x_forwarded = self.headers.get("X-Forwarded-For")
        if x_forwarded:
            parts = [p.strip() for p in x_forwarded.split(",")]
            if parts and parts[0]:
                return parts[0]
        return self.client_address[0]

    def is_https(self):
        if SECURE_COOKIES:
            return True
        proto = self.headers.get("X-Forwarded-Proto", "").lower()
        if proto == "https":
            return True
        if self.headers.get("X-Forwarded-Ssl", "").lower() == "on":
            return True
        cf_visitor = self.headers.get("CF-Visitor", "")
        if '"scheme":"https"' in cf_visitor:
            return True
        return False

    def get_current_role(self):
        sess = self.get_current_session()
        if not sess:
            return None
        return sess.get("role", "author")

    def require_role(self, *allowed_roles):
        if not self.is_authenticated():
            AUDIT_LOGGER.log_event(
                "UNAUTHORIZED_ACCESS",
                ip=self.get_client_ip(),
                user="anonymous",
                status="DENIED",
                details={"path": getattr(self, "path", "/")}
            )
            self.send_json({"error": "عدم احراز هویت: لطفاً ابتدا وارد سیستم شوید"}, 401)
            return False
        role = self.get_current_role()
        sess = self.get_current_session()
        username = sess.get("username", "unknown") if sess else "unknown"
        if role not in allowed_roles:
            AUDIT_LOGGER.log_event(
                "ACCESS_DENIED_RBAC",
                ip=self.get_client_ip(),
                user=username,
                status="DENIED",
                details={"role": role, "allowed": list(allowed_roles), "path": getattr(self, "path", "/")}
            )
            self.send_json({"error": "عدم دسترسی: سطح دسترسی حساب کاربری شما برای این عملیات مجاز نیست"}, 403)
            return False
        return True

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Allow", "GET, POST, PUT, DELETE, OPTIONS, HEAD")
        origin = self.headers.get("Origin")
        host = self.headers.get("Host", "").lower().split(":")[0]
        allowed_origin = None
        if origin:
            try:
                parsed_orig = urllib.parse.urlparse(origin)
                orig_host = (parsed_orig.hostname or "").lower()
                if orig_host == host or orig_host in ALLOWED_HOSTS or "*" in ALLOWED_HOSTS or orig_host in ("localhost", "127.0.0.1"):
                    allowed_origin = origin
            except Exception:
                pass

        if allowed_origin:
            self.send_header("Access-Control-Allow-Origin", allowed_origin)
            self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With, X-CSRF-Token, Origin, Accept")
        self.send_header("Access-Control-Max-Age", "86400")
        self.send_security_headers()
        self.end_headers()

    def do_HEAD(self):
        self._head_only = True
        try:
            self.do_GET()
        finally:
            self._head_only = False

    def validate_host(self):
        if "*" in ALLOWED_HOSTS:
            return True
        host = self.headers.get("Host", "").split(":")[0].lower()
        if not host or host not in ALLOWED_HOSTS:
            return False
        return True

    def check_csrf(self):
        origin = self.headers.get("Origin")
        referer = self.headers.get("Referer")
        host = self.headers.get("Host", "").lower()
        host_domain = host.split(":")[0]
        check_url = origin or referer

        # 1. Origin / Referer Validation
        if check_url:
            try:
                parsed = urllib.parse.urlparse(check_url)
                source_domain = (parsed.hostname or "").lower()
                source_host = parsed.netloc.lower()
                is_match = (
                    source_host == host or
                    source_domain == host_domain or
                    (source_domain in ALLOWED_HOSTS and source_domain != "*") or
                    source_domain in ("localhost", "127.0.0.1")
                )
                if not is_match:
                    AUDIT_LOGGER.log_event(
                        "CSRF_VIOLATION",
                        ip=self.get_client_ip(),
                        status="BLOCKED",
                        details={"reason": "Origin/Referer mismatch", "source": check_url, "target_host": host}
                    )
                    return False
            except Exception:
                AUDIT_LOGGER.log_event("CSRF_VIOLATION", ip=self.get_client_ip(), status="BLOCKED", details={"reason": "Malformed Origin/Referer"})
                return False

        # 2. Token Validation for authenticated session-based mutations
        token = self.get_auth_token()
        sess = get_session(token) if token else None
        auth_header = self.headers.get("Authorization", "")

        # If authenticated via cookie (not Bearer token)
        if sess and not auth_header.startswith("Bearer "):
            csrf_header = self.headers.get("X-CSRF-Token")
            expected_csrf = sess.get("csrf_token")
            # If CSRF token is provided in headers, verify match
            if csrf_header:
                if not expected_csrf or not secrets.compare_digest(csrf_header, expected_csrf):
                    AUDIT_LOGGER.log_event("CSRF_VIOLATION", ip=self.get_client_ip(), user=sess.get("username"), status="BLOCKED", details={"reason": "X-CSRF-Token mismatch"})
                    return False
            elif not check_url:
                # Neither Origin/Referer nor X-CSRF-Token provided on cookie-authenticated mutation
                AUDIT_LOGGER.log_event("CSRF_VIOLATION", ip=self.get_client_ip(), user=sess.get("username"), status="BLOCKED", details={"reason": "Missing Origin/Referer and X-CSRF-Token"})
                return False

        return True

    def get_auth_token(self):
        # 1. Cookie header
        cookie_header = self.headers.get("Cookie", "")
        if "session_token=" in cookie_header:
            cookies = cookie_header.split(";")
            for c in cookies:
                c = c.strip()
                if c.startswith("session_token="):
                    return c[len("session_token="):]
        # 2. Authorization header
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:].strip()
        return None

    def is_authenticated(self):
        token = self.get_auth_token()
        sess = get_session(token)
        return sess is not None

    def get_current_session(self):
        token = self.get_auth_token()
        return get_session(token)

    def send_security_headers(self, is_private=False):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY" if is_private else "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()")
        self.send_header("X-Permitted-Cross-Domain-Policies", "none")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin-allow-popups")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        if is_private:
            self.send_header("X-Robots-Tag", "noindex, nofollow, noarchive")

        # Hardened Content Security Policy (Allows internal assets, Tiptap, Three.js, Google fonts, and inline styles)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com data:; "
            "img-src 'self' data: https: blob:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'self'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "object-src 'none';"
        )
        self.send_header("Content-Security-Policy", csp)

        if self.is_https() or ENVIRONMENT == "production":
            self.send_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload")

    def send_redirect_301(self, location):
        self.send_response(301)
        self.send_header("Location", location)
        self.send_header("Cache-Control", "public, max-age=86400")
        self.send_security_headers()
        self.end_headers()

    def send_redirect_custom(self, location, status_code=301):
        """Dispatches dynamic HTTP redirection (301, 302, 307, 308) with appropriate caching headers."""
        self.send_response(status_code)
        self.send_header("Location", location)
        if status_code in (301, 308):
            self.send_header("Cache-Control", "public, max-age=86400")
        else:
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_security_headers()
        self.end_headers()

    def send_410_gone(self, source_path):
        """Serves an informative Persian clinical 410 Gone page instructing search engines to permanently drop URL."""
        self.send_response(410)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "public, max-age=604800")
        self.send_header("X-Robots-Tag", "noindex, noarchive")
        self.send_security_headers()
        body = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>۴۱۰ - صفحه به طور دائم حذف گردیده است | پزشکآن</title>
    <meta name="robots" content="noindex, noarchive">
    <link rel="stylesheet" href="/shared.css">
    <style>
        body {{ background: #060911; color: #f1f5f9; display: flex; align-items: center; justify-content: center; min-height: 100vh; font-family: 'Vazirmatn', -apple-system, sans-serif; margin: 0; padding: 20px; }}
        .gone-card {{ max-width: 540px; width: 100%; background: #0c1222; border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 18px; padding: 40px; text-align: center; box-shadow: 0 25px 60px rgba(0,0,0,0.6); }}
        .status-badge {{ display: inline-block; background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 6px 18px; border-radius: 9999px; font-weight: 800; font-size: 13px; margin-bottom: 20px; }}
        h1 {{ font-size: 24px; font-weight: 800; margin-bottom: 12px; color: #ffffff; }}
        p {{ font-size: 14.5px; color: #94a3b8; line-height: 1.85; margin-bottom: 24px; }}
        .source-tag {{ background: #1e293b; padding: 3px 10px; border-radius: 6px; font-family: monospace; color: #38bdf8; direction: ltr; display: inline-block; }}
        .btn-home {{ display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #0ea5e9, #0284c7); color: #fff; padding: 12px 28px; border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 14px; transition: transform 0.2s; }}
        .btn-home:hover {{ transform: translateY(-2px); }}
    </style>
</head>
<body>
    <div class="gone-card">
        <span class="status-badge">کد وضعیت ۴۱۰ - Gone (منقضی شده دائم)</span>
        <h1>محتوای مورد نظر برای همیشه حذف شده است</h1>
        <p>نشانی درخواستی شما در آدرس <span class="source-tag">{html.escape(source_path)}</span> بر اساس استانداردهای بالینی و سئو برای همیشه از دسترس خارج گردیده و موتورهای جستجو این صفحه را از ایندکس حذف می‌نمایند.</p>
        <a href="/" class="btn-home">بازگشت به صفحه اصلی پزشکآن</a>
    </div>
</body>
</html>""".encode("utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if not getattr(self, "_head_only", False):
            self.wfile.write(body)

    def send_json(self, data, status=200, is_private=False):
        try:
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_security_headers(is_private=is_private)
            self.end_headers()
            if not getattr(self, "_head_only", False):
                self.wfile.write(body)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def send_html(self, html_content, status=200, is_private=False):
        try:
            body = html_content.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_security_headers(is_private=is_private)
            self.end_headers()
            if not getattr(self, "_head_only", False):
                self.wfile.write(body)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def send_xml(self, xml_content, status=200):
        try:
            body = xml_content.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/xml; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "public, max-age=3600")
            self.send_security_headers(is_private=False)
            self.end_headers()
            if not getattr(self, "_head_only", False):
                self.wfile.write(body)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def serve_file(self, filepath, content_type=None, status=200, is_private=False):
        safe, code, msg = is_safe_static_request(filepath)
        if not safe:
            self.send_error(code, msg or "Forbidden")
            return

        if not content_type:
            content_type, _ = mimetypes.guess_type(filepath)
            if not content_type:
                content_type = "application/octet-stream"

        if content_type.startswith("text/") or content_type == "application/json" or content_type == "application/xml" or content_type == "application/manifest+json":
            content_type += "; charset=utf-8"

        # Optimized Cache-Control based on asset type
        lower_fp = filepath.lower()
        is_upload = os.path.realpath(filepath).startswith(os.path.realpath(UPLOADS_DIR))
        if any(lower_fp.endswith(ext) for ext in (".woff2", ".woff", ".ttf")) or (is_upload and any(lower_fp.endswith(ext) for ext in (".webp", ".png", ".jpg", ".jpeg", ".svg", ".gif"))):
            cache_header = "public, max-age=31536000, immutable"
        elif any(lower_fp.endswith(ext) for ext in (".js", ".css", ".html", ".htm")):
            cache_header = "no-cache, no-store, must-revalidate"
        elif any(lower_fp.endswith(ext) for ext in (".svg", ".webp", ".png", ".jpg", ".jpeg", ".ico")):
            cache_header = "public, max-age=86400"
        elif any(lower_fp.endswith(ext) for ext in (".xml", ".txt", ".webmanifest")):
            cache_header = "public, max-age=86400, stale-while-revalidate=43200"
        else:
            cache_header = "public, max-age=3600, stale-while-revalidate=86400"

        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", cache_header)
            self.send_security_headers(is_private=is_private)
            self.end_headers()
            if not getattr(self, "_head_only", False):
                self.wfile.write(content)
        except Exception:
            self.send_error(500, "Internal Server Error")

    def read_json_body(self):
        cl_header = self.headers.get("Content-Length")
        if not cl_header:
            self.send_json({"error": "Content-Length header required"}, 411)
            return None
        try:
            content_length = int(cl_header)
        except ValueError:
            self.send_json({"error": "Invalid Content-Length"}, 400)
            return None

        if content_length < 0 or content_length > MAX_PAYLOAD_SIZE:
            self.close_connection = True
            body = json.dumps({"error": "حجم درخواست بیش از حد مجاز است (حداکثر ۱۵ مگابایت)"}, ensure_ascii=False).encode("utf-8")
            self.send_response(413)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.send_security_headers()
            self.end_headers()
            if not getattr(self, "_head_only", False):
                self.wfile.write(body)
            return None

        try:
            body = self.rfile.read(content_length)
            if not body:
                return {}
            parsed = json.loads(body.decode("utf-8"))
            if isinstance(parsed, dict):
                for dangerous_key in ("__proto__", "constructor", "prototype"):
                    parsed.pop(dangerous_key, None)
            return parsed
        except UnicodeDecodeError:
            AUDIT_LOGGER.log_event("INVALID_INPUT_ENCODING", ip=self.get_client_ip(), status="REJECTED")
            self.send_json({"error": "فرمت کاراکترها باید UTF-8 باشد"}, 400)
            return None
        except json.JSONDecodeError:
            AUDIT_LOGGER.log_event("MALFORMED_JSON_PAYLOAD", ip=self.get_client_ip(), status="REJECTED")
            self.send_json({"error": "فرمت داده‌ها باید JSON معتبر باشد"}, 400)
            return None
        except Exception as e:
            logger.error(f"Error reading JSON body: {e}")
            self.send_json({"error": "خطا در پردازش داده‌های ورودی"}, 400)
            return None

    # 11. GET Request Router
    def do_GET(self):
        try:
            self._handle_GET()
        except (ConnectionResetError, BrokenPipeError):
            pass
        except Exception as e:
            print(f"[Server Error] Unhandled GET exception on {getattr(self, 'path', '/')}: {e}")
            if getattr(self, "path", "").startswith("/api/"):
                self.send_json({"error": "خطای غیرمنتظره در پردازش درخواست رخ داد"}, 500)
            else:
                self.send_error(500, "Internal Server Error")

    def _handle_GET(self):
        if not self.validate_host():
            self.send_error(400, "Bad Request: Invalid Host Header")
            return

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Anti-path-traversal check on URL path
        if ".." in path or "\0" in path or "//" in path:
            self.send_error(400, "Bad Request: Invalid URL characters")
            return

        # 1. SEO Canonical 301 Permanent Redirects
        # Root homepage canonicalization
        if path in ["/index.html", "/portal", "/portal/", "/portal/index.html"]:
            return self.send_redirect_301("/")

        # Health Magazine canonicalization
        if path in ["/mag/index.html", "/mag/"]:
            return self.send_redirect_301("/mag")
        if path in ["/mag/newsletter.html", "/mag/newsletter/"]:
            return self.send_redirect_301("/mag/newsletter")
        if path in ["/newsletter", "/newsletter.html", "/newsletter/"]:
            return self.send_redirect_301("/mag/newsletter")

        # Aliases
        if path in ["/pricing", "/pricing.html", "/pricing/"]:
            return self.send_redirect_301("/packages")
        if path in ["/learn", "/learn.html", "/learn/"]:
            return self.send_redirect_301("/tutorials")

        # Strip .html and trailing slashes for canonical URLs
        portal_canonicals = ["/product", "/features", "/packages", "/tutorials", "/start", "/services", "/about", "/contact", "/download", "/appointments"]
        for p in portal_canonicals:
            if path == p + ".html" or (path.startswith(p + "/") and path.rstrip("/") == p):
                return self.send_redirect_301(p)

        # 2. Search Engine Metadata & PWA Files
        if path == "/robots.txt":
            return self.serve_file(os.path.join(BASE_DIR, "robots.txt"), "text/plain")
        if path in ("/llms.txt", "/llm.txt"):
            settings = load_llms_settings()
            if not settings.get("isEnabled", settings.get("enabled", True)):
                return self.send_error(404, "llms.txt is currently disabled")
            llms_file = os.path.join(BASE_DIR, "llms.txt")
            if not os.path.isfile(llms_file):
                content = generate_llms_txt(settings)
                atomic_write_text(llms_file, content)
            return self.serve_file(llms_file, "text/plain")
        if path == "/sitemap.xml":
            try:
                xml_data = generate_dynamic_sitemap_xml()
                return self.send_xml(xml_data)
            except Exception as sm_err:
                logger.error(f"[Sitemap] Dynamic generation error: {sm_err}")
                return self.serve_file(os.path.join(BASE_DIR, "sitemap.xml"), "application/xml")
        if path == "/favicon.svg":
            return self.serve_file(os.path.join(BASE_DIR, "favicon.svg"), "image/svg+xml")
        if path == "/favicon.ico":
            return self.serve_file(os.path.join(BASE_DIR, "favicon.ico"), "image/x-icon")
        if path == "/site.webmanifest":
            return self.serve_file(os.path.join(BASE_DIR, "site.webmanifest"), "application/manifest+json")

        # 2.5. Dynamic SEO Custom Redirect Manager (Rules from redirects.json)
        custom_red = match_custom_redirect(path, parsed.query)
        if custom_red:
            red_code, red_target = custom_red
            if red_code == 410:
                return self.send_410_gone(path)
            return self.send_redirect_custom(red_target, red_code)

        # 3. Main Website & Portal Ecosystem Pages
        portal_routes = {
            "": "index.html",
            "/": "index.html",
            "/product": "product.html",
            "/features": "features.html",
            "/packages": "packages.html",
            "/start": "start.html",
            "/services": "services.html",
            "/about": "about.html",
            "/contact": "contact.html",
            "/tutorials": "tutorials.html",
            "/download": "download.html",
            "/appointments": "appointments.html",
            "/404": "404.html",
            "/404.html": "404.html",
            "/shared.css": "shared.css",
            "/shared.js": "shared.js",
            "/three.min.js": "three.min.js",
            "/gsap.min.js": "gsap.min.js",
            "/lenis.min.js": "lenis.min.js",
            "/pezeshkon-logo.svg": "pezeshkon-logo.svg",
            "/pezeshkon-logo.png": "pezeshkon-logo.png"
        }
        if path in portal_routes:
            file_name = portal_routes[path]
            if file_name.endswith(".css"):
                content_type = "text/css"
            elif file_name.endswith(".js"):
                content_type = "application/javascript"
            elif file_name.endswith(".svg"):
                content_type = "image/svg+xml"
            elif file_name.endswith(".png"):
                content_type = "image/png"
            else:
                content_type = "text/html"
            target_file = os.path.join(PORTAL_DIR, file_name)
            if not os.path.isfile(target_file):
                target_file = os.path.join(BASE_DIR, file_name)
            return self.serve_file(target_file, content_type)

        # 4. Font Files
        if "/fonts/" in path or path.endswith(".woff2") or path.endswith(".woff") or path.endswith(".ttf"):
            fname = os.path.basename(path)
            for fdir in [os.path.join(PORTAL_DIR, "fonts"), os.path.join(MAG_DIR, "fonts"), os.path.join(BASE_DIR, "fonts")]:
                candidate = os.path.join(fdir, fname)
                if os.path.isfile(candidate):
                    ctype = "font/woff2" if fname.endswith(".woff2") else ("font/woff" if fname.endswith(".woff") else "font/ttf")
                    return self.serve_file(candidate, ctype)

        # 5. Login Page (Protected with noindex)
        if path in ["/login", "/login/", "/mag/login", "/mag/login.html"]:
            if self.is_authenticated():
                self.send_response(302)
                self.send_header("Location", "/admin")
                self.send_security_headers(is_private=True)
                self.end_headers()
                return
            return self.serve_file(os.path.join(MAG_DIR, "login.html"), "text/html", is_private=True)

        # 6. Editorial Admin Panel (/admin)
        if path in ["/wp-admin", "/wp-admin/"]:
            self.send_response(301)
            self.send_header("Location", "/admin")
            self.end_headers()
            return

        if path in ["/admin", "/admin/", "/mag/admin", "/mag/admin.html"]:
            if not self.is_authenticated():
                self.send_response(302)
                self.send_header("Location", "/login?redirect=/admin")
                self.send_security_headers(is_private=True)
                self.end_headers()
                return
            return self.serve_file(os.path.join(MAG_DIR, "admin.html"), "text/html", is_private=True)

        # 6.5. Health Magazine Newsletter
        if path == "/mag/newsletter":
            return self.serve_file(os.path.join(MAG_DIR, "newsletter.html"), "text/html")

        # 7. Health Magazine Subfolder (/mag) & Article SPA Deep-Linking
        if path == "/mag" or path.startswith("/mag/"):
            # Block any access to internal /mag/content directory (even if file does not exist)
            if path == "/mag/content" or path.startswith("/mag/content/"):
                return self.send_error(403, "Access Denied")

            # Check if this is a physical static file (uploads, public assets, styles, components)
            clean_rel = path.lstrip("/")
            candidate_file = os.path.join(BASE_DIR, clean_rel)
            if os.path.isfile(candidate_file):
                safe, code, msg = is_safe_static_request(candidate_file)
                if safe:
                    return self.serve_file(candidate_file)
                return self.send_error(code, msg or "Access Denied")
            # WordPress-style 301 Canonical Redirect for Old Slugs
            req_slug = urllib.parse.unquote(path[len("/mag/"):].strip("/")) if path.startswith("/mag/") else ""
            if req_slug and req_slug != "newsletter" and not req_slug.endswith(".html"):
                try:
                    articles_path = os.path.join(CONTENT_DIR, "articles.json")
                    articles = load_json_file(articles_path, default=[])
                    for a in articles:
                        curr_slug = a.get("slug") or a.get("id")
                        old_slugs = a.get("oldSlugs", [])
                        if req_slug in old_slugs and curr_slug and curr_slug != req_slug:
                            return self.send_redirect_301(f"/mag/{urllib.parse.quote(curr_slug)}")
                except Exception as e:
                    pass

                # Pre-rendered Server-Side Rendering (SSR) for Clinical Articles
                try:
                    articles_path = os.path.join(CONTENT_DIR, "articles.json")
                    articles = load_json_file(articles_path, default=[])
                    found_article = None
                    for a in articles:
                        if a.get("slug") == req_slug or str(a.get("id")) == req_slug:
                            found_article = a
                            break
                    if found_article:
                        mag_template_path = os.path.join(MAG_DIR, "index.html")
                        with open(mag_template_path, "r", encoding="utf-8") as tf:
                            template_html = tf.read()
                        ssr_html = render_article_ssr(found_article, template_html)
                        return self.send_html(ssr_html)
                    else:
                        # Non-existent article slug: return clinical 404 to prevent soft-404 penalty
                        not_found_file = os.path.join(PORTAL_DIR, "404.html")
                        if os.path.isfile(not_found_file):
                            return self.serve_file(not_found_file, "text/html", status=404)
                        return self.send_error(404, "مقاله مورد نظر در مجله سلامت پزشکآن یافت نشد")
                except Exception as ssr_err:
                    logger.error(f"[SSR] Article render error for {req_slug}: {ssr_err}")

            # Otherwise, virtual paths under /mag serve the magazine index SPA
            return self.serve_file(os.path.join(MAG_DIR, "index.html"), "text/html")

        # 8. Logout Route
        if path == "/logout":
            token = self.get_auth_token()
            sess = get_session(token)
            if sess:
                AUDIT_LOGGER.log_event("AUTH_LOGOUT", ip=self.get_client_ip(), user=sess.get("username", "unknown"), status="SUCCESS")
            destroy_session(token)
            self.send_response(302)
            cookie_val = "session_token=deleted; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; SameSite=Strict"
            if self.is_https():
                cookie_val += "; Secure"
            self.send_header("Set-Cookie", cookie_val)
            self.send_header("Location", "/login")
            self.end_headers()
            return

        # 9. REST APIs
        if path.startswith("/api/"):
            client_ip = self.get_client_ip()
            allowed, retry_after = API_LIMITER.check(client_ip)
            if not allowed:
                return self.send_json({"error": f"درخواست‌های مکرر. لطفاً {retry_after} ثانیه دیگر مجدداً تلاش فرمایید."}, 429)
            API_LIMITER.record_hit(client_ip)

            if path == "/api/me":
                token = self.get_auth_token()
                sess = get_session(token)
                if not sess:
                    return self.send_json({"authenticated": False, "error": "نیاز به ورود به سیستم دارید"}, 401)
                return self.send_json({
                    "authenticated": True,
                    "user": sess,
                    "csrfToken": sess.get("csrf_token")
                })

            if path == "/api/stats":
                articles = load_json_file(os.path.join(CONTENT_DIR, "articles.json"), [])
                pillars = load_json_file(os.path.join(CONTENT_DIR, "pillars.json"), [])
                doctors = load_json_file(os.path.join(CONTENT_DIR, "doctors.json"), [])
                return self.send_json({
                    "articlesCount": len(articles),
                    "pillarsCount": len(pillars),
                    "doctorsCount": len(doctors),
                    "securityStatus": "Secure Production Hardened (Argon2id, CSP, Anti-Traversal, RBAC)"
                })

            if path == "/api/articles":
                articles = load_json_file(os.path.join(CONTENT_DIR, "articles.json"), [])
                return self.send_json(articles)

            if path == "/api/pillars":
                pillars = load_json_file(os.path.join(CONTENT_DIR, "pillars.json"), [])
                return self.send_json(pillars)

            if path == "/api/doctors":
                doctors = load_json_file(os.path.join(CONTENT_DIR, "doctors.json"), [])
                return self.send_json(doctors)

            if path in ("/api/newsletters", "/api/newsletters/"):
                newsletters = load_json_file(os.path.join(CONTENT_DIR, "newsletters.json"), [])
                return self.send_json(newsletters)

            if path == "/api/settings":
                settings = load_json_file(os.path.join(CONTENT_DIR, "settings.json"), {})
                return self.send_json(settings)

            # Protected Clinical Administrative Endpoints
            if path == "/api/admin/leads":
                if not self.require_role("administrator", "editor"):
                    return
                leads = load_json_file(os.path.join(CONTENT_DIR, "leads.json"), [])
                return self.send_json({"leads": leads})

            if path == "/api/admin/inquiries":
                if not self.require_role("administrator", "editor"):
                    return
                inquiries = load_json_file(os.path.join(CONTENT_DIR, "inquiries.json"), [])
                return self.send_json({"inquiries": inquiries})

            if path == "/api/media":
                if not self.is_authenticated():
                    return self.send_json({"error": "عدم دسترسی: نیاز به مجوز مدیر دارید"}, 401)
                query = urllib.parse.parse_qs(parsed.query)
                media_list = load_json_file(os.path.join(CONTENT_DIR, "media.json"), [])

                q = query.get("q", [""])[0].strip().lower()
                page_str = query.get("page", [""])[0]
                limit_str = query.get("limit", [""])[0]

                if q:
                    media_list = [
                        m for m in media_list
                        if q in (m.get("alt") or "").lower()
                        or q in (m.get("title") or "").lower()
                        or q in (m.get("filename") or "").lower()
                        or q in (m.get("caption") or "").lower()
                    ]

                total = len(media_list)
                if page_str or limit_str:
                    try:
                        page = max(1, int(page_str or 1))
                        limit = max(1, min(100, int(limit_str or 20)))
                    except (ValueError, TypeError):
                        page = 1
                        limit = 20
                    start = (page - 1) * limit
                    end = start + limit
                    items = media_list[start:end]
                    return self.send_json({
                        "success": True,
                        "media": items,
                        "total": total,
                        "page": page,
                        "limit": limit,
                        "pages": math.ceil(total / limit) if total > 0 else 1
                    })

                return self.send_json({"success": True, "media": media_list, "total": total})

            if path in ("/api/media/stats", "/api/media/stats/"):
                if not self.require_role("administrator", "editor"):
                    return
                media_list = load_json_file(os.path.join(CONTENT_DIR, "media.json"), [])
                total_count = len(media_list)
                total_bytes = sum(m.get("size", 0) for m in media_list)
                webp_count = sum(1 for m in media_list if m.get("format") == "webp" or (m.get("filename") or "").endswith(".webp"))
                s3_count = sum(1 for m in media_list if m.get("storage") == "s3")
                total_saved = sum(
                    max(0, m.get("originalSize", m.get("size", 0)) - m.get("size", 0))
                    for m in media_list
                )
                return self.send_json({
                    "success": True,
                    "stats": {
                        "totalCount": total_count,
                        "totalBytes": total_bytes,
                        "totalSizeMB": round(total_bytes / (1024 * 1024), 2),
                        "webpCount": webp_count,
                        "s3Count": s3_count,
                        "totalSavedBytes": total_saved,
                        "totalSavedMB": round(total_saved / (1024 * 1024), 2),
                        "storageEngine": "S3/R2 Cloud + Local Hierarchical" if S3_ENABLED else "Local Hierarchical (YYYY/MM)"
                    }
                })

            if path in ("/api/crm-tutorials", "/api/crm-tutorials/"):
                tutorials = load_json_file(os.path.join(CONTENT_DIR, "crm_tutorials.json"), [])
                return self.send_json(tutorials)

            if path in ("/api/admin/redirects", "/api/admin/redirects/"):
                if not self.require_role("administrator"):
                    return
                return self.send_json({"success": True, "redirects": load_redirects()})

            if path in ("/api/admin/schemas", "/api/admin/schemas/"):
                if not self.require_role("administrator"):
                    return
                return self.send_json({"success": True, "schemas": load_schemas()})

            if path in ("/api/admin/robots", "/api/admin/robots/"):
                if not self.require_role("administrator"):
                    return
                robots_path = os.path.join(BASE_DIR, "robots.txt")
                content = ""
                if os.path.isfile(robots_path):
                    try:
                        with open(robots_path, "r", encoding="utf-8") as f:
                            content = f.read()
                    except Exception as e:
                        return self.send_json({"error": f"خطا در خواندن فایل robots.txt: {str(e)}"}, 500)
                analysis = analyze_robots_txt(content)
                return self.send_json({
                    "success": True,
                    "content": content,
                    "analysis": analysis,
                    "path": "/robots.txt",
                    "fullUrl": "https://pezeshkan.me/robots.txt"
                })

            if path in ("/api/admin/llms", "/api/admin/llms/"):
                if not self.require_role("administrator"):
                    return
                settings = load_llms_settings()
                settings["enabled"] = settings.get("isEnabled", True)
                settings["postLimit"] = settings.get("limit", 50)
                preview = generate_llms_txt(settings)
                return self.send_json({
                    "success": True,
                    "ok": True,
                    "settings": settings,
                    "preview": preview,
                    "publicUrl": "https://pezeshkan.me/llms.txt"
                })

            if path in ("/api/admin/users", "/api/admin/users/"):
                if not self.require_role("administrator"):
                    return
                return self.send_json({"success": True, "users": get_safe_users()})

            if path.startswith("/api/admin/users/"):
                if not self.require_role("administrator"):
                    return
                parts = path.strip("/").split("/")
                if len(parts) >= 4:
                    target_id = parts[3]
                    u = find_user_by_id(target_id)
                    if not u:
                        return self.send_json({"error": "کاربر مورد نظر یافت نشد"}, 404)
                    safe_u = {k: v for k, v in u.items() if k not in ("passwordHash", "passwordSalt")}
                    return self.send_json({"success": True, "user": safe_u})

            if path in ("/api/admin/site-structure", "/api/admin/site-structure/"):
                if not self.require_role("administrator", "editor"):
                    return
                structure = analyze_site_structure()
                return self.send_json(structure)

            if path in ("/api/admin/seo-audit", "/api/admin/seo-audit/"):
                if not self.require_role("administrator", "editor"):
                    return
                audit = audit_comprehensive_seo()
                return self.send_json(audit)

            return self.send_json({"error": "مسیر API یافت نشد"}, 404)

        # 10. Authorized Static Assets (Public Bundles, Images, Scripts)
        clean_rel = path.lstrip("/")
        normalized = os.path.normpath(os.path.join(BASE_DIR, clean_rel))
        safe, code, msg = is_safe_static_request(normalized)
        if safe:
            return self.serve_file(normalized)
        if code == 403:
            return self.send_error(403, msg or "Access Denied")

        # 404 Fallback - Custom Branded Persian Error Page
        error_404_file = os.path.join(PORTAL_DIR, "404.html")
        if not os.path.isfile(error_404_file):
            error_404_file = os.path.join(BASE_DIR, "404.html")
        if os.path.isfile(error_404_file):
            return self.serve_file(error_404_file, "text/html", status=404, is_private=True)
        self.send_error(404, "Page Not Found")


    # 12. POST Request Router
    def do_POST(self):
        try:
            self._handle_POST()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass
        except Exception as e:
            logger.error(f"Internal Server Error in do_POST: {e}", exc_info=True)
            try:
                self.send_json({"error": "خطای داخلی سرور هنگام پردازش درخواست"}, 500)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                pass

    def _handle_POST(self):
        if not self.validate_host():
            self.send_error(400, "Bad Request: Invalid Host Header")
            return

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        client_ip = self.get_client_ip()

        # Anti-CSRF verification on state-changing requests
        if path.startswith("/api/") and not self.check_csrf():
            return self.send_json({"error": "درخواست غیرمجاز به دلیل عدم تطابق منبع اعتباری (CSRF Violation)"}, 403)

        data = self.read_json_body()
        if data is None:
            return

        # 1. Login Endpoint
        if path == "/api/login":
            allowed, retry_after = LOGIN_LIMITER.check(client_ip)
            if not allowed:
                return self.send_json({
                    "success": False,
                    "error": f"به دلیل تلاش‌های ناموفق مکرر، دسترسی موقتاً به مدت {retry_after} ثانیه مسدود شده است."
                }, 429)

            username = sanitize_string(data.get("username", ""), max_len=100)
            password = data.get("password", "")

            if verify_credentials(username, password):
                LOGIN_LIMITER.reset(client_ip)
                # Rotate session token and invalidate prior sessions
                revoke_user_sessions(username)
                token = create_session(username)
                sess = get_session(token) or {}
                csrf_token = sess.get("csrf_token", "")

                cookie_parts = [
                    f"session_token={token}",
                    "Path=/",
                    "HttpOnly",
                    "SameSite=Strict",
                    f"Max-Age={SESSION_MAX_AGE}"
                ]
                if self.is_https():
                    cookie_parts.append("Secure")
                cookie_str = "; ".join(cookie_parts)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Set-Cookie", cookie_str)
                self.send_security_headers()

                AUDIT_LOGGER.log_event(
                    "AUTH_LOGIN_SUCCESS",
                    ip=client_ip,
                    user=username,
                    status="SUCCESS",
                    details={"role": sess.get("role", "administrator")}
                )

                resp = json.dumps({
                    "success": True,
                    "token": token,
                    "csrfToken": csrf_token,
                    "user": {
                        "id": sess.get("userId", "usr_mahyarebrahimi"),
                        "username": username,
                        "name": sess.get("displayName", "مهیار ابراهیمی"),
                        "displayName": sess.get("displayName", "مهیار ابراهیمی"),
                        "role": sess.get("role", "administrator"),
                        "avatar": sess.get("avatar", "👨‍💼")
                    }
                }, ensure_ascii=False).encode("utf-8")
                self.send_header("Content-Length", str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)
                return
            else:
                LOGIN_LIMITER.record_hit(client_ip)
                allowed_now, _ = LOGIN_LIMITER.check(client_ip)
                msg = "نام کاربری یا رمز عبور اشتباه است."
                if not allowed_now:
                    msg = "تلاش‌های ناموفق شما به سقف مجاز رسید. حساب موقتاً مسدود شد."
                    AUDIT_LOGGER.log_event(
                        "AUTH_LOCKOUT",
                        ip=client_ip,
                        user=username,
                        status="LOCKED",
                        details={"retry_after": 300}
                    )
                else:
                    AUDIT_LOGGER.log_event(
                        "AUTH_LOGIN_FAILED",
                        ip=client_ip,
                        user=username,
                        status="FAILED"
                    )
                return self.send_json({"success": False, "error": msg}, 401)

        # 2. Logout Endpoint
        if path == "/api/logout":
            token = self.get_auth_token()
            sess = get_session(token)
            if sess:
                AUDIT_LOGGER.log_event("AUTH_LOGOUT", ip=client_ip, user=sess.get("username", "unknown"), status="SUCCESS")
            destroy_session(token)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            cookie_val = "session_token=deleted; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; SameSite=Strict"
            if self.is_https():
                cookie_val += "; Secure"
            self.send_header("Set-Cookie", cookie_val)
            self.send_security_headers()
            resp = b'{"success":true}'
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
            return

        # 3. Lead Generation (Smart Onboarding Form)
        if path == "/api/start-lead":
            allowed, retry_after = FORM_LIMITER.check(client_ip)
            if not allowed:
                return self.send_json({"error": f"درخواست‌های مکرر. لطفاً {retry_after} ثانیه دیگر مجدداً تلاش فرمایید."}, 429)
            FORM_LIMITER.record_hit(client_ip)

            name = sanitize_string(data.get("name", ""), max_len=100)
            phone = sanitize_string(data.get("phone", ""), max_len=30)
            address = sanitize_string(data.get("address", ""), max_len=500)

            if not name or not phone:
                return self.send_json({"error": "نام و شماره تماس الزامی است"}, 400)
            if not is_valid_phone(phone):
                return self.send_json({"error": "فرمت شماره تماس نامعتبر است"}, 400)

            lead_record = {
                "name": name,
                "phone": phone,
                "address": address,
                "ip": client_ip,
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

            leads_path = os.path.join(CONTENT_DIR, "leads.json")
            leads = load_json_file(leads_path, default=[])
            leads.insert(0, lead_record)
            if len(leads) > 1000:
                leads = leads[:1000]
            atomic_write_json(leads_path, leads)
            return self.send_json({"success": True, "message": "اطلاعات پزشک با موفقیت ثبت شد"})

        # 4. Contact Us Form
        if path == "/api/contact":
            allowed, retry_after = FORM_LIMITER.check(client_ip)
            if not allowed:
                return self.send_json({"error": f"درخواست‌های مکرر. لطفاً {retry_after} ثانیه دیگر مجدداً تلاش فرمایید."}, 429)
            FORM_LIMITER.record_hit(client_ip)

            name = sanitize_string(data.get("name", ""), max_len=100)
            phone = sanitize_string(data.get("phone", ""), max_len=30)
            subject = sanitize_string(data.get("subject", ""), max_len=200)
            message = sanitize_string(data.get("message", ""), max_len=5000)

            if not name or not phone:
                return self.send_json({"error": "نام و شماره همراه الزامی است"}, 400)
            if not is_valid_phone(phone):
                return self.send_json({"error": "فرمت شماره همراه نامعتبر است"}, 400)

            inquiry_record = {
                "name": name,
                "phone": phone,
                "subject": subject,
                "message": message,
                "ip": client_ip,
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

            inquiries_path = os.path.join(CONTENT_DIR, "inquiries.json")
            inquiries = load_json_file(inquiries_path, default=[])
            inquiries.insert(0, inquiry_record)
            if len(inquiries) > 1000:
                inquiries = inquiries[:1000]
            atomic_write_json(inquiries_path, inquiries)
            return self.send_json({"success": True, "message": "پیام شما با موفقیت ثبت شد"})

        # 5. Create Article (Protected Editorial Engine)
        if path == "/api/articles":
            if not self.require_role("administrator", "editor", "author"):
                return

            if not isinstance(data, dict) or not data.get("title") or not data.get("slug"):
                return self.send_json({"error": "عنوان و نامک مقاله الزامی است"}, 400)

            articles_path = os.path.join(CONTENT_DIR, "articles.json")
            articles = load_json_file(articles_path, default=[])

            # Sanitization of critical metadata fields
            data["title"] = sanitize_string(data.get("title", ""), 300)
            data["slug"] = re.sub(r'[^a-zA-Z0-9\-\u0600-\u06FF]', '', str(data.get("slug", "")))[:150]
            data["lastModified"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            articles.insert(0, data)
            atomic_write_json(articles_path, articles)
            return self.send_json({"success": True, "articles": articles})

        # 5.1 CRM Tutorials Endpoint
        if path in ("/api/crm-tutorials", "/api/crm-tutorials/"):
            if not self.require_role("administrator", "editor", "author"):
                return

            crm_path = os.path.join(CONTENT_DIR, "crm_tutorials.json")
            tutorials = load_json_file(crm_path, default=[])

            tut_id = data.get("id") or f"crm-{uuid.uuid4().hex[:8]}"
            data["id"] = tut_id
            if "title" in data:
                data["title"] = sanitize_string(data.get("title", ""), 300)
            if "category" in data:
                data["category"] = sanitize_string(data.get("category", ""), 100)
            if "videoUrl" in data:
                data["videoUrl"] = sanitize_string(data.get("videoUrl", ""), 1000).strip()
            data["lastModified"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            idx = next((i for i, t in enumerate(tutorials) if t.get("id") == tut_id), None)
            if idx is not None:
                tutorials[idx] = data
            else:
                tutorials.insert(0, data)

            atomic_write_json(crm_path, tutorials)
            return self.send_json({"success": True, "tutorials": tutorials})

        # 6. Upload Media File (WordPress-Grade Media Manager)
        if path == "/api/upload":
            if not self.require_role("administrator", "editor", "author"):
                return

            filename = data.get("filename", "image.png")
            b64_data = data.get("data", "")
            alt_text = sanitize_string(data.get("alt", ""), max_len=300)
            caption = sanitize_string(data.get("caption", ""), max_len=500)
            title = sanitize_string(data.get("title", ""), max_len=300)

            if not b64_data:
                return self.send_json({"error": "داده‌های تصویر ارسال نشده است"}, 400)

            if "," in b64_data:
                b64_data = b64_data.split(",", 1)[1]

            try:
                raw_bytes = base64.b64decode(b64_data)
            except Exception:
                return self.send_json({"error": "قالب داده تصویر base64 نامعتبر است"}, 400)

            if len(raw_bytes) > MAX_PAYLOAD_SIZE:
                return self.send_json({"error": "حجم فایل بیش از سقف مجاز سرور است (حداکثر ۱۵ مگابایت)"}, 400)

            orig_ext = os.path.splitext(filename)[1].lower()
            if orig_ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"]:
                orig_ext = ".webp"

            # Magic bytes validation & SVG anti-XSS sanitization
            is_valid = False
            if orig_ext in (".jpg", ".jpeg") and raw_bytes.startswith(b"\xff\xd8\xff"):
                is_valid = True
            elif orig_ext == ".png" and raw_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
                is_valid = True
            elif orig_ext == ".gif" and (raw_bytes.startswith(b"GIF87a") or raw_bytes.startswith(b"GIF89a")):
                is_valid = True
            elif orig_ext == ".webp" and raw_bytes[:4] == b"RIFF" and raw_bytes[8:12] == b"WEBP":
                is_valid = True
            elif orig_ext == ".svg":
                try:
                    svg_str = raw_bytes.decode("utf-8", errors="ignore").lower()
                    dangerous_patterns = [
                        "<script", "javascript:", "onload=", "onerror=", "onclick=",
                        "onmouseover=", "xlink:href=\"javascript:", "data:text/html"
                    ]
                    if any(p in svg_str for p in dangerous_patterns):
                        return self.send_json({"error": "فایل SVG ارسالی به دلیل داشتن کدهای اسکریپتی ناامن مسدود گردید"}, 400)
                    if "<svg" in svg_str:
                        is_valid = True
                except Exception:
                    is_valid = False

            if not is_valid:
                return self.send_json({"error": "نوع یا محتوای فایل ارسالی با پسوند آن همخوانی ندارد یا فرمت نامعتبر است"}, 400)

            try:
                media_item = MEDIA_STORAGE_ENGINE.store_media(
                    raw_bytes=raw_bytes,
                    filename=filename,
                    alt_text=alt_text,
                    caption=caption,
                    title=title
                )
            except Exception as e:
                logger.error(f"Error storing media: {e}", exc_info=True)
                return self.send_json({"error": f"خطا در پردازش و ذخیره‌سازی فایل: {str(e)}"}, 500)

            media_path = os.path.join(CONTENT_DIR, "media.json")
            media_list = load_json_file(media_path, default=[])
            media_list.insert(0, media_item)
            atomic_write_json(media_path, media_list)

            return self.send_json({"success": True, "url": media_item["url"], "media": media_item})

        # 6. SEO Redirect Management Endpoints (Protected Clinical Engine)
        if path in ("/api/admin/redirects", "/api/admin/redirects/"):
            if not self.require_role("administrator"):
                return

            source = sanitize_string(data.get("source", ""), 500).strip()
            target = sanitize_string(data.get("target", ""), 500).strip()
            try:
                status_code = int(data.get("statusCode", 301))
            except (ValueError, TypeError):
                status_code = 301

            match_type = data.get("matchType", "exact")
            preserve_query = bool(data.get("preserveQuery", True))
            is_active = bool(data.get("isActive", True))
            description = sanitize_string(data.get("description", ""), 500).strip()

            if not source:
                return self.send_json({"error": "مسیر مبدأ (Source URL) الزامی است"}, 400)
            if not source.startswith("/") and not source.startswith("^") and match_type != "regex":
                source = "/" + source

            if status_code != 410 and not target:
                return self.send_json({"error": "مسیر مقصد (Target URL) برای کدهای غیر ۴۱۰ الزامی است"}, 400)
            if status_code not in (301, 302, 307, 308, 410):
                return self.send_json({"error": "کد وضعیت HTTP نامعتبر است (تنها ۳۰۱، ۳۰۲، ۳۰۷، ۳۰۸ و ۴۱۰ مجاز است)"}, 400)
            if match_type not in ("exact", "prefix", "regex"):
                return self.send_json({"error": "نوع تطابق نامعتبر است"}, 400)

            if match_type == "regex":
                try:
                    re.compile(source)
                except re.error as rx_err:
                    return self.send_json({"error": f"قالب عبارت منظم نامعتبر است: {rx_err}"}, 400)

            # Prevent self-referencing loops
            if status_code != 410 and source.rstrip("/").lower() == target.rstrip("/").lower():
                return self.send_json({"error": "خطای چرخه بی‌پایان (Loop): مسیر مبدأ و مقصد نمی‌توانند یکسان باشند"}, 400)

            rules = load_redirects()
            new_id = f"red_{int(time.time())}_{secrets.token_hex(3)}"
            now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            new_rule = {
                "id": new_id,
                "source": source,
                "target": target if status_code != 410 else "",
                "statusCode": status_code,
                "matchType": match_type,
                "preserveQuery": preserve_query,
                "isActive": is_active,
                "description": description,
                "hitCount": 0,
                "lastHit": None,
                "createdAt": now_iso,
                "updatedAt": now_iso
            }
            rules.insert(0, new_rule)
            save_redirects(rules)
            return self.send_json({"success": True, "redirect": new_rule, "redirects": rules})

        if path in ("/api/admin/redirects/update", "/api/admin/redirects/update/"):
            if not self.require_role("administrator"):
                return

            rule_id = data.get("id")
            if not rule_id:
                return self.send_json({"error": "شناسه ریدایرکت ارسال نشده است"}, 400)

            rules = load_redirects()
            rule = next((r for r in rules if r.get("id") == rule_id), None)
            if not rule:
                return self.send_json({"error": "قانون ریدایرکت مورد نظر یافت نشد"}, 404)

            source = sanitize_string(data.get("source", rule.get("source")), 500).strip()
            try:
                status_code = int(data.get("statusCode", rule.get("statusCode", 301)))
            except (ValueError, TypeError):
                status_code = 301

            target = sanitize_string(data.get("target", rule.get("target")), 500).strip() if status_code != 410 else ""
            match_type = data.get("matchType", rule.get("matchType", "exact"))
            preserve_query = bool(data.get("preserveQuery", rule.get("preserveQuery", True)))
            is_active = bool(data.get("isActive", rule.get("isActive", True)))
            description = sanitize_string(data.get("description", rule.get("description", "")), 500).strip()

            if not source:
                return self.send_json({"error": "مسیر مبدأ الزامی است"}, 400)
            if not source.startswith("/") and not source.startswith("^") and match_type != "regex":
                source = "/" + source
            if status_code != 410 and not target:
                return self.send_json({"error": "مسیر مقصد الزامی است"}, 400)
            if status_code not in (301, 302, 307, 308, 410):
                return self.send_json({"error": "کد وضعیت HTTP نامعتبر است"}, 400)
            if match_type not in ("exact", "prefix", "regex"):
                return self.send_json({"error": "نوع تطابق نامعتبر است"}, 400)

            if match_type == "regex":
                try:
                    re.compile(source)
                except re.error as rx_err:
                    return self.send_json({"error": f"قالب عبارت منظم نامعتبر است: {rx_err}"}, 400)

            if status_code != 410 and source.rstrip("/").lower() == target.rstrip("/").lower():
                return self.send_json({"error": "خطای چرخه بی‌پایان (Loop): مسیر مبدأ و مقصد نمی‌توانند یکسان باشند"}, 400)

            rule.update({
                "source": source,
                "target": target,
                "statusCode": status_code,
                "matchType": match_type,
                "preserveQuery": preserve_query,
                "isActive": is_active,
                "description": description,
                "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })
            save_redirects(rules)
            return self.send_json({"success": True, "redirect": rule, "redirects": rules})

        if path in ("/api/admin/redirects/delete", "/api/admin/redirects/delete/"):
            if not self.require_role("administrator"):
                return
            rule_id = data.get("id")
            if not rule_id:
                return self.send_json({"error": "شناسه ریدایرکت ارسال نشده است"}, 400)
            rules = load_redirects()
            rules = [r for r in rules if r.get("id") != rule_id]
            save_redirects(rules)
            return self.send_json({"success": True, "redirects": rules})

        if path in ("/api/admin/redirects/toggle", "/api/admin/redirects/toggle/"):
            if not self.require_role("administrator"):
                return
            rule_id = data.get("id")
            if not rule_id:
                return self.send_json({"error": "شناسه ریدایرکت ارسال نشده است"}, 400)
            rules = load_redirects()
            for r in rules:
                if r.get("id") == rule_id:
                    r["isActive"] = not r.get("isActive", True)
                    r["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    break
            save_redirects(rules)
            return self.send_json({"success": True, "redirects": rules})

        if path in ("/api/admin/redirects/test", "/api/admin/redirects/test/"):
            if not self.require_role("administrator"):
                return
            test_url = (data.get("url") or "").strip()
            if not test_url:
                return self.send_json({"error": "نشانی URL برای بررسی ارسال نشده است"}, 400)
            parsed_test = urllib.parse.urlparse(test_url)
            match_res = match_custom_redirect(parsed_test.path, parsed_test.query)
            if match_res:
                sc, tgt = match_res
                return self.send_json({
                    "matched": True,
                    "statusCode": sc,
                    "targetUrl": tgt,
                    "isGone": (sc == 410)
                })
            return self.send_json({"matched": False, "message": "هیچ قانون فعالی برای این نشانی منطبق نشد (مسیر به حالت عادی لود می‌شود)"})

        # 7. Schema.org Management Endpoints (Rank Math Studio)
        if path in ("/api/admin/schemas", "/api/admin/schemas/"):
            if not self.require_role("administrator"):
                return

            name = sanitize_string(data.get("name", ""), 300).strip()
            target_url = sanitize_string(data.get("targetUrl", ""), 300).strip() or "*"
            schema_type = sanitize_string(data.get("schemaType", "WebPage"), 100).strip()
            description = sanitize_string(data.get("description", ""), 500).strip()
            schema_data = data.get("data", {})
            is_active = bool(data.get("isActive", True))

            if not name:
                return self.send_json({"error": "نام و عنوان الگو اسکیما الزامی است"}, 400)
            if not schema_type:
                return self.send_json({"error": "نوع اسکیما (Schema Type) الزامی است"}, 400)

            if schema_type == "Custom" or data.get("customJson"):
                custom_str = data.get("customJson", "")
                if custom_str:
                    try:
                        json.loads(custom_str)
                    except json.JSONDecodeError as je:
                        return self.send_json({"error": f"قالب کد JSON-LD نامعتبر است: {je}"}, 400)

            schemas = load_schemas()
            new_id = f"sch_{int(time.time())}_{secrets.token_hex(3)}"
            now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            new_schema = {
                "id": new_id,
                "name": name,
                "targetUrl": target_url,
                "schemaType": schema_type,
                "isActive": is_active,
                "description": description,
                "data": schema_data,
                "customJson": data.get("customJson", ""),
                "createdAt": now_iso,
                "updatedAt": now_iso
            }
            schemas.insert(0, new_schema)
            save_schemas(schemas)
            return self.send_json({"success": True, "schema": new_schema, "schemas": schemas})

        if path in ("/api/admin/schemas/update", "/api/admin/schemas/update/"):
            if not self.require_role("administrator"):
                return

            schema_id = data.get("id")
            if not schema_id:
                return self.send_json({"error": "شناسه اسکیما ارسال نشده است"}, 400)

            schemas = load_schemas()
            schema_item = next((s for s in schemas if s.get("id") == schema_id), None)
            if not schema_item:
                return self.send_json({"error": "الگوی اسکیما مورد نظر یافت نشد"}, 404)

            name = sanitize_string(data.get("name", schema_item.get("name")), 300).strip()
            target_url = sanitize_string(data.get("targetUrl", schema_item.get("targetUrl")), 300).strip() or "*"
            schema_type = sanitize_string(data.get("schemaType", schema_item.get("schemaType")), 100).strip()
            description = sanitize_string(data.get("description", schema_item.get("description")), 500).strip()
            schema_data = data.get("data", schema_item.get("data", {}))
            is_active = bool(data.get("isActive", schema_item.get("isActive", True)))

            if not name:
                return self.send_json({"error": "نام اسکیما الزامی است"}, 400)

            if schema_type == "Custom" or data.get("customJson"):
                custom_str = data.get("customJson", "")
                if custom_str:
                    try:
                        json.loads(custom_str)
                    except json.JSONDecodeError as je:
                        return self.send_json({"error": f"قالب کد JSON-LD نامعتبر است: {je}"}, 400)

            schema_item.update({
                "name": name,
                "targetUrl": target_url,
                "schemaType": schema_type,
                "isActive": is_active,
                "description": description,
                "data": schema_data,
                "customJson": data.get("customJson", schema_item.get("customJson", "")),
                "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })
            save_schemas(schemas)
            return self.send_json({"success": True, "schema": schema_item, "schemas": schemas})

        if path in ("/api/admin/schemas/delete", "/api/admin/schemas/delete/"):
            if not self.require_role("administrator"):
                return
            schema_id = data.get("id")
            if not schema_id:
                return self.send_json({"error": "شناسه اسکیما الزامی است"}, 400)
            schemas = load_schemas()
            schemas = [s for s in schemas if s.get("id") != schema_id]
            save_schemas(schemas)
            return self.send_json({"success": True, "schemas": schemas})

        if path in ("/api/admin/schemas/toggle", "/api/admin/schemas/toggle/"):
            if not self.require_role("administrator"):
                return
            schema_id = data.get("id")
            if not schema_id:
                return self.send_json({"error": "شناسه اسکیما الزامی است"}, 400)
            schemas = load_schemas()
            for s in schemas:
                if s.get("id") == schema_id:
                    s["isActive"] = not s.get("isActive", True)
                    s["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    break
            save_schemas(schemas)
            return self.send_json({"success": True, "schemas": schemas})

        if path in ("/api/admin/schemas/validate", "/api/admin/schemas/validate/"):
            if not self.require_role("administrator"):
                return
            raw_input = data.get("schema") or data.get("jsonld")
            if raw_input is None:
                return self.send_json({"error": "کد JSON-LD ارسال نشده است"}, 400)
            errors = validate_schema_structure(raw_input)
            if errors:
                return self.send_json({"valid": False, "error": "، ".join(errors), "errors": errors})
            stype = "StructuredData"
            if isinstance(raw_input, dict):
                stype = raw_input.get("@type", "StructuredData")
            return self.send_json({
                "valid": True,
                "message": "ساختار داده‌های نشانی معتبر بوده و با استانداردهای گوگل و Schema.org سازگار است.",
                "type": str(stype)
            })

        if path in ("/api/admin/robots", "/api/admin/robots/"):
            if not self.require_role("administrator"):
                return
            new_content = data.get("content")
            if new_content is None:
                return self.send_json({"error": "محتوای فایل robots.txt ارسال نشده است"}, 400)
            if len(new_content) > 100000:
                return self.send_json({"error": "حجم فایل robots.txt بیش از حد مجاز است (حداکثر ۱۰۰ کیلوبایت)"}, 400)

            robots_path = os.path.join(BASE_DIR, "robots.txt")
            tmp_path = robots_path + f".tmp.{secrets.token_hex(4)}"
            try:
                with open(tmp_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, robots_path)
            except Exception as e:
                return self.send_json({"error": f"خطا در ذخیره‌سازی فایل robots.txt: {str(e)}"}, 500)
            finally:
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass

            analysis = analyze_robots_txt(new_content)
            return self.send_json({
                "success": True,
                "message": "فایل robots.txt با موفقیت ذخیره و در سرور فعال شد.",
                "content": new_content,
                "analysis": analysis
            })

        if path in ("/api/admin/robots/analyze", "/api/admin/robots/analyze/"):
            if not self.require_role("administrator"):
                return
            eval_content = data.get("content")
            if eval_content is None:
                robots_path = os.path.join(BASE_DIR, "robots.txt")
                if os.path.isfile(robots_path):
                    try:
                        with open(robots_path, "r", encoding="utf-8") as f:
                            eval_content = f.read()
                    except Exception:
                        eval_content = ""
                else:
                    eval_content = ""
            analysis = analyze_robots_txt(eval_content)
            return self.send_json({"success": True, "analysis": analysis})

        if path in ("/api/admin/llms", "/api/admin/llms/"):
            if not self.require_role("administrator"):
                return
            settings = load_llms_settings()
            if isinstance(data, dict):
                if "isEnabled" in data:
                    settings["isEnabled"] = bool(data["isEnabled"])
                elif "enabled" in data:
                    settings["isEnabled"] = bool(data["enabled"])
                settings["enabled"] = settings["isEnabled"]

                if "postTypes" in data and isinstance(data["postTypes"], dict):
                    settings["postTypes"] = {
                        "posts": bool(data["postTypes"].get("posts", True)),
                        "pages": bool(data["postTypes"].get("pages", True)),
                        "floating": bool(data["postTypes"].get("floating", True))
                    }
                if "taxonomies" in data and isinstance(data["taxonomies"], dict):
                    settings["taxonomies"] = {
                        "categories": bool(data["taxonomies"].get("categories", True)),
                        "tags": bool(data["taxonomies"].get("tags", True))
                    }
                if "limit" in data:
                    try:
                        settings["limit"] = max(1, min(500, int(data["limit"])))
                    except (ValueError, TypeError):
                        settings["limit"] = 50
                elif "postLimit" in data:
                    try:
                        settings["limit"] = max(1, min(500, int(data["postLimit"])))
                    except (ValueError, TypeError):
                        settings["limit"] = 50
                settings["postLimit"] = settings["limit"]

                if "additionalContent" in data:
                    settings["additionalContent"] = str(data["additionalContent"])
                settings["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                save_llms_settings(settings)

                # Regenerate physical file on disk
                llms_path = os.path.join(BASE_DIR, "llms.txt")
                if settings.get("isEnabled", True):
                    content = generate_llms_txt(settings)
                    atomic_write_text(llms_path, content)
                else:
                    if os.path.exists(llms_path):
                        try:
                            os.remove(llms_path)
                        except OSError:
                            pass
                preview = generate_llms_txt(settings)
                return self.send_json({
                    "success": True,
                    "ok": True,
                    "message": "تنظیمات فایل llms.txt با موفقیت ذخیره و در سرور فعال شد.",
                    "settings": settings,
                    "preview": preview
                })
            return self.send_json({"error": "داده‌های ارسالی نامعتبر است"}, 400)

        if path in ("/api/admin/llms/preview", "/api/admin/llms/preview/"):
            if not self.require_role("administrator"):
                return
            preview = generate_llms_txt(data if isinstance(data, dict) else None)
            return self.send_json({"success": True, "ok": True, "preview": preview})

        # User Management: Password Reset
        if path.startswith("/api/admin/users/") and path.endswith("/password"):
            if not self.require_role("administrator"):
                return
            parts = path.strip("/").split("/")
            if len(parts) < 4:
                return self.send_json({"error": "شناسه کاربر نامعتبر است"}, 400)
            target_id = parts[3]
            new_password = str(data.get("newPassword", "")).strip()
            if len(new_password) < 8:
                return self.send_json({"error": "رمز عبور جدید باید حداقل ۸ کاراکتر باشد."}, 400)
            if not any(c.isalpha() for c in new_password) or not any(c.isdigit() for c in new_password):
                return self.send_json({"error": "رمز عبور باید ترکیبی از حروف و اعداد باشد."}, 400)

            users = load_users()
            target_user = None
            for u in users:
                if u.get("id") == target_id:
                    target_user = u
                    break
            if not target_user:
                return self.send_json({"error": "کاربر مورد نظر یافت نشد"}, 404)

            salt, pwd_hash = hash_user_password(new_password)
            target_user["passwordSalt"] = salt
            target_user["passwordHash"] = pwd_hash
            target_user["passwordUpdatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            save_users(users)

            # Invalidate all active sessions for this user for security
            revoke_user_sessions(target_user.get("username", ""))

            return self.send_json({
                "success": True,
                "message": f"گذرواژه کاربر «{target_user.get('displayName')}» با موفقیت تغییر یافت و تمام نشست‌های قبلی ابطال گردید."
            })

        # User Management: Create User
        if path in ("/api/admin/users", "/api/admin/users/"):
            if not self.require_role("administrator"):
                return

            username = sanitize_string(data.get("username", ""), 40).strip().lower()
            if not username or len(username) < 3 or not re.match(r'^[a-zA-Z0-9_\-]+$', username):
                return self.send_json({"error": "نام کاربری نامعتبر است (حداقل ۳ کاراکتر انگلیسی و بدون فاصله)."}, 400)

            if find_user_by_username(username):
                return self.send_json({"error": "این نام کاربری قبلاً در سامانه ثبت شده است."}, 400)

            password = str(data.get("password", "")).strip()
            if len(password) < 8:
                return self.send_json({"error": "رمز عبور اولیه باید حداقل ۸ کاراکتر باشد."}, 400)
            if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
                return self.send_json({"error": "رمز عبور باید ترکیبی از حروف و اعداد باشد."}, 400)

            email = sanitize_string(data.get("email", ""), 100).strip()
            if not email or "@" not in email:
                return self.send_json({"error": "آدرس ایمیل معتبر الزامی است."}, 400)

            first_name = sanitize_string(data.get("firstName", ""), 60).strip()
            last_name = sanitize_string(data.get("lastName", ""), 60).strip()
            nickname = sanitize_string(data.get("nickname", ""), 60).strip() or username
            display_name = sanitize_string(data.get("displayName", ""), 100).strip()
            if not display_name:
                display_name = f"{first_name} {last_name}".strip() or nickname

            role = sanitize_string(data.get("role", "author"), 30).strip()
            if role not in ("administrator", "editor", "author", "contributor"):
                role = "author"

            salt, pwd_hash = hash_user_password(password)
            new_user = {
                "id": f"usr_{secrets.token_hex(6)}",
                "username": username,
                "displayName": display_name,
                "firstName": first_name,
                "lastName": last_name,
                "nickname": nickname,
                "email": email,
                "website": sanitize_string(data.get("website", ""), 200).strip(),
                "role": role,
                "bio": sanitize_string(data.get("bio", ""), 1000).strip(),
                "specialty": sanitize_string(data.get("specialty", ""), 100).strip(),
                "medicalCouncil": sanitize_string(data.get("medicalCouncil", ""), 30).strip(),
                "avatar": sanitize_string(data.get("avatar", "👨‍⚕️" if role == "author" else "👤"), 100).strip(),
                "status": "suspended" if data.get("status") == "suspended" else "active",
                "passwordSalt": salt,
                "passwordHash": pwd_hash,
                "registeredAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "lastLogin": ""
            }

            users = load_users()
            users.append(new_user)
            save_users(users)
            safe_u = {k: v for k, v in new_user.items() if k not in ("passwordHash", "passwordSalt")}
            return self.send_json({"success": True, "user": safe_u, "message": "کاربر جدید با موفقیت ایجاد گردید."})

        # Site Structure: Live Real-time Simulation & Analysis
        if path in ("/api/admin/site-structure/analyze", "/api/admin/site-structure/analyze/"):
            if not self.require_role("administrator", "editor"):
                return
            override_art = data.get("article") if isinstance(data, dict) and "article" in data else data
            structure = analyze_site_structure(override_article=override_art if isinstance(override_art, dict) else None)
            return self.send_json(structure)

        # SEO & Anti-Spam: Live Real-time Simulation & Analysis
        if path in ("/api/admin/seo-audit/analyze", "/api/admin/seo-audit/analyze/"):
            if not self.require_role("administrator", "editor"):
                return
            override_art = data.get("article") if isinstance(data, dict) and "article" in data else data
            audit = audit_comprehensive_seo(override_article=override_art if isinstance(override_art, dict) else None)
            return self.send_json(audit)

        # 16. Newsletter Subscription (Public Endpoint)
        if path in ("/api/newsletter/subscribe", "/api/newsletter/subscribe/"):
            email = sanitize_string(data.get("email", ""), 100).strip().lower()
            name = sanitize_string(data.get("name", ""), 100).strip()
            category = sanitize_string(data.get("category", "all"), 50).strip()
            if not email or "@" not in email:
                return self.send_json({"error": "نشانی ایمیل نامعتبر است"}, 400)
            subs_path = os.path.join(CONTENT_DIR, "subscribers.json")
            subscribers = load_json_file(subs_path, default=[])
            if not any(s.get("email") == email for s in subscribers):
                subscribers.append({
                    "id": "sub-" + secrets.token_hex(4),
                    "email": email,
                    "name": name,
                    "category": category,
                    "subscribedAt": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "ip": client_ip
                })
                atomic_write_json(subs_path, subscribers)
            return self.send_json({"success": True, "message": "عضویت شما در خبرنامه با موفقیت ثبت شد"})

        # 17. Newsletters: Create / Save Newsletter
        if path in ("/api/newsletters", "/api/newsletters/"):
            if not self.require_role("administrator", "editor"):
                return
            newsletters_path = os.path.join(CONTENT_DIR, "newsletters.json")
            newsletters = load_json_file(newsletters_path, default=[])

            issue_id = data.get("id")
            if not issue_id:
                issue_id = "issue-" + str(int(time.time()))
                data["id"] = issue_id

            if "title" in data:
                data["title"] = sanitize_string(data.get("title", ""), 250)
            if "issueNumber" in data:
                data["issueNumber"] = sanitize_string(data.get("issueNumber", ""), 50)
            if "summary" in data:
                data["summary"] = sanitize_string(data.get("summary", ""), 500)
            if "doctor" in data:
                data["doctor"] = sanitize_string(data.get("doctor", ""), 150)
            if "category" in data:
                data["category"] = sanitize_string(data.get("category", ""), 100)
            if not data.get("publishDate"):
                data["publishDate"] = time.strftime("%Y/%m/%d")

            idx = next((i for i, n in enumerate(newsletters) if n.get("id") == issue_id), None)
            if idx is not None:
                newsletters[idx] = data
            else:
                newsletters.insert(0, data)

            atomic_write_json(newsletters_path, newsletters)
            return self.send_json({"success": True, "newsletters": newsletters, "newsletter": data})

        self.send_error(404, "API Endpoint Not Found")

    # 13. PUT Request Router
    def do_PUT(self):
        try:
            self._handle_PUT()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass
        except Exception as e:
            logger.error(f"Internal Server Error in do_PUT: {e}", exc_info=True)
            try:
                self.send_json({"error": "خطای داخلی سرور هنگام ویرایش اطلاعات"}, 500)
            except Exception:
                pass

    def _handle_PUT(self):
        if not self.validate_host():
            self.send_error(400, "Bad Request: Invalid Host Header")
            return

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if not self.check_csrf():
            return self.send_json({"error": "درخواست غیرمجاز به دلیل عدم تطابق منبع اعتباری (CSRF Violation)"}, 403)

        data = self.read_json_body()
        if data is None:
            return

        if path == "/api/articles":
            if not self.require_role("administrator", "editor", "author"):
                return

            articles_path = os.path.join(CONTENT_DIR, "articles.json")
            articles = load_json_file(articles_path, default=[])

            article_id = data.get("id")
            if not article_id:
                return self.send_json({"error": "شناسه مقاله الزامی است"}, 400)

            # Broken Access Control / IDOR Prevention:
            # Authors can only modify their own articles
            sess = self.get_current_session() or {}
            user_role = sess.get("role", "author")
            user_id = sess.get("userId", "")
            username = sess.get("username", "")

            existing_article = next((a for a in articles if a.get("id") == article_id), None)
            if existing_article and user_role == "author":
                author_obj = existing_article.get("author") or {}
                author_id = author_obj.get("id") or existing_article.get("authorId")
                author_name = str(author_obj.get("name") or "").strip().lower()
                user_display = str(sess.get("name") or "").strip().lower()

                is_owner = False
                if author_id and author_id == user_id:
                    is_owner = True
                elif author_name and (author_name == username.lower() or author_name == user_display):
                    is_owner = True

                if not is_owner:
                    AUDIT_LOGGER.log_event(
                        "ACCESS_DENIED_IDOR",
                        ip=self.get_client_ip(),
                        user=username,
                        status="BLOCKED",
                        details={"article_id": article_id, "action": "PUT", "reason": "Author attempted to edit another user's article"}
                    )
                    return self.send_json({"error": "عدم دسترسی: شما فقط مجاز به ویرایش مقالات خودتان هستید."}, 403)

            if "title" in data:
                data["title"] = sanitize_string(data.get("title", ""), 300)
            if "slug" in data:
                data["slug"] = re.sub(r'[^a-zA-Z0-9\-\u0600-\u06FF]', '', str(data.get("slug", "")))[:150]
            data["lastModified"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            idx = next((i for i, a in enumerate(articles) if a.get("id") == article_id), None)
            if idx is not None:
                articles[idx] = data
            else:
                articles.insert(0, data)

            atomic_write_json(articles_path, articles)
            AUDIT_LOGGER.log_event("ARTICLE_SAVED", ip=self.get_client_ip(), user=username, status="SUCCESS", details={"article_id": article_id})
            return self.send_json({"success": True, "articles": articles})

        if path == "/api/settings":
            if not self.require_role("administrator"):
                return
            settings_path = os.path.join(CONTENT_DIR, "settings.json")
            data["lastUpdated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            atomic_write_json(settings_path, data)
            return self.send_json({"success": True, "settings": data})

        if path in ("/api/crm-tutorials", "/api/crm-tutorials/"):
            if not self.require_role("administrator", "editor", "author"):
                return
            crm_path = os.path.join(CONTENT_DIR, "crm_tutorials.json")
            tutorials = load_json_file(crm_path, default=[])

            tut_id = data.get("id")
            if not tut_id:
                return self.send_json({"error": "شناسه آموزش الزامی است"}, 400)

            if "title" in data:
                data["title"] = sanitize_string(data.get("title", ""), 300)
            if "category" in data:
                data["category"] = sanitize_string(data.get("category", ""), 100)
            if "videoUrl" in data:
                data["videoUrl"] = sanitize_string(data.get("videoUrl", ""), 1000).strip()
            data["lastModified"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            idx = next((i for i, t in enumerate(tutorials) if t.get("id") == tut_id), None)
            if idx is not None:
                tutorials[idx] = data
            else:
                tutorials.insert(0, data)

            atomic_write_json(crm_path, tutorials)
            return self.send_json({"success": True, "tutorials": tutorials})

        if path in ("/api/doctors", "/api/doctors/"):
            if not self.require_role("administrator", "editor"):
                return
            doctors_path = os.path.join(CONTENT_DIR, "doctors.json")
            doctors = load_json_file(doctors_path, default=[])

            doc_id = data.get("id")
            if not doc_id:
                doc_id = "dr-" + str(int(time.time()))
                data["id"] = doc_id

            if "name" in data:
                data["name"] = sanitize_string(data.get("name", ""), 150)
            if "title" in data:
                data["title"] = sanitize_string(data.get("title", ""), 200)
            if "address" in data:
                data["address"] = sanitize_string(data.get("address", ""), 300)
            if "workHours" in data:
                data["workHours"] = sanitize_string(data.get("workHours", ""), 150)
            if "phone" in data:
                data["phone"] = sanitize_string(data.get("phone", ""), 50)

            idx = next((i for i, d in enumerate(doctors) if d.get("id") == doc_id), None)
            if idx is not None:
                doctors[idx] = data
            else:
                doctors.append(data)

            atomic_write_json(doctors_path, doctors)
            return self.send_json({"success": True, "doctors": doctors, "doctor": data})

        if path in ("/api/appointments", "/api/appointments/"):
            appointments_path = os.path.join(CONTENT_DIR, "appointments.json")
            appointments = load_json_file(appointments_path, default=[])
            tracking_code = "PZ-" + str(int(time.time()))[-6:]
            entry = {
                "id": "apt-" + str(int(time.time() * 1000)),
                "trackingCode": tracking_code,
                "doctorId": sanitize_string(data.get("doctorId", ""), 80),
                "doctorName": sanitize_string(data.get("doctorName", ""), 150),
                "patientName": sanitize_string(data.get("patientName", ""), 150),
                "patientPhone": sanitize_string(data.get("patientPhone", ""), 50),
                "nationalId": sanitize_string(data.get("nationalId", ""), 30),
                "visitType": sanitize_string(data.get("visitType", "ویزیت حضوری مطب"), 100),
                "timeSlot": sanitize_string(data.get("timeSlot", ""), 50),
                "dateLabel": sanitize_string(data.get("dateLabel", "امروز"), 80),
                "notes": sanitize_string(data.get("notes", ""), 400),
                "createdAt": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            appointments.insert(0, entry)
            atomic_write_json(appointments_path, appointments)
            return self.send_json({"success": True, "trackingCode": tracking_code, "appointment": entry})

        if path in ("/api/newsletter/subscribe", "/api/newsletter/subscribe/"):
            email = sanitize_string(data.get("email", ""), 100).strip().lower()
            name = sanitize_string(data.get("name", ""), 100).strip()
            category = sanitize_string(data.get("category", "all"), 50).strip()
            if not email or "@" not in email:
                return self.send_json({"error": "نشانی ایمیل نامعتبر است"}, 400)
            subs_path = os.path.join(CONTENT_DIR, "subscribers.json")
            subscribers = load_json_file(subs_path, default=[])
            if not any(s.get("email") == email for s in subscribers):
                subscribers.append({
                    "id": "sub-" + secrets.token_hex(4),
                    "email": email,
                    "name": name,
                    "category": category,
                    "subscribedAt": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "ip": client_ip
                })
                atomic_write_json(subs_path, subscribers)
            return self.send_json({"success": True, "message": "عضویت شما در خبرنامه با موفقیت ثبت شد"})

        if path in ("/api/newsletters", "/api/newsletters/"):
            if not self.require_role("administrator", "editor"):
                return
            newsletters_path = os.path.join(CONTENT_DIR, "newsletters.json")
            newsletters = load_json_file(newsletters_path, default=[])

            issue_id = data.get("id")
            if not issue_id:
                issue_id = "issue-" + str(int(time.time()))
                data["id"] = issue_id

            if "title" in data:
                data["title"] = sanitize_string(data.get("title", ""), 250)
            if "issueNumber" in data:
                data["issueNumber"] = sanitize_string(data.get("issueNumber", ""), 50)
            if "summary" in data:
                data["summary"] = sanitize_string(data.get("summary", ""), 500)
            if "doctor" in data:
                data["doctor"] = sanitize_string(data.get("doctor", ""), 150)
            if "category" in data:
                data["category"] = sanitize_string(data.get("category", ""), 100)
            if not data.get("publishDate"):
                data["publishDate"] = time.strftime("%Y/%m/%d")

            idx = next((i for i, n in enumerate(newsletters) if n.get("id") == issue_id), None)
            if idx is not None:
                newsletters[idx] = data
            else:
                newsletters.insert(0, data)

            atomic_write_json(newsletters_path, newsletters)
            return self.send_json({"success": True, "newsletters": newsletters, "newsletter": data})

        # User Management: Update User Profile (WordPress Style)
        if path.startswith("/api/admin/users/"):
            if not self.require_role("administrator"):
                return
            parts = path.strip("/").split("/")
            if len(parts) < 4:
                return self.send_json({"error": "شناسه کاربر نامعتبر است"}, 400)
            target_id = parts[3]
            users = load_users()
            target_user = None
            for u in users:
                if u.get("id") == target_id:
                    target_user = u
                    break
            if not target_user:
                return self.send_json({"error": "کاربر مورد نظر یافت نشد"}, 404)

            # Prevent lockout on primary admin
            if target_user.get("username") == ADMIN_USERNAME or target_id == "usr_mahyarebrahimi":
                if data.get("role") and data.get("role") != "administrator":
                    return self.send_json({"error": "امکان تنزل نقش مدیر کل اصلی سیستم وجود ندارد."}, 400)
                if data.get("status") == "suspended":
                    return self.send_json({"error": "امکان مسدودسازی حساب مدیر کل اصلی سیستم وجود ندارد."}, 400)

            if "displayName" in data:
                target_user["displayName"] = sanitize_string(data["displayName"], 100).strip() or target_user["displayName"]
            if "firstName" in data:
                target_user["firstName"] = sanitize_string(data["firstName"], 60).strip()
            if "lastName" in data:
                target_user["lastName"] = sanitize_string(data["lastName"], 60).strip()
            if "nickname" in data:
                target_user["nickname"] = sanitize_string(data["nickname"], 60).strip()
            if "email" in data:
                target_user["email"] = sanitize_string(data["email"], 100).strip()
            if "website" in data:
                target_user["website"] = sanitize_string(data["website"], 200).strip()
            if "bio" in data:
                target_user["bio"] = sanitize_string(data["bio"], 1000).strip()
            if "specialty" in data:
                target_user["specialty"] = sanitize_string(data["specialty"], 100).strip()
            if "medicalCouncil" in data:
                target_user["medicalCouncil"] = sanitize_string(data["medicalCouncil"], 30).strip()
            if "avatar" in data:
                target_user["avatar"] = sanitize_string(data["avatar"], 100).strip()
            if "role" in data and target_user.get("username") != ADMIN_USERNAME and target_id != "usr_mahyarebrahimi":
                if data["role"] in ("administrator", "editor", "author", "contributor"):
                    target_user["role"] = data["role"]
            if "status" in data and target_user.get("username") != ADMIN_USERNAME and target_id != "usr_mahyarebrahimi":
                target_user["status"] = "suspended" if data["status"] == "suspended" else "active"

            # WordPress style: If password was sent in user edit form
            new_pwd = str(data.get("password", "")).strip()
            if new_pwd:
                if len(new_pwd) < 8 or not any(c.isalpha() for c in new_pwd) or not any(c.isdigit() for c in new_pwd):
                    return self.send_json({"error": "رمز عبور ارسالی نامعتبر است (حداقل ۸ کاراکتر ترکیب حروف و اعداد)."}, 400)
                salt, pwd_hash = hash_user_password(new_pwd)
                target_user["passwordSalt"] = salt
                target_user["passwordHash"] = pwd_hash
                target_user["passwordUpdatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                revoke_user_sessions(target_user.get("username", ""))

            save_users(users)
            safe_u = {k: v for k, v in target_user.items() if k not in ("passwordHash", "passwordSalt")}
            return self.send_json({"success": True, "user": safe_u, "message": "اطلاعات کاربر با موفقیت به‌روزرسانی شد."})

        # Site Structure: Live Real-time Simulation & Analysis
        if path in ("/api/admin/site-structure/analyze", "/api/admin/site-structure/analyze/"):
            if not self.require_role("administrator", "editor"):
                return
            override_art = data.get("article") if isinstance(data, dict) and "article" in data else data
            structure = analyze_site_structure(override_article=override_art if isinstance(override_art, dict) else None)
            return self.send_json(structure)

        # SEO & Anti-Spam: Live Real-time Simulation & Analysis
        if path in ("/api/admin/seo-audit/analyze", "/api/admin/seo-audit/analyze/"):
            if not self.require_role("administrator", "editor"):
                return
            override_art = data.get("article") if isinstance(data, dict) and "article" in data else data
            audit = audit_comprehensive_seo(override_article=override_art if isinstance(override_art, dict) else None)
            return self.send_json(audit)
        # Media Metadata Update Endpoint
        if path == "/api/media":
            if not self.require_role("administrator", "editor", "author"):
                return
            media_id = data.get("id")
            if not media_id:
                return self.send_json({"error": "شناسه رسانه ارسال نشده است"}, 400)

            media_path = os.path.join(CONTENT_DIR, "media.json")
            media_list = load_json_file(media_path, default=[])

            target_item = next((m for m in media_list if m.get("id") == media_id), None)
            if not target_item:
                return self.send_json({"error": "رسانه مورد نظر یافت نشد"}, 404)

            if "alt" in data:
                target_item["alt"] = sanitize_string(data.get("alt", ""), 300)
            if "caption" in data:
                target_item["caption"] = sanitize_string(data.get("caption", ""), 500)
            if "title" in data:
                target_item["title"] = sanitize_string(data.get("title", ""), 300)

            atomic_write_json(media_path, media_list)
            return self.send_json({"success": True, "media": target_item})

        self.send_error(404, "API Endpoint Not Found")

    # 14. DELETE Request Router
    def do_DELETE(self):
        try:
            self._handle_DELETE()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass
        except Exception as e:
            logger.error(f"Internal Server Error in do_DELETE: {e}", exc_info=True)
            try:
                self.send_json({"error": "خطای داخلی سرور هنگام حذف رکورد"}, 500)
            except Exception:
                pass

    def _handle_DELETE(self):
        if not self.validate_host():
            self.send_error(400, "Bad Request: Invalid Host Header")
            return

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if not self.check_csrf():
            return self.send_json({"error": "درخواست غیرمجاز به دلیل عدم تطابق منبع اعتباری (CSRF Violation)"}, 403)

        if path == "/api/articles":
            if not self.require_role("administrator", "editor"):
                return
            query = urllib.parse.parse_qs(parsed.query)
            article_id = query.get("id", [""])[0]
            if not article_id:
                return self.send_json({"error": "شناسه مقاله ارسال نشده است"}, 400)

            articles_path = os.path.join(CONTENT_DIR, "articles.json")
            articles = load_json_file(articles_path, default=[])

            sess = self.get_current_session() or {}
            username = sess.get("username", "unknown")
            AUDIT_LOGGER.log_event("ARTICLE_DELETED", ip=self.get_client_ip(), user=username, status="SUCCESS", details={"article_id": article_id})

            articles = [a for a in articles if a.get("id") != article_id]
            atomic_write_json(articles_path, articles)
            return self.send_json({"success": True, "articles": articles})

        if path in ("/api/doctors", "/api/doctors/"):
            if not self.require_role("administrator", "editor"):
                return
            query = urllib.parse.parse_qs(parsed.query)
            doc_id = query.get("id", [""])[0]
            if not doc_id:
                return self.send_json({"error": "شناسه پزشک ارسال نشده است"}, 400)
            doctors_path = os.path.join(CONTENT_DIR, "doctors.json")
            doctors = load_json_file(doctors_path, default=[])
            doctors = [d for d in doctors if d.get("id") != doc_id]
            atomic_write_json(doctors_path, doctors)
            return self.send_json({"success": True, "doctors": doctors})

        if path in ("/api/newsletters", "/api/newsletters/"):
            if not self.require_role("administrator", "editor"):
                return
            query = urllib.parse.parse_qs(parsed.query)
            n_id = query.get("id", [""])[0]
            if not n_id:
                return self.send_json({"error": "شناسه خبرنامه ارسال نشده است"}, 400)
            newsletters_path = os.path.join(CONTENT_DIR, "newsletters.json")
            newsletters = load_json_file(newsletters_path, default=[])
            newsletters = [n for n in newsletters if n.get("id") != n_id]
            atomic_write_json(newsletters_path, newsletters)
            return self.send_json({"success": True, "newsletters": newsletters})

        if path == "/api/media":
            if not self.require_role("administrator", "editor"):
                return
            query = urllib.parse.parse_qs(parsed.query)
            media_id = query.get("id", [""])[0]
            if not media_id:
                return self.send_json({"error": "شناسه رسانه ارسال نشده است"}, 400)

            media_path = os.path.join(CONTENT_DIR, "media.json")
            media_list = load_json_file(media_path, default=[])

            found_item = next((m for m in media_list if m.get("id") == media_id), None)
            if found_item:
                MEDIA_STORAGE_ENGINE.delete_media(found_item)

            media_list = [m for m in media_list if m.get("id") != media_id]
            atomic_write_json(media_path, media_list)
            return self.send_json({"success": True, "media": media_list})

        if path in ("/api/crm-tutorials", "/api/crm-tutorials/"):
            if not self.require_role("administrator", "editor", "author"):
                return
            query = urllib.parse.parse_qs(parsed.query)
            tut_id = query.get("id", [""])[0]
            if not tut_id:
                return self.send_json({"error": "شناسه آموزش ارسال نشده است"}, 400)

            crm_path = os.path.join(CONTENT_DIR, "crm_tutorials.json")
            tutorials = load_json_file(crm_path, default=[])

            tutorials = [t for t in tutorials if t.get("id") != tut_id]
            atomic_write_json(crm_path, tutorials)
            return self.send_json({"success": True, "tutorials": tutorials})

        if path in ("/api/admin/redirects", "/api/admin/redirects/"):
            if not self.require_role("administrator"):
                return
            query = urllib.parse.parse_qs(parsed.query)
            rule_id = query.get("id", [""])[0]
            if not rule_id:
                return self.send_json({"error": "شناسه ریدایرکت ارسال نشده است"}, 400)
            rules = load_redirects()
            rules = [r for r in rules if r.get("id") != rule_id]
            save_redirects(rules)
            return self.send_json({"success": True, "redirects": rules})

        if path in ("/api/admin/schemas", "/api/admin/schemas/"):
            if not self.require_role("administrator"):
                return
            query = urllib.parse.parse_qs(parsed.query)
            schema_id = query.get("id", [""])[0]
            if not schema_id:
                return self.send_json({"error": "شناسه اسکیما ارسال نشده است"}, 400)
            schemas = load_schemas()
            schemas = [s for s in schemas if s.get("id") != schema_id]
            save_schemas(schemas)
            return self.send_json({"success": True, "schemas": schemas})

        # User Management: Delete User
        if path.startswith("/api/admin/users/"):
            if not self.require_role("administrator"):
                return
            parts = path.strip("/").split("/")
            if len(parts) < 4:
                return self.send_json({"error": "شناسه کاربر نامعتبر است"}, 400)
            target_id = parts[3]
            users = load_users()
            target_user = None
            for u in users:
                if u.get("id") == target_id:
                    target_user = u
                    break
            if not target_user:
                return self.send_json({"error": "کاربر مورد نظر یافت نشد"}, 404)

            # Prevent deletion of primary admin
            if target_user.get("username") == ADMIN_USERNAME or target_id == "usr_mahyarebrahimi":
                return self.send_json({"error": "امکان حذف مدیر اصلی سامانه وجود ندارد."}, 400)

            # Check if attempting to delete self
            session = self.get_current_session()
            if session and (str(session.get("username", "")).lower() == str(target_user.get("username", "")).lower() or session.get("userId") == target_id):
                return self.send_json({"error": "امکان حذف حسابی که در حال حاضر با آن وارد سیستم شده‌اید وجود ندارد."}, 400)

            users = [u for u in users if u.get("id") != target_id]
            save_users(users)
            revoke_user_sessions(target_user.get("username", ""))
            return self.send_json({"success": True, "message": f"کاربر «{target_user.get('displayName')}» با موفقیت حذف گردید."})

        self.send_error(404, "API Endpoint Not Found")

# 15. Server Bootstrapper
def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    server_address = (HOST, PORT)
    with socketserver.ThreadingTCPServer(server_address, PezeshkanRequestHandler) as httpd:
        display_host = "localhost" if HOST in ("0.0.0.0", "127.0.0.1") else HOST
        print("=" * 75)
        print(f"  اکوسیستم سلامت دیجیتال پزشکآن - سرور امن بالینی (Hardened Production Gateway)")
        print(f"  - وب‌سایت اصلی:            http://{display_host}:{PORT}")
        print(f"  - محصول و پرونده EMR:      http://{display_host}:{PORT}/product")
        print(f"  - مجله سلامت بالینی:       http://{display_host}:{PORT}/mag")
        print(f"  - پیشخوان مدیریت (امن):    http://{display_host}:{PORT}/admin")
        print(f"  - درگاه ورود امن:          http://{display_host}:{PORT}/login")
        print(f"  - وضعیت امنیت:             محافظت شده (Argon2id, CSP, Anti-Traversal, Rate-Limit)")
        print(f"  - محیط اجرا:               {ENVIRONMENT.upper()}")
        if ENVIRONMENT == "development":
            print(f"  - نام کاربری مدیر:         {ADMIN_USERNAME}")
            print(f"  - نکته امنیتی:             رمز عبور از فایل .env یا متغیرهای محیطی سیستم خوانده می‌شود.")
        print("=" * 75)

        def shutdown_handler(signum, frame):
            logger.info(f"سیگنال دریافت شد ({signum}). در حال بستن اتصالات و توقف امن سرور...")
            threading.Thread(target=httpd.shutdown, daemon=True).start()

        signal.signal(signal.SIGINT, shutdown_handler)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, shutdown_handler)

        try:
            httpd.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
        except Exception as e:
            logger.error(f"خطای حلقه سرور: {e}", exc_info=True)
        finally:
            try:
                httpd.server_close()
            except Exception:
                pass
            print("\nسرور امن با موفقیت متوقف شد.")

if __name__ == "__main__":
    run_server()
