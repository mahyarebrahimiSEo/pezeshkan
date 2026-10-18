# -*- coding: utf-8 -*-
"""
Pezeshkan Medical Ecosystem - Django Models Architecture
Full-fidelity mapping to clinical data specifications.
"""

from django.db import models


class Pillar(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام ستون")
    short_name = models.CharField(max_length=100, blank=True, verbose_name="نام کوتاه")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    icon = models.CharField(max_length=100, blank=True, verbose_name="آیکون")
    count_badge = models.CharField(max_length=50, blank=True)
    intent = models.CharField(max_length=100, blank=True)
    dept = models.CharField(max_length=100, blank=True)
    desc = models.TextField(blank=True, verbose_name="توضیحات")
    chips = models.JSONField(default=list, blank=True)
    branches = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pezeshkan_pillars"
        verbose_name = "دپارتمان تخصصی"
        verbose_name_plural = "دپارتمان‌های تخصصی"

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "shortName": self.short_name,
            "slug": self.slug,
            "icon": self.icon,
            "countBadge": self.count_badge,
            "intent": self.intent,
            "dept": self.dept,
            "desc": self.desc,
            "chips": self.chips,
            "branches": self.branches,
        }


class Doctor(models.Model):
    custom_id = models.CharField(max_length=100, blank=True, db_index=True)
    name = models.CharField(max_length=255, verbose_name="نام پزشک")
    clinic_slug = models.SlugField(max_length=100, blank=True, verbose_name="اسلاگ کلینیک/مطب")
    center_type = models.CharField(max_length=50, default="solo", verbose_name="نوع مرکز")
    title = models.CharField(max_length=255, verbose_name="عنوان و تخصص")
    mc_number = models.CharField(max_length=100, blank=True, verbose_name="شماره نظام پزشکی")
    dept = models.CharField(max_length=100, blank=True, verbose_name="بخش")
    pillar_slug = models.CharField(max_length=100, blank=True, verbose_name="اسلاگ ستون")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    reviews_count = models.IntegerField(default=0)
    avatar = models.TextField(blank=True, verbose_name="تصویر پزشک")
    available = models.BooleanField(default=True, verbose_name="در دسترس")
    work_hours = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True, verbose_name="آدرس مطب")
    phone = models.CharField(max_length=50, blank=True, verbose_name="تلفن تماس")
    time_slots = models.JSONField(default=list, blank=True)
    services = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pezeshkan_doctors"
        verbose_name = "پزشک"
        verbose_name_plural = "پزشکان"

    def __str__(self):
        return self.name

    @property
    def quick_booking_url(self):
        slug = self.clinic_slug or self.custom_id or f"doc-{self.id}"
        return f"https://app.pezeshk-on.ir/{slug}/quick-booking"

    def to_dict(self):
        slug = self.clinic_slug or self.custom_id or f"doc-{self.id}"
        return {
            "id": self.custom_id or str(self.id),
            "name": self.name,
            "clinicSlug": self.clinic_slug or self.custom_id,
            "centerType": self.center_type or "solo",
            "quickBookingUrl": self.quick_booking_url,
            "title": self.title,
            "mcNumber": self.mc_number,
            "dept": self.dept,
            "pillarSlug": self.pillar_slug,
            "rating": float(self.rating) if self.rating else 5.0,
            "reviewsCount": self.reviews_count,
            "avatar": self.avatar,
            "available": self.available,
            "workHours": self.work_hours,
            "address": self.address,
            "phone": self.phone,
            "timeSlots": self.time_slots,
            "services": self.services,
        }


