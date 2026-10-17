# -*- coding: utf-8 -*-
"""
Assembles tutorials.html and portal/tutorials.html with full categorization
('آموزش برای پزشکان' and 'آموزش برای مراجعان') and dynamic video player slot.
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r'C:\Users\mahyar\.gemini\antigravity\brain\00b93e50-3b2a-442a-97b8-f82e39947546\.system_generated\logs\transcript_full.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    t_lines = f.readlines()

def get_tut_lines(start, end):
    for idx, l in enumerate(t_lines):
        if 'view_file' in l and 'tutorials.html' in l:
            obj = json.loads(l)
            tc = obj.get('tool_calls', [{}])[0]
            args = tc.get('args', {})
            if args.get('StartLine') == start and args.get('EndLine') == end:
                resp = json.loads(t_lines[idx+1])
                c = resp.get('content', '')
                res = []
                for cl in c.split('\n'):
                    if ': ' in cl:
                        num_part, text_part = cl.split(': ', 1)
                        if num_part.strip().isdigit():
                            res.append(text_part.rstrip('\r'))
                return res
    return []

# 1. Lines 1 to 120 (head, branding, desktop nav up to header-actions)
part1_lines = get_tut_lines(1, 120)

# 2. Missing lines 121 to 169 from portal/about.html (desktop dropdown for doctors)
with open('portal/about.html', 'r', encoding='utf-8') as f:
    about_lines = [l.rstrip('\r\n') for l in f.readlines()]
# In portal/about.html, lines 118 to 166 (0-indexed 117 to 165)
part2_lines = about_lines[117:166]

# 3. Lines 170 to 390 (mobile drawer, hero title & intro)
part3_lines_raw = get_tut_lines(170, 300) + get_tut_lines(300, 450)
# Find where the 3 hero role chips start (around line 390)
hero_chips_idx = -1
for i, line in enumerate(part3_lines_raw):
    if '<!-- 3 Role Architecture Hero Cards -->' in line or 'class="grid-3"' in line and 'hero-role-chip' in part3_lines_raw[i+1]:
        hero_chips_idx = i
        break

if hero_chips_idx == -1:
    # search for hero-role-chip
    for i, line in enumerate(part3_lines_raw):
        if 'hero-role-chip' in line:
            hero_chips_idx = i - 1
            break

part3_lines = part3_lines_raw[:hero_chips_idx]

# 4. Hero Section with 2 Categories
hero_section_html = """      <!-- 2 Category Architecture Hero Cards -->
      <div class="grid-2" style="max-width:880px; margin:0 auto 28px; gap:20px; text-align:right;">
        <div class="hero-role-chip" onclick="filterTutorials('doctors', this, true)" style="background:var(--bg-surface-primary); border:1px solid var(--glass-border); padding:20px 22px; border-radius:var(--radius-md); box-shadow:var(--shadow-elevation); cursor:pointer; display:flex; align-items:center; gap:16px; transition:all 0.25s ease;">
          <div style="width:50px; height:50px; border-radius:14px; background:rgba(0,115,255,0.12); color:var(--brand-primary); display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg class="svg-icon" style="width:26px; height:26px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
          </div>
          <div style="flex-grow:1;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
              <span style="font-weight:900; font-size:16px; color:var(--text-pure);">آموزش برای پزشکان</span>
              <span style="font-size:12px; color:var(--brand-primary); font-weight:800; background:rgba(0,115,255,0.08); padding:3px 10px; border-radius:12px;">۴ راهنما و ویدیو</span>
            </div>
            <div style="font-size:12.5px; color:var(--text-muted); line-height:1.6;">پروتکل اتصال کارتخوان (POS)، قلم نوری بالینی، دستیار AI و انبارداری</div>
          </div>
        </div>

        <div class="hero-role-chip" onclick="filterTutorials('patients', this, true)" style="background:var(--bg-surface-primary); border:1px solid var(--glass-border); padding:20px 22px; border-radius:var(--radius-md); box-shadow:var(--shadow-elevation); cursor:pointer; display:flex; align-items:center; gap:16px; transition:all 0.25s ease;">
          <div style="width:50px; height:50px; border-radius:14px; background:rgba(5,150,105,0.12); color:var(--brand-emerald-vital); display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg class="svg-icon" style="width:26px; height:26px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
          <div style="flex-grow:1;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
              <span style="font-weight:900; font-size:16px; color:var(--text-pure);">آموزش برای مراجعان</span>
              <span style="font-size:12px; color:var(--brand-emerald-vital); font-weight:800; background:rgba(5,150,105,0.08); padding:3px 10px; border-radius:12px;">۲ راهنما و ویدیو</span>
            </div>
            <div style="font-size:12.5px; color:var(--text-muted); line-height:1.6;">اصول CRM پزشکی، پرتال سلامت مراجعین، پرونده ۳۶۰ درجه و نوبت‌دهی</div>
          </div>
        </div>
      </div>

      <div style="display:flex; justify-content:center; gap:16px; flex-wrap:wrap;">
        <span style="background:rgba(0,115,255,0.08); border:1px solid rgba(0,115,255,0.25); color:var(--brand-primary); padding:8px 16px; border-radius:var(--radius-full); font-size:13px; font-weight:700; display:inline-flex; align-items:center; gap:8px;">
          <svg class="svg-icon" style="width:16px; height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          <span>۶ مقاله تخصصی و راهنمای عملیاتی</span>
        </span>
        <span style="background:rgba(5,150,105,0.08); border:1px solid rgba(5,150,105,0.25); color:var(--brand-emerald-vital); padding:8px 16px; border-radius:var(--radius-full); font-size:13px; font-weight:700; display:inline-flex; align-items:center; gap:8px;">
          <svg class="svg-icon" style="width:16px; height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>تاییدیه تیم پزشکی و امنیت PHI</span>
        </span>
        <span style="background:rgba(217,119,6,0.08); border:1px solid rgba(217,119,6,0.25); color:#D97706; padding:8px 16px; border-radius:var(--radius-full); font-size:13px; font-weight:700; display:inline-flex; align-items:center; gap:8px;">
          <svg class="svg-icon" style="width:16px; height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
          <span>بروزرسانی مستمر و پشتیبانی ۲۴/۷</span>
        </span>
      </div>
    </div>
  </section>

  <!-- Search & Categorized Filter Bar -->
  <section style="padding: 20px 0 10px;">
    <div class="container">
      <div class="tutorial-search-box">
        <svg class="svg-icon" style="position:absolute; right:16px; top:14px; color:var(--text-muted); width:18px; height:18px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" id="tutorialSearchInput" class="tutorial-search-input" placeholder="جستجو در مقالات: نوبت‌دهی، قلم نوری، پوز، دستیار AI، پرتال مراجعان..." oninput="handleTutorialSearch()">
      </div>

      <div class="tutorial-filter-bar">
        <button type="button" class="tutorial-filter-btn active" data-filter="all" onclick="filterTutorials('all', this)">
          <svg class="svg-icon" style="width:15px; height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          <span>همه آموزش‌ها (صفحه کلی)</span>
        </button>
        <button type="button" class="tutorial-filter-btn" data-filter="doctors" onclick="filterTutorials('doctors', this)">
          <svg class="svg-icon" style="width:15px; height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
          <span>آموزش برای پزشکان</span>
        </button>
        <button type="button" class="tutorial-filter-btn" data-filter="patients" onclick="filterTutorials('patients', this)">
          <svg class="svg-icon" style="width:15px; height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          <span>آموزش برای مراجعان</span>
        </button>
      </div>
    </div>
  </section>
