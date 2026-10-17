---
name: tiptap-editorial-cms
description: Production Tiptap v2 headless rich-text editor and editorial CMS engine for Next.js. Provides Notion-style slash commands, drag-and-drop image uploading, medical callouts, automatic paste cleaning, and Persian RTL typography enforcement.
keywords:
  - tiptap
  - cms
  - editor
  - rich-text
  - prosemirror
  - novel
  - images
  - upload
  - typography
  - medical-editorial
  - rtl
  - nextjs
license: MIT
---

# Tiptap Editorial CMS & Rich Text Engine

A production-grade, headless rich-text editor and editorial publishing system based on **Tiptap v2** and **ProseMirror** for Next.js and React applications. Engineered specifically for professional publishing workflows, medical portals, and editorial magazines.

---

## 1. Core Architecture

Tiptap is completely headless — you control 100% of the UI, styling (Tailwind CSS), and markup output.

### Essential Packages:
```bash
npm install @tiptap/react @tiptap/pm @tiptap/starter-kit @tiptap/extension-image @tiptap/extension-link @tiptap/extension-placeholder @tiptap/extension-table @tiptap/extension-table-row @tiptap/extension-table-header @tiptap/extension-table-cell @tiptap/extension-underline @tiptap/extension-character-count
```

### Editor Instance Skeleton:
```tsx
'use client';

import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Image from '@tiptap/extension-image';
import Link from '@tiptap/extension-link';
import Placeholder from '@tiptap/extension-placeholder';
import Underline from '@tiptap/extension-underline';
import { ClinicalCallout } from './extensions/ClinicalCallout';
import { CleanPasteExtension } from './extensions/CleanPaste';

export function MedicalEditor({ initialContent, onChange }: { initialContent?: string; onChange: (html: string) => void }) {
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        heading: { levels: [2, 3, 4] }, // Reserve H1 for page hero
      }),
      Underline,
      Link.configure({
        openOnClick: false,
        HTMLAttributes: { class: 'text-cyan-400 underline underline-offset-4 hover:text-cyan-300' },
      }),
      Placeholder.configure({
        placeholder: 'محتوای مقاله را اینجا بنویسید یا برای درج امکانات کلید «/» را بزنید...',
      }),
      Image.configure({
        inline: false,
        HTMLAttributes: { class: 'rounded-xl border border-slate-700/60 shadow-lg mx-auto my-6 max-w-full' },
      }),
      ClinicalCallout,
      CleanPasteExtension,
    ],
    content: initialContent || '',
    editorProps: {
      attributes: {
        class: 'mag-prose prose prose-invert max-w-none min-h-[450px] p-6 focus:outline-none font-vazirmatn text-slate-200 leading-relaxed text-base',
        dir: 'rtl',
      },
    },
    onUpdate: ({ editor }) => {
      onChange(editor.getHTML());
    },
  });

  if (!editor) return null;

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/80 shadow-2xl backdrop-blur-xl">
      {/* Editor Toolbar & Floating Menus */}
      <EditorToolbar editor={editor} />
      <EditorContent editor={editor} />
    </div>
  );
}
```

---

## 2. Advanced Image Handling & Placement

Images are central to medical and editorial content. The editor supports:
1. **Drag-and-Drop & Clipboard Paste:** Automatic file interception and upload.
2. **Clinical Caption & Credit:** Captions rendered with `<figcaption>` under the image.
3. **Responsive Size Presets:** `default` (article width), `wide` (breaks grid margin), `full-bleed` (spans viewport).
4. **Lightbox Preview:** Click to inspect high-resolution clinical scans/infographics.

### Image Upload Interceptor:
```tsx
const handleImageUpload = async (file: File): Promise<string> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const res = await fetch('/api/mag/upload', {
    method: 'POST',
    body: formData,
  });
  
  if (!res.ok) throw new Error('بارگذاری تصویر با خطا مواجه شد');
  const data = await res.json();
  return data.url; // Returns WebP/optimized URL
};

// In editorProps:
handleDrop: (view, event, slice, moved) => {
  if (!moved && event.dataTransfer?.files?.length) {
    const file = event.dataTransfer.files[0];
    if (file.type.startsWith('image/')) {
      handleImageUpload(file).then(url => {
        const { schema } = view.state;
        const coordinates = view.posAtCoords({ left: event.clientX, top: event.clientY });
        if (coordinates) {
          const node = schema.nodes.image.create({ src: url, alt: file.name });
          const transaction = view.state.tr.insert(coordinates.pos, node);
          view.dispatch(transaction);
        }
      });
      return true;
    }
  }
  return false;
}
```

