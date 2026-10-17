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
        # Phase 1: Unauthenticated request -> 401
        print("[Phase 1] Testing unauthenticated GET /api/admin/site-structure...")
        conn.request('GET', '/api/admin/site-structure')
        res = conn.getresponse()
        res.read()
        print(f"    Status: {res.status} (Expected 401)")
        assert res.status == 401, f"Expected 401, got {res.status}"

        # Phase 2: Login as admin
        print("[Phase 2] Logging in as admin (mahyarebrahimi)...")
        login_payload = json.dumps({"username": "mahyarebrahimi", "password": "mahyebi86"}).encode('utf-8')
        conn.request('POST', '/api/login', body=login_payload, headers={'Content-Type': 'application/json'})
        res = conn.getresponse()
        cookie_header = res.getheader('Set-Cookie', '')
        login_data = json.loads(res.read().decode('utf-8'))
        auth_cookie = cookie_header.split(';')[0] if cookie_header else ''
        print(f"    Login status: {res.status}, Logged User: {login_data.get('user', {}).get('displayName')}")
        assert res.status == 200

        # Phase 3: Authenticated GET /api/admin/site-structure
        print("[Phase 3] Testing authenticated GET /api/admin/site-structure...")
        conn.request('GET', '/api/admin/site-structure', headers={'Cookie': auth_cookie})
        res = conn.getresponse()
        body = json.loads(res.read().decode('utf-8'))
        print(f"    Status: {res.status}")
        assert res.status == 200, f"Expected 200, got {res.status}"
        assert body.get('success') is True

        summary = body.get('summary', {})
        articles = body.get('articles', [])
        orphans = body.get('orphans', [])
        silos = body.get('silos', [])

        print(f"    Total Articles: {summary.get('totalArticles')}")
        print(f"    Total Silos/Categories: {summary.get('totalCategories')}")
        print(f"    Total Internal Links: {summary.get('totalInternalLinks')}")
        print(f"    Orphan Count: {summary.get('orphanCount')}")
        print(f"    Health Score: {summary.get('healthScore')}%")

        assert summary.get('totalArticles') == len(articles), "Summary totalArticles must match articles array length"
        assert summary.get('orphanCount') == len(orphans), "Summary orphanCount must match orphans array length"
        assert len(silos) > 0, "Expected at least 1 silo/category"

        # Verify article models have required link metrics
        for art in articles:
            assert 'inlinksCount' in art, f"Missing inlinksCount in article {art.get('id')}"
            assert 'outlinksCount' in art, f"Missing outlinksCount in article {art.get('id')}"
            assert 'isOrphan' in art, f"Missing isOrphan flag in article {art.get('id')}"
            assert 'healthTier' in art, f"Missing healthTier in article {art.get('id')}"

        # Phase 4: Test live simulation via POST /api/admin/site-structure/analyze
        print("[Phase 4] Testing live real-time simulation via POST /api/admin/site-structure/analyze...")
        if len(orphans) > 0:
            target_orphan = orphans[0]
            orphan_slug = target_orphan.get('slug')
            print(f"    Testing healing orphan: '{target_orphan.get('title')}' (/mag/{orphan_slug})")

            # Create a mock article that links to this orphan article
            sim_draft = {
                "id": "draft_simulation_test",
                "title": "مقاله شبیه‌سازی جهت رفع صفحه یتیم",
                "slug": "simulation-test-healer",
                "pillarId": 0,
                "contentHtml": f'<p>در این بخش به مطالعه مقاله جامع <a href="/mag/{orphan_slug}">درمان تخصصی</a> مراجعه فرمایید.</p>'
            }

            sim_body = json.dumps({"article": sim_draft}).encode('utf-8')
            conn.request('POST', '/api/admin/site-structure/analyze', body=sim_body, headers={
                'Cookie': auth_cookie,
                'Content-Type': 'application/json'
            })
            sim_res = conn.getresponse()
            sim_data = json.loads(sim_res.read().decode('utf-8'))
            print(f"    Simulation status: {sim_res.status}")
            assert sim_res.status == 200

            sim_summary = sim_data.get('summary', {})
            sim_orphans = sim_data.get('orphans', [])
            print(f"    Simulated Total Articles: {sim_summary.get('totalArticles')}")
            print(f"    Simulated Internal Links: {sim_summary.get('totalInternalLinks')} (Before: {summary.get('totalInternalLinks')})")
            print(f"    Simulated Orphan Count: {sim_summary.get('orphanCount')} (Before: {summary.get('orphanCount')})")

            # Check that the orphan is healed in the simulation!
            healed_check = any(o.get('slug') == orphan_slug for o in sim_orphans)
            assert not healed_check, f"Orphan article {orphan_slug} should have been healed in the simulation!"
            print(f"    [+] Successfully healed orphan {orphan_slug} in live simulation!")

        print("\n==========================================")
        print(" ALL SITE STRUCTURE & LINKING TESTS PASSED!")
        print("==========================================")
        return True

    finally:
        conn.close()
        httpd.shutdown()
        httpd.server_close()

if __name__ == '__main__':
    ok = run_tests()
    sys.exit(0 if ok else 1)
