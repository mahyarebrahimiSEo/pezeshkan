# -*- coding: utf-8 -*-
"""
Builds the complete Pezeshkan Healthcare Ecosystem Portal pages:
1. portal/index.html (Homepage - /)
2. portal/product.html (Product Page - /product)
3. portal/features.html (Features Page - /features)
4. portal/packages.html (Packages & Pricing - /packages)
5. portal/start.html (Start & Interactive Needs-Assessment Wizard - /start)
6. portal/services.html (Services Page - /services)
7. portal/about.html (About Us - /about)
8. portal/contact.html (Contact Us - /contact)

Based on the official data.html blueprint with dual-theme support,
pure SVG medical icons, and zero developer jargon.
"""

import os
import re

PORTAL_DIR = r"e:\antigravity\pezeshkan_design\portal"

def get_header(active_page="home"):
    nav_items = [
        ("product", "/product", "پرونده الکترونیک (EMR)"),
        ("features", "/features", "امکانات بالینی"),
        ("packages", "/packages", "تعرفه‌ها"),
        ("tutorials", "/tutorials", "آموزش CRM"),
        ("about", "/about", "درباره ما"),
        ("contact", "/contact", "تماس با ما"),
        ("mag", "/mag", "مجله سلامت"),
    ]

    nav_links_html = ""
    for key, url, label in nav_items:
        act = " active" if key == active_page else ""
        extra_cls = " nav-mag" if key == "mag" else ""
        badge = ""
        if key == "mag":
            badge = ' <span class="nav-badge-mag">بالینی</span>'
        nav_links_html += f'<li><a href="{url}" class="nav-link{act}{extra_cls}">{label}{badge}</a></li>\n'

    return f'''
  <!-- Header Bar -->
  <header class="site-header">
    <div class="container header-inner">
      <div style="display:flex; align-items:center; gap:20px;">
        <a href="/" class="brand-wrap" title="صفحه اصلی پزشکآن">
          <div class="brand-icon-box">
            <span class="pulse-ring"></span>
            <svg class="svg-icon" style="width:24px; height:24px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
            </svg>
          </div>
          <div class="brand-text">
            <h1>پزشکـــآن</h1>
            <span>پلتفرم سلامت دیجیتال</span>
          </div>
        </a>
      </div>

      <!-- Desktop Nav -->
      <ul class="main-nav">
        {nav_links_html}
      </ul>

      <!-- Header Actions -->
      <div class="header-actions">
        <button type="button" class="theme-toggle-btn" id="themeToggleBtn" title="تغییر حالت روز و شب" aria-label="تغییر حالت روز و شب">
          <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>

        <a href="/start" class="btn btn-primary header-cta-btn">
          <span>درخواست دمو رایگان</span>
          <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        </a>

        <button type="button" class="mobile-menu-toggle" onclick="toggleMobileMenu()" title="منو" aria-label="منوی موبایل">
          <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
      </div>
    </div>
  </header>

  <!-- Mobile Drawer -->
  <div id="mobileNavDrawer" onclick="handleDrawerBackdropClick(event)">
    <div class="drawer-content">
      <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--glass-border); padding-bottom:14px;">
        <span style="font-weight:900; color:var(--text-pure); font-size:16px;">منوی اکوسیستم پزشکآن</span>
        <button type="button" onclick="toggleMobileMenu()" style="background:none; border:none; color:var(--text-muted); cursor:pointer; display:inline-flex; align-items:center; justify-content:center; width:32px; height:32px;" title="بستن منو">
          <svg class="svg-icon" style="width:20px; height:20px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
      <ul style="list-style:none; display:flex; flex-direction:column; gap:10px;">
        <li><a href="/" class="nav-link">صفحه اصلی</a></li>
        <li><a href="/product" class="nav-link">پرونده الکترونیک (EMR)</a></li>
        <li><a href="/features" class="nav-link">امکانات بالینی</a></li>
        <li><a href="/packages" class="nav-link">تعرفه‌ها و پلن‌ها</a></li>
        <li><a href="/tutorials" class="nav-link">آموزش CRM</a></li>
        <li><a href="/about" class="nav-link">درباره ما</a></li>
        <li><a href="/contact" class="nav-link">تماس با ما</a></li>
        <li><a href="/mag" class="nav-link nav-mag">مجله سلامت</a></li>
      </ul>
      <div style="margin-top:auto; display:flex; flex-direction:column; gap:10px; padding-top:20px; border-top:1px solid var(--glass-border);">
        <a href="/start" class="btn btn-primary" style="width:100%; justify-content:center;">درخواست دمو رایگان ↗</a>
      </div>
    </div>
  </div>
    '''

def get_footer():
    return '''
  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
            <div class="brand-icon-box" style="width:36px; height:36px;">
              <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </div>
            <h4 style="margin:0; font-size:18px;">اکوسیستم سلامت دیجیتال پزشکآن</h4>
          </div>
          <p style="color:var(--text-secondary); line-height:1.9; max-width:440px;">
            پلتفرم پیشرو و دانش‌بنیان مدیریت درمان، پرونده الکترونیک سلامت (EMR)، اتوماسیون مطب و مجله سلامت بالینی. طراحی‌شده با رعایت دقیق‌ترین استانداردهای حریم خصوصی و امنیت داده‌های پزشکی.
          </p>
          <div style="margin-top:16px; display:flex; gap:12px;">
            <span style="background:rgba(0,115,255,0.08); color:var(--brand-primary); padding:4px 10px; border-radius:6px; font-size:11.5px; font-weight:700;">تاییدیه نظام پزشکی</span>
            <span style="background:rgba(5,150,105,0.08); color:var(--brand-emerald-vital); padding:4px 10px; border-radius:6px; font-size:11.5px; font-weight:700;">امنیت ۱۰۰٪ داده‌ها</span>
          </div>
        </div>

        <div class="footer-col">
          <h4>پلتفرم و محصول</h4>
          <ul class="footer-links">
            <li><a href="/product">پرونده الکترونیک سلامت (EMR)</a></li>
            <li><a href="/product#ai">دستیار بالینی هوش مصنوعی</a></li>
            <li><a href="/features">قابلیت‌ها و پنل منشی</a></li>
            <li><a href="/packages">پکیج‌ها و تعرفه‌ها</a></li>
            <li><a href="/start">درخواست دمو و شروع همکاری</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>آموزش و رسانه سلامت</h4>
          <ul class="footer-links">
            <li><a href="/mag">مجله سلامت پزشکآن</a></li>
            <li><a href="/mag#pillars">دپارتمان‌های ۹‌گانه تخصصی</a></li>
            <li><a href="/mag#doctors">پزشکان تاییدشده مجله</a></li>
            <li><a href="/services">تولید محتوا و ارتقای برند کلینیک</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>ارتباط و پشتیبانی</h4>
          <ul class="footer-links">
            <li><a href="/contact">تماس با مرکز ارتباط پزشکان</a></li>
            <li><a href="/about">درباره ما و اعضای هیئت علمی</a></li>
            <li><span style="color:var(--text-muted);">تلفن ۲۴ ساعته:</span> <strong style="color:var(--text-pure);" dir="ltr">۰۲۱-۸۸۸۸۴۴۴۴</strong></li>
            <li><span style="color:var(--text-muted);">دفتر مرکزی:</span> تهران، ونک، برج فناوری سلامت</li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div>© تمامی حقوق مادی و معنوی متعلق به شرکت دانش‌بنیان سلامت دیجیتال پزشکآن است.</div>
        <div style="display:flex; gap:16px;">
          <a href="/about">قوانین و محرمانگی PHI</a>
          <span>•</span>
          <a href="/contact">سلب مسئولیت پزشکی</a>
          <span>•</span>
          <a href="/mag">مجله سلامت بالینی</a>
        </div>
      </div>
    </div>
  </footer>
    '''

def wrap_page(title, content, active_page="home"):
    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | اکوسیستم سلامت دیجیتال پزشکآن</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;800&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="shared.css">
</head>
<body>

  {get_header(active_page)}

  <main>
    {content}
  </main>

  {get_footer()}

  <script src="three.min.js"></script>
  <script src="gsap.min.js"></script>
  <script src="lenis.min.js"></script>
  <script src="shared.js"></script>
