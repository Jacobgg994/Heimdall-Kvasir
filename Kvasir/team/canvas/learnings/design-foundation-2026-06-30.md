# Design Foundation Report

**Date:** 2026-06-30
**Author:** CANVAS (UX/UI Designer)
**Mission:** Design system blueprint for GemLogin, component library recommendations, color system, typography scale, accessibility checklist

---

## Sources Studied

| Resource | Version/Date | Key Takeaway |
|---|---|---|
| Tailwind CSS v4.3.2 | Jun 2026 | CSS-first config with `@theme`, OKLCH color space, Rust-based Oxide compiler |
| shadcn/ui v0.2.0 | Jun 2026 | Code-distribution model, CVA variants, Radix primitives, semantic OKLCH tokens |
| Storybook | Active | Industry standard UI workshop for isolated component development, testing, documentation |
| System UI Theme Spec | Stable | Universal design token format — scales, aliases, cross-framework contract |
| Material Design 3 | Active | Dynamic color, 3-layer tokens, tonal elevation, 15-type scale, expressive motion |

---

## 1. Design System Blueprint for GemLogin

### 1.1 Architecture Layers

The GemLogin design system follows a four-layer architecture inspired by the convergence of System UI Theme Spec and Material Design 3:

```
┌─────────────────────────────────────────┐
│  L4: COMPONENT LAYER                    │
│  shadcn/ui components + GemLogin custom │
├─────────────────────────────────────────┤
│  L3: PATTERN LAYER                      │
│  Layout, navigation, data display       │
├─────────────────────────────────────────┤
│  L2: SEMANTIC TOKEN LAYER               │
│  --color-primary, --text-body, --space-md│
├─────────────────────────────────────────┤
│  L1: PRIMITIVE TOKEN LAYER              │
│  OKLCH values, raw scales               │
└─────────────────────────────────────────┘
```

### 1.2 Token Architecture

Following the System UI Theme Spec (`ThemeShape`) for primitive tokens, with MD3-style semantic abstraction:

**Primitive Tokens** (raw values, never used directly in components):

```css
/* File: tokens/primitives.css */
@theme {
  /* Core palette (OKLCH — perceptually uniform) */
  --color-blue-50:  oklch(0.97 0.02 250);
  --color-blue-100: oklch(0.93 0.04 250);
  --color-blue-200: oklch(0.88 0.06 250);
  --color-blue-300: oklch(0.80 0.09 250);
  --color-blue-400: oklch(0.70 0.14 250);
  --color-blue-500: oklch(0.58 0.18 250);
  --color-blue-600: oklch(0.47 0.18 250);
  --color-blue-700: oklch(0.38 0.15 250);
  --color-blue-800: oklch(0.30 0.11 250);
  --color-blue-900: oklch(0.22 0.07 250);

  /* Neutral scale */
  --color-neutral-50:  oklch(0.99 0 0);
  --color-neutral-100: oklch(0.97 0 0);
  --color-neutral-200: oklch(0.92 0 0);
  --color-neutral-300: oklch(0.87 0 0);
  --color-neutral-400: oklch(0.74 0 0);
  --color-neutral-500: oklch(0.62 0 0);
  --color-neutral-600: oklch(0.50 0 0);
  --color-neutral-700: oklch(0.38 0 0);
  --color-neutral-800: oklch(0.26 0 0);
  --color-neutral-900: oklch(0.15 0 0);

  /* Success / Warning / Error (for GemLogin workflow status) */
  --color-green-500: oklch(0.62 0.18 145);
  --color-amber-500: oklch(0.75 0.16 80);
  --color-red-500:   oklch(0.57 0.21 25);

  /* Spacing scale (4px base) */
  --space-0:   0px;
  --space-1:   0.25rem;  /*  4px */
  --space-2:   0.5rem;   /*  8px */
  --space-3:   0.75rem;  /* 12px */
  --space-4:   1rem;     /* 16px */
  --space-5:   1.25rem;  /* 20px */
  --space-6:   1.5rem;   /* 24px */
  --space-8:   2rem;     /* 32px */
  --space-10:  2.5rem;   /* 40px */
  --space-12:  3rem;     /* 48px */
  --space-16:  4rem;     /* 64px */

  /* Border radius (MD3-inspired) */
  --radius-xs:   0.125rem;   /*  2px */
  --radius-sm:   0.25rem;    /*  4px */
  --radius-md:   0.5rem;     /*  8px */
  --radius-lg:   0.75rem;    /* 12px */
  --radius-xl:   1rem;       /* 16px */
  --radius-2xl:  1.75rem;    /* 28px */
  --radius-full: 9999px;

  /* Shadows / Elevation */
  --shadow-sm:   0 1px 2px 0 oklch(0 0 0 / 0.05);
  --shadow-md:   0 4px 6px -1px oklch(0 0 0 / 0.1);
  --shadow-lg:   0 10px 15px -3px oklch(0 0 0 / 0.1);
  --shadow-xl:   0 20px 25px -5px oklch(0 0 0 / 0.1);

  /* Breakpoints (mobile-first) */
  --breakpoint-sm:  640px;
  --breakpoint-md:  768px;
  --breakpoint-lg:  1024px;
  --breakpoint-xl:  1280px;
  --breakpoint-2xl: 1536px;
}
```

