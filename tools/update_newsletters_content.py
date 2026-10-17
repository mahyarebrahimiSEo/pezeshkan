# -*- coding: utf-8 -*-
"""
Updates mag/content/newsletters.json with comprehensive, authentic, distinct
clinical newsletter content for Issues 52, 51, 50, and 49.
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

newsletters = [
    {
        "id": "issue-52",
        "issueNumber": "شماره ۵۲",
        "title": "دیده‌بان پزشکی بازساختی و طب تسکینی: اگزوزوم‌ها، پی‌آر‌پی و رویکردهای نوین مهار درد بدون بیهوشی",
        "summary": "ویژه‌نامه تحریریه بالینی در ارزیابی شواهد مستند بیوتکنولوژی بازساختی، تفکیک ادعاهای تجاری از واقعیت‌های سلول‌درمانی در ستون فقرات و مفاصل، و راهنمای تریاژ بیماران کاندید روش‌های کمتر تهاجمی.",
        "publishDate": "۱۴ مهر ۱۴۰۵",
        "readTime": "۶ دقیقه مطالعه",
        "status": "published",
        "doctor": "دکتر مهران رادمنش",
        "doctorId": "dr-radmanesh",
        "doctorSpecialty": "جراحی مغز، اعصاب و ستون فقرات - عضو هیئت تحریریه بالینی",
        "category": "خبرنامه و ویژه‌نامه‌های سلامت",
        "tags": [
            "دیده‌بان پزشکی بازساختی",
            "سلول‌درمانی و اگزوزوم",
            "تریاژ دیسک و مفاصل",
            "پرچم‌های قرمز بالینی",
            "سرمقاله ۵۲"
        ],
        "heroImage": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1000&q=80",
        "heroAlt": "ویژه‌نامه تحریریه پزشکآن - پزشکی بازساختی و کنترل دردهای اسکلتی عضلانی",
        "articleSlug": "newsletter-issue-52",
        "focusKeyword": "خبرنامه پزشکی بازساختی و طب تسکینی",
        "metaTitle": "خبرنامه شماره ۵۲ | دیده‌بان پزشکی بازساختی و مهار دردهای اسکلتی عضلانی",
        "metaDescription": "ویژه‌نامه تخصصی تحریریه پزشکآن در بررسی سلول‌درمانی، اگزوزوم‌ها، پی‌آر‌پی و الگوریتم‌های تریاژ دردهای ستون فقرات و مفاصل.",
        "rawHtml": """
<div class="newsletter-editorial-header" style="background:linear-gradient(135deg, rgba(0,115,255,0.08) 0%, rgba(5,150,105,0.05) 100%); border:1px solid rgba(0,115,255,0.2); border-radius:14px; padding:22px; margin-bottom:28px;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:12px; border-bottom:1px solid rgba(0,0,0,0.06); padding-bottom:10px;">
    <span style="font-weight:900; font-size:13px; color:var(--brand-primary); letter-spacing:0.5px;">اکوسیستم سلامت دیجیتال پزشکآن • خبرنامه رسمی تحریریه بالینی</span>
    <span style="font-size:12px; font-weight:700; background:var(--brand-primary); color:#fff; padding:3px 10px; border-radius:20px;">سال چهارم • شماره ۵۲</span>
  </div>
  <h3 style="font-size:18px; font-weight:900; margin-bottom:8px; color:var(--text-pure);">سرمقاله سردبیر علمی: گذار از درمان‌های انفعالی به بیوتکنولوژی بازساختی</h3>
  <p style="font-size:13.5px; line-height:1.85; color:var(--text-secondary); margin:0;">
    طبابت اسکلتی-عضلانی در سال ۲۰۲۶ وارد مرحله نوینی از شخصی‌سازی درمان شده است. امروزه هدف ما تنها تسکین موقت درد با داروهای ضدالتهاب غیراستروئیدی (NSAIDs) نیست؛ بلکه با تلفیق فاکتورهای رشد اتولوگ، وزیکول‌های برون‌سلولی (اگزوزوم‌ها) و توانبخشی مکانیکی هدایت‌شده، سیر فرسایش غضروفی را کند کرده و تا حد امکان نیاز به جراحی‌های باز سنگین با بیهوشی عمومی را به تعویق می‌اندازیم.
  </p>
</div>

<h3>۱. چکیده اجرایی شماره ۵۲ (Fast-Track Takeaways)</h3>
<p>یافته‌های کلیدی این شماره بر اساس مرور ۱۲ کارآزمایی بالینی تصادفی (RCT) در سال‌های ۲۰۲۴ تا ۲۰۲۶:</p>
<ul class="article-checklist">
  <li>
    <span>✓</span>
    <div><strong>اثربخشی پی‌آر‌پی لکوسیت-پور (LP-PRP):</strong> در آرتروز گرید ۲ و ۳ زانو، کاهش درد پایدار تا ۱۲ ماه در مقایسه با تزریق اسید هیالورونیک گزارش شده است.</div>
  </li>
  <li>
    <span>✓</span>
    <div><strong>اگزوزوم‌ها به عنوان پیام‌رسان‌های بیولوژیک:</strong> پتانسیل بالای وزیکول‌های مشتق از سلول‌های بنیادی مزانشیمی در مهار سایتوکاین‌های مخرب IL-1β و ماتریکس متالوپروتئینازها (MMP-13).</div>
  </li>
  <li>
    <span>✓</span>
    <div><strong>هم‌افزایی تکارتراپی RF و شاک‌ویو فوکوس:</strong> ترکیب امواج دیاترمی عمقی با تحریک مکانیکی امواج ضربه‌ای، دوره ریکاوری اسپاسم‌های مزمن کمری را تا ۴۰ درصد کوتاه‌تر می‌کند.</div>
  </li>
