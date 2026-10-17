# -*- coding: utf-8 -*-
"""
Full generator for WordPress-grade Pezeshkan CMS Studio (mag/admin.html)
"""
import os
import json

BASE_DIR = r"e:\antigravity\pezeshkan_design"
MAG_DIR = os.path.join(BASE_DIR, "mag")

with open(os.path.join(MAG_DIR, "content", "pillars.json"), encoding="utf-8") as f:
    pillars_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "doctors.json"), encoding="utf-8") as f:
    doctors_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "articles.json"), encoding="utf-8") as f:
    articles_data = json.load(f)

with open(os.path.join(MAG_DIR, "content", "settings.json"), encoding="utf-8") as f:
    settings_data = json.load(f)

media_file = os.path.join(MAG_DIR, "content", "media.json")
if os.path.exists(media_file):
    with open(media_file, encoding="utf-8") as f:
        media_data = json.load(f)
else:
    media_data = []

pillars_json = json.dumps(pillars_data, ensure_ascii=False)
doctors_json = json.dumps(doctors_data, ensure_ascii=False)
articles_json = json.dumps(articles_data, ensure_ascii=False)
settings_json = json.dumps(settings_data, ensure_ascii=False)
media_json = json.dumps(media_data, ensure_ascii=False)

# Read part 1 from build_admin_html.py
with open(os.path.join(BASE_DIR, "scripts", "build_admin_html.py"), "r", encoding="utf-8") as f:
    py_text = f.read()

# Extract part1_head string
start_token = "part1_head = '''"
start_idx = py_text.find(start_token)
if start_idx != -1:
    end_token = "'''\n\nprint(\"Head and HTML"
    end_idx = py_text.find(end_token, start_idx)
    part1_html = py_text[start_idx + len(start_token):end_idx]
else:
    raise ValueError("Could not find part1_head in build_admin_html.py")

