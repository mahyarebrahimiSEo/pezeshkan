---
name: refine-admin-framework
description: Build scalable, enterprise-grade admin panels, internal tools, and B2B dashboards using the Refine framework with Next.js. Covers data providers, access control (RBAC), auto-generated forms, tables, and auth integration.
keywords:
  - refine
  - admin-panel
  - dashboard
  - nextjs
  - react
  - crud
  - data-provider
  - rbac
  - internal-tools
license: MIT
---

# Refine Framework for Next.js Admin Panels

A production guide for integrating **Refine** (`refinedev/refine`), the leading React framework for building internal tools, CRM dashboards, and content management consoles with Next.js App Router.

---

## 1. Why Refine?

Refine decouples UI from business logic:
- **Zero Boilerplate CRUD:** Automatically handles state management, caching, pagination, sorting, and form validation.
- **Provider-Based Architecture:** Swappable `dataProvider`, `authProvider`, and `accessControlProvider`.
- **Works with any UI library:** Use with Tailwind CSS, Shadcn UI, Ant Design, or Mantine.
- **Server-Side Rendering:** First-class Next.js App Router support with SSR data fetching.

### Installation:
```bash
npm install @refinedev/core @refinedev/nextjs-router
```

---

## 2. Core Setup in Next.js (`app/(admin)/layout.tsx`)

```tsx
'use client';

import { Refine } from '@refinedev/core';
import routerProvider from '@refinedev/nextjs-router';
import { dataProvider } from '@/providers/data-provider';
import { authProvider } from '@/providers/auth-provider';
import { accessControlProvider } from '@/providers/access-control-provider';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <Refine
      routerProvider={routerProvider}
      dataProvider={dataProvider}
      authProvider={authProvider}
      accessControlProvider={accessControlProvider}
      resources={[
        {
          name: 'articles',
          list: '/admin/articles',
          create: '/admin/articles/create',
          edit: '/admin/articles/edit/:id',
          show: '/admin/articles/show/:id',
          meta: { label: 'مقالات مجله' },
        },
        {
          name: 'doctors',
          list: '/admin/doctors',
          create: '/admin/doctors/create',
          edit: '/admin/doctors/edit/:id',
          meta: { label: 'پزشکان ناظر' },
        },
        {
          name: 'pillars',
          list: '/admin/pillars',
          meta: { label: 'پیلارهای سلامت' },
        },
      ]}
    >
      <div className="flex min-h-screen bg-slate-950 font-vazirmatn text-slate-200" dir="rtl">
        {/* Admin Navigation & Content */}
        {children}
      </div>
    </Refine>
  );
}
```

---

## 3. Data Provider Pattern

Custom data provider connecting directly to your Next.js API routes or database:

```typescript
import { DataProvider } from '@refinedev/core';

export const dataProvider: DataProvider = {
  getList: async ({ resource, pagination, sorters, filters }) => {
    const params = new URLSearchParams();
    if (pagination) {
      params.append('page', String(pagination.current || 1));
      params.append('pageSize', String(pagination.pageSize || 10));
    }
    const response = await fetch(`/api/admin/${resource}?${params.toString()}`);
    const data = await response.json();
    return {
      data: data.items,
      total: data.total,
    };
  },
  getOne: async ({ resource, id }) => {
    const res = await fetch(`/api/admin/${resource}/${id}`);
    return { data: await res.json() };
  },
  create: async ({ resource, variables }) => {
    const res = await fetch(`/api/admin/${resource}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(variables),
    });
    return { data: await res.json() };
  },
  update: async ({ resource, id, variables }) => {
    const res = await fetch(`/api/admin/${resource}/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(variables),
    });
    return { data: await res.json() };
  },
  deleteOne: async ({ resource, id }) => {
    const res = await fetch(`/api/admin/${resource}/${id}`, { method: 'DELETE' });
    return { data: await res.json() };
  },
  getApiUrl: () => '/api/admin',
};
```

---

## 4. Access Control (RBAC) Provider

Ensure sensitive medical records or article publishing gates are strictly enforced:

```typescript
import { AccessControlProvider } from '@refinedev/core';

export const accessControlProvider: AccessControlProvider = {
  can: async ({ resource, action, params }) => {
    const role = localStorage.getItem('user_role') || 'author';

    // Rules
    if (role === 'admin') return { can: true };

    if (resource === 'articles') {
      if (action === 'publish' && role !== 'doctor') {
        return { can: false, reason: 'تنها پزشک ناظر یا مدیر مجاز به انتشار مقاله است' };
      }
      return { can: true };
    }

    if (resource === 'settings' && role !== 'admin') {
      return { can: false, reason: 'دسترسی محدود به مدیر کل' };
    }

    return { can: true };
  },
};
```

---

## 5. Instant Table & Form Usage

```tsx
'use client';

import { useTable, useForm } from '@refinedev/core';

export function ArticlesList() {
  const { tableQueryResult } = useTable({ resource: 'articles' });
  const articles = tableQueryResult?.data?.data || [];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">لیست مقالات مجله</h1>
      {/* Auto-managed data listing */}
    </div>
  );
}
```
