# -*- coding: utf-8 -*-
"""
Verification Suite for Blueprint 2.2.0 Integration Flows
Tests:
- FLOW_01 (Patient Quick Booking Bridge & Directory API)
- FLOW_02 (Subscription Plans Model & API)
- FLOW_03 (Clinic Onboarding Leads API & DB isolation)
- FLOW_04 (Doctor Auth & Live Demo URLs in Frontends)
"""
import os
import sys
import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from apps.pezeshkan_core.models import Doctor, SubscriptionPlan, ClinicLead

def test_models():
    print("Testing Models...")
    # Check Doctor clinic_slug & quick_booking_url
    docs = Doctor.objects.all()
    assert docs.count() >= 1, "Doctor table is empty"
    doc = docs.first()
    assert hasattr(doc, 'clinic_slug'), "Doctor missing clinic_slug"
    assert hasattr(doc, 'quick_booking_url'), "Doctor missing quick_booking_url"
    assert "https://app.pezeshk-on.ir/" in doc.quick_booking_url, f"Bad quick_booking_url: {doc.quick_booking_url}"
    print(f"  [OK] Doctor model: {doc.name} -> {doc.quick_booking_url}")

    # Check SubscriptionPlan
    plans = SubscriptionPlan.objects.filter(is_active=True)
    assert plans.count() >= 3, f"Expected at least 3 plans, found {plans.count()}"
    slugs = [p.slug for p in plans]
    assert "starter" in slugs and "pro" in slugs and "enterprise" in slugs, f"Missing core plans: {slugs}"
    print(f"  [OK] Subscription plans: {slugs}")

    # Check ClinicLead
    leads = ClinicLead.objects.all()
    print(f"  [OK] ClinicLead count: {leads.count()}")

def test_api_directory():
    print("Testing GET /api/v1/clinic/public/directory/...")
    req = urllib.request.Request("http://127.0.0.1:3000/api/v1/clinic/public/directory/")
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        assert "count" in data and "results" in data, "Bad directory response structure"
        assert data["count"] > 0, "No doctors in directory"
        first = data["results"][0]
        assert "quick_booking_url" in first, "Doctor entry missing quick_booking_url"
        assert "slug" in first, "Doctor entry missing slug"
        print(f"  [OK] Directory API returned {data['count']} doctors. First: {first['doctor_name']} ({first['quick_booking_url']})")

def test_api_plans():
    print("Testing GET /api/v1/platform/public/plans/...")
    req = urllib.request.Request("http://127.0.0.1:3000/api/v1/platform/public/plans/")
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        assert isinstance(data, list) and len(data) >= 3, "Plans API did not return plans list"
        p = data[0]
        assert "ctaUrl" in p and "/start?plan=" in p["ctaUrl"], f"Bad ctaUrl in plan: {p.get('ctaUrl')}"
        print(f"  [OK] Plans API returned {len(data)} plans. First: {p['title']} (CTA: {p['ctaUrl']})")

def test_api_leads_submission():
    print("Testing POST /api/v1/leads/start/...")
    payload = {
        "doctorName": "دکتر تست اعتبارسنجی",
        "mobile": "09129998877",
        "specialty": "ارتوپدی و توانبخشی",
        "patientsVolume": "بیش از ۶۰ بیمار",
        "challenges": ["قلم نوری و تسریع ثبت پرونده", "اتصال کارتخوان"],
        "clinicAddress": "تهران، میدان ونک",
        "chosenPlan": "starter"
    }
    req = urllib.request.Request(
        "http://127.0.0.1:3000/api/v1/leads/start/",
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 201, f"Expected 201, got {res.status}"
        data = json.loads(res.read().decode('utf-8'))
        assert data["success"] is True, "Lead submission success is not True"
        assert data["redirect_url"] == "https://app.pezeshk-on.ir/demo/doctor", f"Bad redirect_url: {data.get('redirect_url')}"
        lead_id = data["lead"]["id"]
        lead = ClinicLead.objects.get(id=lead_id)
        assert lead.doctor_name == "دکتر تست اعتبارسنجی", "Lead name mismatch in DB"
        print(f"  [OK] Lead created: ID {lead_id}, redirect_url: {data['redirect_url']}")

def test_template_links():
    print("Testing Template & Frontend Wiring...")
    # 1. appointments.html
    apt_html = (BASE_DIR / "portal" / "appointments.html").read_text(encoding="utf-8")
    assert "quickBookingUrl" in apt_html, "appointments.html missing quickBookingUrl binding"
    assert "دریافت نوبت سریع" in apt_html, "appointments.html missing 'دریافت نوبت سریع' CTA"
    print("  [OK] portal/appointments.html has quickBookingUrl external link")

    # 2. packages.html
    pkg_html = (BASE_DIR / "portal" / "packages.html").read_text(encoding="utf-8")
    assert "/start?plan=starter" in pkg_html, "packages.html missing /start?plan=starter link"
    assert "/start?plan=pro" in pkg_html, "packages.html missing /start?plan=pro link"
    print("  [OK] portal/packages.html connects plan buttons to /start?plan={slug}")

    # 3. start.html
    start_html = (BASE_DIR / "portal" / "start.html").read_text(encoding="utf-8")
    assert "/api/v1/leads/start/" in start_html, "start.html missing /api/v1/leads/start/ endpoint call"
    assert "https://app.pezeshk-on.ir/demo/doctor" in start_html, "start.html missing demo link"
    print("  [OK] portal/start.html posts to /api/v1/leads/start/ and displays live demo CTA")

    # 4. shared.js
    shared_js = (BASE_DIR / "portal" / "shared.js").read_text(encoding="utf-8")
    assert "https://app.pezeshk-on.ir/" in shared_js, "shared.js missing https://app.pezeshk-on.ir/ doctor login"
    assert "https://app.pezeshk-on.ir/demo/doctor" in shared_js, "shared.js missing live demo CTA"
    print("  [OK] portal/shared.js auth modal directs doctor to app.pezeshk-on.ir and live demo")

    # 5. index.html
    index_html = (BASE_DIR / "portal" / "index.html").read_text(encoding="utf-8")
    assert "https://app.pezeshk-on.ir/demo/doctor" in index_html, "index.html missing live demo button"
    print("  [OK] portal/index.html hero links to https://app.pezeshk-on.ir/demo/doctor")

if __name__ == "__main__":
    test_models()
    test_api_directory()
    test_api_plans()
    test_api_leads_submission()
    test_template_links()
    print("\nALL BLUEPRINT 2.2.0 INTEGRATION TESTS PASSED 100%!")