**Semantic Tokens** (purpose-named, consumed by components):

```css
/* File: tokens/semantic.css */
:root {
  /* Brand colors */
  --color-brand:       var(--color-blue-500);
  --color-brand-hover: var(--color-blue-600);

  /* Surfaces */
  --color-surface:       oklch(1 0 0);
  --color-surface-alt:   var(--color-neutral-50);
  --color-surface-hover: var(--color-neutral-100);

  /* Text */
  --color-text-primary:   var(--color-neutral-900);
  --color-text-secondary: var(--color-neutral-600);
  --color-text-muted:     var(--color-neutral-400);
  --color-text-on-brand:  oklch(1 0 0);

  /* Status (critical for GemLogin workflow states) */
  --color-status-success: var(--color-green-500);
  --color-status-warning: var(--color-amber-500);
  --color-status-error:   var(--color-red-500);

  /* Borders */
  --color-border:       var(--color-neutral-200);
  --color-border-focus: var(--color-blue-500);

  /* Form controls */
  --color-input-bg:     var(--color-surface);
  --color-input-border: var(--color-neutral-300);

  /* Focus ring */
  --ring-offset: 2px;
  --ring-color:  var(--color-blue-400);
}

.dark {
  --color-surface:       oklch(0.15 0 0);
  --color-surface-alt:   oklch(0.18 0 0);
  --color-surface-hover: oklch(0.22 0 0);
  --color-text-primary:   oklch(0.95 0 0);
  --color-text-secondary: oklch(0.70 0 0);
  --color-text-muted:     oklch(0.50 0 0);
  --color-border:         oklch(0.25 0 0);
  --color-input-bg:       oklch(0.18 0 0);
  --color-input-border:   oklch(0.30 0 0);
}
```

### 1.3 GemLogin-Specific Design Concerns

GemLogin is a workflow automation platform. The design system must account for:

| Concern | Design Response |
|---|---|
| **Workflow canvas** | Infinite-pan zoomable surface, minimal chrome |
| **Block/node editor** | Clear visual hierarchy for block types (action, condition, loop, delay) |
| **Status feedback** | Real-time execution state (running / success / failed / pending) with color-coded borders and icons |
| **Data tables** | High-density row layout, sortable columns, inline editing |
| **Multiple profiles** | Compact avatar + status cards, batch selection |
| **Device pairing** | List-detail split view for gemphone + profile association |
| **Cookie management** | Tree viewer for cookie domains with search/filter |
| **Execution log** | Infinite scroll, filterable by level (info/warn/error), timestamp clusters |

---

## 2. Component Library Recommendations

### 2.1 Recommended Stack

| Layer | Choice | Rationale |
|---|---|---|
| **CSS Framework** | Tailwind CSS v4 | CSS-first `@theme`, OKLCH native, Rust compiler for speed, utility-first rapid prototyping |
| **Component Source** | shadcn/ui | Code ownership model, Radix accessibility, CVA variant system, full customization |
| **Headless Primitives** | Radix UI | ARIA-compliant, keyboard navigation, focus management already handled |
| **UI Workshop** | Storybook | Isolated component development, accessibility testing (a11y addon), visual regression, living documentation |
| **Token Format** | System UI Theme Spec | Universal contract between design tokens and all frameworks |

### 2.2 Component Inventory

Based on shadcn/ui's catalog extended for GemLogin-specific needs:

**Core (import from shadcn/ui):**

