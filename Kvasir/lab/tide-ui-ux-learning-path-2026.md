# TIDE UI/UX Learning Path 2026

> A practical, hands-on curriculum for a junior developer leveling up UI/UX skills.
> Designed to be done alongside regular work -- no theory dumps, just building.

---

## Table of Contents

1. [Hands-On Learning Path (8 Weeks)](#1-hands-on-learning-path-8-weeks)
2. [Best Free Learning Resources 2026](#2-best-free-learning-resources-2026)
3. [Practice Projects (Progressive Difficulty)](#3-practice-projects-progressive-difficulty)
4. [Tools to Master](#4-tools-to-master)
5. [Component Challenge: Build 10 Modern UI Components](#5-component-challenge-build-10-modern-ui-components)
6. [UI Code Review Checklist](#6-ui-code-review-checklist)
7. [Thai Market UI Patterns](#7-thai-market-ui-patterns)
8. [Weekly Schedule Template](#8-weekly-schedule-template)

---

## 1. Hands-On Learning Path (8 Weeks)

### Week 1 -- Visual Fundamentals & The Language of UI

**Goal:** Train your eye. Learn what makes UI look good vs. bad.

| Day | Topic | Exercise |
|-----|-------|----------|
| 1 | Visual hierarchy -- what draws the eye first | Open any 3 popular apps (LINE, Shopee, TikTok). Screenshot. Draw circles around where your eye lands first, second, third. Notice patterns. |
| 2 | Color theory -- hue, saturation, contrast | Pick a color palette from coolors.co. Create a 3-card UI in Figma using only that palette + white. No code. |
| 3 | Typography basics -- serif, sans, hierarchy | Take a paragraph of Thai text. Set it in 3 different font sizes/weights. Arrange as heading + sub + body. |
| 4 | Spacing & the 8px grid | Recreate a simple login screen from memory. Then add an 8px grid overlay. Notice where you were off. |
| 5 | Layout: proximity, alignment, repetition | Open dribbble.com. Find 3 UI shots you like. In Figma, trace the layout boxes (not the content). |
| 6 | Review & copywork | Pick one dribbble shot. Recreate it pixel-by-pixel in Figma. No shortcuts. |
| 7 | REST | Reflect. Note what was hardest. |

**Deliverable:** 3 Figma files -- palette exploration, login screen, dribbble copy.

**Resources:** DesignCourse YouTube (Gary Simon), Laws of UX website.

---

### Week 2 -- Figma Deep Dive: Tool Mastery

**Goal:** Move from "knowing Figma" to being productive in Figma.

| Day | Topic | Exercise |
|-----|-------|----------|
| 1 | Auto Layout basics | Take the login screen from Week 1. Rewrite it using Auto Layout for everything. |
| 2 | Components & instances | Create a button component with 3 variants: primary, secondary, ghost. Use it 10 times on a page. |
| 3 | Variants & properties | Extend the button: add `disabled`, `loading`, `icon` properties. |
| 4 | Component properties (text, boolean, swap) | Create a card component where you can swap the image and change the title text in one click. |
| 5 | Constraints & responsive design | Build a simple dashboard frame. Set constraints so it looks good at 375px and 1440px. |
| 6 | Prototyping basics | Connect 3 screens with interactions: button tap -> next screen, back swipe -> previous. |
| 7 | REST | Polish your component library into a mini design system file. |

**Deliverable:** A Figma file with button system + card component + 3-screen prototype.

**Resources:** freeCodeCamp 6-hour Figma course (YouTube), Figma Learn Design Hub (free, official).

---

### Week 3 -- HTML/CSS Foundations for UI Developers

**Goal:** Build UI with code, not just design tools.

| Day | Topic | Exercise |
|-----|-------|----------|
| 1 | Semantic HTML -- structure over div soup | Take a Figma design. Write the HTML structure first using `<header>`, `<main>`, `<section>`, `<article>`, `<nav>`. |
| 2 | Flexbox -- the modern layout workhorse | Flexbox Froggy (all levels). Then rebuild your login page layout with flexbox. |
| 3 | CSS Grid -- 2D layouts | Grid Garden (all levels). Then build a photo gallery grid. |
| 4 | CSS custom properties (variables) | Take a button component. Extract colors, spacing, radius into CSS variables. Change theme with one `:root` swap. |
| 5 | Responsive design with media queries & container queries | Build a card that stacks at mobile (375px) and becomes a horizontal row at desktop (1024px). |
| 6 | CSS transitions & hover effects | Add smooth hover/active states to your button component. Duration < 300ms. Ease-out curve. |
| 7 | REST + review | Commit your week's work to a repo. |

**Deliverable:** A GitHub repo with a responsive component page (buttons, cards, gallery) using semantic HTML + modern CSS.

**Resources:** Flexbox Froggy, Grid Garden, CSSBattle.dev.

---

### Week 4 -- Building Real Components (HTML/CSS)

**Goal:** 5 UI components built from scratch, with proper states and responsiveness.

Build these without frameworks (vanilla HTML/CSS):

1. **Navigation bar** -- logo, 4 links, mobile hamburger menu, active state
2. **Modal/dialog** -- overlay, centered card, close button (X + Escape key), body scroll lock
3. **Accordion** -- 3 sections, smooth open/close, open indicator icon, keyboard accessible
4. **Tab panel** -- 4 tabs, content panel switches, selected tab underline animation
5. **Form with validation** -- email, password, submit button, inline error messages, success state

**Deliverable:** A single HTML page with all 5 components isolated in sections, fully responsive.

**Key constraint:** No JavaScript frameworks. Pure HTML/CSS/JS. This teaches fundamentals that frameworks abstract away.

---

### Week 5 -- Accessibility First

**Goal:** Build UI that works for everyone. This is not optional in 2026.

| Day | Topic | Exercise |
|-----|-------|----------|
| 1 | Semantic HTML for a11y | Run your Week 4 page through axe DevTools. Fix every issue found. |
| 2 | Keyboard navigation | Tab through your components. Can you reach everything? Can you close the modal with Escape? Can you arrow-key through tabs? |
| 3 | ARIA labels & roles | Add `aria-label` to icon buttons, `aria-expanded` to accordion triggers, `role="tablist"` to tab sets. |
| 4 | Color contrast (WCAG AA) | Use the Chrome DevTools color picker to check every text/background pair. Target 4.5:1 for normal text, 3:1 for large. |
| 5 | Screen reader testing | Turn on VoiceOver (Mac) or NVDA (Windows). Navigate your page with eyes closed. |
| 6 | Focus indicators & reduced motion | Add visible `:focus-visible` outlines. Respect `prefers-reduced-motion`. |
| 7 | REST + audit | Generate a Lighthouse a11y report. Score 95+ or fix until you do. |

**Deliverable:** Your Week 4 page updated with full accessibility fixes. Lighthouse a11y score 95+.

**Resources:** axe DevTools (free Chrome extension), WCAG Quick Reference, NVDA screen reader (free).

---

### Week 6 -- Chrome DevTools for UI Debugging

**Goal:** Use DevTools like a surgeon, not a tourist.

| Day | Topic | Exercise |
|-----|-------|----------|
| 1 | Elements panel -- inspect, edit, delete | Take any live website. Inspect and edit 5 things in real-time (change text, color, padding). |
| 2 | Styles pane -- computed, box model, states | Debug a CSS specificity issue. Find why a rule isn't applying. Check the computed tab. |
| 3 | Layout debugging -- flexbox overlays, grid overlays | Open DevTools Layout panel. Toggle flexbox/grid overlays on a complex layout. Understand the alignment. |
| 4 | Performance -- paint flashing, layout shifts | Record a page load. Check Performance tab. Identify layout shifts (CLS). Find long tasks. |
| 5 | Lighthouse reports | Run Lighthouse on 3 sites (your own, Shopee Thailand, a competitor). Compare scores. |
| 6 | Rendering -- paint, layout, compositing triggers | Go to the Rendering tab. Toggle "paint flashing." Every green flash is a repaint that could be avoided. |
| 7 | REST + practice | Spend 1 hour debugging a real UI issue in your project using DevTools. |

**Deliverable:** A written log of 3 UI bugs you found and fixed using DevTools.

**Resources:** Chrome DevTools docs (free), "Can't Unsee" game for pixel-eye training.

---

### Week 7 -- Animation & Micro-interactions

**Goal:** Make UI feel alive and responsive. Not decorative -- functional.

| Day | Topic | Exercise |
|-----|-------|----------|
| 1 | CSS transitions -- what, when, how long | Add transitions to all interactive elements from Week 4. Duration 150-300ms. Ease-out. |
| 2 | CSS `@keyframes` animations | Create a loading spinner, a skeleton loader, and a "success check" animation. |
| 3 | Transform & opacity only (GPU compositing) | Audit your animations. Replace anything animating `width`, `height`, `top`, `left` with `transform`. |
| 4 | Framer Motion basics (if using React) or Web Animations API | Animate a modal entering from the top and fading in. Exit animation mirrors entry. |
| 5 | Micro-interactions in practice | Add: button press feedback, card hover lift, form field focus glow, error shake. |
| 6 | `prefers-reduced-motion` | Wrap all animations. Respect user motion preferences. Store preference in a CSS custom property. |
| 7 | REST + review | Record a screencast of your animated page. Check that everything is smooth (60fps). |

**Deliverable:** Your Week 4 page with polished micro-interactions. Smooth at 60fps. Respects reduced motion.

**Key principle:** Animation should serve a purpose -- guide attention, give feedback, show relationship. Never animate for its own sake.

---

### Week 8 -- Design-to-Code Handoff & Review

**Goal:** Bridge the gap between Figma design specs and production code.

| Day | Topic | Exercise |
|-----|-------|----------|
| 1 | Figma Dev Mode | Open Dev Mode in Figma. Export CSS code from a design. Compare with your hand-written CSS. |
| 2 | Design tokens -- colors, spacing, typography as code | Extract a `tokens.css` file from a Figma design system. Match variable names 1:1. |
| 3 | Pixel QA -- does code match design? | Take a Figma screen. Build it in code. Overlay the design as a semi-transparent PNG. Check alignment. |
| 4 | Cross-browser testing | Test your page in Chrome, Firefox, Safari, Edge. Find 3 differences. Fix them. |
| 5 | Review other people's UI code | Find a UI component on GitHub. Review it against the checklist in Section 6. |
| 6 | Final project assembly | Package your 10 components (from Section 5) into a single showcase page. |
| 7 | REST + celebrate | You now have a portfolio-ready UI demo. Commit, push, share with the team. |

**Deliverable:** A complete showcase page with all 10 components (Section 5), a11y score 95+, responsive, animated. Figma source files included.

---

## 2. Best Free Learning Resources 2026

### YouTube Channels

| Channel | Best For | Why |
|---------|----------|-----|
| [DesignCourse](https://youtube.com/@DesignCourse) (Gary Simon) | UI fundamentals, color, typography | Most comprehensive free channel. Walks through full designs. |
| [The Futur](https://youtube.com/@thefutur) | Design thinking, client work | Why design decisions matter, not just how. |
| [Flux Academy](https://youtube.com/@FluxAcademy) | Visual aesthetics, Figma to code | High production value. Full design workflows. |
| [freeCodeCamp](https://youtube.com/@freeCodeCamp) | Full-length courses | 6-hour Figma course, CSS courses, responsive design. |
| [Mizko](https://youtube.com/@mizko) | Systematic design thinking | Real-world product design workflows. |
| [AJ&Smart](https://youtube.com/@AJSmart) | UX process, design sprints | Usability testing, user research in practice. |
| [CharliMarieTV](https://youtube.com/@CharliMarieTV) | UX process, career tips | Practical advice from a working designer. |
| [Kevin Powell](https://youtube.com/@KevinPowell) | CSS deep dives | Best CSS teacher on YouTube. Responsive design, modern CSS. |

### Free Courses & Interactive Learning

| Resource | Type | What It Covers |
|----------|------|----------------|
| [Figma Learn Design Hub](https://help.figma.com/hc/en-us/categories/360002042553-Figma-Design) | Official docs + tutorials | Everything Figma: components, variables, auto layout, prototyping |
| [Google UX Design Certificate](https://www.coursera.org/professional-certificates/google-ux-design) (audit free) | Structured course (6 months) | Full UX process: research, wireframing, prototyping, testing |
| [Hack Design](https://hackdesign.org/) | Weekly lessons by email | Lessons from Google/Facebook/Spotify designers |
| [Laws of UX](https://lawsofux.com/) | Reference site | Usability principles with visual examples |
| [Nielsen Norman Group](https://www.nngroup.com/articles/) | Articles & videos | Gold-standard UX research -- practical, evidence-based |
| [Octet Design Figma Course](https://octet.design/academy/figma-course/) | Free structured course | 11 chapters: design to prototyping |

### Interactive Playgrounds (Best for Hands-On Practice)

| Playground | Skill | Link |
|------------|-------|------|
| Flexbox Froggy | CSS Flexbox | flexboxfroggy.com |
| Grid Garden | CSS Grid | cssgridgarden.com |
| CSSBattle | Visual CSS accuracy | cssbattle.dev |
| Frontend Mentor | Real design-to-code challenges | frontendmentor.com |
| CodePen | Social experimentation | codepen.io |
| CSS Zen Garden | One HTML, infinite CSS styles | csszengarden.com |

### Documentation to Bookmark

- [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS) -- The source of truth
- [Web.dev (Google)](https://web.dev/learn/) -- Performance, a11y, responsive guides
- [WCAG Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) -- Accessibility checklist
- [Every Layout](https://every-layout.dev/) -- Reusable CSS layout patterns

---

## 3. Practice Projects (Progressive Difficulty)

### Level 1: Component Pages (Week 1-2 of learning)

Build a page that shows off a single component in all its states. No routing, no frameworks.

- **Profile Card** -- avatar, name, bio, stats, follow button (with idle/hover/active/loading states)
- **Pricing Table** -- 3 tiers, feature list, CTA button, popular badge, hover effects
- **Dashboard Widget** -- chart placeholder, data rows, filter dropdown, refresh button

### Level 2: Single-Page Interfaces (Week 3-4)

Build a full page that looks like a real app. Still static HTML/CSS/JS.

- **Music Player UI** -- cover art, progress bar, play/pause/next, volume slider, playlist sidebar
- **Messaging Interface** -- contact list, chat bubble (sent/received), input bar, typing indicator
- **E-commerce Product Page** -- image gallery with thumbnails, size picker, color swatches, add-to-cart, reviews section

### Level 3: Multi-State & Interactive (Week 5-6)

Add real interactivity, data, and state management.

- **Kanban Board** -- 3 columns (To Do / In Progress / Done), drag cards between columns, add/delete cards, local storage persistence
- **Weather Dashboard** -- fetch from free API, search cities, display current + 5-day forecast, loading/error/empty states, toggle C/F
- **Authentication Flow** -- login form -> validation -> loading spinner -> success redirect -> protected page. Mock API.

### Level 4: Production-Ready App (Week 7-8)

Full app with real polish.

- **Recipe Manager** -- grid of recipe cards, search by ingredient, filter by diet type, click for detail modal, form to add new recipe, save to localStorage. Fully responsive, accessible, animated.

**Golden rule for all projects:** Every component must handle: **idle state, loading state, empty state, error state, edge cases**. This is what separates junior from mid-level work.

---

## 4. Tools to Master

### Figma (Industry Standard)

**What to learn in order:**

1. Frames, shapes, text, images
2. Auto Layout (this is where 80% of the value is)
3. Components & instances
4. Variants & component properties
5. Constraints & responsive resizing
6. Styles (colors, text, effects as reusable tokens)
7. Prototyping (connections, transitions, overlays)
8. Dev Mode (inspect, export CSS, handoff to engineers)

**Free learning path:**
- Days 1-2: [Figma Learn Design Hub](https://help.figma.com/) basics
- Days 3-5: [freeCodeCamp 6-hour Figma course](https://www.freecodecamp.org/news/learn-figma-for-ui-ux-design/) on YouTube
- Day 6+: Rebuild one real app screen per day in Figma

### Chrome DevTools for UI Debugging

**Essential panels:**

| Panel | Use It For | Hotkey |
|-------|------------|--------|
| Elements | Inspect/edit HTML + CSS in real time | Ctrl+Shift+C |
| Styles | Debug specificity, computed values, box model | (Elements panel) |
| Computed | See final rendered values after all overrides | (Styles sidebar) |
| Layout | Visual flexbox/grid overlay debugging | (Layout tab in Elements) |
| Lighthouse | Performance, a11y, SEO, best practices audit | Ctrl+Shift+I -> Lighthouse |
| Performance | Find jank, long tasks, layout thrashing | Ctrl+Shift+I -> Performance |
| Rendering | Paint flashing, layout shift, FPS meter | Ctrl+Shift+P -> "Rendering" |
| Coverage | See unused CSS/JS per page load | Ctrl+Shift+P -> "Coverage" |

**Exercise:** Every day for a week, open DevTools on a different popular site. Find one thing to improve. Take a screenshot of your finding.

### Accessibility Testing Tools

| Tool | Cost | What It Does |
|------|------|-------------|
| [axe DevTools](https://www.deque.com/axe/devtools/) | Free | Automated a11y scan in the browser. Finds 57% of WCAG issues automatically. |
| [Lighthouse](https://developer.chrome.com/docs/lighthouse/) | Free (built into Chrome) | Scores a11y 0-100 with specific guidance. |
| [WAVE](https://wave.webaim.org/) | Free | Visual overlay showing a11y issues directly on the page. |
| [NVDA Screen Reader](https://www.nvaccess.org/) | Free (Windows) | Test your app the way blind users experience it. |
| [Colour Contrast Checker](https://webaim.org/resources/contrastchecker/) | Free | Check WCAG AA/AAA contrast ratios. |
| [Accessibility Insights](https://accessibilityinsights.io/) | Free (Microsoft) | Guided a11y testing for web + Android + Windows. |

**Your minimum standard:** Run axe DevTools on every component you build. Fix every issue. Run Lighthouse a11y audit. Score 95+.

### Additional Tools

| Tool | Purpose | Free? |
|------|---------|-------|
| [Coolors](https://coolors.co/) | Color palette generation | Yes |
| [Fontsource](https://fontsource.org/) | Self-hosted open-source fonts | Yes |
| [Heroicons](https://heroicons.com/) | SVG icons (outline + solid) | Yes |
| [Phosphor Icons](https://phosphoricons.com/) | Flexible icon set | Yes |
| [Can I Use](https://caniuse.com/) | Browser feature support | Yes |
| [PageSpeed Insights](https://pagespeed.web.dev/) | Real-world performance data | Yes |

---

## 5. Component Challenge: Build 10 Modern UI Components

Build these 10 components from scratch (vanilla HTML/CSS/JS or with your framework of choice). Each component must handle all states: idle, hover, active, focus, disabled (where applicable), loading (where applicable), empty (where applicable), error (where applicable), and keyboard interaction.

### The 10 Components

**1. Button System**
- Variants: primary, secondary, ghost, danger, link
- States: idle, hover, active, focus-visible, disabled, loading (spinner)
- Sizes: sm, md, lg
- Full keyboard accessibility (Enter/Space to activate)

**2. Navigation Bar**
- Logo left, links center/right, mobile hamburger
- Active link indicator
- Dropdown submenu on one link (with hover + focus handling)
- Mobile: hamburger toggles full-screen drawer with smooth animation
- Sticky top with backdrop blur

**3. Modal / Dialog**
- Overlay background
- Centered card with title, content, actions
- Close: X button + Escape key + click-outside-to-close
- Body scroll lock when open
- Enter animation (fade in + scale up)
- Exit animation (fade out + scale down)
- Focus trap (Tab cycles within modal)

**4. Accordion / Collapse**
- 3-5 sections
- Only one open at a time (or multiple -- configurable)
- Smooth height animation (not `height: auto` -- use `grid-template-rows` trick or JS)
- Plus/minus or chevron indicator with rotation animation
- `aria-expanded`, `aria-controls`, `role="region"`

**5. Tab Panel**
- Horizontal tab bar, 4 tabs
- Content panel switches on click
- Selected tab underline slides to position
- Keyboard: Arrow keys to switch tabs, Tab to go into content
- `role="tablist"`, `role="tab"`, `role="tabpanel"`

**6. Card Component**
- Image (with aspect ratio), title, description, action button
- Hover: subtle lift (transform + shadow)
- Variants: with/without image, with/without footer, horizontal/vertical layout
- Responsive: vertical on mobile, horizontal on desktop (or grid)
- Skeleton loading state

**7. Form Input System**
- Text input, email, password, textarea, select dropdown
- All with: label, placeholder, helper text, error message
- States: idle, focused, valid, invalid, disabled, readonly
- Inline validation on blur
- Character count for textarea
- Password visibility toggle

**8. Toast / Notification**
- Position: top-right by default
- Variants: success, error, warning, info
- Auto-dismiss after 5s (configurable)
- Stack multiple toasts
- Enter animation (slide in), exit (slide out + fade)
- Close button on each
- Pause dismiss on hover

**9. Tooltip**
- Position: top, bottom, left, right (with auto-flip)
- Show on hover + focus
- Arrow pointing to trigger element
- Delay show (300ms), instant hide
- Pure CSS where possible, JS for positioning
- `role="tooltip"`

**10. Data Table**
- Sortable columns (click header to sort asc/desc with indicator)
- Search/filter row
- Striped rows
- Responsive: horizontal scroll on small screens OR collapse to card layout
- Loading skeleton
- Empty state illustration + message
- Row hover highlight

### Challenge Rules

1. Build in order. Each component uses skills from the previous ones.
2. No copying from component libraries (shadcn, MUI, etc.). Understand the implementation.
3. After building all 10, compare your code with a production library. Note the differences.
4. Keep all 10 in a single repo. This becomes your UI portfolio piece.

---

## 6. UI Code Review Checklist

Use this when reviewing UI code (your own or a teammate's). Organized by priority.

### P0: Must Fix (Blocks Merge)

- [ ] **Keyboard navigation:** Can every interactive element be reached and activated with keyboard alone? Tab order is logical?
- [ ] **Focus indicators:** Every interactive element has a visible `:focus-visible` style (not `outline: none`)?
- [ ] **Color contrast:** All text meets WCAG AA (4.5:1 normal, 3:1 large)? Run axe DevTools.
- [ ] **Form labels:** Every input has an associated `<label>` or `aria-label`?
- [ ] **Semantic HTML:** `<button>` for actions, `<a>` for navigation, headings in proper hierarchy (`h1` -> `h2` -> `h3`)?
- [ ] **No layout shift (CLS):** Content doesn't jump around as page loads. Fixed sizes for images, ads, embeds.
- [ ] **Touch targets:** Every interactive element is at least 44x44px on touch devices (WCAG 2.5.8 AA).

### P1: High Priority

- [ ] **Responsive at breakpoints:** Test at 375px, 768px, 1024px, 1440px. No horizontal scroll. No overlapping elements.
- [ ] **Fluid typography:** Uses `clamp()` or viewport units, not fixed px for body text?
- [ ] **Accessible names for icon-only controls:** `aria-label` on icon buttons. No empty `<span>` as icon.
- [ ] **Reduced motion:** Animations respect `prefers-reduced-motion: reduce`. No autoplaying video/gifs.
- [ ] **Loading states:** Every data-fetching component shows a loading indicator (skeleton is preferred).
- [ ] **Empty states:** When data is empty, user sees a helpful message + action, not a blank white area.
- [ ] **Error states:** API failures show a friendly error message + retry button, not a broken UI or silent failure.

### P2: Should Fix

- [ ] **Animation performance:** Only `transform` and `opacity` are animated (GPU-composited). No `width`, `height`, `top`, `left` animation.
- [ ] **Animation duration:** Hover/active feedback < 150ms. Entrance animations < 300ms.
- [ ] **Consistent spacing:** Uses a spacing scale (4px / 8px / 12px / 16px / 24px / 32px / 48px / 64px). No random values.
- [ ] **Color system:** Uses CSS custom properties, not hardcoded hex values. Works in both light and dark mode.
- [ ] **Image optimization:** `loading="lazy"` on below-fold images. `srcset` for responsive images. Proper aspect ratio.
- [ ] **Font loading:** `font-display: swap` to prevent invisible text during font load. System font stack as fallback.
- [ ] **Modal focus trap:** Tab key cycles within the modal. Closing with Escape works. Body scroll is locked.
- [ ] **Touch support:** Hover effects don't get "stuck" on touch devices. Use `@media (hover: hover)` to gate hover styles.

### P3: Nice to Have

- [ ] **Container queries:** Reusable components adapt to their container, not just the viewport.
- [ ] **Reduced data query:** Respects `prefers-reduced-data` (user wants to save bandwidth).
- [ ] **Print styles:** Basic `@media print` styles so pages are printable.
- [ ] **Progressive enhancement:** Core content and functionality works without JavaScript.
- [ ] **CSS `:has()` usage:** Modern selectors used where appropriate for cleaner CSS.
- [ ] **Bundle size:** CSS/JS is code-split. No unused imports. Tree-shaking verified.

### Browser QA Checklist (Run Before Merge)

- [ ] Chrome (latest) -- layout, fonts, interactions correct
- [ ] Firefox (latest) -- no CSS specificity surprises
- [ ] Safari (latest) -- check for WebKit-only bugs (sticky, scroll, grid)
- [ ] Mobile Safari (iOS 16+) -- touch targets, safe areas (notch), keyboard handling
- [ ] Chrome Android -- same as mobile but with Android behaviors
- [ ] 3G network throttle -- Lighthouse performance, loading experience
- [ ] Screen reader (NVDA / VoiceOver) -- navigate entire flow

### Performance Budget (Google 2026 Core Web Vitals)

| Metric | Target | What It Measures |
|--------|--------|------------------|
| LCP (Largest Contentful Paint) | < 2.5s | Perceived load speed |
| INP (Interaction to Next Paint) | < 200ms | Responsiveness to user input |
| CLS (Cumulative Layout Shift) | < 0.1 | Visual stability |
| TBT (Total Blocking Time) | < 200ms | JS execution blocking main thread |

**Lighthouse targets:** Performance 90+, Accessibility 95+, Best Practices 95+, SEO 90+.

---

## 7. Thai Market UI Patterns

### Why This Matters

Thailand is a mobile-dominant market (80%+ of online purchases happen on mobile). UI patterns that work in Western markets don't always translate. This section covers what specifically works for Thai users.

### Mobile-First Is Not a Slogan -- It's the Only Reality

- **Primary screen size:** 6-inch phone. Not tablet. Not desktop.
- **Thumb zone:** Critical actions (CTA, submit, add-to-cart) must be in the bottom third of the screen within thumb reach.
- **Navigation:** Bottom navigation bars are standard. Hamburger menus have lower engagement.
- **No hover:** Thai users primarily use touch. Never rely on hover for critical functionality. Always test on an actual Android phone.

### LINE Integration Patterns

LINE is not optional in Thailand. It is the primary communication platform.

- **Floating LINE button:** A persistent "Contact via LINE" button (not a popup) outperforms complex support flows. Links to LINE OA.
- **LINE Login:** Consider offering LINE Login as an auth option. Many Thai users have LINE but not Google accounts.
- **LINE Rich Menu:** For web apps, deep-link to specific LINE OA rich menu actions.
- **Share to LINE:** Social sharing should prominently feature LINE, not just Facebook/Twitter.
- **LINE Notify for notifications:** Push notifications through LINE have higher open rates than email or SMS.
- **LINE OA as support channel:** Don't build an in-app chat system. Route support to LINE OA. Users prefer it.

### Payments UX (Thai-Specific)

| Payment Method | UX Consideration |
|----------------|-----------------|
| **PromptPay** (40-44% of online payments) | Show as first payment option. Auto-generate QR code. Show expiry timer (usually 5 min). |
| **TrueMoney Wallet** | Prominent wallet option. Show balance if possible. |
| **Rabbit LINE Pay** | Link to LINE account. Show as LINE-branded option. |
| **COD (Cash on Delivery)** | Still relevant. Show COD fee clearly, not hidden. |
| **Credit/Debit cards** | Show local bank logos (KBank, SCB, BBL, Krungthai). Support 3D Secure 2. |

**Key rule:** The payment method order matters. Hide PromptPay behind a collapsible section and you lose conversions.

### Thai Typography on the Web

**Font recommendations:**

| Use Case | Font | Why |
|----------|------|-----|
| Body text (16px+) | **TH Sarabun New** (Google Fonts) | Most recognizable Thai web font. Clean, official, free. |
| Longer reading | **Cordia New** | Slightly more open counters, better for paragraphs. |
| Headlines | **Noto Sans Thai** | Modern, variable weight, Google-maintained. |
| Accessibility-focused | **FT Manifest UD** | Designed for legibility at small sizes and for low-vision users. |
| Modern/branded | **Anuphan** (Google Fonts) | Modern Thai-Latin pairing, variable weight. |

**Key typography rules for Thai:**

- **Minimum body size: 16px** -- Thai characters need more space than Latin. Below 14px, vowel and tone marks become illegible.
- **Line-height: 1.6-1.8** -- Thai text needs more vertical space due to vowel/tone mark stacking above and below consonants.
- **Font weight:** Thai script at 300 weight (light) becomes illegible. Use regular (400) or medium (500) as minimum.
- **Bilingual layouts:** Allow 30-50% more vertical space for Thai text compared to English. A Thai label can be 2x the character count of its English equivalent.
- **Font pairing:** Use a font that supports both Thai and Latin (Noto Sans Thai, Anuphan, Sarabun). Avoid mixing a Thai font with a separate Latin font -- they often clash.

### Color & Cultural Sensitivity

- **Red:** Can signify danger or debt in Thai culture, not celebration. Avoid red as a primary CTA color unless testing proves otherwise.
- **Yellow:** Auspicious (associated with King Rama IX). Works well for highlights and positive affordances.
- **Gold:** Luxury, premium, Buddhist temples. Works for VIP/premium tiers.
- **Green:** Generally positive (nature, money). Banks use green extensively (KBank, SCB, etc.).
- **Pastel palettes:** Very popular in Thai consumer apps. Soft pinks, peaches, light blues dominate beauty/food/e-commerce.
- **Avoid dark red + black combinations:** Associated with gambling and negative connotations.

### Thai Design Patterns That Convert

- **Social proof at decision points:** Thai users are highly influenced by social proof. Units sold counters, customer review photos (real ones, not stock), and LINE OA verification badges should be visible without scrolling.
- **Festival-themed UI:** Thailand has many shopping festivals (11.11, 12.12, Chinese New Year, Songkran, Mother's Day). Seasonal theming that matches festivals drives conversions. This includes red/gold for Chinese New Year, water/blue for Songkran.
- **Product photography:** Minimum 5 images: front, back, detail close-up, scale reference (worn/used on a real person), lifestyle context. Short video clips showing product in use are expected, not optional.
- **Address forms:** Thai addresses follow "house number, soi, street, sub-district, district, province, postcode" format. Never use Western address templates. Allow Thai script input.
- **Multiple contact channels:** Thai users expect to reach you via LINE, phone call, Facebook page, and in-app chat. Fewer options = less trust.
- **Cash on Delivery = trust signal:** Showing "COD available" prominently increases conversion even for users who pay digitally. It signals the business is real.
- **PromptPay QR as trust signal:** Auto-generated PromptPay QR codes with the business name displayed signal legitimacy.

### Thai Market Mobile Performance

- Thailand has excellent 5G coverage in urban areas but variable connectivity in rural/provincial areas.
- **File sizes matter:** Keep page weight under 1-1.5 MB. Heavy pages with large images lose users on slower connections.
- **CDN with Bangkok edge node:** Essential for sub-second load times. Static assets should be served from Singapore or Bangkok nodes.
- **App-like experience is expected:** Thai mobile users expect PWA-like instant loading. Skeleton screens are preferred over spinners.
- **Offline resilience:** For apps targeting provincial areas, consider service worker caching and offline fallback.

### Localization UX Checklist

- [ ] Thai is the default language, not a toggle
- [ ] Numbers use Thai digit grouping (1,234,567 not 1.234.567)
- [ ] Date format: dd/mm/yyyy or with Buddhist year (พ.ศ. = year + 543)
- [ ] Currency: ฿1,234 (THB symbol, no space, comma separators)
- [ ] Address fields accept Thai script, flexible format, allow long strings
- [ ] Mobile number field: +66 prefix (default), 10-digit Thai numbers validated
- [ ] Time: 24-hour format is standard
- [ ] Font: Thai-supporting font loaded and rendering correctly at 16px+
- [ ] Payment methods: PromptPay first, then wallets, then cards
- [ ] Contact options: LINE at minimum, phone call optional
- [ ] Error messages in Thai, not English machine translations
- [ ] Buddhist calendar support if age/date of birth fields

---

## 8. Weekly Schedule Template

This template fits alongside a full-time job. Adjust as needed.

### Weekdays (Mon-Fri): 45-60 min/day

| Time | Activity |
|------|----------|
| First 10 min | Read one article from Laws of UX or NN Group |
| Next 30 min | Hands-on exercise from this guide |
| Last 5 min | Note one thing you learned + one question for tomorrow |

### Weekends: 2-3 hours each day

- **Saturday:** Build the week's component. Don't skip states. Don't rush.
- **Sunday:** Review + polish. Run a11y audit. Refactor ugly code. Commit.

### Progress Tracking

- Keep a `learning-log.md` with dates, what you built, what you struggled with
- After each component, write 3 sentences about what you'd do differently
- Share progress with PYKE or JIMMY weekly

---

## Quick Reference: What to Learn When

| Skill | Start Week | Proficiency Target |
|-------|-----------|-------------------|
| Visual hierarchy & layout | Week 1 | Can explain why a design works or doesn't |
| Figma basics | Week 2 | Can build production-ready components |
| Semantic HTML | Week 3 | Write meaningful structure without thinking |
| CSS Flexbox & Grid | Week 3 | Reach for the right layout method instinctively |
| Accessibility | Week 5 | Ship nothing that fails axe DevTools |
| DevTools debugging | Week 6 | Fix any CSS issue in under 5 minutes |
| Animation | Week 7 | Add micro-interactions that feel natural |
| Design-to-code handoff | Week 8 | Match Figma within 2px |

---

*Compiled by TIDE -- July 2026*

*Sources: freeCodeCamp, Laws of UX, NN Group, DesignCourse, Figma Learn, WCAG, Google Web.dev, MCIX Agency, Yes Web Design Studio, Chiang Rai Times, Research by Rachapoom Punsongserm (Thammasat University) on Thai typography legibility.*
