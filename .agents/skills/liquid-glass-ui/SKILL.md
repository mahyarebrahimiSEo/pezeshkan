---
name: liquid-glass-ui
description: Design and implement production-ready Liquid Glass components and Apple-like fluid glassmorphism for Next.js, React, HTML, and Tailwind CSS. Enforces the 2026 Liquid Glass optical rules (strict 35-50% translucency budget, ambient background mesh light, specular dual-rim highlights, saturated blur, and chromatic refraction) to eliminate opaque, fake, or flat-looking glass.
metadata:
  version: "2.0.0"
  origin: IntelliHelper-UI + Apple VisionOS Optics + Pezeshkan Clinical Dark DNA
---

# Modern Liquid Glass UI Specification (2026 Standard)

This skill governs the creation of genuine, high-end **Modern Liquid Glass** (شیشه مایع مدرن) across web interfaces. It addresses and fixes the common failure mode where AI generates opaque, plastic, or flat-looking boxes instead of authentic refractive glass.

---

## 1. The 4 Golden Optical Rules of Liquid Glass

Authentic glass requires physical optical metaphors. If any of these 4 rules are violated, the interface will look like a solid dark container rather than real glass:

### Rule 1: The Strict Translucency Budget (Never Opaque)
- **FAIL (The #1 AI mistake):** `rgba(11, 17, 30, 0.88)` or `rgba(0, 0, 0, 0.95)`. At 85%+ opacity, light cannot pass through. It is an opaque block, NOT glass.
- **PASS (Real Glass Translucency):**
  - **Clinical Dark Mode:** `rgba(11, 17, 30, 0.42)` to `rgba(18, 26, 44, 0.52)` (Never exceed 0.55).
  - **Radiant Light Mode:** `rgba(255, 255, 255, 0.55)` to `rgba(255, 255, 255, 0.70)`.

### Rule 2: Background Must Have Ambient Light to Refract
- **Core Principle:** Glass placed over pure flat black `#000000` with no background light has *nothing to blur or refract*, so it inevitably looks flat black.
- **The Solution:** Always place subtle **Ambient Vital Mesh Gradients** or light orbs underneath or behind liquid glass sections:
  ```css
  /* Ambient light layer behind glass containers */
  background: radial-gradient(circle at 20% 30%, rgba(0, 255, 255, 0.15) 0%, transparent 60%),
              radial-gradient(circle at 80% 70%, rgba(0, 229, 153, 0.10) 0%, transparent 65%);
  ```

### Rule 3: The Dual-Rim Specular Highlight (The Liquid Edge)
Real glass catches directional light on its bevels and edges:
- Top bevel catches light (`inset 0 1px 1px 0 rgba(255, 255, 255, 0.35)`).
- Interior volume has faint ambient glow (`inset 0 0 24px 0 rgba(0, 255, 255, 0.04)`).
- Deep drop shadow floats the glass in space:
  ```css
  box-shadow: 
    inset 0 1px 1px 0 rgba(255, 255, 255, 0.30),
    inset 0 0 20px 0 rgba(255, 255, 255, 0.03),
    0 20px 50px -10px rgba(0, 0, 0, 0.65),
    0 0 0 1px rgba(255, 255, 255, 0.10);
  ```

### Rule 4: Multi-Stage Filter Stack (`blur` + `saturate` + `contrast`)
Simple `blur(10px)` produces a dull grey milky smear. Modern liquid glass requires color saturation amplification:
```css
backdrop-filter: blur(24px) saturate(190%) contrast(105%);
-webkit-backdrop-filter: blur(24px) saturate(190%) contrast(105%);
```

---

## 2. Standard CSS Production Recipe for Pezeshkan

Whenever building frontend components (in HTML, CSS, Next.js, or Tailwind), use these exact production classes:

```css
/* Core Liquid Glass Surface */
.pez-liquid-glass {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.10) 0%,
    rgba(15, 23, 42, 0.45) 45%,
    rgba(8, 12, 22, 0.55) 100%
  ) !important;
  backdrop-filter: blur(24px) saturate(190%) contrast(105%) !important;
  -webkit-backdrop-filter: blur(24px) saturate(190%) contrast(105%) !important;
  border: 1px solid rgba(255, 255, 255, 0.14) !important;
  border-top: 1px solid rgba(255, 255, 255, 0.35) !important;
  box-shadow: 
    inset 0 1px 1px 0 rgba(255, 255, 255, 0.30),
    inset 0 0 20px 0 rgba(0, 255, 255, 0.04),
    0 20px 50px -12px rgba(0, 0, 0, 0.70) !important;
  border-radius: 24px;
  position: relative;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Fluid Hover Sheen Effect */
.pez-liquid-glass:hover {
  border-color: rgba(0, 255, 255, 0.35) !important;
  box-shadow: 
    inset 0 1px 2px 0 rgba(255, 255, 255, 0.50),
    inset 0 0 25px 0 rgba(0, 255, 255, 0.08),
    0 24px 60px -10px rgba(0, 0, 0, 0.80),
    0 0 30px -5px rgba(0, 255, 255, 0.20) !important;
  transform: translateY(-2px);
}

/* Subtle Organic Noise Texture overlay to kill digital flatness */
.pez-liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.035'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 1;
}
```

---

## 3. Tailwind CSS Utility Classes

When writing JSX / TSX or Tailwind components, use this composition:

```tsx
<div className="relative overflow-hidden rounded-3xl border border-white/15 border-t-white/35 bg-gradient-to-br from-white/10 via-slate-900/45 to-slate-950/55 p-8 backdrop-blur-xl saturate-[1.9] contrast-[1.05] shadow-[inset_0_1px_1px_rgba(255,255,255,0.3),inset_0_0_20px_rgba(0,255,255,0.05),0_20px_50px_rgba(0,0,0,0.65)] hover:border-cyan-400/40 hover:shadow-[0_0_30px_rgba(0,255,255,0.2)] transition-all duration-300">
  {/* Content goes here */}
</div>
```

---

## 4. Prohibited Gotchas in Chromium & Safari

1. **NEVER add `transform: translateZ(0)` on sticky glass containers:** Breaks Chromium's internal texture cache, causing `backdrop-filter` to freeze or vanish while scrolling.
2. **NEVER use `color-mix` with percentage custom properties:** After LightningCSS bundling, `color-mix(in oklch, var(--x) var(--pct), transparent)` often resolves as 100% transparent.
3. **NEVER put heavy glass on pure opaque cards:** Glass requires transparency. If you put opaque `#0F172A` underneath, the glass effect is completely lost.
