---
name: animation-skill
description: Universal web animation skill pack for AI coding agents — GSAP, R3F/Three.js, Lenis, motion direction, 60fps performance, and accessibility. Covers gsap-scroll (ScrollTrigger + Lenis clock sync), web-animation (choreography, easing, page transitions), motion-taste (do and don't rules), and spatial-webgl.
---

# Web Animation & Scroll Mastery

This skill pack coordinates 4 specialized animation modules for production Next.js and React interfaces:

## Sub-Skills Directory:
1. **`gsap-scroll`** (`skills/gsap-scroll/SKILL.md`): Clock synchronization between Lenis and GSAP ScrollTrigger, lifecycle cleanup with `gsap.context()`, and bounded pinning sequences.
2. **`web-animation`** (`skills/web-animation/SKILL.md`): Scroll choreography, micro-interactions, page transitions, easing curves, and 60fps performance budgets.
3. **`motion-taste`** (`skills/motion-taste/SKILL.md`): Strict anti-slop rules for motion — what to animate vs what to keep static, avoiding dizzying movement.
4. **`spatial-webgl`** (`skills/spatial-webgl/SKILL.md`): Three.js canvas sync with DOM elements.

## Lenis + ScrollTrigger Standard Formula:
```ts
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';

gsap.registerPlugin(ScrollTrigger);
const lenis = new Lenis({ autoRaf: false });
const tick = (time: number) => lenis.raf(time * 1000);
gsap.ticker.add(tick);
gsap.ticker.lagSmoothing(0);
lenis.on('scroll', ScrollTrigger.update);
```
