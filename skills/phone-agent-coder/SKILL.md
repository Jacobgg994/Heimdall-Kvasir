---
name: phone-agent-coder
description: "Turn the Boxphone fleet into a distributed pool of headless coding agents. Termux + Claude Agent SDK + git on each phone, orchestrated from 210.1.1.155. Use when planning a phone-side compute layer, evaluating Claude Code / Aider on ARM Android, or designing distributed agent workflows that need diverse residential IPs."
risk: medium
source: contentsdigital
date_added: "2026-05-21"
---

# Phones as real coding agents

Can a Samsung Note 8 or S7 actually run an AI coding agent in production? **Yes — with caveats.** This skill documents the working architecture, the hard limits, and the actual procedures.

## TL;DR — the answer

**Yes**, our Note 8 / S7 fleet (Android 9, no phantom-process limit) can each run a headless Claude-API-driven coding agent under Termux. **No**, the official Claude Code CLI isn't sold as a Termux build, but the underlying engine — Node 18+ + Anthropic SDK — runs natively. The realistic deployment is: **server-side orchestrator + phone-side focused subagents**, not "60 phones each writing huge codebases independently."

## Hard feasibility data

| Fact | Source | Implication |
|---|---|---|
| Termux supports apt, bash, Node.js, Python, Go, Rust, C, OpenSSH, curl, rsync | termux.dev | Full Linux runtime — no compromises on tooling |
| Termux runs unmodified on Android 7+ without root | termux-app GitHub | Our fleet (Android 9 on N950F/N, G930F) is fully compatible |
| Android 12+ caps phantom processes at 32 system-wide | termux-app GitHub | Newer phones (A155F, A366B on Android 16) are *bad* for this — Android 9 fleet is *better* |
| Claude Code requires Node 18+, official installer targets macOS/Linux/WSL/Windows | code.claude.com/docs | No native Termux install, but Linux install procedures work in Termux's Debian-like env |
| Claude Code is open source at `github.com/anthropics/claude-code` (125k stars) | GitHub README | Can install from source on any platform Node 18+ runs |
| `npm install -g @anthropic-ai/claude-code` (marked deprecated but still works) | GitHub README | One-line install on Termux |
| Anthropic Agent SDK exposes the same engine programmatically | docs.anthropic.com | Build a custom phone-side runtime instead of the heavy CLI |

## What each phone can realistically do

| Hardware | RAM | What it's good at | What it's NOT good at |
|---|---|---|---|
| Note 8 (N950F/N) Android 9 | 6 GB | Running Claude Agent SDK loop on a single repo, web automation via Playwright/Appium, calling Claude API with project context | Compiling Rust / Go / C++ heavy projects, holding multiple repos > 2 GB total |
| S7 (G930F) Android 9 (rooted) | 4 GB | Same as above but slower; best as engagement/web-automation node | Anything with > 1 GB working set in Node |
| A15 / A16 5G (when bought) | 6–8 GB | Same as Note 8 with newer Android — *but* watch the 32-phantom-process limit on Android 14+ | Long-running multi-process pipelines on Android 14+ |

**Per-phone working budget:** ~1 active Node process, ~1.5 GB heap, ~50–100 MB/min API egress on a busy session.

## The three realistic deployment models

### Model A — Server-orchestrator + phone subagents (RECOMMENDED)

```
┌─────────────────────────────────────┐
│ 210.1.1.155 (Ubuntu, ~80 GB RAM)    │
│                                     │
│  Orchestrator (Node.js)             │
│    ├─ Task queue (Postgres)         │
│    ├─ Routing logic                 │
│    └─ Result aggregation            │
│                                     │
└──────────┬──────────────────────────┘
           │ SSH + gemphonefarm script API
   ┌───────┴────────┬─────────┬────────┐
   ▼                ▼         ▼        ▼
 ┌───┐            ┌───┐    ┌───┐    ┌───┐
 │N8 │  agent A   │N8 │ B  │S7 │ C  │A15│ D
 │SDK│ ──Claude──▶│SDK│    │SDK│    │SDK│
 └───┘            └───┘    └───┘    └───┘
```

Each phone runs a focused agent SDK loop on **one task** at a time. Orchestrator dispatches, collects results, retries on failure. Phones never coordinate directly.

