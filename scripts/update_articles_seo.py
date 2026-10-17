# -*- coding: utf-8 -*-
"""
Enriches mag/content/articles.json with full clinical editorial content,
rich HTML, featured image metadata, and complete WordPress/RankMath style SEO fields.
"""

import json
import os

BASE_DIR = r"e:\antigravity\pezeshkan_design"
ARTICLES_FILE = os.path.join(BASE_DIR, "mag", "content", "articles.json")

articles = [
  {
    "id": "lumbar-disc-herniation-nonsurgical",
    "pillarSlug": "/mag/physical-rehab/",
    "branchSlug": "/lumbar-cervical-disc-sciatica/",
    "slug": "nonsurgical-treatments-lumbar-disc-sciatica",
    "title": "راهنمای بالینی درمان غیرجراحی دیسک کمر و سیاتیک: از شاک‌ویو تا لیزر پرتوان",
    "summary": "بررسی علمی راهکارهای نوین توانبخشی و مداخله‌ای بدون نیاز به بیهوشی و تیغ جراحی، همراه با معیارهای تریاژ اورژانس سندرم دم اسب.",
    "readTime": "۸ دقیقه",
    "publishDate": "۲۴ شهریور ۱۴۰۵",
    "lastReviewed": "۲۵ شهریور ۱۴۰۵",
    "status": "published",
    "author": {
      "name": "دکتر مهران رادمنش",
      "title": "متخصص جراحی مغز، اعصاب و ستون فقرات",
      "mcNumber": "۱۱۴۲۸۵"
    },
    "reviewer": {
      "name": "دکتر احسان کریمی",
      "title": "فلوشیپ فوق‌تخصصی درد و اینترونشن ستون فقرات",
      "mcNumber": "۸۹۴۳۲"
    },
    "tags": ["دیسک کمر", "سیاتیک", "تکارتراپی", "شاک‌ویو", "ستون فقرات"],
    "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1200&q=80",
    "imageAlt": "پزشک متخصص مغز و اعصاب در حال بررسی تصویر ام‌آر‌آی ستون فقرات",
    "imageCaption": "تصویربرداری ام‌آر‌آی مقطع لومبار و بیرون‌زدگی دیسک L4-L5",
    "focusKeyword": "درمان غیرجراحی دیسک کمر",
    "metaTitle": "راهنمای بالینی درمان غیرجراحی دیسک کمر و سیاتیک | مجله پزشکآن",
    "metaDescription": "بررسی علمی راهکارهای نوین توانبخشی و مداخله‌ای بدون نیاز به بیهوشی و تیغ جراحی، همراه با معیارهای تریاژ اورژانس سندرم دم اسب.",
    "canonicalUrl": "https://pezeshkan.me/mag/nonsurgical-treatments-lumbar-disc-sciatica",
    "schemaType": "MedicalWebPage",
    "robots": "index, follow",
    "seoScore": 95,
    "rawHtml": "<h2>مقدمه و پاتوفیزیولوژی فتق دیسک لومبار</h2><p>فتق دیسک کمری (Lumbar Disc Herniation) یکی از شایع‌ترین علل درد ارجاعی به اندام تحتانی (درد سیاتیک) است. در بیش از ۸۵ درصد بیماران، با مدیریت صحیح بالینی، نیازی به جراحی باز نخواهد بود. فشار ناشی از بیرون‌زدگی بخش ژلاتینی دیسک (Nucleus Pulposus) بر روی ریشه‌های عصبی L4-L5 یا L5-S1 موجب التهاب حاد شیمیایی و دردهای تیرکشنده می‌شود.</p><figure class=\"clinical-img-figure\"><img src=\"https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1200&q=80\" alt=\"بررسی ام‌آر‌آی ستون فقرات توسط پزشک متخصص مغز و اعصاب\"><figcaption class=\"clinical-img-caption\">تفسیر بالینی اسکن ام‌آر‌آی جهت تعیین میزان درگیری فورامن عصبی</figcaption></figure><h2>علائم هشداردهنده بالینی (Red Flags)</h2><div class=\"clinical-callout warning\"><div class=\"callout-header\">⚠️ هشدار بالینی و تریاژ فوری</div><div>در صورتی که بیمار علائم زیر را تجربه کند، ارجاع اورژانسی به جراح الزامی است:<br>۱. بی‌اختیاری یا احتباس ادرار و مدفوع (سندرم دم اسب)<br>۲. افتادگی مچ پا (Foot Drop)<br>۳. بی‌حسی پیشرونده ناحیه زین اسبی (Saddle Anesthesia)</div></div><h2>پروتکل‌های پیشرفته غیرجراحی در پزشکآن</h2><p>در کلینیک طب فیزیکی، ترکیبی از سه متدولوژی اصلی به کار گرفته می‌شود: تکارتراپی هدفمند (RF Diathermy) جهت کاهش ادم ریشه عصب، شاک‌ویوتراپی فوکوس برای تحریک فاکتورهای رشد کلاژنی، و دکامپرشن دیجیتال مکانیکی.</p><div class=\"clinical-callout advice\"><div class=\"callout-header\">🩺 توصیه تخصصی پزشک ناظر</div><div>استراحت مطلق بیش از ۴۸ ساعت توصیه نمی‌شود؛ تمرینات ایزومتریک سبک و راه رفتن آرام به تسریع روند ترمیم بافت کمک می‌کند.</div></div>",
    "sections": [
      {
        "id": "intro",
        "title": "مقدمه و پاتوفیزیولوژی فتق دیسک لومبار",
        "content": "فتق دیسک کمری یکی از شایع‌ترین علل درد ارجاعی به اندام تحتانی است. در بیش از ۸۵ درصد بیماران نیازی به جراحی باز نخواهد بود."
      },
      {
        "id": "red-flags",
        "title": "علائم هشداردهنده بالینی (Red Flags)",
        "content": "بی‌اختیاری ادرار، افتادگی مچ پا و بی‌حسی زینی نیازمند جراحی اورژانسی در کمتر از ۴۸ ساعت است."
      },
      {
        "id": "conservative-protocols",
        "title": "پروتکل‌های پیشرفته غیرجراحی در پزشکآن",
        "content": "تکارتراپی RF، شاک‌ویو فوکوس و دکامپرشن دیجیتال سه ستون اصلی درمان تسکینی هستند."
      }
    ],
    "faqs": [
      {
        "q": "آیا استراحت مطلق در بستر برای درمان دیسک کمر مفید است؟",
        "a": "خیر؛ استراحت بیش از ۴۸ ساعت موجب ضعف عضلات پارااسپینال می‌شود."
      },
      {
        "q": "چند جلسه فیزیوتراپی پیشرفته لازم است؟",
        "a": "معمولاً دوره استاندارد شامل ۱۰ الی ۱۵ جلسه درمانی است."
      }
    ],
    "citations": [
      {
        "title": "The Lancet: Conservative vs Surgical Management of Lumbar Disc Herniation",
        "link": "https://pubmed.ncbi.nlm.nih.gov/"
      },
      {
        "title": "Spine Journal: Efficacy of High-Intensity Laser Therapy in Radiculopathy",
        "link": "https://pubmed.ncbi.nlm.nih.gov/"
      }
    ]
  },
  {
    "id": "first-trimester-screening-cellfree-dna",
    "pillarSlug": "/mag/maternity-wellness/",
    "branchSlug": "/maternity-pregnancy-fetal-medicine/",
    "slug": "first-trimester-screening-ultrasound-nipt",
    "title": "غربالگری سه ماهه اول بارداری: مقایسه تست ترکیبی با آزمایش ژنتیک سل‌فری (NIPT)",
    "summary": "راهنمای گام‌به‌گام مادران برای سنجش سونوگرافی NT، آزمایش‌های بیوشیمیایی و سل‌فری DNA جهت تشخیص زودهنگام ناهنجاری‌های کروموزومی.",
    "readTime": "۶ دقیقه",
    "publishDate": "۲۰ شهریور ۱۴۰۵",
    "lastReviewed": "۲۵ شهریور ۱۴۰۵",
    "status": "published",
    "author": {
      "name": "دکتر سارا توکلی",
      "title": "فوق تخصص پریناتولوژی و جراح زنان",
      "mcNumber": "۹۸۳۴۱"
    },
    "reviewer": {
      "name": "دکتر مریم دانشور",
      "title": "متخصص ژنتیک پزشکی و جنین‌شناسی",
      "mcNumber": "۷۶۵۲۱"
    },
    "tags": ["غربالگری بارداری", "سونوگرافی NT", "تست NIPT", "سل‌فری", "سندروم داون"],
    "image": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80",
    "imageAlt": "سونوگرافی غربالگری جنین در کلینیک زنان و زایمان",
    "imageCaption": "سونوگرافی شفافیت نوکال (NT) و استخوان بینی (NB) جنین",
    "focusKeyword": "غربالگری سه ماهه اول بارداری",
    "metaTitle": "غربالگری سه ماهه اول بارداری؛ مقایسه تست ترکیبی و NIPT | پزشکآن",
    "metaDescription": "راهنمای جامع مادران برای سونوگرافی NT، دابل مارکر و آزمایش DNA آزاد جنینی (سل‌فری NIPT) با دقت بالای ۹۹ درصد.",
    "canonicalUrl": "https://pezeshkan.me/mag/first-trimester-screening-ultrasound-nipt",
    "schemaType": "MedicalWebPage",
    "robots": "index, follow",
    "seoScore": 94,
    "rawHtml": "<h2>زمان طلایی انجام غربالگری سه ماهه اول</h2><p>دقیق‌ترین پنجره زمانی برای انجام سونوگرافی NT و آزمایش خون دابل مارکر (Free-Beta-hCG و PAPP-A) بین هفته ۱۱ تا ۱۳ هفته و ۶ روز بارداری است که طول سری-دمی جنین (CRL) بین ۴۵ تا ۸۴ میلی‌متر قرار دارد.</p><figure class=\"clinical-img-figure\"><img src=\"https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80\" alt=\"سونوگرافی غربالگری جنین در کلینیک زنان و زایمان\"><figcaption class=\"clinical-img-caption\">سونوگرافی غربالگری ناهنجاری‌های کروموزومی در کلینیک زنان</figcaption></figure><h2>تفاوت تست سل‌فری (NIPT) با غربالگری معمول</h2><p>آزمایش NIPT با ایزوله‌سازی قطعات DNA آزاد جنینی در گردش خون مادر عمل می‌کند. دقت این تست برای تریزومی ۲۱ (سندرم داون) بیش از ۹۹ درصد با نرخ مثبت کاذب کمتر از ۰.۱ درصد است.</p><div class=\"clinical-callout advice\"><div class=\"callout-header\">🩺 توصیه تخصصی پریناتولوژی</div><div>انجام تست NIPT برای تمامی مادران باردار به ویژه بالای ۳۵ سال یا سابقه ناهنجاری کروموزومی توصیه اکید می‌گردد.</div></div>",
    "sections": [
      {
        "id": "screening-timeline",
        "title": "زمان طلایی انجام غربالگری سه ماهه اول",
        "content": "دقیق‌ترین پنجره زمانی بین هفته ۱۱ تا ۱۳ هفته و ۶ روز بارداری است."
      },
      {
        "id": "nipt-vs-combined",
        "title": "تفاوت تست سل‌فری (NIPT) با غربالگری معمول",
        "content": "دقت تست NIPT بیش از ۹۹.۲ درصد با نرخ خطای کمتر از ۰.۱ درصد است."
      }
    ],
    "faqs": [
      {
        "q": "آیا آزمایش سل‌فری نیاز به ناشتا بودن دارد؟",
        "a": "خیر، نیازی به ناشتایی ندارد اما مصرف آب کافی توصیه می‌شود."
      }
    ],
    "citations": [
      {
        "title": "ACOG Practice Bulletin No. 226: Screening for Fetal Chromosomal Abnormalities",
        "link": "https://pubmed.ncbi.nlm.nih.gov/"
      }
    ]
  },
  {
    "id": "chest-pain-triage-emergency-guide",
    "pillarSlug": "/mag/symptoms/",
    "branchSlug": "/acute-chest-pain-triage/",
    "slug": "chest-pain-triage-heart-attack-vs-gastric",
    "title": "تریاژ دردهای حاد قفسه سینه: تمایز بین حمله قلبی، ریفلاکس معده و اسپاسم عضلانی",
    "summary": "دستورالعمل بالینی تصمیم‌گیری سریع هنگام احساس درد در جناغ سینه؛ چه زمانی بلافاصله با اورژانس ۱۱۵ تماس بگیریم؟",
    "readTime": "۵ دقیقه",
    "publishDate": "۱۸ شهریور ۱۴۰۵",
    "lastReviewed": "۲۶ شهریور ۱۴۰۵",
    "status": "published",
    "author": {
      "name": "دکتر حمیدرضا سلیمی",
      "title": "متخصص قلب و عروق و فلوشیپ آنژیوپلاستی",
      "mcNumber": "۱۰۲۹۳۴"
    },
    "reviewer": {
      "name": "دکتر روزبه فرهنگ",
      "title": "متخصص طب اورژانس",
      "mcNumber": "۹۲۱۰۱"
    },
    "tags": ["درد قفسه سینه", "سکته قلبی", "تریاژ اورژانس", "نوار قلب", "آنژین"],
    "image": "https://images.unsplash.com/photo-1628348068343-c6a848d2b6dd?auto=format&fit=crop&w=800&q=80",
    "imageAlt": "گوشی پزشکی و نوار قلب مانیتورینگ بیمار قلبی",
    "imageCaption": "پایش الکتروکاردیوگرام اورژانس در تریاژ کد قرمز",
    "focusKeyword": "درد قفسه سینه",
    "metaTitle": "تریاژ دردهای حاد قفسه سینه: تمایز حمله قلبی از ریفلاکس | پزشکآن",
    "metaDescription": "دستورالعمل بالینی افتراق دردهای قلبی ایسکمیک از مشکلات گوارشی و عضلانی به همراه اقدامات طلایی در ۶۰ دقیقه اول.",
    "canonicalUrl": "https://pezeshkan.me/mag/chest-pain-triage-heart-attack-vs-gastric",
    "schemaType": "MedicalWebPage",
    "robots": "index, follow",
    "seoScore": 96,
    "rawHtml": "<h2>مشخصات بالینی درد ایسکمیک قلبی</h2><p>درد قلبی معمولاً احساس فشار سنگین، سوزش مبهم یا فشردن قفسه سینه است که ممکن است به فک، گردن، شانه چپ، پشت یا هر دو بازو انتشار یابد و همراه با تنگی نفس، تعریق سرد، تهوع یا سرگیجه باشد.</p><div class=\"clinical-callout warning\"><div class=\"callout-header\">🚨 کد قرمز تریاژ اورژانس</div><div>درد فشارنده قفسه سینه بیش از ۵ دقیقه همراه با تعریق سرد یک فوریت پزشکی است. بلافاصله با شماره ۱۱۵ تماس بگیرید و از رانندگی شخصی خودداری کنید.</div></div><h2>دردهای گوارشی و اسکلتی-عضلانی</h2><p>دردهای ناشی از ریفلاکس مری (GERD) با سوزش پشت جناغ پس از غذا و در حالت خوابیده تشدید می‌شوند. دردهای دیواره قفسه سینه (کاستوکندریت) با لمس موضعی یا نفس عمیق تغییر شدت می‌دهند.</p>",
    "sections": [
      {
        "id": "cardiac-features",
        "title": "مشخصات بالینی درد ایسکمیک قلبی",
        "content": "درد قلبی معمولاً احساس فشار سنگین یا سوزش مبهم است که به شانه چپ یا فک منتشر می‌شود."
      },
      {
        "id": "non-cardiac-causes",
        "title": "دردهای گوارشی و اسکلتی-عضلانی",
        "content": "دردهای گوارشی با ترش کردن همراهند اما تا زمان رد ایسکمی با نوار قلب، باید جدی تلقی شوند."
      }
    ],
    "faqs": [
      {
        "q": "آیا درد قفسه سینه در زنان علائم متفاوتی دارد؟",
        "a": "بله؛ زنان ممکن است با خستگی مفرط، تنگی نفس یا درد بالای شکم مراجعه کنند."
      }
    ],
    "citations": [
      {
        "title": "AHA/ACC Guideline for the Evaluation and Diagnosis of Chest Pain",
        "link": "https://pubmed.ncbi.nlm.nih.gov/"
      }
    ]
  },
  {
    "id": "prp-knee-osteoarthritis-injection",
    "pillarSlug": "/mag/physical-rehab/",
    "branchSlug": "/interventions/",
    "slug": "prp-knee-osteoarthritis-injection",
    "title": "تزریق پی‌آر‌پی (PRP) زانو؛ معجزه غضروف‌سازی یا تسکین موقت آرتروز؟",
    "summary": "بررسی شواهد علمی اثر پلاسمای غنی از پلاکت در مهار سایش مفصل زانو، دوز تزریق و اقدامات پس از تزریق پزشک.",
    "readTime": "۶ دقیقه",
    "publishDate": "۲۰ شهریور ۱۴۰۵",
    "lastReviewed": "۲۵ شهریور ۱۴۰۵",
    "status": "published",
    "author": {
      "name": "دکتر مهران رادمنش",
      "title": "متخصص طب فیزیکی و توانبخشی",
      "mcNumber": "۱۱۴۲۸۵"
    },
    "reviewer": {
      "name": "دکتر احسان کریمی",
      "title": "فلوشیپ فوق‌تخصصی درد",
      "mcNumber": "۸۹۴۳۲"
    },
    "tags": ["پی‌آر‌پی", "آرتروز زانو", "تزریق غضروف", "طب فیزیکی"],
    "image": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80",
    "imageAlt": "معاینه مفصل زانو توسط پزشک ارتوپد در کلینیک",
    "imageCaption": "تزریق تحت هدایت سونوگرافی MSK در کلینیک درد",
    "focusKeyword": "پی‌آر‌پی زانو",
    "metaTitle": "تزریق پی‌آر‌پی (PRP) زانو و درمان آرتروز مفصل | پزشکآن",
    "metaDescription": "بررسی شواهد علمی اثربخشی تزریق پلاسمای غنی از پلاکت (PRP) در کاهش دردهای آرتروز زانو و تسریع ترمیم غضروف.",
    "canonicalUrl": "https://pezeshkan.me/mag/prp-knee-osteoarthritis-injection",
    "schemaType": "MedicalWebPage",
    "robots": "index, follow",
    "seoScore": 92,
    "rawHtml": "<h2>مکانیسم اثر پلاسمای غنی از پلاکت در مفصل</h2><p>پلاسمای غنی از پلاکت (PRP) با فعال‌سازی گرانول‌های آلفا و آزادسازی فاکتورهای رشد فیبروبلاستی (FGF) و تبدیل‌کننده بتا (TGF-beta)، باعث مهار متالوپروتئینازها و کاهش روند تخریب کندروسیت‌های مفصلی می‌شود.</p><figure class=\"clinical-img-figure\"><img src=\"https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80\" alt=\"معاینه مفصل زانو توسط پزشک ارتوپد\"><figcaption class=\"clinical-img-caption\">ارزیابی دقیق درجه‌بندی کلگرن-لارنس (Kellgren-Lawrence) آرتروز زانو</figcaption></figure><h2>پروتکل تزریق و مراقبت‌های پس از آن</h2><p>تزریق باید ترجیحاً تحت هدایت سونوگرافی داخل مفصلی صورت گیرد. بیمار باید از مصرف مسکن‌های ضدالتهاب غیراستروئیدی (NSAIDs) مانند ژلوفن به مدت دو هفته قبل و بعد از پروسیجر خودداری کند تا فرآیند طبیعی التیام پلاکت‌ها مختل نشود.</p>",
    "sections": [
      {
        "id": "prp-mechanism",
        "title": "مکانیسم اثر پلاسمای غنی از پلاکت در مفصل",
        "content": "فاکتورهای رشد آزادشده از پلاکت‌ها روند تخریب غضروف را کند کرده و التهاب مایع سینوویال را مهار می‌کنند."
      }
    ],
    "faqs": [
      {
        "q": "تزریق PRP چند جلسه نیاز دارد؟",
        "a": "معمولاً یک تا سه جلسه با فواصل ۳ الی ۴ هفته‌ای توصیه می‌شود."
      }
    ],
    "citations": [
      {
        "title": "Arthroscopy Journal: Platelet-Rich Plasma vs Hyaluronic Acid in Knee Osteoarthritis",
        "link": "https://pubmed.ncbi.nlm.nih.gov/"
      }
    ]
  }
]

with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"Successfully populated {len(articles)} clinical articles with full SEO metadata!")
