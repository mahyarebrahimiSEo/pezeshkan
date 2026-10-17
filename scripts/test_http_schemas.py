# -*- coding: utf-8 -*-
"""
Live HTTP-Level Integration Test for Pezeshkan Rank Math Schema Management System
Spawns PezeshkanRequestHandler on a test port, logs in as admin, and executes live HTTP requests against all schema endpoints.
"""
import http.client
import socketserver
import threading
import time
import os
import sys
import json
import urllib.parse

# UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import server

TEST_PORT = 39872

def run_http_schema_tests():
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", TEST_PORT), server.PezeshkanRequestHandler)
    srv_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    srv_thread.start()
    time.sleep(0.5)

    print("=" * 65)
    print("  آزمایش زنده سوکت HTTP برای اندپوینت‌های استودیو اسکیما (Rank Math API)")
    print("=" * 65)

    try:
        # 1. Test Unauthenticated Access -> 401
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/api/admin/schemas")
        resp = conn.getresponse()
        assert resp.status == 401, f"Expected 401 for unauthenticated request, got {resp.status}"
        print("  [1] PASS: رد درخواست دسترسی غیرمجاز (HTTP 401) بدون نشست احراز هویت")
        conn.close()

        # 2. Login to get admin session cookie
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        login_payload = json.dumps({"username": server.ADMIN_USERNAME, "password": server.ADMIN_PASSWORD})
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/api/login", body=login_payload, headers=headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Login failed with status {resp.status}"
        set_cookie = resp.getheader("Set-Cookie")
        assert set_cookie, "Set-Cookie header missing in login response"
        # Extract cookie value
        cookie_val = set_cookie.split(";")[0]
        auth_headers = {"Cookie": cookie_val, "Content-Type": "application/json"}
        print(f"  [2] PASS: ورود موفقیت‌آمیز مدیر به سامانه و دریافت کوکی امن: {cookie_val[:25]}...")
        conn.close()

        # 3. GET /api/admin/schemas with auth
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        conn.request("GET", "/api/admin/schemas", headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        data = json.loads(resp.read().decode("utf-8"))
        assert data.get("success") is True, "Expected success: True"
        schemas = data.get("schemas", [])
        assert len(schemas) >= 5, f"Expected at least 5 schemas, got {len(schemas)}"
        print(f"  [3] PASS: دریافت موفقیت‌آمیز فهرست {len(schemas)} اسکیما از سرور با احراز هویت")
        conn.close()

        # 4. POST /api/admin/schemas/validate (Valid payload)
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        valid_payload = json.dumps({
            "schema": {
                "@context": "https://schema.org",
                "@type": "MedicalWebPage",
                "headline": "پروتکل بالینی فیزیوتراپی و دیسک کمر",
                "description": "دستورالعمل جامع مداخلات کم‌تهاجمی"
            }
        })
        conn.request("POST", "/api/admin/schemas/validate", body=valid_payload, headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        val_res = json.loads(resp.read().decode("utf-8"))
        assert val_res.get("valid") is True, f"Expected valid: True, got {val_res}"
        print("  [4] PASS: اعتبارسنجی سرور برای اسکیمای معتبر پزشکی تایید شد (Valid: True)")
        conn.close()

        # 5. POST /api/admin/schemas/validate (Invalid payload - missing @context)
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        invalid_payload = json.dumps({
            "schema": {
                "@type": "MedicalWebPage",
                "headline": "فاقد کانتکست"
            }
        })
        conn.request("POST", "/api/admin/schemas/validate", body=invalid_payload, headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        val_res = json.loads(resp.read().decode("utf-8"))
        assert val_res.get("valid") is False, f"Expected valid: False, got {val_res}"
        print(f"  [5] PASS: ممانعت هوشمند سرور از ثبت اسکیمای نامعتبر: {val_res.get('error')}")
        conn.close()

        # 6. POST /api/admin/schemas (Create test schema)
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        new_schema_payload = json.dumps({
            "name": "اسکیمای تستی واحد کنترل کیفیت سئو",
            "targetUrl": "/test-qa-schema",
            "schemaType": "HowTo",
            "scope": "page",
            "description": "تست اتوماسیون",
            "data": {},
            "isActive": True
        })
        conn.request("POST", "/api/admin/schemas", body=new_schema_payload, headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        res_data = json.loads(resp.read().decode("utf-8"))
        created_id = res_data.get("schema", {}).get("id")
        assert created_id, "Expected created schema id"
        print(f"  [6] PASS: ثبت اسکیمای جدید در سرور با شناسه یکتا: {created_id}")
        conn.close()

        # 7. POST /api/admin/schemas/toggle
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        toggle_payload = json.dumps({"id": created_id})
        conn.request("POST", "/api/admin/schemas/toggle", body=toggle_payload, headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        res_toggle = json.loads(resp.read().decode("utf-8"))
        toggled_item = next((s for s in res_toggle.get("schemas", []) if s.get("id") == created_id), None)
        assert toggled_item and toggled_item.get("isActive") is False, "Expected isActive to be toggled to False"
        print("  [7] PASS: سوییچ وضعیت فعال/غیرفعال اسکیمای صفحه با موفقیت اعمال گردید")
        conn.close()

        # 8. POST /api/admin/schemas/delete (Cleanup test schema)
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        del_payload = json.dumps({"id": created_id})
        conn.request("POST", "/api/admin/schemas/delete", body=del_payload, headers=auth_headers)
        resp = conn.getresponse()
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        res_del = json.loads(resp.read().decode("utf-8"))
        assert not any(s.get("id") == created_id for s in res_del.get("schemas", [])), "Schema was not deleted"
        print(f"  [8] PASS: پاکسازی و حذف امن رکورد تستی {created_id} با موفقیت تایید شد")
        conn.close()

        print("=" * 65)
        print("  تمامی آزمایش‌های زنده اندپوینت‌های HTTP اسکیما با موفقیت کامل ۱۰۰٪ سپری شدند!")
        print("=" * 65)

    finally:
        httpd.shutdown()
        httpd.server_close()

if __name__ == "__main__":
    run_http_schema_tests()