| Component | Role |
|---|---|
| `Button` | Actions: primary (brand), secondary, outline, ghost, destructive, link |
| `Input` | Form text entry |
| `Select` | Dropdown selection |
| `Checkbox` | Boolean toggle |
| `Switch` | Toggle with visual state |
| `RadioGroup` | Mutually exclusive options |
| `Dialog` / `Modal` | Blocking workflows, confirmations |
| `Sheet` | Side panels for block configuration |
| `Popover` | Contextual menus, quick actions |
| `DropdownMenu` | Multi-item menus |
| `Tabs` | Profile detail sections |
| `Table` | Data display (profile list, execution logs) |
| `Card` | Profile summary cards, device cards |
| `Badge` | Status indicators (running, success, error) |
| `Tooltip` | Block descriptions, truncated text |
| `Toast` | Execution result notifications |
| `Progress` | Long-running operations |
| `Skeleton` | Loading states |
| `Separator` | Visual section breaks |
| `Command` / `Kbd` | Command palette for quick actions |

**GemLogin-Specific (custom built on Radix primitives):**

| Component | Description |
|---|---|
| `WorkflowCanvas` | Infinite-pan, zoomable SVG/Canvas surface for block wiring |
| `BlockNode` | Draggable node with typed ports (input/output), status border, inline config |
| `BlockPalette` | Sidebar drawer of available block types with search |
| `EdgeLine` | Bezier connector between blocks, animated during execution |
| `ExecutionTimeline` | Scrollable log with timestamps, levels, search |
| `ProfileCard` | Compact card: ID, status, device pair, last active |
| `DeviceSelector` | List of gemphones with proxy port, model, status |
| `CookieTree` | Domain-grouped cookie viewer with expand/collapse columns |
| `StatusIndicator` | Animated dot + label: idle, running, success, failed, pending |
| `BatchActionBar` | Floating bar appearing on multi-select: mass start/stop/delete |

### 2.3 Component Architecture Rules

Following shadcn/ui community best practices (2026):

1. **Extend with CVA** — every component uses `class-variance-authority` for type-safe variants
2. **Forward refs** — all interactive components forward refs for form library integration
3. **Preserve Radix primitives** — never override keyboard navigation or ARIA attributes from the underlying Radix component
4. **Use `cn()`** — `clsx` + `tailwind-merge` for safe class composition
5. **Use `asChild`** — for flexible trigger elements without losing accessibility
6. **No `!important`** — never use `!important` in component styles
7. **Semantic tokens only** — components use `bg-primary` not `bg-blue-500`
8. **No manual dark mode** — `dark:` variants are never needed; semantic tokens handle it

### 2.4 Storybook Integration

```
.storybook/
├── main.ts          # Config: stories location, addons (a11y, controls, docs, actions)
├── preview.ts       # Global decorators: ThemeProvider, mock data
├── manager.ts       # Branding, sidebar ordering
└── themes/
    ├── light.ts
    └── dark.ts      # Dark mode toggle in Storybook toolbar
```

Each component gets:
- **Playground story** — interactive controls for all variants
- **States story** — loading, empty, error, disabled states
- **Accessibility story** — a11y addon results, focus behavior demo
- **Dark mode story** — visual verification in both themes

---

## 3. Color System

### 3.1 Color Philosophy

- **OKLCH color space** — perceptually uniform, better than HSL/RGB for design system scales
- **Semantic naming** over literal naming (e.g., `--color-primary` not `--color-blue-500`)
- **Tonal palettes** — 10-step scale (50–900) for each hue, mirroring Tailwind's convention
- **Accessibility-first** — all pairings validated against WCAG 2.2 contrast requirements

### 3.2 Primary Palette

Based on a deep blue identity for GemLogin (trust, automation, data):

| Step | OKLCH Value | Usage |
|---|---|---|
| 50 | `oklch(0.97 0.02 250)` | Background tint |
| 100 | `oklch(0.93 0.04 250)` | Hover surfaces |
| 200 | `oklch(0.88 0.06 250)` | Disabled states |
| 300 | `oklch(0.80 0.09 250)` | Borders, outlines |
| 400 | `oklch(0.70 0.14 250)` | Secondary brand elements |
| **500** | `oklch(0.58 0.18 250)` | **Primary brand** |
| 600 | `oklch(0.47 0.18 250)` | Hover states |
| 700 | `oklch(0.38 0.15 250)` | Active states |
| 800 | `oklch(0.30 0.11 250)` | Pressed text |
| 900 | `oklch(0.22 0.07 250)` | High-contrast backgrounds |