</body>
</html>
'''

# ==============================================================================
# 1. HOMEPAGE CONTENT (portal/index.html)
# ==============================================================================
home_content = '''
  <!-- 01. Hero Section with 3D ECG Monitor & Widescreen Presence -->
  <section class="hero-section">
    <div class="container">
      <div class="hero-box">

        <!-- 3D Medical Device Console with Three.js WebGL & Dynamic Telemetry Screen -->
        <div class="hero-device-stage">
          <div id="threeDeviceContainer" class="three-device-container"></div>

          <!-- Subtle Scroll Hint: Placed DIRECTLY after ECG Device and visible on fold -->
          <div class="scroll-prompt-hint" id="scrollPromptHint" onclick="if(window.lenis){ window.lenis.scrollTo(window.scrollY + 480); } else { window.scrollBy({ top: 480, behavior: 'smooth' }); }" title="کلیک برای مشاهده سایر بخش‌ها">
            <span>سیستم مانیتورینگ آماده به کار است • برای مشاهده سایر بخش‌ها به پایین اسکرول کنید</span>
            <svg class="svg-icon scroll-arrow-bounce" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
        </div>

        <!-- Hero Text Block (Rendered smoothly below) -->
        <div class="hero-text-block">
          <div class="hero-pill-badge hero-anim-item">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            <span>اکوسیستم یکپارچه مدیریت درمان و پرونده الکترونیک سلامت</span>
          </div>

          <h1 class="hero-title hero-anim-item">
            پزشکـــآن؛ مدیریت هوشمند مطب و جریان مراجعین بدون اتلاف وقت
          </h1>
          
          <p class="hero-subtitle hero-anim-item">
            صرفه‌جویی ۳ دقیقه‌ای در هر ویزیت با قلم نوری، هشدار هوشمند تداخلات دارویی توسط دستیار بالینی AI، اتوماسیون کامل پذیرش منشی و پرونده ابری امن بیماران.
          </p>

          <div class="hero-actions hero-anim-item">
            <a href="/start" class="btn btn-primary" style="padding:12px 28px; font-size:15px;">
              <span>درخواست دمو و شروع همکاری</span>
              <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </a>
            <a href="/product" class="btn btn-secondary" style="padding:12px 24px; font-size:15px;">
              <span>کالبدشکافی ماژول‌های محصول</span>
              <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
            </a>
            <a href="/mag" class="btn btn-vital" style="padding:12px 24px; font-size:15px;">
              <span>مشاهده مجله سلامت پزشکآن</span>
              <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            </a>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- 02. Problem Statement: چالش‌های اتلاف وقت پزشکان -->
  <section style="padding:48px 0;">
    <div class="container">
      <div class="section-title-wrap">
        <span class="section-pill-tag">چالش‌های سنتی مطب‌ها</span>
        <h2 class="section-h2">چرا روزانه بیش از ۲ ساعت از وقت ارزشمند پزشک هدر می‌رود؟</h2>
        <p class="section-sub">بررسی دقیق موانع بهره‌وری در مطب‌های سنتی و علت اصلی ازدحام و نارضایتی بیماران</p>
      </div>

      <div class="grid-4">
        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(225,29,72,0.1); color:#E11D48;">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
          </div>
          <h3 class="card-h3">پراکندگی پرونده‌های کاغذی</h3>
          <p class="card-desc">جستجوی سوابق قدیمی بیمار میان انبوه زونکن‌ها و گم شدن تصاویر رادیولوژی و آزمایش‌ها.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(217,119,6,0.1); color:#D97706;">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          </div>
          <h3 class="card-h3">خستگی نگارش دستی شرح‌حال</h3>
          <p class="card-desc">صرف ۳ تا ۵ دقیقه زمان در هر ویزیت برای تایپ خسته‌کننده با کیبورد یا نگارش شتاب‌زده با خودکار.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(2,132,199,0.1); color:#0284C7;">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </div>
          <h3 class="card-h3">ازدحام و تماس‌های مکرر با منشی</h3>
          <p class="card-desc">اشغال دائمی تلفن مطب برای هماهنگی ویزیت و پاسخ به سوالات ساده درباره زمان حضور پزشک.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(124,58,237,0.1); color:#7C3AED;">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="10" y1="14" x2="14" y2="18"/><line x1="14" y1="14" x2="10" y2="18"/></svg>
          </div>
          <h3 class="card-h3">لغو ناگهانی نوبت‌ها (No-Show)</h3>
          <p class="card-desc">عدم مراجعه ۱۵ الی ۳۰ درصد بیماران بدون اطلاع قبلی و اتلاف وقت پزشک و ضرر مالی کلینیک.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 03. Product Solution: پاسخ یکپارچه پزشکآن -->
  <section style="padding:48px 0; background:var(--bg-surface-secondary);">
    <div class="container">
      <div class="section-title-wrap">
        <span class="section-pill-tag">پاسخ مهندسی پزشکآن</span>
        <h2 class="section-h2">یک اکوسیستم جامع برای مدیریت ۰ تا ۱۰۰ درمان</h2>
        <p class="section-sub">اتصال یکپارچه پزشک، منشی، بیمارستان و مراجعین در یک بستر ابری امن و فوق‌سریع</p>
      </div>

      <div class="grid-3">
        <div class="panel-card">
          <div class="card-icon-wrap">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          </div>
          <h3 class="card-h3">پرونده الکترونیک سلامت (EMR)</h3>
          <p class="card-desc">ثبت سریع شرح‌حال با قلم نوری، بارگذاری آنی تصاویر MRI و آزمایش‌ها با دسترسی مادام‌العمر امن.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(5,150,105,0.1); color:#059669;">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2z"/><path d="M12 2a10 10 0 0 1 10 10h-10V2z"/></svg>
          </div>
          <h3 class="card-h3">دستیار بالینی هوش مصنوعی</h3>
          <p class="card-desc">پایش بلادرنگ تداخلات دارویی، پیشنهاد آزمایش‌های تکمیلی و اردرست‌های اختصاصی هر تخصص.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(217,119,6,0.1); color:#D97706;">
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>
          </div>
          <h3 class="card-h3">میزکار هوشمند منشی و کارتخوان</h3>
          <p class="card-desc">اتصال مستقیم نرم‌افزار به پوز بانکی، مدیریت صف یونیت‌ها و حذف کامل خطای تسویه حساب مطب.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 04. Treatment Journey: تایم‌لاین امضای پزشکآن -->
  <section style="padding:56px 0;">
    <div class="container">
      <div class="section-title-wrap">
        <span class="section-pill-tag">امضای معماری پزشکآن</span>
        <h2 class="section-h2">مسیر ۶ مرحله‌ای درمان هوشمند (Treatment Journey)</h2>
        <p class="section-sub">از نخستین رزرو نوبت تا تکمیل سیر بهبودی بیمار با سیگنال‌های هدایت‌گر بالینی</p>
      </div>

      <div class="journey-timeline">
        <div class="journey-step">
          <div class="journey-step-num">۱</div>
          <h4 class="journey-step-title">نوبت‌دهی هوشمند</h4>
          <p class="journey-step-desc">رزرو از سایت با پیامک تایید حاوی لینک لوکیشن و توصیه‌های پیش از ویزیت.</p>
        </div>
        <div class="journey-step">
          <div class="journey-step-num">۲</div>
          <h4 class="journey-step-title">پذیرش بدون صف</h4>
          <p class="journey-step-desc">ورود به مطب، ثبت با کارتخوان و تخصیص آنی شماره در مانیتور سالن انتظار.</p>
        </div>
        <div class="journey-step">
          <div class="journey-step-num">۳</div>
          <h4 class="journey-step-title">تریاژ بالینی اولیه</h4>
          <p class="journey-step-desc">ثبت علائم حیاتی (فشار، وزن، اکسیژن) توسط دستیار در پرونده الکترونیک.</p>
        </div>
        <div class="journey-step">
          <div class="journey-step-num">۴</div>
          <h4 class="journey-step-title">ویزیت با قلم نوری</h4>
          <p class="journey-step-desc">معاینه پزشک، رسم آناتومی، انتخاب اردرست‌ها با یک کلیک و ثبت کد ICD-10.</p>
        </div>
        <div class="journey-step">
          <div class="journey-step-num">۵</div>
          <h4 class="journey-step-title">نسخه هوشمند</h4>
          <p class="journey-step-desc">ارسال خودکار نسخه به بیمه تامین اجتماعی/سلامت همراه با بررسی تداخل دارو.</p>
        </div>
        <div class="journey-step">
          <div class="journey-step-num">۶</div>
          <h4 class="journey-step-title">پیگیری و وفادارسازی</h4>
          <p class="journey-step-desc">ارسال برنامه مصرف دارو، پیامک احوال‌پرسی خودکار و یادآوری چکاپ مجدد.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 05. Packages Preview: تعرفه‌ها -->
  <section style="padding:48px 0; background:var(--bg-surface-secondary);">
    <div class="container">
      <div class="section-title-wrap">
        <span class="section-pill-tag">تعرفه‌های شفاف</span>
        <h2 class="section-h2">پلن‌های متناسب با مقیاس مطب و کلینیک شما</h2>
        <p class="section-sub">بدون هزینه پنهان، همراه با پشتیبانی فنی ۲۴ ساعته و استقرار حضوری در مطب</p>
      </div>

      <div class="grid-3">
        <div class="pricing-card">
          <div class="price-title">طرح پایه (Starter)</div>
          <div class="price-desc">ویژه مطب‌های تک‌پزشک با مراجعه متوسط</div>
          <div class="price-amount-box">
            <span class="price-amount">۱,۴۵۰,۰۰۰</span>
            <span class="price-unit">تومان / ماهانه</span>
          </div>
          <ul class="pricing-features-list">
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پرونده الکترونیک سلامت نامحدود</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> اتصال به سامانه نسخه الکترونیک بیمه‌ها</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پنل نوبت‌دهی آنلاین با یادآور پیامکی</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پشتیبانی تلفنی در ساعات اداری</li>
          </ul>
          <a href="/start?plan=starter" class="btn btn-secondary" style="width:100%; justify-content:center;">انتخاب طرح پایه</a>
        </div>

        <div class="pricing-card popular">
          <span class="popular-badge">بیشترین انتخاب پزشکان</span>
          <div class="price-title">طرح حرفه‌ای (Pro)</div>
          <div class="price-desc">ویژه مطب‌های پرمراجعه و ۲ یونیت فعال</div>
          <div class="price-amount-box">
            <span class="price-amount" style="color:var(--brand-primary);">۲,۸۵۰,۰۰۰</span>
            <span class="price-unit">تومان / ماهانه</span>
          </div>
          <ul class="pricing-features-list">
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> تمام قابلیت‌های طرح پایه</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> <strong>دستیار بالینی هوش مصنوعی (AI Copilot)</strong></li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> اتصال مستقیم دستگاه کارتخوان مطب به EMR</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پشتیبانی اختصاصی ۲۴ ساعته VIP</li>
          </ul>
          <a href="/start?plan=pro" class="btn btn-primary" style="width:100%; justify-content:center;">شروع با طرح حرفه‌ای</a>
        </div>

        <div class="pricing-card">
          <div class="price-title">سازمانی (Enterprise)</div>
          <div class="price-desc">ویژه کلینیک‌های چندتخصصی و بیمارستان‌ها</div>
          <div class="price-amount-box">
            <span class="price-amount">تماس بگیرید</span>
            <span class="price-unit">تعرفه سفارشی</span>
          </div>
          <ul class="pricing-features-list">
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> کاربران و یونیت‌های درمانی نامحدود</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> سرور اختصاصی و پایگاه داده ایزوله بیمارستان</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> اتصال به سامانه‌های HIS و PACS تصویربرداری</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> استقرار و آموزش حضوری کلیه پرسنل</li>
          </ul>
          <a href="/contact?subject=enterprise" class="btn btn-secondary" style="width:100%; justify-content:center;">مشاوره سازمانی</a>
        </div>
      </div>
    </div>
  </section>

  <!-- 06. Trust & Pilot Clinic Results: دکتر ناصح -->
  <section style="padding:56px 0;">
    <div class="container">
      <div class="section-title-wrap">
        <span class="section-pill-tag">نتایج بالینی مستند</span>
        <h2 class="section-h2">رضایت ۹۸٪ پزشکان در کلینیک‌های پایلوت</h2>
        <p class="section-sub">گزارش عملکرد واقعی سامانه در کلینیک پایلوت دکتر ناصح و سایر مراکز درمانی همکار</p>
      </div>

      <div class="grid-3">
        <div class="panel-card" style="text-align:center;">
          <div style="font-size:36px; font-weight:900; color:var(--brand-primary); font-family:'JetBrains Mono', var(--font-family);">۷۸٪</div>
          <h4 style="font-size:16px; font-weight:800; margin:8px 0;">کاهش تماس‌های تلفنی منشی</h4>
          <p style="font-size:13px; color:var(--text-muted);">پاسخ خودکار به سوالات نوبت‌دهی و لوکیشن از طریق پیامک‌های هوشمند.</p>
        </div>

        <div class="panel-card" style="text-align:center;">
          <div style="font-size:36px; font-weight:900; color:var(--brand-emerald-vital); font-family:'JetBrains Mono', var(--font-family);">۳ دقیقه</div>
          <h4 style="font-size:16px; font-weight:800; margin:8px 0;">تسریع در هر ویزیت</h4>
          <p style="font-size:13px; color:var(--text-muted);">بهره‌مندی از قالب‌های آماده معاینات بالینی و ثبت شرح‌حال با قلم نوری.</p>
        </div>

        <div class="panel-card" style="text-align:center;">
          <div style="font-size:36px; font-weight:900; color:var(--brand-amber); font-family:'JetBrains Mono', var(--font-family);">۵۰۰,۰۰۰+</div>
          <h4 style="font-size:16px; font-weight:800; margin:8px 0;">نسخه الکترونیک موفق</h4>
          <p style="font-size:13px; color:var(--text-muted);">بدون قطعی حتی در ساعات اوج بار با آپ‌تایم ۹۹.۹۸٪ سرورهای ابری.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 07. Latest from Health Magazine -->
  <section style="padding:48px 0; background:var(--bg-surface-secondary);">
    <div class="container">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:32px; flex-wrap:wrap; gap:16px;">
        <div>
          <span class="section-pill-tag">مجله سلامت پزشکآن</span>
          <h2 class="section-h2" style="margin:0;">تازه‌ترین مقالات بالینی و سبک زندگی</h2>
        </div>
        <a href="/mag" class="btn btn-secondary">
          <span>ورود به مجله اکسون‌لایف</span>
          <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        </a>
      </div>

      <div class="grid-3">
        <div class="panel-card" style="padding:0; overflow:hidden;">
          <img src="https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=600&q=80" alt="دیسک کمر" style="width:100%; height:180px; object-fit:cover;">
          <div style="padding:20px;">
            <span style="font-size:11px; background:#E0F2FE; color:#0369A1; padding:2px 8px; border-radius:4px; font-weight:700;">ستون فقرات و درد</span>
            <h3 style="font-size:15.5px; font-weight:800; margin:10px 0 6px;"><a href="/mag">درمان غیرجراحی دیسک کمر و سیاتیک: از شاک‌ویو تا لیزر</a></h3>
            <p style="font-size:12.5px; color:var(--text-muted); line-height:1.6;">راهکارهای مدرن طب فیزیکی بدون نیاز به بیهوشی و جراحی باز.</p>
          </div>
        </div>

        <div class="panel-card" style="padding:0; overflow:hidden;">
          <img src="https://images.unsplash.com/photo-1559757175-5700dde675bc?auto=format&fit=crop&w=600&q=80" alt="حمله قلبی" style="width:100%; height:180px; object-fit:cover;">
          <div style="padding:20px;">
            <span style="font-size:11px; background:#ECFDF5; color:#065F46; padding:2px 8px; border-radius:4px; font-weight:700;">قلب و عروق</span>
            <h3 style="font-size:15.5px; font-weight:800; margin:10px 0 6px;"><a href="/mag">علائم هشداردهنده سکته قلبی در بانوان و زمان طلایی</a></h3>
            <p style="font-size:12.5px; color:var(--text-muted); line-height:1.6;">تفاوت‌های تریاژ انفارکتوس میوکارد در زنان و معیارهای ارجاع فوری.</p>
          </div>
        </div>

        <div class="panel-card" style="padding:0; overflow:hidden;">
          <img src="https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=600&q=80" alt="میگرن" style="width:100%; height:180px; object-fit:cover;">
          <div style="padding:20px;">
            <span style="font-size:11px; background:#FEF3C7; color:#92400E; padding:2px 8px; border-radius:4px; font-weight:700;">مغز و اعصاب</span>
            <h3 style="font-size:15.5px; font-weight:800; margin:10px 0 6px;"><a href="/mag">پروتکل تریاژ بالینی سردردهای میگرنی و اورژانس ردفلگ</a></h3>
            <p style="font-size:12.5px; color:var(--text-muted); line-height:1.6;">تزریق بوتاکس درمانی، آنتی‌بادی‌های CGRP و تمایز با سکته مغزی.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 08. Congress Special Offer Banner -->
  <section class="container">
    <div class="congress-banner">
      <div class="congress-content">
        <h3>آفر اختصاصی کنگره پزشکی آبان ۱۴۰۵</h3>
        <p>
          پزشکان و مدیران مراکزی که از طریق وب‌سایت ثبت‌نام کنند، از <strong>۳ ماه اشتراک کاملاً رایگان</strong> به همراه نصب و استقرار حضوری در مطب بهره‌مند خواهند شد.
        </p>
      </div>
      <div>
        <a href="/start?offer=congress" class="btn" style="background:#FFFFFF; color:#0073FF; font-weight:900; font-size:15px; padding:12px 28px;">
          دریافت بسته هدیه کنگره
        </a>
      </div>
    </div>
  </section>