class Article(models.Model):
    STATUS_CHOICES = (
        ("published", "منتشر شده"),
        ("draft", "پیش‌نویس"),
        ("archived", "بایگانی"),
    )
    custom_id = models.CharField(max_length=100, blank=True, db_index=True)
    title = models.CharField(max_length=500, verbose_name="عنوان مقاله")
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    summary = models.TextField(blank=True, verbose_name="خلاصه")
    raw_html = models.TextField(blank=True)
    content_html = models.TextField(verbose_name="متن مقاله (HTML)")
    image = models.TextField(blank=True, verbose_name="تصویر شاخص")
    image_alt = models.CharField(max_length=500, blank=True)
    pillar_id = models.CharField(max_length=50, blank=True)
    category_name = models.CharField(max_length=100, blank=True)
    category_icon = models.CharField(max_length=100, blank=True)
    doctor_id = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=255, default="تیم تحریریه پزشکان")
    read_time = models.CharField(max_length=50, default="۵ دقیقه")
    last_reviewed = models.CharField(max_length=100, blank=True)
    tag = models.CharField(max_length=100, blank=True)
    tag_class = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="published")
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    focus_keyword = models.CharField(max_length=255, blank=True)
    faqs = models.JSONField(default=list, blank=True)
    schema_type = models.CharField(max_length=100, default="MedicalWebPage")
    old_slugs = models.JSONField(default=list, blank=True)
    schema_data = models.JSONField(default=dict, blank=True)
    custom_schema_json = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pezeshkan_articles"
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "id": self.custom_id or self.id,
            "title": self.title,
            "slug": self.slug,
            "summary": self.summary,
            "rawHtml": self.raw_html,
            "contentHtml": self.content_html,
            "image": self.image,
            "imageAlt": self.image_alt,
            "pillarId": self.pillar_id,
            "categoryName": self.category_name,
            "categoryIcon": self.category_icon,
            "doctorId": self.doctor_id,
            "author": self.author,
            "readTime": self.read_time,
            "lastReviewed": self.last_reviewed,
            "tag": self.tag,
            "tagClass": self.tag_class,
            "status": self.status,
            "metaTitle": self.meta_title,
            "metaDescription": self.meta_description,
            "focusKeyword": self.focus_keyword,
            "faqs": self.faqs,
            "schemaType": self.schema_type,
            "oldSlugs": self.old_slugs,
            "schemaData": self.schema_data,
            "customSchemaJson": self.custom_schema_json,
            "lastModified": self.last_modified.isoformat() if self.last_modified else None,
        }


class Appointment(models.Model):
    STATUS_CHOICES = (
        ("pending", "در انتظار بررسی"),
        ("confirmed", "تایید شده"),
        ("cancelled", "لغو شده"),
        ("completed", "انجام شده"),
    )
    custom_id = models.CharField(max_length=100, blank=True)
    tracking_code = models.CharField(max_length=32, unique=True, verbose_name="کد رهگیری")
    doctor_id = models.CharField(max_length=50, verbose_name="شناسه پزشک")
    doctor_name = models.CharField(max_length=255, blank=True, verbose_name="نام پزشک")
    patient_name = models.CharField(max_length=255, verbose_name="نام بیمار")
    patient_phone = models.CharField(max_length=50, verbose_name="تلفن بیمار")
    national_id = models.CharField(max_length=50, blank=True, verbose_name="کد ملی")
    visit_type = models.CharField(max_length=100, default="ویزیت حضوری مطب")
    date_label = models.CharField(max_length=100, verbose_name="تاریخ نوبت")
    time_slot = models.CharField(max_length=100, verbose_name="ساعت نوبت")
    notes = models.TextField(blank=True, verbose_name="یادداشت")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="confirmed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pezeshkan_appointments"
        verbose_name = "نوبت پزشکی"
        verbose_name_plural = "نوبت‌های پزشکی"
        indexes = [
            models.Index(fields=["doctor_id", "date_label", "time_slot"]),
            models.Index(fields=["patient_phone"]),
        ]

    def __str__(self):
        return f"{self.tracking_code} - {self.patient_name} ({self.date_label} {self.time_slot})"

    def to_dict(self):
        return {
            "id": self.custom_id or str(self.id),
            "trackingCode": self.tracking_code,
            "doctorId": self.doctor_id,
            "doctorName": self.doctor_name,
            "patientName": self.patient_name,
            "patientPhone": self.patient_phone,
            "nationalId": self.national_id,
            "visitType": self.visit_type,
            "dateLabel": self.date_label,
            "timeSlot": self.time_slot,
            "notes": self.notes,
            "status": self.status,
            "createdAt": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updatedAt": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None,
        }


class MediaItem(models.Model):
    custom_id = models.CharField(max_length=100, blank=True)
    filename = models.CharField(max_length=255, verbose_name="نام فایل")
    url = models.TextField(verbose_name="آدرس فایل")
    variants = models.JSONField(default=dict, blank=True)
    dimensions = models.JSONField(default=dict, blank=True)
    format = models.CharField(max_length=20, default="webp")
    size = models.BigIntegerField(default=0)
    original_size = models.BigIntegerField(default=0)
    saved_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    storage = models.CharField(max_length=50, default="local")
    alt = models.CharField(max_length=500, blank=True)
    title = models.CharField(max_length=500, blank=True)
    caption = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pezeshkan_media"
        verbose_name = "رسانه"
        verbose_name_plural = "کتابخانه رسانه"

    def to_dict(self):
        return {
            "id": self.custom_id or self.id,
            "filename": self.filename,
            "url": self.url,
            "variants": self.variants,
            "dimensions": self.dimensions,
            "format": self.format,
            "size": self.size,
            "originalSize": self.original_size,
            "savedPercentage": float(self.saved_percentage) if self.saved_percentage else 0.0,
            "storage": self.storage,
            "alt": self.alt,
            "title": self.title,
            "caption": self.caption,
            "uploadedAt": self.uploaded_at.isoformat() if self.uploaded_at else None,
        }