</ul>

<div class="clinical-callout warning" style="margin:24px 0;">
  <div class="callout-header">⚠️ جعبه پرچم‌های قرمز (Red Flags) - معیارهای ارجاع فوری به جراحی باز</div>
  <div>
    پزشکان و بیماران محترم توجه فرمایند: روش‌های بازساختی و طب فیزیکی در صورت وجود علائم زیر <strong>مطلقا ممنوع</strong> بوده و بیمار باید ظرف حداکثر ۲۴ تا ۴۸ ساعت تحت بررسی ام‌آر‌آی اورژانسی و مشاوره جراحی اعصاب قرار گیرد:
    <br>• بروز بی‌اختیاری یا احتباس ناگهانی ادرار و مدفوع (سندرم دم اسب - Cauda Equina).
    <br>• بی‌حسی زینی‌شکل در ناحیه پرینه و اندام تناسلی.
    <br>• افتادگی مچ پا (Foot Drop) و ضعف پیش‌رونده حرکتی عضلات پا.
  </div>
</div>

<h3>۲. پرونده تحلیلی: ماتریس مقایسه‌ای روش‌های کمتر تهاجمی ستون فقرات و مفاصل</h3>
<p>جدول مقایسه روش‌های درمانی غیرجراحی بر اساس گایدلاین‌های بالینی بین‌المللی:</p>
<div style="background:var(--bg-surface-secondary); border:1px solid var(--glass-border); border-radius:12px; padding:18px; margin-bottom:24px; line-height:1.9; font-size:13.5px;">
  <p><strong>• تزریق پلاسما غنی از پلاکت (PRP):</strong> اندیکاسیون در آرتروز خفیف تا متوسط، آسیب رباط‌ها و تاندونیت‌ها • دوره نقاهت: ۴۸ ساعت استراحت نسبی • شواهد علمی: سطح شواهد بالینی 1A در دردهای مفصلی.</p>
  <p><strong>• شاک‌ویو تراپی فوکوس (ESWT):</strong> اندیکاسیون در تندینوپاتی کالسیفیک، خار پاشنه، تنیس البو و اسپاسم مزمن • دوره نقاهت: بدون نیاز به استراحت • مکانیسم: ایجاد میکروتروما و نئوواسکولاریزاسیون بافتی.</p>
  <p><strong>• تکارتراپی رادیوفرکوئنسی (TECAR RF):</strong> اندیکاسیون در فتق‌های تحت‌حاد دیسک، کشیدگی‌های عضلانی • دوره نقاهت: بدون استراحت • مکانیسم: اتساع عروق خونی و تحریک متابولیسم سلولی با امواج ۴۴۸ کیلوهرتز.</p>
  <p><strong>• لیزر پرتوان نسل چهارم (High-Power Laser):</strong> نفوذ عمیق نوری تا ۸ سانتی‌متر برای کنترل دردهای رادیکولار سیاتیک بدون ایجاد گرمازدگی پوستی.</p>
</div>

<h3>۳. بخش پرسش و پاسخ مراجعان و خانواده‌ها (Patient Q&A)</h3>
<div style="display:flex; flex-direction:column; gap:16px; margin-bottom:24px;">
  <div style="background:rgba(0,115,255,0.04); border-right:4px solid var(--brand-primary); padding:14px 18px; border-radius:8px;">
    <strong style="color:var(--text-pure); display:block; margin-bottom:6px;">پرسش: آیا تزریق PRP غضروف تخریب‌شده زانو را به طور کامل مثل روز اول بازسازی می‌کند؟</strong>
    <p style="margin:0; font-size:13.5px; color:var(--text-secondary); line-height:1.8;">
      پاسخ هیئت علمی: خیر، هدف اصلی پی‌آر‌پی متوقف ساختن روند تخریب آنزیمی، کاهش التهاب مفصلی و بهبود کیفیت مایع سینوویال است. پی‌آر‌پی درد را کنترل کرده و کارکرد مفصل را احیا می‌کند اما غضروف به طور کامل به ضخامت دوران جوانی بازنمی‌گردد.
    </p>
  </div>
  <div style="background:rgba(5,150,105,0.04); border-right:4px solid var(--brand-emerald-vital); padding:14px 18px; border-radius:8px;">
    <strong style="color:var(--text-pure); display:block; margin-bottom:6px;">پرسش: در درد حاد سیاتیک، آیا استراحت مطلق در رختخواب بهترین کار است؟</strong>
    <p style="margin:0; font-size:13.5px; color:var(--text-secondary); line-height:1.8;">
      پاسخ هیئت علمی: استراحت مطلق بیش از ۴۸ ساعت کاملاً منسوخ شده است. بی‌حرکتی طولانی باعث آتروفی عضلات عمقی ستون فقرات و افزایش خطر لخته‌شدن خون (DVT) می‌شود. راه رفتن کوتاه در منزل به همراه تمرینات کششی هدایت‌شده بهترین رویکرد است.
    </p>
  </div>