'''

# Write portal/index.html
with open(os.path.join(PORTAL_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(wrap_page("صفحه اصلی", home_content, "home"))

print("Generated: portal/index.html")

# ==============================================================================
# 2. PRODUCT PAGE (portal/product.html)
# ==============================================================================
product_content = '''
  <section style="padding:48px 0 24px;">
    <div class="container">
      <div class="hero-box" style="margin-top:0;">
        <span class="hero-pill-badge">کالبدشکافی ماژول‌های پلتفرم</span>
        <h1 class="hero-title">فراتر از یک نرم‌افزار نوبت‌دهی؛ سیستم جامع مدیریت درمان</h1>
        <p class="hero-subtitle">
          پزشکآن ۵ ماژول فوق‌پیشرفته را در یک بستر هماهنگ ادغام کرده است تا تجربه مطب‌داری، کیفیت ویزیت و تعامل با بیماران را به بالاترین استاندارد جهانی ارتقا دهد.
        </p>
        <div style="display:flex; gap:12px; flex-wrap:wrap;">
          <a href="/start" class="btn btn-primary">درخواست تست رایگان در مطب</a>
          <a href="/packages" class="btn btn-secondary">مشاهده تعرفه‌ها</a>
        </div>
      </div>
    </div>
  </section>

  <section style="padding:24px 0 56px;">
    <div class="container">
      
      <!-- Module 1: EMR -->
      <div class="panel-card" style="margin-bottom:32px;">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:36px; align-items:center;">
          <div>
            <span class="section-pill-tag">ماژول شماره ۱</span>
            <h2 style="font-size:24px; font-weight:900; color:var(--text-pure); margin-bottom:12px;">پرونده الکترونیک سلامت (EMR) با قلم نوری</h2>
            <p style="color:var(--text-secondary); line-height:1.9; margin-bottom:18px;">
              حس نگارش طبیعی روی کاغذ بدون معطلی تایپ! با قلم‌های نوری حساس به فشار و کدهای بین‌المللی ICD-10، شرح‌حال بیمار را در کمتر از ۱ دقیقه ثبت کنید.
            </p>
            <ul style="list-style:none; display:flex; flex-direction:column; gap:10px; font-size:13.5px;">
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> رسم آناتومی بدن، مشخص کردن موضع درد و ترسیم شماتیک ضایعات</li>
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> بارگذاری فایل‌های دایکام (DICOM)، سی‌تی‌اسکن و آزمایش‌های آزمایشگاهی</li>
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> دسترسی سریع به سیر درمانی و نسخه‌های پیشین بیمار در ۱ ثانیه</li>
            </ul>
          </div>
          <div style="background:var(--bg-canvas); border:1px solid var(--glass-border); border-radius:var(--radius-lg); padding:24px; text-align:center;">
            <div style="font-size:12px; color:var(--brand-primary); font-weight:800; margin-bottom:10px;">پیش‌نمایش محیط EMR ویزیت</div>
            <img src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=600&q=80" alt="EMR" style="width:100%; height:240px; object-fit:cover; border-radius:var(--radius-md);">
          </div>
        </div>
      </div>

      <!-- Module 2: AI Clinical Copilot -->
      <div class="panel-card" style="margin-bottom:32px;" id="ai">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:36px; align-items:center;">
          <div style="order:2;">
            <span class="section-pill-tag" style="background:rgba(5,150,105,0.1); color:#059669;">ماژول شماره ۲</span>
            <h2 style="font-size:24px; font-weight:900; color:var(--text-pure); margin-bottom:12px;">دستیار بالینی هوش مصنوعی (AI Clinical Copilot)</h2>
            <p style="color:var(--text-secondary); line-height:1.9; margin-bottom:18px;">
              چشم دوم پزشک در مطب! هنگام ثبت دارو، هوش مصنوعی تداخلات خطرناک با داروهای پیشین بیمار را به صورت هشدار قرمز نمایش می‌دهد.
            </p>
            <ul style="list-style:none; display:flex; flex-direction:column; gap:10px; font-size:13.5px;">
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پایش دوز مجاز دارو بر اساس وزن، سن، کراتینین و عملکرد کلیه</li>
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پیشنهاد اردرست‌های آزمایشگاهی تکمیلی مطابق گایدلاین‌های ۲۰۲۶</li>
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> صفر کردن خطاهای ناخواسته دارویی و کاهش دعاوی حقوقی پزشکی</li>
            </ul>
          </div>
          <div style="order:1; background:var(--bg-canvas); border:1px solid var(--glass-border); border-radius:var(--radius-lg); padding:24px; text-align:center;">
            <div style="font-size:12px; color:#059669; font-weight:800; margin-bottom:10px;">پایش تداخلات و هشدارهای تشخیصی</div>
            <img src="https://images.unsplash.com/photo-1530497610245-94d3c16cda28?auto=format&fit=crop&w=600&q=80" alt="AI Copilot" style="width:100%; height:240px; object-fit:cover; border-radius:var(--radius-md);">
          </div>
        </div>
      </div>

      <!-- Module 3: Reception Desk -->
      <div class="panel-card" style="margin-bottom:32px;">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:36px; align-items:center;">
          <div>
            <span class="section-pill-tag">ماژول شماره ۳</span>
            <h2 style="font-size:24px; font-weight:900; color:var(--text-pure); margin-bottom:12px;">میزکار منشی و سیستم پذیرش پوز متصل</h2>
            <p style="color:var(--text-secondary); line-height:1.9; margin-bottom:18px;">
              پایان ازدحام سالن انتظار مطب! منشی با کشیدن کارتخوان مبلغ ویزیت را از نرم‌افزار بدون امکان اشتباه به پوز ارسال کرده و نوبت بیمار را در مانیتور فعال می‌کند.
            </p>
            <ul style="list-style:none; display:flex; flex-direction:column; gap:10px; font-size:13.5px;">
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> صف‌بندی هوشمند چند یونیت درمانی و نمایش زمان تخمینی ویزیت</li>
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> محاسبه خودکار درصد پزشکان سهام‌دار و پزشکان پرکیس مطب</li>
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> گزارش مالی روزانه و انطباق ۱۰۰٪ با سامانه مودیان مالیاتی</li>
            </ul>
          </div>
          <div style="background:var(--bg-canvas); border:1px solid var(--glass-border); border-radius:var(--radius-lg); padding:24px; text-align:center;">
            <div style="font-size:12px; color:var(--brand-primary); font-weight:800; margin-bottom:10px;">مدیریت صف و کارتخوان هوشمند</div>
            <img src="https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=600&q=80" alt="Reception" style="width:100%; height:240px; object-fit:cover; border-radius:var(--radius-md);">
          </div>
        </div>
      </div>

      <!-- Module 4: Patient Portal -->
      <div class="panel-card" style="margin-bottom:32px;">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:36px; align-items:center;">
          <div style="order:2;">
            <span class="section-pill-tag">ماژول شماره ۴</span>
            <h2 style="font-size:24px; font-weight:900; color:var(--text-pure); margin-bottom:12px;">پورتال اختصاصی و اپلیکیشن پرونده بیمار</h2>
            <p style="color:var(--text-secondary); line-height:1.9; margin-bottom:18px;">
              بیمار سوابق نسخه‌ها، دستورات دارویی و تاریخچه مراجعات خود را همیشه در گوشی همراه دارد. دیگر نیازی به تماس تلفنی برای پرسیدن ساعت مصرف دارو نیست.
            </p>
            <ul style="list-style:none; display:flex; flex-direction:column; gap:10px; font-size:13.5px;">
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> یادآوری هوشمند پیامکی برای روز و ساعت مصرف داروهای حیاتی</li>
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> رزرو نوبت پیگیری (Follow-up) با یک کلیک بدون انتظار پشت خط</li>
              <li style="display:flex; gap:8px; align-items:center;"><svg class="svg-icon" style="width:14px; height:14px; color:#059669; flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> ثبت رضایت‌سنجی و نظرسنجی درمان برای تقویت برند مطب</li>
            </ul>
          </div>
          <div style="order:1; background:var(--bg-canvas); border:1px solid var(--glass-border); border-radius:var(--radius-lg); padding:24px; text-align:center;">
            <div style="font-size:12px; color:var(--brand-primary); font-weight:800; margin-bottom:10px;">پورتال موبایلی بیمار</div>
            <img src="https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=600&q=80" alt="Patient Portal" style="width:100%; height:240px; object-fit:cover; border-radius:var(--radius-md);">
          </div>
        </div>
      </div>

      <!-- Module 5: PHI Security -->
      <div class="panel-card" style="border-right:4px solid #059669;">
        <span class="section-pill-tag" style="background:rgba(5,150,105,0.1); color:#059669;">امنیت درجه پزشکی (Medical Grade Security)</span>
        <h2 style="font-size:22px; font-weight:900; color:var(--text-pure); margin:8px 0 12px;">حفاظت ۱۰۰٪ از داده‌های سلامت (PHI & HIPAA Compliance)</h2>
        <p style="color:var(--text-secondary); line-height:1.9;">
          اطلاعات پرونده بیماران با پیشرفته‌ترین رمزنگاری AES-256 و پروتکل کنترل دسترسی نقشی (RBAC) محافظت می‌شود. هیچ فردی جز پزشک معالج به جزئیات شرح‌حال محرمانه بیمار دسترسی نخواهد داشت و تمامی ورودها در لاگ‌های حسابرسی دیجیتال ثبت می‌گردد.
        </p>
      </div>

    </div>
  </section>
'''

with open(os.path.join(PORTAL_DIR, "product.html"), "w", encoding="utf-8") as f:
    f.write(wrap_page("معرفی محصول و ماژول‌ها", product_content, "product"))

print("Generated: portal/product.html")

# ==============================================================================
# 3. FEATURES PAGE (portal/features.html)
# ==============================================================================
features_content = '''
  <section style="padding:48px 0 32px;">
    <div class="container">
      <div class="section-title-wrap">
        <span class="section-pill-tag">تفکیک نقش‌محور قابلیت‌ها</span>
        <h1 class="section-h2" style="font-size:32px;">قابلیت‌های اکوسیستم پزشکآن برای تمام اعضای درمان</h1>
        <p class="section-sub">تفکیک دقیق ابزارها بر اساس نیازهای واقعی پزشک، منشی مطب، مدیر کلینیک و بیمار</p>
      </div>

      <div class="grid-2" style="gap:28px;">
        <!-- Role A: Doctor -->
        <div class="panel-card">
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
            <div class="card-icon-wrap" style="margin:0;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
            <div>
              <h3 style="font-size:18px; font-weight:800; color:var(--text-pure);">تجربه پزشک (Doctor Experience)</h3>
              <span style="font-size:12px; color:var(--brand-primary); font-weight:700;">تسریع ویزیت و تمرکز بر درمان</span>
            </div>
          </div>
          <ul style="list-style:none; display:flex; flex-direction:column; gap:10px; font-size:13.5px; color:var(--text-secondary); line-height:1.7;">
            <li>• پشتیبانی کامل از قلم نوری و شناسایی دست‌خط پزشک</li>
            <li>• ثبت کدهای استاندارد بین‌المللی تشخیص (ICD-10) با یک جستجوی صوتی یا متنی</li>
            <li>• بسته‌های اردرست دارویی از پیش‌تعریف‌شده برای هر تخصص (قلب، ارتوپدی، زنان...)</li>
            <li>• پایش تداخلات دارویی و هشدارهای بالینی با هوش مصنوعی</li>
            <li>• دسترسی به آرشیو تصاویر رادیولوژی و ام‌آر‌آی در کمتر از ۲ ثانیه</li>
          </ul>
        </div>

        <!-- Role B: Clinic Management -->
        <div class="panel-card">
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
            <div class="card-icon-wrap" style="margin:0; background:rgba(5,150,105,0.1); color:#059669;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg></div>
            <div>
              <h3 style="font-size:18px; font-weight:800; color:var(--text-pure);">مدیریت کلینیک و منشی (Clinic Operations)</h3>
              <span style="font-size:12px; color:#059669; font-weight:700;">صفر شدن صف و انضباط کامل مالی</span>
            </div>
          </div>
          <ul style="list-style:none; display:flex; flex-direction:column; gap:10px; font-size:13.5px; color:var(--text-secondary); line-height:1.7;">
            <li>• اتصال مستقیم صندوق به کارتخوان بانکی و جلوگیری از خطای دستی منشی</li>
            <li>• سیستم صف هوشمند و اعلام صوتی نوبت‌ها در مانیتور سالن انتظار</li>
            <li>• انبارداری داروها و مواد مصرفی یونیت‌ها با هشدار پایان موجودی</li>
            <li>• محاسبه دقیق سهم پزشکان بر اساس تعرفه خدمات و کسورات قانونی</li>
            <li>• مدیریت چند شیفت کاری و دسترسی جداگانه برای منشی‌های صبح و عصر</li>
          </ul>
        </div>

        <!-- Role C: Patient Journey -->
        <div class="panel-card">
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
            <div class="card-icon-wrap" style="margin:0; background:rgba(217,119,6,0.1); color:#D97706;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg></div>
            <div>
              <h3 style="font-size:18px; font-weight:800; color:var(--text-pure);">سفر بیمار (Patient Journey)</h3>
              <span style="font-size:12px; color:#D97706; font-weight:700;">آرامش خاطر و دسترسی آسان به درمان</span>
            </div>
          </div>
          <ul style="list-style:none; display:flex; flex-direction:column; gap:10px; font-size:13.5px; color:var(--text-secondary); line-height:1.7;">
            <li>• رزرو نوبت اینترنتی با انتخاب زمان دقیق حضور و پزشک معالج</li>
            <li>• دریافت پیامک تایید با نقشه مطب و دستورالعمل آمادگی قبل از آزمایش</li>
            <li>• دسترسی ابری امن به نسخه‌ها و سوابق آزمایشگاهی در هر زمان و مکان</li>
            <li>• امکان ارسال سوالات پیگیری دوره درمان به دستیار پزشک</li>
            <li>• ثبت بازخورد و ارزیابی کیفیت خدمت پس از پایان ویزیت</li>
          </ul>
        </div>

        <!-- Role D: Automation -->
        <div class="panel-card">
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
            <div class="card-icon-wrap" style="margin:0; background:rgba(124,58,237,0.1); color:#7C3AED;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></div>
            <div>
              <h3 style="font-size:18px; font-weight:800; color:var(--text-pure);">اتوماسیون هوشمند (Smart Automation)</h3>
              <span style="font-size:12px; color:#7C3AED; font-weight:700;">حذف کارهای تکراری و اداری</span>
            </div>
          </div>
          <ul style="list-style:none; display:flex; flex-direction:column; gap:10px; font-size:13.5px; color:var(--text-secondary); line-height:1.7;">
            <li>• سیستم جایگزینی سریع بیماران در لیست انتظار در صورت لغو نوبت</li>
            <li>• همگام‌سازی بلادرنگ با سرورهای تامین اجتماعی و بیمه سلامت بدون قطعی</li>
            <li>• ارسال خودکار پیامک تبریک تولد، یادآوری تمدید نسخه و چکاپ سالانه</li>
            <li>• تهیه نسخه پشتیبان ابری خودکار هر ۶ ساعت در سرورهای ایزوله بانکی</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
'''

with open(os.path.join(PORTAL_DIR, "features.html"), "w", encoding="utf-8") as f:
    f.write(wrap_page("قابلیت‌های اکوسیستم پزشکآن", features_content, "features"))

print("Generated: portal/features.html")

# ==============================================================================
# 4. PACKAGES & PRICING PAGE (portal/packages.html)
# ==============================================================================
packages_content = '''
  <section style="padding:48px 0 24px;">
    <div class="container">
      <div class="section-title-wrap">
        <span class="section-pill-tag">تعرفه‌های شفاف و منصفانه</span>
        <h1 class="section-h2" style="font-size:32px;">پلن مناسب مطب یا کلینیک خود را انتخاب کنید</h1>
        <p class="section-sub">با ۲۰٪ تخفیف در پرداخت سالانه، همراه با استقرار حضوری رایگان در مطب و پشتیبانی ۲۴ ساعته</p>
      </div>

      <!-- Pricing Switcher -->
      <div class="pricing-switcher-wrap">
        <span style="font-size:13.5px; font-weight:700; color:var(--text-primary);">پرداخت ماهانه</span>
        <span style="background:rgba(5,150,105,0.1); color:#059669; padding:4px 10px; border-radius:var(--radius-full); font-size:11.5px; font-weight:800;">۲۰٪ تخفیف سالانه</span>
      </div>

      <div class="grid-3">
        <div class="pricing-card">
          <div class="price-title">طرح پایه (Starter)</div>
          <div class="price-desc">ویژه مطب‌های تک‌پزشک با مراجعه روزانه تا ۳۰ بیمار</div>
          <div class="price-amount-box">
            <span class="price-amount">۱,۴۵۰,۰۰۰</span>
            <span class="price-unit">تومان / ماهانه</span>
          </div>
          <ul class="pricing-features-list">
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پرونده الکترونیک سلامت نامحدود</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> ثبت نسخه الکترونیک تامین اجتماعی و سلامت</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پنل نوبت‌دهی آنلاین با یادآور پیامکی</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> دسترسی تک کاربر منشی + ۱ پزشک</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پشتیبانی در ساعات اداری</li>
          </ul>
          <a href="/start?plan=starter" class="btn btn-secondary" style="width:100%; justify-content:center;">انتخاب طرح پایه</a>
        </div>

        <div class="pricing-card popular">
          <span class="popular-badge">انتخاب اول پزشکان و مراکز پرمراجعه</span>
          <div class="price-title">طرح حرفه‌ای (Pro)</div>
          <div class="price-desc">ویژه مطب‌های شلوغ، کلینیک‌های ۲ یونیت و تخصص‌های جراحی</div>
          <div class="price-amount-box">
            <span class="price-amount" style="color:var(--brand-primary);">۲,۸۵۰,۰۰۰</span>
            <span class="price-unit">تومان / ماهانه</span>
          </div>
          <ul class="pricing-features-list">
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> تمام قابلیت‌های طرح پایه به صورت نامحدود</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> <strong>دستیار بالینی هوش مصنوعی (AI Copilot)</strong></li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پشتیبانی از قلم نوری و کدهای ICD-10</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> اتصال مستقیم پوز بانکی به نرم‌افزار مطب</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پورتال اختصاصی و اپلیکیشن پرونده بیمار</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> پشتیبانی شبانه‌روزی ۲۴ ساعته VIP</li>
          </ul>
          <a href="/start?plan=pro" class="btn btn-primary" style="width:100%; justify-content:center;">شروع با طرح حرفه‌ای</a>
        </div>

        <div class="pricing-card">
          <div class="price-title">سازمانی (Enterprise)</div>
          <div class="price-desc">ویژه کلینیک‌های بزرگ، پلی‌کلینیک‌ها و بیمارستان‌ها</div>
          <div class="price-amount-box">
            <span class="price-amount">سفارشی</span>
            <span class="price-unit">بر اساس تعداد یونیت</span>
          </div>
          <ul class="pricing-features-list">
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> تعداد یونیت و پزشکان نامحدود</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> سرور ابری اختصاصی و پایگاه داده ایزوله</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> یکپارچگی با سامانه‌های HIS، PACS و آزمایشگاه</li>
            <li class="feature-item"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> مدیر حساب اختصاصی و تیم استقرار حضوری</li>
          </ul>
          <a href="/contact?subject=enterprise" class="btn btn-secondary" style="width:100%; justify-content:center;">تماس با واحد فروش سازمانی</a>
        </div>
      </div>
    </div>
  </section>
