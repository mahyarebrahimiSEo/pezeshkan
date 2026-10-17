---
name: responsive-design
description: Master responsive web design, mobile-first architecture, container queries, fluid typography, flexbox/grid adaptation, touch targets, and cross-device testing. Trigger when building or fixing responsive layouts, mobile views, tablet/desktop breakpoints, overflow bugs, or viewport adaptations.
keywords:
  - responsive
  - mobile-first
  - breakpoints
  - media-queries
  - container-queries
  - fluid-typography
  - touch-targets
  - flexbox
  - css-grid
  - layout
  - mobile
  - tablet
  - rtl
license: MIT
---

# Responsive Web Design (RWD) & Adaptive Layouts

Expert engineering patterns for building resilient, pixel-perfect responsive web interfaces that adapt gracefully across all device sizes — from 320px ultra-compact phones to 4K ultra-wide monitors.

---

## 1. Core Philosophy: Mobile-First Architecture

Always construct UI starting from the smallest viewport constraint (320px) and expand upwards using `min-width` queries.

- **Why Mobile-First:** Building desktop-first leads to overriding styles with clumsy `max-width` hacks that fight CSS cascade and increase bundle size. Mobile-first code is cleaner, lighter, and intrinsically responsive.
- **Breakpoint Standard:**
  - `xs`: `< 480px` — Compact phones (iPhone SE, Galaxy A series)
  - `sm`: `640px` — Large phones & mobile landscape
  - `md`: `768px` — Tablets (iPad portrait, large foldables)
  - `lg`: `1024px` — Tablets landscape & small laptops
  - `xl`: `1280px` — Standard desktop displays
  - `2xl`: `1536px` — Wide monitors & desktop workstations

```css
/* CORRECT: Mobile-first upward expansion */
.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}
```

---

## 2. Intrinsic Responsiveness (No Media Queries Needed)

Modern CSS provides tools that adapt without explicit breakpoint declarations:

### A. Auto-Fitting Responsive Grids
Automatically wraps items into columns based on minimum available width:
```css
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
  gap: 1.25rem;
}
```
*Note:* The `min(100%, 280px)` is critical to prevent grid blowouts on screens smaller than 280px.

### B. Flexbox Auto-Wrapping & Protection
```css
.badge-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

/* PREVENT FLEX-CHILD OVERFLOW: Essential for titles/ellipses */
.flex-item-content {
  min-width: 0; /* Prevents child from expanding beyond parent */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

---

## 3. Container Queries (`@container`)

Viewport queries measure the browser window; **Container Queries** measure the parent element. This enables components to adapt based on where they are placed (e.g., in a narrow 300px sidebar vs a wide 900px main area).

```css
/* 1. Define parent container */
.widget-wrapper {
  container-type: inline-size;
  container-name: widget;
}