"""

# 5. Roadmap Section (4 steps)
roadmap_html = """  <!-- 4-Step Interactive Deployment Roadmap -->
  <section style="padding: 10px 0 20px;">
    <div class="container">
      <div class="panel-card" style="padding: 24px; border: 1px solid var(--glass-border);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px; flex-wrap:wrap; gap:10px;">
          <div>
            <h3 style="font-size:17px; font-weight:900; color:var(--text-pure); margin-bottom:4px;">نقشه راه ۴ مرحله‌ای استقرار سامانه پزشکآن در مطب</h3>
            <p style="font-size:13px; color:var(--text-muted); margin:0;">مسیر گام‌به‌گام راه‌اندازی بدون اختلال در ویزیت بیماران و فرآیند پذیرش کلینیک</p>
          </div>
          <span style="font-size:12px; font-weight:800; color:var(--brand-primary); background:rgba(0,115,255,0.08); padding:6px 14px; border-radius:var(--radius-full); border:1px solid rgba(0,115,255,0.2);">زمان استقرار: کمتر از ۴۸ ساعت</span>
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
"""

# Load CRM tutorial data
with open('mag/content/crm_tutorials.json', 'r', encoding='utf-8') as f:
    crm_tutorials = json.load(f)

# 6. Grid Cards Section
grid_cards_html = """  <!-- 6 In-Depth Clinical CRM Tutorial Articles Categorized by Doctors vs Patients -->
  <section style="padding: 20px 0 60px;">
    <div class="container">
      <div class="grid-3" id="tutorialGrid" style="gap:24px;">