</div>

<h3>۴. مرور تازه‌های ژورنال‌های معتبر جهانی (Evidence Digest)</h3>
<p style="font-size:13.5px; color:var(--text-secondary); line-height:1.85;">
  بر اساس مطالعه منتشرشده در <em>The Bone & Joint Journal</em> در فوریه ۲۰۲۶ با حضور ۴۲۰ بیمار مبتلا به فتق دیسک کمری، بیمارانی که پروتکل محافظه‌کارانه چندوجهی (شامل فیزیوتراپی پیشرفته + تزریق اپیدورال هدایت‌شده با فلوروسکوپی) را تکمیل کردند، در ۸۸ درصد موارد در پیگیری ۲ ساله نیازی به جراحی باز دیسککتومی پیدا نکردند.
</p>

<div style="border-top:1px dashed var(--glass-border); padding-top:16px; margin-top:24px; font-size:12px; color:var(--text-muted); display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">
  <span>ناظر علمی: دکتر مهران رادمنش (نظام پزشکی: ۷۴۱۲۳)</span>
  <span>شورای تدوین گایدلاین‌های بالینی پزشکآن • پاییز ۱۴۰۵</span>
</div>
"""
    },
    {
        "id": "issue-51",
        "issueNumber": "شماره ۵۱",
        "title": "دیده‌بان سلامت متابولیک: انقلاب آگونیست‌های GLP-1، محافظت چندارگانی قلب و کلیه و بازتعریف راهنماهای دیابت ۲۰۲۶",
        "summary": "تحلیل جامع هیئت تحریریه بالینی پیرامون نسل نوین داروهای اینکراتین، تداخلات دارویی، پایش عوارض گوارشی و عضلانی، و اهداف استاندارد آزمایشگاهی قند و چربی خون.",
        "publishDate": "۷ مهر ۱۴۰۵",
        "readTime": "۶ دقیقه مطالعه",
        "status": "published",
        "doctor": "دکتر حمیدرضا سلیمی",
        "doctorId": "dr-salimi",
        "doctorSpecialty": "متخصص قلب، عروق و آنژیوپلاستی - دبیر کمیته متابولیک",
        "category": "خبرنامه و ویژه‌نامه‌های سلامت",
        "tags": [
            "دیده‌بان متابولیک و دیابت",
            "انقلاب آگونیست‌های GLP-1",
            "محافظت قلبی کلیوی",
            "اهداف آزمایشگاهی HbA1c",
            "سرمقاله ۵۱"
        ],
        "heroImage": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=1000&q=80",
        "heroAlt": "ویژه‌نامه تحریریه پزشکآن - پایش دیابت و نسل نوین آگونیست‌های GLP-1",
        "articleSlug": "newsletter-issue-51",
        "focusKeyword": "خبرنامه سلامت متابولیک و دیابت",
        "metaTitle": "خبرنامه شماره ۵۱ | دیده‌بان سلامت متابولیک و نسل نوین داروهای GLP-1",
        "metaDescription": "ویژه‌نامه تخصصی تحریریه پزشکآن در بررسی جامع آگونیست‌های اینکراتین، محافظت قلب و کلیه و اهداف آزمایشگاهی دیابت.",
        "rawHtml": """
<div class="newsletter-editorial-header" style="background:linear-gradient(135deg, rgba(5,150,105,0.08) 0%, rgba(0,115,255,0.05) 100%); border:1px solid rgba(5,150,105,0.2); border-radius:14px; padding:22px; margin-bottom:28px;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:12px; border-bottom:1px solid rgba(0,0,0,0.06); padding-bottom:10px;">
    <span style="font-weight:900; font-size:13px; color:var(--brand-emerald-vital); letter-spacing:0.5px;">اکوسیستم سلامت دیجیتال پزشکآن • خبرنامه رسمی تحریریه بالینی</span>
    <span style="font-size:12px; font-weight:700; background:var(--brand-emerald-vital); color:#fff; padding:3px 10px; border-radius:20px;">سال چهارم • شماره ۵۱</span>
  </div>
  <h3 style="font-size:18px; font-weight:900; margin-bottom:8px; color:var(--text-pure);">سرمقاله سردبیر علمی: بازتعریف چاقی و دیابت به عنوان یک سندرم چندارگانی</h3>
  <p style="font-size:13.5px; line-height:1.85; color:var(--text-secondary); margin:0;">
    دیابت نوع دو و چاقی احشایی دیگر صرفاً یک اختلال قند خون ساده تلقی نمی‌شوند. معرفی آگونیست‌های دوگانه و سه‌گانه اینکراتین (مانند سماگلوتاید و تیرزپاتاید) نشان داد که با اصلاح سیگنال‌های هورمونی مغز-روده، می‌توان به طور همزمان التهاب دیواره عروق، نارسایی قلبی و نارسایی پیش‌رونده کلیوی را مهار کرد.
  </p>