class Redirect(models.Model):
    custom_id = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=500, unique=True)
    target = models.CharField(max_length=500)
    status_code = models.IntegerField(default=301)
    match_type = models.CharField(max_length=50, default="exact")
    preserve_query = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    hit_count = models.BigIntegerField(default=0)
    last_hit = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pezeshkan_redirects"
        verbose_name = "تغییر مسیر"
        verbose_name_plural = "تغییر مسیرهای سئو"

    def to_dict(self):
        return {
            "id": self.custom_id or str(self.id),
            "source": self.source,
            "target": self.target,
            "statusCode": self.status_code,
            "matchType": self.match_type,
            "preserveQuery": self.preserve_query,
            "isActive": self.is_active,
            "description": self.description,
            "hitCount": self.hit_count,
            "lastHit": self.last_hit.isoformat() if self.last_hit else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }


class SiteSetting(models.Model):
    site_title = models.CharField(max_length=255, default="پزشکان - مجله جامع سلامت")
    site_subtitle = models.CharField(max_length=255, blank=True)
    editorial_leader = models.CharField(max_length=255, blank=True)
    announcement_banner = models.TextField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    emergency_triage_enabled = models.BooleanField(default=True)
    seo = models.JSONField(default=dict, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pezeshkan_settings"
        verbose_name = "تنظیمات عمومی سایت"

    def to_dict(self):
        return {
            "siteTitle": self.site_title,
            "siteSubtitle": self.site_subtitle,
            "editorialLeader": self.editorial_leader,
            "announcementBanner": self.announcement_banner,
            "contactPhone": self.contact_phone,
            "emergencyTriageEnabled": self.emergency_triage_enabled,
            "seo": self.seo,
            "lastUpdated": self.last_updated.isoformat() if self.last_updated else None,
        }


class UserAccount(models.Model):
    custom_id = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    nickname = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    role = models.CharField(max_length=50, default="administrator")
    bio = models.TextField(blank=True)
    avatar = models.TextField(blank=True)
    specialty = models.CharField(max_length=255, blank=True)
    medical_council = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, default="active")
    registered_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    password_salt = models.CharField(max_length=128, blank=True)
    password_hash = models.CharField(max_length=255)

    class Meta:
        db_table = "pezeshkan_users"
        verbose_name = "کاربر بالینی"
        verbose_name_plural = "کاربران بالینی"

    def to_dict(self):
        return {
            "id": self.custom_id or str(self.id),
            "username": self.username,
            "displayName": self.display_name or self.username,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "nickname": self.nickname,
            "email": self.email,
            "website": self.website,
            "role": self.role,
            "bio": self.bio,
            "avatar": self.avatar,
            "specialty": self.specialty,
            "medicalCouncil": self.medical_council,
            "status": self.status,
            "registeredAt": self.registered_at.isoformat() if self.registered_at else None,
            "lastLogin": self.last_login.isoformat() if self.last_login else None,
        }


class Newsletter(models.Model):
    custom_id = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    date = models.CharField(max_length=100, blank=True)
    read_time = models.CharField(max_length=50, default="۴ دقیقه")
    excerpt = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    metrics = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=50, default="published")

    class Meta:
        db_table = "pezeshkan_newsletters"
        verbose_name = "خبرنامه پزشکی"
        verbose_name_plural = "خبرنامه‌های پزشکی"

    def to_dict(self):
        return {
            "id": self.custom_id or self.id,
            "title": self.title,
            "slug": self.slug,
            "date": self.date,
            "readTime": self.read_time,
            "excerpt": self.excerpt,
            "contentHtml": self.content_html,
            "tags": self.tags,
            "metrics": self.metrics,
            "status": self.status,
        }


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=100, default="عمومی")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = "pezeshkan_subscribers"

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "category": self.category,
            "subscribedAt": self.subscribed_at.isoformat() if self.subscribed_at else None,
            "ip": self.ip,
        }


class Inquiry(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pezeshkan_inquiries"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
            "status": self.status,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class CrmTutorial(models.Model):
    custom_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=100, blank=True)
    video_url = models.URLField(max_length=1000, blank=True)
    description = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pezeshkan_crm_tutorials"

    def to_dict(self):
        return {
            "id": self.custom_id,
            "title": self.title,
            "category": self.category,
            "videoUrl": self.video_url,
            "description": self.description,
            "lastModified": self.last_modified.isoformat() if self.last_modified else None,
        }


