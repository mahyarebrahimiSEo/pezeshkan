# -*- coding: utf-8 -*-
"""
Synchronize newsletters data across newsletter.html, index.html, and admin panels.
Ensures modals render the complete rich clinical digest and single clean badges.
"""
import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAG_DIR = os.path.join(BASE_DIR, "mag")
CONTENT_FILE = os.path.join(MAG_DIR, "content", "newsletters.json")
NEWSLETTER_HTML = os.path.join(MAG_DIR, "newsletter.html")
INDEX_HTML = os.path.join(MAG_DIR, "index.html")

with open(CONTENT_FILE, "r", encoding="utf-8") as f:
    newsletters = json.load(f)

print(f"Loaded {len(newsletters)} newsletters from {CONTENT_FILE}")
fallback_js = json.dumps(newsletters, ensure_ascii=False)

# -------------------------------------------------------------
# 1. UPDATE mag/newsletter.html
# -------------------------------------------------------------
with open(NEWSLETTER_HTML, "r", encoding="utf-8") as f:
    nl_content = f.read()

# Replace the obsolete top editionsData block (between lines 68 and 203)
pattern_editions = re.compile(
    r"\s*// بانک اطلاعاتی متنی شماره‌های خبرنامه جهت رندر در مودال[\s\S]*?document\.addEventListener\('keydown', \(e\) => \{[\s\S]*?\}\);\s*",
    re.MULTILINE
)

top_replacement = """
    // پل ارتباطی سازگار با موتور اصلی باز کردن مودال خبرنامه
    function openEditionModal(id) {
      return openNewsletterModal(id);
    }
    function closeEditionModal(e) {
      const modal = document.getElementById('editionModal');
      if (!modal) return;
      if (e && e.target && e.target !== modal && !e.target.classList.contains('edition-modal-close') && !e.target.closest('.edition-modal-close')) {
        return;
      }
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const modal = document.getElementById('editionModal');
        if (modal && modal.style.display === 'flex') {
          modal.style.display = 'none';
          document.body.style.overflow = '';
        }
      }
    });
"""

if pattern_editions.search(nl_content):
    nl_content = pattern_editions.sub(lambda m: "\n" + top_replacement + "\n", nl_content)
    print("✓ Replaced top editionsData block in mag/newsletter.html")
else:
    print("! Top editionsData block pattern not matched")

# Replace static cards inside #newsletterIssuesListWrap
pattern_cards = re.compile(
    r"<!-- شماره ۵۲ -->[\s\S]*?<!-- شماره ۴۹ -->[\s\S]*?</div>\s*</div>\s*</section>",
    re.MULTILINE
)