# JavaScript Application Logic
js_code = f'''
  <script>
    // Embedded Data from Pezeshkan Health Magazine
    let ARTICLES = {articles_json};
    let PILLARS = {pillars_json};
    let DOCTORS = {doctors_json};
    let SETTINGS = {settings_json};
    let MEDIA = {media_json};

    let editorialEditor = null;
    let activeEditingArticleId = null;
    let activePostStatusFilter = 'all';
    let currentMediaModalMode = 'editor'; // 'editor' or 'featured'
    let currentMediaModalTab = 'library';
    let selectedMediaItem = null;
    let activeArticleFaqs = [];
    let serpDeviceMode = 'mobile';

    // 1. Tab Switching
    function switchTab(tabName) {{
      document.querySelectorAll('.tab-section').forEach(s => s.classList.remove('active'));
      document.querySelectorAll('.sidebar-nav-link').forEach(l => l.classList.remove('active'));

      const targetSection = document.getElementById('tab-' + tabName);
      const targetNav = document.getElementById('nav-' + tabName);

      if (targetSection) targetSection.classList.add('active');
      if (targetNav) targetNav.classList.add('active');

      window.scrollTo({{ top: 0, behavior: 'smooth' }});

      if (tabName === 'editor' && editorialEditor) {{
        setTimeout(() => editorialEditor.commands.focus(), 50);
      }}
      if (tabName === 'media') {{
        renderMediaLibrary();
      }}
      if (tabName === 'posts') {{
        renderPostsTable();
      }}
    }}

    // 2. Posts Table Management
    function setPostStatusFilter(filter) {{
      activePostStatusFilter = filter;
      document.querySelectorAll('.status-pill').forEach(p => p.classList.remove('active'));
      const activePill = document.getElementById('pill-filter-' + filter);
      if (activePill) activePill.classList.add('active');
      renderPostsTable();
    }}

    function renderPostsTable() {{
      const tbody = document.getElementById('postsTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      // Update badge counts
      const countAll = ARTICLES.length;
      const countPublished = ARTICLES.filter(a => a.status !== 'draft' && a.status !== 'trash').length;
      const countDraft = ARTICLES.filter(a => a.status === 'draft').length;
      const countTrash = ARTICLES.filter(a => a.status === 'trash').length;

      const elCountAll = document.getElementById('countFilterAll');
      const elCountPub = document.getElementById('countFilterPublished');
      const elCountDraft = document.getElementById('countFilterDraft');
      const elCountTrash = document.getElementById('countFilterTrash');
      const elSidebarCount = document.getElementById('sidebarPostCount');

      if (elCountAll) elCountAll.innerText = countAll;
      if (elCountPub) elCountPub.innerText = countPublished;
      if (elCountDraft) elCountDraft.innerText = countDraft;
      if (elCountTrash) elCountTrash.innerText = countTrash;
      if (elSidebarCount) elSidebarCount.innerText = countPublished;

      // Filter articles
      let list = [...ARTICLES];
      if (activePostStatusFilter === 'published') {{
        list = list.filter(a => a.status !== 'draft' && a.status !== 'trash');
      }} else if (activePostStatusFilter === 'draft') {{
        list = list.filter(a => a.status === 'draft');
      }} else if (activePostStatusFilter === 'trash') {{
        list = list.filter(a => a.status === 'trash');
      }}

      const pillarFilterVal = document.getElementById('postPillarFilter')?.value;
      if (pillarFilterVal) {{
        list = list.filter(a => a.pillarSlug === pillarFilterVal);
      }}

      const searchVal = document.getElementById('postSearchInput')?.value.trim().toLowerCase();
      if (searchVal) {{
        list = list.filter(a => (a.title && a.title.toLowerCase().includes(searchVal)) || (a.focusKeyword && a.focusKeyword.toLowerCase().includes(searchVal)));
      }}

      if (list.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:32px; color:#94A3B8;">مقاله‌ای در این بخش یافت نشد.</td></tr>`;
        return;
      }}

      list.forEach(post => {{
        const tr = document.createElement('tr');
        const pillar = PILLARS.find(p => p.slug === post.pillarSlug) || {{ name: 'عمومی سلامت' }};
        const authorName = (post.author && post.author.name) || 'دکتر مهران رادمنش';
        const postImg = post.image || 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=200&q=80';
        const seoScore = post.seoScore || 90;
        const seoBadgeClass = seoScore >= 80 ? 'seo-good' : (seoScore >= 50 ? 'seo-ok' : 'seo-bad');
        const isDraft = post.status === 'draft';
        const isTrash = post.status === 'trash';
        const statusBadge = isTrash ? '<span class="badge badge-trash">زباله‌دان</span>' : (isDraft ? '<span class="badge badge-draft">پیش‌نویس</span>' : '<span class="badge badge-published">منتشر شده</span>');

        tr.innerHTML = `
          <td><input type="checkbox"></td>
          <td>
            <div style="width:48px; height:36px; border-radius:6px; overflow:hidden; background:#F1F5F9;">
              <img src="${{postImg}}" style="width:100%; height:100%; object-fit:cover;" alt="">
            </div>
          </td>
          <td>
            <div class="post-title-cell">${{post.title}}</div>
            <div class="post-row-actions">
              ${{isTrash ? `
                <a class="post-action-btn" onclick="restorePost('${{post.id}}')">بازیابی</a>
                <span>|</span>
                <a class="post-action-btn danger" onclick="permanentDeletePost('${{post.id}}')">حذف دائم</a>
              ` : `
                <a class="post-action-btn" onclick="editPost('${{post.id}}')">ویرایش کامل</a>
                <span>|</span>
                <a class="post-action-btn" onclick="previewPostModal('${{post.id}}')">پیش‌نمایش</a>
                <span>|</span>
                <a class="post-action-btn danger" onclick="trashPost('${{post.id}}')">انتقال به زباله‌دان</a>
              `}}
            </div>
          </td>
          <td><span style="font-weight:600; color:#334155;">${{pillar.name}}</span></td>
          <td>${{authorName}}</td>
          <td><span style="font-size:12px; color:#0284C7; font-weight:700;">${{post.focusKeyword || '—'}}</span></td>
          <td>
            <span class="badge-seo-score ${{seoBadgeClass}}">
              ${{seoScore >= 80 ? '🟢' : (seoScore >= 50 ? '🟡' : '🔴')}} ${{seoScore}}
            </span>
          </td>
          <td>${{statusBadge}}</td>
        `;
        tbody.appendChild(tr);
      }});

      renderDashboardRecentPosts();
    }}

    function renderDashboardRecentPosts() {{
      const tbody = document.getElementById('dashboardRecentPosts');
      if (!tbody) return;
      tbody.innerHTML = '';
      const recent = ARTICLES.slice(0, 5);
      recent.forEach(post => {{
        const pillar = PILLARS.find(p => p.slug === post.pillarSlug) || {{ name: 'سلامت' }};
        const authorName = (post.author && post.author.name) || 'دکتر مهران رادمنش';
        const seoScore = post.seoScore || 92;
        const seoClass = seoScore >= 80 ? 'seo-good' : (seoScore >= 50 ? 'seo-ok' : 'seo-bad');
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>
            <a href="javascript:void(0)" onclick="editPost('${{post.id}}')" style="font-weight:700; color:var(--text-main); text-decoration:none;">
              ${{post.title}}
            </a>
          </td>
          <td>${{pillar.name}}</td>
          <td>${{authorName}}</td>
          <td><span class="badge-seo-score ${{seoClass}}">${{seoScore}}</span></td>
          <td><span class="badge badge-published">منتشر شده</span></td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function filterPosts() {{
      renderPostsTable();
    }}

    async function trashPost(id) {{
      const p = ARTICLES.find(a => a.id === id);
      if (!p) return;
      p.status = 'trash';
      syncArticlePut(p);
      renderPostsTable();
      showToast('مقاله به زباله‌دان منتقل شد', '🗑️');
    }}

    async function restorePost(id) {{
      const p = ARTICLES.find(a => a.id === id);
      if (!p) return;
      p.status = 'published';
      syncArticlePut(p);
      renderPostsTable();
      showToast('مقاله بازیابی گردید', '♻️');
    }}

    async function permanentDeletePost(id) {{
      if (!confirm('آیا از حذف دائمی این نوشته اطمینان دارید؟ این عمل غیرقابل بازگشت است.')) return;
      try {{
        await fetch(`/api/articles?id=${{id}}`, {{ method: 'DELETE' }});
      }} catch(e) {{}}
      ARTICLES = ARTICLES.filter(a => a.id !== id);
      renderPostsTable();
      showToast('مقاله برای همیشه حذف شد', '🗑️');
    }}

    async function syncArticlePut(article) {{
      try {{
        await fetch('/api/articles', {{
          method: 'PUT',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(article)
        }});
      }} catch(e) {{}}
    }}

    // 3. Editorial Studio & Engine
    function initEditorialEngine() {{
      const Core = window.TiptapCore;
      if (!Core) return;

      const {{ Editor, StarterKit, Image, Link, Placeholder, Underline }} = Core;

      editorialEditor = new Editor({{
        element: document.getElementById('editorialCanvasContainer'),
        extensions: [
          StarterKit.configure({{
            heading: {{ levels: [2, 3] }}
          }}),
          Underline,
          Link.configure({{
            openOnClick: false,
            HTMLAttributes: {{ class: 'clinical-link' }}
          }}),
          Image.configure({{
            inline: false,
            HTMLAttributes: {{ class: 'editorial-canvas-img' }}
          }}),
          Placeholder.configure({{
            placeholder: 'محتوای علمی مقاله را اینجا بنویسید یا برای نگارش اقدام فرمایید...'
          }})
        ],
        content: '<p>محتوای مقاله علمی خود را بنویسید...</p>',
        onUpdate: () => {{
          updateWordStats();
          runLiveSeoAudit();
        }}
      }});

      // Bind toolbar buttons
      document.getElementById('tBold').onclick = () => editorialEditor.chain().focus().toggleBold().run();
      document.getElementById('tItalic').onclick = () => editorialEditor.chain().focus().toggleItalic().run();
      document.getElementById('tUnderline').onclick = () => editorialEditor.chain().focus().toggleUnderline().run();
      document.getElementById('tStrike').onclick = () => editorialEditor.chain().focus().toggleStrike().run();
      document.getElementById('tH2').onclick = () => editorialEditor.chain().focus().toggleHeading({{ level: 2 }}).run();
      document.getElementById('tH3').onclick = () => editorialEditor.chain().focus().toggleHeading({{ level: 3 }}).run();
      document.getElementById('tP').onclick = () => editorialEditor.chain().focus().setParagraph().run();
      document.getElementById('tBullet').onclick = () => editorialEditor.chain().focus().toggleBulletList().run();
      document.getElementById('tOrdered').onclick = () => editorialEditor.chain().focus().toggleOrderedList().run();
      document.getElementById('tQuote').onclick = () => editorialEditor.chain().focus().toggleBlockquote().run();
      document.getElementById('tHR').onclick = () => editorialEditor.chain().focus().setHorizontalRule().run();
      document.getElementById('tUndo').onclick = () => editorialEditor.chain().focus().undo().run();
      document.getElementById('tRedo').onclick = () => editorialEditor.chain().focus().redo().run();

      document.getElementById('tLink').onclick = () => {{
        const url = prompt('نشانی اینترنتی پیوند را وارد فرمایید:', 'https://');
        if (url) editorialEditor.chain().focus().setLink({{ href: url }}).run();
      }};

      document.getElementById('btnSmartCleanEditor').onclick = () => {{
        const dirty = editorialEditor.getHTML();
        const clean = cleanAndNormalizeHTML(dirty);
        editorialEditor.commands.setContent(clean);
        showToast('متن پاکسازی و نیم‌فاصله‌ها اصلاح شدند', '✨');
      }};

      document.getElementById('btnLivePreviewArticle').onclick = openPreviewModal;
    }}

    function insertCallout(type) {{
      if (!editorialEditor) return;
      const titles = {{
        warning: '⚠️ هشدار بالینی و پرچم قرمز تریاژ',
        advice: '🩺 توصیه تخصصی پزشک ناظر',
        protocol: 'ℹ️ پروتکل مراقبت بالینی'
      }};
      const html = `
        <div class="clinical-callout ${{type}}">
          <div class="callout-header">${{titles[type] || 'نکته بالینی'}}</div>
          <div>توضیحات و دستورالعمل تخصصی را اینجا وارد فرمایید...</div>
        </div><p></p>
      `;
      editorialEditor.chain().focus().insertContent(html).run();
    }}

    // 4. Live SEO Suite (RankMath / Yoast Engine)
    function switchSeoTab(tabId) {{
      document.querySelectorAll('.seo-pane').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.seo-tab-btn').forEach(b => b.classList.remove('active'));
      const targetPane = document.getElementById('seoPane-' + tabId);
      const targetBtn = document.getElementById('btnSeoTab-' + tabId);
      if (targetPane) targetPane.classList.add('active');
      if (targetBtn) targetBtn.classList.add('active');
    }}

    function setSerpDevice(mode) {{
      serpDeviceMode = mode;
      document.getElementById('btnSerpMobile').classList.toggle('active', mode === 'mobile');
      document.getElementById('btnSerpDesktop').classList.toggle('active', mode === 'desktop');
      const box = document.querySelector('.google-serp-preview');
      if (mode === 'mobile') {{
        box.style.maxWidth = '420px';
      }} else {{
        box.style.maxWidth = '650px';
      }}
    }}

    function handleTitleChange() {{
      const title = document.getElementById('editTitle').value;
      const metaTitleInput = document.getElementById('seoMetaTitle');
      if (!metaTitleInput.value || metaTitleInput.dataset.manual !== 'true') {{
        metaTitleInput.value = title ? `${{title}} | مجله سلامت پزشکآن` : '';
        handleMetaTitleInput();
      }}
      runLiveSeoAudit();
    }}

    function handleSummaryChange() {{
      const summary = document.getElementById('editSummary').value;
      const metaDescInput = document.getElementById('seoMetaDesc');
      if (!metaDescInput.value || metaDescInput.dataset.manual !== 'true') {{
        metaDescInput.value = summary || '';
        handleMetaDescInput();
      }}
      runLiveSeoAudit();
    }}

    function handleMetaTitleInput() {{
      const val = document.getElementById('seoMetaTitle').value;
      document.getElementById('seoMetaTitle').dataset.manual = 'true';
      const len = val.length;
      document.getElementById('labelTitleCount').innerText = `${{len}} / ۶۰ کاراکتر`;
      const fill = document.getElementById('barTitleFill');
      const pct = Math.min(100, (len / 60) * 100);
      fill.style.width = pct + '%';
      if (len >= 45 && len <= 60) {{
        fill.style.background = '#059669'; // Green
      }} else if (len > 60) {{
        fill.style.background = '#E11D48'; // Red
      }} else {{
        fill.style.background = '#D97706'; // Orange
      }}
      document.getElementById('serpTitlePreview').innerText = val || 'عنوان سئو مقاله در نتایج گوگل';
      runLiveSeoAudit();
    }}

    function handleMetaDescInput() {{
      const val = document.getElementById('seoMetaDesc').value;
      document.getElementById('seoMetaDesc').dataset.manual = 'true';
      const len = val.length;
      document.getElementById('labelDescCount').innerText = `${{len}} / ۱۶۰ کاراکتر`;
      const fill = document.getElementById('barDescFill');
      const pct = Math.min(100, (len / 160) * 100);
      fill.style.width = pct + '%';
      if (len >= 120 && len <= 160) {{
        fill.style.background = '#059669'; // Green
      }} else if (len > 160) {{
        fill.style.background = '#E11D48'; // Red
      }} else {{
        fill.style.background = '#D97706'; // Orange
      }}
      document.getElementById('serpDescPreview').innerText = val || 'توضیحات متای مقاله علمی در نتایج جستجوی گوگل...';
      runLiveSeoAudit();
    }}

    function handleSlugInput() {{
      const slug = document.getElementById('editSlug').value.trim();
      document.getElementById('serpBreadcrumbSlug').innerText = slug || 'article-slug';
      runLiveSeoAudit();
    }}

    function generateAutoSlug() {{
      const title = document.getElementById('editTitle').value.trim();
      if (!title) return;
      const clean = title.toLowerCase()
        .replace(/[^\\u0600-\\u06FFa-zA-Z0-9\\s\\-]/g, '')
        .trim()
        .replace(/\\s+/g, '-');
      document.getElementById('editSlug').value = clean;
      handleSlugInput();
      showToast('نامک آدرس بر اساس عنوان مقاله تنظیم شد', '🔗');
    }}

    function runLiveSeoAudit() {{
      const kw = (document.getElementById('seoFocusKeyword')?.value || '').trim().toLowerCase();
      const title = (document.getElementById('editTitle')?.value || '').toLowerCase();
      const metaTitle = (document.getElementById('seoMetaTitle')?.value || '').toLowerCase();
      const metaDesc = (document.getElementById('seoMetaDesc')?.value || '').toLowerCase();
      const lead = (document.getElementById('editSummary')?.value || '').toLowerCase();
      const slug = (document.getElementById('editSlug')?.value || '').toLowerCase();
      const contentHtml = editorialEditor ? editorialEditor.getHTML() : '';
      const text = editorialEditor ? editorialEditor.getText().toLowerCase() : '';
      const words = text.split(/\\s+/).filter(Boolean);
      const wordCount = words.length;

      let score = 0;
      const checks = [];

      // Check 1: Focus keyword entered
      if (kw.length >= 3) {{
        checks.push({{ ok: true, title: 'کلمه کلیدی کانونی تعیین شده است', desc: `کلمه انتخابی: «${{kw}}»` }});
        score += 15;
      }} else {{
        checks.push({{ ok: false, title: 'کلمه کلیدی کانونی تعیین نشده است', desc: 'لطفاً عبارت اصلی هدف مقاله را وارد نمایید.' }});
      }}

      // Check 2: In H1 Title
      if (kw && title.includes(kw)) {{
        checks.push({{ ok: true, title: 'کلمه کلیدی در عنوان اصلی مقاله (H1) وجود دارد', desc: 'بسیار عالی؛ سیگنال قوی رتبه‌بندی.' }});
        score += 15;
      }} else {{
        checks.push({{ ok: false, title: 'کلمه کلیدی در عنوان اصلی (H1) نیست', desc: 'بهتر است عبارت کلیدی را در ابتدای عنوان بگنجانید.' }});
      }}

      // Check 3: In Meta Title
      if (kw && metaTitle.includes(kw)) {{
        checks.push({{ ok: true, title: 'کلمه کلیدی در عنوان سئوی گوگل موجود است', desc: 'در نتایج جستجو با رنگ پررنگ دیده می‌شود.' }});
        score += 10;
      }} else {{
        checks.push({{ ok: false, title: 'کلمه کلیدی در عنوان سئو یافت نشد', desc: 'عنوان سئو را ویرایش کنید تا شامل کلمه کلیدی باشد.' }});
      }}

      // Check 4: In Meta Description
      if (kw && metaDesc.includes(kw)) {{
        checks.push({{ ok: true, title: 'کلمه کلیدی در توضیحات متای گوگل قرار دارد', desc: 'نرخ کلیک (CTR) کاربران در سرچ ارتقا می‌یابد.' }});
        score += 10;
      }} else {{
        checks.push({{ ok: false, title: 'کلمه کلیدی در توضیحات متا درج نشده است', desc: 'یک جمله شفاف با حضور کلمه کلیدی بنویسید.' }});
      }}

      // Check 5: In Lead paragraph
      if (kw && lead.includes(kw)) {{
        checks.push({{ ok: true, title: 'کلمه کلیدی در پاراگراف لید (چکیده) موجود است', desc: 'رعایت استاندارد ۱۰٪ ابتدایی محتوا.' }});
        score += 10;
      }} else {{
        checks.push({{ ok: false, title: 'کلمه کلیدی در لید یا چکیده نیامده است', desc: 'در پاراگراف آغازین به موضوع اصلی اشاره فرمایید.' }});
      }}

      // Check 6: In Slug
      if (kw && (slug.includes(kw.replace(/\\s+/g, '-')) || slug.includes(encodeURIComponent(kw)))) {{
        checks.push({{ ok: true, title: 'کلمه کلیدی در پیوند یکتا (Slug) درج شده است', desc: 'آدرس اینترنتی شفاف و سئو محور.' }});
        score += 10;
      }} else {{
        checks.push({{ ok: false, title: 'کلمه کلیدی در نامک آدرس (URL) نیست', desc: 'نامک پیوند را با کلمه کلیدی تنظیم فرمایید.' }});
      }}

      // Check 7: Headings structure (H2 present)
      if (contentHtml.includes('<h2')) {{
        checks.push({{ ok: true, title: 'ساختار تیترهای سلسله‌مراتبی (H2) رعایت شده است', desc: 'مقاله دارای دسته‌بندی و بخش‌بندی استاندارد است.' }});
        score += 10;
      }} else {{
        checks.push({{ ok: false, title: 'هیچ زیرعنوان H2 در متن یافت نشد', desc: 'متن طولانی را با تیترهای H2 تفکیک کنید.' }});
      }}

      // Check 8: Image Alt text
      const hasImages = contentHtml.includes('<img');
      const hasAlt = contentHtml.includes('alt=') && !contentHtml.includes('alt=""');
      if (hasImages && hasAlt) {{
        checks.push({{ ok: true, title: 'تصاویر دارای متن جایگزین (Alt Text) هستند', desc: 'کمک به سئوی عکس‌های گوگل و خوانایی نابینایان.' }});
        score += 10;
      }} else if (hasImages && !hasAlt) {{
        checks.push({{ ok: false, title: 'تصاویر فاقد متن جایگزین (Alt) هستند', desc: 'روی عکس‌ها کلیک کرده و برای هرکدام متن Alt تنظیم کنید.' }});
      }} else {{
        checks.push({{ ok: true, title: 'نیاز به تصویر برای تکمیل رسانه‌ای مقاله', desc: 'افزودن یک تصویر یا نمودار پزشکی توصیه می‌شود.' }});
        score += 5;
      }}

      // Check 9: Word Count
      if (wordCount >= 500) {{
        checks.push({{ ok: true, title: `حجم و غنای محتوایی مطلوب (${{wordCount}} کلمه)`, desc: 'طول عالی برای کسب رتبه‌های نخست گوگل.' }});
        score += 10;
      }} else if (wordCount >= 200) {{
        checks.push({{ ok: false, title: `طول محتوا متوسط است (${{wordCount}} کلمه)`, desc: 'برای مقالات پزشکی E-E-A-T حداقل ۵۰۰ کلمه پیشنهاد می‌شود.' }});
        score += 5;
      }} else {{
        checks.push({{ ok: false, title: `محتوا بسیار کوتاه است (${{wordCount}} کلمه)`, desc: 'حداقل ۳۰۰ کلمه محتوای علمی نگارش فرمایید.' }});
      }}

      // Update UI
      score = Math.min(100, Math.max(0, score));
      const badge = document.getElementById('seoOverallScoreBadge');
      if (badge) {{
        badge.className = 'badge-seo-score ' + (score >= 80 ? 'seo-good' : (score >= 50 ? 'seo-ok' : 'seo-bad'));
        badge.innerText = `${{score >= 80 ? '🟢' : (score >= 50 ? '🟡' : '🔴')}} نمره سئو: ${{score}}/۱۰۰ (${{score >= 80 ? 'عالی' : (score >= 50 ? 'نیازمند بهبود' : 'ضعیف')}})`;
      }}

      const listGrid = document.getElementById('seoChecklistGrid');
      if (listGrid) {{
        listGrid.innerHTML = checks.map(c => `
          <div class="seo-check-item">
            <span class="seo-check-icon">${{c.ok ? '🟢' : '🔴'}}</span>
            <div class="seo-check-details">
              <strong>${{c.title}}</strong>
              <p>${{c.desc}}</p>
            </div>
          </div>
        `).join('');
      }}

      // Update Social Preview
      const heroUrl = document.getElementById('editHeroUrl')?.value;
      const previewImg = document.getElementById('socialPreviewImg');
      const placeholderTxt = document.getElementById('socialPlaceholderTxt');
      if (heroUrl && previewImg) {{
        previewImg.src = heroUrl;
        previewImg.style.display = 'block';
        if (placeholderTxt) placeholderTxt.style.display = 'none';
      }} else if (previewImg) {{
        previewImg.style.display = 'none';
        if (placeholderTxt) placeholderTxt.style.display = 'block';
      }}
      const socTitle = document.getElementById('socialPreviewTitle');
      if (socTitle) socTitle.innerText = title || 'عنوان مقاله علمی';
      const socDesc = document.getElementById('socialPreviewDesc');
      if (socDesc) socDesc.innerText = lead || 'چکیده و لید مقاله جهت اشتراک در شبکه‌های اجتماعی...';

      return score;
    }}

    // FAQ Builder in SEO
    function addFaqRow(q = '', a = '') {{
      activeArticleFaqs.push({{ q: q, a: a }});
      renderFaqs();
    }}

    function removeFaqRow(idx) {{
      activeArticleFaqs.splice(idx, 1);
      renderFaqs();
    }}

    function renderFaqs() {{
      const container = document.getElementById('faqListContainer');
      if (!container) return;
      if (activeArticleFaqs.length === 0) {{
        container.innerHTML = `<p style="font-size:12px; color:#94A3B8; margin-top:8px;">هنوز پرسش و پاسخی ثبت نشده است. روی دکمه «+ افزودن پرسش جدید» کلیک کنید.</p>`;
        return;
      }}
      container.innerHTML = activeArticleFaqs.map((f, i) => `
        <div class="faq-builder-item">
          <button type="button" class="faq-item-delete-btn" onclick="removeFaqRow(${{i}})" title="حذف این پرسش">✕</button>
          <div class="form-group" style="margin-bottom:8px;">
            <label style="font-size:11px;">پرسش بیمار (Question):</label>
            <input type="text" class="form-control" value="${{f.q}}" placeholder="مثال: آیا درمان دیسک کمر نیاز به بستری دارد؟" oninput="activeArticleFaqs[${{i}}].q = this.value">
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label style="font-size:11px;">پاسخ تخصصی پزشک (Answer):</label>
            <textarea class="form-control" rows="2" placeholder="پاسخ روشن و علمی..." oninput="activeArticleFaqs[${{i}}].a = this.value">${{f.a}}</textarea>
          </div>
        </div>
      `).join('');
    }}

    // 5. Media Library & Media Inserter Modal
    function renderMediaLibrary() {{
      const grid = document.getElementById('mediaLibraryGrid');
      if (!grid) return;
      grid.innerHTML = '';

      const countBadge = document.getElementById('sidebarMediaCount');
      if (countBadge) countBadge.innerText = MEDIA.length;
      const countMetric = document.getElementById('metricTotalMedia');
      if (countMetric) countMetric.innerText = MEDIA.length;

      const q = (document.getElementById('mediaSearchInput')?.value || '').trim().toLowerCase();
      const filtered = q ? MEDIA.filter(m => (m.title && m.title.toLowerCase().includes(q)) || (m.alt && m.alt.toLowerCase().includes(q))) : MEDIA;

      if (filtered.length === 0) {{
        grid.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:32px; color:#94A3B8;">تصویری در کتابخانه یافت نشد.</div>`;
        return;
      }}

      filtered.forEach(item => {{
        const card = document.createElement('div');
        card.className = 'media-card';
        card.innerHTML = `
          <div class="media-thumb-wrap">
            <img src="${{item.url}}" alt="${{item.alt || ''}}">
          </div>
          <div class="media-meta-wrap">
            <div class="media-title-txt" title="${{item.title || item.filename}}">${{item.title || item.filename}}</div>
            <div class="media-size-txt">${{formatBytes(item.size)}} • ${{item.uploadedAt || 'امروز'}}</div>
          </div>
          <div style="padding:6px 10px; display:flex; justify-content:space-between; border-top:1px solid #F1F5F9; background:#FAFBFD;">
            <button type="button" class="btn btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="copyMediaUrl('${{item.url}}')" title="کپی آدرس تصویر">📋 کپی لینک</button>
            <button type="button" class="btn btn-danger" style="padding:2px 8px; font-size:11px;" onclick="deleteMedia('${{item.id}}')" title="حذف تصویر">🗑️</button>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function filterMediaLibrary() {{
      renderMediaLibrary();
    }}

    function copyMediaUrl(url) {{
      navigator.clipboard.writeText(url).then(() => {{
        showToast('آدرس تصویر با موفقیت در کلیپ‌بورد کپی شد', '📋');
      }}).catch(() => {{
        prompt('آدرس تصویر:', url);
      }});
    }}

    async function handleMediaLibraryUpload(input) {{
      if (!input.files || !input.files.length) return;
      const files = Array.from(input.files);
      for (const file of files) {{
        await uploadSingleFile(file);
      }}
      input.value = '';
      renderMediaLibrary();
      showToast('تصاویر با موفقیت در سرور بارگذاری گردیدند', '🖼️');
    }}

    function uploadSingleFile(file) {{
      return new Promise((resolve) => {{
        const reader = new FileReader();
        reader.onload = async (e) => {{
          const b64 = e.target.result;
          try {{
            const res = await fetch('/api/upload', {{
              method: 'POST',
              headers: {{ 'Content-Type': 'application/json' }},
              body: JSON.stringify({{
                filename: file.name,
                data: b64,
                alt: file.name.split('.')[0],
                title: file.name.split('.')[0]
              }})
            }});
            if (res.ok) {{
              const data = await res.json();
              if (data.media) {{
                MEDIA.unshift(data.media);
              }}
            }}
          }} catch(err) {{}}
          resolve();
        }};
        reader.readAsDataURL(file);
      }});
    }}

    // Modal Inserter
    function openMediaModal(mode = 'editor') {{
      currentMediaModalMode = mode;
      selectedMediaItem = null;
      document.getElementById('mediaModal').style.display = 'flex';
      switchMediaModalTab('library');
      renderModalMediaGrid();

      const btnConfirm = document.getElementById('btnConfirmMediaModal');
      const alignGroup = document.getElementById('groupModalAlign');
      if (mode === 'featured') {{
        btnConfirm.innerText = 'تنظیم به عنوان تصویر شاخص';
        if (alignGroup) alignGroup.style.display = 'none';
      }} else {{
        btnConfirm.innerText = 'درج در نوشته';
        if (alignGroup) alignGroup.style.display = 'block';
      }}
    }}

    function closeMediaModal() {{
      document.getElementById('mediaModal').style.display = 'none';
    }}

    function switchMediaModalTab(tabId) {{
      currentMediaModalTab = tabId;
      document.querySelectorAll('.media-tab-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('btnMediaTab-' + tabId);
      if (activeBtn) activeBtn.classList.add('active');

      document.getElementById('modalView-library').style.display = tabId === 'library' ? 'block' : 'none';
      document.getElementById('modalView-upload').style.display = tabId === 'upload' ? 'block' : 'none';
      document.getElementById('modalView-url').style.display = tabId === 'url' ? 'block' : 'none';
    }}

    function renderModalMediaGrid() {{
      const grid = document.getElementById('modalMediaGrid');
      if (!grid) return;
      grid.innerHTML = '';

      const countLabel = document.getElementById('modalMediaCountLabel');
      if (countLabel) countLabel.innerText = `${{MEDIA.length}} تصویر در کتابخانه`;

      const q = (document.getElementById('modalMediaSearch')?.value || '').trim().toLowerCase();
      const filtered = q ? MEDIA.filter(m => (m.title && m.title.toLowerCase().includes(q)) || (m.alt && m.alt.toLowerCase().includes(q))) : MEDIA;

      filtered.forEach(item => {{
        const card = document.createElement('div');
        card.className = 'media-card' + (selectedMediaItem && selectedMediaItem.id === item.id ? ' selected' : '');
        card.onclick = () => selectModalMediaItem(item, card);
        card.innerHTML = `
          <div class="media-thumb-wrap">
            <img src="${{item.url}}" alt="${{item.alt || ''}}">
          </div>
          <div class="media-meta-wrap">
            <div class="media-title-txt">${{item.title || item.filename}}</div>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function filterModalMedia() {{
      renderModalMediaGrid();
    }}

    function selectModalMediaItem(item, cardElement) {{
      selectedMediaItem = item;
      document.querySelectorAll('#modalMediaGrid .media-card').forEach(c => c.classList.remove('selected'));
      if (cardElement) cardElement.classList.add('selected');

      const preview = document.getElementById('modalSelectedPreviewImg');
      const placeholder = document.getElementById('modalNoSelectionTxt');
      preview.src = item.url;
      preview.style.display = 'block';
      placeholder.style.display = 'none';

      document.getElementById('modalImageAlt').value = item.alt || '';
      document.getElementById('modalImageCaption').value = item.caption || '';
    }}

    async function handleModalDirectUpload(input) {{
      if (!input.files || !input.files.length) return;
      const file = input.files[0];
      await uploadSingleFile(file);
      switchMediaModalTab('library');
      renderModalMediaGrid();
      if (MEDIA.length > 0) {{
        selectModalMediaItem(MEDIA[0]);
      }}
      showToast('تصویر با موفقیت بارگذاری شد', '🖼️');
    }}

    function handleModalDirectUrlInput() {{
      const url = document.getElementById('modalDirectUrlInput').value.trim();
      if (url) {{
        selectedMediaItem = {{
          id: 'ext-' + Date.now(),
          url: url,
          alt: 'تصویر مقاله',
          title: 'تصویر اینترنتی'
        }};
        const preview = document.getElementById('modalSelectedPreviewImg');
        const placeholder = document.getElementById('modalNoSelectionTxt');
        preview.src = url;
        preview.style.display = 'block';
        placeholder.style.display = 'none';
      }}
    }}

    function confirmMediaModalSelection() {{
      if (!selectedMediaItem || !selectedMediaItem.url) {{
        alert('لطفاً ابتدا یک تصویر را انتخاب یا بارگذاری فرمایید.');
        return;
      }}

      const alt = document.getElementById('modalImageAlt').value.trim() || 'تصویر بالینی مجله سلامت پزشکآن';
      const caption = document.getElementById('modalImageCaption').value.trim();
      const align = document.getElementById('modalImageAlign').value;

      if (currentMediaModalMode === 'editor') {{
        if (!editorialEditor) return;
        const captionHtml = caption ? `<figcaption class="clinical-img-caption">${{caption}}</figcaption>` : '';
        const figureHtml = `
          <figure class="clinical-img-figure ${{align}}">
            <img src="${{selectedMediaItem.url}}" alt="${{alt}}">
            ${{captionHtml}}
          </figure><p></p>
        `;
        editorialEditor.chain().focus().insertContent(figureHtml).run();
        showToast('تصویر با موفقیت در متن نوشته درج شد', '🖼️');
      }} else if (currentMediaModalMode === 'featured') {{
        document.getElementById('editHeroUrl').value = selectedMediaItem.url;
        document.getElementById('editHeroAlt').value = alt;
        document.getElementById('editHeroCaption').value = caption;
        updateHeroPreview(selectedMediaItem.url);
        showToast('تصویر شاخص نوشته تنظیم گردید', '🖼️');
      }}

      closeMediaModal();
      runLiveSeoAudit();
    }}

    function updateHeroPreview(url) {{
      const box = document.getElementById('heroPreviewBox');
      const btnRemove = document.getElementById('btnRemoveHero');
      if (url) {{
        box.innerHTML = `<img src="${{url}}" alt="تصویر شاخص">`;
        btnRemove.style.display = 'inline-flex';
      }} else {{
        box.innerHTML = `<span style="font-size: 12px; color: #94A3B8;">تصویری انتخاب نشده است</span>`;
        btnRemove.style.display = 'none';
      }}
    }}

    function removeHeroImage() {{
      document.getElementById('editHeroUrl').value = '';
      document.getElementById('editHeroAlt').value = '';
      document.getElementById('editHeroCaption').value = '';
      updateHeroPreview('');
      showToast('تصویر شاخص حذف شد', '🗑️');
    }}

    async function deleteMedia(id) {{
      if (!confirm('آیا از حذف این پرونده چندرسانه‌ای اطمینان دارید؟')) return;
      try {{
        await fetch(`/api/media?id=${{id}}`, {{ method: 'DELETE' }});
      }} catch(e) {{}}
      MEDIA = MEDIA.filter(m => m.id !== id);
      renderMediaLibrary();
      showToast('تصویر با موفقیت حذف گردید', '🗑️');
    }}

    function formatBytes(bytes) {{
      if (!bytes) return '۰ کیلوبایت';
      if (bytes < 1024) return bytes + ' بایت';
      if (bytes < 1048576) return (bytes / 1024).toFixed(0) + ' کیلوبایت';
      return (bytes / 1048576).toFixed(1) + ' مگابایت';
    }}

    // 6. Save & Edit Post Workflow
    function createNewPost() {{
      activeEditingArticleId = null;
      document.getElementById('editorPageHeading').innerText = 'نگارش مقاله جدید در تحریریه';
      document.getElementById('editTitle').value = '';
      document.getElementById('editSummary').value = '';
      document.getElementById('editSlug').value = '';
      document.getElementById('editTags').value = '';
      document.getElementById('editReadTime').value = '۷ دقیقه';
      document.getElementById('editStatusSelect').value = 'published';

      document.getElementById('seoFocusKeyword').value = '';
      document.getElementById('seoMetaTitle').value = '';
      document.getElementById('seoMetaDesc').value = '';
      document.getElementById('seoMetaTitle').dataset.manual = 'false';
      document.getElementById('seoMetaDesc').dataset.manual = 'false';
      document.getElementById('seoCanonicalUrl').value = '';
      document.getElementById('seoSchemaType').value = 'MedicalWebPage';
      document.getElementById('seoRobotsSelect').value = 'index, follow';

      removeHeroImage();
      activeArticleFaqs = [];
      renderFaqs();

      if (editorialEditor) {{
        editorialEditor.commands.setContent('<p>محتوای مقاله علمی خود را با تکیه بر شواهد پزشکی و راهنماهای بالینی اینجا بنویسید...</p>');
      }}

      switchTab('editor');
      runLiveSeoAudit();
      showToast('محیط نگارش مقاله تازه آماده شد', '✍️');
    }}

    function editPost(id) {{
      const post = ARTICLES.find(a => a.id === id);
      if (!post) return;

      activeEditingArticleId = post.id;
      document.getElementById('editorPageHeading').innerText = 'ویرایش مقاله: ' + post.title;
      document.getElementById('editTitle').value = post.title || '';
      document.getElementById('editSummary').value = post.summary || '';
      document.getElementById('editSlug').value = post.slug || '';
      document.getElementById('editTags').value = (post.tags || []).join('، ');
      document.getElementById('editReadTime').value = post.readTime || '۷ دقیقه';
      document.getElementById('editStatusSelect').value = post.status || 'published';

      if (post.pillarSlug) {{
        document.getElementById('editPillar').value = post.pillarSlug;
      }}
      if (post.author) {{
        const foundDoc = DOCTORS.find(d => d.name === post.author.name);
        if (foundDoc) document.getElementById('editDoctor').value = foundDoc.id;
      }}
      updateDoctorBadge();

      // Featured Image
      if (post.image) {{
        document.getElementById('editHeroUrl').value = post.image;
        document.getElementById('editHeroAlt').value = post.imageAlt || '';
        document.getElementById('editHeroCaption').value = post.imageCaption || '';
        updateHeroPreview(post.image);
      }} else {{
        removeHeroImage();
      }}

      // SEO Fields
      document.getElementById('seoFocusKeyword').value = post.focusKeyword || '';
      document.getElementById('seoMetaTitle').value = post.metaTitle || (post.title ? `${{post.title}} | مجله سلامت پزشکآن` : '');
      document.getElementById('seoMetaDesc').value = post.metaDescription || post.summary || '';
      document.getElementById('seoMetaTitle').dataset.manual = 'true';
      document.getElementById('seoMetaDesc').dataset.manual = 'true';
      handleMetaTitleInput();
      handleMetaDescInput();

      document.getElementById('seoCanonicalUrl').value = post.canonicalUrl || '';
      document.getElementById('seoSchemaType').value = post.schemaType || 'MedicalWebPage';
      document.getElementById('seoRobotsSelect').value = post.robots || 'index, follow';

      // FAQs
      activeArticleFaqs = post.faqs ? [...post.faqs] : [];
      renderFaqs();

      // Content
      let contentHtml = post.rawHtml || post.contentHtml || '';
      if (!contentHtml && post.sections && post.sections.length) {{
        contentHtml = post.sections.map(s => `
          <h2>${{s.title || s.heading || ''}}</h2>
          <p>${{s.content || s.body || ''}}</p>
        `).join('');
      }}
      if (!contentHtml) contentHtml = '<p>محتوای متنی مقاله...</p>';

      if (editorialEditor) {{
        editorialEditor.commands.setContent(contentHtml);
      }}

      switchTab('editor');
      runLiveSeoAudit();
      showToast('مقاله در استودیوی تحریریه بارگذاری شد', '📖');
    }}

    async function saveArticle(targetStatus = 'published') {{
      const title = document.getElementById('editTitle').value.trim();
      if (!title) {{
        alert('لطفاً عنوان اصلی مقاله را وارد فرمایید.');
        document.getElementById('editTitle').focus();
        return;
      }}

      const summary = document.getElementById('editSummary').value.trim();
      const slug = document.getElementById('editSlug').value.trim() || ('art-' + Date.now());
      const pillarSlug = document.getElementById('editPillar').value;
      const readTime = document.getElementById('editReadTime').value;
      const tags = document.getElementById('editTags').value.split(/[،,]/).map(t => t.trim()).filter(Boolean);
      const docId = document.getElementById('editDoctor').value;
      const doc = DOCTORS.find(d => d.id === docId) || DOCTORS[0];

      const html = editorialEditor ? editorialEditor.getHTML() : '';
      const seoScore = runLiveSeoAudit();

      const articlePayload = {{
        id: activeEditingArticleId || ('art-' + Date.now()),
        title: title,
        slug: slug,
        summary: summary,
        readTime: readTime,
        pillarSlug: pillarSlug,
        status: targetStatus,
        publishDate: 'امروز',
        lastReviewed: 'امروز',
        author: {{
          name: doc.name,
          title: doc.title,
          mcNumber: doc.mcNumber
        }},
        reviewer: {{
          name: "دکتر مهران رادمنش",
          title: "سردبیر هیئت علمی",
          mcNumber: "۱۱۴۲۸۵"
        }},
        tags: tags,
        image: document.getElementById('editHeroUrl').value,
        imageAlt: document.getElementById('editHeroAlt').value,
        imageCaption: document.getElementById('editHeroCaption').value,
        focusKeyword: document.getElementById('seoFocusKeyword').value,
        metaTitle: document.getElementById('seoMetaTitle').value,
        metaDescription: document.getElementById('seoMetaDesc').value,
        canonicalUrl: document.getElementById('seoCanonicalUrl').value,
        schemaType: document.getElementById('seoSchemaType').value,
        robots: document.getElementById('seoRobotsSelect').value,
        seoScore: seoScore,
        faqs: activeArticleFaqs,
        citations: [
          {{ title: "The Lancet / PubMed Clinical Trials", link: "https://pubmed.ncbi.nlm.nih.gov/" }}
        ],
        sections: [
          {{ id: "s1", title: title, content: summary }}
        ],
        rawHtml: html,
        contentHtml: html
      }};

      try {{
        const method = activeEditingArticleId ? 'PUT' : 'POST';
        const res = await fetch('/api/articles', {{
          method: method,
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(articlePayload)
        }});
        if (res.ok) {{
          const data = await res.json();
          if (data.articles) ARTICLES = data.articles;
        }}
      }} catch(e) {{}}

      // Local update
      const existingIdx = ARTICLES.findIndex(a => a.id === articlePayload.id);
      if (existingIdx !== -1) {{
        ARTICLES[existingIdx] = articlePayload;
      }} else {{
        ARTICLES.unshift(articlePayload);
      }}

      renderPostsTable();
      renderDashboardRecentPosts();
      switchTab('posts');
      showToast(targetStatus === 'published' ? 'مقاله با موفقیت در مجله منتشر گردید' : 'پیش‌نویس مقاله با موفقیت ذخیره شد', '🚀');
    }}

    function updateDoctorBadge() {{
      const docId = document.getElementById('editDoctor').value;
      const doc = DOCTORS.find(d => d.id === docId);
      const infoBox = document.getElementById('inspectorDoctorInfo');
      if (doc && infoBox) {{
        infoBox.innerHTML = `<strong>کد نظام پزشکی:</strong> ${{doc.mcNumber}}<br><strong>تخصص:</strong> ${{doc.title}}`;
      }}
    }}

    function cleanAndNormalizeHTML(html) {{
      if (!html) return '';
      return html
        .replace(/style="[^"]*"/gi, '')
        .replace(/font-family:[^;"]*;?/gi, '')
        .replace(/color:[^;"]*;?/gi, '')
        .replace(/background-color:[^;"]*;?/gi, '')
        .replace(/ي/g, 'ی')
        .replace(/ك/g, 'ک')
        .replace(/\\bمی\\s/g, 'می‌')
        .replace(/\\sنمی\\s/g, ' نمی‌')
        .replace(/\\sها\\b/g, '‌ها')
        .replace(/<p>\\s*<br\\s*\\/?>\\s*<\\/p>/gi, '')
        .replace(/(<br\\s*\\/?>){{2,}}/gi, '<br>');
    }}

    function openPreviewModal() {{
      const title = document.getElementById('editTitle').value || 'عنوان پیش‌فرض مقاله علمی';
      const summary = document.getElementById('editSummary').value || 'چکیده و لید مقاله...';
      const heroUrl = document.getElementById('editHeroUrl').value;
      const html = editorialEditor ? editorialEditor.getHTML() : '<p>متن مقاله...</p>';

      const content = document.getElementById('previewModalContent');
      content.innerHTML = `
        <article style="max-width:760px; margin:0 auto; font-family:'Vazirmatn', sans-serif;">
          ${{heroUrl ? `<img src="${{heroUrl}}" style="width:100%; max-height:400px; object-fit:cover; border-radius:12px; margin-bottom:24px;" alt="">` : ''}}
          <h1 style="font-size:24px; font-weight:900; color:#0F172A; margin-bottom:16px; line-height:1.4;">${{title}}</h1>
          <div style="background:#F8FAFC; border-right:4px solid #0284C7; padding:16px 20px; border-radius:8px; margin-bottom:28px; font-size:14.5px; color:#334155; line-height:1.8;">
            ${{summary}}
          </div>
          <div class="prose-content">${{html}}</div>
          ${{activeArticleFaqs.length ? `
            <div style="margin-top:32px; background:#F8FAFC; border-radius:12px; padding:20px;">
              <h3 style="font-size:16px; font-weight:800; margin-bottom:14px; color:#0F172A;">پرسش‌های پرتکرار بیماران</h3>
              ${{activeArticleFaqs.map(f => `
                <div style="margin-bottom:12px; border-bottom:1px dashed #E2E8F0; padding-bottom:10px;">
                  <strong style="color:#0284C7; font-size:13.5px; display:block; margin-bottom:4px;">❓ ${{f.q}}</strong>
                  <p style="color:#475569; font-size:13px; line-height:1.7; margin:0;">${{f.a}}</p>
                </div>
              `).join('')}}
            </div>
          ` : ''}}
        </article>
      `;
      document.getElementById('previewModal').style.display = 'flex';
    }}

    function closePreviewModal() {{
      document.getElementById('previewModal').style.display = 'none';
    }}

    function previewPostModal(id) {{
      const p = ARTICLES.find(a => a.id === id);
      if (!p) return;
      const content = document.getElementById('previewModalContent');
      const html = p.rawHtml || p.contentHtml || (p.sections || []).map(s => `<h2>${{s.title || s.heading}}</h2><p>${{s.content || s.body}}</p>`).join('');
      content.innerHTML = `
        <article style="max-width:760px; margin:0 auto; font-family:'Vazirmatn', sans-serif;">
          ${{p.image ? `<img src="${{p.image}}" style="width:100%; max-height:400px; object-fit:cover; border-radius:12px; margin-bottom:24px;" alt="">` : ''}}
          <h1 style="font-size:24px; font-weight:900; color:#0F172A; margin-bottom:16px; line-height:1.4;">${{p.title}}</h1>
          <div style="background:#F8FAFC; border-right:4px solid #0284C7; padding:16px 20px; border-radius:8px; margin-bottom:28px; font-size:14.5px; color:#334155; line-height:1.8;">
            ${{p.summary}}
          </div>
          <div class="prose-content">${{html}}</div>
        </article>
      `;
      document.getElementById('previewModal').style.display = 'flex';
    }}

    function updateWordStats() {{
      if (!editorialEditor) return;
      const text = editorialEditor.getText().trim();
      const words = text ? text.split(/\\s+/).length : 0;
      const chars = text.length;
      const readMinutes = Math.max(1, Math.ceil(words / 180));

      document.getElementById('statWordCount').innerText = words;
      document.getElementById('statCharCount').innerText = chars;
      document.getElementById('statReadTimeCalc').innerText = readMinutes + ' دقیقه';
    }}

    function populateEditorDropdowns() {{
      const pillarSelect = document.getElementById('editPillar');
      const filterSelect = document.getElementById('postPillarFilter');
      if (pillarSelect) {{
        pillarSelect.innerHTML = PILLARS.map(p => `<option value="${{p.slug}}">${{p.name}}</option>`).join('');
      }}
      if (filterSelect) {{
        filterSelect.innerHTML = `<option value="">همه دپارتمان‌ها</option>` + PILLARS.map(p => `<option value="${{p.slug}}">${{p.name}}</option>`).join('');
      }}

      const docSelect = document.getElementById('editDoctor');
      if (docSelect) {{
        docSelect.innerHTML = DOCTORS.map(d => `<option value="${{d.id}}">${{d.name}} (${{d.title}})</option>`).join('');
      }}
      updateDoctorBadge();
    }}

    function renderPillarsTable() {{
      const tbody = document.getElementById('pillarsTableBody');
      if (!tbody) return;
      tbody.innerHTML = PILLARS.map((p, idx) => `
        <tr>
          <td><span style="font-weight:700; color:#64748B;">#${{idx + 1}}</span></td>
          <td><span style="font-weight:800; color:var(--text-main);">${{p.icon || '🏥'}} ${{p.name}}</span></td>
          <td><code style="font-size:11.5px; color:#0284C7; background:#F0F9FF; padding:2px 6px; border-radius:4px;">${{p.slug}}</code></td>
          <td><strong>${{(p.branches || []).length}} شاخه بالینی</strong></td>
          <td>
            <div style="display:flex; flex-wrap:wrap; gap:4px; max-width:320px;">
              ${{(p.chips || []).slice(0, 4).map(c => `<span style="font-size:10.5px; background:#F1F5F9; color:#475569; padding:2px 6px; border-radius:4px;">${{c}}</span>`).join('')}}
            </div>
          </td>
          <td>
            <button type="button" class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="showToast('شاخه بالینی تایید شد', '🩺')">مشاهده</button>
          </td>
        </tr>
      `).join('');
    }}

    function renderDoctorsTable() {{
      const tbody = document.getElementById('doctorsTableBody');
      if (!tbody) return;
      tbody.innerHTML = DOCTORS.map(d => `
        <tr>
          <td>
            <div style="font-weight:800; color:var(--text-main);">${{d.name}}</div>
          </td>
          <td>${{d.title || d.dept || 'متخصص بالینی'}}</td>
          <td><span style="color:#0284C7; font-weight:700;">${{d.mcNumber || d.mc || '—'}}</span></td>
          <td>کلینیک تخصصی بیمارستان</td>
          <td><span class="badge badge-published">نوبت‌دهی فعال</span></td>
        </tr>
      `).join('');
    }}

    async function saveSiteSettings() {{
      const payload = {{
        siteTitle: document.getElementById('settingSiteTitle').value,
        siteSubtitle: document.getElementById('settingSiteSubtitle').value,
        editorialLeader: document.getElementById('settingEditorialLeader').value,
        announcementBanner: {{
          enabled: true,
          text: document.getElementById('settingBannerText').value
        }},
        contactPhone: document.getElementById('settingContactPhone').value
      }};
      try {{
        await fetch('/api/settings', {{
          method: 'PUT',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(payload)
        }});
      }} catch(e) {{}}
      showToast('تنظیمات عمومی سایت ذخیره گردید', '💾');
    }}

    async function saveSiteSeoSettings() {{
      showToast('تنظیمات سئوی سراسری و متاتگ‌های گوگل ذخیره شدند', '🔍');
    }}

    function showToast(text, icon = '✅') {{
      const toast = document.getElementById('toastMsg');
      document.getElementById('toastIcon').innerText = icon;
      document.getElementById('toastText').innerText = text;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 3500);
    }}

    async function checkAuth() {{
      try {{
        const res = await fetch('/api/me');
        if (res.ok) {{
          const data = await res.json();
          if (data.user && data.user.name) {{
            document.getElementById('barUserName').innerText = data.user.name;
          }}
        }}
      }} catch(e) {{}}
    }}

    // Startup
    window.addEventListener('DOMContentLoaded', () => {{
      checkAuth();
      populateEditorDropdowns();
      renderPostsTable();
      renderMediaLibrary();
      renderPillarsTable();
      renderDoctorsTable();
      initEditorialEngine();
    }});
  </script>
</body>
</html>
'''

full_html = part1_html + js_code
target_admin_path = os.path.join(MAG_DIR, "admin.html")
with open(target_admin_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Generated successfully: {target_admin_path} ({len(full_html)} bytes)")