### 3.3 Semantic Color Roles

| Role | Light Token | Dark Token | WCAG Target |
|---|---|---|---|
| `primary` | blue-500 | blue-300 | 4.5:1 on surface |
| `primary-foreground` | white | neutral-900 | — |
| `surface` | white | neutral-900 | — |
| `surface-alt` | neutral-50 | neutral-800 | — |
| `foreground` | neutral-900 | neutral-50 | — |
| `muted` | neutral-100 | neutral-800 | — |
| `muted-foreground` | neutral-500 | neutral-400 | 3:1 on muted bg |
| `destructive` | red-500 | red-400 | 4.5:1 on surface |
| `border` | neutral-200 | neutral-700 | — |
| `input` | neutral-300 | neutral-600 | 3:1 edge contrast |
| `ring` | blue-400 (opacity 0.5) | blue-300 (opacity 0.5) | 3:1 on any bg |

### 3.4 Status Colors (GemLogin Workflow Execution)

```
Running  → blue-500 (pulsing animation)
Success  → green-500
Failed   → red-500 (with error icon)
Pending  → amber-500
Idle     → neutral-400
```

### 3.5 Dynamic Color (Future)

Following MD3's dynamic color pattern: the system should eventually support deriving the full palette from a single seed color via the `@material/material-color-utilities` library, enabling user-defined themes.

---

## 4. Typography Scale

### 4.1 Typeface Selection

| Role | Font Stack | Fallback |
|---|---|---|
| **Display / Headline** | `'Inter', 'SF Pro Display'` | `system-ui, sans-serif` |
| **Body / Label** | `'Inter', 'SF Pro Text'` | `system-ui, sans-serif` |
| **Monospace** (code, logs, cookies) | `'JetBrains Mono', 'Fira Code'` | `monospace` |

Inter is chosen for its exceptional legibility at all sizes, extensive weight range (100–900), and variable font support.

### 4.2 Type Scale

Derived from MD3's 15-point scale, adapted for web (rem units):

| Token | Size | Line Height | Weight | Tracking | Use |
|---|---|---|---|---|---|
| `display-xl` | 3.5625rem (57px) | 4rem (64px) | 400 | -0.25px | Hero headers |
| `display-lg` | 2.8125rem (45px) | 3.25rem (52px) | 400 | 0 | Section titles |
| `display-md` | 2.25rem (36px) | 2.75rem (44px) | 400 | 0 | Page headings |
| `headline-xl` | 2rem (32px) | 2.5rem (40px) | 600 | 0 | Panel titles |
| `headline-lg` | 1.75rem (28px) | 2.25rem (36px) | 600 | 0 | Section headers |
| `headline-md` | 1.5rem (24px) | 2rem (32px) | 600 | 0 | Card titles |
| `title-lg` | 1.375rem (22px) | 1.75rem (28px) | 600 | 0 | Dialog headers |
| `title-md` | 1rem (16px) | 1.5rem (24px) | 600 | 0.15px | Subheaders |
| `title-sm` | 0.875rem (14px) | 1.25rem (20px) | 600 | 0.1px | Small section labels |
| `body-lg` | 1rem (16px) | 1.5rem (24px) | 400 | 0.5px | Body text, descriptions |
| `body-md` | 0.875rem (14px) | 1.25rem (20px) | 400 | 0.25px | Compact body |
| `body-sm` | 0.75rem (12px) | 1rem (16px) | 400 | 0.4px | Captions, metadata |
| `label-lg` | 0.875rem (14px) | 1.25rem (20px) | 500 | 0.1px | Button text |
| `label-md` | 0.75rem (12px) | 1rem (16px) | 500 | 0.5px | Tab labels |
| `label-sm` | 0.6875rem (11px) | 1rem (16px) | 500 | 0.5px | Badge text |

### 4.3 CSS Token Definition

```css
@theme {
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Display */
  --text-display-xl: 3.5625rem;
  --text-display-xl--line-height: 4rem;
  --text-display-xl--font-weight: 400;
  --text-display-xl--letter-spacing: -0.015625rem;

  /* (repeat for all 15 scale points...) */

  /* Body - primary reading */
  --text-body-lg: 1rem;
  --text-body-lg--line-height: 1.5rem;
  --text-body-lg--font-weight: 400;

  /* Label - UI elements */
  --text-label-lg: 0.875rem;
  --text-label-lg--line-height: 1.25rem;
  --text-label-lg--font-weight: 500;
}
```

