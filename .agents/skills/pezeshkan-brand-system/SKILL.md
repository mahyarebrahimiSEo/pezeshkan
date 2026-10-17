---
name: pezeshkan-brand-system
description: "Master design system, brand colors, visual tokens, and UI/UX design principles for the Pezeshkan Healthcare Ecosystem. Governs the Clinical Dark DNA, 70/20/10 design ratio, semantic color tokens, glassmorphism hierarchy, Persian RTL typography, signature vital components, and strict anti-pattern avoidance for Next.js, React, and Tailwind CSS."
---

# Pezeshkan Brand & Design System Specification

## 1. Product Vision & Visual DNA

Pezeshkan is an integrated **Healthcare Ecosystem** connecting Doctors, Patients, Clinics, Staff, and Administrators.
- **Fundamental Principle:** *One Ecosystem, One Visual Language, Contextual Experiences for each role.*
- **Core Visual Direction:** **Clinical Technology** — high-precision, trustworthy, scientific, and calm.
- **Strictly Prohibited Direction:** **Cyberpunk / Sci-Fi / Gaming UI**. No harsh neon glows, no excessive dark sci-fi decorations.

### The 70 / 20 / 10 Design Ratio
Every page, dashboard, and marketing surface in Pezeshkan must respect this strict compositional balance:
1. **70% Clean Modern SaaS / Product UI:** Generous whitespace, structured grid layouts, crisp typography, clean data tables, accessible forms, and high-contrast usability.
2. **20% Vital Signal DNA:** Subtle waveforms, live pulse indicators, node connections, and signal paths representing dynamic clinical health data.
3. **10% Medical Monitor Metaphor:** Hardware-inspired dials, glass-layered displays, signal sweep indicators, and subtle illuminated bezels.

---

## 2. Brand Color Palette & Semantic Tokens

### Primary Rule: Never Hardcode Hex Colors
Do NOT use raw hex codes (e.g. `#00FFFF`, `#00E599`, `#0F172A`) directly inside JSX, TSX, or inline CSS.
Always use CSS custom properties (`var(--color-signal-primary)`) or Tailwind semantic utility classes (`text-signal-primary`, `bg-surface-glass`).

### The 4 Vital Semantic Colors
| Semantic Role | Token Name | Hex Value | Meaning & Approved Usage |
| :--- | :--- | :--- | :--- |
| **Vital Turquoise / Cyan** | `--color-signal-primary` | `#00FFFF` | **Information, Interaction, Connection, Processing.** Primary CTA button, active tabs, focused states, primary vital signal waves. |
| **Highlight Green** | `--color-signal-success` | `#00E599` | **Health, Normal Status, Alive, Success, Confirmation.** Pezeshkan Status Beacon, normal vital signs, completed appointments, positive clinical indicators. |
| **Warm Yellow / Amber** | `--color-signal-warning` | `#F59E0B` | **Attention, Pending Review, Triage Caution.** Pending appointments, lab results requiring validation, warnings. |
| **Clinical Red** | `--color-signal-critical` | `#EF4444` | **Critical Emergency, Urgent Triage, System Error.** Heart rate alarms, critical triage, destructive actions. **STRICT RULE:** Never use Red as a decorative or brand background color! |

### Environment & Surface Colors (Clinical Dark Base)
Dark Mode is the **Core Primary Experience** of Pezeshkan, reflecting modern diagnostic workstations and clinical monitoring displays.

| Token | CSS Variable | Hex / RGBA | Role |
| :--- | :--- | :--- | :--- |
| **Canvas Background** | `--color-bg-base` | `#090D16` | Deepest clinical navy, foundation of the entire application. |
| **Card Surface** | `--color-surface-base` | `#0F172A` | Solid card background with 1px border. |
| **Glass Surface** | `--color-surface-glass` | `rgba(15, 23, 42, 0.70)` | Frosted glass cards with `backdrop-blur-md` and `border-white/10`. |
| **Elevated Overlay** | `--color-surface-elevated` | `rgba(15, 23, 42, 0.88)` | Modals, floating dropdowns, command palettes. |
| **Subtle Border** | `--color-border-subtle` | `rgba(255, 255, 255, 0.08)` | Dividers, card borders, table row borders. |
| **Interactive Border** | `--color-border-interactive` | `rgba(0, 255, 255, 0.25)` | Hover states on interactive cards or inputs. |

### Text & Contrast Hierarchy
- `--color-text-primary`: `#F8FAFC` (Pure clinical white/slate-50 for high readability)
- `--color-text-secondary`: `#94A3B8` (Slate-400 for descriptions, table column headers)
- `--color-text-muted`: `#64748B` (Slate-500 for helper notes, timestamps)

---

## 3. Surface & Glassmorphism Architecture

Glassmorphism in Pezeshkan is an architectural layer for depth, NOT a blanket decoration.

