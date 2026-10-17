# -*- coding: utf-8 -*-
"""
Script to build the production-grade Pezeshkan Magazine (Day Mode)
with complete categories, interactive subcategories dropdown/mega-menu,
high-resolution medical featured images for all articles,
and 100% pure medical SVG icons from better-icons.
"""

import json

# Load icons
with open('mag/components/medical_icons.json', 'r', encoding='utf-8') as f:
    icons = json.load(f)

# Load pillars
with open('mag/content/pillars.json', 'r', encoding='utf-8') as f:
    pillars = json.load(f)

# Map category icons to medical SVG keys
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
            'desc': (b.get('clusters', [{}])[0].get('desc', ''))[:90] if b.get('clusters') else 'راهنمای بالینی و تشخیصی تخصصی'
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

# High resolution medical photography for articles
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
            {'id': 's1', 'title': 'علائم کلاسیک درد ایسکمیک قلبی', 'content': 'درد قلبی معمولاً احساس فشار و سنگینی شدید روی قفسه سینه است که به گردن، فک یا شانه و دست چپ منتشر می‌شود و ممکن است با تعریق سرد همراه باشد.'},
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

print('Total Categories prepared:', len(categories_js))
print('Total Articles prepared:', len(articles_js))