**Best use cases:**
- 60 parallel "review this PR" agents — each reads a different repo
- 40 "scrape this URL + draft a TikTok script + push to queue" pipelines
- 30 "test this affiliate landing page from a different IP" agents
- 20 "monitor this competitor's price and post if it drops" loops

**Cost shape:** API spend is the dominant cost; phone cost is amortized. Run 200 agent-hours/day across the fleet for ~฿1,500–3,000/day in tokens (Claude Haiku for cheap tasks, Sonnet for complex).

### Model B — Phones as edge IP / web-automation, server runs Claude

The phone does NOT run the LLM agent. Instead:
- Server (210.1.1.155) runs Claude Code / Agent SDK
- When the agent needs to "see" a Thai site behind geo-blocks, it dispatches a Playwright-on-Termux job to a TH-grouped phone
- Phone returns screenshots / HTML / cookie state
- Agent continues reasoning on the server

**Why this is often the right choice:** keeps the heavy thinking on a 16-core server (fast iteration), uses phones for what only phones do well (real device fingerprints + residential IP egress).

### Model C — Phone as standalone agent, no server

A single Note 8 with Termux + Claude Code, used by a developer in the field as their primary dev box. **Works, but masochistic.** Screen is small, keyboard is touch. Better with a Bluetooth keyboard + HDMI dock. Realistic only as a backup workflow or for SSH terminal control.

## Installation — Termux + Claude Agent SDK (Model A)

This is the per-phone setup. Run once per device. ~25 minutes per phone.

### Step 1 — install Termux

Download Termux **from F-Droid** (Play Store version is abandoned). The APK directly:

```
https://f-droid.org/repo/com.termux_1020.apk     # or latest at f-droid.org
```

Sideload to the phone via adb:

```bash
adb -s <device_id> install termux-1020.apk
```

### Step 2 — bootstrap Termux

Open Termux on the phone (you can also do this via adb shell after Termux is launched once). Inside Termux:

```bash
pkg update && pkg upgrade -y
pkg install -y nodejs git openssh curl which python build-essential
termux-setup-storage          # grant storage access — useful for repos under ~/storage/shared
```

### Step 3 — pick your agent runtime

**Option A1 — official Claude Code CLI (heavier, more features):**

```bash
# The deprecated npm route still works on Termux because we're effectively Debian Linux
npm install -g @anthropic-ai/claude-code

# Verify
claude --version
```

**Option A2 — lightweight custom agent (recommended for fleet):**

```bash
mkdir -p ~/agent && cd ~/agent
npm init -y
npm install @anthropic-ai/sdk dotenv yargs
```

Then drop in a small Node script that polls a task queue and dispatches each task to Claude. See `templates/agent-runner.js` in this skill.

### Step 4 — auth

Each phone needs an API key. Provision per-phone keys from Anthropic Console with per-key spend caps (e.g. $5/day) so a runaway phone can't blow your budget.

```bash
echo 'ANTHROPIC_API_KEY=sk-ant-...' >> ~/agent/.env
chmod 600 ~/agent/.env
```

### Step 5 — sshd for orchestrator control

```bash
pkg install -y openssh
sshd                  # start sshd
passwd                # set a password for the orchestrator to use
# Or better: drop the orchestrator's public key into ~/.ssh/authorized_keys
```

Phones expose sshd on port 8022 by default. Orchestrator SSHes in to start/stop the agent runtime.

### Step 6 — keep Termux awake

Termux has a wakelock helper to keep the runtime alive:

```bash
termux-wake-lock          # call this in the agent's startup script
```

Also disable battery optimization for Termux in Android Settings → Battery → never sleep.

## Phantom-process gotcha (Android 12+)

If you ever use a phone on Android 12+, set Developer Options → "Disable child process restrictions". Without this, Android kills processes whenever the global count exceeds 32 *across all apps*. Termux + sshd + Node child processes will hit this immediately.

Our Note 8 / S7 fleet on Android 9 is unaffected. Worth knowing before buying A15s.

## Cost-per-task math

A focused agent task ("write a blog post, generate 5 image prompts, draft 3 TikTok scripts") averages:

| Provider | Approx. cost per task | Per phone per day at 8 tasks/hr × 12 hr | Fleet of 60 at the same rate |
|---|---|---|---|
| Claude Haiku 4.5 | $0.02–$0.05 | $2–$5 | $120–$300 |
| Claude Sonnet 4.6 | $0.10–$0.25 | $10–$24 | $600–$1,440 |
| Gemini 2.5 Flash | $0.005–$0.015 | $0.5–$1.5 | $30–$90 |
| QCCAP OS (your platform) | $0 | $0 | $0 |