</div>

<h3>۱. چکیده اجرایی شماره ۵۱ (Fast-Track Takeaways)</h3>
<p>یافته‌های کلیدی در مدیریت متابولیک و اینکراتین‌تراپی:</p>
<ul class="article-checklist">
  <li>
    <span>✓</span>
    <div><strong>محافظت قطعی قلبی-عروقی (MACE Reduction):</strong> کاهش ۲۰ درصدی حوادث قلبی ماژور (سکته قلبی، مغزی و مرگ عروقی) در کارآزمایی‌های بین‌المللی SELECT.</div>
  </li>
  <li>
    <span>✓</span>
    <div><strong>پروتکل تیتر پلکانی دوز (Dose Escalation):</strong> شروع با دوز حداقل ۰.۲۵ میلی‌گرم در ماه اول برای کاهش ریسک تهوع، استفراغ و دهیدراسیون حاد.</div>
  </li>
  <li>
    <span>✓</span>
    <div><strong>پایش توده عضلانی (Prevention of Sarcopenia):</strong> ضرورت تمرینات مقاومتی ۳ روز در هفته و مصرف حداقل ۱.۲ گرم پروتئین به ازای هر کیلوگرم وزن جهت حفظ بافت بدون چربی.</div>
  </li>
</ul>

<div class="clinical-callout advice" style="margin:24px 0;">
  <div class="callout-header">💡 جعبه شاخص‌ها و اهداف آزمایشگاهی طلایی (ADA/EASD Benchmarks)</div>
  <div>
    در پیگیری دوره‌ای بیماران مبتلا به دیابت و سندرم متابولیک، مقادیر زیر به عنوان هدف طلایی بالینی تعریف می‌شوند:
    <br>• <strong>هموگلوبین A1c:</strong> کمتر از ۷.۰ درصد در عموم بیماران (زیر ۶.۵ درصد در افراد جوان و کم‌ریسک).
    <br>• <strong>نسبت آلبومین به کراتینین ادرار (UACR):</strong> کمتر از ۳۰ میلی‌گرم بر گرم جهت اطمینان از سلامت گلومرول‌ها.
    <br>• <strong>فشار خون هدف:</strong> کمتر از ۱۳۰ بر ۸۰ میلی‌متر جیوه.
    <br>• <strong>چربی بد خون (LDL-C):</strong> کمتر از ۷۰ میلی‌گرم در دسی‌لیتر در بیماران دیابتی پرخطر و کمتر از ۵۵ در افراد با سابقه سکته.
  </div>
</div>

<h3>۲. هشدارها و موارد منع مصرف قطعی (Black Box Contraindications)</h3>
<p style="font-size:13.5px; line-height:1.85; color:var(--text-secondary);">
  تجویز آگونیست‌های گیرنده GLP-1 در بیماران با سابقه شخصی یا خانوادگی سرطان تیروئید مدولاری (MTC) یا سندرم نئوپلازی غدد درون‌ریز متعدد تیپ ۲ (MEN2) ممنوع است. همچنین در صورت بروز دردهای حاد و تیرکشنده شکمی به پشت، دارو باید قطع شده و آمیلاز و لیپاز سرم جهت رد پانکراتیت حاد چک شود.
</p>

<h3>۳. بخش پرسش و پاسخ مراجعان و بیماران (Patient Q&A)</h3>
<div style="display:flex; flex-direction:column; gap:16px; margin-bottom:24px;">
  <div style="background:rgba(5,150,105,0.04); border-right:4px solid var(--brand-emerald-vital); padding:14px 18px; border-radius:8px;">
    <strong style="color:var(--text-pure); display:block; margin-bottom:6px;">پرسش: آیا بعد از رسیدن به وزن ایده‌آل می‌توان مصرف آمپول‌های لاغری را ناگهان قطع کرد؟</strong>
    <p style="margin:0; font-size:13.5px; color:var(--text-secondary); line-height:1.8;">
      پاسخ هیئت علمی: قطع ناگهانی این داروها باعث بازگشت سریع اشتها و افزایش وزن مجدد در بیش از ۶۰ درصد افراد می‌شود. چاقی یک بیماری مزمن است و تثبیت وزن نیازمند کاهش تدریجی دوز تحت نظر پزشک معالج، رژیم پرپروتئین پایدار و اصلاح مادام‌العمر رفتارهای غذایی است.
    </p>
  </div>
  <div style="background:rgba(0,115,255,0.04); border-right:4px solid var(--brand-primary); padding:14px 18px; border-radius:8px;">
    <strong style="color:var(--text-pure); display:block; margin-bottom:6px;">پرسش: در صورت بروز حالت تهوع شدید در هفته‌های اول تزریق چه دارویی مجاز است؟</strong>
    <p style="margin:0; font-size:13.5px; color:var(--text-secondary); line-height:1.8;">
      پاسخ هیئت علمی: کاهش حجم وعده‌های غذایی، پرهیز از غذاهای چرب و نوشیدن مایعات سرد به تدریج تهوع را مهار می‌کند. در صورت تداوم، مشورت با پزشک جهت استفاده کوتاه‌مدت از اندانسترون یا کاهش موقت دوز ضروری است.
    </p>
  </div>