new_static_cards = """<!-- شماره ۵۲ -->
        <div class="issue-item-card">
          <div class="issue-badge-col">
            <span class="issue-number-badge">شماره ۵۲</span>
            <span class="issue-date">سه‌شنبه گذشته</span>
          </div>
          <div class="issue-content-col">
            <div class="issue-category-tag">دسته‌بندی: خبرنامه و ویژه‌نامه‌های سلامت</div>
            <h3>دیده‌بان پزشکی بازساختی و طب تسکینی: اگزوزوم‌ها، پی‌آر‌پی و رویکردهای نوین مهار درد بدون بیهوشی</h3>
            <p>
              تحلیل بالینی درمان‌های بیولوژیک در آرتروز مفاصل و دیسکوپاتی، مقایسه پلاسمای غنی از پلاکت با فاکتورهای رشد سلولی و الزامات توانبخشی حرکتی.
            </p>
            <div class="issue-key-points">
              <span class="issue-key-tag">پزشکی بازساختی و اگزوزوم</span>
              <span class="issue-key-tag">تزریقات مفصلی PRP</span>
              <span class="issue-key-tag">دکتر مهران رادمنش</span>
            </div>
          </div>
          <div class="issue-action-col" style="flex-wrap:wrap; gap:10px;">
            <button type="button" class="btn-read-issue" onclick="openNewsletterModal('issue-52')" style="cursor:pointer;">
              <span>مطالعه نسخه کامل خبرنامه</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            </button>
            <a href="/mag?article=newsletter-issue-52" class="btn-subtle-issue">
              <span>مشاهده در دسته‌بندی خبرنامه</span> ↗
            </a>
          </div>
        </div>

        <!-- شماره ۵۱ -->
        <div class="issue-item-card">
          <div class="issue-badge-col">
            <span class="issue-number-badge">شماره ۵۱</span>
            <span class="issue-date">دو هفته قبل</span>
          </div>
          <div class="issue-content-col">
            <div class="issue-category-tag">دسته‌بندی: خبرنامه و ویژه‌نامه‌های سلامت</div>
            <h3>دیده‌بان سلامت متابولیک: انقلاب آگونیست‌های GLP-1، محافظت چندارگانی قلب و کلیه و بازتعریف راهنماهای دیابت ۲۰۲۶</h3>
            <p>
              تحلیل جامع کارآزمایی‌های بالینی سماگلوتاید و تیرزپاتاید، محافظت اندام هدف در نارسایی قلبی و کلیوی و استانداردهای پایش پیوسته گلوکز (CGM).
            </p>
            <div class="issue-key-points">
              <span class="issue-key-tag">آگونیست‌های GLP-1</span>
              <span class="issue-key-tag">محافظت کاردیورنال</span>
              <span class="issue-key-tag">دکتر حمیدرضا سلیمی</span>
            </div>
          </div>
          <div class="issue-action-col" style="flex-wrap:wrap; gap:10px;">
            <button type="button" class="btn-read-issue" onclick="openNewsletterModal('issue-51')" style="cursor:pointer;">
              <span>مطالعه نسخه کامل خبرنامه</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            </button>
            <a href="/mag?article=newsletter-issue-51" class="btn-subtle-issue">
              <span>مشاهده در دسته‌بندی خبرنامه</span> ↗
            </a>
          </div>
        </div>

        <!-- شماره ۵۰ -->
        <div class="issue-item-card">
          <div class="issue-badge-col">
            <span class="issue-number-badge">شماره ۵۰</span>
            <span class="issue-date">سه هفته قبل</span>
          </div>
          <div class="issue-content-col">
            <div class="issue-category-tag">دسته‌بندی: خبرنامه و ویژه‌نامه‌های سلامت</div>
            <h3>دیده‌بان فوریت‌های قلب و عروق: راهنمای تریاژ دردهای حاد قفسه سینه، امتیازدهی HEART و الگوریتم ساعات طلایی نجات</h3>
            <p>
              پروتکل اورژانس افتراق سندرم کرونری حاد از دردهای گوارشی و عضلانی اسکلتی، اهمیت تریاژ پیش‌بیمارستانی و پایش نشانگرهای تروپونین فوق‌حساس.
            </p>
            <div class="issue-key-points">
              <span class="issue-key-tag">تریاژ حاد قلبی</span>
              <span class="issue-key-tag">امتیاز HEART</span>
              <span class="issue-key-tag">دکتر حمیدرضا سلیمی</span>
            </div>
          </div>
          <div class="issue-action-col" style="flex-wrap:wrap; gap:10px;">
            <button type="button" class="btn-read-issue" onclick="openNewsletterModal('issue-50')" style="cursor:pointer;">
              <span>مطالعه نسخه کامل خبرنامه</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            </button>
            <a href="/mag?article=newsletter-issue-50" class="btn-subtle-issue">
              <span>مشاهده در دسته‌بندی خبرنامه</span> ↗
            </a>
          </div>
        </div>

        <!-- شماره ۴۹ -->
        <div class="issue-item-card">
          <div class="issue-badge-col">
            <span class="issue-number-badge">شماره ۴۹</span>
            <span class="issue-date">یک ماه قبل</span>
          </div>
          <div class="issue-content-col">
            <div class="issue-category-tag">دسته‌بندی: خبرنامه و ویژه‌نامه‌های سلامت</div>
            <h3>دیده‌بان سلامت مادر، جنین و ژنتیک: جهش‌های غربالگری دوران بارداری؛ از تست سل‌فری (NIPT) تا پایش شریان رحمی</h3>
            <p>
              راهنمای جامع پریناتولوژی برای غربالگری ناهنجاری‌های کروموزومی، سونوگرافی داپلر شریان رحمی در پیشگیری از پره‌اکلامپسی و نشانگرهای بیوشیمیایی سه‌ماهه اول.
            </p>
            <div class="issue-key-points">
              <span class="issue-key-tag">تست NIPT سل‌فری</span>
              <span class="issue-key-tag">داپلر شریان رحمی</span>
              <span class="issue-key-tag">دکتر سارا توکلی</span>
            </div>
          </div>
          <div class="issue-action-col" style="flex-wrap:wrap; gap:10px;">
            <button type="button" class="btn-read-issue" onclick="openNewsletterModal('issue-49')" style="cursor:pointer;">
              <span>مطالعه نسخه کامل خبرنامه</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            </button>
            <a href="/mag?article=newsletter-issue-49" class="btn-subtle-issue">
              <span>مشاهده در دسته‌بندی خبرنامه</span> ↗
            </a>
          </div>
        </div>

      </div>
    </section>"""