'''

with open(os.path.join(PORTAL_DIR, "packages.html"), "w", encoding="utf-8") as f:
    f.write(wrap_page("پکیج‌ها و تعرفه‌ها", packages_content, "packages"))

print("Generated: portal/packages.html")

# ==============================================================================
# 5. START & ONBOARDING WIZARD PAGE (portal/start.html)
# ==============================================================================
start_content = '''
  <section style="padding:48px 0 56px;">
    <div class="container" style="max-width:860px;">
      
      <div class="section-title-wrap">
        <span class="section-pill-tag">ویزارد هوشمند نیازسنجی مطب</span>
        <h1 class="section-h2" style="font-size:30px;">در ۵ دقیقه بهترین پلن متناسب با مطب خود را پیدا کنید</h1>
        <p class="section-sub">با پاسخ به ۴ سوال کوتاه، تیم فنی پزشکآن نسخه اختصاصی متناسب با تخصص شما را آماده و نصب می‌نماید.</p>
      </div>

      <div class="panel-card" style="padding:40px;">
        
        <!-- Step 1: Specialty -->
        <div id="wizardStep1" class="wizard-step">
          <div style="font-size:12px; font-weight:800; color:var(--brand-primary); margin-bottom:8px;">گام ۱ از ۴: تخصص پزشکی</div>
          <h3 style="font-size:18px; font-weight:900; color:var(--text-pure); margin-bottom:18px;">زمینه و تخصص فعالیت مطب یا مرکز درمانی شما چیست؟</h3>
          
          <div class="grid-2" style="gap:12px; margin-bottom:24px;">
            <label style="background:var(--bg-surface-secondary); padding:14px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; display:flex; align-items:center; gap:10px;">
              <input type="radio" name="specialty" value="مغز و اعصاب و ستون فقرات" checked>
              <strong>مغز، اعصاب و ستون فقرات</strong>
            </label>
            <label style="background:var(--bg-surface-secondary); padding:14px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; display:flex; align-items:center; gap:10px;">
              <input type="radio" name="specialty" value="قلب و عروق و دیابت">
              <strong>قلب، عروق و کنترل دیابت</strong>
            </label>
            <label style="background:var(--bg-surface-secondary); padding:14px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; display:flex; align-items:center; gap:10px;">
              <input type="radio" name="specialty" value="ارتوپدی و توانبخشی">
              <strong>ارتوپدی، مفاصل و فیزیوتراپی</strong>
            </label>
            <label style="background:var(--bg-surface-secondary); padding:14px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; display:flex; align-items:center; gap:10px;">
              <input type="radio" name="specialty" value="زنان و زایمان">
              <strong>زنان، زایمان و نازایی</strong>
            </label>
            <label style="background:var(--bg-surface-secondary); padding:14px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; display:flex; align-items:center; gap:10px;">
              <input type="radio" name="specialty" value="پوست، مو و زیبایی">
              <strong>پوست، مو و کلینیک زیبایی</strong>
            </label>
            <label style="background:var(--bg-surface-secondary); padding:14px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; display:flex; align-items:center; gap:10px;">
              <input type="radio" name="specialty" value="سایر تخصص‌های بالینی">
              <strong>سایر تخصص‌های بالینی و جراحی</strong>
            </label>
          </div>

          <div style="display:flex; justify-content:flex-end;">
            <button type="button" class="btn btn-primary" onclick="nextWizardStep(2)">ادامه مرحله بعد ↗</button>
          </div>
        </div>

        <!-- Step 2: Patients Volume -->
        <div id="wizardStep2" class="wizard-step" style="display:none;">
          <div style="font-size:12px; font-weight:800; color:var(--brand-primary); margin-bottom:8px;">گام ۲ از ۴: حجم مراجعین</div>
          <h3 style="font-size:18px; font-weight:900; color:var(--text-pure); margin-bottom:18px;">روزانه به طور میانگین چند بیمار ویزیت می‌فرمایید؟</h3>
          
          <div class="grid-3" style="gap:12px; margin-bottom:24px;">
            <label style="background:var(--bg-surface-secondary); padding:16px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; text-align:center;">
              <input type="radio" name="patientsVolume" value="کمتر از ۲۰ بیمار" checked>
              <div style="font-size:18px; font-weight:900; margin:8px 0 4px;">کمتر از ۲۰ بیمار</div>
              <div style="font-size:11.5px; color:var(--text-muted);">مطب انفرادی</div>
            </label>
            <label style="background:var(--bg-surface-secondary); padding:16px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; text-align:center;">
              <input type="radio" name="patientsVolume" value="۲۰ تا ۶۰ بیمار">
              <div style="font-size:18px; font-weight:900; margin:8px 0 4px;">۲۰ تا ۶۰ بیمار</div>
              <div style="font-size:11.5px; color:var(--text-muted);">مطب شلوغ و پرمراجعه</div>
            </label>
            <label style="background:var(--bg-surface-secondary); padding:16px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; text-align:center;">
              <input type="radio" name="patientsVolume" value="بیش از ۶۰ بیمار">
              <div style="font-size:18px; font-weight:900; margin:8px 0 4px;">بیش از ۶۰ بیمار</div>
              <div style="font-size:11.5px; color:var(--text-muted);">کلینیک چندتخصصی</div>
            </label>
          </div>

          <div style="display:flex; justify-content:space-between;">
            <button type="button" class="btn btn-secondary" onclick="nextWizardStep(1)">← مرحله قبل</button>
            <button type="button" class="btn btn-primary" onclick="nextWizardStep(3)">ادامه مرحله بعد ↗</button>
          </div>
        </div>

        <!-- Step 3: Main Challenge -->
        <div id="wizardStep3" class="wizard-step" style="display:none;">
          <div style="font-size:12px; font-weight:800; color:var(--brand-primary); margin-bottom:8px;">گام ۳ از ۴: هدف اصلی شما</div>
          <h3 style="font-size:18px; font-weight:900; color:var(--text-pure); margin-bottom:18px;">بزرگترین دغدغه‌ای که مایلید با پزشکآن حل شود چیست؟</h3>
          
          <div style="display:flex; flex-direction:column; gap:12px; margin-bottom:24px;">
            <label style="background:var(--bg-surface-secondary); padding:14px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; display:flex; align-items:center; gap:10px;">
              <input type="checkbox" name="challenges" value="قلم نوری و تسریع ثبت پرونده" checked>
              <span>نیاز به قلم نوری و سرعت بخشیدن به نگارش شرح‌حال</span>
            </label>
            <label style="background:var(--bg-surface-secondary); padding:14px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; display:flex; align-items:center; gap:10px;">
              <input type="checkbox" name="challenges" value="اتصال کارتخوان و انضباط منشی" checked>
              <span>اتصال کارتخوان به سیستم و نظم بخشیدن به پذیرش و صندوق مطب</span>
            </label>
            <label style="background:var(--bg-surface-secondary); padding:14px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; display:flex; align-items:center; gap:10px;">
              <input type="checkbox" name="challenges" value="کاهش لغو نوبت No-Show">
              <span>کاهش لغو نوبت‌ها (No-Show) و ساماندهی پیامک‌های نوبت‌دهی</span>
            </label>
            <label style="background:var(--bg-surface-secondary); padding:14px; border-radius:var(--radius-md); border:1px solid var(--glass-border); cursor:pointer; display:flex; align-items:center; gap:10px;">
              <input type="checkbox" name="challenges" value="نسخه الکترونیک بدون قطعی">
              <span>نسخه الکترونیک بیمه تامین اجتماعی بدون قطعی</span>
            </label>
          </div>

          <div style="display:flex; justify-content:space-between;">
            <button type="button" class="btn btn-secondary" onclick="nextWizardStep(2)">← مرحله قبل</button>
            <button type="button" class="btn btn-primary" onclick="nextWizardStep(4)">تکمیل اطلاعات پزشک ↗</button>
          </div>
        </div>

        <!-- Step 4: Contact Form -->
        <div id="wizardStep4" class="wizard-step" style="display:none;">
          <div style="font-size:12px; font-weight:800; color:var(--brand-primary); margin-bottom:8px;">گام نهایی: هماهنگی دمو حضوری</div>
          <h3 style="font-size:18px; font-weight:900; color:var(--text-pure); margin-bottom:18px;">مشخصات پزشک یا نماینده مرکز درمانی</h3>
          
          <div style="display:flex; flex-direction:column; gap:14px; margin-bottom:24px;">
            <div>
              <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:6px;">نام و نام خانوادگی پزشک / مدیر مرکز:</label>
              <input type="text" id="docName" class="form-control" placeholder="دکتر ..." style="padding:10px 14px; width:100%; border:1px solid var(--glass-border); border-radius:var(--radius-sm); font-family:var(--font-family);" required>
            </div>
            <div>
              <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:6px;">شماره همراه (جهت ارسال لینک پرتال و پیامک هماهنگی):</label>
              <input type="tel" id="docPhone" class="form-control" placeholder="۰۹۱۲..." style="padding:10px 14px; width:100%; border:1px solid var(--glass-border); border-radius:var(--radius-sm); font-family:var(--font-family);" dir="ltr" required>
            </div>
            <div>
              <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:6px;">شهر و آدرس مطب / کلینیک:</label>
              <input type="text" id="docAddress" class="form-control" placeholder="تهران، خیابان ولیعصر..." style="padding:10px 14px; width:100%; border:1px solid var(--glass-border); border-radius:var(--radius-sm); font-family:var(--font-family);">
            </div>
          </div>

          <div style="display:flex; justify-content:space-between;">
            <button type="button" class="btn btn-secondary" onclick="nextWizardStep(3)">مرحله قبل</button>
            <button type="button" class="btn btn-primary" onclick="submitWizard()">
              <span>ثبت و دریافت مشاوره تخصصی رایگان</span>
              <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </div>

        <!-- Success Result Step -->
        <div id="wizardStepSuccess" class="wizard-step" style="display:none; text-align:center; padding:20px 0;">
          <div style="width:64px; height:64px; border-radius:50%; background:rgba(5,150,105,0.1); color:#059669; display:inline-flex; align-items:center; justify-content:center; margin-bottom:16px;">
            <svg class="svg-icon" style="width:32px; height:32px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <h3 style="font-size:22px; font-weight:900; color:var(--text-pure); margin-bottom:8px;">درخواست شما با موفقیت ثبت گردید</h3>
          <p style="color:var(--text-secondary); line-height:1.8; max-width:520px; margin:0 auto 24px;">
            همکاران بخش پشتیبانی بالینی پزشکآن ظرف حداکثر ۲ ساعت کاری جهت هماهنگی جلسه دمو حضوری و تقدیم بسته هدیه کنگره با شما تماس خواهند گرفت.
          </p>
          <a href="/" class="btn btn-secondary">بازگشت به صفحه اصلی</a>
        </div>

      </div>

    </div>
  </section>

  <script>
    function nextWizardStep(stepNum) {
      for (let i = 1; i <= 4; i++) {
        const el = document.getElementById('wizardStep' + i);
        if (el) el.style.display = 'none';
      }
      const target = document.getElementById('wizardStep' + stepNum);
      if (target) target.style.display = 'block';
    }

    async function submitWizard() {
      const name = document.getElementById('docName').value.trim();
      const phone = document.getElementById('docPhone').value.trim();
      if (!name || !phone) {
        alert('لطفا نام و شماره همراه را وارد فرمایید.');
        return;
      }
      try {
        await fetch('/api/start-lead', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: name,
            phone: phone,
            address: document.getElementById('docAddress').value,
            createdAt: new Date().toISOString()
          })
        });
      } catch(e) {}
      
      for (let i = 1; i <= 4; i++) {
        document.getElementById('wizardStep' + i).style.display = 'none';
      }
      document.getElementById('wizardStepSuccess').style.display = 'block';
    }
  </script>
'''

with open(os.path.join(PORTAL_DIR, "start.html"), "w", encoding="utf-8") as f:
    f.write(wrap_page("شروع همکاری و ویزارد نیازسنجی مطب", start_content, "start"))

print("Generated: portal/start.html")

# ==============================================================================
# 6. SERVICES PAGE (portal/services.html)
# ==============================================================================
services_content = '''
  <section style="padding:48px 0 32px;">
    <div class="container">
      <div class="section-title-wrap">
        <span class="section-pill-tag">پشتیبانی و استقرار تخصصی</span>
        <h1 class="section-h2" style="font-size:32px;">خدمات مکمل استقرار اکوسیستم پزشکآن در مطب</h1>
        <p class="section-sub">تجهیز صفر تا صد سخت‌افزاری، آموزش حضوری به کادر درمان و تضمین امنیت شبکه مطب</p>
      </div>

      <div class="grid-3">
        <div class="panel-card">
          <div class="card-icon-wrap"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div>
          <h3 class="card-h3">تجهیز سخت‌افزاری و قلم نوری</h3>
          <p class="card-desc">تامین و کالیبراسیون تخصصی قلم‌های نوری حساس به فشار ویژه ویزیت پزشک، دستگاه‌های کارتخوان چندکاره و تبلت‌های بالینی.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(5,150,105,0.1); color:#059669;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg></div>
          <h3 class="card-h3">راه‌اندازی شبکه امن و ایزوله مطب</h3>
          <p class="card-desc">پیکربندی شبکه محلی بی‌سیم با فایروال پزشکی جهت جلوگیری از هرگونه نفوذ خارجی و تضمین اتصال پرسرعت بدون قطعی به سرور.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(217,119,6,0.1); color:#D97706;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
          <h3 class="card-h3">آموزش حضوری کادر مطب و منشی‌ها</h3>
          <p class="card-desc">اعزام کارشناس ارشد استقرار به مطب شما جهت آموزش گام‌به‌گام به منشی و دستیار و تضمین تسلط کامل آنها ظرف ۳ روز کاری.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(124,58,237,0.1); color:#7C3AED;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
          <h3 class="card-h3">پشتیبانی VIP و خط مستقیم پزشکان</h3>
          <p class="card-desc">شماره تماس اختصاصی ویژه پزشکان جهت رفع هرگونه پرسش بالینی یا فنی در کمتر از ۳ دقیقه توسط کارشناسان ارشد نرم‌افزار.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(2,132,199,0.1); color:#0284C7;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></div>
          <h3 class="card-h3">تولید محتوای ویدئویی پزشکی (ON-SUPP)</h3>
          <p class="card-desc">بازوی تخصصی سناریونویسی و تصویربرداری در مطب برای پزشکانی که مایل به افزایش مراجعین با انتشار محتوای موثق در مجله سلامت هستند.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(225,29,72,0.1); color:#E11D48;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg></div>
          <h3 class="card-h3">مهاجرت داده‌ها از نرم‌افزارهای قدیمی</h3>
          <p class="card-desc">انتقال بدون خطا و رایگان تمامی اطلاعات بیماران و سوابق پرونده‌ها از نرم‌افزارهای سنتی پیشین شما به ساختار ابری پزشکآن.</p>
        </div>
      </div>
    </div>
  </section>
