import os
import sys
import time
import urllib.request
import urllib.error
import subprocess

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("Starting server.py on port 3009 for SEO endpoint verification...")
env = os.environ.copy()
env["PORT"] = "3009"
env["HOST"] = "127.0.0.1"
proc = subprocess.Popen([sys.executable, "server.py"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(1.5)

base = "http://127.0.0.1:3009"

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirectHandler)

tests = [
    # (path, expected_status, expected_location, expected_ctype, expected_robot_header)
    ("/", 200, None, "text/html", None),
    ("/robots.txt", 200, None, "text/plain", None),
    ("/sitemap.xml", 200, None, "application/xml", None),
    ("/favicon.svg", 200, None, "image/svg+xml", None),
    ("/site.webmanifest", 200, None, "application/manifest+json", None),
    ("/index.html", 301, "/", None, None),
    ("/portal/index.html", 301, "/", None, None),
    ("/product.html", 301, "/product", None, None),
    ("/product/", 301, "/product", None, None),
    ("/pricing", 301, "/packages", None, None),
    ("/learn", 301, "/tutorials", None, None),
    ("/mag/index.html", 301, "/mag", None, None),
    ("/admin", 302, "/login?redirect=/admin", None, "noindex"),
    ("/nonexistent-page-xyz", 404, None, "text/html", "noindex"),
]

passed = 0
failed = 0

for path, exp_code, exp_loc, exp_ctype, exp_robots in tests:
    url = base + path
    req = urllib.request.Request(url)
    try:
        resp = opener.open(req)
        code = resp.getcode()
        headers = resp.headers
    except urllib.error.HTTPError as e:
        code = e.code
        headers = e.headers
    except Exception as e:
        print(f"❌ Error connecting to {path}: {e}")
        failed += 1
        continue

    ok = True
    reasons = []

    if code != exp_code:
        ok = False
        reasons.append(f"Expected status {exp_code}, got {code}")

    if exp_loc:
        loc = headers.get("Location")
        if loc != exp_loc:
            ok = False
            reasons.append(f"Expected Location '{exp_loc}', got '{loc}'")

    if exp_ctype:
        ctype = headers.get("Content-Type", "")
        if exp_ctype not in ctype:
            ok = False
            reasons.append(f"Expected Content-Type containing '{exp_ctype}', got '{ctype}'")

    if exp_robots:
        robots = headers.get("X-Robots-Tag", "")
        if exp_robots not in robots:
            ok = False
            reasons.append(f"Expected X-Robots-Tag containing '{exp_robots}', got '{robots}'")

    if ok:
        print(f"✅ {path.ljust(25)} -> Status: {code} | OK")
        passed += 1
    else:
        print(f"❌ {path.ljust(25)} -> FAILED: {', '.join(reasons)}")
        failed += 1

proc.terminate()
try:
    proc.wait(timeout=2)
except Exception:
    proc.kill()

print(f"\nResults: {passed} passed, {failed} failed.")
if failed > 0:
    sys.exit(1)
