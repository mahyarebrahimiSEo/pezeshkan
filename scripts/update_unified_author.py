# -*- coding: utf-8 -*-
"""
Update unified author to 'تیم متخصص محتوا نویس پزشکآن' across all articles,
newsletters, modals, cards, and admin panels. Add dedicated Author & Scientific
Verification Box with the exact requested statement.
"""
import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAG_DIR = os.path.join(BASE_DIR, "mag")
ARTICLES_JSON = os.path.join(MAG_DIR, "content", "articles.json")
NEWSLETTERS_JSON = os.path.join(MAG_DIR, "content", "newsletters.json")
INDEX_HTML = os.path.join(MAG_DIR, "index.html")
NEWSLETTER_HTML = os.path.join(MAG_DIR, "newsletter.html")
ADMIN_HTML = os.path.join(MAG_DIR, "admin.html")
ROOT_ADMIN_HTML = os.path.join(BASE_DIR, "admin.html")

AUTHOR_NAME = "تیم متخصص محتوا نویس پزشکآن"
AUTHOR_TITLE = "تحریریه علمی و شورای پایش بالینی مجله سلامت پزشکآن"
AUTHOR_AVATAR = "https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=200&q=80"
AUTHOR_BADGE = "دارای تأییدیه علمی و استناد به منابع معتبر"

# 1. Update articles.json
with open(ARTICLES_JSON, "r", encoding="utf-8") as f:
    articles = json.load(f)

for a in articles:
    a["author"] = {
        "name": AUTHOR_NAME,
        "title": AUTHOR_TITLE,
        "avatar": AUTHOR_AVATAR,
        "badge": AUTHOR_BADGE
    }