"""

for art in crm_tutorials:
    code = art['code']
    cat = 'doctors' if art['category'] == 'آموزش برای پزشکان' else 'patients'
    badge_label = art['category']
    read_time = art.get('readTime', '۶ دقیقه مطالعه')
    if '•' in read_time:
        read_time_short = read_time.split('•')[0].strip()
    else:
        read_time_short = read_time

    video_badge = ''
    if art.get('videoUrl') and art['videoUrl'].strip():
        video_badge = """            <span style="display:inline-flex; align-items:center; gap:4px; font-size:11.5px; color:#38BDF8; background:rgba(0,115,255,0.12); border:1px solid rgba(0,115,255,0.3); border-radius:12px; padding:2px 8px; font-weight:700;">
              <svg class="svg-icon" style="width:12px; height:12px;" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              <span>دارای ویدیو</span>
            </span>"""

    grid_cards_html += f"""
        <!-- Article {code}: {art['category']} -->
        <div class="panel-card tutorial-card" data-category="{cat}">
          <div class="card-meta" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="tutorial-badge">{badge_label}</span>
{video_badge}
            </div>
            <span style="display:inline-flex; align-items:center; gap:5px; font-size:12px; color:var(--text-muted);">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span>{read_time_short}</span>
            </span>
          </div>
          <h3>{art['title']}</h3>
          <p>
            {art['summary']}
          </p>
          <div style="margin-top:auto; border-top:1px solid var(--glass-border); padding-top:14px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:12px; color:var(--brand-primary); font-weight:700; display:inline-flex; align-items:center; gap:6px;">
              <svg class="svg-icon" style="width:14px; height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <span>مخاطب: {art['category']}</span>
            </span>
            <button type="button" class="btn btn-outline" style="padding:6px 14px; font-size:12.5px; display:inline-flex; align-items:center; gap:6px;" onclick="openArticleModal('{code}')">
              <span>مطالعه کامل</span>
              <svg class="svg-icon" style="width:13px; height:13px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </button>
          </div>
        </div>
"""

grid_cards_html += """      </div>
    </div>
  </section>
