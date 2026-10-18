# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - Enterprise Middleware Layer
Includes Dynamic SEO Redirect Engine & Clinical Security Headers
"""

import re
import threading
from urllib.parse import urlparse
from django.conf import settings
from django.db import models
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.utils import timezone


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
    threading.Thread(target=_worker, daemon=True).start()


class RedirectAndSecurityMiddleware:
    """
    Handles dynamic SEO redirects, appointment booking aliases, and security headers.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
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
            from apps.pezeshkan_core.models import Redirect
            try:
                # Check exact match
                active_rules = list(Redirect.objects.filter(is_active=True))
                matched_rule = None
                target_url = None

                clean_path = path.rstrip('/') or '/'
                for rule in active_rules:
                    rule_source = rule.source.strip()
                    rule_clean = rule_source.rstrip('/') or '/'

                    if rule.match_type == 'exact' and clean_path == rule_clean:
                        matched_rule = rule
                        target_url = rule.target
                        break
                    elif rule.match_type == 'prefix' and clean_path.startswith(rule_clean):
                        matched_rule = rule
                        suffix = clean_path[len(rule_clean):]
                        target_url = rule.target.rstrip('/') + suffix
                        break
                    elif rule.match_type == 'regex':
                        try:
                            if re.search(rule_source, path):
                                matched_rule = rule
                                target_url = re.sub(rule_source, rule.target, path)
                                break
                        except Exception:
                            continue

                if matched_rule and target_url:
                    # Avoid infinite loop
                    if target_url.rstrip('/') != clean_path:
                        _record_redirect_hit(matched_rule.id)
                        if matched_rule.preserve_query and raw_query:
                            sep = '&' if '?' in target_url else '?'
                            target_url = f"{target_url}{sep}{raw_query}"

                        if matched_rule.status_code == 301:
                            return HttpResponsePermanentRedirect(target_url)
                        elif matched_rule.status_code == 302:
                            return HttpResponseRedirect(target_url)
                        elif matched_rule.status_code == 410:
                            return HttpResponse("410 Gone - This resource has been permanently removed.", status=410)
            except Exception:
                pass

        # 3. Continue Request
        response = self.get_response(request)

        # 4. Clinical Security Headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'

        return response
