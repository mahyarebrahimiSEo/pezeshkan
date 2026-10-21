# -*- coding: utf-8 -*-
"""
Build script for Pezeshkan Health Magazine with:
- Explicit Vazirmatn font for all buttons including mega-menu trigger
- Floating Category Mega-Dropdown that floats outside the scroll container (100% reliable hover)
- Colored, styled, and spaced-out category scrollbar with 18px separation and left/right arrows
- Intuitive clinical search palette with instant trending chips and categorized results
- Engaging page scrollbar, animated progress line, and smooth back-to-top button
- 100% pure medical SVG icons and featured images for all articles
"""

import json

# Load icons
with open('mag/components/medical_icons.json', 'r', encoding='utf-8') as f:
    icons = json.load(f)

# Load pillars
with open('mag/content/pillars.json', 'r', encoding='utf-8') as f:
    pillars = json.load(f)

cat_icon_map = {
    0: 'spine',
    1: 'maternity',
    2: 'heart',
    3: 'lab',
    4: 'emergency',
    5: 'surgery',
    6: 'skin',
    7: 'digestive',
    8: 'pharma'
}

categories_js = []
for p in pillars:
    cid = p['id']
    icon_key = cat_icon_map.get(cid, 'hospital')
    branches = []
    for b in p.get('branches', []):
        branches.append({
            'title': b.get('title', ''),
            'desc': (b.get('clusters', [{}])[0].get('desc', ''))[:85] if b.get('clusters') else 'راهنمای بالینی و تشخیصی تخصصی'
        })
    categories_js.append({
        'id': cid,
        'name': p['name'],
        'iconKey': icon_key,
        'dept': p['dept'],
        'desc': p['desc'],
        'chips': p.get('chips', []),
        'subcategories': branches
    })