with open(ARTICLES_JSON, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("✓ Updated mag/content/articles.json")

# 2. Update newsletters.json
with open(NEWSLETTERS_JSON, "r", encoding="utf-8") as f:
    newsletters = json.load(f)

for n in newsletters:
    n["doctor"] = AUTHOR_NAME
    n["doctorName"] = AUTHOR_NAME
    n["doctorId"] = "pezeshkan-editorial-team"
    n["doctorSpecialty"] = AUTHOR_TITLE
    n["author"] = {
        "name": AUTHOR_NAME,
        "title": AUTHOR_TITLE
    }

with open(NEWSLETTERS_JSON, "w", encoding="utf-8") as f:
    json.dump(newsletters, f, ensure_ascii=False, indent=2)

print("✓ Updated mag/content/newsletters.json")

# 3. Update mag/index.html
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    idx_content = f.read()

# Update articlesData authors in inline JS
def update_articles_data(content):
    # Regex find let articlesData = [ ... ];
    pattern = re.compile(r"let articlesData = (\[[\s\S]*?\]);\s*let newslettersData", re.MULTILINE)
    m = pattern.search(content)
    if not m:
        print("! articlesData pattern not matched in index.html")
        return content
    try:
        data = json.loads(m.group(1))
        for art in data:
            art["author"] = {
                "name": AUTHOR_NAME,
                "title": AUTHOR_TITLE,
                "avatar": AUTHOR_AVATAR,
                "badge": AUTHOR_BADGE
            }
        new_json = json.dumps(data, ensure_ascii=False)
        return content[:m.start(1)] + new_json + content[m.end(1):]
    except Exception as e:
        print("! Error updating articlesData json:", e)
        return content

idx_content = update_articles_data(idx_content)

# Update newslettersData in mag/index.html
def update_newsletters_data(content):
    pattern = re.compile(r"let newslettersData = (\[[\s\S]*?\]);\s*function escapeHtml", re.MULTILINE)
    m = pattern.search(content)
    if not m:
        print("! newslettersData pattern not matched in index.html")
        return content
    try:
        data = json.loads(m.group(1))
        for n in data:
            n["doctor"] = AUTHOR_NAME
            n["doctorName"] = AUTHOR_NAME
            n["doctorId"] = "pezeshkan-editorial-team"
            n["doctorSpecialty"] = AUTHOR_TITLE
            n["author"] = {
                "name": AUTHOR_NAME,
                "title": AUTHOR_TITLE
            }
        new_json = json.dumps(data, ensure_ascii=False)
        return content[:m.start(1)] + new_json + content[m.end(1):]
    except Exception as e:
        print("! Error updating newslettersData json:", e)
        return content

idx_content = update_newsletters_data(idx_content)

# Update openArticleReader in mag/index.html to add the Author & Verification Box
reader_pattern = re.compile(
    r"function openArticleReader\(id, pushState = true\) \{[\s\S]*?document\.getElementById\('articleReaderContent'\)\.innerHTML = `[\s\S]*?`;\s*\}",
    re.MULTILINE
)

new_reader_code = """function openArticleReader(id, pushState = true) {
      const art = findArticleBySlugOrId(id) || articlesData[0];
      if (!art) return;
      if (window.lenis) { window.lenis.scrollTo(0, { duration: 1.1 }); } else { window.scrollTo({ top: 0, behavior: 'smooth' }); }

      document.getElementById('viewHubMain').style.display = 'none';
      document.getElementById('viewCategoryArea').style.display = 'none';
      document.getElementById('viewArticleReaderArea').style.display = 'block';

      const canonicalSlug = art.slug || art.id;
      const targetUrl = `/mag/${encodeURIComponent(canonicalSlug)}`;

      if (pushState && window.history && window.history.pushState) {
        window.history.pushState({ view: 'article', id: art.id, slug: canonicalSlug }, art.title, targetUrl);
      } else if (!pushState && window.history && window.history.replaceState) {
        if (window.location.pathname !== targetUrl) {
          window.history.replaceState({ view: 'article', id: art.id, slug: canonicalSlug }, art.title, targetUrl);
        }
      }
      document.title = `${art.title} | مجله سلامت بالینی پزشکآن`;

      // Update Canonical Link in Head
      let canonicalEl = document.querySelector('link[rel="canonical"]');
      if (!canonicalEl) {
        canonicalEl = document.createElement('link');
        canonicalEl.setAttribute('rel', 'canonical');
        document.head.appendChild(canonicalEl);
      }
      canonicalEl.setAttribute('href', `https://pezeshkan.me${targetUrl}`);

      const artIcon = medicalIcons[art.categoryIcon] || medicalIcons['stethoscope'];

      const tocHtml = (art.sections || []).map(s => `
        <li style="margin-bottom:10px;"><a href="#${s.id}" style="color:var(--text-body); font-size:13px; font-weight:600;">• ${s.title}</a></li>
      `).join('');

      const sectionsHtml = (art.sections || []).map(s => `
        <div id="${s.id}" style="margin-bottom:28px;">
          <h3 style="font-size:18px; font-weight:800; color:var(--text-heading); margin-bottom:12px; border-right:3px solid var(--color-primary); padding-right:12px;">${s.title}</h3>
          <p style="font-size:15px; color:var(--text-body); line-height:1.9;">${s.content}</p>
        </div>
      `).join('');

      document.getElementById('articleReaderContent').innerHTML = `
        <aside class="reader-sidebar">
          <h4 style="font-size:14px; font-weight:800; color:var(--text-heading); margin-bottom:14px;">فهرست مطالب مقاله</h4>
          <ul style="list-style:none; padding:0; margin-bottom:24px;">${tocHtml}</ul>
          
          <!-- باکس نویسنده و تاییدیه علمی در ستون کناری -->
          <div class="author-verification-sidebar-card" style="border-top:1px solid var(--border-color); padding-top:16px;">
            <div style="font-size:11px; font-weight:800; color:var(--color-primary); margin-bottom:10px; display:flex; align-items:center; gap:6px;">
              <span>✍️</span>
              <span>نویسنده و هیئت تحریریه بالینی</span>
            </div>
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
              <div style="position:relative; flex-shrink:0;">
                <div style="width:44px; height:44px; border-radius:50%; background:linear-gradient(135deg, #0073FF 0%, #00C48C 100%); display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-size:19px; box-shadow:0 3px 10px rgba(0,115,255,0.25);">
                  🩺
                </div>
                <span style="position:absolute; bottom:-2px; left:-2px; background:#00E599; color:#0F172A; width:16px; height:16px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:900; border:2px solid #FFFFFF;">✓</span>
              </div>
              <div>
                <h5 style="font-size:13.5px; font-weight:900; color:var(--text-heading); margin:0;">تیم متخصص محتوا نویس پزشکآن</h5>
                <span style="font-size:11px; color:var(--text-secondary); display:block; margin-top:2px;">تحریریه علمی و پایش بالینی مجله</span>
              </div>
            </div>

            <div style="background:linear-gradient(135deg, rgba(0, 115, 255, 0.05) 0%, rgba(0, 229, 153, 0.04) 100%); border:1px solid rgba(0, 115, 255, 0.16); border-radius:10px; padding:12px; margin-bottom:14px;">
              <div style="display:flex; align-items:center; gap:6px; font-size:11.5px; font-weight:800; color:#059669; margin-bottom:6px;">
                ${medicalIcons['shield_check']}
                <span>تأییدیه علمی و منابع معتبر</span>
              </div>
              <p style="font-size:12px; color:var(--text-body); line-height:1.8; margin:0; font-weight:600;">
                این مقاله توسط متخصصین نوشته شده و دارای تایید علمی هستش و از منابع معتبر بین‌المللی استخراج شده است.
              </p>
            </div>

            <button class="btn-ui btn-primary-gradient" style="width:100%; justify-content:center; font-size:12px; padding:9px 12px;" onclick="openBookingDrawer()">
              ${medicalIcons['stethoscope']}
              <span>مشاوره با پزشکان متخصص پزشکآن</span>
            </button>
          </div>
        </aside>

        <article class="reader-article-body">
          <img src="${art.image}" class="reader-hero-img" alt="${art.title}">
          
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
            <div style="display:flex; align-items:center; gap:10px;">
              <span class="hero-tag-badge">
                ${artIcon}
                <span>${art.tag}</span>
              </span>
              <span style="font-size:12px; color:var(--text-secondary);">آخرین بازبینی علمی: ${art.lastReviewed}</span>
            </div>
            <div style="font-size:12px; color:var(--color-primary); font-weight:700; display:flex; align-items:center; gap:6px;">
              <span>✍️ نویسنده:</span>
              <span>تیم متخصص محتوا نویس پزشکآن</span>
            </div>
          </div>

          <h1 style="font-size:24px; font-weight:900; color:var(--text-heading); margin-bottom:16px; line-height:1.5;">${art.title}</h1>
          <div style="background:var(--bg-subtle); border-right:4px solid var(--color-primary); padding:16px; border-radius:8px; margin-bottom:28px; font-size:14.5px; color:var(--text-body); line-height:1.8;">
            ${art.summary}
          </div>

          <div class="article-rich-content">${formatArticleHtml(art.rawHtml || art.contentHtml || sectionsHtml)}</div>

          ${(art.faqs && art.faqs.length) ? `
            <div style="margin-top:32px; background:var(--bg-subtle); border-radius:var(--radius-md); padding:20px;">
              <h4 style="font-size:16px; font-weight:800; color:var(--text-heading); margin-bottom:16px;">پرسش‌های پرتکرار بیماران (FAQ)</h4>
              ${art.faqs.map(f => `
                <div style="margin-bottom:14px; border-bottom:1px dashed var(--border-color); padding-bottom:12px;">
                  <strong style="display:block; color:var(--text-heading); font-size:14px; margin-bottom:6px;">❓ ${f.q}</strong>
                  <p style="color:var(--text-body); font-size:13.5px; line-height:1.8; margin:0;">${f.a}</p>
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${(art.citations && art.citations.length) ? `
            <div style="margin-top:20px; font-size:12px; color:var(--text-secondary); background:rgba(2,132,199,0.05); border:1px solid rgba(2,132,199,0.15); border-radius:8px; padding:12px 16px;">
              <strong>مراجع علمی و استنادهای بالینی:</strong>
              <ul style="margin:6px 0 0 16px; padding:0;">
                ${art.citations.map(c => `<li><a href="${c.link}" target="_blank" rel="noopener noreferrer" style="color:var(--color-primary); text-decoration:underline;">${c.title}</a></li>`).join('')}
              </ul>
            </div>
          ` : ''}

          <!-- باکس کامل نویسنده و تاییدیه علمی زیر مقاله -->
          <div class="article-author-verification-box" style="margin-top:32px; background:linear-gradient(135deg, rgba(0, 115, 255, 0.05) 0%, rgba(0, 229, 153, 0.04) 100%); border:1px solid rgba(0, 115, 255, 0.18); border-radius:16px; padding:22px;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div style="position:relative; flex-shrink:0;">
                  <div style="width:52px; height:52px; border-radius:50%; background:linear-gradient(135deg, #0073FF 0%, #00C48C 100%); display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-size:24px; box-shadow:0 4px 14px rgba(0,115,255,0.25);">
                    🩺
                  </div>
                  <span style="position:absolute; bottom:-2px; left:-2px; background:#00E599; color:#0F172A; width:18px; height:18px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:900; border:2px solid #FFFFFF;">✓</span>
                </div>
                <div>
                  <div style="font-size:11px; font-weight:800; color:var(--color-primary); margin-bottom:2px;">درباره نویسنده مقاله</div>
                  <h4 style="font-size:16px; font-weight:900; color:var(--text-heading); margin:0;">تیم متخصص محتوا نویس پزشکآن</h4>
                  <span style="font-size:12px; color:var(--text-secondary);">شورای علمی، تدوین بالینی و راستی‌آزمایی شواهد پزشکی اکوسیستم سلامت پزشکآن</span>
                </div>
              </div>
              <span style="background:rgba(0, 229, 153, 0.12); color:#059669; border:1px solid rgba(0, 229, 153, 0.3); padding:4px 12px; border-radius:20px; font-size:12px; font-weight:800; display:inline-flex; align-items:center; gap:6px;">
                🛡️ دارای تأییدیه علمی تحریریه
              </span>
            </div>

            <div style="background:#FFFFFF; border:1px solid rgba(0, 115, 255, 0.12); border-radius:12px; padding:14px 16px;">
              <div style="display:flex; align-items:flex-start; gap:10px;">
                <span style="font-size:18px; line-height:1.2;">✨</span>
                <div>
                  <strong style="font-size:13.5px; color:var(--text-heading); display:block; margin-bottom:4px;">ضمانت اصالت و اعتبار محتوای سلامت:</strong>
                  <p style="font-size:13px; color:var(--text-body); line-height:1.85; margin:0; font-weight:600;">
                    این مقاله توسط متخصصین نوشته شده و دارای تایید علمی هستش و از منابع معتبر و گایدلاین‌های بالینی بین‌المللی تدوین شده است.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="reader-cta-card" style="margin-top:24px;">
            <div>
              <h4 style="font-size:15px; font-weight:800; color:var(--text-heading); margin-bottom:4px;">نیاز به بررسی دقیق‌تر پرونده پزشکی خود دارید؟</h4>
              <p style="font-size:12.5px; color:var(--text-secondary);">می‌توانید مستقیماً آزمایش‌ها و گزارش‌های تصویربرداری خود را جهت ارزیابی به پزشکان متخصص پزشکآن ارسال فرمایید.</p>
            </div>
            <button class="btn-ui btn-primary-gradient" onclick="openBookingDrawer()">
              ${medicalIcons['calendar']}
              <span>رزرو ویزیت آنلاین یا حضوری</span>
            </button>
          </div>
        </article>
      `;
    }"""

if reader_pattern.search(idx_content):
    idx_content = reader_pattern.sub(lambda m: new_reader_code, idx_content)
    print("✓ Replaced openArticleReader in mag/index.html")
else:
    print("! openArticleReader pattern not matched in mag/index.html")

# Update openHomeNewsletterModal in mag/index.html to add the Author & Verification Box
home_modal_pattern = re.compile(
    r"function openHomeNewsletterModal\(id\) \{[\s\S]*?function closeHomeNewsletterModal\(e\) \{",
    re.MULTILINE
)

new_home_modal_code = """function openHomeNewsletterModal(id) {
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

      const doctorName = 'تیم متخصص محتوا نویس پزشکآن';
      const doctorSpec = 'تحریریه علمی و شورای پایش بالینی مجله سلامت پزشکآن';
      const pubDate = issue.publishDate || issue.lastReviewed || 'مهر ۱۴۰۵';
      const readTime = issue.readTime || '۶ دقیقه';
      const heroImg = issue.heroImage || issue.image || '';

      body.innerHTML = `
        ${heroImg ? `<img src="${heroImg}" alt="${escapeHtml(issue.title)}" style="width:100%; max-height:280px; object-fit:cover; border-radius:12px; margin-bottom:20px; box-shadow:0 4px 16px rgba(0,0,0,0.08);">` : ''}
        
        <!-- باکس نویسنده و تاییدیه علمی خبرنامه -->
        <div class="newsletter-author-verification-box" style="background: linear-gradient(135deg, rgba(0, 115, 255, 0.05) 0%, rgba(0, 229, 153, 0.04) 100%); border: 1px solid rgba(0, 115, 255, 0.18); border-radius: 14px; padding: 16px 18px; margin-bottom: 20px;">
          <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 12px;">
              <div style="position: relative; flex-shrink: 0;">
                <div style="width: 46px; height: 46px; border-radius: 50%; background: linear-gradient(135deg, #0073FF 0%, #00C48C 100%); display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-size: 20px; box-shadow: 0 4px 12px rgba(0, 115, 255, 0.2);">
                  🩺
                </div>
                <span style="position: absolute; bottom: -2px; left: -2px; background: #00E599; color: #0F172A; width: 16px; height: 16px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 9px; font-weight: 900; border: 2px solid #FFFFFF;">✓</span>
              </div>
              <div>
                <div style="font-size: 11px; font-weight: 800; color: var(--color-primary); margin-bottom: 2px;">نویسنده و ناظر علمی ویژه‌نامه</div>
                <h4 style="font-size: 15px; font-weight: 900; color: var(--text-heading); margin: 0;">تیم متخصص محتوا نویس پزشکآن</h4>
                <span style="font-size: 11.5px; color: var(--text-secondary);">${doctorSpec}</span>
              </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="background: rgba(0, 229, 153, 0.12); color: #059669; border: 1px solid rgba(0, 229, 153, 0.28); padding: 4px 10px; border-radius: 20px; font-size: 11.5px; font-weight: 800;">
                🛡️ تأیید علمی
              </span>
              <span style="font-size: 12px; color: var(--text-secondary);">📅 ${escapeHtml(pubDate)}</span>
            </div>
          </div>

          <div style="background: #FFFFFF; border: 1px solid rgba(0, 115, 255, 0.12); border-radius: 10px; padding: 10px 14px;">
            <div style="display: flex; align-items: flex-start; gap: 8px;">
              <span style="font-size: 16px; line-height: 1.2;">✨</span>
              <p style="font-size: 12.5px; color: var(--text-body); line-height: 1.85; margin: 0; font-weight: 600;">
                این مقاله و خبرنامه توسط متخصصین نوشته شده و دارای تایید علمی هستش و از منابع معتبر و گایدلاین‌های بالینی بین‌المللی تدوین شده است.
              </p>
            </div>
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

if home_modal_pattern.search(idx_content):
    idx_content = home_modal_pattern.sub(lambda m: new_home_modal_code, idx_content)
    print("✓ Replaced openHomeNewsletterModal in mag/index.html")
else:
    print("! openHomeNewsletterModal pattern not matched in mag/index.html")

# Replace any occurrence of 'تیم محتوایی پزشکآن' in index.html with 'تیم متخصص محتوا نویس پزشکآن'
idx_content = idx_content.replace("تیم محتوایی پزشکآن", AUTHOR_NAME)

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(idx_content)

print(f"✓ mag/index.html updated successfully! ({len(idx_content)} bytes)")

# 4. Update mag/newsletter.html
with open(NEWSLETTER_HTML, "r", encoding="utf-8") as f:
    nl_content = f.read()

# Replace any occurrence of 'تیم محتوایی پزشکآن' or old doctor names in tags
nl_content = nl_content.replace("تیم محتوایی پزشکآن", AUTHOR_NAME)
nl_content = nl_content.replace("دکتر مهران رادمنش", AUTHOR_NAME)
nl_content = nl_content.replace("دکتر حمیدرضا سلیمی", AUTHOR_NAME)
nl_content = nl_content.replace("دکتر سارا توکلی", AUTHOR_NAME)

# Update openNewsletterModal in mag/newsletter.html
nl_modal_pattern = re.compile(
    r"function openNewsletterModal\(id\) \{[\s\S]*?function closeEditionModal\(e\) \{",
    re.MULTILINE
)

new_nl_modal_code = """function openNewsletterModal(id) {
      const cleanId = String(id || '').replace(/^issue-/, '').replace(/^newsletter-/, '').replace(/^شماره\\s*/, '').trim();
      let item = (NEWSLETTERS_DATA || []).find(n => {
        if (!n) return false;
        if (n.id === id) return true;
        const nCleanId = String(n.id || '').replace(/^issue-/, '').replace(/^newsletter-/, '').replace(/^شماره\\s*/, '').trim();
        const nNumClean = String(n.issueNumber || '').replace(/^شماره\\s*/, '').trim();
        return nCleanId === cleanId || nNumClean === cleanId || ('issue-' + nNumClean) === String(id) || n.issueNumber === id;
      });

      if (!item && Array.isArray(FALLBACK_NEWSLETTERS)) {
        item = FALLBACK_NEWSLETTERS.find(n => {
          if (!n) return false;
          if (n.id === id) return true;
          const nCleanId = String(n.id || '').replace(/^issue-/, '').replace(/^newsletter-/, '').replace(/^شماره\\s*/, '').trim();
          const nNumClean = String(n.issueNumber || '').replace(/^شماره\\s*/, '').trim();
          return nCleanId === cleanId || nNumClean === cleanId || ('issue-' + nNumClean) === String(id) || n.issueNumber === id;
        });
      }

      if (!item) return;

      const modal = document.getElementById('editionModal');
      const badge = document.getElementById('modalBadge');
      const body = document.getElementById('modalBody');
      const link = document.getElementById('modalCategoryLink');

      const rawNum = String(item.issueNumber || item.id || '').replace(/^issue-/, '').replace(/^شماره\\s*/, '').trim();
      if (badge) badge.textContent = `شماره ${rawNum}`;
      
      const articleSlug = item.articleSlug || item.relatedArticleSlug || ('newsletter-issue-' + rawNum);
      if (link) {
        link.href = `/mag?article=${articleSlug}`;
        link.innerHTML = `<span>مطالعه نسخه کامل در دسته‌بندی خبرنامه</span> ↗`;
        link.style.display = 'inline-flex';
      }

      const docName = 'تیم متخصص محتوا نویس پزشکآن';
      const docSpec = 'تحریریه علمی و شورای پایش بالینی مجله سلامت پزشکآن';
      const pubDate = item.publishDate || 'شماره جاری';
      const readTime = item.readTime || '۶ دقیقه';
      const fullHtml = item.contentHtml || item.rawHtml || item.content || '';

      if (body) {
        body.innerHTML = `
          <div style="background: rgba(0, 115, 255, 0.05); border: 1px solid rgba(0, 115, 255, 0.15); border-radius: 12px; padding: 12px 18px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <div style="font-size: 13px; font-weight: 800; color: var(--color-primary); display: flex; align-items: center; gap: 8px;">
              <span>📋</span>
              <span>ویژه‌نامه رسمی تحریریه بالینی پزشکآن • شماره ${rawNum}</span>
            </div>
            <button type="button" class="btn-ui btn-subtle-outline" onclick="window.print()" style="font-size: 11.5px; padding: 4px 10px; border-radius: 6px; cursor: pointer;" title="چاپ ویژه‌نامه">
              🖨️ چاپ این شماره
            </button>
          </div>

          <!-- باکس نویسنده و تاییدیه علمی خبرنامه -->
          <div class="newsletter-author-verification-box" style="background: linear-gradient(135deg, rgba(0, 115, 255, 0.05) 0%, rgba(0, 229, 153, 0.04) 100%); border: 1px solid rgba(0, 115, 255, 0.18); border-radius: 14px; padding: 16px 18px; margin-bottom: 22px;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
              <div style="display: flex; align-items: center; gap: 12px;">
                <div style="position: relative; flex-shrink: 0;">
                  <div style="width: 46px; height: 46px; border-radius: 50%; background: linear-gradient(135deg, #0073FF 0%, #00C48C 100%); display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-size: 20px; box-shadow: 0 4px 12px rgba(0, 115, 255, 0.2);">
                    🩺
                  </div>
                  <span style="position: absolute; bottom: -2px; left: -2px; background: #00E599; color: #0F172A; width: 16px; height: 16px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 9px; font-weight: 900; border: 2px solid #FFFFFF;">✓</span>
                </div>
                <div>
                  <div style="font-size: 11px; font-weight: 800; color: var(--color-primary); margin-bottom: 2px;">نویسنده و هیئت تحریریه بالینی</div>
                  <h4 style="font-size: 15px; font-weight: 900; color: var(--text-heading); margin: 0;">تیم متخصص محتوا نویس پزشکآن</h4>
                  <span style="font-size: 11.5px; color: var(--text-secondary);">${docSpec}</span>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="background: rgba(0, 229, 153, 0.12); color: #059669; border: 1px solid rgba(0, 229, 153, 0.28); padding: 4px 10px; border-radius: 20px; font-size: 11.5px; font-weight: 800;">
                  🛡️ تأیید علمی
                </span>
                <span style="font-size: 12px; color: var(--text-secondary);">📅 ${pubDate}</span>
                <span style="font-size: 12px; color: var(--text-secondary);">⏱ ${readTime}</span>
              </div>
            </div>

            <div style="background: #FFFFFF; border: 1px solid rgba(0, 115, 255, 0.12); border-radius: 10px; padding: 10px 14px;">
              <div style="display: flex; align-items: flex-start; gap: 8px;">
                <span style="font-size: 16px; line-height: 1.2;">✨</span>
                <p style="font-size: 12.5px; color: var(--text-body); line-height: 1.85; margin: 0; font-weight: 600;">
                  این مقاله و خبرنامه توسط متخصصین نوشته شده و دارای تایید علمی هستش و از منابع معتبر و گایدلاین‌های بالینی بین‌المللی تدوین شده است.
                </p>
              </div>
            </div>
          </div>

          <h2 style="font-size:20px; font-weight:900; line-height:1.5; color:var(--text-heading); margin-bottom:14px;">
            ${item.title}
          </h2>
          ${item.summary ? `
            <div style="background:rgba(0,115,255,0.06); border-right:4px solid var(--color-primary); border-radius:10px; padding:14px 18px; font-size:14px; font-weight:700; color:var(--color-primary); line-height:1.85; margin-bottom:24px;">
              <div style="font-size:11.5px; font-weight:800; color:var(--text-secondary); margin-bottom:6px;">سرمقاله سردبیر علمی و لید بالینی:</div>
              ${item.summary}
            </div>
          ` : ''}
          <div class="edition-content-article" style="font-size:14.5px; line-height:1.9; color:var(--text-body);">
            ${fullHtml}
          </div>
        `;
      }

      if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
      }
    }

    function closeEditionModal(e) {"""

if nl_modal_pattern.search(nl_content):
    nl_content = nl_modal_pattern.sub(lambda m: new_nl_modal_code, nl_content)
    print("✓ Replaced openNewsletterModal in mag/newsletter.html")
else:
    print("! openNewsletterModal pattern not matched in mag/newsletter.html")

# Update FALLBACK_NEWSLETTERS in mag/newsletter.html with unified doctor/author
fallback_nl_pattern = re.compile(r"const FALLBACK_NEWSLETTERS = (\[[\s\S]*?\]);\s*let NEWSLETTERS_DATA", re.MULTILINE)
m_nl = fallback_nl_pattern.search(nl_content)
if m_nl:
    try:
        nl_data = json.loads(m_nl.group(1))
        for item in nl_data:
            item["doctor"] = AUTHOR_NAME
            item["doctorName"] = AUTHOR_NAME
            item["doctorId"] = "pezeshkan-editorial-team"
            item["doctorSpecialty"] = AUTHOR_TITLE
            item["author"] = {
                "name": AUTHOR_NAME,
                "title": AUTHOR_TITLE
            }
        new_nl_json = json.dumps(nl_data, ensure_ascii=False)
        nl_content = nl_content[:m_nl.start(1)] + new_nl_json + nl_content[m_nl.end(1):]
        print("✓ Updated FALLBACK_NEWSLETTERS in mag/newsletter.html")
    except Exception as e:
        print("! Error updating FALLBACK_NEWSLETTERS in newsletter.html:", e)

with open(NEWSLETTER_HTML, "w", encoding="utf-8") as f:
    f.write(nl_content)

print(f"✓ mag/newsletter.html updated successfully! ({len(nl_content)} bytes)")

# 5. Update mag/admin.html and root admin.html
for apath in [ADMIN_HTML, ROOT_ADMIN_HTML]:
    if os.path.exists(apath):
        with open(apath, "r", encoding="utf-8") as f:
            ad_content = f.read()
        
        # Replace doctor selector default to include Pezeshkan Editorial Team
        ad_content = ad_content.replace(
            "dEdit.innerHTML = DOCTORS.map",
            'dEdit.innerHTML = `<option value="pezeshkan-editorial-team" selected>تیم متخصص محتوا نویس پزشکآن — تحریریه علمی و پایش بالینی</option>` + DOCTORS.map'
        )
        ad_content = ad_content.replace(
            "nDocEdit.innerHTML = DOCTORS.map",
            'nDocEdit.innerHTML = `<option value="pezeshkan-editorial-team" selected>تیم متخصص محتوا نویس پزشکآن — تحریریه علمی و پایش بالینی</option>` + DOCTORS.map'
        )
        
        with open(apath, "w", encoding="utf-8") as f:
            f.write(ad_content)
        print(f"✓ Updated {apath}")

print("All updates successfully completed!")
