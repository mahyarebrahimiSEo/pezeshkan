---
name: strapi-headless-cms
description: Production Strapi Headless CMS architecture, WordPress-like content management, Content-Type modeling, Next.js integration, media library handling, role-based access, and on-demand ISR revalidation.
keywords:
  - strapi
  - cms
  - headless-cms
  - wordpress-alternative
  - nextjs
  - content-types
  - media-library
  - rbac
  - rest-api
  - graphql
  - webhooks
license: MIT
---

# Strapi Headless CMS & WordPress-Like Architecture

A production-grade guide for implementing and integrating **Strapi** (`strapi/strapi`), the leading open-source headless CMS that provides an intuitive, all-in-one content management experience similar to WordPress, engineered to pair seamlessly with Next.js.

---

## 1. Why Strapi is the Modern WordPress Alternative

Strapi replicates the familiar and powerful WordPress editorial model while maintaining clean headless separation:

| WordPress Feature | Strapi Equivalent | Advantage in Strapi |
|---|---|---|
| نوشته‌ها و برگه‌ها (Posts & Pages) | Collection Types & Single Types | تعریف آزادانه فیلدها بدون محدودیت‌های قالب |
| کتابخانه رسانه (Media Library) | Upload Plugin & Media Library | مدیریت پوشه‌بندی، متادیتای سئو، تغییر سایز خودکار |
| افزونه ACF (Custom Fields) | Content-Type Builder | ساخت ویژوال انواع روابط، کامپوننت‌ها و فیلدهای بالینی |
| افزونه Yoast / RankMath | SEO Shared Component | تزریق استاندارد متاتگ‌ها و اسکیماهای پزشکی گوگل |
| کاربران و نقش‌ها (Roles) | Users & Permissions Plugin | تفکیک دقیق دسترسی نویسنده، پزشک ناظر و مدیر کل |
| خروجی API | Auto-generated REST & GraphQL | بدون پلاگین اضافی، سریع، با قابلیت فیلترهای عمیق |

---

## 2. Quick Setup & Project Architecture

### Initializing Strapi Backend:
```bash
npx create-strapi-app@latest backend --quickstart --typescript
```

### Directory Layout (Hybrid Frontend + Backend):
```text
pezeshkan_ecosystem/
├── frontend/ (pezeshkan_design)     # Next.js App Router (فرانت‌اند مجله و سایت)
│   ├── app/
│   │   ├── mag/                     # روت‌های مجله سلامت
│   │   └── api/revalidate/          # وب‌هوک بازسازی کش آنی
│   └── lib/strapi.ts                # کلاینت ارتباطی با استراپی
│
└── backend/                         # سامانه استراپی (پنل ادمین و دیتابیس)
    ├── config/                      # تنظیمات سرور، پایگاه‌داده و امنیت
    └── src/
        ├── api/                     # مدل‌های مقاله، پزشک و پیلارها
        └── components/              # کامپوننت‌های اشتراکی سئو و کادرهای بالینی
```

---

## 3. Medical Magazine Content-Type Schema

Inside Strapi's **Content-Type Builder**, define the core models:

### 1. `Article` (نوشته‌های مجله):
- `title` (Text - Short): عنوان فارسی مقاله
- `slug` (UID based on title): نامک سئو برای آدرس URL
- `excerpt` (Text - Long): چکیده بالینی مقاله
- `content` (Rich Text / Blocks): متن اصلی مقاله با ویرایشگر غنی
- `featuredImage` (Media - Single): تصویر شاخص با متن جایگزین
- `readingTime` (Integer): تخمین زمان مطالعه به دقیقه
- `pillar` (Relation): نسبت One-to-Many با مدل `Pillar`
- `medicalReviewer` (Relation): نسبت One-to-One با مدل `Doctor` (برای تایید E-E-A-T)
- `seo` (Component): متاتگ‌های سئو، کلمات کلیدی، عنوان شبکه‌های اجتماعی

### 2. `Doctor` (پزشکان ناظر و اعضای هیئت تحریریه):
- `name` (Text): نام و نام خانوادگی پزشک
- `avatar` (Media - Single): عکس پرسنلی رسمی
- `medicalCouncilId` (Text): کد نظام پزشکی معتبر
- `specialty` (Text): تخصص بالینی (مثلاً فوق‌تخصص قلب و عروق)
- `bio` (Text): معرفی و سوابق علمی

### 3. `Pillar` (۹ پیلار اصلی سلامت مجله):
- `title` (Text): نام پیلار (تغذیه، گوارش، قلب، سلامت روان، ...)
- `slug` (UID): شناسه انگلیسی پیلار
- `color` (Text): کد رنگ هویت بصری
- `icon` (Text / Media): نماد آیکون پیلار

