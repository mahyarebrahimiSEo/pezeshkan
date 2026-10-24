# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - Enterprise Middleware Layer
Includes Dynamic SEO Redirect Engine & Clinical Security Headers
Built on Django's canonical MiddlewareMixin for seamless sync & async execution.
"""

import re
import time
import concurrent.futures
from django.conf import settings
from django.db import models
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

# Bounded executor for logging hits without crashing under high concurrency
_HIT_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=4, thread_name_prefix="RedirectLogger")
_REDIRECTS_CACHE = None
_REDIRECTS_CACHE_TIME = 0


def _record_redirect_hit(redirect_id):
    def _worker():
        try:
            from apps.pezeshkan_core.models import Redirect
            Redirect.objects.filter(id=redirect_id).update(
                hit_count=models.F('hit_count') + 1,
                last_hit=timezone.now()
            )
        except Exception:
            pass
    try:
        _HIT_EXECUTOR.submit(_worker)
    except Exception:
        pass


def get_active_redirects():
    global _REDIRECTS_CACHE, _REDIRECTS_CACHE_TIME
    now = time.time()
    if _REDIRECTS_CACHE is not None and (now - _REDIRECTS_CACHE_TIME) < 60:
        return _REDIRECTS_CACHE
    try:
        from apps.pezeshkan_core.models import Redirect
        _REDIRECTS_CACHE = list(Redirect.objects.filter(is_active=True))
        _REDIRECTS_CACHE_TIME = now
    except Exception:
        _REDIRECTS_CACHE = []
    return _REDIRECTS_CACHE


class RedirectAndSecurityMiddleware(MiddlewareMixin):
    """
    Handles dynamic SEO redirects, appointment booking aliases, and security headers.
    High-concurrency optimized with in-memory caching and bounded thread pool.
    Fully compatible with sync views, async views, WSGI, and ASGI via MiddlewareMixin.
    """
    def process_request(self, request):
        path = request.path
        raw_query = request.META.get('QUERY_STRING', '')

        # 1. Appointment System Aliases (Always 301 Redirect)
        if path.rstrip('/') in ('/nobat', '/nobat-dehi', '/reserve', '/booking', '/appointment'):
            target = getattr(settings, 'APPOINTMENT_SYSTEM_URL', '') or '/appointments'
            if raw_query:
                target += f"?{raw_query}"
            return HttpResponsePermanentRedirect(target)

        # 2. Dynamic SEO Redirects (Skip for static, media, admin, and api)
        if not path.startswith(('/static/', '/uploads/', '/api/', '/admin/')):
            try:
                active_rules = get_active_redirects()
                clean_path = path.rstrip('/') or '/'
                for rule in active_rules:
                    rule_source = rule.source.strip()
                    rule_clean = rule_source.rstrip('/') or '/'

                    matched = False
                    target_url = None
                    if rule.match_type == 'exact' and clean_path == rule_clean:
                        matched = True
                        target_url = rule.target
                    elif rule.match_type == 'prefix' and clean_path.startswith(rule_clean):
                        matched = True
                        suffix = clean_path[len(rule_clean):]
                        target_url = rule.target.rstrip('/') + suffix
                    elif rule.match_type == 'regex':
                        try:
                            if re.search(rule_source, path):
                                matched = True
                                target_url = re.sub(rule_source, rule.target, path)
                        except Exception:
                            continue

                    if matched and target_url and target_url.rstrip('/') != clean_path:
                        _record_redirect_hit(rule.id)
                        if rule.preserve_query and raw_query:
                            sep = '&' if '?' in target_url else '?'
                            target_url = f"{target_url}{sep}{raw_query}"

                        if rule.status_code == 301:
                            return HttpResponsePermanentRedirect(target_url)
                        elif rule.status_code == 302:
                            return HttpResponseRedirect(target_url)
                        elif rule.status_code == 410:
                            return HttpResponse("410 Gone - This resource has been permanently removed.", status=410)
            except Exception:
                pass

        return None

    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        return response