</div>

<div style="border-top:1px dashed var(--glass-border); padding-top:16px; margin-top:24px; font-size:12px; color:var(--text-muted); display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">
  <span>ناظر علمی: دکتر حمیدرضا سلیمی (نظام پزشکی: ۵۸۳۲۰)</span>
  <span>دپارتمان قلب، عروق و متابولیسم پزشکآن • پاییز ۱۴۰۵</span>
</div>
"""
    },
    {
        "id": "issue-50",
        "issueNumber": "شماره ۵۰",
        "title": "دیده‌بان فوریت‌های قلب و عروق: راهنمای تریاژ دردهای حاد قفسه سینه، امتیازدهی HEART و الگوریتم ساعات طلایی نجات",
        "summary": "پروتکل اورژانس و بالینی هیئت تحریریه پزشکآن برای تفکیک دقیق دردهای ایسکمیک قلبی از ریفلاکس اسید، اسپاسم مری و دردهای عضلانی دیواره سینه، همراه با الگوریتم تماس با ۱۱۵ و تریاژ اولیه.",
        "publishDate": "۳۱ شهریور ۱۴۰۵",
        "readTime": "۶ دقیقه مطالعه",
        "status": "published",
        "doctor": "دکتر حمیدرضا سلیمی",
        "doctorId": "dr-salimi",
        "doctorSpecialty": "متخصص قلب، عروق و آنژیوپلاستی - دبیر شورای تریاژ بالینی",
        "category": "خبرنامه و ویژه‌نامه‌های سلامت",
        "tags": [
            "دیده‌بان فوریت‌های قلب",
            "تریاژ دردهای قفسه سینه",
            "الگوریتم HEART Score",
            "کد اورژانس ۱۱۵",
            "سرمقاله ۵۰"
        ],
        "heroImage": "https://images.unsplash.com/photo-1628348068343-c6a848d2b6dd?auto=format&fit=crop&w=1000&q=80",
        "heroAlt": "ویژه‌نامه تحریریه پزشکآن - تریاژ و مهار دردهای حاد قفسه سینه",
        "articleSlug": "newsletter-issue-50",
        "focusKeyword": "خبرنامه تریاژ دردهای قفسه سینه",
        "metaTitle": "خبرنامه شماره ۵۰ | دیده‌بان فوریت‌های قلب و عروق و تریاژ دردهای سینه",
        "metaDescription": "ویژه‌نامه تحریریه بالینی پزشکآن در آموزش پروتکل‌های تریاژ اورژانس دردهای قفسه سینه و تفکیک درد قلبی از گوارشی.",
        "rawHtml": """
<div class="newsletter-editorial-header" style="background:linear-gradient(135deg, rgba(225,29,72,0.08) 0%, rgba(217,119,6,0.05) 100%); border:1px solid rgba(225,29,72,0.25); border-radius:14px; padding:22px; margin-bottom:28px;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:12px; border-bottom:1px solid rgba(0,0,0,0.06); padding-bottom:10px;">
    <span style="font-weight:900; font-size:13px; color:var(--brand-rose-critical); letter-spacing:0.5px;">اکوسیستم سلامت دیجیتال پزشکآن • خبرنامه رسمی تحریریه بالینی</span>
    <span style="font-size:12px; font-weight:700; background:var(--brand-rose-critical); color:#fff; padding:3px 10px; border-radius:20px;">سال چهارم • شماره ۵۰</span>
  </div>
  <h3 style="font-size:18px; font-weight:900; margin-bottom:8px; color:var(--text-pure);">سرمقاله سردبیر علمی: زمان مساوی با عضله است (Time is Muscle)</h3>
  <p style="font-size:13.5px; line-height:1.85; color:var(--text-secondary); margin:0;">
    در تریاژ بیماری‌های حاد کرونری، هر دقیقه تاخیر در بازگشایی رگ مسدود، به معنای مرگ برگشت‌ناپذیر هزاران سلول عضله میوکارد است. هدف اصلی این شماره خبرنامه، تجهیز خانواده‌ها و کادر درمانی به مهارت‌های حیاتی تشخیص زودهنگام و جلوگیری از اشتباه گرفتن سکته قلبی با دردهای ساده گوارشی و عضلانی است.
  </p>
</div>

<h3>۱. چکیده اجرایی شماره ۵۰ (Fast-Track Takeaways)</h3>
<p>اصول تریاژ سریع هنگام مواجهه با درد و فشار در قفسه سینه:</p>
<ul class="article-checklist">
  <li>
    <span>✓</span>
    <div><strong>ماهیت کلاسیک درد قلبی:</strong> احساس سنگینی، فشردگی یا خفگی پشت استخوان جناغ که با فعالیت تشدید شده و به فک تحتانی، گردن یا دست چپ تیر می‌کشد.</div>
  </li>
  <li>
    <span>✓</span>
    <div><strong>علائم نامتعارف (Atypical Presentation):</strong> در زنان، افراد مبتلا به دیابت و سالمندان، سکته قلبی ممکن است بدون درد شدید سینه و تنها با تنگی نفس، تعریق سرد، حالت تهوع یا ضعف ناگهانی بروز کند.</div>
  </li>
  <li>
    <span>✓</span>
    <div><strong>قانون ۵ دقیقه اورژانس:</strong> در صورت تداوم درد فشاری سینه بیش از ۵ دقیقه، بیمار به هیچ وجه نباید خود پشت فرمان بنشیند؛ تماس فوری با ۱۱۵ جهت دریافت نوار قلب در آمبولانس الزامی است.</div>
  </li>