'''

with open(os.path.join(PORTAL_DIR, "services.html"), "w", encoding="utf-8") as f:
    f.write(wrap_page("خدمات جامع استقرار و تجهیز مطب", services_content, "services"))

print("Generated: portal/services.html")

# ==============================================================================
# 7. ABOUT US PAGE (portal/about.html)
# ==============================================================================
about_content = '''
  <section style="padding:48px 0 32px;">
    <div class="container">
      <div class="section-title-wrap">
        <span class="section-pill-tag">داستان و رسالت ما</span>
        <h1 class="section-h2" style="font-size:32px;">پزشکآن؛ بازتعریف رابطه پزشک، درمان و فناوری</h1>
        <p class="section-sub">یک پلتفرم دانش‌بنیان خلق‌شده با همفکری مستقیم جراحان، متخصصان بالینی و مهندسان هوش مصنوعی</p>
      </div>

      <div class="panel-card" style="margin-bottom:36px;">
        <h3 style="font-size:20px; font-weight:900; color:var(--text-pure); margin-bottom:12px;">رسالت بنیادین ما در سلامت دیجیتال ایران</h3>
        <p style="color:var(--text-secondary); line-height:2.0; font-size:15px;">
          اکوسیستم سلامت «پزشکآن» با این باور بنیادین متولد شد که فناوری نباید بار اضافه بر دوش پزشک باشد، بلکه باید زمان او را برای توجه عمیق به بیمار آزاد کند. ما با حذف اصطکاک‌های فرساینده اداری، پرونده‌های کاغذی و خطاهای دستی، مطب‌های پزشکی را به مدرن‌ترین مراکز پایش سلامت تبدیل می‌کنیم.
        </p>
      </div>

      <div class="grid-3" style="margin-bottom:40px;">
        <div class="panel-card">
          <div class="card-icon-wrap"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
          <h4 style="font-size:16.5px; font-weight:800; margin-bottom:8px;">حریم خصوصی و رازداری بالینی</h4>
          <p style="font-size:13px; color:var(--text-secondary); line-height:1.8;">اطلاعات پرونده پزشکی بیماران امانتی مقدس است. بالاترین پروتکل‌های رمزنگاری در سرورهای ایزوله حافظ حریم مطب شماست.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(5,150,105,0.1); color:#059669;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg></div>
          <h4 style="font-size:16.5px; font-weight:800; margin-bottom:8px;">تاییدیه و نظارت جامعه پزشکی</h4>
          <p style="font-size:13px; color:var(--text-secondary); line-height:1.8;">تمام فرم‌های EMR، گایدلاین‌های نسخه و ماژول‌ها تحت نظارت مستقیم اساتید هیئت علمی دانشگاه طراحی شده است.</p>
        </div>

        <div class="panel-card">
          <div class="card-icon-wrap" style="background:rgba(217,119,6,0.1); color:#D97706;"><svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></div>
          <h4 style="font-size:16.5px; font-weight:800; margin-bottom:8px;">سرعت و سادگی بدون پیچیدگی</h4>
          <p style="font-size:13px; color:var(--text-secondary); line-height:1.8;">هیچ پزشکی نباید دوره‌های آموزشی طولانی ببیند؛ کار با نرم‌افزار پزشکآن ظرف ۳۰ دقیقه برای هر پزشک و منشی کاملاً شهودی است.</p>
        </div>
      </div>
    </div>
  </section>
'''

with open(os.path.join(PORTAL_DIR, "about.html"), "w", encoding="utf-8") as f:
    f.write(wrap_page("درباره اکوسیستم پزشکآن", about_content, "about"))

print("Generated: portal/about.html")

# ==============================================================================
# 8. CONTACT US PAGE (portal/contact.html)
# ==============================================================================
contact_content = '''
  <section style="padding:48px 0 56px;">
    <div class="container">
      <div class="section-title-wrap">
        <span class="section-pill-tag">ارتباط مستقیم و پشتیبانی ۲۴ ساعته</span>
        <h1 class="section-h2" style="font-size:32px;">همواره در کنار جامعه پزشکی و سلامت کشور هستیم</h1>
        <p class="section-sub">پاسخگویی شبانه‌روزی ویژه پزشکان و هماهنگی استقرار حضوری کارشناس در مطب</p>
      </div>

      <div class="grid-2" style="gap:36px; align-items:start;">
        <!-- Contact Form -->
        <div class="panel-card" style="padding:36px;">
          <h3 style="font-size:18px; font-weight:800; color:var(--text-pure); margin-bottom:16px;">ارسال پیام مستقیم به واحد پشتیبانی و فروش</h3>
          
          <form onsubmit="handleContactSubmit(event)">
            <div style="margin-bottom:14px;">
              <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:6px;">نام و نام خانوادگی:</label>
              <input type="text" id="cName" class="form-control" placeholder="دکتر ..." style="width:100%; padding:10px 14px; border:1px solid var(--glass-border); border-radius:var(--radius-sm); font-family:var(--font-family);" required>
            </div>
            
            <div style="margin-bottom:14px;">
              <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:6px;">شماره همراه:</label>
              <input type="tel" id="cPhone" class="form-control" placeholder="۰۹۱۲..." style="width:100%; padding:10px 14px; border:1px solid var(--glass-border); border-radius:var(--radius-sm); font-family:var(--font-family);" dir="ltr" required>
            </div>

            <div style="margin-bottom:14px;">
              <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:6px;">موضوع پیام:</label>
              <select id="cSubject" style="width:100%; padding:10px 14px; border:1px solid var(--glass-border); border-radius:var(--radius-sm); font-family:var(--font-family); background:var(--bg-surface-primary); color:var(--text-main);">
                <option value="دمو حضوری در مطب">درخواست دمو و استقرار حضوری در مطب</option>
                <option value="مشاوره خرید پکیج">مشاوره خرید و مقایسه پکیج‌ها</option>
                <option value="همکاری در مجله سلامت">همکاری پزشک در هیئت تحریریه مجله سلامت</option>
                <option value="پشتیبانی فنی">پشتیبانی فنی سامانه مطب</option>
              </select>
            </div>

            <div style="margin-bottom:20px;">
              <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:6px;">متن پیام شما:</label>
              <textarea id="cMessage" style="width:100%; min-height:100px; padding:10px 14px; border:1px solid var(--glass-border); border-radius:var(--radius-sm); font-family:var(--font-family); line-height:1.7;" placeholder="پیام خود را بنویسید..."></textarea>
            </div>

            <button type="submit" class="btn btn-primary" style="width:100%; justify-content:center; padding:12px;">ارسال پیام به واحد پزشکان ↗</button>
          </form>
        </div>

        <!-- Info Column -->
        <div>
          <div class="panel-card" style="margin-bottom:20px;">
            <h4 style="font-size:16px; font-weight:800; color:var(--text-pure); margin-bottom:12px;">خطوط تماس شبانه‌روزی</h4>
            <div style="display:flex; flex-direction:column; gap:10px; font-size:14px;">
              <div style="display:flex; justify-content:space-between; border-bottom:1px solid var(--glass-border); padding-bottom:8px;">
                <span style="color:var(--text-muted);">پشتیبانی ویژه پزشکان (۲۴ ساعته):</span>
                <strong style="color:var(--brand-primary);" dir="ltr">۰۲۱-۸۸۸۸۴۴۴۴</strong>
              </div>
              <div style="display:flex; justify-content:space-between; border-bottom:1px solid var(--glass-border); padding-bottom:8px;">
                <span style="color:var(--text-muted);">واحد استقرار و دمو حضوری:</span>
                <strong style="color:var(--brand-emerald-vital);" dir="ltr">۰۲۱-۸۸۸۸۵۵۵۵</strong>
              </div>
              <div style="display:flex; justify-content:space-between;">
                <span style="color:var(--text-muted);">ایمیل ارتباط سازمانی:</span>
                <strong dir="ltr">info@pezeshkan.ir</strong>
              </div>
            </div>
          </div>

          <div class="panel-card">
            <h4 style="font-size:16px; font-weight:800; color:var(--text-pure); margin-bottom:8px;">دفتر مرکزی و نمایشگاه دائمی تجهیزات مطب</h4>
            <p style="color:var(--text-secondary); line-height:1.8; font-size:13.5px; margin-bottom:14px;">
              تهران، میدان ونک، خیابان ملاصدرا، پلاک ۷۲، برج فناوری سلامت پزشکآن، طبقه ۸.
            </p>
            <div style="background:var(--bg-canvas); border-radius:var(--radius-sm); padding:16px; text-align:center; color:var(--text-muted); font-size:12px;">
              امکان تست حضوری قلم‌های نوری و مانیتورینگ درمان در شوروم مرکزی با هماهنگی قبلی
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <script>
    async function handleContactSubmit(e) {
      e.preventDefault();
      const name = document.getElementById('cName').value.trim();
      const phone = document.getElementById('cPhone').value.trim();
      if (!name || !phone) return;
      try {
        await fetch('/api/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: name,
            phone: phone,
            subject: document.getElementById('cSubject').value,
            message: document.getElementById('cMessage').value,
            createdAt: new Date().toISOString()
          })
        });
      } catch(err) {}
      alert('پیام شما با موفقیت ثبت شد. کارشناسان ما به زودی با شما تماس خواهند گرفت.');
      window.location.href = '/';
    }
  </script>