class SubscriptionPlan(models.Model):
    slug = models.SlugField(max_length=100, unique=True, verbose_name="شناسه پلن")
    title = models.CharField(max_length=255, verbose_name="عنوان پکیج")
    duration = models.CharField(max_length=100, default="ماهانه", verbose_name="دوره زمانی")
    price = models.BigIntegerField(default=0, verbose_name="قیمت به تومان")
    price_formatted = models.CharField(max_length=100, blank=True, verbose_name="قیمت نمایشی")
    period = models.CharField(max_length=50, blank=True, default="/ ماهانه")
    badge = models.CharField(max_length=100, blank=True, verbose_name="برچسب محبوب/ویژه")
    is_featured = models.BooleanField(default=False, verbose_name="پلن برگزیده")
    description = models.TextField(blank=True, verbose_name="توضیحات پلن")
    max_doctors = models.IntegerField(default=1, verbose_name="سقف پزشکان مطب")
    max_secretaries = models.IntegerField(default=1, verbose_name="سقف منشی‌ها")
    max_appointments = models.IntegerField(default=100, verbose_name="سقف نوبت در ماه")
    is_unlimited = models.BooleanField(default=False, verbose_name="فلگ پکیج VIP")
    sms_credits = models.IntegerField(default=500, verbose_name="سهمیه پیامک هدیه")
    flag_analytics = models.BooleanField(default=False, verbose_name="گزارشات پیشرفته مالی")
    flag_eprescribe = models.BooleanField(default=False, verbose_name="نسخه الکترونیک")
    flag_custom_sms = models.BooleanField(default=False, verbose_name="پیامک سفارشی")
    features = models.JSONField(default=list, blank=True, verbose_name="ویژگی‌های پلن")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pezeshkan_subscription_plans"
        verbose_name = "پکیج اشتراک مطب"
        verbose_name_plural = "پکیج‌های اشتراک مطب"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "duration": self.duration,
            "price": self.price,
            "priceFormatted": self.price_formatted or f"{self.price:,} تومان",
            "period": self.period,
            "badge": self.badge,
            "isFeatured": self.is_featured,
            "description": self.description,
            "maxDoctors": self.max_doctors,
            "maxSecretaries": self.max_secretaries,
            "maxAppointments": self.max_appointments,
            "isUnlimited": self.is_unlimited,
            "smsCredits": self.sms_credits,
            "flagAnalytics": self.flag_analytics,
            "flagEprescribe": self.flag_eprescribe,
            "flagCustomSms": self.flag_custom_sms,
            "features": self.features,
            "isActive": self.is_active,
            "ctaUrl": f"/start?plan={self.slug}",
        }


class ClinicLead(models.Model):
    STATUS_CHOICES = (
        ("new", "جدید / بررسی نشده"),
        ("contacted", "تماس گرفته شده"),
        ("demo_scheduled", "دمو هماهنگ شده"),
        ("converted", "تبدیل به مشتری"),
        ("rejected", "عدم تمایل / ناموفق"),
    )

    doctor_name = models.CharField(max_length=255, verbose_name="نام پزشک یا مدیر مرکز")
    mobile = models.CharField(max_length=50, verbose_name="شماره همراه")
    specialty = models.CharField(max_length=150, blank=True, verbose_name="تخصص بالینی")
    patients_volume = models.CharField(max_length=100, blank=True, verbose_name="حجم مراجعین روزانه")
    challenges = models.JSONField(default=list, blank=True, verbose_name="دغدغه‌ها و نیازها")
    clinic_address = models.TextField(blank=True, verbose_name="شهر و نشانی مطب")
    chosen_plan = models.CharField(max_length=100, blank=True, verbose_name="پلن انتخابی")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="new", verbose_name="وضعیت لید")
    notes = models.TextField(blank=True, verbose_name="یادداشت تیم فروش")
    ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        db_table = "pezeshkan_clinic_leads"
        verbose_name = "لید کلینیک و شروع همکاری"
        verbose_name_plural = "لیدهای کلینیک و شروع همکاری"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.doctor_name} ({self.mobile})"

    def to_dict(self):
        return {
            "id": self.id,
            "doctorName": self.doctor_name,
            "mobile": self.mobile,
            "specialty": self.specialty,
            "patientsVolume": self.patients_volume,
            "challenges": self.challenges,
            "clinicAddress": self.clinic_address,
            "chosenPlan": self.chosen_plan,
            "status": self.status,
            "notes": self.notes,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }

