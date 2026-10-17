---
name: payload-cms
description: Production Payload CMS 3.0 architecture for Next.js fullstack applications. Manages medical collections, rich-text editing, media uploads, version history, doctor reviews, and Google Medical E-E-A-T schema generation.
keywords:
  - payload-cms
  - cms
  - nextjs
  - headless-cms
  - medical-editorial
  - database
  - collections
  - schema
  - media
  - permissions
license: MIT
---

# Payload CMS 3.0 Fullstack Engine for Next.js

A production-grade guide for implementing **Payload CMS 3.0** as a native, fullstack headless content management system running directly inside the Next.js App Router.

---

## 1. Architecture Overview

Payload 3.0 runs directly inside Next.js — there is no separate Node.js server. The admin dashboard is hosted under `/admin` and shares the same database and runtime environment.

### Installation:
```bash
npm install payload @payloadcms/next @payloadcms/richtext-lexical @payloadcms/db-postgres sharp
```

### Config File (`payload.config.ts`):
```typescript
import { buildConfig } from 'payload';
import { postgresAdapter } from '@payloadcms/db-postgres';
import { lexicalEditor } from '@payloadcms/richtext-lexical';
import { Articles } from './collections/Articles';
import { Doctors } from './collections/Doctors';
import { Pillars } from './collections/Pillars';
import { Media } from './collections/Media';

export default buildConfig({
  admin: {
    user: 'users',
    meta: {
      titleSuffix: '- پنل تحریریه مجله پزشکآن',
    },
  },
  collections: [Articles, Doctors, Pillars, Media],
  editor: lexicalEditor({}),
  secret: process.env.PAYLOAD_SECRET || 'SECRET_KEY',
  db: postgresAdapter({
    pool: { connectionString: process.env.DATABASE_URI },
  }),
  sharp,
});
```

---

## 2. Collections Schema for Medical Magazine

### Articles Collection (`collections/Articles.ts`):
```typescript
import { CollectionConfig } from 'payload';

export const Articles: CollectionConfig = {
  slug: 'articles',
  labels: { singular: 'مقاله', plural: 'مقالات' },
  admin: {
    useAsTitle: 'title',
    defaultColumns: ['title', 'pillar', 'status', 'publishedAt'],
  },
  versions: {
    drafts: true, // Enables Draft/Publish workflow
    maxPerDoc: 20,
  },
  fields: [
    {
      name: 'title',
      label: 'عنوان مقاله',
      type: 'text',
      required: true,
    },
    {
      name: 'slug',
      label: 'نامک (Slug سئو)',
      type: 'text',
      required: true,
      unique: true,
      index: true,
    },
    {
      name: 'pillar',
      label: 'پیلار سلامت (موضوع اصلی)',
      type: 'relationship',
      relationTo: 'pillars',
      required: true,
    },
    {
      name: 'featuredImage',
      label: 'تصویر شاخص',
      type: 'upload',
      relationTo: 'media',
      required: true,
    },
    {
      name: 'author',
      label: 'نویسنده محتوا',
      type: 'relationship',
      relationTo: 'users',
      required: true,
    },
    {
      name: 'medicalReviewer',
      label: 'پزشک ناظر (تأییدیه E-E-A-T)',
      type: 'relationship',
      relationTo: 'doctors',
      required: true,
    },
    {
      name: 'content',
      label: 'متن اصلی مقاله',
      type: 'richText',
      required: true,
    },
    {
      name: 'status',
      label: 'وضعیت انتشار',
      type: 'select',
      defaultValue: 'draft',
      options: [
        { label: 'پیش‌نویس اولیه', value: 'draft' },
        { label: 'در انتظار بازبینی پزشک', value: 'pending_medical_review' },
        { label: 'تأیید شده و منتشر', value: 'published' },
      ],
    },
    {
      name: 'seo',
      label: 'تنظیمات سئو پزشکی',
      type: 'group',
      fields: [
        { name: 'metaTitle', label: 'عنوان متا', type: 'text' },
        { name: 'metaDescription', label: 'توضیحات متا', type: 'textarea' },
        { name: 'medicalCondition', label: 'بیماری یا شرایط بالینی مرتبط', type: 'text' },
      ],
    },
  ],
};
```

### Media Collection (`collections/Media.ts`):
Automated optimization and image resizing:
```typescript
import { CollectionConfig } from 'payload';

export const Media: CollectionConfig = {
  slug: 'media',
  upload: {
    staticDir: 'public/media',
    imageSizes: [
      { name: 'thumbnail', width: 300, height: 200, position: 'centre' },
      { name: 'card', width: 640, height: 360, position: 'centre' },
      { name: 'hero', width: 1280, height: 720, position: 'centre' },
    ],
    adminThumbnail: 'thumbnail',
    mimeTypes: ['image/*'],
    formatOptions: {
      format: 'webp',
      options: { quality: 85 },
    },
  },
  fields: [
    { name: 'alt', label: 'متن جایگزین (Alt)', type: 'text', required: true },
    { name: 'caption', label: 'کپشن توضیحی تصویر', type: 'text' },
    { name: 'medicalSource', label: 'منبع تصویر پزشکی', type: 'text' },
  ],
};
```

---

## 3. Querying Inside Next.js (Local API)

Server Components query Payload directly in-process with zero network overhead:

```tsx
// app/mag/[slug]/page.tsx
import { getPayload } from 'payload';
import config from '@/payload.config';
import { notFound } from 'next/navigation';

export default async function ArticlePage({ params }: { params: { slug: string } }) {
  const payload = await getPayload({ config });
  
  const { docs } = await payload.find({
    collection: 'articles',
    where: {
      slug: { equals: params.slug },
      status: { equals: 'published' },
    },
    depth: 2, // Automatically populates doctor and media relations
  });

  const article = docs[0];
  if (!article) return notFound();

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold font-vazirmatn text-white">{article.title}</h1>
      {/* Article Content Rendered */}
    </main>
  );
}
```

---

## 4. Automatic Google Medical E-E-A-T Schema

Injects structured data for Google Medical Search guidelines:

```tsx
export function MedicalArticleSchema({ article, doctor }: { article: any; doctor: any }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'MedicalWebPage',
    headline: article.title,
    description: article.seo?.metaDescription,
    image: article.featuredImage?.sizes?.hero?.url || article.featuredImage?.url,
    datePublished: article.publishedAt,
    dateModified: article.updatedAt,
    author: {
      '@type': 'Person',
      name: article.author?.name,
    },
    reviewedBy: {
      '@type': 'Physician',
      name: doctor.name,
      medicalSpecialty: doctor.specialty,
      identifier: doctor.medicalCouncilId,
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```
