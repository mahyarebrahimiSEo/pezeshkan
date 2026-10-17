---
name: admin-dashboard-builder
description: Design and implement production-ready admin panels and operational dashboards for Next.js and React. Covers TanStack Table, Shadcn UI primitives, responsive sidebars, CRUD workflows, role-based navigation, clinical review queues, and dark mode tokens.
keywords:
  - admin-panel
  - dashboard
  - nextjs
  - react
  - shadcn
  - tanstack-table
  - crud
  - data-table
  - rbac
  - clinical-dark
  - rtl
license: MIT
---

# Admin Dashboard Builder for Next.js

A comprehensive engineering guide for building fast, maintainable, and visually cohesive admin dashboards, clinical editorial panels, and management consoles using Next.js (App Router), Tailwind CSS, Shadcn UI, and TanStack Table.

---

## 1. Dashboard Layout Architecture

Every robust admin panel relies on a 3-part layout:
1. **Collapsible Responsive Sidebar:** Sticky desktop navigation that collapses to icons or off-canvas drawer on mobile (`< 1024px`).
2. **Global Header:** Search/Command palette (`Cmd+K`), notifications bell, clinical alert status, and user avatar dropdown with role badge.
3. **Main Content Canvas:** Dynamic breadcrumbs, page header with primary CTA, filter toolbar, and responsive content area.

### Directory Structure (Next.js App Router):
```text
app/
├── (admin)/
│   ├── layout.tsx             # Root admin layout (Sidebar + Header + Shell)
│   ├── dashboard/page.tsx      # Overview metrics & quick actions
│   ├── articles/              # Magazine editorial table & editor
│   │   ├── page.tsx           # Articles list (TanStack Data Table)
│   │   ├── [id]/page.tsx      # Edit article
│   │   └── new/page.tsx       # Create article
│   ├── doctors/               # Medical reviewers & credentials
│   ├── media/                 # File library & image manager
│   └── settings/              # System & SEO configuration
```

---

## 2. Advanced Data Tables (TanStack Table v8)

Data tables are the core of an admin panel. Never use raw static HTML tables for large datasets.

### Essential Data Table Capabilities:
- **Server-Side Pagination & Sorting:** Keep payload light and fast.
- **Debounced Global & Column Filtering:** Instant search by title, slug, or author.
- **Faceted Status Filters:** Multi-select pills for article status (`پیش‌نویس`, `در انتظار بازبینی پزشک`, `منتشر شده`).
- **Batch Row Actions:** Delete, change status, or export selected rows.
- **Column Visibility Dropdown:** Let operators hide/show fields based on screen size.

### Sample Data Table Component:
```tsx
'use client';

import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
  createColumnHelper,
} from '@tanstack/react-table';
import { useState } from 'react';

interface ArticleItem {
  id: string;
  title: string;
  pillar: string;
  doctorReviewer?: string;
  status: 'draft' | 'pending_review' | 'published';
  updatedAt: string;
}

export function ArticlesDataTable({ data }: { data: ArticleItem[] }) {
  const [globalFilter, setGlobalFilter] = useState('');
  
  const columns = [
    {
      accessorKey: 'title',
      header: 'عنوان مقاله',
      cell: (info: any) => (
        <div className="font-medium text-white max-w-md truncate">
          {info.getValue()}
        </div>
      ),
    },
    {
      accessorKey: 'pillar',
      header: 'پیلار سلامت',
      cell: (info: any) => (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-cyan-950/60 text-cyan-300 border border-cyan-800/40">
          {info.getValue()}
        </span>
      ),
    },
    {
      accessorKey: 'status',
      header: 'وضعیت',
      cell: (info: any) => {
        const val = info.getValue();
        const styles = {
          published: 'bg-emerald-950/60 text-emerald-300 border-emerald-800/40',
          pending_review: 'bg-amber-950/60 text-amber-300 border-amber-800/40',
          draft: 'bg-slate-800 text-slate-300 border-slate-700',
        }[val] || 'bg-slate-800 text-slate-300';
        const labels = {
          published: 'منتشر شده',
          pending_review: 'در انتظار بازبینی',
          draft: 'پیش‌نویس',
        }[val];
        return (
          <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${styles}`}>
            {labels}
          </span>
        );
      },
    },
  ];

  const table = useReactTable({
    data,
    columns,
    state: { globalFilter },
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <div className="space-y-4">
      {/* Search Input */}
      <div className="flex items-center justify-between">
        <input
          value={globalFilter ?? ''}
          onChange={(e) => setGlobalFilter(e.target.value)}
          placeholder="جستجوی عنوان یا پیلار..."
          className="px-4 py-2 bg-slate-900 border border-slate-800 rounded-xl text-sm text-slate-200 focus:outline-none focus:border-cyan-500 w-72"
        />
      </div>
      {/* Table Surface */}
      <div className="rounded-xl border border-slate-800 bg-slate-950/60 overflow-hidden shadow-xl">
        <table className="w-full text-sm text-slate-300 text-start" dir="rtl">
          <thead className="bg-slate-900/80 text-xs text-slate-400 border-b border-slate-800">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th key={header.id} className="py-3 px-4 text-start font-medium">
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id} className="hover:bg-slate-900/40 transition-colors">
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="py-3 px-4">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

---

## 3. Clinical Dark DNA & Visual Tokens

In corporate or clinical tools, readability and eye strain prevention are critical:
- **Backgrounds:** Deep dark blue/slate surfaces (`#090D16`, `#0F172A`) instead of pitch black `#000000`.
- **Borders:** Translucent hairline borders (`rgba(255,255,255,0.08)` or `border-slate-800`).
- **Accent Hierarchy:**
  - Cyan (`#00FFFF`): Primary action buttons, active navigation links, and focus rings.
  - Emerald (`#00E599`): Approved status, published articles, healthy system status.
  - Amber (`#F59E0B`): Pending medical reviews, triage warnings.
  - Red (`#EF4444`): Destructive actions, rejected reviews, critical system alerts.

---

## 4. Role-Based Access Control (RBAC) in Admin

Define 3 distinct editorial roles:
1. **Author (نویسنده محتوا):** Can create, edit own drafts, and submit for review.
2. **Medical Reviewer (پزشک ناظر):** Can view submitted articles, verify medical facts, add review notes, and approve.
3. **Administrator (مدیر ارشد):** Full access to publish, delete, manage users, and configure settings.

```typescript
// Middleware or Page Gate
export function verifyAdminAccess(userRole: string, requiredRole: 'author' | 'doctor' | 'admin') {
  const roleHierarchy = { author: 1, doctor: 2, admin: 3 };
  return roleHierarchy[userRole] >= roleHierarchy[requiredRole];
}
```

---

## 5. Form Handling with Zod Validation

Use **React Hook Form** paired with **Zod** for robust schema validation:
```typescript
import { z } from 'zod';

export const articleFormSchema = z.object({
  title: z.string().min(5, 'عنوان مقاله باید حداقل ۵ کاراکتر باشد'),
  slug: z.string().regex(/^[a-z0-9-]+$/, 'نامک باید فقط شامل حروف کوچک، اعداد و خط تیره باشد'),
  pillarId: z.string().min(1, 'انتخاب پیلار سلامت الزامی است'),
  featuredImageUrl: z.string().url('آدرس تصویر شاخص نامعتبر است'),
  content: z.string().min(50, 'متن مقاله نباید کمتر از ۵۰ کاراکتر باشد'),
  doctorReviewerId: z.string().optional(),
});
```