/* 2. Style children based on container width */
@container widget (min-width: 450px) {
  .widget-card {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
}

@container widget (max-width: 449px) {
  .widget-card {
    display: flex;
    flex-direction: column;
  }
}
```

In Tailwind CSS:
```html
<div class="@container">
  <div class="flex flex-col @md:flex-row @lg:gap-6">
    <!-- Adapts to its own container width -->
  </div>
</div>
```

---

## 4. Fluid Typography & Fluid Spacing (`clamp()`)

Eliminate jarring jumps between breakpoints by smoothly interpolating font size and padding between minimum and maximum viewport boundaries:

$$\text{Preferred} = \text{MinSize} + (\text{MaxSize} - \text{MinSize}) \times \frac{\text{Viewport} - \text{MinViewport}}{\text{MaxViewport} - \text{MinViewport}}$$

### Practical Clamp Scale:
```css
:root {
  /* Headings scale fluidly from 320px to 1440px */
  --font-h1: clamp(1.75rem, 1.2rem + 2.5vw, 3rem);     /* 28px -> 48px */
  --font-h2: clamp(1.35rem, 1rem + 1.6vw, 2.25rem);    /* 22px -> 36px */
  --font-h3: clamp(1.15rem, 0.95rem + 1vw, 1.6rem);    /* 18px -> 26px */
  --font-body: clamp(0.95rem, 0.9rem + 0.25vw, 1.05rem);/* 15px -> 17px */

  /* Fluid gutters and padding */
  --gutter-x: clamp(1rem, 0.5rem + 2.5vw, 3rem);
  --section-py: clamp(2rem, 1rem + 4vw, 5rem);
}
```

---

## 5. Dynamic Viewport Units (`dvh`, `svh`, `lvh`)

Traditional `100vh` causes severe layout jumps and cutoffs on mobile Chrome/Safari because of address bars opening and closing during scroll.

- `100dvh` (Dynamic): Automatically resizes as address bar expands/contracts. Ideal for full-screen modals, navigation drawers, and mobile hero sections.
- `100svh` (Small): Smallest possible viewport (when address bar is fully expanded).
- `100lvh` (Large): Largest possible viewport (when address bar is collapsed).

```css
/* CORRECT: Full-screen mobile hero / modal */
.mobile-hero {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
}
```

---

## 6. RTL & Logical Properties (Persian / Iranian Web)

For Persian interfaces (e.g., Pezeshkan with Vazirmatn font and `dir="rtl"`):
Never use hardcoded directional CSS properties (`left`, `right`). Always use CSS Logical Properties:

| Physical (Avoid) | Logical (Mandatory) | Tailwind Equivalent |
|---|---|---|
| `margin-left` / `margin-right` | `margin-inline-start` / `margin-inline-end` | `ms-*` / `me-*` |
| `padding-left` / `padding-right` | `padding-inline-start` / `padding-inline-end` | `ps-*` / `pe-*` |
| `left: 0` / `right: 0` | `inset-inline-start: 0` / `inset-inline-end: 0` | `start-0` / `end-0` |
| `border-left` | `border-inline-start` | `border-s` |
| `text-align: right` | `text-align: start` | `text-start` |

---

## 7. Touch Targets & Pointer Precision

Touch screens require larger target areas and safe spacing compared to mice:

```css
/* Accessible minimum tap target: 44x44px (iOS) / 48x48px (Android/WCAG) */
.touch-target {
  min-height: 48px;
  min-width: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Hover styles ONLY on devices that actually support hovering */
@media (hover: hover) and (pointer: fine) {
  .btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 255, 255, 0.2);
  }
}

/* Touch active feedback for mobile */
@media (hover: none) and (pointer: coarse) {
  .btn:active {
    transform: scale(0.97);
    opacity: 0.9;
  }
}
```

---

## 8. Mobile Safe Area Insets (Notches & Home Indicators)

To support modern iPhone Dynamic Island, camera cutouts, and Android bottom navigation gestures:

```html
<!-- Mandatory in <head> -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

```css
/* Sticky headers and footers with safe-area padding */
.app-header {
  padding-top: max(1rem, env(safe-area-inset-top));
  padding-inline: max(1rem, env(safe-area-inset-left));
}

.bottom-nav {
  padding-bottom: max(0.75rem, env(safe-area-inset-bottom));
}
```

---

## 9. Zero-Overflow & Horizontal Scroll Elimination Checklist

Horizontal scrolling on mobile is a critical UI bug. Apply these rules across all layouts:

1. **Root Overflow Guard:**
   ```css
   html, body {
     overflow-x: hidden;
     max-width: 100vw;
   }
   ```
2. **Text Wrapping:**
   ```css
   p, h1, h2, h3, h4, span {
     overflow-wrap: break-word;
     word-break: break-word;
   }
   ```
3. **Responsive Images & Media:**
   ```css
   img, video, canvas, svg {
     max-width: 100%;
     height: auto;
     display: block;
   }
   ```
4. **Data Tables on Mobile:**
   - Option A: Wrapper with `overflow-x: auto` and scroll shadow indicators.
   - Option B: Transform table rows into stacked cards on viewports `< 640px`.
5. **Debug Command to Catch Rogue Width Elements:**
   ```javascript
   // Run in browser console to find elements exceeding viewport:
   document.querySelectorAll('*').forEach(el => {
     if (el.offsetWidth > document.documentElement.offsetWidth) {
       console.log('Overflowing element:', el);
     }
   });
   ```

---

## 10. Verification & Audit Protocol

Before considering any page or component responsive:
- [ ] Tested at **320px** (minimum smartphone viewport, iPhone SE).
- [ ] Tested at **375px / 390px** (standard iPhone / Android portrait).
- [ ] Tested at **768px** (tablet portrait).
- [ ] Tested at **1024px** (tablet landscape / laptop).
- [ ] Tested at **1440px+** (desktop wide).
- [ ] Verified **zero horizontal scrollbar** on mobile.
- [ ] Touch targets are at least **44×44px** on buttons, inputs, links.
- [ ] Persian text with Vazirmatn renders without awkward line-breaks (`text-wrap: balance` on headings).
- [ ] Modals and drawers use `100dvh` and handle virtual keyboard popups.
- [ ] RTL layout alignment remains intact across all breakpoints.