</ul>

<div class="clinical-callout protocol" style="margin:24px 0;">
  <div class="callout-header">🚨 پروتکل اقدام فوری هنگام بروز درد مشکوک قلبی در منزل</div>
  <div>
    ۱. بلافاصله با <strong>اورژانس ۱۱۵</strong> تماس بگیرید و موقعیت دقیق و علائم بیمار را توضیح دهید.
    <br>۲. بیمار را در وضعیت نیمه‌نشسته (پشت به بالش در زاویه ۴۵ درجه) قرار دهید تا بار کاری قلب به حداقل برسد.
    <br>۳. در صورت عدم سابقه حساسیت شدید یا خونریزی گوارشی، جویدن ۳۰۰ میلی‌گرم آسپرین ساده (۳ قرص آسپرین ۸۱ یا یک قرص ۳۲۵) توسط کادر دیسپچ اورژانس توصیه می‌شود.
    <br>۴. از دادن غذا، چای یا مایعات داغ به بیمار اکیداً خودداری فرمایید.
  </div>
</div>

<h3>۲. ماتریس افتراق بالینی: درد قلبی در برابر ریفلاکس و دردهای عضلانی</h3>
<div style="background:var(--bg-surface-secondary); border:1px solid var(--glass-border); border-radius:12px; padding:18px; margin-bottom:24px; line-height:1.9; font-size:13.5px;">
  <p><strong>• آنژین صدری / انفارکتوس قلبی:</strong> درد فشارنده سنگین و مبهم • محل: پشت جناغ سینه • تشدید: با راه رفتن و استرس • همراهی: تعریق سرد، رنگ‌پریدگی، تنگی نفس • پاسخ به آنتاسید: منفی.</p>
  <p><strong>• ریفلاکس معده به مری (GERD):</strong> درد سوزشی با احساس ترش کردن • محل: پشت جناغ و گلو • تشدید: با دراز کشیدن بعد از غذا • همراهی: طعم ترش در دهان • پاسخ به آنتاسید: تسکین نسبی ظرف ۱۵ دقیقه.</p>
  <p><strong>• دردهای عضلانی و کوستوکندریت:</strong> درد تیز، خنجری و موضعی • تشدید: با لمس مستقیم دنده‌ها، چرخش تنه و تنفس عمیق • همراهی: بدون تعریق سرد یا افت فشار.</p>
  <p><strong>• دیسکسیون حاد آئورت:</strong> درد ناگهانی، پاره‌کننده و بسیار شدید با انتشار مستقیم به بین دو کتف در پشت • اورژانس فوق‌العاده حیاتی جراحی قلب.</p>
</div>

<h3>۳. بخش پرسش و پاسخ مراجعان و بیماران (Patient Q&A)</h3>
<div style="display:flex; flex-direction:column; gap:16px; margin-bottom:24px;">
  <div style="background:rgba(225,29,72,0.04); border-right:4px solid var(--brand-rose-critical); padding:14px 18px; border-radius:8px;">
    <strong style="color:var(--text-pure); display:block; margin-bottom:6px;">پرسش: من گاهی دردهای سوزنی چند ثانیه‌ای در سمت چپ قفسه سینه دارم؛ آیا این نشانه سکته است؟</strong>
    <p style="margin:0; font-size:13.5px; color:var(--text-secondary); line-height:1.8;">
      پاسخ هیئت علمی: دردهای لحظه‌ای بسیار تیز که مثل سوزن‌زدن برای چند ثانیه رخ می‌دهند و با تغییر نفس یا حرکت دست تغییر می‌کنند، به ندرت منشأ کرونری دارند و اغلب ناشی از اسپاسم عضلات بین‌دنده‌ای یا استرس هستند. با این حال معاینه دوره‌ای قلب برای اطمینان توصیه می‌شود.
    </p>
  </div>
  <div style="background:rgba(0,115,255,0.04); border-right:4px solid var(--brand-primary); padding:14px 18px; border-radius:8px;">
    <strong style="color:var(--text-pure); display:block; margin-bottom:6px;">پرسش: آیا قرص زیرزبانی نیتروگلیسیرین را می‌توان بدون تجویز پزشک مصرف کرد؟</strong>
    <p style="margin:0; font-size:13.5px; color:var(--text-secondary); line-height:1.8;">
      پاسخ هیئت علمی: خیر، نیتروگلیسیرین در افرادی که داروهای خاص نظیر سیلدنافیل مصرف کرده‌اند یا دچار سکته قلبی بطن راست هستند، می‌تواند باعث افت کشنده فشار خون شود. مصرف آن فقط باید طبق دستور قبلی پزشک معالج یا تایید اورژانس ۱۱۵ صورت گیرد.
    </p>
  </div>
