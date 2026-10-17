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
        # 1. Unauthenticated request to /api/admin/users -> 401
        print("[1] Testing unauthenticated GET /api/admin/users...")
        conn.request('GET', '/api/admin/users')
        res = conn.getresponse()
        res.read()
        print(f"    Status: {res.status} (Expected 401)")
        assert res.status == 401, f"Expected 401, got {res.status}"

        # 2. Login with admin credentials (mahyarebrahimi / mahyebi86)
        print("[2] Logging in as admin (mahyarebrahimi)...")
        login_payload = json.dumps({"username": "mahyarebrahimi", "password": "mahyebi86"}).encode('utf-8')
        conn.request('POST', '/api/login', body=login_payload, headers={'Content-Type': 'application/json'})
        res = conn.getresponse()
        cookie_header = res.getheader('Set-Cookie', '')
        login_data = json.loads(res.read().decode('utf-8'))
        print(f"    Login status: {res.status}, DisplayName: {login_data.get('user', {}).get('displayName')}")
        assert res.status == 200, f"Login failed: {res.status}"
        assert login_data.get('user', {}).get('displayName') == "مهیار ابراهیمی", "Expected displayName 'مهیار ابراهیمی'"
        auth_cookie = cookie_header.split(';')[0] if cookie_header else ''

        # 3. Authenticated GET /api/admin/users
        print("[3] Testing authenticated GET /api/admin/users...")
        conn.request('GET', '/api/admin/users', headers={'Cookie': auth_cookie})
        res = conn.getresponse()
        body = json.loads(res.read().decode('utf-8'))
        print(f"    Status: {res.status}, Total users: {len(body.get('users', []))}")
        assert res.status == 200
        assert body.get('success') is True
        users = body.get('users', [])
        assert len(users) >= 5, "Expected at least 5 initial users"

        # Security check: passwordHash and passwordSalt must NOT be exposed!
        for u in users:
            assert 'passwordHash' not in u, f"Security Violation: passwordHash exposed for user {u.get('username')}"
            assert 'passwordSalt' not in u, f"Security Violation: passwordSalt exposed for user {u.get('username')}"

        mahyar_user = next((u for u in users if u.get('username') == 'mahyarebrahimi'), None)
        assert mahyar_user is not None
        assert mahyar_user.get('displayName') == "مهیار ابراهیمی"
        print(f"    Mahyar user verified: role={mahyar_user.get('role')}, displayName={mahyar_user.get('displayName')}")

        # 4. Create new user via POST /api/admin/users
        print("[4] Testing POST /api/admin/users (Create new author)...")
        # 4a. Reject short password
        bad_payload = json.dumps({
            "username": "dr_rostami",
            "password": "123",
            "displayName": "دکتر نیلوفر رستمی",
            "email": "rostami@pezeshkan.me",
            "role": "author"
        }).encode('utf-8')
        conn.request('POST', '/api/admin/users', body=bad_payload,
                     headers={'Content-Type': 'application/json', 'Cookie': auth_cookie})
        res = conn.getresponse()
        res.read()
        print(f"    Short password rejection status: {res.status} (Expected 400)")
        assert res.status == 400

        # 4b. Successful creation
        good_payload = json.dumps({
            "username": "dr_rostami",
            "password": "Rostami@2026Pass",
            "displayName": "دکتر نیلوفر رستمی",
            "firstName": "نیلوفر",
            "lastName": "رستمی",
            "nickname": "دکتر رستمی",
            "email": "rostami@pezeshkan.me",
            "website": "https://pezeshkan.me/mag/aesthetics-skin/",
            "role": "author",
            "specialty": "متخصص پوست، مو و زیبایی",
            "medicalCouncil": "۱۴۲۵۸۰",
            "bio": "متخصص پوست و لیزر، عضو انجمن متخصصین پوست ایران.",
            "avatar": "👩‍⚕️",
            "status": "active"
        }).encode('utf-8')
        conn.request('POST', '/api/admin/users', body=good_payload,
                     headers={'Content-Type': 'application/json', 'Cookie': auth_cookie})
        res = conn.getresponse()
        created_data = json.loads(res.read().decode('utf-8'))
        print(f"    Creation status: {res.status}, Message: {created_data.get('message')}")
        assert res.status == 200
        new_user_id = created_data.get('user', {}).get('id')
        assert new_user_id is not None

        # Verify new user can log in
        print("[5] Testing login with newly created author (dr_rostami)...")
        rostami_login = json.dumps({"username": "dr_rostami", "password": "Rostami@2026Pass"}).encode('utf-8')
        conn.request('POST', '/api/login', body=rostami_login, headers={'Content-Type': 'application/json'})
        res = conn.getresponse()
        rostami_login_data = json.loads(res.read().decode('utf-8'))
        print(f"    Author login status: {res.status}, Name: {rostami_login_data.get('user', {}).get('name')}")
        assert res.status == 200
        assert rostami_login_data.get('user', {}).get('displayName') == "دکتر نیلوفر رستمی"

        # 6. Update user profile via PUT /api/admin/users/<id> (WordPress style)
        print("[6] Testing PUT /api/admin/users/<id> (WordPress style profile update)...")
        update_payload = json.dumps({
            "displayName": "نیلوفر رستمی",
            "firstName": "نیلوفر",
            "lastName": "رستمی",
            "nickname": "نیلوفر",
            "email": "dr.rostami@pezeshkan.me",
            "bio": "ویرایش شده: متخصص پوست و زیبایی، پژوهشگر لیزرهای جوانسازی.",
            "specialty": "متخصص پوست و پیوند مو"
        }).encode('utf-8')
        conn.request('PUT', f'/api/admin/users/{new_user_id}', body=update_payload,
                     headers={'Content-Type': 'application/json', 'Cookie': auth_cookie})
        res = conn.getresponse()
        update_res = json.loads(res.read().decode('utf-8'))
        print(f"    Update status: {res.status}, New displayName: {update_res.get('user', {}).get('displayName')}")
        assert res.status == 200
        assert update_res.get('user', {}).get('displayName') == "نیلوفر رستمی"

        # 7. Dedicated password change via POST /api/admin/users/<id>/password
        print("[7] Testing POST /api/admin/users/<id>/password...")
        pwd_change_payload = json.dumps({"newPassword": "NewSecurePass2026!"}).encode('utf-8')
        conn.request('POST', f'/api/admin/users/{new_user_id}/password', body=pwd_change_payload,
                     headers={'Content-Type': 'application/json', 'Cookie': auth_cookie})
        res = conn.getresponse()
        pwd_res = json.loads(res.read().decode('utf-8'))
        print(f"    Password change status: {res.status}, Message: {pwd_res.get('message')}")
        assert res.status == 200

        # Verify old password now fails
        print("    Verifying old password fails...")
        conn.request('POST', '/api/login', body=rostami_login, headers={'Content-Type': 'application/json'})
        res = conn.getresponse()
        res.read()
        print(f"    Old password login status: {res.status} (Expected 401)")
        assert res.status == 401

        # Verify new password succeeds
        print("    Verifying new password succeeds...")
        new_login = json.dumps({"username": "dr_rostami", "password": "NewSecurePass2026!"}).encode('utf-8')
        conn.request('POST', '/api/login', body=new_login, headers={'Content-Type': 'application/json'})
        res = conn.getresponse()
        new_login_data = json.loads(res.read().decode('utf-8'))
        print(f"    New password login status: {res.status}")
        assert res.status == 200

        # 8. Test safety guards: Cannot delete primary admin or current user
        print("[8] Testing safety guards (Prevent admin deletion)...")
        mahyar_id = mahyar_user.get('id')
        conn.request('DELETE', f'/api/admin/users/{mahyar_id}', headers={'Cookie': auth_cookie})
        res = conn.getresponse()
        res.read()
        print(f"    Delete primary admin status: {res.status} (Expected 400)")
        assert res.status == 400

        # 9. Delete created author via DELETE /api/admin/users/<id>
        print("[9] Testing DELETE /api/admin/users/<id>...")
        conn.request('DELETE', f'/api/admin/users/{new_user_id}', headers={'Cookie': auth_cookie})
        res = conn.getresponse()
        del_res = json.loads(res.read().decode('utf-8'))
        print(f"    Delete author status: {res.status}, Message: {del_res.get('message')}")
        assert res.status == 200

        # Verify user is deleted
        conn.request('GET', f'/api/admin/users/{new_user_id}', headers={'Cookie': auth_cookie})
        res = conn.getresponse()
        res.read()
        assert res.status == 404

        print("\n[SUCCESS] All User & Author Management tests passed with 100% success!")
    finally:
        conn.close()
        httpd.shutdown()

if __name__ == '__main__':
    run_tests()
