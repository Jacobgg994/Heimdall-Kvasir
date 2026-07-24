# Modern UI Architecture Patterns 2026

> Research compiled for CORAL dev team — practical, actionable findings for a Thai-market SaaS team

---

## Table of Contents

1. [React Server Components (RSC)](#1-react-server-components-rsc)
2. [Streaming SSR & Partial Hydration](#2-streaming-ssr--partial-hydration)
3. [Islands Architecture](#3-islands-architecture)
4. [Signals & State Management](#4-signals--state-management)
5. [Edge & Distributed Rendering](#5-edge--distributed-rendering)
6. [AI-Driven UI Patterns](#6-ai-driven-ui-patterns)
7. [Performance as UX](#7-performance-as-ux)
8. [Cross-Platform Convergence](#8-cross-platform-convergence)

---

## 1. React Server Components (RSC)

### Production Readiness: MATURE

React Server Components are **fully stable since React 19** and are the default architectural choice in Next.js App Router. No longer experimental — major e-commerce, analytics, and SaaS apps are in production.

| Metric | 2026 Reality |
|---|---|
| Stability | Stable since React 19 (2024) |
| Primary framework | Next.js App Router (most mature) |
| Other support | React Router v7 (experimental), Waku (alpha) |
| Typical bundle reduction | 40–74% JavaScript reduction |
| TTFB improvement | 3-5x faster with streaming |

**Caveat**: The Flight protocol has had CVEs (e.g., React2Shell CVE-2025-55182, CVSS 10.0). Keep React deps updated.

### Key Patterns

**Default to Server Components**: Every component is a server component by default. Only add `'use client'` for event listeners, browser APIs, hooks, or lifecycle effects.

**Push client boundaries to leaves**: Keep root and trunk as server components. Use the children pattern to wrap server content in client wrappers without pulling the tree client-side.

**Eliminate waterfalls**: Parallel `await` with `Promise.all()` in server components. Each `Suspense` boundary is an independent streaming unit — granular boundaries enable progressive rendering.

**Four-layer cache model**:
| Layer | Scope | Use Case |
|---|---|---|
| Request memoization | Single request | `cache()` from React |
| Process memory | Worker lifetime | Risky in serverless — avoid |
| Shared cache (Redis) | Cross-request | Tag-based invalidation |
| CDN cache | Global | Public/personalized split |

**Partial Prerendering (PPR)**: Serves a static shell from edge cache at T=0, streams dynamic content. Drops TTFB from ~400ms to ~40ms.

### When NOT to Use

| Scenario | Better Approach |
|---|---|
| Real-time dashboards | Client components (WebSocket) |
| Rich text editors | Client components (browser APIs) |
| Offline-first apps | Client-driven architecture |
| Highly interactive collaborative tools | Client-first with targeted server islands |

### Recommendation for Thai-Market SaaS Team

**Adopt Next.js App Router as the default stack**. The mental model shift (server-first, explicit client boundaries) delivers real performance wins that benefit users on mobile networks in Thailand. Start with 1-2 static routes, then expand. Do NOT flip the switch globally.

### Key Resources
- react.dev — RSC docs (React 19+)
- nextjs.org/docs/app — App Router docs
- DebugBear RSC guide (debugbear.com/blog/react-server-components)

---

## 2. Streaming SSR & Partial Hydration

### Framework Comparison

| Dimension | Next.js App Router | Remix (React Router v7) | Astro |
|---|---|---|---|
| Default model | SSR + RSC | SSR-first, progressive enhancement | Static HTML, zero JS default |
| Streaming | Native via Suspense | Supported, less emphasized | Server Islands (Astro 5) |
| Partial hydration | RSC + `'use client'` | Selective hydration | Islands (per-component independent) |
| Default JS to client | Only client components | SSR + hydration | **Zero** — islands opt in |
| Runtime overhead | React runtime ~45KB | React runtime ~45KB | Per-island framework only |
| Best for | Full-stack apps | Form-heavy, data-driven apps | Content sites, docs, marketing |

### How Streaming Differs

**Next.js**: HTML chunks sent per Suspense boundary. Static shell first, async components stream in. PPR (Next 16) allows build-time prerendered shells served from CDN with dynamic regions streaming from origin.

**Remix**: Co-located route loaders (`loader`/`action`). HTML forms work without JS — progressive degradation graceful by default. Streaming exists but is not the flagship feature.

**Astro**: Static HTML by default. Server Islands add request-time dynamic regions streamed into an otherwise static page. Fundamentally different — most of the page hits CDN, only dynamic islands stream.

### When to Choose Which

| Scenario | Recommended | Why |
|---|---|---|
| Content-heavy (docs, blogs, marketing) | **Astro** | Zero JS default, best CWV out of box |
| Full-stack SaaS app (auth, dashboard) | **Next.js App Router** | One framework handles both; largest ecosystem |
| Form-heavy mutation app (admin panels) | **Remix** | Loader/action clarity, progressive enhancement |
| SEO-critical + dynamic personalization | **Next.js or Remix** | Both SSR well; Next.js more hybrid patterns |
| Marketing site + few interactive widgets | **Astro with embedded islands** | Static shell + isolated React/Vue/Svelte |

### Recommendation for Thai-Market SaaS Team

**Default to Next.js App Router** for the main SaaS product. Use **Astro** for marketing site, landing pages, and content. This split gives you RSC performance for app features and zero-JS marketing pages.

### Key Resources
- nextjs.org/docs/app/guides/streaming
- astro.build/docs/server-islands
- Sujeet Jaiswal — Modern Rendering Architectures (sujeet.pro)

---

## 3. Islands Architecture

### The Core Idea

Invert the SPA model: ship **static HTML by default**, only interactive "islands" opt in to client-side JS. Popularized by Astro, Qwik, Fresh, and Marko.

### Astro vs Qwik

| Aspect | Astro | Qwik |
|---|---|---|
| Default JS | **Zero** — unless island opts in | ~1KB (Qwikloader), lazy-fetch |
| Mechanism | Partial hydration | **Resumability** — never re-executes server logic |
| Framework support | Multi-framework (React, Vue, Svelte, Solid) | Single (Qwik — Preact-like) |
| State between islands | Harder — events, server, or shared bus | Built-in via serialized closures |
| Ecosystem | Very mature, large plugin ecosystem | Smaller, fewer integrations |

### When to Use Islands

**Best for Astro**:
- Content-driven sites — zero JS by default = best CWV
- Multi-framework teams — mix React, Vue, Svelte in one project
- Progressive enhancement — add interactivity only where needed

**Best for Qwik**:
- Mobile-first, latency-bound apps — eliminates hydration
- Many interactive elements, low per-user interaction frequency
- Edge-first architectures — state serialized into HTML

### Trade-offs

**Astro islands**:
- State sharing across islands is hard (no shared runtime context)
- Each island ships its own framework runtime
- Not for app-like UIs where every component affects every other

**Qwik**:
- Smaller ecosystem, fewer UI libraries
- Developers must learn `$` suffix conventions, `useLexicalScope()`
- First interaction on cold mobile still requires network fetch for handler

### Decision Framework

Every page region sits on 3 axes:
1. **Where rendered** — build (SSG), request (SSR), client (CSR)
2. **What ships** — nothing, serialized state, framework runtime
3. **When interactive** — never, on load, on idle, on visible, on interaction

### Recommendation for Thai-Market SaaS Team

**Use Astro for marketing/content pages**. The zero-JS default directly benefits Thai users on mid-range phones and slower connections. For the main SaaS app, Next.js RSC is a better fit. Do not use islands architecture for highly interactive dashboards — the state-sharing cost compounds.

### Key Resources
- docs.astro.build/en/concepts/islands
- qwik.dev/docs
- Addy Osmani — Islands Architecture (original 2019 post)

---

## 4. Signals & State Management

### The Signals Revolution

Signals have become the **dominant reactivity pattern** across frameworks. SolidJS, Angular, Preact, Vue, Svelte, Qwik, and Ember all have signal-based systems. TC39 is pursuing a native JS Signals proposal.

### TC39 Signals Proposal

- **Status**: Working toward Stage 2 (early 2026)
- **Goal**: Standard reactive primitive in JavaScript — framework-agnostic, engine-optimizable
- **API shape**:
  ```js
  const count = new Signal.State(0);
  const doubled = new Signal.Computed(() => count.get() * 2);
  count.set(5);
  console.log(doubled.get()); // 10
  ```
- **Scope limits**: Standardizes reactive graph (State + Computed) but NOT rendering, effects, or scheduling
- **Polyfill**: `signal-polyfill` on npm

### Framework Comparison

| Aspect | SolidJS | Angular | Preact Signals |
|---|---|---|---|
| Model | Push (sync, topological) | Pull (lazy, microtask-batched) | Hybrid (direct + VDOM) |
| Update timing | Synchronous | Microtask batch | Mixed |
| Glitch-free | Topological sort | Pull-based + lazy eval | Version-number comparison |
| Standalone | Yes (14KB) | Yes (22KB, includes zone) | Yes (3KB core) |

### Benchmarks (1,200-node dashboard, 10k updates/sec)

| Implementation | Render time | Memory | Bundle |
|---|---|---|---|
| Plain React useState | 180ms | ~40MB | baseline |
| @preact/signals-react | 18ms | 29MB | +4KB |
| @preact/signals-core (vanilla) | **12ms** | **18MB** | **3KB** |
| MobX | ~15ms | 42MB | +17KB |
| RxJS | ~20ms | 47MB | 47KB |

### 2026 Landscape: Three Coexisting Patterns

| Pattern | Best for | Example |
|---|---|---|
| **Signals** | High-frequency updates, real-time data, fine-grained reactivity | @preact/signals-core, Solid, Angular |
| **Stores** | Complex business logic, time-travel debugging | Zustand, Pinia, Redux Toolkit |
| **Atoms** | Component-level state, derived values | Jotai, Recoil |

Emerging best practice: **use all three together** — signals for real-time data, stores for business logic, atoms for UI state.

### What's Replacing Redux/Zustand?

Redux and Zustand aren't dead, but their role is shrinking. For most state needs in 2026:
- **Signals** handle fine-grained reactivity (real-time dashboards, form fields, collaborative editing)
- **Zustand** stays relevant for complex cross-cutting business logic
- **Redux Toolkit** persists for legacy codebases and teams that need DevTools/time-travel debugging
- **New projects default to signals** for local state, stores for shared business logic

### Recommendation for Thai-Market SaaS Team

**If using React**: Keep Zustand for shared business logic state. Add `@preact/signals-react` for high-frequency updates (real-time monitoring, form reactivity). Do NOT port everything to signals overnight — introduce incrementally where the render performance matters.

**If evaluating SolidJS or Angular**: Signals are native — no extra library needed.

**Long-term**: Watch TC39 Signals progress. Native signals in JS would eliminate framework lock-in for state.

### Key Resources
- TC39 Signals proposal repo (github.com/tc39/proposal-signals)
- signal-polyfill (npm)
- Preact Signals docs (preactjs.com/guide/v10/signals)
- SolidJS reactivity docs (solidjs.com/guides/reactivity)

---

## 5. Edge & Distributed Rendering

### Production Readiness: MATURE for auth/routing, EVOLVING for full UI rendering

Edge computing for UI has settled into clear patterns in 2026. Edge functions (V8 isolates, Deno) run at CDN edge nodes instead of centralized servers.

### Latency Impact

| Approach | Typical RTT |
|---|---|
| Traditional centralized SSR | 150-200ms (Singapore to Virginia) |
| Serverless (regional) | 50-100ms |
| **Edge rendering** | **10-50ms** (global CDN nodes) |

Even 100ms delay measurably affects conversion rates. For Thai users connecting to US-based servers, edge rendering can cut TTFB from ~450ms to under 150ms.

### What Edge Functions Are Good For

| Use Case | Suitability |
|---|---|
| Auth token validation | Excellent |
| Geo-routing / locale detection | Excellent |
| A/B testing assignment | Excellent |
| Lightweight SSR shells | Good |
| Cache key generation | Good |
| Heavy computation / DB queries | **Poor** — keep on origin |
| Long-running tasks | **Poor** — execution limits |

### Platform Comparison (2026)

| Platform | Runtime | Cold Start | Execution Limit | Bundle Limit |
|---|---|---|---|---|
| Cloudflare Workers | V8 isolates | <5ms | 30s CPU | 5MB |
| Vercel Edge Functions | V8 isolates | <5ms | 25s | 4MB |
| Netlify Edge Functions | Deno | <5ms | **50ms** | — |
| Deno Deploy | Deno | <5ms | — | — |

**Netlify's 50ms limit** is a hard constraint — only suitable for the most lightweight operations.

### Emerging 2026 Patterns

1. **API Gateway at Edge**: Auth, rate limiting, A/B routing at edge; delegate compute to microservices
2. **Predictive edge rendering** (MIT research): Pre-render likely next pages at edge nodes — click latency near zero
3. **Edge-Adaptive UI** (Carnegie Mellon): Dynamically adjust rendering strategy based on device, network, and interaction patterns
4. **Edge-Intermediate Representation** (Microsoft): Compile UI code to device-independent IR; final render at edge — reduces cross-device perf variance by 76%

### Recommendation for Thai-Market SaaS Team

**Deploy edge functions for auth, geo-routing, and lightweight personalization** only. Do NOT move database access or heavy compute to edge. Use Cloudflare Workers or Vercel Edge Functions — both are mature. The primary benefit for Thai users is reduced latency to edge nodes in Southeast Asia (Singapore, Tokyo, Mumbai).

### Key Resources
- Cloudflare Workers docs (developers.cloudflare.com/workers)
- Vercel Edge Functions docs (vercel.com/docs/functions/edge-functions)
- Feature-Sliced Design blog on edge rendering (feature-sliced.design)

---

## 6. AI-Driven UI Patterns

### Production Readiness: RAPIDLY EVOLVING — use in production with guardrails

AI-driven UI in 2026 has moved beyond "chat in a corner" to **generative UI** — AI generates and streams interactive components as part of the user experience.

### Core Patterns

#### 1. Streamable UI (`streamUI`)

The dominant pattern from Vercel AI SDK. Instead of streaming raw text, the server streams serialized **React Server Components** over SSE. The client hydrates them immediately — charts, forms, and dashboards render while the AI is still generating.

**Architecture**: Server → Client streams React Flight payload; Client → Server triggers Server Actions for bidirectional interactivity.

**Guardrails**: Use LangGraph max iteration policies to prevent infinite loops.

#### 2. Registry / Component Library Pattern

1. Define a registry — map component names to Zod schemas + render functions
2. Convert to AI SDK tools — turn registry into tool definitions the LLM can call
3. Render validated components — client validates args at runtime and renders matching component

Decouples "what the LLM decides" from "what renders" — prevents hallucinations from crashing the UI.

#### 3. Display-Only vs Round-Trip Components

- **Display-only** (weather, chart, code block): LLM picks args, component renders, done
- **Round-trip** (Confirm, ChooseOne, form): LLM pauses after rendering; user interacts via `ctx.respond(answer)` — answer sent back as tool result — LLM continues

This is the foundation for copilot-style approval flows and multi-step agent interactions.

#### 4. UX Middleware (2026 Evolution)

A critique from 2026: "Why does your AI product still look like a chatbot?" The argument is that LLMs asked to handle both reasoning and UI generation suffer from context pollution. The solution is a **deterministic orchestration layer** (UX Middleware) that decouples intent from interface — LLM focuses on data, middleware handles component selection.

### Key Libraries (2026)

| Library | Purpose | Key Feature |
|---|---|---|
| **Vercel AI SDK** (`ai`) | Core streaming, tool calling, `streamUI` | RSC streaming, server actions |
| **assistant-ui** | Production chat primitives | Composable Thread, Message, Composer |
| **streamfield** | Partial-object reveal | Field-by-field diff + animation |
| **gen-ui-chat** | Headless generative UI | Registry -> AI SDK tools pattern |
| **dynamic-ui-mcp** | MCP + direct library | Built-in charts/forms/wizards |
| **@react-native-ai/json-ui** | Mobile generative UI | Tool-calling over streaming |
| **BranderUX** | UX Middleware (2026) | Decouples LLM reasoning from UI |

### Common Pitfalls

- **Prompt fragility**: LLMs handling both reasoning and UI generation suffer context pollution
- **Infinite loops**: Always set max iteration boundaries on AI tool loops
- **Hallucination in UI**: Validate component args with Zod/schemas before rendering
- **State leakage**: Clear separation between AI session state and application state

### Recommendation for Thai-Market SaaS Team

**Start with the Vercel AI SDK + registry pattern** for targeted AI features (customer support copilot, AI-assisted form filling, smart search). Do not try to AI-generate the entire UI. Focus on discrete, high-value enhancements:

- AI chat for customer support (pre-built components for common queries)
- AI-assisted data filtering and report generation
- Smart form auto-completion from natural language input

**Avoid**: Fully generative dashboards, AI-controlled navigation, or autonomous UI layout for now — the UX middleware pattern is still maturing.

### Key Resources
- sdk.vercel.ai/docs — Vercel AI SDK
- Manning — Build AI-Enhanced Web Apps (livebook.manning.com)
- assistant-ui docs (assistant-ui.com)
- "It's 2026. Why Does Your AI Product Still Look Like a Chatbot?" (generativeai.pub)

---

## 7. Performance as UX

### Core Web Vitals in 2026

The biggest change: **INP (Interaction to Next Paint) has fully replaced FID** since March 2024.

| Rating | INP |
|---|---|
| Good | <= 200ms |
| Needs Improvement | 200ms - 500ms |
| Poor | > 500ms |

**Impact**: ~43% of sites that passed FID now fail INP. Pass rates dropped from ~93% (FID) to ~65% (INP).

### INP: Why It's Harder

- FID measured only input delay of the first interaction
- INP measures the **full interaction lifecycle** (input delay + processing + presentation) for **every** interaction
- Reports the **worst** interaction (98th percentile for pages with 50+ interactions)

### Practical Priority Order

1. **Fix INP first** — hardest to pass, requires JS architecture changes
2. **Optimize LCP** — hero image, server response time
3. **Fix CLS** — dimensions on all media, font-display

### Key Optimization Techniques

**For INP**:
```
// Yield to main thread pattern
async function handleInteraction(action) {
  setVisualState(action);       // paint feedback immediately
  await yieldToMain();          // yield to browser
  const result = await processData(action);
  setResults(result);
}

function yieldToMain() {
  if ('scheduler' in window && 'yield' in window.scheduler) {
    return window.scheduler.yield();
  }
  return new Promise(resolve => setTimeout(resolve, 0));
}
```

- Use `useDeferredValue` / `startTransition` in React
- Offload analytics and heavy computation to Web Workers
- Code splitting + defer third-party scripts

**For LCP**:
- Modern formats: AVIF (50% smaller than JPEG) + WebP fallback
- `fetchpriority="high"` on hero image
- Never lazy-load the LCP image
- Preload LCP resource: `<link rel="preload" as="image" href="/hero.avif">`
- `font-display: swap` for custom fonts
- CDN with edge caching

**For CLS**:
- Explicit `width`/`height` on all images
- `aspect-ratio` in CSS
- Reserve space for ads/dynamic content
- `font-display: swap` eliminates FOIT/CLS from fonts

### Streaming Patterns for Performance

Streaming SSR directly improves perceived performance:
- Static shell arrives immediately (nav, sidebar, fallbacks)
- Dynamic content arrives progressively
- PPR (Next.js) serves static shell from CDN at T=0

**Real-world data**: Removing 5-10 unnecessary third-party scripts often improves INP more than any advanced optimization. Fixing hero image + server response improves LCP by 30-50%.

### Tools

| Tool | Purpose |
|---|---|
| Chrome UX Report (CrUX) | Real-user field data (what Google ranks on) |
| PageSpeed Insights | Combines lab + field data |
| Chrome DevTools Performance | Debug INP interactively |
| web-vitals JS library | Custom RUM collection |
| Lighthouse / WebPageTest | Lab data for debugging |

### Recommendation for Thai-Market SaaS Team

**Invest in INP before anything else**. Thai users on mid-range Android phones over LTE are exactly the demographic where INP matters most. Key actions:

1. Audit and remove unnecessary third-party scripts (chat widgets, analytics, ads)
2. Implement yield-to-main pattern for all interaction handlers
3. Move heavy computation to Web Workers
4. Defer non-critical JS (intersection observer-based loading)
5. Use Next.js `<Image>` with `priority` for hero images

This is higher impact than any framework choice.

### Key Resources
- web.dev/articles/inp — INP explainer
- web.dev/articles/vitals — Core Web Vitals
- Chrome DevTools Performance panel
- web-vitals library (npm)

---

## 8. Cross-Platform Convergence

### The 2026 Landscape

Five major contenders: **React Native + Expo**, **Flutter**, **Compose Multiplatform (KMP)**, **Tauri 2 Mobile**, and newcomer **Lynx** (ByteDance, open-sourced March 2025). React Native and Flutter dominate mobile with ~70% combined professional adoption.

### Comparison Table

| Criterion | React Native + Expo | Flutter | Tauri 2 Mobile |
|---|---|---|---|
| Language | TypeScript/JS | Dart | Rust + Web frontend |
| Rendering | Native components (Fabric) | Self-rendered (Impeller) | System WebView |
| Startup | ~600-700ms | ~400-600ms | ~100-150ms (desktop) |
| Memory | ~145-160MB | ~125-145MB | ~30-45MB |
| App size (empty) | 13-15MB | 14-17MB | 6-8MB |
| Animation perf | Good (55-58 FPS) | Excellent (60+ FPS) | Moderate |
| Desktop support | Moderate | Strong | Strong |
| Mobile maturity | Very mature | Very mature | Beta/stable since 2024 |
| Ecosystem size | Largest (npm) | Very large (pub.dev) | Growing |
| OTA updates | Built-in (EAS) | Third-party | Limited |
| Learning curve | Low (JS/React) | Medium (Dart) | Medium-high (Rust) |
| UI consistency | Good (native per platform) | Excellent (pixel-perfect) | Moderate (WebView) |

### React Native + Expo (Default Choice for Web Teams)

**What changed in 2026**:
- New Architecture default since RN 0.76 — Fabric renderer + TurboModules + JSI
- Expo is the de facto standard — SDK 53, Expo Router 4, EAS Build, EAS Update (OTA)
- Hermes engine default — AOT bytecode, <200ms cold start
- RN 1.0 slated for late 2026

**Best for**:
- Web-background teams (JS/React ecosystem)
- Content-driven apps (e-commerce, news, social)
- Fast iteration with OTA updates
- Native feel (uses platform UI components)

### Flutter (Visual Consistency Champion)

**What changed in 2026**:
- Impeller renderer default on all platforms — no more Skia shader compilation jank
- Material You 3 full support with dynamic color
- Multi-platform: mobile + desktop + web + embedded from one codebase

**Best for**:
- Pixel-perfect consistency across platforms
- Smooth 60/120fps animations
- Brand-led visual-heavy apps
- Mobile + desktop + web from one codebase

### Tauri 2 Mobile (The Lightweight Contender)

**What changed in 2026**:
- Tauri 2.0 (Oct 2024) — official iOS and Android support
- 6-8MB bundles (vs Electron's 150MB+)
- Rust backend + system WebView frontend

**Best for**:
- Desktop-first tools with mobile companion
- Security-critical apps (Rust memory safety, permission model)
- Teams comfortable with Rust

### The Lynx Wildcard (ByteDance)

- Open-sourced March 2025
- Web-first rendering (CSS + Flexbox layout on threads)
- Built for the Douyin ecosystem — may gain traction in Asia
- Early stage — not production-recommended for 2026

### Trends Shaping 2026

- **Multi-surface deployment** is the new default (mobile + desktop + web from one codebase)
- **On-device AI** (Apple Intelligence, Gemini Nano) reshaping mobile capabilities
- **Tauri displacing Electron** for new desktop builds (3x YoY npm growth)
- **AI tooling** (Cursor, Copilot, Claude Code) reducing build times 30-50%

### Recommendation for Thai-Market SaaS Team

**Default to React Native + Expo** for mobile. Reasons:

1. Your team likely knows JS/React already — lowest learning curve
2. OTA updates via EAS — ship fixes without App Store review (critical for fast-moving SaaS)
3. Large talent pool in Thailand (React devs are abundant)
4. Expo handles 80% of build complexity (certificates, builds, routing)

**Use Flutter** only if animation performance or pixel-perfect brand consistency is a non-negotiable requirement.

**Do NOT use Tauri for mobile** in 2026 for a Thai-market consumer app — ecosystem and plugin maturity aren't there. Tauri is excellent for desktop tools internally.

### Key Resources
- reactnative.dev — React Native docs
- docs.expo.dev — Expo docs
- flutter.dev — Flutter docs
- v2.tauri.app — Tauri 2 docs
- youngju.dev — cross-platform deep dives (2026)

---

## Summary: Architecture Decisions for a Thai-Market SaaS Team

| Layer | Recommendation | Rationale |
|---|---|---|
| **Main web app** | Next.js App Router (RSC) | Server-first, streaming, largest ecosystem |
| **Marketing site** | Astro | Zero JS default, best CWV, multi-framework islands |
| **Mobile app** | React Native + Expo | JS/React familiarity, OTA updates, talent availability |
| **State management** | Zustand (shared logic) + @preact/signals-core (high-freq updates) | Incremental signals adoption, no rewrite |
| **Edge compute** | Cloudflare Workers or Vercel Edge Functions | Auth, geo-routing, lightweight SSR only |
| **AI features** | Vercel AI SDK + registry pattern | Targeted copilot/smart form features, not full generative UI |
| **Performance focus** | INP first (yield-to-main, web workers, third-party script audit) | Thai users on mid-range Android + LTE |
| **Desktop (internal tools)** | Tauri | Tiny bundles, Rust security |

### Decisions to Make

1. **Next.js vs Remix for main app**: Next.js wins for ecosystem size and RSC maturity. Revisit only if your app is form-heavy with complex mutations — Remix's loader/action model may serve better there.

2. **React vs Solid for new components**: If starting greenfield, evaluate SolidJS for its signal-native reactivity and smaller bundles. For existing React codebases, stay with React RSC.

3. **Mobile-first or responsive web**: For Thai market where mid-range Android dominates, consider building the mobile experience first. Expo + Next.js share the React ecosystem — components can be shared.

4. **AI investment level**: Do NOT build a fully generative UI in 2026. Invest in targeted copilot features with strict guardrails. The UX middleware pattern needs another year to mature.

5. **Performance budget**: Set a hard limit of <200ms INP and <2.5s LCP on 3G. Test on mid-range Android devices (not just your dev machine). This is the single highest-impact decision for user retention in emerging markets.

---

> *Research compiled July 2026. Sources linked inline. Revisit this document quarterly — the UI architecture landscape is evolving fast.*