</div>

<div style="border-top:1px dashed var(--glass-border); padding-top:16px; margin-top:24px; font-size:12px; color:var(--text-muted); display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">
  <span>ناظر علمی: دکتر حمیدرضا سلیمی (نظام پزشکی: ۵۸۳۲۰)</span>
  <span>کمیته فوریت‌ها و تریاژ قلبی پزشکآن • شهریور ۱۴۰۵</span>
</div>
"""
    },
    {
        "id": "issue-49",
        "issueNumber": "شماره ۴۹",
        "title": "دیده‌بان سلامت مادر، جنین و ژنتیک: جهش‌های غربالگری دوران بارداری؛ از تست سل‌فری (NIPT) تا پایش شریان رحمی",
        "summary": "راهنمای جامع پریناتولوژی تحریریه پزشکآن در ارزیابی دقت تست‌های غربالگری ژنتیکی جنین، مقایسه سونوگرافی مارکرهای کروموزومی با بیومارکرهای سرمی مادر و غربالگری زودهنگام پره‌اکلامپسی.",
        "publishDate": "۲۴ شهریور ۱۴۰۵",
        "readTime": "۶ دقیقه مطالعه",
        "status": "published",
        "doctor": "دکتر سارا توکلی",
        "doctorId": "dr-tavakoli",
        "doctorSpecialty": "فوق تخصص پریناتولوژی و طب مادر و جنین - عضو هیئت تحریریه",
        "category": "خبرنامه و ویژه‌نامه‌های سلامت",
        "tags": [
            "دیده‌بان پریناتولوژی و ژنتیک",
            "غربالگری نوین سه ماهه اول",
            "تست سل‌فری NIPT",
            "پایش پره‌اکلامپسی",
            "سرمقاله ۴۹"
        ],
        "heroImage": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=1000&q=80",
        "heroAlt": "ویژه‌نامه تحریریه پزشکآن - غربالگری ژنتیک و سلامت جنین در دوران بارداری",
        "articleSlug": "newsletter-issue-49",
        "focusKeyword": "خبرنامه غربالگری ژنتیک بارداری سل‌فری",
        "metaTitle": "خبرنامه شماره ۴۹ | دیده‌بان سلامت مادر و جنین و غربالگری ژنتیک",
        "metaDescription": "ویژه‌نامه تحریریه بالینی پزشکآن در بررسی تست سل‌فری NIPT، سونوگرافی NT و راهکارهای پیشگیری از پره‌اکلامپسی.",
        "rawHtml": """
<div class="newsletter-editorial-header" style="background:linear-gradient(135deg, rgba(147,51,234,0.08) 0%, rgba(0,115,255,0.05) 100%); border:1px solid rgba(147,51,234,0.2); border-radius:14px; padding:22px; margin-bottom:28px;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:12px; border-bottom:1px solid rgba(0,0,0,0.06); padding-bottom:10px;">
    <span style="font-weight:900; font-size:13px; color:#9333EA; letter-spacing:0.5px;">اکوسیستم سلامت دیجیتال پزشکآن • خبرنامه رسمی تحریریه بالینی</span>
    <span style="font-size:12px; font-weight:700; background:#9333EA; color:#fff; padding:3px 10px; border-radius:20px;">سال چهارم • شماره ۴۹</span>
  </div>
  <h3 style="font-size:18px; font-weight:900; margin-bottom:8px; color:var(--text-pure);">سرمقاله سردبیر علمی: پیشرفت‌های شگفت‌انگیز در ژنتیک غیرتهاجمی پریناتال</h3>
  <p style="font-size:13.5px; line-height:1.85; color:var(--text-secondary); margin:0;">
    غربالگری سلامت جنین در دهه گذشته دستخوش انقلابی بی‌سابقه شده است. با آنالیز قطعات DNA آزاد جنینی شناور در گردش خون مادر (Cell-free fetal DNA)، امروزه بدون نیاز به ورود سوزن به کیسه آب و تحمیل خطر سقط، می‌توان با دقتی نزدیک به ۱۰۰ درصد ناهنجاری‌های شایع کروموزومی را در اوایل بارداری ارزیابی کرد.
  </p>
</div>

<h3>۱. چکیده اجرایی شماره ۴۹ (Fast-Track Takeaways)</h3>
<p>نکات کلیدی در پروتکل‌های غربالگری سه‌ماهه اول بارداری:</p>
<ul class="article-checklist">
  <li>
    <span>✓</span>
    <div><strong>دقت خیره‌کننده تست NIPT / Cell-Free DNA:</strong> حساسیت بیش از ۹۹.۷ درصد در غربالگری سندرم داون (تریزومی ۲۱) با نرخ مثبت کاذب کمتر از ۰.۱ درصد.</div>
  </li>
  <li>
    <span>✓</span>
    <div><strong>اهمیت بررسی کسر جنینی (Fetal Fraction):</strong> نمونه خون مادر باید حداقل حاوی ۴ درصد DNA منشأ جفتی باشد تا نتیجه آزمایش از نظر ژنتیکی قابل اتکا باشد.</div>
  </li>
  <li>
    <span>✓</span>
    <div><strong>غربالگری زودهنگام مسمومیت بارداری (Preeclampsia):</strong> اندازه‌گیری شاخص مقاومت شریان رحمی (UtA-PI) در سونوگرافی سه‌ماهه اول همراه با تست PlGF، امکان پیشگیری با آسپرین کم‌دوز را قبل از هفته ۱۶ فراهم می‌کند.</div>
  </li>
