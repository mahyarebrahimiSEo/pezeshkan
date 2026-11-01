---
name: frontend-debugging
description: "Specialized frontend debugging skill for diagnosing and resolving layout bugs, CSS/styling issues, optical glass rendering defects, GSAP/Lenis scroll and animation glitches, responsive viewport overflow, and JavaScript UI errors. Follows strict root cause investigation, repro-isolate-fix-verify loops, and DOM/CSSOM inspection playbooks."
---

# Frontend Debugging & Visual Defect Diagnostic Engine

> **The Iron Law of Frontend Debugging:**
> NEVER apply band-aid fixes (`!important`, `z-index: 999999`, or random `margin` hacks) without first proving the root cause in the CSSOM or DOM tree.

---

## 1. The 4-Phase Frontend Debugging Protocol

Every frontend issue must pass through this 4-phase discipline:

### Phase 1: Reproduce & Evidence Capture
- Identify the exact viewport width, browser engine (Chromium, WebKit, Gecko), and theme mode (Light/Dark) where the defect occurs.
- Check browser console for uncaught exceptions, hydration errors, or failed asset loads.
- Capture the computed styles and DOM geometry of the defective node.

### Phase 2: Root Cause Isolation (CSSOM & Runtime)
- Disable styles systematically in reverse order to find the specific rule triggering the defect.
- Identify whether the bug is caused by:
  1. A Stacking Context collision (`transform`, `filter`, or `opacity` creating a new stacking context).
  2. A Box Sizing or Flex/Grid constraint violation (e.g. flex child without `min-width: 0`).
  3. An overflow containment defect (`overflow: hidden` on an ancestor breaking `position: sticky`).
  4. An optical glass failure (background opacity exceeding 55%, or missing ambient light underneath).
  5. A JavaScript lifecycle or animation desynchronization.

### Phase 3: Surgical & Standardized Fix
- Apply the minimal, architectural fix that addresses the root cause at the token or layout level.
- Clean up any unused legacy rules, temporary debug borders, or obsolete workarounds.

### Phase 4: Multi-Viewport & Dual-Theme Verification
- Test across 3 standard breakpoints: Desktop (1440px / 1280px), Tablet (768px), and Mobile (375px).
- Verify in both Radiant Light Mode and Deep Surgical Dark Mode.
- Verify smooth 60fps scrolling without layout shifts (CLS < 0.1).

---

## 2. Specialized Diagnostic Playbooks

### Playbook A: CSS Layout & Overflow Diagnostics
- **Horizontal Scrollbar on Mobile**:
  - Run the DOM overflow detector script:
    ```js
    document.querySelectorAll('*').forEach(el => {
      if (el.scrollWidth > document.documentElement.clientWidth) {
        console.warn('Overflowing element:', el, 'Width:', el.scrollWidth);
      }
    });
    ```
  - Root cause: An element has a hardcoded `width: Xpx` instead of `max-width: 100%`, or a negative margin without boundary containment.
  - Fix: Ensure container has `max-width: 100%`, `box-sizing: border-box`, and text wraps with `overflow-wrap: break-word`.

- **Flexbox Text Truncation / Grid Blowout**:
  - Root cause: Flex children default to `min-width: auto`. A long word or table column will expand beyond the parent container.
  - Fix: Add `min-width: 0;` (or `min-h-0` in Tailwind) to the direct flex child.

- **`position: sticky` Not Sticking**:
  - Root cause: Any ancestor node with `overflow: hidden`, `overflow: auto`, or `overflow: clip` breaks sticky positioning.
  - Fix: Inspect ancestor chain with `window.getComputedStyle(parent).overflow`. Remove unnecessary overflow rules from ancestors.

---

### Playbook B: Optical Liquid Glass & Rendering Diagnostics
- **Glass Card Appears as a Solid Opaque Box**:
  - Root cause: Background alpha is too high (> 0.55 in dark mode, > 0.85 in light mode), blocking light penetration.
  - Fix: Set dark mode background to `rgba(15, 23, 42, 0.44)` and light mode to `rgba(255, 255, 255, 0.72)`.

- **`backdrop-filter: blur()` Does Not Blur Background**:
  - Check 1: Does the background have visual contrast? A flat black `#000000` with no ambient mesh gradient has nothing to blur. Add `background: radial-gradient(...)` behind the glass.
  - Check 2: Does an ancestor have `transform`, `filter`, or `perspective`? These can isolate the backdrop filter on Chromium.
  - Check 3: Is `-webkit-backdrop-filter` included for Safari/iOS compatibility?

- **Blurry Text or Fuzzy Icons on Glass Cards**:
  - Root cause: Subpixel rendering issue caused by fractional translate values (`translate(-50%, -50%)`) or non-integer widths.
  - Fix: Apply `transform: translateZ(0); backface-visibility: hidden;` or round pixel values with CSS `round()`.

---

### Playbook C: GSAP, Lenis & Scroll Choreography Diagnostics
- **Jittery Scrubbing or Pinning Jumps**:
  - Root cause: Lenis and GSAP running on two separate requestAnimationFrame loops.
  - Fix: Ensure Lenis is driven exclusively by the GSAP ticker:
    ```js
    gsap.registerPlugin(ScrollTrigger);
    const lenis = new Lenis({ autoRaf: false });
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
    lenis.on('scroll', ScrollTrigger.update);
    ```
- **ScrollTrigger Triggers at the Wrong Scroll Position**:
  - Root cause: Layout height changed after dynamic content or images loaded, but triggers were not recalculated.
  - Fix: Call `ScrollTrigger.refresh()` after DOM changes, font loading, or tab switching.

- **Memory Leaks and Ghost Event Handlers**:
  - Root cause: Creating tweens or ScrollTriggers in React/vanilla components without tearing them down on unmount.
  - Fix: Always wrap GSAP animations in `gsap.context()` and execute `ctx.revert()` upon teardown.

---

### Playbook D: RTL Persian Typography & Bidirectional Layouts
- **Broken Alignment or Reverse Direction Bugs**:
  - Ensure parent container has `dir="rtl"`.
  - Use logical CSS properties: `margin-inline-start`, `margin-inline-end`, `padding-inline-start`, `inset-inline-start` instead of hardcoded `left`/`right`.
  - Ensure numerical data, phone numbers, and codes retain LTR direction with `dir="ltr"` and `unicode-bidi: isolate`.
  - Enforce `font-variant-numeric: tabular-nums` on all countdowns, clock displays, and financial fee splits to prevent width jitter.

---

## 3. Quick Verification Checklist

When diagnosing any bug:
1. Console: Are there zero red errors or unhandled promise rejections?
2. Network: Did all SVG icons, WebP images, and fonts load with 200 OK?
3. DOM: Is there zero horizontal scroll on mobile (`window.innerWidth === document.documentElement.clientWidth`)?
4. Performance: Does the frame rate maintain 60fps during scroll?
5. Contrast: Do text and interactive elements pass WCAG AA (4.5:1 for body, 3:1 for large text)?
