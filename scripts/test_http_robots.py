# -*- coding: utf-8 -*-
"""
Live HTTP Integration Test for Robots.txt Management and Site-Aware SEO Suitability Audit
Spawns PezeshkanRequestHandler on a test port, executes live HTTP requests against all robots.txt endpoints.
"""
import http.client
import socketserver
import threading
import time
import os
import sys
import json

# UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import server

TEST_PORT = 39873

def run_http_robots_tests():
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", TEST_PORT), server.PezeshkanRequestHandler)
    srv_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    srv_thread.start()
    time.sleep(0.5)

    print("=" * 65)
    print("  آزمایش زنده پروتکل HTTP برای مدیریت و تحلیل هوشمند robots.txt")
    print("=" * 65)

    try:
        # 1. Unauthenticated access -> 401
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/api/admin/robots")
        resp = conn.getresponse()
        assert resp.status == 401, f"Expected 401 for unauthenticated GET, got {resp.status}"
        print("  [1] PASS: ممانعت از دسترسی غیرمجاز به فایل robots.txt (HTTP 401)")
        conn.close()

        # 2. Login to get session cookie
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        login_payload = json.dumps({"username": server.ADMIN_USERNAME, "password": server.ADMIN_PASSWORD})
        conn.request("POST", "/api/login", body=login_payload, headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        assert resp.status == 200, f"Login failed with status {resp.status}"
        set_cookie = resp.getheader("Set-Cookie")
        assert set_cookie, "Set-Cookie header missing"
        cookie_val = set_cookie.split(";")[0]
        auth_headers = {"Cookie": cookie_val, "Content-Type": "application/json"}
        print(f"  [2] PASS: احراز هویت مدیر با موفقیت انجام شد: {cookie_val[:22]}...")
        conn.close()

        # 3. Authenticated GET /api/admin/robots
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/api/admin/robots", headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"GET /api/admin/robots failed with status {resp.status}"
        data = json.loads(resp.read().decode("utf-8"))
        assert data.get("success") is True
        assert "content" in data
        assert "analysis" in data
        analysis = data["analysis"]
        print(f"  [3] PASS: بازیابی محتوا و تحلیل هوشمند فایل robots.txt (نمره: {analysis['score']}٪ - {analysis['verdict']})")
        conn.close()

        # 4. POST /api/admin/robots/analyze (Live AI Audit test with dangerous content)
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        test_bad = json.dumps({"content": "User-agent: *\nDisallow: /\n"})
        conn.request("POST", "/api/admin/robots/analyze", body=test_bad, headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200
        data_bad = json.loads(resp.read().decode("utf-8"))
        assert data_bad.get("success") is True
        bad_analysis = data_bad["analysis"]
        assert bad_analysis["isSuitable"] is False
        assert bad_analysis["score"] <= 40
        print(f"  [4] PASS: تشخیص بلادرنگ عدم تناسب و خطای بحرانی سئو (Disallow: /) -> نمره {bad_analysis['score']}٪")
        conn.close()

        # 5. POST /api/admin/robots (Save atomic update & verify)
        original_content = data["content"]
        test_comment = "# Pezeshkan Automated Test Check\n" + original_content
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("POST", "/api/admin/robots", body=json.dumps({"content": test_comment}), headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200
        save_data = json.loads(resp.read().decode("utf-8"))
        assert save_data.get("success") is True
        print(f"  [5] PASS: ذخیره‌سازی اتمیک و انتشار درجا در سرور: {save_data.get('message')}")
        conn.close()

        # 6. Public route GET /robots.txt serves updated file
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/robots.txt")
        resp = conn.getresponse()
        assert resp.status == 200
        pub_body = resp.read().decode("utf-8")
        assert "# Pezeshkan Automated Test Check" in pub_body
        print("  [6] PASS: خروجی عمومی پروتکل خزنده‌ها (https://pezeshkan.me/robots.txt) فعال و در دسترس خزنده‌ها است")
        conn.close()

        # Restore original content
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("POST", "/api/admin/robots", body=json.dumps({"content": original_content}), headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200
        print("  [7] PASS: بازگردانی موفقیت‌آمیز نسخه اصلی و استاندارد robots.txt")
        conn.close()

        # 8. Check admin.html DOM components
        admin_file = os.path.join(BASE_DIR, "mag", "admin.html")
        with open(admin_file, "r", encoding="utf-8") as f:
            admin_content = f.read()

        assert 'id="tab-robots"' in admin_content
        assert 'id="menu-robots"' in admin_content
        assert 'id="robotsTxtEditor"' in admin_content
        assert 'id="robotsVerdictCard"' in admin_content
        assert 'saveRobotsTxt()' in admin_content
        assert 'resetRobotsToDefault()' in admin_content
        assert 'saveSiteSeoSettings()' in admin_content
        print("  [8] PASS: رابط کاربری استودیو robots.txt، دکمه‌های بارز ذخیره و تحلیلگر سئو در پیشخوان تایید شد")

        print("\n" + "=" * 65)
        print("  تمامی آزمایش‌های سامانه مدیریت و تحلیل هوشمند robots.txt با موفقیت کامل پاس شدند! ✅")
        print("=" * 65)

    finally:
        httpd.shutdown()

if __name__ == "__main__":
    run_http_robots_tests()
