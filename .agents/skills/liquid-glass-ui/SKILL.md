---
name: liquid-glass-ui
description: Design and implement production-ready Liquid Glass components and Apple-like fluid glassmorphism for Next.js, React, and Tailwind CSS. Covers frosted fills, smoked dark glass, chrome capsules, GlassBar, GlassContentCard, and Chromium backdrop-filter performance rules.
metadata:
  origin: IntelliHelper/IntelliHelper-UI
---

# Liquid Glass UI Skill

Guide for designing and building production-grade **Liquid Glass** surfaces and fluid glassmorphism components in Next.js and Tailwind CSS, adapted from the `IntelliHelper-UI` component library.

## When to Activate

- Designing modern glassmorphic cards, hero overlays, navigation bars, or dialog modals with a fluid/milky glass texture.
- Implementing Apple VisionOS / iOS style Liquid Glass materials with realistic refraction, highlights, and backdrop blur.
- Building components like `GlassBar`, `GlassContentCard`, `GlassContentPanel`, and `GlassIconButton`.
- Styling clinical dark glass surfaces that integrate with the Pezeshkan Healthcare design tokens (`#00FFFF`, `#00E599`).

## Core Architecture & Components

The library provides modular, copy-paste React components located in `.agents/plugins/IntelliHelper-UI/packages/ui/src/`:

1. **`GlassBar`** (`glass-bar.tsx`):
   - Floating navigation bar or toolbar encapsulated in a pill/capsule shape (`glass-chrome glass-chrome-capsule`).
   - Supports sizes (`sm`, `default`, `lg`) and optional entry animation (`animate-float-in`).

2. **`GlassContentCard` & `GlassContentPanel`** (`glass-content-card.tsx`):
   - Multi-panel card with gradient backdrop layers and frosted glass overlays.
   - Ideal for featured articles, doctor profile showcases, and clinical analytics cards.

3. **`GlassIconButton`** (`glass-icon-button.tsx`):
   - Circular glass action buttons with specular highlights and active/hover feedback.

## Essential CSS Tokens (Tailwind CSS & OKLCH)

Liquid Glass requires high-precision color definitions and backdrop filters for both Clinical Dark and Clinical Radiant Light modes:

```css
/* Clinical Radiant Light Mode (Frosted Glass 2.0 / Apple VisionOS Light) */
:root, :root.light {
  /* Frosted white light glass fill — crisp clinical frost, high readability */
  --glass-surface-fill: rgba(255, 255, 255, 0.82);
  --glass-panel-bg: rgba(255, 255, 255, 0.78);
  --glass-header-bg: rgba(255, 255, 255, 0.75);
  --glass-dialog-bg: rgba(255, 255, 255, 0.88);
  --glass-dialog-elevated-bg: rgba(255, 255, 255, 0.94);
  --glass-surface-bg: rgba(255, 255, 255, 0.70);
  --glass-surface-thin-bg: rgba(255, 255, 255, 0.50);
  
  /* Floating capsule highlights & dock borders */
  --glass-chrome-bg: rgba(255, 255, 255, 0.92);
  --glass-chrome-border: rgba(255, 255, 255, 0.90);
  --glass-chrome-shadow: 0 10px 30px -5px rgba(0, 102, 255, 0.06), 0 4px 12px rgba(11, 25, 44, 0.04);
  --glass-chrome-inset: inset 0 1px 1px rgba(255, 255, 255, 1);
  --glass-chrome-rim: 0 0 0 1px rgba(0, 102, 255, 0.08);

  /* Shared frost filter stack */
  --glass-frost: blur(20px) saturate(180%);
  --glass-frost-heavy: blur(28px) saturate(190%);
}

:root.dark {
  /* Smoked dark glass fill — readable frost, never clear plastic */
  --glass-surface-fill: oklch(0.24 0.015 270);
  --glass-panel-bg: oklch(0.24 0.015 270 / 0.78);
  --glass-header-bg: oklch(0.24 0.015 270 / 0.72);
  --glass-dialog-bg: oklch(0.24 0.015 270 / 0.74);
  --glass-dialog-elevated-bg: oklch(0.26 0.015 270 / 0.84);
  --glass-surface-bg: oklch(0.24 0.015 270 / 0.68);
  --glass-surface-thin-bg: oklch(0.26 0.015 270 / 0.55);
  
  /* Chrome capsule highlights */
  --glass-chrome-bg: oklch(0.3 0.018 270 / 0.72);
  --glass-chrome-border: oklch(1 0 0 / 0.16);
  --glass-chrome-shadow: 0 4px 16px oklch(0 0 0 / 0.32), 0 12px 40px oklch(0 0 0 / 0.4);
  --glass-chrome-inset: inset 0 1px 0 oklch(1 0 0 / 0.14);
  --glass-chrome-rim: 0 0 0 0.5px oklch(1 0 0 / 0.2);

  /* Shared frost filter stack */
  --glass-frost: blur(16px) saturate(180%);
  --glass-frost-heavy: blur(24px) saturate(190%);
}
```

## Critical Implementation Rules & Gotchas

1. **NEVER use percentage custom properties in `color-mix`**:
   - `color-mix(in oklch, var(--x) var(--pct), transparent)` fails after LightningCSS bundling and frequently renders 100% transparent in Safari and Chrome.
   - **Fix:** Always bake alpha directly into the color value: `oklch(0.24 0.015 270 / 0.78)`.

2. **NEVER add `transform: translateZ(0)` on sticky glass elements**:
   - Applying 3D transforms to sticky headers or sidebars breaks Chromium's internal texture caching for `backdrop-filter`, causing the blurred background to freeze or vanish while scrolling.

3. **Always pair `blur()` with `saturate()`**:
   - Simple `blur(...)` can look dull and milky grey. Adding `saturate(180%)` keeps colors underneath the glass vibrant and authentic to physical glass optics.

4. **Clinical Alignment**:
   - Combine with `pezeshkan-brand-system` by tinting border rims with `rgba(0, 255, 255, 0.15)` (Medical Cyan highlight) instead of pure white where active focus is needed.
