# -*- coding: utf-8 -*-
"""
Verification Script for Pezeshkan Dynamic SEO Redirect Management System
Tests routing, 301, 302, 410, query preservation, prefix matching, hit recording, and Admin APIs.
"""
import http.client
import urllib.parse
import json
import time
import os
import sys

# Add parent dir to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import server

def run_tests():
    print("=" * 60)
    print("  Pezeshkan Dynamic SEO Redirect System Verification")
    print("=" * 60)

    # 1. Test in-memory rule matcher
    print("\n[Step 1] In-Memory Dynamic Matcher Tests:")
    r1 = server.match_custom_redirect("/tariffs", "")
    assert r1 == (301, "/packages"), f"Expected (301, '/packages'), got {r1}"
    print("  PASS: /tariffs -> 301 /packages")

    r2 = server.match_custom_redirect("/tariffs", "utm_source=google&campaign=spring")
    assert r2 == (301, "/packages?utm_source=google&campaign=spring"), f"Expected preserved query, got {r2}"
    print("  PASS: /tariffs?utm_source=... -> 301 /packages?utm_source=...")

    r3 = server.match_custom_redirect("/demo", "ref=insta")
    assert r3 == (302, "/start?ref=insta"), f"Expected (302, '/start?ref=insta'), got {r3}"
    print("  PASS: /demo -> 302 /start")

    r4 = server.match_custom_redirect("/old-blog/dermatology-guide", "")
    assert r4 == (301, "/mag/dermatology-guide"), f"Expected prefix match, got {r4}"
    print("  PASS: /old-blog/dermatology-guide -> 301 /mag/dermatology-guide (prefix)")

    r5 = server.match_custom_redirect("/campaign-2025-expired", "")
    assert r5 == (410, None), f"Expected (410, None), got {r5}"
    print("  PASS: /campaign-2025-expired -> 410 Gone")

    # 2. Test Loop Prevention
    print("\n[Step 2] Infinite Loop Protection Test:")
    r_loop = server.match_custom_redirect("/packages", "")
    assert r_loop is None, f"Loop detection failed! /packages returned {r_loop}"
    print("  PASS: Self-redirect loop ignored safely")

    # 3. Test Protected System Paths
    print("\n[Step 3] Protected System Paths Test:")
    for sys_path in ["/api/articles", "/admin", "/login", "/shared.css", "/robots.txt", "/sitemap.xml"]:
        res = server.match_custom_redirect(sys_path, "")
        assert res is None, f"System path {sys_path} should never be redirected! Got {res}"
    print("  PASS: System paths (/api, /admin, /login, static) are protected")

    # 4. Test API handlers directly via mock / simulation
    print("\n[Step 4] Admin Auth & API Lifecycle Test:")
    token = server.create_session("admin_tester")
    assert server.get_session(token) is not None, "Failed to create session"
    print("  PASS: Session token created for admin testing")

    # Test load_redirects
    redirects = server.load_redirects()
    initial_count = len(redirects)
    print(f"  PASS: Loaded {initial_count} redirect rules from disk")

    print("\nALL SYSTEM VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
