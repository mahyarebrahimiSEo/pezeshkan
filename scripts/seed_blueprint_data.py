# -*- coding: utf-8 -*-
"""
Seed script for Pezeshkan Blueprint 2.2.0:
- Subscription plans (Starter, Pro, Enterprise)
- Doctors clinic_slug and center_type alignment
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from apps.pezeshkan_core.models import SubscriptionPlan, Doctor

def seed_plans():
    plans_data = [
        {
            "slug": "starter",
            "title": "طرح پایه مطب (Starter)",
            "duration": "ماهانه",
            "price": 5000000,
            "price_formatted": "۵,۰۰۰,۰۰۰ تومان",
            "period": "/ ماهانه (۳ ماه نخست رایگان)",
            "badge": "دوره آزمایشی رایگان",
            "is_featured": False,
            "description": "ویژه مطب‌های تک‌پزشک با مراجعه متوسط روزانه و نیاز به ثبت نسخه سریع",
            "max_doctors": 1,
            "max_secretaries": 1,
            "max_appointments": 300,
            "is_unlimited": False,
            "sms_credits": 500,
            "flag_analytics": False,
            "flag_eprescribe": True,
            "flag_custom_sms": False,
            "features": [
                "پرونده الکترونیک سلامت نامحدود",
                "ثبت نسخه الکترونیک تامین اجتماعی و سلامت",
                "پنل نوبت‌دهی آنلاین با یادآور پیامکی",
                "استقرار و آموزش حضوری رایگان در مطب",
                "پشتیبانی در ساعات اداری"
            ],
            "order": 1,
            "is_active": True,
        },
        {
            "slug": "pro",
            "title": "طرح حرفه‌ای (Pro)",
            "duration": "ماهانه",
            "price": 8500000,
            "price_formatted": "۸,۵۰۰,۰۰۰ تومان",
            "period": "/ ماهانه (۳ ماه نخست رایگان)",
            "badge": "بیشترین انتخاب پزشکان",
            "is_featured": True,
            "description": "ویژه مطب‌های پرمراجعه، کلینیک‌ها و مراکز با ۲ یونیت یا پزشک فعال",
            "max_doctors": 3,
            "max_secretaries": 3,
            "max_appointments": 1000,
            "is_unlimited": False,
            "sms_credits": 2000,
            "flag_analytics": True,
            "flag_eprescribe": True,
            "flag_custom_sms": True,
            "features": [
                "تمام قابلیت‌های طرح پایه به صورت نامحدود",
                "دستیار بالینی هوش مصنوعی (AI Copilot)",
                "اتصال مستقیم دستگاه کارتخوان مطب به EMR",
                "پورتال و اپلیکیشن اختصاصی بیماران کلینیک",
                "پشتیبانی اختصاصی شبانه‌روزی ۲۴ ساعته VIP"
            ],
            "order": 2,
            "is_active": True,
        },
        {
            "slug": "enterprise",
            "title": "سازمانی و بیمارستانی (Enterprise)",
            "duration": "سالانه / سفارشی",
            "price": 0,
            "price_formatted": "سفارشی",
            "period": "بر اساس تعداد یونیت",
            "badge": "پایلوت آزمایشی ۳ ماهه",
            "is_featured": False,
            "description": "ویژه کلینیک‌های چندتخصصی، مراکز درمانی و بیمارستان‌ها",
            "max_doctors": 999,
            "max_secretaries": 999,
            "max_appointments": 99999,
            "is_unlimited": True,
            "sms_credits": 10000,
            "flag_analytics": True,
            "flag_eprescribe": True,
            "flag_custom_sms": True,
            "features": [
                "کاربران و یونیت‌های درمانی نامحدود",
                "سرور اختصاصی و پایگاه داده ایزوله بیمارستان",
                "اتصال به سامانه‌های HIS و PACS تصویربرداری",
                "استقرار و آموزش حضوری کلیه پرسنل"
            ],
            "order": 3,
            "is_active": True,
        }
    ]

    for p in plans_data:
        obj, created = SubscriptionPlan.objects.update_or_create(
            slug=p["slug"],
            defaults=p
        )
        print(f"Plan: {obj.slug} (Created: {created})")

def update_doctors():
    # Ensure standard doctors have clinic_slug
    for doc in Doctor.objects.all():
        if not doc.clinic_slug:
            doc.clinic_slug = doc.custom_id or f"doc-{doc.id}"
            if not doc.center_type:
                doc.center_type = "solo"
            doc.save()
            print(f"Updated doctor {doc.id} with slug {doc.clinic_slug}")

    # Ensure Dr. Naseh from blueprint exists
    dr_naseh, created = Doctor.objects.update_or_create(
        clinic_slug="dr-naseh",
        defaults={
            "custom_id": "dr-naseh",
            "name": "دکتر ناصح یوسفی",
            "title": "متخصص طب فیزیکی، توانبخشی و الکترودیاگنوزیس",
            "mc_number": "۱۰۴۵۸۰",
            "dept": "کلینیک تخصصی طب فیزیکی و توانبخشی",
            "pillar_slug": "physical-rehab",
            "rating": 4.95,
            "reviews_count": 310,
            "available": True,
            "center_type": "solo",
            "work_hours": "شنبه تا چهارشنبه - ۱۵:۰۰ الی ۲۰:۰۰",
            "address": "تهران، روبروی مترو شادمان، ساختمان پزشکان فجر، طبقه ۳",
            "phone": "۰۲۱-۶۶۰۲۰۳۰۸",
            "time_slots": ["۱۵:۳۰", "۱۶:۱۵", "۱۷:۰۰", "۱۷:۴۵", "۱۸:۳۰", "۱۹:۱۵"],
            "services": ["ویزیت تخصصی ستون فقرات", "نوار عصب و عضله (EMG-NCS)", "لیزرتراپی پرتوان", "درمان دیسک کمر"],
        }
    )
    print(f"Dr. Naseh: {dr_naseh.clinic_slug} (Created: {created})")

if __name__ == "__main__":
    seed_plans()
    update_doctors()
    print("Seed completed successfully!")