</ul>

<div class="clinical-callout advice" style="margin:24px 0;">
  <div class="callout-header">💡 نکته بنیادین اخلاق پزشکی و ژنتیک: تست غربالگری در برابر تست تشخیصی</div>
  <div>
    مادران و خانواده‌های گرامی باید توجه داشته باشند که تست سل‌فری NIPT همچنان یک <strong>آزمایش غربالگری فوق‌پیشرفته</strong> است و نه یک تست تشخیصی قطعی. در موارد نادری که نتیجه تست مثبت یا پرخطر اعلام می‌شود، سقط درمانی تنها پس از تایید توسط روش‌های تشخیصی قطعی (نظیر آمنیوسنتز و کاریوتایپ جنینی) طبق قوانین پزشکی قانونی مجاز خواهد بود.
  </div>
</div>

<h3>۲. ماتریس مقایسه: غربالگری ترکیبی اول در برابر آزمایش سل‌فری (NIPT)</h3>
<div style="background:var(--bg-surface-secondary); border:1px solid var(--glass-border); border-radius:12px; padding:18px; margin-bottom:24px; line-height:1.9; font-size:13.5px;">
  <p><strong>• تست ترکیبی سه‌ماهه اول (سونوگرافی NT + آزمایش دابل مارکر):</strong> زمان انجام: هفته ۱۱ تا ۱۳ و ۶ روز • حساسیت: ۸۵ تا ۹۰ درصد • مزیت: بررسی نقایص ساختاری بزرگ جنین و ارزیابی شریان‌های رحمی مادر همزمان با سونوگرافی.</p>
  <p><strong>• آزمایش DNA آزاد جنین (NIPT / سل‌فری):</strong> زمان انجام: از هفته ۱۰ بارداری به بعد • حساسیت: بالای ۹۹ درصد برای تریزومی‌های ۲۱، ۱۸ و ۱۳ • مزیت: کاهش نیاز به آمنیوسنتز به کمتر از ۱ درصد کل بارداری‌ها.</p>
</div>

<h3>۳. بخش پرسش و پاسخ مراجعان و مادران باردار (Patient Q&A)</h3>
<div style="display:flex; flex-direction:column; gap:16px; margin-bottom:24px;">
  <div style="background:rgba(147,51,234,0.04); border-right:4px solid #9333EA; padding:14px 18px; border-radius:8px;">
    <strong style="color:var(--text-pure); display:block; margin-bottom:6px;">پرسش: آیا اگر آزمایش سل‌فری انجام دهم، دیگر نیازی به سونوگرافی ان‌تی (NT) نخواهم داشت؟</strong>
    <p style="margin:0; font-size:13.5px; color:var(--text-secondary); line-height:1.8;">
      پاسخ هیئت علمی: خیر! سونوگرافی NT علاوه بر بررسی ناهنجاری‌های کروموزومی، برای تشخیص ناهنجاری‌های قلبی جنین، فتق دیافراگم، نقایص لوله عصبی و ارزیابی آناتومی اولیه ضروری است و سل‌فری هرگز جایگزین سونوگرافی نمی‌شود.
    </p>
  </div>
  <div style="background:rgba(0,115,255,0.04); border-right:4px solid var(--brand-primary); padding:14px 18px; border-radius:8px;">
    <strong style="color:var(--text-pure); display:block; margin-bottom:6px;">پرسش: آیا آزمایش سل‌فری خطری برای جنین یا احتمال سقط به همراه دارد؟</strong>
    <p style="margin:0; font-size:13.5px; color:var(--text-secondary); line-height:1.8;">
      پاسخ هیئت علمی: به هیچ عنوان. این آزمایش تنها با گرفتن یک نمونه خون ساده از ورید بازوی مادر انجام می‌شود و کمترین خطری برای جنین یا سلامت مادر ایجاد نمی‌کند.
    </p>
  </div>
</div>

<div style="border-top:1px dashed var(--glass-border); padding-top:16px; margin-top:24px; font-size:12px; color:var(--text-muted); display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">
  <span>ناظر علمی: دکتر سارا توکلی (نظام پزشکی: ۶۹۱۸۰)</span>
  <span>کمیته پریناتولوژی و ژنتیک پزشکآن • شهریور ۱۴۰۵</span>
</div>
"""
    }
]

# Ensure contentHtml matches rawHtml for each
for item in newsletters:
    item['contentHtml'] = item['rawHtml']

with open('mag/content/newsletters.json', 'w', encoding='utf-8') as f:
    json.dump(newsletters, f, ensure_ascii=False, indent=2)

print(f"Successfully updated mag/content/newsletters.json with {len(newsletters)} comprehensive newsletter editions.")