---

## 4. Querying Strapi from Next.js (App Router)

Use `fetch` with deep population in Next.js Server Components:

```typescript
// lib/strapi.ts
const STRAPI_URL = process.env.NEXT_PUBLIC_STRAPI_URL || 'http://localhost:1337';
const STRAPI_TOKEN = process.env.STRAPI_API_TOKEN;

export async function fetchStrapi(path: string, urlParamsObject = {}, options = {}) {
  const queryString = new URLSearchParams(urlParamsObject).toString();
  const requestUrl = `${STRAPI_URL}/api${path}${queryString ? `?${queryString}` : ''}`;

  const response = await fetch(requestUrl, {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${STRAPI_TOKEN}`,
    },
    next: { revalidate: 3600 }, // 1 hour ISR cache default
    ...options,
  });

  if (!response.ok) {
    throw new Error(`خطا در برقراری ارتباط با استراپی: ${response.statusText}`);
  }

  return await response.json();
}
```

### Fetching a Magazine Article with Relations:
```tsx
// app/mag/[slug]/page.tsx
import { fetchStrapi } from '@/lib/strapi';
import { notFound } from 'next/navigation';

export default async function ArticlePage({ params }: { params: { slug: string } }) {
  // Deep populate relations (Pillar, Doctor, Featured Image, SEO)
  const query = {
    'filters[slug][$eq]': params.slug,
    'populate[featuredImage]': 'true',
    'populate[pillar]': 'true',
    'populate[medicalReviewer][populate]': 'avatar',
    'populate[seo]': 'true',
  };

  const { data } = await fetchStrapi('/articles', query);
  const article = data?.[0];

  if (!article) return notFound();

  return (
    <article className="container mx-auto px-4 py-12 max-w-4xl font-vazirmatn text-slate-200" dir="rtl">
      <h1 className="text-4xl font-black text-white leading-tight mb-4">{article.title}</h1>
      
      {/* Doctor Reviewer Badge */}
      {article.medicalReviewer && (
        <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-900 border border-slate-800 my-6">
          <span className="text-xs text-emerald-400 bg-emerald-950/60 px-2 py-1 rounded-md border border-emerald-800/40">
            تأیید شده توسط پزشک
          </span>
          <span className="text-sm text-slate-300 font-medium">
            دکتر {article.medicalReviewer.name} (نظام پزشکی: {article.medicalReviewer.medicalCouncilId})
          </span>
        </div>
      )}

      {/* Main Content */}
      <div className="prose prose-invert prose-cyan max-w-none text-slate-300 leading-8">
        {/* Render RichText blocks */}
      </div>
    </article>
  );
}
```

---

## 5. Instant Revalidation (On-Demand ISR Webhook)

When an editor clicks "Publish" in Strapi, Next.js instantly clears the cache and regenerates the page without waiting:

### Next.js Revalidation Route (`app/api/revalidate/route.ts`):
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { revalidatePath } from 'next/cache';

export async function POST(req: NextRequest) {
  const secret = req.nextUrl.searchParams.get('secret');
  
  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ message: 'توکن نامعتبر است' }, { status: 401 });
  }

  const body = await req.json();
  const slug = body?.entry?.slug;

  if (slug) {
    revalidatePath(`/mag/${slug}`);
    revalidatePath('/mag');
    return NextResponse.json({ revalidated: true, path: `/mag/${slug}` });
  }

  return NextResponse.json({ message: 'شناسه مقاله یافت نشد' }, { status: 400 });
}
```

### Strapi Webhook Settings:
In Strapi Admin $\to$ **Settings** $\to$ **Webhooks**:
- URL: `https://pezeshkan.com/api/revalidate?secret=YOUR_SECRET`
- Events: `entry.publish`, `entry.unpublish`, `entry.update`

---

## 6. Security & Production Checklist

1. **Role-Based Permissions (RBAC):**
   - In **Settings $\to$ Roles**: configure Public role to ONLY have `find` and `findOne` permissions for `Article`, `Pillar`, and `Doctor`.
   - Never expose draft articles to public routes.
2. **Media Optimization:**
   - Configure responsive breakpoints in `config/plugins.ts` for automatic WebP generation.
3. **CORS & CSRF:**
   - In `config/middlewares.ts`, whitelist only the Next.js production domain:
   ```javascript
   cors: {
     origin: ['http://localhost:3000', 'https://pezeshkan.com'],
   }
   ```
4. **Environment Variables:**
   - Secure `ADMIN_JWT_SECRET`, `API_TOKEN_SALT`, and database credentials in `.env`.