### The 3 Glass Golden Rules
1. **Maximum 2 Nested Glass Layers:** Never nest glass cards more than 2 levels deep (Canvas -> Glass Card -> Tooltip/Button). Excessive glass ruins contrast and slows GPU rendering.
2. **Readability First:** If medical data, tabular reports, or lengthy clinical text is displayed, use a solid surface (`bg-surface-base`) rather than translucent glass.
3. **Controlled Glow:** Glow effects must be soft, diffused, and low-opacity:
   ```css
   /* Correct Clinical Subtle Glow */
   box-shadow: 0 0 20px -5px rgba(0, 255, 255, 0.15);
   /* Prohibited Cyberpunk Intense Glow */
   /* box-shadow: 0 0 50px rgba(0, 255, 255, 0.8); -> STRICTLY FORBIDDEN */
   ```

### Recommended Tailwind Card Recipe
```tsx
<div className="relative rounded-2xl bg-slate-900/70 backdrop-blur-md border border-white/10 p-6 shadow-xl transition-all duration-300 hover:border-cyan-500/30 hover:shadow-cyan-500/5">
  {children}
</div>
```

---

## 4. Typography & Persian RTL Standards

### Font Family & Configuration
- **Primary Persian Font:** `Vazirmatn` (variable font, weights 300 to 800).
- **Secondary Display / Monospace:** `JetBrains Mono` or tabular numerals for clinical metrics and numeric data.
- **RTL Enforcement:** All containers must respect `dir="rtl"`, Persian punctuation marks (، ؛ ؟), and proper letter-spacing (`tracking-normal` for Persian text).
- **Line Height:** Persian text requires generous vertical rhythm: `leading-relaxed` (1.7 to 1.8) for body copy, avoiding squished diacritics.

### Medical Data & Tabular Numerals
When displaying heart rates (BPM), blood pressure (mmHg), timestamps, or financial KPIs:
- Use `tabular-nums` (`font-feature-settings: 'tnum'`) so numbers do not jump or jitter during live data updates.
- Keep English acronyms (ECG, SpO2, MRI, CT) clearly formatted alongside Persian labels.

---

## 5. Signature Components & Interaction Language

### 1. Pezeshkan Status Beacon
- Represents the alive/connected state of the system or tele-health doctor.
- Visual: A small circular indicator with a subtle breathing pulse:
  ```tsx
  <span className="relative flex h-3 w-3">
    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
    <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500 shadow-[0_0_8px_#00e599]"></span>
  </span>
  ```

### 2. Floating Vital Navigation
- Signature navigation reserved strictly for the **Home / Landing** surface.
- Compact floating capsule with blur glassmorphism, quick shortcuts, and vital status summary.
- Internal pages (Doctor panel, Clinic, Magazine) use contextual topbars, breadcrumbs, and standard sidebars.

### 3. Vital Dial & Vital Ring
- Circular metric indicator used for high-impact metrics (Doctor daily capacity, Clinic occupancy, Patient recovery progress).
- The Ring color adapts contextually: Vital Green for on-track, Cyan for processing, Amber for near-limit.

### 4. Vital Grid
- Subtle geometric background grid representing medical graph paper.
- Grid opacity must never exceed 15% (`opacity-10` to `opacity-15`) to remain an ambient foundation rather than distracting visual clutter.

---

## 6. Strict Anti-Patterns (The "Never Do" List)

1. **NO "ECG Everywhere":** Do not put an animated heart-rate wave on every card, header, or divider. Keep ECG animations focused only on the 3D Hero and actual clinical telemetry widgets.
2. **NO Cyberpunk / Gamer Aesthetics:** Pezeshkan is an Iranian digital health standard, not a neon video game. Keep borders subtle (1px, low opacity).
3. **NO Decorative Red:** Never use red for buttons, borders, or backgrounds unless communicating an emergency alert, critical error, or high-triage warning.
4. **NO Raw Hex Codes:** Every color must map to a CSS token or Tailwind config variable.
5. **NO Blank Glass Text Overlays:** Never place low-contrast grey text directly over heavily blurred backgrounds. Always verify WCAG AAA contrast ratio.
6. **NO Hardcoded Breakpoints:** Always use Tailwind breakpoints (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`) with mobile-first architecture.
7. **NO Unchecked Motion:** All animations must respect `@media (prefers-reduced-motion: reduce)`.

---

## 7. Pre-Implementation Quality Checklist

Before writing or approving any UI component:
- [ ] Are colors mapped to `--color-signal-*` or `--color-surface-*` tokens?
- [ ] Is Persian RTL alignment strictly maintained with `Vazirmatn` font?
- [ ] Are numbers in data tables or KPI cards formatted with `tabular-nums`?
- [ ] Is the glass layer hierarchy at or under 2 levels?
- [ ] Does the component gracefully scale from mobile (375px) to desktop (1440px+)?
- [ ] Are all interaction states (Idle, Hover, Active, Focus-visible, Disabled, Loading) explicitly designed?
- [ ] Is the 70/20/10 ratio preserved without decorative over-branding?
