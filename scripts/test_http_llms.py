import http.client
import json
import os
import socket
import sys
import threading
import time
from http.server import HTTPServer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_tests():
    port = get_free_port()
    print(f"[*] Starting ephemeral test server on port {port}...")

    httpd = HTTPServer(('127.0.0.1', port), server.PezeshkanRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    conn = http.client.HTTPConnection('127.0.0.1', port)

    try:
        # 1. Test unauthenticated access to /api/admin/llms
        print("[1] Testing unauthenticated GET /api/admin/llms...")
        conn.request('GET', '/api/admin/llms')
        res = conn.getresponse()
        data = res.read()
        print(f"    Status: {res.status} (Expected 401)")
        assert res.status == 401, f"Expected 401, got {res.status}"

        # 2. Login as admin
        print("[2] Logging in to /api/login...")
        login_payload = json.dumps({"username": "mahyarebrahimi", "password": "mahyebi86"}).encode('utf-8')
        conn.request('POST', '/api/login', body=login_payload, headers={'Content-Type': 'application/json'})
        res = conn.getresponse()
        cookie_header = res.getheader('Set-Cookie', '')
        res.read()
        print(f"    Login status: {res.status}, Cookie: {cookie_header}")
        assert res.status == 200, f"Login failed: {res.status}"
        auth_cookie = cookie_header.split(';')[0] if cookie_header else ''

        # 3. Authenticated GET /api/admin/llms
        print("[3] Testing authenticated GET /api/admin/llms...")
        conn.request('GET', '/api/admin/llms', headers={'Cookie': auth_cookie})
        res = conn.getresponse()
        body = json.loads(res.read().decode('utf-8'))
        print(f"    Status: {res.status}")
        assert res.status == 200, f"Expected 200, got {res.status}"
        assert 'settings' in body, "Response missing 'settings'"
        assert 'preview' in body, "Response missing 'preview'"
        print(f"    Current enabled: {body['settings'].get('enabled')}")
        print(f"    Post types: {body['settings'].get('postTypes')}")
        print(f"    Preview length: {len(body['preview'])} chars")

        # 4. Test live preview generation via POST /api/admin/llms/preview
        print("[4] Testing POST /api/admin/llms/preview...")
        preview_payload = {
            "enabled": True,
            "postTypes": {"posts": True, "pages": False, "floating": False},
            "taxonomies": {"categories": True, "tags": False},
            "postLimit": 10,
            "additionalContent": "## Custom Note\n- Live test addition."
        }
        conn.request('POST', '/api/admin/llms/preview',
                     body=json.dumps(preview_payload).encode('utf-8'),
                     headers={'Content-Type': 'application/json', 'Cookie': auth_cookie})
        res = conn.getresponse()
        preview_res = json.loads(res.read().decode('utf-8'))
        print(f"    Status: {res.status}")
        assert res.status == 200
        assert 'Custom Note' in preview_res['preview'], "Custom content missing from preview"

        # 5. Test saving settings via POST /api/admin/llms
        print("[5] Testing POST /api/admin/llms...")
        save_payload = {
            "enabled": True,
            "postTypes": {"posts": True, "pages": True, "floating": True},
            "taxonomies": {"categories": True, "tags": True},
            "postLimit": 50,
            "additionalContent": "## راهنمای مدل‌های زبانی هوش مصنوعی\n- برای پرسش‌های بالینی از ارجاعات مقالات علمی استفاده کنید."
        }
        conn.request('POST', '/api/admin/llms',
                     body=json.dumps(save_payload).encode('utf-8'),
                     headers={'Content-Type': 'application/json', 'Cookie': auth_cookie})
        res = conn.getresponse()
        save_res = json.loads(res.read().decode('utf-8'))
        print(f"    Status: {res.status}")
        assert res.status == 200
        assert save_res.get('ok') is True

        # Verify llms.txt exists on disk
        llms_path = os.path.join(os.path.dirname(__file__), '..', 'llms.txt')
        assert os.path.exists(llms_path), "llms.txt file was not written to disk"
        with open(llms_path, 'r', encoding='utf-8') as f:
            disk_content = f.read()
        print(f"    Disk llms.txt size: {len(disk_content)} bytes")
        assert "## راهنمای مدل‌های زبانی هوش مصنوعی" in disk_content

        # 6. Test public endpoint /llms.txt
        print("[6] Testing public GET /llms.txt...")
        conn.request('GET', '/llms.txt')
        res = conn.getresponse()
        public_data = res.read().decode('utf-8')
        print(f"    Status: {res.status}, Content-Type: {res.getheader('Content-Type')}")
        assert res.status == 200
        assert 'text/plain' in res.getheader('Content-Type', '')
        assert '# پزشکآن' in public_data
        assert 'مقالات و راهنماهای بالینی' in public_data

        # 7. Test public endpoint alias /llm.txt
        print("[7] Testing public alias GET /llm.txt...")
        conn.request('GET', '/llm.txt')
        res = conn.getresponse()
        alias_data = res.read().decode('utf-8')
        print(f"    Status: {res.status}")
        assert res.status == 200
        assert alias_data == public_data

        # 8. Test disabling llms.txt
        print("[8] Testing disabling llms.txt...")
        disable_payload = {
            "enabled": False,
            "postTypes": {"posts": True, "pages": True, "floating": True},
            "taxonomies": {"categories": True, "tags": True},
            "postLimit": 50,
            "additionalContent": ""
        }
        conn.request('POST', '/api/admin/llms',
                     body=json.dumps(disable_payload).encode('utf-8'),
                     headers={'Content-Type': 'application/json', 'Cookie': auth_cookie})
        res = conn.getresponse()
        res.read()
        assert res.status == 200

        conn.request('GET', '/llms.txt')
        res = conn.getresponse()
        res.read()
        print(f"    Disabled status: {res.status} (Expected 404)")
        assert res.status == 404

        # 9. Re-enable llms.txt
        print("[9] Re-enabling llms.txt...")
        save_payload["enabled"] = True
        conn.request('POST', '/api/admin/llms',
                     body=json.dumps(save_payload).encode('utf-8'),
                     headers={'Content-Type': 'application/json', 'Cookie': auth_cookie})
        res = conn.getresponse()
        res.read()
        assert res.status == 200

        conn.request('GET', '/llms.txt')
        res = conn.getresponse()
        assert res.status == 200
        res.read()

        print("\n[SUCCESS] All LLMS.txt backend and public tests passed!")
    finally:
        conn.close()
        httpd.shutdown()

if __name__ == '__main__':
    run_tests()