if pattern_cards.search(nl_content):
    nl_content = pattern_cards.sub(lambda m: new_static_cards, nl_content)
    print("✓ Replaced static cards in mag/newsletter.html")
else:
    print("! Static cards pattern not matched")

# Replace bottom script in mag/newsletter.html
bottom_pattern = re.compile(
    r"// حافظه محلی کش خبرنامه‌ها[\s\S]*?function closeEditionModal\(e\) \{[\s\S]*?\}",
    re.MULTILINE
)

new_bottom_script = f"""// حافظه محلی کش خبرنامه‌ها جهت رندر سریع و آفلاین
    const FALLBACK_NEWSLETTERS = {fallback_js};
    let NEWSLETTERS_DATA = FALLBACK_NEWSLETTERS;

    // بارگذاری خبرنامه‌ها از API با اولویت داده‌های به‌روز سرور
    async function loadNewsletters() {{
      try {{
        const local = localStorage.getItem('pezeshkan_admin_newsletters');
        if (local) {{
          const parsed = JSON.parse(local);
          if (Array.isArray(parsed) && parsed.length > 0) {{
            NEWSLETTERS_DATA = parsed;
            renderNewslettersList(parsed);
          }}
        }}
      }} catch(e) {{}}

      try {{
        const res = await fetch('/api/newsletters');
        if (!res.ok) throw new Error('Network error');
        const list = await res.json();
        if (Array.isArray(list) && list.length > 0) {{
          NEWSLETTERS_DATA = list;
          renderNewslettersList(list);
          try {{ localStorage.setItem('pezeshkan_admin_newsletters', JSON.stringify(list)); }} catch(e) {{}}
        }}
      }} catch (err) {{
        console.warn('Could not load dynamic newsletters, keeping static fallback:', err);
        if (!NEWSLETTERS_DATA || NEWSLETTERS_DATA.length === 0) {{
          NEWSLETTERS_DATA = FALLBACK_NEWSLETTERS;
          renderNewslettersList(FALLBACK_NEWSLETTERS);
        }}
      }}
    }}

    // رندر پویا لیست خبرنامه‌ها در صفحه با بج تمیز و یکتا
    function renderNewslettersList(list) {{
      const container = document.getElementById('newsletterIssuesListWrap');
      if (!container) return;

      const published = (list || []).filter(item => item.status === 'published' || !item.status);
      if (published.length === 0) return;

      container.innerHTML = published.map(item => {{
        const rawNum = String(item.issueNumber || item.id || '').replace(/^issue-/, '').replace(/^شماره\\s*/, '').trim();
        const slug = item.articleSlug || item.relatedArticleSlug || ('newsletter-issue-' + rawNum);
        const docName = item.doctor || item.doctorName || 'شورای سردبیری مجله سلامت';
        return `
        <div class="issue-item-card">
          <div class="issue-badge-col">
            <span class="issue-number-badge">شماره ${{rawNum}}</span>
            <span class="issue-date">${{item.publishDate || 'منتشر شده'}}</span>
          </div>
          <div class="issue-content-col">
            <div class="issue-category-tag">دسته‌بندی: خبرنامه و ویژه‌نامه‌های سلامت</div>
            <h3>${{item.title}}</h3>
            <p>${{item.summary || ''}}</p>
            <div class="issue-key-points">
              ${{(item.tags || []).map(t => `<span class="issue-key-tag">${{t}}</span>`).join('')}}
              <span class="issue-key-tag">داوری علمی: ${{docName}}</span>
            </div>
          </div>
          <div class="issue-action-col" style="flex-wrap:wrap; gap:8px;">
            <button type="button" class="btn-read-issue" onclick="openNewsletterModal('${{item.id || ('issue-' + rawNum)}}')" style="cursor:pointer;">
              <span>مطالعه نسخه کامل خبرنامه</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            </button>
            <a href="/mag?article=${{slug}}" class="btn-subtle-issue">
              <span>مشاهده در دسته‌بندی خبرنامه</span> ↗
            </a>
          </div>
        </div>
        `;
      }}).join('');
    }}

    // باز کردن مودال مطالعه نسخه کامل شماره خبرنامه
    function openEditionModal(id) {{
      return openNewsletterModal(id);
    }}

    function openNewsletterModal(id) {{
      const cleanId = String(id || '').replace(/^issue-/, '').replace(/^newsletter-/, '').replace(/^شماره\\s*/, '').trim();
      let item = (NEWSLETTERS_DATA || []).find(n => {{
        if (!n) return false;
        if (n.id === id) return true;
        const nCleanId = String(n.id || '').replace(/^issue-/, '').replace(/^newsletter-/, '').replace(/^شماره\\s*/, '').trim();
        const nNumClean = String(n.issueNumber || '').replace(/^شماره\\s*/, '').trim();
        return nCleanId === cleanId || nNumClean === cleanId || ('issue-' + nNumClean) === String(id) || n.issueNumber === id;
      }});

      if (!item && Array.isArray(FALLBACK_NEWSLETTERS)) {{
        item = FALLBACK_NEWSLETTERS.find(n => {{
          if (!n) return false;
          if (n.id === id) return true;
          const nCleanId = String(n.id || '').replace(/^issue-/, '').replace(/^newsletter-/, '').replace(/^شماره\\s*/, '').trim();
          const nNumClean = String(n.issueNumber || '').replace(/^شماره\\s*/, '').trim();
          return nCleanId === cleanId || nNumClean === cleanId || ('issue-' + nNumClean) === String(id) || n.issueNumber === id;
        }});
      }}

      if (!item) return;

      const modal = document.getElementById('editionModal');
      const badge = document.getElementById('modalBadge');
      const body = document.getElementById('modalBody');
      const link = document.getElementById('modalCategoryLink');

      const rawNum = String(item.issueNumber || item.id || '').replace(/^issue-/, '').replace(/^شماره\\s*/, '').trim();
      if (badge) badge.textContent = `شماره ${{rawNum}}`;
      
      const articleSlug = item.articleSlug || item.relatedArticleSlug || ('newsletter-issue-' + rawNum);
      if (link) {{
        link.href = `/mag?article=${{articleSlug}}`;
        link.innerHTML = `<span>مطالعه نسخه کامل در دسته‌بندی خبرنامه</span> ↗`;
        link.style.display = 'inline-flex';
      }}

      const docName = item.doctor || item.doctorName || 'شورای سردبیری مجله بالینی پزشکآن';
      const docSpec = item.doctorSpecialty || 'تحریریه علمی و پژوهشی مجله سلامت';
      const pubDate = item.publishDate || 'شماره جاری';
      const readTime = item.readTime || '۶ دقیقه';
      const fullHtml = item.contentHtml || item.rawHtml || item.content || '';

      if (body) {{
        body.innerHTML = `
          <div style="background: rgba(0, 115, 255, 0.05); border: 1px solid rgba(0, 115, 255, 0.15); border-radius: 12px; padding: 12px 18px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <div style="font-size: 13px; font-weight: 800; color: var(--color-primary); display: flex; align-items: center; gap: 8px;">
              <span>📋</span>
              <span>ویژه‌نامه رسمی تحریریه بالینی پزشکآن • شماره ${{rawNum}}</span>
            </div>
            <button type="button" class="btn-ui btn-subtle-outline" onclick="window.print()" style="font-size: 11.5px; padding: 4px 10px; border-radius: 6px; cursor: pointer;" title="چاپ ویژه‌نامه">
              🖨️ چاپ این شماره
            </button>
          </div>

          <h2 style="font-size:20px; font-weight:900; line-height:1.5; color:var(--text-heading); margin-bottom:14px;">
            ${{item.title}}
          </h2>
          <div style="display:flex; align-items:center; gap:16px; font-size:12.5px; color:var(--text-secondary); margin-bottom:20px; padding-bottom:14px; border-bottom:1px solid var(--border-light); flex-wrap:wrap;">
            <span>✍️ ناظر علمی و نگارش: <strong style="color:var(--text-heading);">${{docName}}</strong> <span style="font-size:11.5px; color:var(--text-muted);">(${{docSpec}})</span></span>
            <span>📅 تاریخ انتشار: ${{pubDate}}</span>
            <span>⏱ زمان مطالعه: ${{readTime}}</span>
          </div>
          ${{item.summary ? `
            <div style="background:rgba(0,115,255,0.06); border-right:4px solid var(--color-primary); border-radius:10px; padding:14px 18px; font-size:14px; font-weight:700; color:var(--color-primary); line-height:1.85; margin-bottom:24px;">
              <div style="font-size:11.5px; font-weight:800; color:var(--text-secondary); margin-bottom:6px;">سرمقاله سردبیر علمی و لید بالینی:</div>
              ${{item.summary}}
            </div>
          ` : ''}}
          <div class="edition-content-article" style="font-size:14.5px; line-height:1.9; color:var(--text-body);">
            ${{fullHtml}}
          </div>
        `;
      }}

      if (modal) {{
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
      }}
    }}

    // بستن مودال
    function closeEditionModal(e) {{
      if (e && e.target && e.target !== document.getElementById('editionModal') && !e.target.classList.contains('edition-modal-close') && !e.target.closest('.edition-modal-close')) {{
        return;
      }}
      const modal = document.getElementById('editionModal');
      if (modal) {{
        modal.style.display = 'none';
        document.body.style.overflow = '';
      }}
    }}"""

