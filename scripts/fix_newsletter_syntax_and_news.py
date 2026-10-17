# -*- coding: utf-8 -*-
"""
Fix missing closing brace on closeEditionModal and restore loadLatestNews,
renderNewsCards, renderFallbackNews in mag/newsletter.html.
"""
import os
import subprocess

NEWSLETTER_HTML = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mag", "newsletter.html")

with open(NEWSLETTER_HTML, "r", encoding="utf-8") as f:
    content = f.read()

target = """    function closeEditionModal(e) {
      if (e && e.target && e.target !== document.getElementById('editionModal') && !e.target.classList.contains('edition-modal-close') && !e.target.closest('.edition-modal-close')) {
        return;
      }
      const modal = document.getElementById('editionModal');
      if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }"""

replacement = """    function closeEditionModal(e) {
      if (e && e.target && e.target !== document.getElementById('editionModal') && !e.target.classList.contains('edition-modal-close') && !e.target.closest('.edition-modal-close')) {
        return;
      }
      const modal = document.getElementById('editionModal');
      if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
      }
    }

    // بارگذاری تازه‌ترین اخبار و مقالات مجله سلامت
    async function loadLatestNews() {
      const container = document.getElementById('latestNewsCardsGrid');
      if (!container) return;

      try {
        const res = await fetch('/api/articles');
        if (res.ok) {
          const articles = await res.json();
          if (Array.isArray(articles) && articles.length > 0) {
            const published = articles.filter(a => a.status === 'published' || !a.status).slice(0, 4);
            renderNewsCards(published);
            return;
          }
        }
      } catch (err) {
        console.warn('Could not load dynamic articles, loading fallback news:', err);
      }

      renderFallbackNews();
    }

    function renderNewsCards(articles) {
      const container = document.getElementById('latestNewsCardsGrid');
      if (!container || !articles.length) return;

      container.innerHTML = articles.map(art => {
        const excerpt = art.lead || art.excerpt || art.summary || (art.content ? art.content.replace(/<[^>]*>?/gm, '').substring(0, 115) + '...' : 'توضیحات و تحلیل‌های جامع بالینی این مقاله در مجله سلامت پزشکآن...');
        const image = art.heroImage || art.image || 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=700&q=80';
        const docName = 'تیم متخصص محتوا نویس پزشکآن';
        const category = art.category || art.categoryName || 'خبر سلامت';
        const readTime = art.readTime || '۵ دقیقه';
        const slug = art.slug || art.id;

        return `
          <div class="medical-news-card">
            <div class="medical-news-thumb-wrap">
              <img src="${image}" alt="${art.title}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=700&q=80'">
              <span class="news-badge-overlay">${category}</span>
            </div>
            <div class="medical-news-content">
              <a href="/mag/${encodeURIComponent(slug)}" style="text-decoration:none;">
                <h3 class="medical-news-title">${art.title}</h3>
              </a>
              <p class="medical-news-desc">${excerpt}</p>
              <div class="medical-news-meta">
                <div class="news-author-mini">
                  <div class="news-author-avatar">✍️</div>
                  <span>${docName}</span>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="font-size:11px; color:var(--text-muted);">${readTime}</span>
                  <a href="/mag/${encodeURIComponent(slug)}" class="btn-ui btn-subtle-outline" style="font-size:11.5px; padding:5px 10px;">
                    <span>مطالعه خبر</span> ↗
                  </a>
                </div>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderFallbackNews() {
      const container = document.getElementById('latestNewsCardsGrid');
      if (!container) return;
      const fallbackItems = [
        {
          title: "تایید پروتکل جدید درمان غیرجراحی فتق دیسک در کنگره ستون فقرات ۲۰۲۶",
          lead: "نتایج کلینیکی ارزیابی ۳۰۰۰ بیمار نشان می‌دهد ترکیب لیزر پرتوان و فیزیوتراپی تخصصی نرخ نیاز به جراحی باز را تا ۷۳ درصد کاهش می‌دهد.",
          category: "ارتوپدی و ستون فقرات",
          author: "تیم متخصص محتوا نویس پزشکآن",
          readTime: "۴ دقیقه مطالعه",
          image: "https://images.unsplash.com/photo-1551076805-e1869033e561?auto=format&fit=crop&w=700&q=80",
          slug: "lumbar-disc-herniation-nonsurgical"
        },
        {
          title: "هشدار سازمان غذا و دارو درباره مصرف خودسرانه آنالوگ‌های GLP-1 برای لاغری",
          lead: "بررسی بالینی خطرات تهوع پایدار، گاستروپارزی و افت قند خون در مصرف غیراصولی آمپول‌های سماگلوتاید بدون آزمایش‌های اولیه عملکرد کلیوی و تیروئید.",
          category: "غدد و متابولیسم",
          author: "تیم متخصص محتوا نویس پزشکآن",
          readTime: "۶ دقیقه مطالعه",
          image: "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=700&q=80",
          slug: "diabetes-type2-hba1c-management"
        },
        {
          title: "دستورالعمل تازه‌ متغیرهای غربالگری پیشرفته بارداری و دقت تست سل‌فری",
          lead: "راهنمای تطبیقی کالج زنان برای تفسیر مقادیر MoM، سونوگرافی مارکرهای ژنتیکی و زمان طلایی نمونه‌گیری خون مادر برای آزمایش NIPT.",
          category: "زنان و زایمان",
          author: "تیم متخصص محتوا نویس پزشکآن",
          readTime: "۵ دقیقه مطالعه",
          image: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80",
          slug: "first-trimester-screening-cellfree-dna"
        }
      ];
      renderNewsCards(fallbackItems);
    }"""

if target in content:
    content = content.replace(target, replacement)
    print("✓ Successfully replaced target string in newsletter.html")
else:
    # Try normalizing CRLF
    content_norm = content.replace("\r\n", "\n")
    target_norm = target.replace("\r\n", "\n")
    replacement_norm = replacement.replace("\r\n", "\n")
    if target_norm in content_norm:
        content_norm = content_norm.replace(target_norm, replacement_norm)
        content = content_norm
        print("✓ Successfully replaced target string with LF normalization in newsletter.html")
    else:
        print("! Target string not found")

with open(NEWSLETTER_HTML, "w", encoding="utf-8") as f:
    f.write(content)

# Syntax check all scripts
import re
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', content)
print(f"Checking syntax for {len(scripts)} scripts in newsletter.html...")
all_ok = True
for idx, s in enumerate(scripts):
    fname = f"temp_check_{idx}.js"
    with open(fname, "w", encoding="utf-8") as tf:
        tf.write(s)
    res = subprocess.run(["node", "-c", fname], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Script {idx} syntax error:")
        print(res.stderr)
        all_ok = False
    else:
        print(f"✓ Script {idx} syntax OK")
    try:
        os.remove(fname)
    except:
        pass

if all_ok:
    print("ALL SCRIPTS PASSED SYNTAX CHECK 100%!")
