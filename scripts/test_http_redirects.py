# -*- coding: utf-8 -*-
"""
Live HTTP-Level Integration Test for Pezeshkan Redirect System
Spawns PezeshkanRequestHandler on a test port, fires live HTTP requests, and verifies headers and response codes.
"""
import http.client
import socketserver
import threading
import time
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import server

TEST_PORT = 39871

def run_http_tests():
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", TEST_PORT), server.PezeshkanRequestHandler)
    srv_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    srv_thread.start()
    time.sleep(0.5)

    print("=" * 60)
    print("  Live HTTP Socket & Header Verifications")
    print("=" * 60)

    try:
        # 1. Test 301 Redirect on /tariffs
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/tariffs")
        resp = conn.getresponse()
        assert resp.status == 301, f"Expected status 301, got {resp.status}"
        assert resp.getheader("Location") == "/packages", f"Expected Location /packages, got {resp.getheader('Location')}"
        assert "max-age=86400" in (resp.getheader("Cache-Control") or ""), "Expected public cache header on 301"
        print("  PASS: HTTP 301 Permanent Redirect on /tariffs verified with Location and Cache-Control headers")
        conn.close()

        # 2. Test 302 Redirect with Query Preservation on /demo?utm_source=seo_audit
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/demo?utm_source=seo_audit")
        resp = conn.getresponse()
        assert resp.status == 302, f"Expected status 302, got {resp.status}"
        assert resp.getheader("Location") == "/start?utm_source=seo_audit", f"Expected preserved query, got {resp.getheader('Location')}"
        assert "no-cache" in (resp.getheader("Cache-Control") or ""), "Expected no-cache on 302"
        print("  PASS: HTTP 302 Found Redirect with UTM preservation verified")
        conn.close()

        # 3. Test Prefix 301 on /old-blog/cardiology-101
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/old-blog/cardiology-101")
        resp = conn.getresponse()
        assert resp.status == 301, f"Expected status 301, got {resp.status}"
        assert resp.getheader("Location") == "/mag/cardiology-101", f"Expected Location /mag/cardiology-101, got {resp.getheader('Location')}"
        print("  PASS: Prefix Match /old-blog/* -> /mag/* verified")
        conn.close()

        # 4. Test 410 Gone on /campaign-2025-expired
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/campaign-2025-expired")
        resp = conn.getresponse()
        assert resp.status == 410, f"Expected status 410, got {resp.status}"
        assert resp.getheader("X-Robots-Tag") == "noindex, noarchive", f"Expected X-Robots-Tag header, got {resp.getheader('X-Robots-Tag')}"
        body = resp.read().decode("utf-8")
        assert "۴۱۰" in body, "Expected Persian 410 page body"
        print("  PASS: HTTP 410 Gone verified with X-Robots-Tag: noindex, noarchive and branded Persian UI")
        conn.close()

        # 5. Test Canonical SEO Redirect on /product.html
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/product.html")
        resp = conn.getresponse()
        assert resp.status == 301, f"Expected status 301, got {resp.status}"
        assert resp.getheader("Location") == "/product", f"Expected Location /product, got {resp.getheader('Location')}"
        print("  PASS: Canonical .html stripping redirect verified")
        conn.close()

        print("\nALL HTTP INTEGRATION TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
    finally:
        httpd.shutdown()

if __name__ == "__main__":
    run_http_tests()
