# اکوسیستم سلامت دیجیتال پزشکآن (Pezeshkan Ecosystem)
## مستندات مهندسی، معماری فرانت‌اند و شناسنامه ساب‌فولدر مجله سلامت (`/mag`)

---

### ۱. معماری کلی اکوسیستم (Architecture Separation)
مطابق سند مرجع و منشور مصوب:
- **وب‌سایت عمومی (پزشکان - Pezeshkan):** لایه جذب (Acquisition)، بازاریابی، آموزش، مجله سلامت، سئو و تولید لید.
- **اپلیکیشن بالینی (پزشکآن - Pezeshk-On):** لایه محصول، تریاژ، پرونده الکترونیک، نوبت‌دهی بالینی و مدیریت درمان.
- **ساب‌فولدر مجله (`/mag` یا `/magazine`):** هاب محتوایی پیشرفته بر پایه استانداردهای بالینی، ۹ پیلار اصلی سلامت، موتور تبدیل خواننده به بیمار/کاربر (HIS Bridge Engine) و سئوی E-E-A-T.

---

### ۲. ساختار شاخه‌ها و فایل‌های پروژه (Organized Directory Tree)

```text
pezeshkan_design/
├── docs/                                # مستندات راهبردی و مصوب سیستم
│   ├── architecture/                    # مشخصات فنی و معماری وب‌سایت و اتصال به اپلیکیشن
│   │   ├── PEZESHK.docx                 # سند جامع ساخت صفحات وب‌سایت و دستور Coding Agent
│   │   ├── PEZESHKAN_Website_Front_End_Implementation_&_AI_Coding_Agent_Master.docx
│   │   ├── PEZESHKON_FRONT_06_END_ARCHITECTURE_&_IMPLEMENTATION_SPECIFICATION.odt
│   │   ├── PEZESHKAN Web-App Integration Master Plan.docx
│   │   └── Product Growth & Release Master Plan.odt
│   │
│   ├── design-system/                   # سیستم طراحی، هویت بصری، کامپوننت‌ها و انیمیشن
│   │   ├── PEZESHKON Brand and Visual Identity System v1.0.docx
│   │   ├── Brand & Digital Experience Design Charter - V1.1.odt
│   │   ├── PEZESHKON_UI_UX_DESIGN_SYSTEM_&_INTERACTION_SPECIFICATION.odt
│   │   ├── 07-PEZESHKON COMPONENT LIBRARY DOCUMENTATION & CONTRACT.odt
│   │   ├── 08_Untitled_1PEZESHKON_PANEL_BY_PANEL_UX_&_COMPONENT_APPLICATION.odt
│   │   ├── MOTION DESIGN SYSTEM & VITAL INTERACTION LANGUAGE.odt
│   │   └── prompts/                     # دستورالعمل‌ها و پرامپت‌های استودیو طراحی
│   │       ├── VISUAL PROMPT.odt
│   │       └── VISUAL PROMPT 1.docx
│   │
│   └── archive_duplicates/              # آرشیو فایل‌های تکراری و هم‌پوشان (حفظ سوابق)
│       ├── 08_Untitled_1PEZESHKON_PANEL_BY_PANEL_UX_&_COMPONENT_APPLICATION (1).odt
│       └── PEZESHKAN Web ↔ App Integration Master Plan.docx
│
├── dossiers/                            # شناسنامه‌ها و پروتوتایپ‌های تعاملی Front-End
│   ├── pezeshkan_magazine_subfolder_dossier.html   # شناسنامه جامع و طرح مهندسی ساب‌فولدر مجله
│   ├── pezeshkan_axon_life_design_dossier.html    # بنچ‌مارک طراحی بر پایه آکسون‌لایف
│   ├── pezeshkan_pillar_clusters.html             # اطلس تعاملی پیلارها و کلاسترهای سئو
│   └── pezeshkan_pillar_clusters.zip              # فایل فشرده پیلارها
│
├── scripts/                             # اسکریپت‌های کمکی و استخراج داده
│   ├── scratch_node.js
│   └── output_pillars.json
│
└── mag/                                 # ساختار مهندسی ساب‌فولدر مجله (در حال توسعه)
    ├── content/                         # ساختار داده‌ای ۹ پیلار و مقالات کلاستر
    ├── components/                      # کامپوننت‌های بالینی فرانت‌اند
    ├── schemas/                         # ساختارهای اسکیما و سئو پزشکی گوگل
    └── public/                          # مدیا و است‌های بهینه‌شده
```

---

### ۳. اصول کلیدی سیستم طراحی پزشکآن (Clinical Dark DNA)
- **پالت رنگی سیگنال بالینی:**
  - فیروزه‌ای حیاتی (`#00FFFF`): داده، فناوری و اینتراکشن
  - سبز تپش حیات (`#00E599`): سلامت، وضعیت پایدار و تایید علمی
  - کهربایی هشدار (`#F59E0B`): هشدارهای مراقبتی و تفکیک تریاژ
  - قرمز بالینی (`#EF4444`): هشدارهای حاد پزشکی و اورژانس
- **تایپوگرافی:** وزیرمتن استاندارد (Vazirmatn)
- **استایل:** شیشه‌ای (Glassmorphism Dark) با بلور و عمق بصری
- **استاندارد سئو پزشکی:** انطباق ۱۰۰٪ با معیارهای Google E-E-A-T و اسکیماهای تفکیکی پزشکی.