'''

with open(os.path.join(PORTAL_DIR, "contact.html"), "w", encoding="utf-8") as f:
    f.write(wrap_page("تماس با ما و مرکز پشتیبانی", contact_content, "contact"))

print("Generated: portal/contact.html")

# ==============================================================================
# 9. CRM TUTORIALS & ACADEMY CONTENT (portal/tutorials.html)
# ==============================================================================
tutorials_content = '''
  <section class="page-hero">
    <div class="container" style="text-align:center;">
      <span class="section-pill-tag">آکادمی آموزش تخصصی پزشکآن</span>
      <h1 class="page-hero-title">مرکز جامع آموزش CRM و مدیریت یکپارچه مطب</h1>
      <p class="page-hero-subtitle" style="max-width:720px; margin:0 auto 28px; font-size:15px; color:var(--text-secondary); line-height:1.8;">
        پایگاه دانش بالینی و راهنمای جامع اتوماسیون مطب؛ تفکیک‌شده بر اساس ۳ محور تخصصی عملیاتی:
      </p>

      <!-- 3 Role Architecture Hero Cards -->
      <div class="grid-3" style="max-width:960px; margin:0 auto 28px; gap:16px; text-align:right;">
        <div class="hero-role-chip" onclick="filterTutorials('doctor', 'doctor', true)" style="background:var(--bg-surface-primary); border:1px solid var(--glass-border); padding:16px 18px; border-radius:var(--radius-md); box-shadow:var(--shadow-elevation); cursor:pointer; display:flex; align-items:center; gap:14px;">
          <div style="width:44px; height:44px; border-radius:12px; background:rgba(0,115,255,0.1); color:var(--brand-primary); display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg class="svg-icon" style="width:22px; height:22px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
          </div>
          <div style="flex-grow:1;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3px;">
              <span style="font-weight:900; font-size:14.5px; color:var(--text-pure);">ویژه پزشک و درمان</span>
              <span style="font-size:11px; color:var(--brand-primary); font-weight:700;">۲ راهنما</span>
            </div>
            <div style="font-size:12px; color:var(--text-muted); line-height:1.5;">قلم نوری، چارت آناتومی و دستیار نسخه AI</div>
          </div>
        </div>

        <div class="hero-role-chip" onclick="filterTutorials('receptionist', 'receptionist', true)" style="background:var(--bg-surface-primary); border:1px solid var(--glass-border); padding:16px 18px; border-radius:var(--radius-md); box-shadow:var(--shadow-elevation); cursor:pointer; display:flex; align-items:center; gap:14px;">
          <div style="width:44px; height:44px; border-radius:12px; background:rgba(5,150,105,0.1); color:var(--brand-emerald-vital); display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg class="svg-icon" style="width:22px; height:22px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 11l-3-3m0 0l-3 3m3-3v8"/></svg>
          </div>
          <div style="flex-grow:1;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3px;">
              <span style="font-weight:900; font-size:14.5px; color:var(--text-pure);">ویژه منشی و پذیرش</span>
              <span style="font-size:11px; color:var(--brand-emerald-vital); font-weight:700;">۲ راهنما</span>
            </div>
            <div style="font-size:12px; color:var(--text-muted); line-height:1.5;">اتصال کارتخوان (POS)، نوبت‌دهی و انبارداری</div>
          </div>
        </div>

        <div class="hero-role-chip" onclick="filterTutorials('user', 'user', true)" style="background:var(--bg-surface-primary); border:1px solid var(--glass-border); padding:16px 18px; border-radius:var(--radius-md); box-shadow:var(--shadow-elevation); cursor:pointer; display:flex; align-items:center; gap:14px;">
          <div style="width:44px; height:44px; border-radius:12px; background:rgba(217,119,6,0.1); color:#D97706; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg class="svg-icon" style="width:22px; height:22px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
          <div style="flex-grow:1;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3px;">
              <span style="font-weight:900; font-size:14.5px; color:var(--text-pure);">ویژه مراجعین و مدیریت</span>
              <span style="font-size:11px; color:#D97706; font-weight:700;">۲ راهنما</span>
            </div>
            <div style="font-size:12px; color:var(--text-muted); line-height:1.5;">پرونده ۳۶۰ درجه، پرتال سلامت و تراز مالیاتی</div>
          </div>
        </div>
      </div>

      <div style="display:flex; justify-content:center; gap:16px; flex-wrap:wrap;">
        <span style="background:rgba(0,115,255,0.08); border:1px solid rgba(0,115,255,0.25); color:var(--brand-primary); padding:8px 16px; border-radius:var(--radius-full); font-size:13px; font-weight:700; display:inline-flex; align-items:center; gap:8px;">
          <svg class="svg-icon" style="width:16px; height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          <span>۶ مقاله تخصصی و راهنمای عملیاتی</span>
        </span>
        <span style="background:rgba(5,150,105,0.08); border:1px solid rgba(5,150,105,0.25); color:var(--brand-emerald-vital); padding:8px 16px; border-radius:var(--radius-full); font-size:13px; font-weight:700; display:inline-flex; align-items:center; gap:8px;">
          <svg class="svg-icon" style="width:16px; height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span>استقرار صفر تا صد زیر ۴۸ ساعت</span>
        </span>
        <span style="background:rgba(217,119,6,0.08); border:1px solid rgba(217,119,6,0.25); color:#D97706; padding:8px 16px; border-radius:var(--radius-full); font-size:13px; font-weight:700; display:inline-flex; align-items:center; gap:8px;">
          <svg class="svg-icon" style="width:16px; height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>منطبق با استانداردهای سپاس و سازمان نظام پزشکی</span>
        </span>
      </div>
    </div>
  </section>

  <!-- Interactive Search & Role-Based Filtering Bar -->
  <section style="padding: 20px 0 10px;">
    <div class="container">
      <div class="tutorial-search-box">
        <svg class="svg-icon" style="position:absolute; right:16px; top:14px; color:var(--text-muted); width:18px; height:18px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" id="tutorialSearchInput" class="tutorial-search-input" placeholder="جستجو در مقالات: نوبت‌دهی، قلم نوری، پوز، دستیار AI، حسابداری..." oninput="handleTutorialSearch()">
      </div>

      <div class="tutorial-filter-bar">
        <button type="button" class="tutorial-filter-btn active" data-filter="all" onclick="filterTutorials('all', this)">
          <svg class="svg-icon" style="width:15px; height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          <span>همه آموزش‌ها</span>
        </button>
        <button type="button" class="tutorial-filter-btn" data-filter="doctor" onclick="filterTutorials('doctor', this)">
          <svg class="svg-icon" style="width:15px; height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
          <span>برای پزشک</span>
        </button>
        <button type="button" class="tutorial-filter-btn" data-filter="receptionist" onclick="filterTutorials('receptionist', this)">
          <svg class="svg-icon" style="width:15px; height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 11l-3-3m0 0l-3 3m3-3v8"/></svg>
          <span>برای منشی</span>
        </button>
        <button type="button" class="tutorial-filter-btn" data-filter="user" onclick="filterTutorials('user', this)">
          <svg class="svg-icon" style="width:15px; height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          <span>برای کاربر</span>
        </button>
      </div>
    </div>
  </section>

  <!-- Featured Masterclass Roadmap Card (Crystal-Clear in Day & Dark Modes) -->
  <section style="padding: 10px 0 30px;">
    <div class="container">
      <div class="panel-card" style="border: 2px solid rgba(0, 115, 255, 0.25); background: var(--bg-surface-primary); box-shadow: var(--shadow-elevation);">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px; margin-bottom:24px;">
          <div>
            <div style="display:inline-flex; align-items:center; gap:8px; margin-bottom:8px;">
              <span class="tutorial-badge">راهنمای مرجع مستقر‌سازی</span>
              <span style="font-size:12px; color:var(--brand-primary); font-weight:700;">نسخه استاندارد بالینی ۱۴۰۴</span>
            </div>
            <h2 style="font-size:22px; font-weight:900; color:var(--text-pure); margin:6px 0 8px;">نقشه راه ۴ گام راه‌اندازی اتوماسیون هوشمند مطب و CRM پزشکآن</h2>
            <p style="color:var(--text-secondary); font-size:14px; max-width:700px; margin:0; line-height:1.75;">
              برای رسیدن به بیشترین بازدهی بالینی و صرفه‌جویی ۳ دقیقه‌ای در هر ویزیت، توصیه می‌کنیم مراحل استقرار را بر اساس این نقشه راه پیاده‌سازی فرمایید.
            </p>
          </div>
          <a href="/start" class="btn btn-primary" style="padding:10px 20px; font-size:13px; display:inline-flex; align-items:center; gap:8px;">
            <span>شروع پیکربندی مطب شما</span>
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
          </a>
        </div>

        <div class="grid-4" style="gap:16px;">
          <div style="background:var(--bg-surface-secondary); padding:18px 16px; border-radius:var(--radius-md); border:1px solid var(--glass-border); transition:all 0.25s ease;">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
              <span style="color:var(--brand-primary); font-weight:900; font-size:15px;">گام اول</span>
              <svg class="svg-icon" style="width:20px; height:20px; color:var(--brand-primary);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            </div>
            <h4 style="font-size:14.5px; font-weight:800; color:var(--text-pure); margin-bottom:8px;">تعریف پرسنل و سطوح دسترسی</h4>
            <p style="color:var(--text-muted); font-size:12.5px; line-height:1.75; margin:0;">ایجاد حساب کاربری مجزا برای پزشک، منشی و دستیار با تفکیک کامل دسترسی پرونده‌های مالی و محرمانه.</p>
          </div>

          <div style="background:var(--bg-surface-secondary); padding:18px 16px; border-radius:var(--radius-md); border:1px solid var(--glass-border); transition:all 0.25s ease;">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
              <span style="color:var(--brand-emerald-vital); font-weight:900; font-size:15px;">گام دوم</span>
              <svg class="svg-icon" style="width:20px; height:20px; color:var(--brand-emerald-vital);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>
            </div>
            <h4 style="font-size:14.5px; font-weight:800; color:var(--text-pure); margin-bottom:8px;">اتصال پوز بانکی و سامانه پیامک</h4>
            <p style="color:var(--text-muted); font-size:12.5px; line-height:1.75; margin:0;">همگام‌سازی کارتخوان از طریق پورت LAN یا USB با نرم‌افزار جهت انتقال خودکار ارقام و پیامک تایید نوبت.</p>
          </div>

          <div style="background:var(--bg-surface-secondary); padding:18px 16px; border-radius:var(--radius-md); border:1px solid var(--glass-border); transition:all 0.25s ease;">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
              <span style="color:var(--brand-primary-light); font-weight:900; font-size:15px;">گام سوم</span>
              <svg class="svg-icon" style="width:20px; height:20px; color:var(--brand-primary-light);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="M2 2l7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg>
            </div>
            <h4 style="font-size:14.5px; font-weight:800; color:var(--text-pure); margin-bottom:8px;">کالیبراسیون قلم نوری و چارت</h4>
            <p style="color:var(--text-muted); font-size:12.5px; line-height:1.75; margin:0;">شخصی‌سازی شابلون‌های شرح‌حال و بارگذاری چارت‌های اختصاصی تخصص پزشکی (ارتوپدی، پوست، قلب، دندان و...).</p>
          </div>

          <div style="background:var(--bg-surface-secondary); padding:18px 16px; border-radius:var(--radius-md); border:1px solid var(--glass-border); transition:all 0.25s ease;">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
              <span style="color:#D97706; font-weight:900; font-size:15px;">گام چهارم</span>
              <svg class="svg-icon" style="width:20px; height:20px; color:#D97706;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            </div>
            <h4 style="font-size:14.5px; font-weight:800; color:var(--text-pure); margin-bottom:8px;">فعال‌سازی دستیار AI و باشگاه CRM</h4>
            <p style="color:var(--text-muted); font-size:12.5px; line-height:1.75; margin:0;">روشن کردن رادار پایش تداخلات دارویی و سناریوهای پیگیری درمان مراجعین (Post-Op) جهت افزایش وفاداری.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 6 In-Depth Clinical CRM Tutorial Articles Categorized by Audience -->
  <section style="padding: 20px 0 60px;">
    <div class="container">
      <div class="grid-3" id="tutorialGrid" style="gap:24px;">

        <!-- Article 1: For Receptionist / Secretary -->
        <div class="panel-card tutorial-card" data-category="receptionist">
          <div class="card-meta">
            <span class="tutorial-badge">برای منشی • پایانه و نوبت‌دهی</span>
            <span style="display:inline-flex; align-items:center; gap:5px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span>۶ دقیقه مطالعه</span>
            </span>
          </div>
          <h3>اتصال هوشمند دستگاه کارتخوان (POS) به نرم‌افزار نوبت‌دهی و پیشگیری از خطای انسانی منشی</h3>
          <p>
            آموزش پروتکل اتصال پوزهای فناپ، به‌پرداخت، سداد و آسان‌پرداخت از طریق LAN و پورت سریال، انتقال خودکار ارقام ویزیت بدون ورود دستی مبلغ، و رفع کامل خطای مغایرت در پایان شیفت کاری مطب.
          </p>
          <div style="margin-top:auto; border-top:1px solid var(--glass-border); padding-top:14px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:12px; color:var(--brand-emerald-vital); font-weight:700; display:inline-flex; align-items:center; gap:6px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <span>مخاطب: کادر پذیرش و منشی مطب</span>
            </span>
            <button type="button" class="btn btn-outline" style="padding:6px 14px; font-size:12.5px; display:inline-flex; align-items:center; gap:6px;" onclick="openArticleModal('art-1')">
              <span>مطالعه کامل</span>
              <svg class="svg-icon" style="width:13px; height:13px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </button>
          </div>
        </div>

        <!-- Article 2: For User / Patients & Clinic Management -->
        <div class="panel-card tutorial-card" data-category="user">
          <div class="card-meta">
            <span class="tutorial-badge">برای کاربر • پرتال مراجعین و وفاداری</span>
            <span style="display:inline-flex; align-items:center; gap:5px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span>۸ دقیقه مطالعه</span>
            </span>
          </div>
          <h3>اصول CRM پزشکی: ایجاد پرونده ۳۶۰ درجه بیمار، پرتال سلامت مراجعین و باشگاه وفاداری</h3>
          <p>
            چگونه با پرونده ۳۶۰ درجه، ثبت منظم سوابق مراجعات، پیامک‌های هوشمند مراقبت پس از درمان (Post-op Follow-up) و یادآوری دوره‌ای چکاپ‌ها، نرخ بازگشت مراجعین و وفاداری کلینیک را تا ۵۰٪ ارتقا دهیم.
          </p>
          <div style="margin-top:auto; border-top:1px solid var(--glass-border); padding-top:14px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:12px; color:var(--brand-primary); font-weight:700; display:inline-flex; align-items:center; gap:6px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <span>مخاطب: مراجعین و مدیران کلینیک</span>
            </span>
            <button type="button" class="btn btn-outline" style="padding:6px 14px; font-size:12.5px; display:inline-flex; align-items:center; gap:6px;" onclick="openArticleModal('art-2')">
              <span>مطالعه کامل</span>
              <svg class="svg-icon" style="width:13px; height:13px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </button>
          </div>
        </div>

        <!-- Article 3: For Doctor -->
        <div class="panel-card tutorial-card" data-category="doctor">
          <div class="card-meta">
            <span class="tutorial-badge">برای پزشک • قلم نوری و ویزیت</span>
            <span style="display:inline-flex; align-items:center; gap:5px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span>۷ دقیقه مطالعه</span>
            </span>
          </div>
          <h3>راهنمای جامع کار با قلم نوری و چارت دیجیتال آناتومی در ویزیت بالینی بدون کیبورد</h3>
          <p>
            تکنیک‌های یادداشت‌برداری سریع روی چارت‌های تخصصی، ترسیم تغییرات پاتولوژیک روی تصاویر رادیولوژی و سونوگرافی، و نحوه تبدیل خودکار دست‌خط پزشک به داده‌های استاندارد با موتور OCR اختصاصی فارسی.
          </p>
          <div style="margin-top:auto; border-top:1px solid var(--glass-border); padding-top:14px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:12px; color:var(--brand-primary-light); font-weight:700; display:inline-flex; align-items:center; gap:6px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <span>مخاطب: پزشک متخصص و عمومی</span>
            </span>
            <button type="button" class="btn btn-outline" style="padding:6px 14px; font-size:12.5px; display:inline-flex; align-items:center; gap:6px;" onclick="openArticleModal('art-3')">
              <span>مطالعه کامل</span>
              <svg class="svg-icon" style="width:13px; height:13px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </button>
          </div>
        </div>

        <!-- Article 4: For Doctor -->
        <div class="panel-card tutorial-card" data-category="doctor">
          <div class="card-meta">
            <span class="tutorial-badge">برای پزشک • دستیار نسخه هوشمند</span>
            <span style="display:inline-flex; align-items:center; gap:5px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span>۹ دقیقه مطالعه</span>
            </span>
          </div>
          <h3>نحوه پیکربندی دستیار بالینی هوش مصنوعی (AI) و سیستم پایش تداخلات دارویی</h3>
          <p>
            راهنمای تنظیم آستانه هشدارهای تداخل دارویی Major/Severe، بررسی خودکار حساسیت‌های دارویی و آلرژی بیمار در هنگام تجویز نسخه، و محاسبه تطبیقی دوز متناسب با سن، وزن و شاخص عملکرد کلیوی (GFR).
          </p>
          <div style="margin-top:auto; border-top:1px solid var(--glass-border); padding-top:14px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:12px; color:var(--brand-rose-critical); font-weight:700; display:inline-flex; align-items:center; gap:6px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <span>مخاطب: پزشک معالج و تجویز نسخه</span>
            </span>
            <button type="button" class="btn btn-outline" style="padding:6px 14px; font-size:12.5px; display:inline-flex; align-items:center; gap:6px;" onclick="openArticleModal('art-4')">
              <span>مطالعه کامل</span>
              <svg class="svg-icon" style="width:13px; height:13px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </button>
          </div>
        </div>

        <!-- Article 5: For User / Patients & Finance -->
        <div class="panel-card tutorial-card" data-category="user">
          <div class="card-meta">
            <span class="tutorial-badge">برای کاربر • حسابداری و گزارش مالی</span>
            <span style="display:inline-flex; align-items:center; gap:5px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span>۱۰ دقیقه مطالعه</span>
            </span>
          </div>
          <h3>حسابداری شفاف مطب و کلینیک: گزارش‌گیری مالیاتی و محاسبه تسهیم درآمد پزشکان</h3>
          <p>
            آموزش فرمول‌نویسی سهم پزشکان مهمان و سهامداران، تسهیم درآمد خدمات پاراکلینیک، صدور خروجی استاندارد ماده ۱۶۹ مکرر برای سازمان امور مالیاتی و مدیریت دقیق کسورات و مطالبات بیمه‌های درمانی پایه و تکمیلی.
          </p>
          <div style="margin-top:auto; border-top:1px solid var(--glass-border); padding-top:14px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:12px; color:#D97706; font-weight:700; display:inline-flex; align-items:center; gap:6px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <span>مخاطب: مدیران کلینیک و کاربران مالی</span>
            </span>
            <button type="button" class="btn btn-outline" style="padding:6px 14px; font-size:12.5px; display:inline-flex; align-items:center; gap:6px;" onclick="openArticleModal('art-5')">
              <span>مطالعه کامل</span>
              <svg class="svg-icon" style="width:13px; height:13px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </button>
          </div>
        </div>

        <!-- Article 6: For Receptionist / Secretary -->
        <div class="panel-card tutorial-card" data-category="receptionist">
          <div class="card-meta">
            <span class="tutorial-badge">برای منشی • انبارداری و ثبت مواد</span>
            <span style="display:inline-flex; align-items:center; gap:5px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span>۶ دقیقه مطالعه</span>
            </span>
          </div>
          <h3>انبارداری هوشمند تجهیزات، بارکد اسکن و پیشگیری از زیان انقضای داروهای مطب</h3>
          <p>
            مدیریت موجودی ژل‌ها، بوتاکس، نخ‌های جراحی، ایمپلنت‌ها و داروهای تزریقی؛ اسکن بارکد اصالت کالا (UID/IRC)، هشدار خودکار نزدیک شدن به موعد انقضا و کسر مستقیم از انبار به ازای هر پرونده بالینی.
          </p>
          <div style="margin-top:auto; border-top:1px solid var(--glass-border); padding-top:14px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:12px; color:var(--brand-emerald-vital); font-weight:700; display:inline-flex; align-items:center; gap:6px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <span>مخاطب: منشی و دستیار مطب</span>
            </span>
            <button type="button" class="btn btn-outline" style="padding:6px 14px; font-size:12.5px; display:inline-flex; align-items:center; gap:6px;" onclick="openArticleModal('art-6')">
              <span>مطالعه کامل</span>
              <svg class="svg-icon" style="width:13px; height:13px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </button>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- Article Interactive Modal Reader -->
  <div id="articleModalBackdrop" class="article-modal-backdrop" onclick="handleModalBackdropClick(event)">
    <div class="article-modal-dialog">
      <div class="article-modal-header">
        <div style="display:flex; align-items:center; gap:12px;">
          <span id="modalCategoryBadge" class="tutorial-badge">آموزش CRM</span>
          <span id="modalReadTime" style="font-size:12.5px; color:var(--text-muted); display:inline-flex; align-items:center; gap:5px;">
            <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span id="modalReadTimeText">۶ دقیقه مطالعه</span>
          </span>
        </div>
        <button type="button" onclick="closeArticleModal()" style="background:none; border:none; color:var(--text-secondary); cursor:pointer; display:inline-flex; align-items:center; justify-content:center; width:32px; height:32px; border-radius:50%;" title="بستن">
          <svg class="svg-icon" style="width:18px; height:18px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <div class="article-modal-body" id="articleModalContent">
        <!-- Injected via JavaScript -->
      </div>

      <div style="padding:16px 24px; border-top:1px solid var(--glass-border); background:var(--bg-surface-secondary); display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:12.5px; color:var(--text-muted);">اکوسیستم سلامت دیجیتال پزشکآن • پایگاه دانش بالینی</span>
        <div style="display:flex; gap:10px;">
          <button type="button" class="btn btn-outline" style="padding:6px 14px; font-size:12.5px;" onclick="window.print()">چاپ راهنما</button>
          <button type="button" class="btn btn-primary" style="padding:6px 16px; font-size:12.5px;" onclick="closeArticleModal()">بستن پنجره</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Dedicated Support & Consultation CTA -->
  <section style="padding: 40px 0 80px;">
    <div class="container">
      <div class="panel-card" style="text-align:center; padding:44px 24px; border:2px solid rgba(0,115,255,0.3); background:radial-gradient(circle at 50% 50%, rgba(0,115,255,0.08) 0%, transparent 80%), var(--bg-surface-primary);">
        <span class="section-pill-tag">استقرار اختصاصی و آموزش پرسنل مطب</span>
        <h2 style="font-size:24px; font-weight:900; color:var(--text-pure); margin:12px 0 16px;">به راهنمایی حضوری یا آنلاین برای تیم پذیرش و کادر درمانی نیاز دارید؟</h2>
        <p style="color:var(--text-secondary); max-width:650px; margin:0 auto 28px; line-height:1.9;">
          کارشناسان بالینی و فنی پزشکآن به صورت رایگان در مطب یا کلینیک شما حاضر شده و تمام مراحل اتصال پوز، قلم‌های نوری و پرونده الکترونیک را برای پرسنل آموزش می‌دهند.
        </p>
        <div style="display:flex; justify-content:center; gap:14px; flex-wrap:wrap;">
          <a href="/start" class="btn btn-primary" style="padding:12px 28px;">
            <span>درخواست استقرار و آموزش رایگان</span>
            <svg class="svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
          </a>
          <a href="/contact" class="btn btn-outline" style="padding:12px 24px;">
            <span>تماس با واحد آموزش پزشکان</span>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Script for Search, Filter & Modal Engine -->
  <script>
    const checkIconSvg = '<svg class="svg-icon" style="width:14px; height:14px; color:var(--brand-emerald-vital); flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>';

    const tutorialArticles = {
      'art-1': {
        title: 'اتصال هوشمند دستگاه کارتخوان (POS) به نرم‌افزار نوبت‌دهی و پیشگیری از خطای انسانی منشی',
        category: 'برای منشی و پذیرش',
        readTime: '۶ دقیقه مطالعه • ویژه منشی و مدیر مطب',
        html: `
          <h4>مقدمه و ضرورت اتصال مستقیم کارتخوان به پرونده سلامت</h4>
          <p>
            یکی از رایج‌ترین گلوگاه‌های اتلاف وقت و کسری مالی در مطب‌های شلوغ، ورود دستی مبالغ ویزیت و خدمات توسط منشی است. اشتباه در یک صفر می‌تواند باعث زیان قابل توجه یا نارضایتی مراجعین شود. سامانه پزشکآن با اتصال مستقیم شبکه به پوزهای بانکی، امکان ارسال خودکار مبلغ نهایی خدمات و داروها را تنها با یک کلیک فراهم می‌سازد.
          </p>

          <div class="article-callout">
            <strong>نکته کلیدی امنیت مالی:</strong> با اتصال پروتکل پوز، تا زمانی که تراکنش موفق از سوی سوئیچ بانکی تایید نشده و شماره پیگیری (RRN) به پرونده سنجاق نشود، فاکتور مالی بیمار تسویه نشده باقی می‌ماند. این فرآیند از ثبت نوبت بدون پرداخت پیشگیری می‌کند.
          </div>

          <h4>مراحل سه‌گانه راه‌اندازی کارتخوان در نرم‌افزار پزشکآن</h4>
          <p>برای برقراری ارتباط بین کامپیوتر مطب و پوز، مراحل زیر را طی کنید:</p>

          <ul class="article-checklist">
            <li>
              <span>۱.</span>
              <div>
                <strong>انتخاب نحوه ارتباط فیزیکی:</strong>
                پوز را از طریق کابل شبکه LAN به سوئیچ مطب، یا از طریق کابل مبدل USB به پورت کیس متصل کنید. ارتباط از طریق شبکه پایدارترین گزینه در کلینیک‌های دارای چند سیستم است.
              </div>
            </li>
            <li>
              <span>۲.</span>
              <div>
                <strong>تنظیم آی‌پی استاتیک در تنظیمات کارتخوان:</strong>
                در منوی پیکربندی پوز، گزینه IP اختصاصی را فعال کرده و یک آدرس لوکال (مثلاً 192.168.1.150) به دستگاه تخصیص دهید.
              </div>
            </li>
            <li>
              <span>۳.</span>
              <div>
                <strong>ثبت پوز در پنل پذیرش پزشکآن:</strong>
                به بخش «تنظیمات سخت‌افزار مطب > مدیریت پایانه‌های فروش» بروید، نام شرکت ارائه‌دهنده پرداخت (PSP) را انتخاب کنید و IP دستگاه را ذخیره نمایید. دکمه «تست ارتباط» را بزنید؛ در صورت موفقیت، صفحه نمایش پوز بوق تایید می‌زند.
              </div>
            </li>
          </ul>

          <h4>سناریوی عملیاتی در زمان پذیرش بیمار</h4>
          <p>
            هنگامی که بیمار به میز پذیرش مراجعه می‌کند، منشی نوع خدمات (ویزیت، تزریقات، پانسمان، نوار قلب و...) را تیک می‌زند. نرم‌افزار به صورت خودکار سهم بیمه را کسر کرده و مبلغ خالص را روی صفحه پوز نمایش می‌دهد. بیمار کارت خود را کشیده و رمز را وارد می‌کند. بلافاصله فیش بیمار با بارکد نوبت صادر شده و پیامک خوش‌آمد و شماره نوبت به تلفن همراه بیمار ارسال می‌گردد.
          </p>

          <h4>مغایرت‌گیری انتهای شیفت در ۵ ثانیه</h4>
          <p>
            در پایان روز کاری، منشی نیازی به جمع زدن فیش‌های کاغذی ندارد. با کلیک بر روی دکمه «بستن شیفت و مغایرت‌گیری»، سیستم پزشکآن گزارش تراز بانکی را از سوئیچ استعلام کرده و با فهرست مراجعین مطابقت می‌دهد. در صورت وجود هرگونه تفاوت، دقیقاً مشخص می‌شود کدام نوبت لغو یا مرجوع شده است.
          </p>
        `
      },
      'art-2': {
        title: 'اصول CRM پزشکی: ایجاد پرونده ۳۶۰ درجه بیمار، پرتال سلامت مراجعین و باشگاه وفاداری',
        category: 'برای کاربر و مراجعین',
        readTime: '۸ دقیقه مطالعه • ویژه پزشک و مدیریت کلینیک',
        html: `
          <h4>مفهوم CRM در مراکز درمانی و تفاوت آن با بازرگانی</h4>
          <p>
            سیستم مدیریت ارتباط با مشتری (CRM) در محیط پزشکی به معنای ایجاد رابطه مستمر، مبتنی بر اعتماد و همدلی با مراجعین است. بیمار در پزشکی به دنبال درمان قطعی، پیگیری دلسوزانه و حفظ حریم شخصی خود است. CRM هوشمند پزشکآن این رابطه را بدون ایجاد زحمت اضافه برای کادر درمان اتوماسیون می‌کند.
          </p>

          <div class="article-callout">
            <strong>آمار مستند:</strong> کلینیک‌هایی که از پروتکل پیگیری خودکار (Follow-up) پس از ویزیت استفاده می‌کنند، با کاهش ۶۵ درصدی عدم مراجعه مجدد (No-Show) و افزایش ۴۰ درصدی رضایت مراجعین مواجه شده‌اند.
          </div>

          <h4>ارکان پرونده ۳۶۰ درجه سلامت مراجعین</h4>
          <p>پرونده ۳۶۰ درجه در پزشکآن شامل اطلاعات جامعی است که در هر مراجعه پیش روی پزشک قرار می‌گیرد:</p>

          <ul class="article-checklist">
            <li>
              <span><svg class="svg-icon" style="width:14px; height:14px; color:var(--brand-emerald-vital);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></span>
              <div>
                <strong>تایم‌لاین تعاملات بالینی:</strong>
                تمام ویزیت‌ها، تغییرات علائم حیاتی، سیر تغییر قند خون یا فشار خون، و یادداشت‌های دست‌نویس پزشک روی یک خط زمانی گرافیکی.
              </div>
            </li>
            <li>
              <span><svg class="svg-icon" style="width:14px; height:14px; color:var(--brand-emerald-vital);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></span>
              <div>
                <strong>ترجیحات شخصی و کانال‌های ارتباطی:</strong>
                ساعات مورد علاقه بیمار برای ویزیت، میزان رضایت از نوبت قبلی، و کانال ترجیحی پیامک یا تماس تلفنی.
              </div>
            </li>
            <li>
              <span><svg class="svg-icon" style="width:14px; height:14px; color:var(--brand-emerald-vital);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></span>
              <div>
                <strong>شبکه خانوادگی بیمار:</strong>
                امکان اتصال پرونده فرزندان، والدین یا همسر جهت بررسی سوابق بیماری‌های ارثی و خانوادگی در یک نگاه.
              </div>
            </li>
          </ul>

          <h4>سناریوهای اتوماسیون پیامکی پس از درمان (Post-Op Care)</h4>
          <p>
            پس از پایان ویزیت، پزشک یا منشی نیازی به یادآوری دستی ندارند. بر اساس نوع خدمت ثبت‌شده در پرونده، سناریوهای زیر به صورت کاملاً خودکار اجرا می‌شوند:
          </p>
          <p>
            • <strong>۲۴ ساعت بعد از جراحی سرپایی:</strong> پیامک احوالپرسی حاوی توصیه‌های مراقبت از پانسمان و شماره خط اضطراری مطب.<br>
            • <strong>۴۸ ساعت بعد:</strong> ارسال فرم تک‌سوالی رضایت‌سنجی (NPS) برای پایش میزان درد و علائم احتمالی تب یا تورم.<br>
            • <strong>یک هفته قبل از موعد چکاپ دوره‌ای:</strong> پیامک یادآوری هوشمند با لینک رزرو آنلاین نوبت اختصاصی بدون معطلی.<br>
            • <strong>روز تولد بیمار:</strong> تبریک اختصاصی با نام بیمار و پیشنهاد ویزیت غربالگری سلامت خانواده.
          </p>

          <h4>صیانت از حریم خصوصی بیمار در CRM</h4>
          <p>
            تمامی تعاملات و پیامک‌ها مطابق با قانون حفاظت از داده‌های سلامت ارسال می‌شوند. هیچ‌گونه اطلاعات حساس بیماری (نظیر تشخیص‌های پاتولوژی خاص) در متن پیامک عمومی قرار نمی‌گیرد و بیمار از طریق لینک امن رمزدار و احراز هویت با کد یکبارمصرف به نتایج دسترسی خواهد داشت.
          </p>
        `
      },
      'art-3': {
        title: 'راهنمای جامع کار با قلم نوری و چارت دیجیتال آناتومی در ویزیت بالینی بدون کیبورد',
        category: 'برای پزشک',
        readTime: '۷ دقیقه مطالعه • ویژه پزشک متخصص و عمومی',
        html: `
          <h4>چرا کیبورد مانع ارتباط چشمی پزشک و بیمار است؟</h4>
          <p>
            تحقیقات بالینی نشان داده‌اند که تایپ کردن شرح‌حال با کیبورد در اتاق ویزیت، باعث انقطاع ارتباط چشمی پزشک با مراجع شده و حس بی‌توجهی را در بیمار القا می‌کند. قلم نوری با شبیه‌سازی کامل حس کاغذ و خودکار، به پزشک اجازه می‌دهد همزمان با گفتگو، علائم را ترسیم و یادداشت‌برداری کند.
          </p>

          <div class="article-callout">
            <strong>موتور OCR هوشمند فارسی:</strong> نرم‌افزار پزشکآن مجهز به هوش مصنوعی تشخیص دست‌خط پزشکان ایرانی است. دست‌نویس شما در لحظه آنالیز شده و علاوه بر نگهداری شکل دست‌خط اصلی، به متن تایپی قابل جستجو تبدیل می‌شود.
          </div>

          <h4>تنظیمات و کالیبراسیون قلم نوری برای مطب</h4>
          <ul class="article-checklist">
            <li>
              <span>۱.</span>
              <div>
                <strong>نصب درایور قلم و حساسیت به فشار (Pressure Sensitivity):</strong>
                قلم‌های نوری پزشکی (نظیر Wacom و Huion) دارای ۸۱۹۲ سطح حساسیت به فشار هستند. در پنل تنظیمات قلم پزشکآن، حالت «نوشتار روان پزشکی» را انتخاب کنید تا لرزش دست به صورت خودکار فیلتر شود.
              </div>
            </li>
            <li>
              <span>۲.</span>
              <div>
                <strong>شخصی‌سازی دکمه‌های میانبر قلم:</strong>
                دکمه پایینی قلم را روی «پاک‌کن فوری» و دکمه بالایی را روی «حرکت بین صفحات چارت» تنظیم نمایید تا نیازی به لمس موس نداشته باشید.
              </div>
            </li>
            <li>
              <span>۳.</span>
              <div>
                <strong>استفاده از چارت‌های سه‌بعدی و دوبعدی آناتومی:</strong>
                به تناسب تخصص خود، چارت اسکلتی، عضلانی، دندانپزشکی، پوستی یا قلبی را فراخوانی کرده و دقیقاً موضع درد یا تزریق را علامت‌گذاری کنید.
              </div>
            </li>
          </ul>

          <h4>نشانه‌گذاری مستقیم روی تصاویر پاراکلینیک</h4>
          <p>
            با باز کردن تصویر رادیولوژی، سونوگرافی یا عکس رنگی بیمار در محیط پزشکآن، می‌توانید با قلم رنگی (قرمز، زرد، فیروزه‌ای) ضایعه یا شکستگی را علامت زده، اندازه ضایعه را با ابزار خط‌کش کالیبره‌شده مشخص کنید و این تصویر نشانه‌گذاری‌شده را به عنوان مستند ضمیمه پرونده ابری فرمایید.
          </p>
        `
      },
      'art-4': {
        title: 'نحوه پیکربندی دستیار بالینی هوش مصنوعی (AI) و سیستم پایش تداخلات دارویی',
        category: 'برای پزشک',
        readTime: '۹ دقیقه مطالعه • ویژه پزشک معالج و نسخه الکترونیک',
        html: `
          <h4>فلسفه دستیار هوش مصنوعی: دستیار مکمل پزشک، نه تصمیم‌گیرنده</h4>
          <p>
            دستیار هوش مصنوعی پزشکآن به عنوان یک لایه حفاظتی بی‌صدا عمل می‌کند. این سیستم همزمان با نوشتن نسخه یا انتخاب داروها، کاتالوگ دارونامه رسمی ایران و مراجع بین‌المللی (UpToDate و Lexicomp) را در کسری از ثانیه اسکن می‌کند تا در صورت وجود هرگونه تداخل مرگبار یا حساسیت بیمار، قبل از تایید نهایی هشدار دهد.
          </p>

          <div class="article-callout">
            <strong>دسته‌بندی شدت هشدارها:</strong> هشدارهای تداخل به سه سطح «ماژور (قرمز - خطر ایست قلبی، خونریزی شدید یا کما)»، «متوسط (زرد - کاهش اثربخشی داروها)» و «خفیف (آبی - توصیه‌های زمانی مصرف)» تفکیک می‌شوند.
          </div>

          <h4>مراحل فعال‌سازی و شخصی‌سازی قوانین دستیار AI</h4>
          <ul class="article-checklist">
            <li>
              <span>•</span>
              <div>
                <strong>تنظیم حساسیت آلرت‌ها:</strong>
                در منوی «تنظیمات بالینی > دستیار هوشمند نسخه»، می‌توانید انتخاب کنید که فقط تداخلات Major نمایش داده شوند تا از خستگی ناشی از هشدارهای مکرر (Alert Fatigue) جلوگیری شود.
              </div>
            </li>
            <li>
              <span>•</span>
              <div>
                <strong>پایش عملکرد کلیه و کبد بر اساس سن و آزمایش:</strong>
                سیستم با خواندن آخرین تست کراتینین بیمار، نرخ فیلتراسیون گلومرولی (eGFR) را به صورت خودکار محاسبه کرده و در صورت نیاز به تعدیل دوز داروهایی مانند متفورمین یا آنتی‌بیوتیک‌ها، دوز پیشنهادی را پیشنهاد می‌کند.
              </div>
            </li>
            <li>
              <span>•</span>
              <div>
                <strong>پیشنهاد جایگزین‌های ژنریک در زمان کمبود دارو:</strong>
                در صورتی که دارویی در بازار نایاب باشد، دستیار بالینی ژنریک‌های هم‌گروه با دوز درمانی مشابه را به پزشک پیشنهاد می‌دهد.
              </div>
            </li>
          </ul>

          <h4>پروتکل مستندسازی و رد هشدار (Override)</h4>
          <p>
            پزشک همواره تصمیم‌گیرنده نهایی است. در صورتی که منافع بالینی تجویز دو داروی متداخل از خطرات آن بیشتر باشد، پزشک می‌تواند با زدن دکمه «تایید با آگاهی از تداخل» و درج یک یادداشت بالینی کوتاه، نسخه را صادر کند. این یادداشت در گزارش‌های قانونی ثبت شده و نشان‌دهنده اشراف علمی پزشک بر کیس درمانی است.
          </p>
        `
      },
      'art-5': {
        title: 'حسابداری شفاف مطب و کلینیک: گزارش‌گیری مالیاتی و محاسبه تسهیم درآمد پزشکان',
        category: 'برای کاربر و مراجعین',
        readTime: '۱۰ دقیقه مطالعه • ویژه مدیریت و کاربران مالی',
        html: `
          <h4>چالش‌های محاسبات مالی در مطب‌های چندپزشکه و کلینیک‌ها</h4>
          <p>
            تسهیم سهم پزشکان بر اساس K خدمات، کسر استهلاک دستگاه‌ها و مواد مصرفی، محاسبه سهم درمانگاه و تعیین تکلیف کسورات بیمه، محاسبات پایان ماه را به فرآیندی زمان‌بر و مستعد اختلاف تبدیل می‌کند. ماژول مالی پزشکآن این فرآیند را به صورت خودکار و شفاف حل می‌کند.
          </p>

          <div class="article-callout">
            <strong>سازگاری با سامانه مودیان و ماده ۱۶۹ مکرر:</strong> خروجی مالی پزشکآن منطبق با آخرین استانداردهای سازمان امور مالیاتی بوده و به صورت فایل اکسل یا اکسس با کدینگ رسمی جهت بارگذاری در سامانه مودیان صادر می‌شود.
          </div>

          <h4>روش گام‌به‌گام تعریف فرمول‌های تسهیم</h4>
          <ul class="article-checklist">
            <li>
              <span>۱.</span>
              <div>
                <strong>تعریف درصد و حق‌العمل پزشک:</strong>
                تعیین درصد سهم پزشک از ویزیت، جراحی‌های سرپایی و خدمات تشخیصی (مثلاً ۷۰٪ پزشک، ۳۰٪ کلینیک).
              </div>
            </li>
            <li>
              <span>۲.</span>
              <div>
                <strong>کسر خودکار هزینه تجهیزات مصرفی:</strong>
                اگر در یک پروسه از ژل، کیت مصرفی یا داروی خاصی استفاده شده باشد، بهای تمام‌شده ماده مصرفی قبل از تسهیم کسر شده یا مستقیماً به حساب انبار منتقل می‌شود.
              </div>
            </li>
            <li>
              <span>۳.</span>
              <div>
                <strong>مدیریت پیش‌پرداخت و بیمه‌های تکمیلی:</strong>
                ثبت پیش‌پرداخت‌های مراجعین برای خدمات بلندمدت (نظیر ارتودنسی یا کاشت مو) و تسویه مرحله‌ای همگام با پیشرفت درمان.
              </div>
            </li>
          </ul>

          <h4>گزارش‌های مدیریتی سودآوری خدمات</h4>
          <p>
            علاوه بر ترازنامه ریالی، مدیر مطب می‌تواند گزارش نموداری خدمات را مشاهده کند: پردرآمدترین ساعت‌های مطب کدامند؟ کدام خدمات بیشترین حاشیه سود را ایجاد کرده‌اند؟ و نرخ بازگشت سرمایه تجهیزات خریداری‌شده چه مقدار بوده است؟
          </p>
        `
      },
      'art-6': {
        title: 'انبارداری هوشمند تجهیزات، بارکد اسکن و پیشگیری از زیان انقضای داروهای مطب',
        category: 'برای منشی و پذیرش',
        readTime: '۶ دقیقه مطالعه • ویژه منشی و کادر پذیرش',
        html: `
          <h4>پیشگیری از خسارت‌های سنگین ناشی از ابطال تاریخ انقضا</h4>
          <p>
            در کلینیک‌های پوست، مو، جراحی سرپایی و دندانپزشکی، نگهداری داروهای بیهوشی، فیلرها، بوتاکس، گرافت‌های استخوانی و کیت‌های آزمایشگاهی سرمایه قابل توجهی را به خود اختصاص می‌دهد. منقضی شدن حتی یک جعبه فیلر یا بوتاکس می‌تواند سود چندین ویزیت را از بین ببرد.
          </p>

          <div class="article-callout">
            <strong>پایش هوشمند زنجیره سرما (Cold Chain):</strong> پزشکآن علاوه بر پایش تاریخ انقضا، قابلیت ثبت شماره سریال برچسب اصالت کالو (IRC) و پایش تاریخ انقضا را بر اساس استاندارد سازمان غذا و دارو دارد.
          </div>

          <h4>فرآیند عملیاتی انبارداری در مطب</h4>
          <ul class="article-checklist">
            <li>
              <span>•</span>
              <div>
                <strong>اسکن سریع در لحظه ورود کالا:</strong>
                به محض رسیدن فاکتور خرید، منشی یا دستیار بارکد محصول را با بارکدخوان اسکن می‌کند. بچ‌نامبر و تاریخ انقضا به صورت اتوماتیک در سیستم ثبت می‌شوند.
              </div>
            </li>
            <li>
              <span>•</span>
              <div>
                <strong>قانون خروج کالا به ترتیب انقضا (FEFO - First Expired, First Out):</strong>
                هنگامی که پزشک در حال ثبت تزریق یا استفاده از محصول است، سیستم هوشمند بسته‌ای را پیشنهاد می‌کند که تاریخ انقضای نزدیک‌تری دارد تا موجودی قدیمی‌تر ابتدا مصرف شود.
              </div>
            </li>
            <li>
              <span>•</span>
              <div>
                <strong>هشدار نقطه سفارش مجدد (Reorder Point):</strong>
                به محض کاهش موجودی به حداقل آستانه بحرانی، هشداری زرد رنگ روی صفحه منشی ظاهر شده و فهرست اقلام مورد نیاز برای خرید مجدد تهیه می‌گردد.
              </div>
            </li>
          </ul>

          <h4>سنجاق کردن بارکد مواد مصرفی به پرونده قضایی و قانونی بیمار</h4>
          <p>
            یکی از مهم‌ترین الزامات بازرسی‌های پزشکی قانونی، امکان ردیابی شماره سریال بوتاکس، پروتز یا فیلر تزریق‌شده به بیمار است. با ثبت اتوماتیک در پرونده، در هر زمان می‌توان اثبات کرد چه کالایی با چه بچ‌نامبری و از چه شرکتی برای کدام بیمار مصرف شده است.
          </p>
        `
      }
    };

    function openArticleModal(artId) {
      const art = tutorialArticles[artId];
      if (!art) return;
      document.getElementById('modalCategoryBadge').innerText = art.category;
      document.getElementById('modalReadTimeText').innerText = art.readTime;
      document.getElementById('articleModalContent').innerHTML = 
        '<h2 style="font-size:20px; font-weight:900; color:var(--text-pure); margin-bottom:18px; line-height:1.5;">' + art.title + '</h2>' + art.html;
      const modal = document.getElementById('articleModalBackdrop');
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
      if (window.lenis) window.lenis.stop();
    }

    function closeArticleModal() {
      const modal = document.getElementById('articleModalBackdrop');
      modal.classList.remove('active');
      document.body.style.overflow = '';
      if (window.lenis) window.lenis.start();
    }

    function handleModalBackdropClick(e) {
      if (e.target.id === 'articleModalBackdrop') {
        closeArticleModal();
      }
    }

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        closeArticleModal();
      }
    });

    function filterTutorials(category, btn, doScroll = false) {
      let targetBtn = btn;
      if (typeof btn === 'string') {
        targetBtn = document.querySelector(`.tutorial-filter-btn[data-filter="${btn}"]`);
      }
      if (targetBtn) {
        document.querySelectorAll('.tutorial-filter-btn').forEach(b => b.classList.remove('active'));
        targetBtn.classList.add('active');
      }

      const cards = document.querySelectorAll('.tutorial-card');
      cards.forEach(card => {
        const cat = card.getAttribute('data-category');
        if (category === 'all' || cat === category) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });

      if (doScroll) {
        const target = document.getElementById('tutorialGrid');
        if (target) {
          if (window.lenis) {
            window.lenis.scrollTo(target, { offset: -90 });
          } else {
            target.scrollIntoView({ behavior: 'smooth' });
          }
        }
      }
    }

    function handleTutorialSearch() {
      const query = document.getElementById('tutorialSearchInput').value.trim().toLowerCase();
      const cards = document.querySelectorAll('.tutorial-card');
      cards.forEach(card => {
        const text = card.innerText.toLowerCase();
        if (!query || text.includes(query)) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }
  </script>
'''

with open(os.path.join(PORTAL_DIR, "tutorials.html"), "w", encoding="utf-8") as f:
    f.write(wrap_page("آموزش جامع CRM و مدیریت مطب", tutorials_content, "tutorials"))

print("Generated: portal/tutorials.html")
print("All 9 portal pages generated successfully!")