---

## 3. Intelligent Content Sanitization & Design Guardrail

The user often pastes content from Microsoft Word, Google Docs, Telegram, or scientific PDFs. Without normalization, messy inline CSS, arbitrary colors, and bad font styles destroy the design system.

### The CleanPaste Rule:
- **Strips Inline Styles:** Removes all `style="font-size:...; color:...; font-family:..."` attributes.
- **Normalizes Headings:** Downgrades pasted `H1` tags to `H2` or `H3` to preserve single-H1 SEO structure.
- **Cleans Line Breaks:** Replaces multiple blank paragraphs (`<p><br></p><p><br></p>`) with unified spacing.
- **Persian Typography Normalizer:**
  - Converts Arabic letters (ي $\to$ ی, ك $\to$ ک).
  - Replaces double spaces with single space.
  - Inserts Zero-Width Non-Joiner (ZWNJ / نیم‌فاصله) for common prefixes/suffixes (می‌شود، کتاب‌ها، نشان‌دهنده).
  - Formats standard Persian quotation marks (« ... »).
  - Sets numbers in tables and statistics to tabular numerals.

---

## 4. Custom Medical Extensions (Clinical DNA)

### A. Clinical Callout Node (`/callout`):
Specialized medical warning / triage alert blocks:
- `warning` (قرمز/کهربایی - احتیاط و عوارض جانبی)
- `advice` (سبز - توصیه تخصصی پزشک)
- `info` (فیروزه‌ای - ارجاع و آگاهی‌بخشی)

```tsx
import { Node, mergeAttributes } from '@tiptap/core';

export const ClinicalCallout = Node.create({
  name: 'clinicalCallout',
  group: 'block',
  content: 'block+',
  defining: true,
  
  addAttributes() {
    return {
      type: { default: 'info' }, // 'warning' | 'advice' | 'info'
    };
  },
  
  parseHTML() {
    return [{ tag: 'div[data-type="clinical-callout"]' }];
  },
  
  renderHTML({ node, HTMLAttributes }) {
    const type = node.attrs.type;
    const styles = {
      warning: 'border-amber-500/50 bg-amber-950/20 text-amber-200',
      advice: 'border-emerald-500/50 bg-emerald-950/20 text-emerald-200',
      info: 'border-cyan-500/50 bg-cyan-950/20 text-cyan-200',
    }[type] || 'border-cyan-500/50 bg-cyan-950/20 text-cyan-200';

    return [
      'div',
      mergeAttributes(HTMLAttributes, {
        'data-type': 'clinical-callout',
        class: `my-6 rounded-xl border p-4 backdrop-blur-md flex gap-3 ${styles}`,
      }),
      ['div', { class: 'shrink-0 mt-1' }, '⚠️'],
      ['div', { class: 'callout-content flex-1' }, 0],
    ];
  },
});
```

---

## 5. Slash Commands Menu (`/`)

Editors use the `/` key to quickly insert elements without lifting their hands from the keyboard:
- `/h2` $\to$ تیتر اصلی بخش (H2)
- `/h3` $\to$ زیرعنوان (H3)
- `/image` $\to$ آپلود تصویر پزشکی با کپشن
- `/alert` $\to$ کادر هشدار و توصیه بالینی
- `/table` $\to$ جدول دوز دارو و مشخصات بالینی
- `/quote` $\to$ نقل‌قول پزشک متخصص با تصویر و کد نظام پزشکی
- `/ref` $\to$ ارجاع به منبع علمی و شناسه PubMed

---

## 6. Rendering Clean Output in Next.js

```tsx
// Frontend Article Viewer Component
export function ArticleRenderer({ htmlContent }: { htmlContent: string }) {
  return (
    <article 
      className="mag-prose prose prose-invert prose-cyan max-w-none font-vazirmatn text-slate-300 leading-8 selection:bg-cyan-500/30 selection:text-cyan-200"
      dangerouslySetInnerHTML={{ __html: htmlContent }}
    />
  );
}
```
