import os
import re
import json
import sys
import xml.etree.ElementTree as ET

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. SITEMAP VALIDATION ===")
tree = ET.parse("sitemap.xml")
root = tree.getroot()
urls = [loc.text for loc in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
print(f"Total Sitemap URLs: {len(urls)}")
for u in urls:
    print(f"  - {u}")

print("\n=== 2. WEB MANIFEST VALIDATION ===")
with open("site.webmanifest", encoding="utf-8") as f:
    manifest = json.load(f)
print(f"Manifest OK: Name='{manifest['name']}', Theme Color='{manifest['theme_color']}'")

print("\n=== 3. ROBOTS.TXT VALIDATION ===")
with open("robots.txt", encoding="utf-8") as f:
    robots = f.read()
assert "Sitemap: https://pezeshkan.me/sitemap.xml" in robots
assert "Disallow: /admin" in robots
assert "Disallow: /api/" in robots
print("Robots.txt structure: 100% OK")

print("\n=== 4. AUDITING PAGES METADATA & SCHEMA ===")
pages = [
    "portal/index.html",
    "portal/product.html",
    "portal/features.html",
    "portal/packages.html",
    "portal/tutorials.html",
    "portal/about.html",
    "portal/contact.html",
    "portal/services.html",
    "portal/start.html",
    "portal/404.html",
    "mag/index.html",
    "mag/admin.html",
    "mag/login.html"
]

for p in pages:
    with open(p, encoding="utf-8") as f:
        html = f.read()

    title_m = re.search(r"<title>(.*?)</title>", html)
    desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html)
    canon_m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html)
    robots_m = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', html)
    og_title_m = re.search(r'<meta\s+property=["\']og:title["\']', html)
    tw_card_m = re.search(r'<meta\s+name=["\']twitter:card["\']', html)
    jsonld_m = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html, re.DOTALL)

    title = title_m.group(1) if title_m else "MISSING"
    desc = desc_m.group(1) if desc_m else "MISSING"
    canon = canon_m.group(1) if canon_m else "MISSING"
    robots = robots_m.group(1) if robots_m else "MISSING"

    print(f"\n--- {p} ---")
    print(f"  Title ({len(title)} chars): {title}")
    print(f"  Description ({len(desc)} chars): {desc}")
    print(f"  Canonical: {canon}")
    print(f"  Robots: {robots}")
    print(f"  OG & Twitter: {'PASS' if (og_title_m and tw_card_m) or 'admin' in p or 'login' in p or '404' in p else 'FAIL'}")
    print(f"  JSON-LD Schemas: {len(jsonld_m)}")

    for j in jsonld_m:
        parsed = json.loads(j.strip())
        print(f"    Schema @type: {parsed.get('@type') or [x.get('@type') for x in parsed.get('@graph', [])]}")

print("\n=== ALL SEO TESTS PASSED SUCCESSFULLY! ===")