if bottom_pattern.search(nl_content):
    nl_content = bottom_pattern.sub(lambda m: new_bottom_script, nl_content)
    print("✓ Replaced bottom script & modal renderer in mag/newsletter.html")
else:
    print("! Bottom script pattern not matched")

with open(NEWSLETTER_HTML, "w", encoding="utf-8") as f:
    f.write(nl_content)

print(f"✓ mag/newsletter.html successfully updated! (length: {len(nl_content)})")

# -------------------------------------------------------------
# 2. UPDATE mag/index.html
# -------------------------------------------------------------
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    idx_content = f.read()

# Replace let newslettersData = [...] in mag/index.html
pattern_idx_newsletters = re.compile(
    r"let newslettersData = \[[\s\S]*?\];\s*",
    re.MULTILINE
)

new_idx_newsletters_line = f"let newslettersData = {fallback_js};\n"

if pattern_idx_newsletters.search(idx_content):
    idx_content = pattern_idx_newsletters.sub(lambda m: new_idx_newsletters_line, idx_content)
    print("✓ Replaced newslettersData in mag/index.html")
else:
    print("! newslettersData in mag/index.html not matched")

# Update openHomeNewsletterModal to ensure clean badge and full HTML
pattern_open_home = re.compile(
    r"function openHomeNewsletterModal\(id\) \{[\s\S]*?function closeHomeNewsletterModal\(e\) \{",
    re.MULTILINE
)