"""

# 7. Modal Reader Dialog & Consultation CTA
modal_and_cta_html = """  <!-- Article Interactive Modal Reader -->
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
        <!-- Injected via JavaScript with video slot (if present) and article text -->
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
"""

# 8. Script section with articles, video player renderer, search and filter engine
tutorial_articles_js = {}
for art in crm_tutorials:
    tutorial_articles_js[art['code']] = {
        'id': art['id'],
        'code': art['code'],
        'title': art['title'],
        'category': art['category'],
        'readTime': art.get('readTime', ''),
        'videoUrl': art.get('videoUrl', ''),
        'html': art.get('html', '')
    }

script_html = f"""  <!-- Script for Search, Filter & Modal Engine with Dynamic Video Player -->
  <script>
    const checkIconSvg = '<svg class="svg-icon" style="width:14px; height:14px; color:var(--brand-emerald-vital); flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>';

    let tutorialArticles = {json.dumps(tutorial_articles_js, ensure_ascii=False, indent=6)};

    // Video Player Renderer: Aparat, YouTube, or Direct Video (MP4/WebM)
    // If videoUrl is absent or empty, returns empty string (only text will be rendered)
    function renderCrmVideoPlayerHtml(url) {{
      if (!url || typeof url !== 'string' || !url.trim()) return '';
      const cleanUrl = url.trim();

      // Aparat embed
      const aparatMatch = cleanUrl.match(/aparat\\.com\\/(?:v\\/|video\\/video\\/embed\\/videohash\\/)([a-zA-Z0-9]+)/i);
      if (aparatMatch && aparatMatch[1]) {{
        const hash = aparatMatch[1];
        return `
          <div class="tutorial-video-wrapper" style="position:relative; width:100%; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin-bottom:20px; background:#000; border:1px solid rgba(255,255,255,0.12); box-shadow:0 8px 24px rgba(0,0,0,0.35);">
            <iframe src="https://www.aparat.com/video/video/embed/videohash/${{hash}}/vt/frame" style="position:absolute; top:0; left:0; width:100%; height:100%; border:none;" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>
          </div>
        `;
      }}

      // YouTube embed
      const ytMatch = cleanUrl.match(/(?:youtube\\.com\\/(?:watch\\?v=|embed\\/)|youtu\\.be\\/)([a-zA-Z0-9_-]+)/i);
      if (ytMatch && ytMatch[1]) {{
        const ytId = ytMatch[1];
        return `
          <div class="tutorial-video-wrapper" style="position:relative; width:100%; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin-bottom:20px; background:#000; border:1px solid rgba(255,255,255,0.12); box-shadow:0 8px 24px rgba(0,0,0,0.35);">
            <iframe src="https://www.youtube-nocookie.com/embed/${{ytId}}" style="position:absolute; top:0; left:0; width:100%; height:100%; border:none;" allowfullscreen="true"></iframe>
          </div>
        `;
      }}

      // Direct video file (mp4 / webm / ogg)
      if (/\\.(mp4|webm|ogg)($|\\?)/i.test(cleanUrl)) {{
        return `
          <div class="tutorial-video-wrapper" style="width:100%; border-radius:12px; margin-bottom:20px; overflow:hidden; background:#000; border:1px solid rgba(255,255,255,0.12); box-shadow:0 8px 24px rgba(0,0,0,0.35);">
            <video controls style="width:100%; max-height:460px; display:block; outline:none;" preload="metadata">
              <source src="${{cleanUrl}}">
              مرورگر شما از پخش مستقیم این ویدیو پشتیبانی نمی‌کند.
            </video>
          </div>
        `;
      }}

      // Generic HTTP embed
      if (cleanUrl.startsWith('http')) {{
        return `
          <div class="tutorial-video-wrapper" style="position:relative; width:100%; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin-bottom:20px; background:#000; border:1px solid rgba(255,255,255,0.12); box-shadow:0 8px 24px rgba(0,0,0,0.35);">
            <iframe src="${{cleanUrl}}" style="position:absolute; top:0; left:0; width:100%; height:100%; border:none;" allowfullscreen="true"></iframe>
          </div>
        `;
      }}

      return '';
    }}

    function openArticleModal(artId) {{
      const art = tutorialArticles[artId];
      if (!art) return;
      document.getElementById('modalCategoryBadge').innerText = art.category;
      document.getElementById('modalReadTimeText').innerText = art.readTime || '۶ دقیقه مطالعه';
      
      const videoHtml = renderCrmVideoPlayerHtml(art.videoUrl);
      document.getElementById('articleModalContent').innerHTML = 
        '<h2 style="font-size:20px; font-weight:900; color:var(--text-pure); margin-bottom:18px; line-height:1.5;">' + art.title + '</h2>' +
        videoHtml +
        art.html;
      
      const modal = document.getElementById('articleModalBackdrop');
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
      if (window.lenis) window.lenis.stop();
    }}

    function closeArticleModal() {{
      const modal = document.getElementById('articleModalBackdrop');
      modal.classList.remove('active');
      document.body.style.overflow = '';
      if (window.lenis) window.lenis.start();
    }}

    function handleModalBackdropClick(e) {{
      if (e.target.id === 'articleModalBackdrop') {{
        closeArticleModal();
      }}
    }}

    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') {{
        closeArticleModal();
      }}
    }});

    function filterTutorials(category, btn, doScroll = false) {{
      let targetBtn = btn;
      if (typeof btn === 'string') {{
        targetBtn = document.querySelector(`.tutorial-filter-btn[data-filter="${{btn}}"]`);
      }}
      if (targetBtn) {{
        document.querySelectorAll('.tutorial-filter-btn').forEach(b => b.classList.remove('active'));
        targetBtn.classList.add('active');
      }}

      // Map alias categories
      let normalized = category;
      if (category === 'doctor' || category === 'receptionist') normalized = 'doctors';
      if (category === 'user' || category === 'patient') normalized = 'patients';

      const cards = document.querySelectorAll('.tutorial-card');
      cards.forEach(card => {{
        const cat = card.getAttribute('data-category');
        if (normalized === 'all' || cat === normalized) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});

      if (doScroll) {{
        const target = document.getElementById('tutorialGrid');
        if (target) {{
          if (window.lenis) {{
            window.lenis.scrollTo(target, {{ offset: -90 }});
          }} else {{
            target.scrollIntoView({{ behavior: 'smooth' }});
          }}
        }}
      }}
    }}

    function handleTutorialSearch() {{
      const query = document.getElementById('tutorialSearchInput').value.trim().toLowerCase();
      const cards = document.querySelectorAll('.tutorial-card');
      cards.forEach(card => {{
        const text = card.innerText.toLowerCase();
        if (!query || text.includes(query)) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    // Dynamic Live Sync with API
    async function fetchCrmTutorialsLive() {{
      try {{
        const res = await fetch('/api/crm-tutorials');
        if (res.ok) {{
          const data = await res.json();
          if (Array.isArray(data) && data.length) {{
            data.forEach(item => {{
              if (item.code) {{
                tutorialArticles[item.code] = item;
              }}
            }});
          }}
        }}
      }} catch (e) {{
        console.warn('Live CRM tutorials fetch failed:', e);
      }}
    }}

    // Auto-select training section when navigated from Header Role Menus
    document.addEventListener('DOMContentLoaded', function() {{
      fetchCrmTutorialsLive();
      try {{
        const params = new URLSearchParams(window.location.search);
        const role = (params.get('category') || params.get('role') || params.get('audience') || '').toLowerCase();
        if (role === 'user' || role === 'patient' || role === 'patients') {{
          filterTutorials('patients', 'patients', false);
        }} else if (role === 'doctor' || role === 'doctors' || role === 'receptionist' || role === 'secretary') {{
          filterTutorials('doctors', 'doctors', false);
        }}
      }} catch (e) {{}}
    }});
  </script>
"""

# 9. Footer & external scripts (from lines 1141 to 1215 of original)
footer_lines = get_tut_lines(1050, 1218)
# Find where footer starts
footer_idx = -1
for i, line in enumerate(footer_lines):
    if '<!-- Footer -->' in line:
        footer_idx = i
        break

part9_lines = footer_lines[footer_idx:]

# Assemble the whole document
full_content = "\n".join(part1_lines) + "\n" + \
               "\n".join(part2_lines) + "\n" + \
               "\n".join(part3_lines) + "\n" + \
               hero_section_html + "\n" + \
               roadmap_html + "\n" + \
               grid_cards_html + "\n" + \
               modal_and_cta_html + "\n" + \
               script_html + "\n  </main>\n\n  " + \
               "\n".join(part9_lines)

# Write to tutorials.html and portal/tutorials.html
with open('tutorials.html', 'w', encoding='utf-8') as f:
    f.write(full_content)

with open('portal/tutorials.html', 'w', encoding='utf-8') as f:
    f.write(full_content)

print(f"Successfully generated tutorials.html ({len(full_content)} bytes)")
print(f"Successfully generated portal/tutorials.html ({len(full_content)} bytes)")
