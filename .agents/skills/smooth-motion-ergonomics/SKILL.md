---
name: smooth-motion-ergonomics
description: "Production engine for buttery-smooth 60fps/120fps web animations, zero-jank hardware acceleration, and eye-friendly motion ergonomics. Eliminates animation lag, layout thrashing, and visual dizziness using GPU compositing, calibrated cubic-bezier easing, Lenis lag smoothing, and vestibular comfort rules."
---

# Smooth Motion Ergonomics & High-Performance Animation Engine

> **The Golden Law of Eye-Comfort Animation:**
> Animations exist to guide user attention and confirm state changes — NEVER to show off.
> If motion draws attention to *itself* rather than the content, or causes eye fatigue and dizziness, it is a failure.

---

## 1. Zero-Lag & 60FPS/120FPS Performance Architecture

To guarantee 100% lag-free execution across all browsers and screens (from 60Hz office monitors to 120Hz ProMotion displays):

### Rule 1: The Transform & Opacity Compositor Sandbox
- **ONLY ANIMATE COMPOSITED PROPERTIES:**
  - `transform` (translate3d, scale, rotate)
  - `opacity`
- **NEVER ANIMATE LAYOUT OR PAINT PROPERTIES CONTINUOUSLY:**
  - `top`, `left`, `right`, `bottom` (triggers reflow / layout thrashing)
  - `width`, `height`, `margin`, `padding` (triggers full tree reflow)
  - `box-shadow` or `backdrop-filter` on continuous scroll scrub (causes heavy GPU pixel fill rate drops)
  - `border-radius` during movement
- **Hardware Acceleration Enabler:**
  Use 3D transforms to force rendering onto dedicated GPU layers:
  ```css
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
  perspective: 1000px;
  ```

### Rule 2: Surgical `will-change` Lifecycle
- Apply `will-change: transform, opacity` ONLY right before or during active animation.
- NEVER put `will-change` permanently on dozens of static CSS elements (this hogs hundreds of megabytes of GPU VRAM and causes stutter).
- In GSAP/JS, let GSAP handle auto-promotion and cleanup.

### Rule 3: Unified Clock Synchronization (Lenis + GSAP)
- Ensure a single clock drives Lenis smooth scroll and ScrollTrigger:
  ```ts
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';
  import Lenis from 'lenis';

  gsap.registerPlugin(ScrollTrigger);
  const lenis = new Lenis({ 
    duration: 1.15, 
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    autoRaf: false 
  });

  const tick = (time: number) => lenis.raf(time * 1000);
  gsap.ticker.add(tick);
  gsap.ticker.lagSmoothing(0); // Zero lag smoothing: Prevents jarring catch-up jumps on CPU spikes
  lenis.on('scroll', ScrollTrigger.update);
  ```

---

## 2. Motion Ergonomics & Eye-Comfort Principles (Anti-Dizziness)

### The "Soft Settle" Deceleration Curve
- Human eyes track decelerating objects with zero strain. Accelerating or bouncy objects cause visual tension and micro-fatigue.
- Standard Motion Easing Curves:
  - **Fluid Soft Settle (Default)**: `cubic-bezier(0.16, 1, 0.3, 1)` or GSAP `power3.out`.
  - **Subtle Micro-Interaction**: `cubic-bezier(0.2, 0, 0, 1)`.
  - **AVOID**: Bouncy springs (`bounce`, `elastic`) on text and medical cards; they look amateurish and vibrate the retina.

### Travel Distance Budget
- **Card Entrance / Section Reveal**: Max travel `y: 20px` to `y: 32px`. Never fly elements from 100px away.
- **Button / Card Hover**: Max travel `y: -2px` to `y: -4px`.
- **Text & Paragraphs**: Max travel `y: 12px` to `y: 16px`.

### Natural Stagger Cascading
- When revealing multiple cards or list items, stagger them by **50ms to 75ms** (`stagger: 0.06`).
- A stagger below 30ms looks like a broken flicker.
- A stagger above 100ms feels painfully slow and delays reading.

### Visual Quietness & Rhythm
- No more than ONE primary animated movement in the active viewport at any given time.
- Supporting elements move in concert with the primary element, not against it.
- Never use infinite looping rotations or oscillations on text or primary cards. Continuous motion is reserved strictly for subtle vital pulses (like the 3D heart pulse or status beacon dot).

---

## 3. Accessibility & Reduced Motion Guarantee

Always respect the user's system preferences for vestibular comfort:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

In GSAP:
```ts
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (prefersReducedMotion) {
  gsap.set(target, { autoAlpha: 1, y: 0, scale: 1 });
}
```

---

## 4. Verification & Frame Rate Audit Checklist

Before releasing any frontend motion or scroll feature:
1. **Frame Rate Audit**: Run Chrome DevTools Performance monitor — does FPS stay at a flat 60/120fps with green bars during fast scrolling?
2. **CPU Profile**: Are there zero long tasks (> 50ms) during scroll?
3. **Reflow Counter**: Does scrolling cause zero Layout (reflow) events?
4. **Eye Fatigue Check**: Read a 3-line paragraph while scrolling past — is the text sharp and readable without motion blur or dizziness?
5. **Reduced Motion**: When `prefers-reduced-motion` is enabled, does all clinical content appear immediately and remain 100% accessible?