articles_js = [
    {
        'id': 'lumbar-disc-herniation-nonsurgical',
        'title': 'راهنمای بالینی درمان غیرجراحی دیسک کمر و سیاتیک: از شاک‌ویو تا لیزر پرتوان',
        'summary': 'بررسی علمی پروتکل‌های طب فیزیکی بدون نیاز به بیهوشی و تیغ جراحی، همراه با علائم هشداردهنده سندرم دم اسب و بازتوانی مفاصل.',
        'image': 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1200&q=80',
        'imageAlt': 'پزشک متخصص مغز و اعصاب در حال بررسی تصویر ام‌آر‌آی ستون فقرات',
        'categoryName': 'درد، ستون فقرات و توانبخشی',
        'categoryIcon': 'spine',
        'author': {
            'name': 'دکتر مهران رادمنش',
            'title': 'متخصص جراحی مغز، اعصاب و ستون فقرات',
            'mc': '۱۱۴۲۸۵',
            'avatar': 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۸ دقیقه مطالعه',
        'lastReviewed': '۲۵ شهریور ۱۴۰۵',
        'tag': 'ستون فقرات و مفاصل',
        'tagClass': 'tag-blue',
        'sections': [
            {'id': 's1', 'title': 'فتق دیسک کمری چگونه باعث درد سیاتیک می‌شود؟', 'content': 'فتق دیسک کمری یکی از شایع‌ترین علل دردهای تیرکشنده به اندام‌های تحتانی است. بیش از ۸۵ درصد بیماران با پروتکل‌های غیرتهاجمی نظیر تکارتراپی و شاک‌ویو بهبود می‌یابند و نیازی به جراحی باز ندارند.'},
            {'id': 's2', 'title': 'علائم خطری که نیاز به جراحی فوری دارند (Red Flags)', 'content': 'بی‌اختیاری یا احتباس ادرار، افتادگی مچ پا و عدم توانایی در ایستادن روی پاشنه، و بی‌حسی شدید ناحیه زینی نیازمند مداخله جراحی اورژانسی در کمتر از ۴۸ ساعت است.'},
            {'id': 's3', 'title': 'پروتکل‌های درمانی تکارتراپی و شاک‌ویو در کلینیک', 'content': 'تکارتراپی با فرکانس رادیویی هدفمند ادم عصب را کاهش می‌دهد و شاک‌ویوتراپی با امواج صوتی پرانرژی خون‌رسانی و بازسازی بافت دیسک را شتاب می‌بخشد.'}
        ]
    },
    {
        'id': 'first-trimester-screening-cellfree-dna',
        'title': 'غربالگری سه ماهه اول بارداری؛ مقایسه تست ترکیبی با آزمایش سل‌فری (NIPT)',
        'summary': 'راهنمای جامع مادران برای سونوگرافی NT، آزمایش‌های بیوشیمیایی و تست سل‌فری جهت تشخیص زودهنگام ناهنجاری‌های کروموزومی جنین.',
        'image': 'https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80',
        'imageAlt': 'سونوگرافی غربالگری جنین در کلینیک زنان و زایمان',
        'categoryName': 'سلامت زنان، بارداری و زایمان',
        'categoryIcon': 'maternity',
        'author': {
            'name': 'دکتر سارا توکلی',
            'title': 'فوق تخصص پریناتولوژی و جراح زنان',
            'mc': '۹۸۳۴۱',
            'avatar': 'https://images.unsplash.com/photo-1594824813576-92d90ef26d4d?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۶ دقیقه مطالعه',
        'lastReviewed': '۲۴ شهریور ۱۴۰۵',
        'tag': 'مادر و بارداری',
        'tagClass': 'tag-teal',
        'sections': [
            {'id': 's1', 'title': 'بهترین زمان برای انجام غربالگری سه ماهه اول', 'content': 'دقیق‌ترین بازه زمانی برای انجام سونوگرافی NT و آزمایش خون ترکیبی بین هفته ۱۱ تا ۱۳ هفته و ۶ روز بارداری است.'},
            {'id': 's2', 'title': 'تست سل‌فری (NIPT) چقدر دقیق است؟', 'content': 'آزمایش سل‌فری با سنجش DNA آزاد جنین در خون مادر، با دقت بیش از ۹۹.۲ درصد سندرم داون و اختلالات کروموزومی را شناسایی می‌کند.'}
        ]
    },
    {
        'id': 'chest-pain-triage-emergency-guide',
        'title': 'تریاژ دردهای حاد قفسه سینه؛ تمایز حمله قلبی از ریفلاکس معده و اسپاسم',
        'summary': 'دستورالعمل بالینی تشخیص سریع هنگام احساس درد و سنگینی پشت جناغ سینه؛ چه زمانی باید فوراً با اورژانس ۱۱۵ تماس گرفت؟',
        'image': 'https://images.unsplash.com/photo-1628348068343-c6a848d2b6dd?auto=format&fit=crop&w=800&q=80',
        'imageAlt': 'گوشی پزشکی و نوار قلب مانیتورینگ بیمار قلبی',
        'categoryName': 'قلب، عروق، دیابت و غدد',
        'categoryIcon': 'heart',
        'author': {
            'name': 'دکتر حمیدرضا سلیمی',
            'title': 'متخصص قلب و عروق و آنژیوپلاستی',
            'mc': '۱۰۲۹۳۴',
            'avatar': 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۵ دقیقه مطالعه',
        'lastReviewed': '۲۶ شهریور ۱۴۰۵',
        'tag': 'اورژانس قلب',
        'tagClass': 'tag-orange',
        'sections': [
            {'id': 's1', 'title': 'علائم کلاسیک درد ایسکمیک قلبی', 'content': 'درد قلبی معمولاً احساس فشار و سنگینی شدید روی قفسه سینه است که به گردن، فک یا شانه و دست چپ منتشر می‌شود.'},
            {'id': 's2', 'title': 'تفاوت درد ریفلاکس گوارشی با درد قلبی', 'content': 'سوزش سردل پس از غذا خوردن رخ می‌دهد اما در هر درد حاد قفسه سینه ابتدا باید مشکل قلبی با نوار قلب رد شود.'}
        ]
    },
    {
        'id': 'prp-knee-osteoarthritis-injection',
        'title': 'تزریق پی‌آر‌پی (PRP) زانو؛ معجزه غضروف‌سازی یا تسکین موقت آرتروز؟',
        'summary': 'بررسی شواهد علمی اثر پلاسمای غنی از پلاکت در مهار سایش مفصل زانو، دوز تزریق و اقدامات پس از تزریق پزشک.',
        'image': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80',
        'imageAlt': 'معاینه مفصل زانو توسط پزشک ارتوپد در کلینیک',
        'categoryName': 'درد، ستون فقرات و توانبخشی',
        'categoryIcon': 'spine',
        'author': {
            'name': 'دکتر مهران رادمنش',
            'title': 'متخصص طب فیزیکی و توانبخشی',
            'mc': '۱۱۴۲۸۵',
            'avatar': 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۶ دقیقه مطالعه',
        'lastReviewed': '۲۰ شهریور ۱۴۰۵',
        'tag': 'تزریقات مفصلی',
        'tagClass': 'tag-blue',
        'sections': [
            {'id': 's1', 'title': 'پی‌آر‌پی چگونه به ترمیم غضروف کمک می‌کند؟', 'content': 'پلاسمای غنی از پلاکت با آزادسازی فاکتورهای رشد فیبروبلاستی، فرآیند التیام سلول‌های بافت مفصلی را تحریک می‌کند.'}
        ]
    },
    {
        'id': 'diabetes-type2-hba1c-management',
        'title': 'مدیریت قند خون و دیابت نوع ۲؛ از متفورمین و اوزمپیک تا اصلاح سبک زندگی',
        'summary': 'اهداف استاندارد هموگلوبین A1c، پایش قند خون ناشتا و پس از غذا و پیشگیری از عوارض چشمی و کلیوی دیابت.',
        'image': 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=800&q=80',
        'imageAlt': 'دستگاه تست قند خون و مراقبت دیابت',
        'categoryName': 'قلب، عروق، دیابت و غدد',
        'categoryIcon': 'heart',
        'author': {
            'name': 'دکتر حمیدرضا سلیمی',
            'title': 'فوق تخصص غدد و متابولیسم',
            'mc': '۱۰۲۹۳۴',
            'avatar': 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۷ دقیقه مطالعه',
        'lastReviewed': '۲۱ شهریور ۱۴۰۵',
        'tag': 'دیابت و غدد',
        'tagClass': 'tag-teal',
        'sections': [
            {'id': 's1', 'title': 'هدف درمانی در آزمایش A1c چقدر است؟', 'content': 'برای اکثر افراد بالغ مبتلا به دیابت، هدف هموگلوبین A1c زیر ۷ درصد تعریف می‌شود تا خطر آسیب عروقی به حداقل برسد.'}
        ]
    },
    {
        'id': 'stroke-fast-emergency-protocol',
        'title': 'پروتکل اورژانسی سکته مغزی (FAST)؛ هر دقیقه تاخیر معادل مرگ ۲ میلیون نورون',
        'summary': 'شناسایی افتادگی گوشه صورت، ضعف بازو، اختلال در تکلم و ضرورت رساندن بیمار در بازه طلایی تزریق داروی ترومبولیتیک.',
        'image': 'https://images.unsplash.com/photo-1587745416684-47953f16f02f?auto=format&fit=crop&w=800&q=80',
        'imageAlt': 'تیم اورژانس و مراقبت‌های حاد بیمارستانی',
        'categoryName': 'راهنمای علائم و تریاژ اورژانس',
        'categoryIcon': 'emergency',
        'author': {
            'name': 'دکتر مهران رادمنش',
            'title': 'متخصص مغز و اعصاب',
            'mc': '۱۱۴۲۸۵',
            'avatar': 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۵ دقیقه مطالعه',
        'lastReviewed': '۲۳ شهریور ۱۴۰۵',
        'tag': 'تریاژ و فوریت‌ها',
        'tagClass': 'tag-orange',
        'sections': [
            {'id': 's1', 'title': 'زمان طلایی ۴.۵ ساعته در سکته مغزی', 'content': 'تزریق داروی آلتپلاز برای باز کردن لخته مغزی فقط در ۴.۵ ساعت ابتدایی آغاز علائم موثر و مجاز است.'}
        ]
    },
    {
        'id': 'bariatric-sleeve-gastrectomy-guide',
        'title': 'جراحی لاپاراسکوپی اسلیو معده؛ شرایط شاخص توده بدنی (BMI) و مراقبت‌ها',
        'summary': 'چه کسانی کاندید مناسب جراحی لاپاراسکوپیک چاقی هستند؟ مقایسه اسلیو با بای‌پس و رژیم غذایی فازهای پس از عمل.',
        'image': 'https://images.unsplash.com/photo-1551076805-e1869033e561?auto=format&fit=crop&w=800&q=80',
        'imageAlt': 'اتاق عمل جراحی لاپاراسکوپی پیشرفته',
        'categoryName': 'جراحی‌های چاقی و لاپاراسکوپی',
        'categoryIcon': 'surgery',
        'author': {
            'name': 'دکتر نادر فرهمند',
            'title': 'فلوشیپ جراحی لاپاراسکوپی پیشرفته',
            'mc': '۸۵۴۱۲',
            'avatar': 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۸ دقیقه مطالعه',
        'lastReviewed': '۱۹ شهریور ۱۴۰۵',
        'tag': 'جراحی لاپاراسکوپی',
        'tagClass': 'tag-blue',
        'sections': [
            {'id': 's1', 'title': 'معیارهای بین‌المللی کاندیداتوری جراحی چاقی', 'content': 'افراد با BMI بالای ۳۵ همراه با بیماری‌های زمینه‌ای نظیر دیابت یا فشار خون کاندید انجام اسلیو لاپاراسکوپی هستند.'}
        ]
    },
    {
        'id': 'finasteride-minoxidil-hair-loss',
        'title': 'فیناستراید و ماینوکسیدیل؛ آیا واقعاً جلوی ریزش موی ارثی را می‌گیرند؟',
        'summary': 'بررسی علمی مکانیسم اثر قرص فیناستراید، محلول ماینوکسیدیل، مزوتراپی و بررسی عوارض جانبی بر اساس متون درماتولوژی.',
        'image': 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&w=800&q=80',
        'imageAlt': 'پزشک متخصص درماتولوژی و مراقبت از پوست و مو',
        'categoryName': 'پوست، مو و زیبایی',
        'categoryIcon': 'skin',
        'author': {
            'name': 'دکتر الهام مسعودی',
            'title': 'متخصص پوست، مو و زیبایی',
            'mc': '۱۱۲۸۴۰',
            'avatar': 'https://images.unsplash.com/photo-1594824813576-92d90ef26d4d?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۷ دقیقه مطالعه',
        'lastReviewed': '۲۲ شهریور ۱۴۰۵',
        'tag': 'پوست و مو',
        'tagClass': 'tag-teal',
        'sections': [
            {'id': 's1', 'title': 'مکانیسم مهار ریزش مو با فیناستراید', 'content': 'فیناستراید با مهار آنزیم ۵-آلفا ردوکتاز مانع تبدیل تستوسترون به هورمون مخرب فولیکول (DHT) می‌شود.'}
        ]
    },
    {
        'id': 'cbc-blood-test-interpretation',
        'title': 'راهنمای جامع تفسیر آزمایش خون CBC؛ تشخیص انواع کم‌خونی و پلاکت',
        'summary': 'بررسی فاکتورهای هموگلوبین، MCV، گلبول‌های سفید (WBC) و فریتین برای درک وضعیت ایمنی و خستگی مزمن.',
        'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80',
        'imageAlt': 'آزمایشگاه بیوشیمی و بررسی میکروسکوپی نمونه خون',
        'categoryName': 'چکاپ، تفسیر آزمایش‌ها و تصویربرداری',
        'categoryIcon': 'lab',
        'author': {
            'name': 'دکتر الهام مسعودی',
            'title': 'متخصص پاتولوژی و آزمایشگاه',
            'mc': '۱۱۲۸۴۰',
            'avatar': 'https://images.unsplash.com/photo-1594824813576-92d90ef26d4d?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۶ دقیقه مطالعه',
        'lastReviewed': '۲۴ شهریور ۱۴۰۵',
        'tag': 'تفسیر آزمایش‌ها',
        'tagClass': 'tag-blue',
        'sections': [
            {'id': 's1', 'title': 'نقش شاخص‌های MCV و MCH در افتراق کم‌خونی‌ها', 'content': 'کاهش MCV نشان‌دهنده کم‌خونی فقر آهن یا تالاسمی مینور است، در حالی که افزایش آن می‌تواند کمبود ویتامین B12 را نشان دهد.'}
        ]
    },
    {
        'id': 'gerd-endoscopy-gastric-ulcer',
        'title': 'ریفلاکس اسید معده و زخم‌های گوارشی؛ چه زمانی آندوسکوپی ضروری است؟',
        'summary': 'علائم زنگ خطر در سوزش سر دل، بررسی باکتری هلیکوباکتر پیلوری و جدیدترین داروهای مهارکننده پمپ پروتون (PPI).',
        'image': 'https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?auto=format&fit=crop&w=800&q=80',
        'imageAlt': 'مشاوره گوارش و کبد در کلینیک آندوسکوپی',
        'categoryName': 'گوارش، کبد و نشیمنگاه (پروکتولوژی)',
        'categoryIcon': 'digestive',
        'author': {
            'name': 'دکتر نادر فرهمند',
            'title': 'فوق تخصص گوارش و کبد بالینی',
            'mc': '۸۵۴۱۲',
            'avatar': 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۶ دقیقه مطالعه',
        'lastReviewed': '۱۸ شهریور ۱۴۰۵',
        'tag': 'گوارش و کبد',
        'tagClass': 'tag-teal',
        'sections': [
            {'id': 's1', 'title': 'علائم نیازمند آندوسکوپی فوری در بیماری‌های گوارشی', 'content': 'دشواری در بلع غذا (دیسفاژی)، کاهش وزن بدون دلیل و وجود خون در مدفوع ضرورت انجام آندوسکوپی را قطعی می‌کند.'}
        ]
    },
    {
        'id': 'ibuprofen-aspirin-drug-interaction',
        'title': 'راهنمای ایمنی داروها؛ خطرات تداخل هم‌زمان ایبوپروفن، آسپرین و استامینوفن',
        'summary': 'بررسی دوز مجاز مسکن‌های رایج، محافظت از مخاط معده و نحوه مصرف ایمن در سالمندان و مبتلایان به فشار خون.',
        'image': 'https://images.unsplash.com/photo-1471864190281-a93a3070b6de?auto=format&fit=crop&w=800&q=80',
        'imageAlt': 'کپسول‌ها و قرص‌های دارویی در دپارتمان فارماکولوژی',
        'categoryName': 'دانشنامه و اطلاعات دارویی',
        'categoryIcon': 'pharma',
        'author': {
            'name': 'دکتر سارا توکلی',
            'title': 'دکترای داروسازی بالینی',
            'mc': '۹۸۳۴۱',
            'avatar': 'https://images.unsplash.com/photo-1594824813576-92d90ef26d4d?auto=format&fit=crop&w=200&q=80'
        },
        'readTime': '۵ دقیقه مطالعه',
        'lastReviewed': '۱۷ شهریور ۱۴۰۵',
        'tag': 'اطلاعات دارویی',
        'tagClass': 'tag-blue',
        'sections': [
            {'id': 's1', 'title': 'چرا مصرف هم‌زمان مسکن‌های NSAID خطرناک است؟', 'content': 'مصرف همزمان ایبوپروفن و آسپرین خطر خونریزی معده را تا ۴ برابر افزایش داده و اثر محافظتی آسپرین روی قلب را کاهش می‌دهد.'}
        ]
    }
]

html_template = f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>مجله سلامت پزشکآن لایف | دانشنامه و راهنمای جامع پزشکی</title>
  
  <!-- فونت استاندارد وزیرمتن -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <style>
    /* ==========================================================================
       سیستم طراحی تم روز پزشکآن لایف (Day Mode - Clinical Light Aesthetic)
       برگرفته از وب‌سایت Axon Life (axon.me/life)
       رنگ‌بندی بالینی سفید، سرمه‌ای، آبی اکسون و سبز سلامت همراه با آیکون‌های وکتور SVG
       ========================================================================== */
    :root {{
      --bg-base: #F8FAFC;
      --bg-surface: #FFFFFF;
      --bg-subtle: #F1F5F9;
      --bg-elevated: #FFFFFF;
      
      --color-primary: #0073FF;
      --color-primary-hover: #0056cc;
      --color-primary-light: #EBF4FF;
      --color-teal: #059669;
      --color-teal-light: #ECFDF5;
      --color-orange: #F97316;
      --color-orange-light: #FFF7ED;
      --color-red: #DC2626;
      --color-red-light: #FEF2F2;
      
      --text-heading: #0F172A;
      --text-body: #334155;
      --text-secondary: #64748B;
      --text-muted: #94A3B8;
      
      --border-color: #E2E8F0;
      --border-light: #EDF2F7;
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 16px -2px rgba(15, 23, 42, 0.06);
      --shadow-lg: 0 12px 32px -4px rgba(15, 23, 42, 0.10);
      --shadow-card-hover: 0 14px 30px rgba(0, 115, 255, 0.14);
      
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --radius-xl: 24px;
      --radius-full: 9999px;
      
      --font-main: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
      font-family: var(--font-main);
    }}

    html {{
      scroll-behavior: smooth;
    }}

    body {{
      background-color: var(--bg-base);
      color: var(--text-body);
      font-family: var(--font-main);
      font-size: 15px;
      line-height: 1.8;
      overflow-x: hidden;
    }}

    /* Global Sleek Scrollbar */
    ::-webkit-scrollbar {{
      width: 8px;
    }}
    ::-webkit-scrollbar-track {{
      background: #F1F5F9;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #CBD5E1;
      border-radius: 9999px;
      border: 2px solid #F1F5F9;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: var(--color-primary);
    }}

    a {{
      color: var(--color-primary);
      text-decoration: none;
      transition: all 0.2s ease;
    }}
    a:hover {{
      color: var(--color-primary-hover);
    }}

    .container {{
      max-width: 1340px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    .svg-icon {{
      display: inline-block;
      width: 1.25em;
      height: 1.25em;
      vertical-align: -0.2em;
      stroke-width: 2;
      stroke: currentColor;
      fill: none;
      flex-shrink: 0;
    }}

    /* ==========================================================================
       1. هدر اصلی اپلیکیشن با پالت جستجوی هوشمند بالینی
       ========================================================================== */
    .main-header {{
      background: #FFFFFF;
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: var(--shadow-sm);
    }}
    .header-content {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 74px;
      gap: 20px;
    }}
    .brand-logo-wrap {{
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
    }}
    .brand-icon-box {{
      width: 44px;
      height: 44px;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, var(--color-primary) 0%, #0056cc 100%);
      color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(0, 115, 255, 0.28);
    }}
    .brand-title-text {{
      font-size: 19px;
      font-weight: 900;
      color: var(--text-heading);
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .brand-title-text span.badge {{
      font-size: 11px;
      font-weight: 700;
      background: var(--color-primary-light);
      color: var(--color-primary);
      padding: 2px 8px;
      border-radius: var(--radius-full);
      letter-spacing: normal;
    }}
    .brand-subtitle {{
      font-size: 11.5px;
      color: var(--text-secondary);
      margin-top: -2px;
    }}

    /* Search Bar with Instant Clinical Palette */
    .header-search-bar {{
      flex: 1;
      max-width: 480px;
      position: relative;
    }}
    .search-input-box {{
      position: relative;
      display: flex;
      align-items: center;
    }}
    .search-input-box input {{
      width: 100%;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-full);
      padding: 10px 44px 10px 40px;
      font-size: 13.5px;
      font-family: var(--font-main);
      color: var(--text-heading);
      transition: all 0.25s ease;
      outline: none;
    }}
    .search-input-box input:focus {{
      background: #FFFFFF;
      border-color: var(--color-primary);
      box-shadow: 0 0 0 3px rgba(0, 115, 255, 0.16);
    }}
    .search-input-box .search-icon {{
      position: absolute;
      right: 14px;
      color: var(--text-muted);
      pointer-events: none;
      display: flex;
      align-items: center;
    }}
    .search-input-box .search-clear-btn {{
      position: absolute;
      left: 12px;
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      display: none;
      align-items: center;
      padding: 4px;
    }}

    /* Quick Clinical Search Flyout */
    .search-flyout-palette {{
      position: absolute;
      top: calc(100% + 10px);
      right: 0;
      left: 0;
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      box-shadow: 0 18px 40px -4px rgba(15, 23, 42, 0.18);
      padding: 16px 20px;
      display: none;
      z-index: 1200;
      animation: flyoutSlide 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    @keyframes flyoutSlide {{
      from {{ opacity: 0; transform: translateY(-8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .flyout-header-title {{
      font-size: 12.5px;
      font-weight: 800;
      color: var(--text-heading);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .quick-chips-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 16px;
    }}
    .quick-chip-btn {{
      padding: 5px 12px;
      border-radius: var(--radius-full);
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      font-size: 11.5px;
      color: var(--text-body);
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: var(--font-main);
    }}
    .quick-chip-btn:hover {{
      background: var(--color-primary-light);
      border-color: var(--color-primary);
      color: var(--color-primary);
    }}
    .search-results-section {{
      border-top: 1px solid var(--border-light);
      padding-top: 12px;
      max-height: 380px;
      overflow-y: auto;
    }}
    .search-cat-group-label {{
      font-size: 11px;
      font-weight: 800;
      color: var(--color-primary);
      margin: 8px 0 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .search-res-item {{
      padding: 9px 12px;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: background 0.15s ease;
      display: flex;
      flex-direction: column;
    }}
    .search-res-item:hover {{
      background: var(--color-primary-light);
    }}
    .search-res-title {{
      font-size: 13.5px;
      font-weight: 700;
      color: var(--text-heading);
    }}
    .search-res-sub {{
      font-size: 11.5px;
      color: var(--text-secondary);
      margin-top: 2px;
    }}

    .header-actions-group {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .btn-ui {{
      padding: 9px 18px;
      border-radius: var(--radius-full);
      font-size: 13px;
      font-weight: 700;
      font-family: var(--font-main);
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border: none;
      outline: none;
      white-space: nowrap;
    }}
    .btn-primary-gradient {{
      background: var(--color-primary);
      color: #FFFFFF;
      box-shadow: 0 4px 12px rgba(0, 115, 255, 0.25);
    }}
    .btn-primary-gradient:hover {{
      background: var(--color-primary-hover);
      transform: translateY(-1px);
      box-shadow: 0 6px 16px rgba(0, 115, 255, 0.35);
    }}
    .btn-subtle-outline {{
      background: #FFFFFF;
      color: var(--text-heading);
      border: 1px solid var(--border-color);
    }}
    .btn-subtle-outline:hover {{
      border-color: var(--color-primary);
      color: var(--color-primary);
      background: var(--color-primary-light);
    }}

    /* ==========================================================================
       2. نوار دسته‌بندی‌ها با اسکرول رنگی، فلش‌های ناوبری و منوی آبشاری شناور
       ========================================================================== */
    .category-navbar {{
      background: #FFFFFF;
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 74px;
      z-index: 950;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
      overflow: visible;
    }}
    .category-nav-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      position: relative;
    }}

    /* Horizontal Scroll Area with Arrows */
    .category-scroll-container {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex: 1;
      overflow: hidden;
      position: relative;
    }}
    .nav-scroll-btn {{
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      color: var(--color-primary);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(0,0,0,0.06);
      transition: all 0.2s ease;
      flex-shrink: 0;
      z-index: 10;
      font-family: var(--font-main);
    }}
    .nav-scroll-btn:hover {{
      background: var(--color-primary);
      color: #FFFFFF;
      border-color: var(--color-primary);
      transform: scale(1.06);
    }}

    .category-pills-list {{
      display: flex;
      align-items: center;
      gap: 7px;
      overflow-x: auto;
      scroll-behavior: smooth;
      padding-top: 10px;
      padding-bottom: 18px; /* فاصله مشخص و مناسب از نوار اسکرول */
      margin-bottom: 2px;
      flex: 1;
    }}
    /* اسکرول‌بار اختصاصی، رنگ‌شده و متمایز */
    .category-pills-list::-webkit-scrollbar {{
      height: 6px;
    }}
    .category-pills-list::-webkit-scrollbar-track {{
      background: #E2E8F0;
      border-radius: 9999px;
      margin: 0 25px;
    }}
    .category-pills-list::-webkit-scrollbar-thumb {{
      background: linear-gradient(90deg, #0073FF 0%, #00B4D8 100%);
      border-radius: 9999px;
      box-shadow: 0 1px 4px rgba(0, 115, 255, 0.35);
    }}
    .category-pills-list::-webkit-scrollbar-thumb:hover {{
      background: linear-gradient(90deg, #0056cc 0%, #0096c7 100%);
    }}
    .category-pills-list {{
      scrollbar-width: thin;
      scrollbar-color: #0073FF #E2E8F0;
    }}

    .nav-pill-item {{
      padding: 7px 14px;
      border-radius: var(--radius-full);
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-body);
      background: var(--bg-subtle);
      border: 1px solid transparent;
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-main);
    }}
    .nav-pill-item:hover, .nav-pill-item.active, .nav-pill-item.hover-active {{
      color: var(--color-primary);
      background: var(--color-primary-light);
      border-color: rgba(0, 115, 255, 0.28);
    }}
    .chevron-icon {{
      width: 12px;
      height: 12px;
      transition: transform 0.2s ease;
      stroke-width: 2.2;
    }}
    .nav-pill-item.hover-active .chevron-icon {{
      transform: rotate(180deg);
    }}

    /* دکمه مگامنو با فونت تضمین‌شده وزیرمتن */
    .mega-menu-trigger-btn {{
      padding: 8px 16px;
      border-radius: var(--radius-full);
      font-size: 12.5px;
      font-weight: 800;
      font-family: var(--font-main);
      color: var(--color-primary);
      background: var(--color-primary-light);
      border: 1px solid rgba(0, 115, 255, 0.25);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 7px;
      white-space: nowrap;
      transition: all 0.2s ease;
      flex-shrink: 0;
    }}
    .mega-menu-trigger-btn:hover {{
      background: var(--color-primary);
      color: #FFFFFF;
      box-shadow: 0 4px 12px rgba(0, 115, 255, 0.25);
    }}

    /* ==========================================================================
       پالت منوی آبشاری شناور خارج از کانتینر اسکرول (Floating Navbar Mega-Dropdown)
       بدون مشکل clip شدن و کاملاً آزاد روی صفحه
       ========================================================================== */
    .navbar-floating-dropdown {{
      position: absolute;
      top: calc(100% + 2px);
      right: 24px;
      left: 24px;
      max-width: 1100px;
      margin: 0 auto;
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-xl);
      box-shadow: 0 20px 48px -6px rgba(15, 23, 42, 0.16);
      padding: 24px 28px;
      display: none;
      z-index: 1200;
      animation: megaSlideDown 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    @keyframes megaSlideDown {{
      from {{ opacity: 0; transform: translateY(-8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .dropdown-top-meta {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 14px;
      margin-bottom: 16px;
    }}
    .dropdown-top-meta h4 {{
      font-size: 16px;
      font-weight: 800;
      color: var(--text-heading);
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .dropdown-subcats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }}
    .dropdown-subcat-card {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 12px 14px;
      cursor: pointer;
      transition: all 0.18s ease;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .dropdown-subcat-card:hover {{
      background: var(--color-primary-light);
      border-color: rgba(0, 115, 255, 0.35);
      transform: translateY(-2px);
    }}
    .dropdown-subcat-title {{
      font-size: 13px;
      font-weight: 800;
      color: var(--text-heading);
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .dropdown-subcat-desc {{
      font-size: 11.5px;
      color: var(--text-secondary);
      line-height: 1.6;
    }}
    .dropdown-bottom-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--border-light);
      padding-top: 12px;
      font-size: 13px;
    }}

    /* Subcategory Dynamic Strip */
    .subcategory-strip {{
      background: var(--bg-subtle);
      border-bottom: 1px solid var(--border-color);
      padding: 8px 0;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .subcat-strip-label {{
      font-size: 12px;
      font-weight: 700;
      color: var(--text-secondary);
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .subcat-chips-scroll {{
      display: flex;
      align-items: center;
      gap: 7px;
      overflow-x: auto;
      scrollbar-width: none;
    }}
    .subcat-chips-scroll::-webkit-scrollbar {{
      display: none;
    }}
    .subcat-pill {{
      padding: 4px 12px;
      border-radius: var(--radius-full);
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-body);
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
      font-family: var(--font-main);
    }}
    .subcat-pill:hover, .subcat-pill.active {{
      background: var(--color-primary);
      color: #FFFFFF;
      border-color: var(--color-primary);
    }}

    /* Main Container Area */
    .main-wrapper {{
      padding-top: 28px;
      padding-bottom: 80px;
    }}

    /* ==========================================================================
       3. هیروی نامتقارن ۵ تایی با تصاویر شاخص باکیفیت (Asymmetrical 5-Story Hero)
       ========================================================================== */
    .hero-magazine-grid {{
      display: grid;
      grid-template-columns: 1.55fr 1fr;
      gap: 24px;
      margin-bottom: 36px;
    }}
    @media (max-width: 992px) {{
      .hero-magazine-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .hero-primary-card {{
      background-size: cover;
      background-position: center;
      border-radius: var(--radius-xl);
      border: 1px solid var(--border-color);
      min-height: 440px;
      padding: 36px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      position: relative;
      overflow: hidden;
      box-shadow: var(--shadow-md);
      cursor: pointer;
      transition: all 0.3s ease;
    }}
    .hero-primary-card::before {{
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, rgba(15, 23, 42, 0.2) 0%, rgba(15, 23, 42, 0.65) 50%, rgba(15, 23, 42, 0.94) 100%);
      z-index: 1;
      transition: opacity 0.3s ease;
    }}
    .hero-primary-card:hover {{
      transform: translateY(-3px);
      box-shadow: var(--shadow-card-hover);
    }}
    .hero-primary-card:hover::before {{
      background: linear-gradient(180deg, rgba(15, 23, 42, 0.15) 0%, rgba(15, 23, 42, 0.6) 45%, rgba(15, 23, 42, 0.96) 100%);
    }}
    .hero-primary-content {{
      position: relative;
      z-index: 2;
      color: #FFFFFF;
    }}
    .hero-tag-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(0, 115, 255, 0.92);
      color: #FFFFFF;
      padding: 5px 14px;
      border-radius: var(--radius-full);
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 12px;
      backdrop-filter: blur(8px);
    }}
    .hero-title-text {{
      font-size: 26px;
      font-weight: 900;
      line-height: 1.5;
      margin-bottom: 10px;
      color: #FFFFFF;
    }}
    .hero-desc-text {{
      font-size: 14px;
      line-height: 1.8;
      color: #E2E8F0;
      margin-bottom: 16px;
      max-width: 90%;
    }}
    .hero-meta-row {{
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 12.5px;
      color: #CBD5E1;
      flex-wrap: wrap;
    }}

    .hero-secondary-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }}
    @media (max-width: 580px) {{
      .hero-secondary-grid {{
        grid-template-columns: 1fr;
      }}
    }}
    .hero-secondary-card {{
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      transition: all 0.25s ease;
    }}
    .hero-secondary-card:hover {{
      border-color: var(--color-primary);
      box-shadow: var(--shadow-card-hover);
      transform: translateY(-2px);
    }}
    .secondary-img-wrap {{
      height: 120px;
      width: 100%;
      overflow: hidden;
      position: relative;
      background: #E2E8F0;
    }}
    .secondary-img-wrap img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.35s ease;
    }}
    .hero-secondary-card:hover .secondary-img-wrap img {{
      transform: scale(1.06);
    }}
    .secondary-tag {{
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(6px);
      padding: 3px 8px;
      border-radius: var(--radius-full);
      font-size: 10.5px;
      font-weight: 700;
      color: var(--color-primary);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}
    .secondary-card-body {{
      padding: 14px;
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: space-between;
    }}
    .secondary-title-text {{
      font-size: 13.5px;
      font-weight: 800;
      color: var(--text-heading);
      line-height: 1.6;
      margin-bottom: 8px;
    }}
    .secondary-meta-text {{
      font-size: 11.5px;
      color: var(--text-secondary);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* ==========================================================================
       4. نوار سه‌گانه اعتماد و قابلیت‌های کلینیکی (Trust Strip)
       ========================================================================== */
    .clinical-trust-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
      gap: 16px;
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-xl);
      padding: 20px 24px;
      margin-bottom: 44px;
      box-shadow: var(--shadow-sm);
    }}
    .trust-strip-item {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    .strip-icon-box {{
      width: 44px;
      height: 44px;
      border-radius: var(--radius-md);
      background: var(--color-primary-light);
      color: var(--color-primary);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .strip-icon-box.teal {{
      background: var(--color-teal-light);
      color: var(--color-teal);
    }}
    .strip-icon-box.orange {{
      background: var(--color-orange-light);
      color: var(--color-orange);
    }}
    .strip-details h4 {{
      font-size: 14px;
      font-weight: 800;
      color: var(--text-heading);
      margin-bottom: 2px;
    }}
    .strip-details p {{
      font-size: 12px;
      color: var(--text-secondary);
    }}

    /* ==========================================================================
       5. کارت‌های هاب دسته‌بندی با چیپ‌ها (Category Hub Cards)
       ========================================================================== */
    .section-head-bar {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 14px;
    }}
    .section-title-wrap h2 {{
      font-size: 21px;
      font-weight: 900;
      color: var(--text-heading);
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .section-title-wrap p {{
      font-size: 13px;
      color: var(--text-secondary);
      margin-top: 3px;
    }}

    .category-cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 340px), 1fr));
      gap: 22px;
      margin-bottom: 50px;
    }}
    .dept-card {{
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s ease;
    }}
    .dept-card:hover {{
      border-color: var(--color-primary);
      box-shadow: var(--shadow-card-hover);
      transform: translateY(-2px);
    }}
    .dept-card-header {{
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 12px;
    }}
    .dept-card-icon {{
      width: 44px;
      height: 44px;
      border-radius: var(--radius-md);
      background: var(--bg-subtle);
      color: var(--color-primary);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .dept-card-meta h3 {{
      font-size: 16px;
      font-weight: 800;
      color: var(--text-heading);
    }}
    .dept-card-meta span {{
      font-size: 12px;
      color: var(--text-muted);
    }}
    .dept-card-desc {{
      font-size: 13px;
      color: var(--text-body);
      line-height: 1.7;
      margin-bottom: 16px;
    }}
    .dept-chips-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      margin-bottom: 20px;
    }}
    .dept-chip {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      padding: 4px 12px;
      border-radius: var(--radius-full);
      font-size: 12px;
      color: var(--text-body);
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: var(--font-main);
    }}
    .dept-chip:hover {{
      background: var(--color-primary-light);
      color: var(--color-primary);
      border-color: var(--color-primary);
    }}
    .dept-card-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--border-light);
      padding-top: 14px;
    }}
    .dept-count-badge {{
      font-size: 12px;
      color: var(--text-secondary);
    }}
    .dept-view-link {{
      color: var(--color-primary);
      font-weight: 700;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 4px;
      background: none;
      border: none;
      cursor: pointer;
      font-family: var(--font-main);
    }}

    /* ==========================================================================
       6. بنر داخلی اکسون (InsideBanner)
       ========================================================================== */
    .axon-inside-banner {{
      background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
      border-radius: var(--radius-xl);
      padding: 40px 48px;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 32px;
      margin-bottom: 50px;
      box-shadow: var(--shadow-lg);
    }}
    @media (max-width: 860px) {{
      .axon-inside-banner {{
        flex-direction: column;
        align-items: flex-start;
        padding: 30px;
      }}
    }}
    .inside-text h3 {{
      font-size: 22px;
      font-weight: 900;
      margin-bottom: 10px;
      color: #FFFFFF;
    }}
    .inside-text p {{
      font-size: 14px;
      color: #CBD5E1;
      line-height: 1.8;
      max-width: 640px;
    }}
    .inside-cta-btn {{
      background: #FFFFFF;
      color: #0F172A;
      font-weight: 800;
      font-size: 14px;
      padding: 13px 28px;
      border-radius: var(--radius-full);
      display: inline-flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      border: none;
      white-space: nowrap;
      transition: all 0.25s ease;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
      font-family: var(--font-main);
    }}
    .inside-cta-btn:hover {{
      background: var(--color-primary-light);
      color: var(--color-primary);
      transform: translateY(-2px);
    }}

    /* ==========================================================================
       7. کارت‌های مقالات دارای تصاویر شاخص بالینی (Editorial Cards with Images)
       ========================================================================== */
    .editorial-cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr));
      gap: 24px;
      margin-bottom: 50px;
    }}
    .magazine-article-card {{
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      transition: all 0.25s ease;
    }}
    .magazine-article-card:hover {{
      border-color: var(--color-primary);
      box-shadow: var(--shadow-card-hover);
      transform: translateY(-3px);
    }}
    .card-thumb-wrap {{
      width: 100%;
      height: 195px;
      position: relative;
      overflow: hidden;
      background: #E2E8F0;
    }}
    .card-thumb-wrap img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }}
    .magazine-article-card:hover .card-thumb-wrap img {{
      transform: scale(1.05);
    }}
    .thumb-tag-badge {{
      position: absolute;
      top: 12px;
      right: 12px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      padding: 4px 12px;
      border-radius: var(--radius-full);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--color-primary);
      box-shadow: 0 2px 8px rgba(0,0,0,0.12);
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .thumb-readtime-badge {{
      position: absolute;
      top: 12px;
      left: 12px;
      background: rgba(15, 23, 42, 0.75);
      color: #FFFFFF;
      padding: 3px 9px;
      border-radius: 6px;
      font-size: 11px;
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .article-card-body {{
      padding: 20px;
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: space-between;
    }}
    .mag-title {{
      font-size: 16px;
      font-weight: 800;
      color: var(--text-heading);
      line-height: 1.6;
      margin-bottom: 10px;
    }}
    .mag-summary {{
      font-size: 13px;
      color: var(--text-body);
      line-height: 1.8;
      margin-bottom: 16px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .mag-author-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--border-light);
      padding-top: 12px;
      font-size: 12.5px;
      color: var(--text-secondary);
    }}
    .doctor-avatar-circle {{
      width: 30px;
      height: 30px;
      border-radius: 50%;
      object-fit: cover;
      border: 1.5px solid var(--color-primary);
    }}

    /* ==========================================================================
       8. مگامنو کامل تمام دپارتمان‌ها و زیردسته‌ها (Mega Menu Modal)
       ========================================================================== */
    .mega-modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }}
    .mega-modal-box {{
      background: #FFFFFF;
      border-radius: var(--radius-xl);
      max-width: 1080px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 32px;
      box-shadow: var(--shadow-lg);
      position: relative;
    }}
    .mega-modal-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 16px;
      margin-bottom: 24px;
    }}
    .mega-modal-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
      gap: 20px;
    }}
    .mega-cat-column {{
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      padding: 16px;
      border: 1px solid var(--border-color);
    }}
    .mega-cat-col-title {{
      font-size: 14.5px;
      font-weight: 800;
      color: var(--text-heading);
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 10px;
    }}
    .mega-subcat-item {{
      font-size: 12px;
      color: var(--text-body);
      padding: 5px 8px;
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.15s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .mega-subcat-item:hover {{
      background: var(--color-primary-light);
      color: var(--color-primary);
    }}

    /* ==========================================================================
       9. ریدر اختصاصی مقاله و دراور نوبت‌دهی
       ========================================================================== */
    .reader-layout-grid {{
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 32px;
    }}
    @media (max-width: 900px) {{
      .reader-layout-grid {{
        grid-template-columns: 1fr;
      }}
    }}
    .reader-sidebar {{
      position: sticky;
      top: 140px;
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 20px;
      height: fit-content;
      box-shadow: var(--shadow-sm);
    }}
    .reader-article-body {{
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-xl);
      padding: 36px;
      box-shadow: var(--shadow-sm);
    }}
    .reader-hero-img {{
      width: 100%;
      max-height: 380px;
      object-fit: cover;
      border-radius: var(--radius-lg);
      margin-bottom: 24px;
    }}

    .reading-progress-bar {{
      position: fixed;
      top: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #0073FF 0%, #00E599 100%);
      z-index: 2200;
      width: 0%;
      transition: width 0.1s ease;
    }}

    /* Floating Back to Top Button */
    .back-to-top-btn {{
      position: fixed;
      bottom: 28px;
      left: 28px;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #FFFFFF;
      border: 1px solid var(--border-color);
      color: var(--color-primary);
      display: none;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.15);
      z-index: 900;
      transition: all 0.25s ease;
    }}
    .back-to-top-btn:hover {{
      background: var(--color-primary);
      color: #FFFFFF;
      transform: translateY(-3px);
      box-shadow: 0 8px 20px rgba(0, 115, 255, 0.3);
    }}

    .drawer-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.5);
      backdrop-filter: blur(4px);
      z-index: 1500;
      display: none;
      justify-content: flex-start;
    }}
    .drawer-body-box {{
      background: #FFFFFF;
      width: 440px;
      max-width: 90vw;
      height: 100%;
      padding: 32px;
      box-shadow: -4px 0 24px rgba(0, 0, 0, 0.15);
      overflow-y: auto;
    }}

    /* ==========================================================================
       سیستم ریسپانسیو پیشرفته و تطبیق‌پذیر با انواع نمایشگرها (Advanced RWD)
       موبایل، تبلت، لپ‌تاپ و صفحات فوق‌عریض مطابق با اصول responsive-design
       ========================================================================== */

    /* 1. تبلت‌ها و صفحات کوچک‌تر از 992px */
    @media (max-width: 992px) {{
      .main-header {{
        position: relative;
      }}
      .header-content {{
        flex-wrap: wrap;
        height: auto;
        padding: 12px 0;
        gap: 12px;
      }}
      .brand-title-text {{
        font-size: 17px;
      }}
      .brand-icon-box {{
        width: 38px;
        height: 38px;
      }}
      .header-search-bar {{
        order: 3;
        width: 100%;
        max-width: 100%;
      }}
      .category-navbar {{
        top: 0;
      }}
      .navbar-floating-dropdown {{
        right: 12px;
        left: 12px;
        padding: 20px 16px;
        max-height: 75dvh;
        overflow-y: auto;
      }}
      .dropdown-subcats-grid {{
        grid-template-columns: repeat(auto-fill, minmax(min(100%, 260px), 1fr));
      }}
      .hero-magazine-grid {{
        grid-template-columns: 1fr;
        gap: 20px;
      }}
      .reader-layout-grid {{
        grid-template-columns: 1fr;
        gap: 24px;
      }}
      .reader-sidebar {{
        position: relative;
        top: 0;
      }}
    }}

    /* 2. موبایل‌های استاندارد و صفحات کوچک‌تر از 640px */
    @media (max-width: 640px) {{
      .container {{
        padding: 0 16px;
      }}
      .main-wrapper {{
        padding-top: 18px;
        padding-bottom: 60px;
      }}
      .brand-subtitle {{
        display: none;
      }}
      .header-actions-group .btn-subtle-outline {{
        display: none;
      }}
      .btn-ui {{
        padding: 8px 14px;
        font-size: 12px;
      }}
      .mega-menu-trigger-btn span {{
        display: inline;
      }}
      .category-pills-list {{
        padding-top: 8px;
        padding-bottom: 14px;
      }}
      .hero-primary-card {{
        min-height: 330px;
        padding: 22px 18px;
      }}
      .hero-title-text {{
        font-size: 20px;
        line-height: 1.55;
      }}
      .hero-desc-text {{
        font-size: 13px;
        line-height: 1.7;
        max-width: 100%;
      }}
      .hero-secondary-grid {{
        grid-template-columns: 1fr;
        gap: 12px;
      }}
      .hero-secondary-card {{
        flex-direction: row;
        align-items: center;
      }}
      .secondary-img-wrap {{
        width: 120px;
        height: 105px;
        flex-shrink: 0;
      }}
      .secondary-card-body {{
        padding: 10px 12px;
      }}
      .secondary-title-text {{
        font-size: 12.5px;
        line-height: 1.5;
        margin-bottom: 4px;
      }}
      .clinical-trust-strip {{
        padding: 16px;
        gap: 14px;
      }}
      .axon-inside-banner {{
        padding: 26px 20px;
      }}
      .inside-text h3 {{
        font-size: 18px;
      }}
      .inside-text p {{
        font-size: 13px;
      }}
      .inside-cta-btn {{
        width: 100%;
        justify-content: center;
      }}
      .editorial-cards-grid {{
        gap: 18px;
      }}
      .card-thumb-wrap {{
        height: 180px;
      }}
      .reader-article-body {{
        padding: 22px 16px;
      }}
      .reader-hero-img {{
        max-height: 220px;
      }}
      .reader-article-body h1 {{
        font-size: 20px;
      }}
      .drawer-body-box {{
        width: 100%;
        max-width: 100vw;
        padding: 24px 18px;
      }}
      .mega-modal-box {{
        padding: 20px 16px;
        max-height: 90dvh;
      }}
      .back-to-top-btn {{
        bottom: 18px;
        left: 18px;
        width: 40px;
        height: 40px;
      }}
    }}

    /* 3. موبایل‌های خیلی باریک (Ultra-compact <= 400px) */
    @media (max-width: 400px) {{
      .container {{
        padding: 0 12px;
      }}
      .hero-secondary-card {{
        flex-direction: column;
      }}
      .secondary-img-wrap {{
        width: 100%;
        height: 120px;
      }}
      .hero-title-text {{
        font-size: 18px;
      }}
      .dept-card {{
        padding: 18px 14px;
      }}
      .quick-chips-row {{
        gap: 4px;
      }}
      .quick-chip-btn {{
        font-size: 11px;
        padding: 4px 9px;
      }}
    }}
  </style>
</head>
<body>

  <!-- نوار گرادینت پیشرفت مطالعه و پیمایش صفحه -->
  <div class="reading-progress-bar" id="readingProgressBar"></div>

  <!-- دکمه شناور بازگشت به بالای صفحه -->
  <button class="back-to-top-btn" id="backToTopBtn" onclick="scrollToTop()" title="بازگشت به بالای صفحه">
    {icons['chevron_down']}
  </button>

  <!-- ۱. هدر اصلی اپلیکیشن با پالت جستجوی هوشمند بالینی -->
  <header class="main-header">
    <div class="container header-content">
      <div class="brand-logo-wrap" onclick="showMainHub()">
        <div class="brand-icon-box">
          {icons['hospital']}
        </div>
        <div>
          <div class="brand-title-text">
            مجله سلامت پزشکآن
            <span class="badge">لایف</span>
          </div>
          <div class="brand-subtitle">دانشنامه و راهنمای تخصصی پزشکی بالینی</div>
        </div>
      </div>

      <!-- پالت جستجوی هوشمند و بی دغدغه -->
      <div class="header-search-bar">
        <div class="search-input-box">
          <input type="text" id="mainSearchInput" placeholder="جستجوی بیماری، علائم بالینی، آزمایش یا نام دارو..." onfocus="openSearchPalette()" oninput="handleSmartSearch(this.value)">
          <span class="search-icon">
            {icons['search']}
          </span>
          <button class="search-clear-btn" id="searchClearBtn" onclick="clearSearchInput()" title="پاک کردن">
            {icons['close']}
          </button>
        </div>

        <!-- پالت هوشمند با کلیدواژه‌های پرتکرار و نتایج دسته‌بندی‌شده -->
        <div class="search-flyout-palette" id="searchFlyoutPalette">
          <div id="quickTrendingQueriesBox">
            <div class="flyout-header-title">
              {icons['stethoscope']}
              <span>موضوعات پرتکرار و کلیدواژه‌های داغ بیماران:</span>
            </div>
            <div class="quick-chips-row">
              <span class="quick-chip-btn" onclick="executeQuickSearch('دیسک کمر')">درمان دیسک کمر</span>
              <span class="quick-chip-btn" onclick="executeQuickSearch('تفسیر آزمایش خون')">تفسیر آزمایش خون CBC</span>
              <span class="quick-chip-btn" onclick="executeQuickSearch('فشار خون')">کنترل فشار خون</span>
              <span class="quick-chip-btn" onclick="executeQuickSearch('غربالگری بارداری')">غربالگری بارداری NIPT</span>
              <span class="quick-chip-btn" onclick="executeQuickSearch('ریزش مو فیناستراید')">ریزش مو و فیناستراید</span>
              <span class="quick-chip-btn" onclick="executeQuickSearch('اسلیو معده')">جراحی اسلیو معده</span>
              <span class="quick-chip-btn" onclick="executeQuickSearch('ریفلاکس معده')">سوزش و رفلاکس معده</span>
              <span class="quick-chip-btn" onclick="executeQuickSearch('درد قفسه سینه')">تریاژ درد سینه</span>
            </div>
          </div>
          <div class="search-results-section" id="searchResultsSection" style="display:none;"></div>
        </div>
      </div>

      <div class="header-actions-group">
        <button class="btn-ui btn-subtle-outline" onclick="openBookingDrawer()">
          {icons['stethoscope']}
          <span>مشاوره با پزشک</span>
        </button>
        <button class="btn-ui btn-primary-gradient" onclick="openBookingDrawer()">
          {icons['calendar']}
          <span>نوبت‌دهی آنلاین</span>
        </button>
      </div>
    </div>
  </header>

  <!-- ۲. نوار کامل دسته‌بندی‌ها با اسکرول رنگ‌شده و فلش‌های ناوبری -->
  <nav class="category-navbar">
    <div class="container category-nav-inner">
      
      <!-- کانتینر اسکرول افقی با فلش‌های چپ و راست -->
      <div class="category-scroll-container">
        <button class="nav-scroll-btn" onclick="scrollCategoryList(1)" title="مشاهده موارد قبلی">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
        </button>

        <div class="category-pills-list" id="categoryPillsList">
          <!-- دکمه خانه مجله با آیکون بیمارستان -->
          <div class="nav-pill-item active" onclick="showMainHub()">
            {icons['hospital']}
            <span>صفحه اصلی مجله</span>
          </div>
          <!-- دسته‌بندی‌ها با آیکون‌های وکتور پزشکی در JS لود می‌شوند -->
        </div>

        <button class="nav-scroll-btn" onclick="scrollCategoryList(-1)" title="مشاهده موارد بعدی">
          <svg class="svg-icon" viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"/></svg>
        </button>
      </div>

      <!-- دکمه مگامنو با فونت رسمی وزیرمتن -->
      <button class="mega-menu-trigger-btn" onclick="openMegaMenuModal()">
        {icons['scan']}
        <span>فهرست کامل دپارتمان‌ها</span>
      </button>
    </div>

    <!-- پالت منوی آبشاری شناور (Floating Dropdown) خارج از کانتینر اسکرول -->
    <div class="navbar-floating-dropdown" id="floatingCategoryDropdown" onmouseenter="keepDropdownOpen()" onmouseleave="scheduleCloseDropdown()">
      <div class="dropdown-top-meta">
        <div>
          <h4 id="dropCatTitle">
            {icons['hospital']}
            <span>عنوان دپارتمان</span>
          </h4>
          <p id="dropCatDept" style="font-size:12px; color:var(--text-muted); margin-top:3px;"></p>
        </div>
        <span id="dropCatCountBadge" style="font-size:12px; background:var(--color-primary-light); color:var(--color-primary); padding:4px 12px; border-radius:var(--radius-full); font-weight:800;">
          زیردسته‌های تخصصی
        </span>
      </div>

      <div class="dropdown-subcats-grid" id="dropSubcatsGrid"></div>

      <div class="dropdown-bottom-footer">
        <div id="dropCatActionLink" style="color:var(--color-primary); font-weight:800; cursor:pointer; display:flex; align-items:center; gap:6px;">
          <span>مشاهده تمام مقالات و راهنماهای این دپارتمان</span>
          {icons['arrow_left']}
        </div>
        <button class="btn-ui btn-primary-gradient" style="padding:6px 16px; font-size:12px;" onclick="openBookingDrawer()">
          {icons['calendar']}
          <span>نوبت‌دهی آنلاین این بخش</span>
        </button>
      </div>
    </div>

    <!-- نوار چیپ‌های زیردسته‌های تخصصی فعال -->
    <div class="subcategory-strip" id="subcategoryStrip" style="display:none;">
      <div class="container" style="display:flex; align-items:center; gap:12px;">
        <span class="subcat-strip-label" id="subcatStripLabel">
          {icons['shield_check']}
          <span>زیردسته‌های این بخش:</span>
        </span>
        <div class="subcat-chips-scroll" id="subcatChipsScroll"></div>
      </div>
    </div>
  </nav>

  <!-- بدنه اصلی برنامه -->
  <main class="container main-wrapper">

    <!-- نمای ۱: هاب اصلی مجله -->
    <div id="viewHubMain">
      
      <!-- ۳. هیروی نامتقارن ۵ تایی مطابق با Axon Life -->
      <section style="margin-bottom: 36px;">
        <div class="hero-magazine-grid">
          
          <!-- کارت خبر اول و لید اصلی با تصویر شاخص باکیفیت -->
          <div class="hero-primary-card" style="background-image: url('{articles_js[0]['image']}');" onclick="openArticleReader('{articles_js[0]['id']}')">
            <div class="hero-primary-content">
              <span class="hero-tag-badge">
                {icons['spine']}
                <span>{articles_js[0]['tag']}</span>
              </span>
              <h2 class="hero-title-text">{articles_js[0]['title']}</h2>
              <p class="hero-desc-text">{articles_js[0]['summary']}</p>
              <div class="hero-meta-row">
                <span style="display:flex; align-items:center; gap:6px;">
                  <img src="{articles_js[0]['author']['avatar']}" class="doctor-avatar-circle" alt="{articles_js[0]['author']['name']}">
                  {articles_js[0]['author']['name']} ({articles_js[0]['author']['title']})
                </span>
                <span>•</span>
                <span style="display:flex; align-items:center; gap:6px;">
                  {icons['clock']}
                  {articles_js[0]['readTime']}
                </span>
              </div>
            </div>
          </div>

          <!-- ۴ کارت ثانویه هیرو با تصاویر شاخص و تگ‌های تخصصی -->
          <div class="hero-secondary-grid">
            
            <div class="hero-secondary-card" onclick="openArticleReader('{articles_js[1]['id']}')">
              <div class="secondary-img-wrap">
                <img src="{articles_js[1]['image']}" alt="{articles_js[1]['imageAlt']}">
                <span class="secondary-tag">
                  {icons['maternity']}
                  <span>{articles_js[1]['tag']}</span>
                </span>
              </div>
              <div class="secondary-card-body">
                <h3 class="secondary-title-text">{articles_js[1]['title']}</h3>
                <div class="secondary-meta-text">
                  <span>{articles_js[1]['author']['name']}</span>
                  <span>•</span>
                  <span>{articles_js[1]['readTime']}</span>
                </div>
              </div>
            </div>

            <div class="hero-secondary-card" onclick="openArticleReader('{articles_js[2]['id']}')">
              <div class="secondary-img-wrap">
                <img src="{articles_js[2]['image']}" alt="{articles_js[2]['imageAlt']}">
                <span class="secondary-tag">
                  {icons['heart']}
                  <span>{articles_js[2]['tag']}</span>
                </span>
              </div>
              <div class="secondary-card-body">
                <h3 class="secondary-title-text">{articles_js[2]['title']}</h3>
                <div class="secondary-meta-text">
                  <span>{articles_js[2]['author']['name']}</span>
                  <span>•</span>
                  <span>{articles_js[2]['readTime']}</span>
                </div>
              </div>
            </div>

            <div class="hero-secondary-card" onclick="openArticleReader('{articles_js[3]['id']}')">
              <div class="secondary-img-wrap">
                <img src="{articles_js[3]['image']}" alt="{articles_js[3]['imageAlt']}">
                <span class="secondary-tag">
                  {icons['spine']}
                  <span>{articles_js[3]['tag']}</span>
                </span>
              </div>
              <div class="secondary-card-body">
                <h3 class="secondary-title-text">{articles_js[3]['title']}</h3>
                <div class="secondary-meta-text">
                  <span>{articles_js[3]['author']['name']}</span>
                  <span>•</span>
                  <span>{articles_js[3]['readTime']}</span>
                </div>
              </div>
            </div>

            <div class="hero-secondary-card" onclick="openArticleReader('{articles_js[4]['id']}')">
              <div class="secondary-img-wrap">
                <img src="{articles_js[4]['image']}" alt="{articles_js[4]['imageAlt']}">
                <span class="secondary-tag">
                  {icons['heart']}
                  <span>{articles_js[4]['tag']}</span>
                </span>
              </div>
              <div class="secondary-card-body">
                <h3 class="secondary-title-text">{articles_js[4]['title']}</h3>
                <div class="secondary-meta-text">
                  <span>{articles_js[4]['author']['name']}</span>
                  <span>•</span>
                  <span>{articles_js[4]['readTime']}</span>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- ۴. نوار سه‌گانه اعتماد و قابلیت‌های کلینیکی -->
      <section class="clinical-trust-strip">
        <div class="trust-strip-item">
          <div class="strip-icon-box">
            {icons['shield_check']}
          </div>
          <div class="strip-details">
            <h4>بررسی و صحه‌گذاری پزشکی</h4>
            <p>مقالات مستقیماً توسط متخصصان دارای کد نظام پزشکی بازبینی و تایید می‌شوند.</p>
          </div>
        </div>
        <div class="trust-strip-item">
          <div class="strip-icon-box teal">
            {icons['hospital']}
          </div>
          <div class="strip-details">
            <h4>اتصال مستقیم به مطب و بیمارستان</h4>
            <p>امکان دریافت فوری نوبت آنلاین یا مشاوره بالینی با نویسنده مقاله.</p>
          </div>
        </div>
        <div class="trust-strip-item">
          <div class="strip-icon-box orange">
            {icons['stethoscope']}
          </div>
          <div class="strip-details">
            <h4>دانشنامه و مرجع سلامت</h4>
            <p>بیش از ۳۴۰ سرفصل تشخیصی، دارویی و درمانی به‌روز و بدون اصطلاحات پیچیده.</p>
          </div>
        </div>
      </section>

      <!-- ۵. کارت‌های هاب دسته‌بندی موضوعی با چیپ‌ها -->
      <section style="margin-bottom: 50px;">
        <div class="section-head-bar">
          <div class="section-title-wrap">
            <h2>
              {icons['hospital']}
              <span>دپارتمان‌های تخصصی مجله سلامت</span>
            </h2>
            <p>دسته‌بندی موضوعی مقالات علمی و تشخیصی بر اساس نیازهای درمانی بیماران</p>
          </div>
        </div>
        <div class="category-cards-grid" id="categoryCardsGrid"></div>
      </section>

      <!-- ۶. بنر تبدیل اکسون (InsideBanner) -->
      <section class="axon-inside-banner">
        <div class="inside-text">
          <h3>از آگاهی تا درمان: کنار شماییم</h3>
          <p>
            تمامی محتواهای این پایگاه توسط پزشکان فوق‌تخصص و با کد نظام پزشکی معتبر تهیه شده است. برای بررسی پرونده یا دریافت ویزیت تخصصی حضوری یا تله‌مدیسین، می‌توانید همین حالا اقدام فرمایید.
          </p>
        </div>
        <button class="inside-cta-btn" onclick="openBookingDrawer()">
          <span>درخواست نوبت پزشک متخصص</span>
          {icons['arrow_left']}
        </button>
      </section>

      <!-- ۷. تازه‌های مقالات همراه با تصاویر شاخص بالینی -->
      <section style="margin-bottom: 60px;">
        <div class="section-head-bar">
          <div class="section-title-wrap">
            <h2>
              {icons['stethoscope']}
              <span>تازه‌های سلامت و مقالات برگزیده</span>
            </h2>
            <p>راهنماهای خودمراقبتی و مقالات بررسی شده توسط پزشکان بیمارستان</p>
          </div>
        </div>
        <div class="editorial-cards-grid" id="editorialCardsGrid"></div>
      </section>

    </div>

    <!-- نمای ۲: جزییات دپارتمان و زیردسته‌ها -->
    <div id="viewCategoryArea" style="display: none; padding-bottom: 60px;">
      <div style="margin-bottom: 24px;">
        <button class="btn-ui btn-subtle-outline" onclick="showMainHub()">
          {icons['arrow_left']}
          <span>بازگشت به صفحه اصلی مجله</span>
        </button>
      </div>
      <div id="categoryDetailContent"></div>
    </div>

    <!-- نمای ۳: ریدر مطالعه کامل مقاله -->
    <div id="viewArticleReaderArea" style="display: none; padding-bottom: 60px;">
      <div class="reader-layout-grid" id="articleReaderContent"></div>
    </div>

  </main>

  <!-- ۸. مگامنو مدال فهرست کامل تمام دپارتمان‌ها و زیردسته‌ها -->
  <div class="mega-modal-backdrop" id="megaMenuModal" onclick="if(event.target===this) closeMegaMenuModal()">
    <div class="mega-modal-box">
      <div class="mega-modal-header">
        <div>
          <h3 style="font-size:18px; font-weight:900; color:var(--text-heading); display:flex; align-items:center; gap:8px;">
            {icons['hospital']}
            <span>راهنمای جامع دپارتمان‌ها و زیردسته‌های سلامت</span>
          </h3>
          <p style="font-size:12px; color:var(--text-secondary); margin-top:2px;">تمام بخش‌های تخصصی کلینیک و دانشنامه سلامت پزشکآن</p>
        </div>
        <button style="background:none; border:none; color:var(--text-secondary); cursor:pointer; font-size:20px;" onclick="closeMegaMenuModal()">
          {icons['close']}
        </button>
      </div>
      <div class="mega-modal-grid" id="megaModalGrid"></div>
    </div>
  </div>

  <!-- ۹. دراور رزرو و نوبت‌دهی آنلاین -->
  <div class="drawer-backdrop" id="bookingDrawerBackdrop" onclick="if(event.target===this) closeBookingDrawer()">
    <div class="drawer-body-box">
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; border-bottom: 1px solid var(--border-color); padding-bottom: 16px;">
        <div>
          <h3 style="font-size: 16px; font-weight: 800; color: var(--text-heading);">درخواست نوبت پزشک متخصص</h3>
          <p style="font-size: 11.5px; color: var(--color-primary);">اتصال مستقیم به سامانه نوبت‌دهی بیمارستان</p>
        </div>
        <button style="background:none; border:none; color:var(--text-secondary); cursor:pointer;" onclick="closeBookingDrawer()">
          {icons['close']}
        </button>
      </div>

      <form onsubmit="handleDrawerBooking(event)">
        <div style="margin-bottom: 18px;">
          <label style="display:block; font-size:12px; font-weight:700; color:var(--text-heading); margin-bottom:6px;">پزشک و دپارتمان تخصصی</label>
          <select id="selectDoctorDrawer" style="width:100%; background:var(--bg-subtle); border:1px solid var(--border-color); border-radius:8px; padding:10px; font-family:var(--font-main);" required></select>
        </div>
        <div style="margin-bottom: 18px;">
          <label style="display:block; font-size:12px; font-weight:700; color:var(--text-heading); margin-bottom:6px;">نوع ویزیت</label>
          <select style="width:100%; background:var(--bg-subtle); border:1px solid var(--border-color); border-radius:8px; padding:10px; font-family:var(--font-main);">
            <option>ویزیت حضوری در کلینیک بیمارستان</option>
            <option>مشاوره آنلاین تصویری (Telemedicine)</option>
            <option>تفسیر آزمایش‌ها و تصویربرداری ام‌آر‌آی</option>
          </select>
        </div>
        <div style="margin-bottom: 18px;">
          <label style="display:block; font-size:12px; font-weight:700; color:var(--text-heading); margin-bottom:6px;">نام و نام خانوادگی بیمار</label>
          <input type="text" id="patientNameField" placeholder="مثال: علیرضا حسینی" style="width:100%; background:var(--bg-subtle); border:1px solid var(--border-color); border-radius:8px; padding:10px; font-family:var(--font-main);" required>
        </div>
        <div style="margin-bottom: 24px;">
          <label style="display:block; font-size:12px; font-weight:700; color:var(--text-heading); margin-bottom:6px;">شماره تلفن همراه</label>
          <input type="tel" id="patientPhoneField" placeholder="۰۹۱۲xxxxxxx" style="width:100%; background:var(--bg-subtle); border:1px solid var(--border-color); border-radius:8px; padding:10px; font-family:var(--font-main);" required>
        </div>

        <button type="submit" class="btn-ui btn-primary-gradient" style="width: 100%; justify-content: center; padding: 13px; font-size: 14px;">
          تایید و ثبت نوبت بالینی
        </button>
      </form>

      <div id="bookingSuccessBox" style="display:none; margin-top:24px; text-align:center;">
        <div style="color:var(--color-teal); font-size:36px; margin-bottom:8px;">
          {icons['shield_check']}
        </div>
        <h4 style="font-size:16px; font-weight:800; color:var(--text-heading);">نوبت شما با موفقیت ثبت شد</h4>
        <p style="font-size:12.5px; color:var(--text-body); margin:8px 0;" id="bookingSuccessDetails"></p>
        <div style="background:var(--color-teal-light); border:1px dashed var(--color-teal); border-radius:8px; padding:10px; font-family:monospace; color:var(--color-teal); font-weight:700;" id="bookingCodeDetails"></div>
      </div>
    </div>
  </div>

  <!-- فوتر اپلیکیشن تم روز -->
  <footer class="main-footer">
    <div class="container">
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:32px; margin-bottom:36px;">
        <div>
          <h4 style="font-size:16px; font-weight:900; color:var(--text-heading); margin-bottom:12px;">مجله سلامت پزشکآن لایف</h4>
          <p style="line-height:1.8; color:var(--text-body);">
            پلتفرم هوشمند آموزش سلامت، سبک زندگی و پرونده الکترونیک. تمامی مقالات با بازبینی مستقیم پزشکان تاییدشده بیمارستان منتشر می‌گردد.
          </p>
        </div>
        <div>
          <h4 style="font-size:15px; font-weight:800; color:var(--text-heading); margin-bottom:12px;">دپارتمان‌های شاخص</h4>
          <ul style="list-style:none; display:flex; flex-direction:column; gap:8px;">
            <li><a href="#" onclick="showCategoryDetail(0)">درمان غیرجراحی ستون فقرات</a></li>
            <li><a href="#" onclick="showCategoryDetail(1)">سلامت زنان، بارداری و زایمان</a></li>
            <li><a href="#" onclick="showCategoryDetail(2)">بخش قلب، عروق و کنترل دیابت</a></li>
            <li><a href="#" onclick="showCategoryDetail(8)">دانشنامه جامع داروها</a></li>
          </ul>
        </div>
        <div>
          <h4 style="font-size:15px; font-weight:800; color:var(--text-heading); margin-bottom:12px;">سلب مسئولیت پزشکی</h4>
          <p style="line-height:1.8; color:var(--text-secondary);">
            اطلاعات این سامانه با هدف افزایش دانش سلامت و آگاهی بیماران فراهم شده است و هرگز جایگزین ویزیت، مشاوره یا تشخیص تخصصی پزشک معالج نخواهد بود.
          </p>
        </div>
      </div>
      <div style="border-top:1px solid var(--border-color); padding-top:20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <span>© تمامی حقوق متعلق به اکوسیستم سلامت دیجیتال پزشکآن است.</span>
        <span style="color:var(--color-primary); font-weight:600;">طراحی تم روز با هویت بصری Axon Life و آیکون‌های وکتور پزشکی</span>
      </div>
    </div>
  </footer>

  <!-- اسکریپت‌ها و داده‌های جامع -->
  <script>
    // دیکشنری آیکون‌های برداری پزشکی معتبر
    const medicalIcons = {json.dumps(icons, ensure_ascii=False)};

    // اطلاعات دسته‌بندی‌ها و تمام زیردسته‌ها
    const categoriesData = {json.dumps(categories_js, ensure_ascii=False)};

    // مقالات تحریریه به همراه تصاویر شاخص باکیفیت و متادیتا
    const articlesData = {json.dumps(articles_js, ensure_ascii=False)};

    const doctorsList = [
      {{ "id": "dr-radmanesh", "name": "دکتر مهران رادمنش", "dept": "متخصص جراحی مغز و ستون فقرات", "mc": "۱۱۴۲۸۵" }},
      {{ "id": "dr-tavakoli", "name": "دکتر سارا توکلی", "dept": "فوق تخصص زنان، زایمان و پریناتولوژی", "mc": "۹۸۳۴۱" }},
      {{ "id": "dr-salimi", "name": "دکتر حمیدرضا سلیمی", "dept": "متخصص قلب و عروق و آنژیوپلاستی", "mc": "۱۰۲۹۳۴" }},
      {{ "id": "dr-masoudi", "name": "دکتر الهام مسعودی", "dept": "متخصص پوست، مو و زیبایی", "mc": "۱۱۲۸۴۰" }},
      {{ "id": "dr-farahmand", "name": "دکتر نادر فرهمند", "dept": "فلوشیپ لاپاراسکوپی و گوارش", "mc": "۸۵۴۱۲" }}
    ];

    let currentCategoryId = null;
    let dropdownCloseTimer = null;

    // راه‌اندازی صفحه
    function initPage() {{
      renderNavPills();
      renderCategoryCards();
      renderEditorialCards();
      renderMegaMenuContent();
      populateDoctorSelect();
      setupReadingProgress();
      setupGlobalClickListeners();
    }}

    // رندر نوار دسته‌بندی‌ها
    function renderNavPills() {{
      const list = document.getElementById('categoryPillsList');
      const homePill = list.firstElementChild;
      list.innerHTML = '';
      if (homePill) list.appendChild(homePill);

      categoriesData.forEach((cat, idx) => {{
        const catIcon = medicalIcons[cat.iconKey] || medicalIcons['hospital'];
        const chevron = medicalIcons['chevron_down'];

        const pill = document.createElement('div');
        pill.className = 'nav-pill-item';
        pill.id = `navPill_${{idx}}`;
        pill.innerHTML = `
          ${{catIcon}}
          <span>${{cat.name}}</span>
          <span class="chevron-icon">${{chevron}}</span>
        `;

        // تعامل ماوس برای باز شدن فوری منوی آبشاری بدون باگ overflow
        pill.addEventListener('mouseenter', () => openCategoryDropdown(idx, pill));
        pill.addEventListener('mouseleave', () => scheduleCloseDropdown());
        pill.addEventListener('click', () => showCategoryDetail(idx));

        list.appendChild(pill);
      }});
    }}

    // باز کردن منوی آبشاری شناور در سطح Category Navbar
    function openCategoryDropdown(catIdx, pillElement) {{
      clearTimeout(dropdownCloseTimer);
      const dropdown = document.getElementById('floatingCategoryDropdown');
      const cat = categoriesData[catIdx];
      if (!cat) return;

      // هایلایت کردن پیل فعال
      document.querySelectorAll('.nav-pill-item').forEach(p => p.classList.remove('hover-active'));
      if (pillElement) pillElement.classList.add('hover-active');

      const catIcon = medicalIcons[cat.iconKey] || medicalIcons['hospital'];

      // تنظیم سربرگ منوی آبشاری
      document.getElementById('dropCatTitle').innerHTML = `
        ${{catIcon}}
        <span>${{cat.name}}</span>
      `;
      document.getElementById('dropCatDept').textContent = cat.dept;
      document.getElementById('dropCatCountBadge').textContent = `${{cat.subcategories.length}} زیردسته و خدمت تخصصی`;

      // رندر گرید زیردسته‌ها
      const grid = document.getElementById('dropSubcatsGrid');
      grid.innerHTML = (cat.subcategories || []).map(sub => `
        <div class="dropdown-subcat-card" onclick="selectSubcategoryFromDropdown(${{catIdx}}, '${{sub.title}}')">
          <div class="dropdown-subcat-title">
            ${{medicalIcons['shield_check']}}
            <span>${{sub.title}}</span>
          </div>
          <div class="dropdown-subcat-desc">${{sub.desc}}</div>
        </div>
      `).join('');

      document.getElementById('dropCatActionLink').onclick = () => {{
        closeCategoryDropdown();
        showCategoryDetail(catIdx);
      }};

      dropdown.style.display = 'block';
    }}

    function keepDropdownOpen() {{
      clearTimeout(dropdownCloseTimer);
    }}

    function scheduleCloseDropdown() {{
      dropdownCloseTimer = setTimeout(() => {{
        closeCategoryDropdown();
      }}, 180);
    }}

    function closeCategoryDropdown() {{
      const dropdown = document.getElementById('floatingCategoryDropdown');
      if (dropdown) dropdown.style.display = 'none';
      document.querySelectorAll('.nav-pill-item').forEach(p => p.classList.remove('hover-active'));
    }}

    function selectSubcategoryFromDropdown(catIdx, subTitle) {{
      closeCategoryDropdown();
      showCategoryDetail(catIdx);
      setTimeout(() => {{
        searchKeyword(subTitle);
      }}, 150);
    }}

    // پیمایش افقی نوار دسته‌بندی‌ها با کلیک روی فلش‌ها
    function scrollCategoryList(direction) {{
      const list = document.getElementById('categoryPillsList');
      const step = 280 * direction;
      list.scrollBy({{ left: step, behavior: 'smooth' }});
    }}

    // رندر کارت‌های هاب موضوعی
    function renderCategoryCards() {{
      const grid = document.getElementById('categoryCardsGrid');
      grid.innerHTML = '';
      categoriesData.forEach((cat, idx) => {{
        const card = document.createElement('div');
        card.className = 'dept-card';

        const catIcon = medicalIcons[cat.iconKey] || medicalIcons['hospital'];

        let chipsHtml = '';
        if (cat.chips) {{
          chipsHtml = cat.chips.map(chip => `
            <span class="dept-chip" onclick="searchKeyword('${{chip}}')">${{chip}}</span>
          `).join('');
        }}

        card.innerHTML = `
          <div>
            <div class="dept-card-header">
              <div class="dept-card-icon">${{catIcon}}</div>
              <div class="dept-card-meta">
                <h3>${{cat.name}}</h3>
                <span>${{cat.dept}}</span>
              </div>
            </div>
            <p class="dept-card-desc">${{cat.desc}}</p>
            <div class="dept-chips-list">${{chipsHtml}}</div>
          </div>
          <div class="dept-card-footer">
            <span class="dept-count-badge">${{cat.subcategories.length}} زیردسته و خدمت تخصصی</span>
            <button class="dept-view-link" onclick="showCategoryDetail(${{idx}})">
              <span>مشاهده مقالات این بخش</span>
              ${{medicalIcons['arrow_left']}}
            </button>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    // رندر کارت‌های مقالات با تصاویر شاخص باکیفیت
    function renderEditorialCards() {{
      const grid = document.getElementById('editorialCardsGrid');
      grid.innerHTML = '';
      articlesData.forEach(art => {{
        const card = document.createElement('div');
        card.className = 'magazine-article-card';
        card.onclick = () => openArticleReader(art.id);

        const artIcon = medicalIcons[art.categoryIcon] || medicalIcons['stethoscope'];

        card.innerHTML = `
          <div class="card-thumb-wrap">
            <img src="${{art.image}}" alt="${{art.imageAlt || art.title}}" loading="lazy">
            <span class="thumb-tag-badge">
              ${{artIcon}}
              <span>${{art.tag || 'مقاله بالینی'}}</span>
            </span>
            <span class="thumb-readtime-badge">
              ${{medicalIcons['clock']}}
              <span>${{art.readTime}}</span>
            </span>
          </div>

          <div class="article-card-body">
            <div>
              <h3 class="mag-title">${{art.title}}</h3>
              <p class="mag-summary">${{art.summary}}</p>
            </div>
            <div class="mag-author-footer">
              <span style="display:flex; align-items:center; gap:8px;">
                <img src="${{art.author.avatar}}" class="doctor-avatar-circle" alt="${{art.author.name}}">
                <span>${{art.author.name}}</span>
              </span>
              <span style="color:var(--color-primary); font-weight:700; display:inline-flex; align-items:center; gap:4px;">
                مطالعه کامل
                ${{medicalIcons['arrow_left']}}
              </span>
            </div>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    // رندر محتوای مگامنو جامع
    function renderMegaMenuContent() {{
      const grid = document.getElementById('megaModalGrid');
      grid.innerHTML = '';
      categoriesData.forEach((cat, idx) => {{
        const col = document.createElement('div');
        col.className = 'mega-cat-column';

        const catIcon = medicalIcons[cat.iconKey] || medicalIcons['hospital'];

        let subList = '';
        (cat.subcategories || []).forEach(sub => {{
          subList += `
            <div class="mega-subcat-item" onclick="selectSubcategoryFromModal(${{idx}}, '${{sub.title}}')">
              ${{medicalIcons['shield_check']}}
              <span>${{sub.title}}</span>
            </div>
          `;
        }});

        col.innerHTML = `
          <div class="mega-cat-col-title" onclick="showCategoryDetailFromModal(${{idx}})" style="cursor:pointer;">
            ${{catIcon}}
            <span>${{cat.name}}</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:4px;">
            ${{subList}}
          </div>
        `;
        grid.appendChild(col);
      }});
    }}

    function selectSubcategoryFromModal(catIdx, subTitle) {{
      closeMegaMenuModal();
      showCategoryDetail(catIdx);
      setTimeout(() => {{
        searchKeyword(subTitle);
      }}, 150);
    }}

    function showCategoryDetailFromModal(catIdx) {{
      closeMegaMenuModal();
      showCategoryDetail(catIdx);
    }}

    function openMegaMenuModal() {{
      document.getElementById('megaMenuModal').style.display = 'flex';
    }}
    function closeMegaMenuModal() {{
      document.getElementById('megaMenuModal').style.display = 'none';
    }}

    // به‌روزرسانی نوار زیردسته‌های پویا
    function updateSubcategoryStrip(catIdx) {{
      const strip = document.getElementById('subcategoryStrip');
      const label = document.getElementById('subcatStripLabel');
      const scroll = document.getElementById('subcatChipsScroll');

      if (catIdx === null || catIdx === undefined) {{
        strip.style.display = 'none';
        return;
      }}

      const cat = categoriesData[catIdx];
      if (!cat) return;

      label.innerHTML = `
        ${{medicalIcons[cat.iconKey] || medicalIcons['hospital']}}
        <span>زیردسته‌های ${{cat.name}}:</span>
      `;

      scroll.innerHTML = '';
      (cat.subcategories || []).forEach(sub => {{
        const pill = document.createElement('span');
        pill.className = 'subcat-pill';
        pill.textContent = sub.title;
        pill.onclick = () => searchKeyword(sub.title);
        scroll.appendChild(pill);
      }});

      strip.style.display = 'block';
    }}

    // نمایش صفحه جزییات دپارتمان
    function showCategoryDetail(idx) {{
      const cat = categoriesData[idx];
      if (!cat) return;
      currentCategoryId = idx;
      window.scrollTo({{ top: 0, behavior: 'smooth' }});

      document.getElementById('viewHubMain').style.display = 'none';
      document.getElementById('viewArticleReaderArea').style.display = 'none';
      document.getElementById('viewCategoryArea').style.display = 'block';

      updateSubcategoryStrip(idx);

      const catIcon = medicalIcons[cat.iconKey] || medicalIcons['hospital'];

      let subcatsCardsHtml = (cat.subcategories || []).map(sub => `
        <div class="dropdown-subcat-card" onclick="searchKeyword('${{sub.title}}')">
          <div class="dropdown-subcat-title">
            ${{medicalIcons['shield_check']}}
            <span>${{sub.title}}</span>
          </div>
          <div class="dropdown-subcat-desc">${{sub.desc}}</div>
        </div>
      `).join('');

      let chipsHtml = (cat.chips || []).map(c => `
        <span class="dept-chip" onclick="searchKeyword('${{c}}')">${{c}}</span>
      `).join('');

      document.getElementById('categoryDetailContent').innerHTML = `
        <div style="background:#FFFFFF; border:1px solid var(--border-color); border-radius:var(--radius-xl); padding:36px; margin-bottom:32px; box-shadow:var(--shadow-sm);">
          <div style="display:flex; align-items:center; gap:16px; margin-bottom:14px;">
            <div class="dept-card-icon" style="width:54px; height:54px; font-size:26px;">${{catIcon}}</div>
            <div>
              <h2 style="font-size:22px; font-weight:900; color:var(--text-heading);">${{cat.name}}</h2>
              <span style="font-size:12px; color:var(--text-secondary);">${{cat.dept}}</span>
            </div>
          </div>
          <p style="font-size:14.5px; color:var(--text-body); line-height:1.8; margin-bottom:20px;">${{cat.desc}}</p>
          
          <h4 style="font-size:14px; font-weight:800; color:var(--text-heading); margin-bottom:12px;">زیردسته‌ها و خدمات کلینیکی این دپارتمان:</h4>
          <div class="dropdown-subcats-grid" style="margin-bottom:24px;">
            ${{subcatsCardsHtml}}
          </div>

          <div style="margin-bottom:20px;">
            <h4 style="font-size:13px; font-weight:700; color:var(--text-heading); margin-bottom:8px;">موضوعات پرتکرار و کلیدواژه‌های جستجو:</h4>
            <div class="dept-chips-list">${{chipsHtml}}</div>
          </div>
          <button class="btn-ui btn-primary-gradient" onclick="openBookingDrawer()">
            ${{medicalIcons['calendar']}}
            <span>دریافت نوبت از متخصصان این دپارتمان</span>
          </button>
        </div>

        <div class="section-head-bar">
          <h3 style="font-size:18px; font-weight:800; color:var(--text-heading);">مقالات منتشر شده در این دپارتمان</h3>
        </div>
        <div class="editorial-cards-grid" id="catArticlesList"></div>
      `;

      // فیلتر مقالات مربوط به این دسته‌بندی
      const grid = document.getElementById('catArticlesList');
      const filtered = articlesData.filter(a => a.categoryName.includes(cat.name) || cat.name.includes(a.categoryName));
      const toShow = filtered.length ? filtered : articlesData.slice(0, 4);

      toShow.forEach(art => {{
        const card = document.createElement('div');
        card.className = 'magazine-article-card';
        card.onclick = () => openArticleReader(art.id);
        const artIcon = medicalIcons[art.categoryIcon] || medicalIcons['stethoscope'];
        card.innerHTML = `
          <div class="card-thumb-wrap">
            <img src="${{art.image}}" alt="${{art.title}}">
            <span class="thumb-tag-badge">
              ${{artIcon}}
              <span>${{art.tag}}</span>
            </span>
          </div>
          <div class="article-card-body">
            <h3 class="mag-title">${{art.title}}</h3>
            <p class="mag-summary">${{art.summary}}</p>
            <div class="mag-author-footer">
              <span>${{art.author.name}}</span>
              <span style="color:var(--color-primary); font-weight:700; display:inline-flex; align-items:center; gap:4px;">
                مطالعه مقاله
                ${{medicalIcons['arrow_left']}}
              </span>
            </div>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    // مطالعه کامل مقاله در ریدر اختصاصی
    function openArticleReader(id) {{
      const art = articlesData.find(a => a.id === id) || articlesData[0];
      window.scrollTo({{ top: 0, behavior: 'smooth' }});

      document.getElementById('viewHubMain').style.display = 'none';
      document.getElementById('viewCategoryArea').style.display = 'none';
      document.getElementById('viewArticleReaderArea').style.display = 'block';

      const artIcon = medicalIcons[art.categoryIcon] || medicalIcons['stethoscope'];

      const tocHtml = (art.sections || []).map(s => `
        <li style="margin-bottom:10px;"><a href="#${{s.id}}" style="color:var(--text-body); font-size:13px; font-weight:600;">• ${{s.title}}</a></li>
      `).join('');

      const sectionsHtml = (art.sections || []).map(s => `
        <div id="${{s.id}}" style="margin-bottom:28px;">
          <h3 style="font-size:18px; font-weight:800; color:var(--text-heading); margin-bottom:12px; border-right:3px solid var(--color-primary); padding-right:12px;">${{s.title}}</h3>
          <p style="font-size:15px; color:var(--text-body); line-height:1.9;">${{s.content}}</p>
        </div>
      `).join('');

      document.getElementById('articleReaderContent').innerHTML = `
        <aside class="reader-sidebar">
          <h4 style="font-size:14px; font-weight:800; color:var(--text-heading); margin-bottom:14px;">فهرست مطالب مقاله</h4>
          <ul style="list-style:none; padding:0; margin-bottom:24px;">${{tocHtml}}</ul>
          
          <div style="border-top:1px solid var(--border-color); padding-top:16px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
              <img src="${{art.author.avatar}}" class="doctor-avatar-circle" style="width:42px; height:42px;" alt="${{art.author.name}}">
              <div>
                <h5 style="font-size:13px; font-weight:800; color:var(--text-heading);">${{art.author.name}}</h5>
                <span style="font-size:11px; color:var(--text-secondary);">${{art.author.title}}</span>
              </div>
            </div>
            <div style="font-size:11.5px; color:var(--color-teal); background:var(--color-teal-light); padding:4px 8px; border-radius:6px; margin-bottom:12px; display:inline-flex; align-items:center; gap:4px;">
              ${{medicalIcons['shield_check']}}
              <span>کد نظام پزشکی: ${{art.author.mc}}</span>
            </div>
            <button class="btn-ui btn-primary-gradient" style="width:100%; justify-content:center; font-size:12px; padding:8px 12px;" onclick="openBookingDrawer()">
              ${{medicalIcons['stethoscope']}}
              <span>درخواست مشاوره با نویسنده</span>
            </button>
          </div>
        </aside>

        <article class="reader-article-body">
          <img src="${{art.image}}" class="reader-hero-img" alt="${{art.title}}">
          
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
            <span class="hero-tag-badge">
              ${{artIcon}}
              <span>${{art.tag}}</span>
            </span>
            <span style="font-size:12px; color:var(--text-secondary);">آخرین بازبینی علمی: ${{art.lastReviewed}}</span>
          </div>

          <h1 style="font-size:24px; font-weight:900; color:var(--text-heading); margin-bottom:16px; line-height:1.5;">${{art.title}}</h1>
          <div style="background:var(--bg-subtle); border-right:4px solid var(--color-primary); padding:16px; border-radius:8px; margin-bottom:28px; font-size:14.5px; color:var(--text-body); line-height:1.8;">
            ${{art.summary}}
          </div>

          <div>${{sectionsHtml}}</div>

          <div style="background:var(--bg-subtle); border-radius:var(--radius-lg); padding:24px; margin-top:36px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;">
            <div>
              <h4 style="font-size:15px; font-weight:800; color:var(--text-heading); margin-bottom:4px;">نیاز به بررسی دقیق‌تر پرونده پزشکی خود دارید؟</h4>
              <p style="font-size:12.5px; color:var(--text-secondary);">می‌توانید مستقیماً آزمایش‌ها و گزارش ام‌آر‌آی خود را برای پزشک مربوطه ارسال فرمایید.</p>
            </div>
            <button class="btn-ui btn-primary-gradient" onclick="openBookingDrawer()">
              ${{medicalIcons['calendar']}}
              <span>رزرو ویزیت آنلاین یا حضوری</span>
            </button>
          </div>
        </article>
      `;
    }}

    // بازگشت به صفحه اصلی مجله
    function showMainHub() {{
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
      document.getElementById('viewCategoryArea').style.display = 'none';
      document.getElementById('viewArticleReaderArea').style.display = 'none';
      document.getElementById('viewHubMain').style.display = 'block';
      updateSubcategoryStrip(null);
    }}

    // کنترل نوار پیشرفت مطالعه و دکمه بازگشت به بالا
    function setupReadingProgress() {{
      const backBtn = document.getElementById('backToTopBtn');
      window.addEventListener('scroll', () => {{
        const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        document.getElementById('readingProgressBar').style.width = scrolled + '%';

        if (winScroll > 280) {{
          backBtn.style.display = 'flex';
        }} else {{
          backBtn.style.display = 'none';
        }}
      }});
    }}

    function scrollToTop() {{
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // ==========================================================================
    // سیستم جستجوی پیشرفته و بی دغدغه بالینی
    // ==========================================================================
    function openSearchPalette() {{
      document.getElementById('searchFlyoutPalette').style.display = 'block';
    }}

    function clearSearchInput() {{
      const input = document.getElementById('mainSearchInput');
      input.value = '';
      document.getElementById('searchClearBtn').style.display = 'none';
      document.getElementById('quickTrendingQueriesBox').style.display = 'block';
      document.getElementById('searchResultsSection').style.display = 'none';
      input.focus();
    }}

    function executeQuickSearch(query) {{
      const input = document.getElementById('mainSearchInput');
      input.value = query;
      handleSmartSearch(query);
      input.focus();
    }}

    function handleSmartSearch(query) {{
      const clearBtn = document.getElementById('searchClearBtn');
      const trendingBox = document.getElementById('quickTrendingQueriesBox');
      const resSection = document.getElementById('searchResultsSection');

      if (!query || query.trim().length === 0) {{
        clearBtn.style.display = 'none';
        trendingBox.style.display = 'block';
        resSection.style.display = 'none';
        return;
      }}

      clearBtn.style.display = 'flex';
      trendingBox.style.display = 'none';
      resSection.style.display = 'block';

      const q = query.trim().toLowerCase();

      // ۱. تطبیق دپارتمان‌ها
      let matchedCats = [];
      categoriesData.forEach((c, idx) => {{
        if (c.name.toLowerCase().includes(q) || c.desc.toLowerCase().includes(q)) {{
          matchedCats.push({{ title: c.name, sub: c.dept, act: () => {{ closeSearchPalette(); showCategoryDetail(idx); }} }});
        }}
      }});

      // ۲. تطبیق زیردسته‌ها
      let matchedSubcats = [];
      categoriesData.forEach((c, cIdx) => {{
        (c.subcategories || []).forEach(sub => {{
          if (sub.title.toLowerCase().includes(q) || sub.desc.toLowerCase().includes(q)) {{
            matchedSubcats.push({{ title: sub.title, sub: `دپارتمان: ${{c.name}}`, act: () => {{ closeSearchPalette(); selectSubcategoryFromDropdown(cIdx, sub.title); }} }});
          }}
        }});
      }});

      // ۳. تطبیق مقالات
      let matchedArticles = [];
      articlesData.forEach(art => {{
        if (art.title.toLowerCase().includes(q) || art.summary.toLowerCase().includes(q)) {{
          matchedArticles.push({{ title: art.title, sub: `توسط ${{art.author.name}} (${{art.tag}})`, act: () => {{ closeSearchPalette(); openArticleReader(art.id); }} }});
        }}
      }});

      let html = '';

      if (matchedCats.length) {{
        html += `<div class="search-cat-group-label">دپارتمان‌های تخصصی:</div>`;
        matchedCats.forEach(m => {{
          html += `
            <div class="search-res-item" onclick="triggerSearchAction('${{encodeURI(m.title)}}')">
              <div class="search-res-title">${{highlightMatch(m.title, q)}}</div>
              <div class="search-res-sub">${{m.sub}}</div>
            </div>
          `;
        }});
      }}

      if (matchedSubcats.length) {{
        html += `<div class="search-cat-group-label">خدمات تشخیصی و زیردسته‌ها:</div>`;
        matchedSubcats.slice(0, 5).forEach(m => {{
          html += `
            <div class="search-res-item" onclick="triggerSearchAction('${{encodeURI(m.title)}}')">
              <div class="search-res-title">${{highlightMatch(m.title, q)}}</div>
              <div class="search-res-sub">${{m.sub}}</div>
            </div>
          `;
        }});
      }}

      if (matchedArticles.length) {{
        html += `<div class="search-cat-group-label">مقالات و راهنماهای پزشکی:</div>`;
        matchedArticles.slice(0, 5).forEach(m => {{
          html += `
            <div class="search-res-item" onclick="triggerSearchAction('${{encodeURI(m.title)}}')">
              <div class="search-res-title">${{highlightMatch(m.title, q)}}</div>
              <div class="search-res-sub">${{m.sub}}</div>
            </div>
          `;
        }});
      }}

      if (!matchedCats.length && !matchedSubcats.length && !matchedArticles.length) {{
        html = `
          <div style="padding:16px; text-align:center; color:var(--text-muted); font-size:13px;">
            <p>موردی برای «${{query}}» یافت نشد.</p>
            <p style="font-size:12px; margin-top:6px; color:var(--color-primary); cursor:pointer;" onclick="openBookingDrawer()">
              درخواست مشاوره مستقیم با پزشک در خصوص این موضوع
            </p>
          </div>
        `;
      }}

      window._activeSearchResults = [...matchedCats, ...matchedSubcats, ...matchedArticles];
      resSection.innerHTML = html;
    }}

    function highlightMatch(text, query) {{
      const idx = text.toLowerCase().indexOf(query.toLowerCase());
      if (idx === -1) return text;
      const match = text.substr(idx, query.length);
      return text.substring(0, idx) + '<b style="color:var(--color-primary); background:rgba(0,115,255,0.1); border-radius:3px;">' + match + '</b>' + text.substring(idx + query.length);
    }}

    function triggerSearchAction(encodedTitle) {{
      const title = decodeURI(encodedTitle);
      const item = (window._activeSearchResults || []).find(x => x.title === title);
      if (item && item.act) {{
        item.act();
      }}
    }}

    function closeSearchPalette() {{
      document.getElementById('searchFlyoutPalette').style.display = 'none';
    }}

    function searchKeyword(keyword) {{
      const input = document.getElementById('mainSearchInput');
      input.value = keyword;
      openSearchPalette();
      handleSmartSearch(keyword);
    }}

    function setupGlobalClickListeners() {{
      document.addEventListener('click', (e) => {{
        const searchBox = document.querySelector('.header-search-bar');
        if (searchBox && !searchBox.contains(e.target)) {{
          closeSearchPalette();
        }}
      }});

      // کلید میانبر اسلش یا کنترل+K برای تمرکز روی جستجو
      document.addEventListener('keydown', (e) => {{
        if ((e.key === '/' || (e.ctrlKey && e.key === 'k')) && document.activeElement.tagName !== 'INPUT') {{
          e.preventDefault();
          const input = document.getElementById('mainSearchInput');
          input.focus();
          openSearchPalette();
        }}
        if (e.key === 'Escape') {{
          closeSearchPalette();
          closeCategoryDropdown();
          closeMegaMenuModal();
          closeBookingDrawer();
        }}
      }});
    }}

    // دراور نوبت‌دهی آنلاین
    function openBookingDrawer() {{
      document.getElementById('bookingDrawerBackdrop').style.display = 'flex';
    }}
    function closeBookingDrawer() {{
      document.getElementById('bookingDrawerBackdrop').style.display = 'none';
    }}

    function populateDoctorSelect() {{
      const sel = document.getElementById('selectDoctorDrawer');
      sel.innerHTML = doctorsList.map(d => `
        <option value="${{d.id}}">${{d.name}} — ${{d.dept}} (نظام: ${{d.mc}})</option>
      `).join('');
    }}

    function handleDrawerBooking(e) {{
      e.preventDefault();
      const patient = document.getElementById('patientNameField').value;
      const docSel = document.getElementById('selectDoctorDrawer');
      const docName = docSel.options[docSel.selectedIndex].text;
      const code = 'PZK-' + Math.floor(100000 + Math.random() * 900000);

      document.getElementById('bookingSuccessDetails').textContent = `بیمار گرامی ${{patient}}، درخواست ویزیت شما برای ${{docName}} با موفقیت در سامانه ثبت شد.`;
      document.getElementById('bookingCodeDetails').textContent = `کد پیگیری تریاژ و نوبت: ${{code}}`;
      document.getElementById('bookingSuccessBox').style.display = 'block';
    }}

    // اجرای تابع اولیه
    document.addEventListener('DOMContentLoaded', initPage);
  </script>
</body>
</html>'''

with open('mag/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Updated mag/index.html with floating dropdown, custom scrollbar, search palette, and font fixes!')