For the Thai content + affiliate workload, Haiku and Gemini Flash cover ~80%; Sonnet for hero strategy/edits. **Fleet-wide compute cost: ~฿4–10k/day at full burn**, against an expected MRR target of ฿1M+. The ratio works.

## Real use cases on our fleet

| Use case | Suitable model | Per-phone task count / day | Why it shines on phones |
|---|---|---|---|
| Per-product TikTok script + caption + hashtags | Haiku | 100+ | Phones double as the eventual posting device — same context |
| Daily Shopee competitor price + review scrape, return diff | Haiku | 50+ | Phones have real residential IPs; reviewing competitor sees the Thai-localized site |
| Per-client CDS blog draft, image-prompt list, social variants | Sonnet | 20 | Stateful context per client kept on that client's dedicated phone |
| Real-mobile UX test of a landing page (Playwright on Termux) | Haiku | 30 | Tests the real Android Chrome experience, not a desktop emulator |
| Code-review subagent for a small repo (≤ 5k LoC) | Sonnet | 5–10 | Cheap parallelism — 60 reviewers in 5 minutes |
| Generate + commit a daily affiliate-links update JSON | Haiku | 1 | Per-phone provenance; the same phone that posts knows what changed |

## Use cases where the phone is NOT the right tool

- Compiling a Next.js production build → use server
- Multi-file refactors across a > 100k LoC repo → use server (slow IO + RAM constrained)
- Anything that needs > 4 GB RAM → use server
- Long-running daemons that span > 24 hr → memory leaks compound on phones
- iOS development → no Xcode, full stop

## Orchestrator design (server-side)

Postgres `agent_tasks` table:

| Column | Purpose |
|---|---|
| `id` | uuid |
| `phone_id` | which phone gets it (null = any) |
| `kind` | `tiktok_script` / `shopee_scrape` / `code_review` / etc. |
| `prompt` | the user-message body |
| `context` | JSON: files, urls, prior tool outputs |
| `model` | `haiku-4-5` / `sonnet-4-6` / `gemini-2.5-flash` |
| `status` | queued / running / done / failed |
| `result` | JSON: model response + token usage |
| `attempts` | int |
| `created_at`, `finished_at` | timestamps |

Phone-side runner: polls `agent_tasks WHERE phone_id=$me AND status='queued' LIMIT 1`, marks running, calls the model, writes result.

Orchestrator: writes new tasks (from cron, webhooks, or our existing CMS events), watches `status='failed'`, retries up to 3×.

## Risk register

| Risk | Mitigation |
|---|---|
| Phone overheats during sustained work | Charge through powered USB hub with thermal pads; throttle to 12 hr/day, not 24 |
| One phone leaks API key | Per-phone keys with $5/day caps; rotate weekly |
| Anthropic rate-limits the fleet IP | Use per-phone egress (one IPv6 /64 per phone) so each looks like a distinct customer |
| Termux update breaks the runtime | Pin all package versions; rebuild Termux image once per quarter |
| Phone dies mid-task | Orchestrator retry; tasks must be idempotent |
| `npm install` route gets fully blocked by Anthropic | Switch to Agent SDK from npm directly — different package, same API |
| Android 12+ kills processes | Use Android 9 fleet only; flag any Android ≥12 phone as engagement-only |

## When to use this skill

- User asks "can phones write code?" or "Claude Code on phone?"
- Designing the agent orchestrator on 210.1.1.155
- Cost-per-task math for fleet-side AI compute
- Choosing model routing (Haiku vs Sonnet vs Gemini per task class)
- Diagnosing phantom-process kills on newer Android devices

## Files in this skill

| File | Contents |
|---|---|
| `templates/agent-runner.js` | Minimal Node.js + Anthropic SDK runner that polls a Postgres task queue (copy-paste-ready) |
| `templates/setup-termux.sh` | Step-by-step installer to flash + bootstrap a phone from zero |
| `reference/cost-routing.md` | Which provider / model for which task class |
| `sops/phone-as-coder-onboarding.md` | Per-phone activation procedure (25 min/phone) |