new_open_home_code = """function openHomeNewsletterModal(id) {
      const cleanId = String(id || '').replace(/^issue-/, '').replace(/^newsletter-/, '').replace(/^شماره\\s*/, '').trim();
      const issue = (newslettersData || []).find(n => {
        if (!n) return false;
        if (n.id === id) return true;
        const nCleanId = String(n.id || '').replace(/^issue-/, '').replace(/^newsletter-/, '').replace(/^شماره\\s*/, '').trim();
        const nNumClean = String(n.issueNumber || '').replace(/^شماره\\s*/, '').trim();
        return nCleanId === cleanId || nNumClean === cleanId || ('issue-' + nNumClean) === String(id) || n.issueNumber === id;
      }) || (newslettersData && newslettersData[0]);
      if (!issue) return;

      const modal = document.getElementById('homeNewsletterModal');
      const badge = document.getElementById('homeModalIssueBadge');
      const body = document.getElementById('homeModalBody');
      if (!modal || !badge || !body) return;

      const rawNum = String(issue.issueNumber || issue.id || '').replace(/^issue-/, '').replace(/^شماره\\s*/, '').trim();
      badge.textContent = `شماره ${rawNum}`;

      let contentHtml = '';
      if (issue.contentHtml) {
        contentHtml = issue.contentHtml;
      } else if (issue.rawHtml) {
        contentHtml = issue.rawHtml;
      } else if (issue.sections && issue.sections.length) {
        contentHtml = issue.sections.map(s => `
          <div style="margin-bottom: 24px;">
            <h3 style="font-size: 17px; font-weight: 800; color: var(--text-heading); margin-bottom: 10px; border-right: 3px solid var(--color-primary); padding-right: 10px;">${escapeHtml(s.title || s.heading)}</h3>
            <p style="font-size: 14.5px; color: var(--text-body); line-height: 1.85;">${escapeHtml(s.content || s.text)}</p>
          </div>
        `).join('');
      } else {
        contentHtml = `<p>${escapeHtml(issue.summary || '')}</p>`;
      }

      const doctorName = issue.doctor || (issue.author && issue.author.name) || 'تیم محتوایی پزشکآن';
      const doctorSpec = issue.doctorSpecialty || (issue.author && issue.author.title) || 'تحریریه علمی و پژوهشی مجله';
      const pubDate = issue.publishDate || issue.lastReviewed || 'مهر ۱۴۰۵';
      const readTime = issue.readTime || '۶ دقیقه';
      const heroImg = issue.heroImage || issue.image || '';

      body.innerHTML = `
        ${heroImg ? `<img src="${heroImg}" alt="${escapeHtml(issue.title)}" style="width:100%; max-height:280px; object-fit:cover; border-radius:12px; margin-bottom:20px; box-shadow:0 4px 16px rgba(0,0,0,0.08);">` : ''}
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:14px; font-size:12.5px; color:var(--text-secondary); background:var(--bg-subtle); padding:10px 14px; border-radius:10px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-weight:700; color:var(--text-heading);">✍️ تهیه و تنظیم:</span>
            <span style="color:var(--color-primary); font-weight:700;">${escapeHtml(doctorName)}</span>
            <span>(${escapeHtml(doctorSpec)})</span>
          </div>
          <div style="display:flex; align-items:center; gap:12px;">
            <span>📅 ${escapeHtml(pubDate)}</span>
            <span>⏱️ ${escapeHtml(readTime)}</span>
          </div>
        </div>
        <h2 style="font-size:20px; font-weight:900; color:var(--text-heading); margin-bottom:14px; line-height:1.5;">${escapeHtml(issue.title)}</h2>
        <div style="background:rgba(0,115,255,0.05); border-right:4px solid var(--color-primary); padding:14px 18px; border-radius:8px; margin-bottom:24px; font-size:14px; color:var(--text-body); line-height:1.8;">
          ${escapeHtml(issue.summary || '')}
        </div>
        <div class="article-rich-content" style="margin-bottom:24px;">
          ${contentHtml}
        </div>
        <div style="background:var(--bg-subtle); border:1px solid var(--border-color); border-radius:12px; padding:16px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
          <span style="font-size:13px; color:var(--text-body);">آیا می‌خواهید نسخه‌های بعدی خبرنامه مستقیماً برای شما ارسال شود؟</span>
          <a href="/mag/newsletter#newsletterForm" class="btn-ui btn-primary-gradient" style="font-size:12px; padding:6px 14px; text-decoration:none;">عضویت رایگان در خبرنامه</a>
        </div>
      `;

      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }

    function closeHomeNewsletterModal(e) {"""

if pattern_open_home.search(idx_content):
    idx_content = pattern_open_home.sub(lambda m: new_open_home_code, idx_content)
    print("✓ Replaced openHomeNewsletterModal in mag/index.html")
else:
    print("! openHomeNewsletterModal in mag/index.html not matched")

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(idx_content)

print(f"✓ mag/index.html successfully updated! (length: {len(idx_content)})")
