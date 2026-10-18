# -*- coding: utf-8 -*-
"""
Live Integration Test for Pezeshkan Backend Audit Fixes & Appointment System
Tests:
1. Aliases & Redirects (/nobat, /nobat-dehi, /reserve, etc.)
2. Appointment Booking (POST /api/appointments) & Duplicate Conflict Prevention
3. Appointment Tracking (GET /api/appointments?code=... / phone=...)
4. Doctor Management (POST /api/doctors)
5. Settings Deep Merge (PUT /api/settings preserving existing keys)
6. Redirect Hit Counting and Lock Re-entrancy
"""

import http.client
import socketserver
import threading
import time
import os
import sys
import json
import urllib.parse

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import server

TEST_PORT = 39873

def run_tests():
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", TEST_PORT), server.PezeshkanRequestHandler)
    srv_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    srv_thread.start()
    time.sleep(0.5)

    print("=" * 65)
    print("  آزمایش جامع یکپارچگی بک‌اند، سیستم نوبت‌دهی و ادغام تنظیمات")
    print("=" * 65)

    try:
        # 1. Test 301 Redirects for Appointment Aliases
        for alias in ["/nobat", "/nobat-dehi", "/reserve", "/booking", "/appointment"]:
            conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
            conn.request("GET", alias)
            resp = conn.getresponse()
            assert resp.status == 301, f"Expected 301 for {alias}, got {resp.status}"
            loc = resp.getheader("Location")
            assert loc == "/appointments" or (server.APPOINTMENT_SYSTEM_URL and loc == server.APPOINTMENT_SYSTEM_URL), f"Unexpected location {loc}"
            conn.close()
        print("  [1] PASS: تغییر مسیر خودکار و ریدایرکت ۳۰۱ برای نام‌های مستعار نوبت‌دهی (/nobat, /reserve, ...)")

        # 2. Test Booking New Appointment via POST /api/appointments
        unique_slot = f"slot_{int(time.time())}"
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        booking_payload = json.dumps({
            "doctorId": "999",
            "doctorName": "دکتر آزمایشی سینا",
            "patientName": "بیمار تستی",
            "patientPhone": "09129998877",
            "nationalId": "0011223344",
            "dateLabel": "1405-07-20",
            "timeSlot": unique_slot,
            "notes": "ویزیت چکاپ قلب"
        })
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/api/appointments", body=booking_payload, headers=headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200 for appointment booking, got {resp.status}"
        resp_data = json.loads(resp.read().decode("utf-8"))
        assert resp_data.get("ok") is True or resp_data.get("success") is True, f"Booking response not ok: {resp_data}"
        tracking_code = resp_data.get("trackingCode")
        assert tracking_code and tracking_code.startswith("PZ-"), f"Invalid tracking code: {tracking_code}"
        print(f"  [2] PASS: ثبت نوبت جدید با موفقیت و صدور کد رهگیری معتبر: {tracking_code}")
        conn.close()

        # 3. Test Duplicate Booking Prevention (409 Conflict)
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("POST", "/api/appointments", body=booking_payload, headers=headers)
        resp = conn.getresponse()
        assert resp.status == 409, f"Expected 409 conflict for duplicate booking, got {resp.status}"
        print("  [3] PASS: جلوگیری هوشمند از نوبت‌دهی تکراری و بازگشت خطای ۴۰۹ (Double-booking Prevention)")
        conn.close()

        # 4. Test Appointment Tracking via GET /api/appointments?code=...
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", f"/api/appointments?code={tracking_code}")
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200 for tracking code query, got {resp.status}"
        found_data = json.loads(resp.read().decode("utf-8"))
        assert found_data.get("trackingCode") == tracking_code, "Tracking code mismatch"
        print(f"  [4] PASS: استعلام عمومی نوبت توسط بیمار با کد پیگیری {tracking_code}")
        conn.close()

        # 5. Login as Admin
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        login_payload = json.dumps({"username": server.ADMIN_USERNAME, "password": server.ADMIN_PASSWORD})
        conn.request("POST", "/api/login", body=login_payload, headers=headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Login failed with status {resp.status}"
        set_cookie = resp.getheader("Set-Cookie")
        assert set_cookie, "Set-Cookie header missing"
        cookie_val = set_cookie.split(";")[0]
        auth_headers = {
            "Cookie": cookie_val,
            "Content-Type": "application/json",
            "Origin": f"http://127.0.0.1:{TEST_PORT}",
            "Referer": f"http://127.0.0.1:{TEST_PORT}/admin.html"
        }
        print("  [5] PASS: لاگین مدیر ارشد و ایجاد نشست احراز هویت ادمین")
        conn.close()

        # 6. Admin GET /api/admin/appointments
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/api/admin/appointments", headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200 for admin appointments, got {resp.status}"
        admin_apps = json.loads(resp.read().decode("utf-8"))
        if isinstance(admin_apps, dict) and "appointments" in admin_apps:
            admin_apps = admin_apps["appointments"]
        assert any(a.get("trackingCode") == tracking_code for a in admin_apps), "Created appointment not in admin list"
        print(f"  [6] PASS: دریافت فهرست نوبت‌های ثبت‌شده در پیشخوان مدیریت (تعداد: {len(admin_apps)})")
        conn.close()

        # 7. Test POST /api/doctors (Creating new doctor from admin)
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        new_doc = {
            "id": "doc_test_888",
            "name": "دکتر آزمایشی نوین",
            "title": "متخصص جراحی مغز و اعصاب",
            "mcNumber": "MC-888999",
            "dept": "جراحی مغز",
            "rating": 5.0,
            "reviewsCount": 12
        }
        conn.request("POST", "/api/doctors", body=json.dumps(new_doc), headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200 for POST /api/doctors, got {resp.status}"
        print("  [7] PASS: ثبت و ذخیره‌سازی پزشک جدید از طریق اندپوینت مدیریت POST /api/doctors")
        conn.close()

        # 8. Test Settings Deep Merge (PUT /api/settings)
        # Fetch current settings first
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/api/settings")
        resp = conn.getresponse()
        curr_settings = json.loads(resp.read().decode("utf-8"))
        original_title = curr_settings.get("siteTitle")
        conn.close()

        # Update only partial SEO setting
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        partial_update = {
            "seo": {
                "googleSiteVerification": "AUDIT_VERIFY_TOKEN_999",
                "bingVerification": "BING_TOKEN_888"
            }
        }
        conn.request("PUT", "/api/settings", body=json.dumps(partial_update), headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200 for PUT /api/settings, got {resp.status}"
        updated_resp = json.loads(resp.read().decode("utf-8"))
        updated_settings = updated_resp.get("settings", updated_resp)
        
        # Verify deep merge: siteTitle must NOT be erased!
        assert updated_settings.get("siteTitle") == original_title, f"siteTitle was wiped! Expected {original_title}, got {updated_settings.get('siteTitle')}"
        assert updated_settings.get("seo", {}).get("googleSiteVerification") == "AUDIT_VERIFY_TOKEN_999", "SEO verification token missing"
        print("  [8] PASS: ادغام بازگشتی و عمیق تنظیمات (Deep Merge) بدون پاک شدن عنوان سایت و داده‌های حیاتی")
        conn.close()

        # 9. Test Lock Re-entrancy during redirect tracking
        try:
            server.record_redirect_hit("/test-reentrant-slug")
            print("  [9] PASS: عملکرد ایمن RLock و جلوگیری از Deadlock در ثبت آمار ریدایرکت‌ها")
        except Exception as e:
            raise AssertionError(f"Lock deadlock occurred: {e}")

        print("=" * 65)
        print("🎉 تمام آزمایش‌های بک‌اند و سیستم نوبت‌دهی با موفقیت ۱۰۰٪ پاس شدند!")
        print("=" * 65)

    finally:
        httpd.shutdown()

if __name__ == "__main__":
    run_tests()