---

## 5. Accessibility Checklist

### 5.1 WCAG 2.2 Level AA — Full Checklist

#### Perceivable (1.x)

- [ ] **1.1.1 Non-text Content** — All icons, images, and status indicators have meaningful alt text or `aria-label`. Decorative elements use `aria-hidden="true"`.
- [ ] **1.3.1 Info and Relationships** — Semantic HTML (`<nav>`, `<main>`, `<header>`, `<footer>`, `<table>`, `<ul>`) used for structure. ARIA landmarks present.
- [ ] **1.4.1 Use of Color** — Status is never conveyed by color alone. Every color code (green=success, red=failed) paired with an icon or text label.
- [ ] **1.4.3 Contrast (Minimum)** — Text meets **4.5:1** (body) and **3:1** (large text 18px+ bold or 24px+ regular). Tooltips, placeholders, and disabled text exempt.
- [ ] **1.4.4 Resize Text** — 200% zoom with no content loss or horizontal scroll.
- [ ] **1.4.10 Reflow** — No horizontal scroll at 400% zoom (320px equivalent viewport).
- [ ] **1.4.11 Non-text Contrast** — UI components (buttons, inputs, focus indicators) meet **3:1** against adjacent backgrounds.
- [ ] **1.4.12 Text Spacing** — No content loss when user overrides line height (1.5x), paragraph spacing (2x), word spacing (0.16x), letter spacing (0.12x).
- [ ] **1.4.13 Content on Hover or Focus** — Tooltips and popovers are dismissible (Esc), hoverable (pointer moves onto them), and persistent (don't disappear automatically).

#### Operable (2.x)

- [ ] **2.1.1 Keyboard** — Every interactive element (buttons, links, form controls, draggable blocks) is reachable and operable via keyboard alone.
- [ ] **2.1.2 No Keyboard Trap** — Focus never trapped. Modals trap focus only while open, release on close.
- [ ] **2.1.4 Character Key Shortcuts** — If single-key shortcuts exist, they are remappable or turn-offable.
- [ ] **2.4.1 Bypass Blocks** — Skip-to-content link present, visible on first Tab.
- [ ] **2.4.3 Focus Order** — Logical DOM order. Left-to-right, top-to-bottom. No `tabindex > 0`.
- [ ] **2.4.4 Link Purpose (In Context)** — Links/buttons have clear, unique labels. No "click here".
- [ ] **2.4.6 Headings and Labels** — Descriptive headings and form labels.
- [ ] **2.4.7 Focus Visible** — Every focusable element has a visible 2px+ focus ring (3:1 contrast). Never `outline: none`.
- [ ] **2.4.11 Focus Not Obscured (NEW in 2.2)** — Focused element not hidden by sticky headers, banners, or floating UI.
- [ ] **2.5.3 Label in Name** — Accessible name of a component includes the visible text.
- [ ] **2.5.7 Dragging Movements (NEW in 2.2)** — Drag-and-drop operations (e.g., block arrangement on canvas) have a single-pointer alternative (e.g., up/down buttons, paste coordinates).
- [ ] **2.5.8 Target Size (NEW in 2.2)** — Interactive targets at least **24x24 CSS pixels**. Best practice: 44x44px for touch targets.

#### Understandable (3.x)

- [ ] **3.2.1 On Focus** — No unexpected context changes on focus.
- [ ] **3.2.2 On Input** — No unexpected context changes on input without warning.
- [ ] **3.2.6 Consistent Help (NEW in 2.2)** — Help mechanisms in same relative order across pages.
- [ ] **3.3.1 Error Identification** — Form errors described in text, programmatically associated with the input.
- [ ] **3.3.2 Labels or Instructions** — Every form input has a visible `<label>` or `aria-label`.
- [ ] **3.3.7 Redundant Entry (NEW in 2.2)** — Information from a previous step is auto-filled or available for selection.
- [ ] **3.3.8 Accessible Authentication (NEW in 2.2)** — No cognitive function tests (CAPTCHA) without alternatives. Support passkeys, magic links.

#### Robust (4.x)

- [ ] **4.1.2 Name, Role, Value** — All custom controls expose proper name, role, and value via ARIA.
- [ ] **4.1.3 Status Messages** — Dynamic updates (execution status, toast notifications, progress) use `aria-live="polite"` or `role="status"/"alert"`.

### 5.2 GemLogin-Specific Accessibility Requirements

#### Workflow Canvas
- [ ] Block nodes are keyboard navigable (Tab between blocks, Enter to open config, Arrow keys to nudge position)
- [ ] Edge connections announce their source and target blocks to screen readers
- [ ] Canvas zoom level is communicated to screen readers
- [ ] Execution state changes (running -> success/failed) are announced via `aria-live` region
- [ ] Drag-to-connect alternative: select source block, then select target block from a list

#### Execution Log
- [ ] Each log entry is a list item in a semantic `<ol>`
- [ ] Log level (info/warn/error) conveyed by text prefix, not color alone
- [ ] New entries appended dynamically are announced via `aria-live="polite"`
- [ ] Filter controls have clear labels and keyboard support

#### Profile Management
- [ ] Profile cards in a list have `role="list"` / `role="listitem"`
- [ ] Batch selection checkboxes are properly labeled
- [ ] Status badges include text labels (not just color)

#### Block Configuration Dialogs
- [ ] Dialogs trap focus, return it on close
- [ ] All form controls in block config have labels
- [ ] Validation errors are announced to screen readers
- [ ] Required fields are indicated both visually and programmatically (`aria-required="true"`)

### 5.3 Testing Protocol

| Tool/Method | Frequency | What It Catches |
|---|---|---|
| **axe DevTools** (automated) | Every PR | ~40-50% of issues: contrast, ARIA, heading structure |
| **Keyboard-only walkthrough** | Every feature | Focus order, traps, missing Tab stops |
| **VoiceOver (macOS)** | Weekly | Screen reader comprehension, label quality |
| **NVDA (Windows)** | Weekly | Cross-platform screen reader verification |
| **Browser zoom 200%** | Every PR | Text overflow, layout breakage |
| **Contrast checker** | Every color change | Token pairings meeting 4.5:1 / 3:1 |
| **Text Spacing bookmarklet** | Design QA | 1.4.12 compliance |

---

## 6. Development Workflow

### 6.1 Toolchain

```
Figma (design tokens) 
  → Tokens Studio / Style Dictionary (token export)
  → CSS custom properties (tokens/primitives.css + tokens/semantic.css)
  → Tailwind v4 @theme (mapping)
  → shadcn/ui components (consumed via cn() + CVA)
  → Storybook (isolated preview, docs, a11y tests)
```

### 6.2 File Structure

```
design-system/
├── tokens/
│   ├── primitives.css       # Raw color, spacing, radius, shadow values
│   └── semantic.css         # Purpose-mapped tokens (light + dark)
├── components/
│   ├── ui/                  # shadcn/ui base components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   └── ...
│   └── gemlogin/            # GemLogin-specific components
│       ├── workflow-canvas.tsx
│       ├── block-node.tsx
│       ├── status-indicator.tsx
│       └── ...
├── stories/
│   ├── button.stories.tsx
│   ├── block-node.stories.tsx
│   └── ...
├── hooks/
│   ├── use-keyboard-navigation.ts
│   └── use-focus-trap.ts
└── lib/
    └── utils.ts              # cn() helper
```

---

## 7. Key Recommendations Summary

1. **Use Tailwind v4 with OKLCH** — The CSS-first `@theme` paradigm combined with OKLCH color space gives a modern, maintainable, perceptually uniform foundation.

2. **Adopt shadcn/ui as component source** — Code ownership model means full control; Radix underneath guarantees accessibility; CVA ensures consistent variant patterns.

3. **Build Storybook from day one** — Isolated component development, automatic accessibility scanning, and living documentation are critical for a workflow tool with many states.

4. **Three-layer token architecture** — Primitive values (OKLCH) -> Semantic tokens (purpose-named) -> Component consumption. Never hardcode raw colors in components.

5. **MD3-inspired type scale** — 15-point scale with Inter font family covers every UI need from hero displays to badge labels.

6. **WCAG 2.2 AA as minimum bar** — The new 2.4.11 (Focus Not Obscured), 2.5.7 (Dragging Alternatives), and 2.5.8 (Target Size) criteria are especially relevant for the GemLogin workflow canvas and block manipulation.

7. **Accessibility is not optional** — Every component must pass automated + manual + screen reader testing before being considered complete.
