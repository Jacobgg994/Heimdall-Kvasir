---
name: boxphone-thai-growth
description: "Operate the 60+ device Boxphone (gemphonefarm) farm for Thai-market growth: TikTok Shop / Shopee / Lazada affiliate at scale, LINE OA setups, and the contentsdigital.us CDS retainer engine. Includes the 90-day plan, Thai viral hook library, affiliate stack integration, and SOPs. Invoke when working on Thai market revenue, phone farm orchestration, affiliate operations, or CDS client work."
risk: low
source: contentsdigital
date_added: "2026-05-21"
---

# Boxphone Thai Growth Operations

Reusable playbook + tooling for running the Thai-market growth operation across the 60-device Boxphone farm, the contentsdigital.us writer/CMS stack, and the multi-platform affiliate system. Use this skill any time you're working on:

- Phone farm device management (`gemphonefarm` MCP tools)
- Thai TikTok Shop / Shopee / Lazada affiliate posting
- Contents Digital Service (CDS) client retainers
- LINE OA setups
- The 90-day execution plan
- Thai-language viral content patterns

## Available MCP tools (use these first)

| Tool | Purpose |
|---|---|
| `mcp__gemphonefarm__gemphonefarm_list_devices` | Returns all phones with status, model, proxy, group |
| `mcp__gemphonefarm__gemphonefarm_list_groups` | Returns TH / VN / US device groups |
| `mcp__gemphonefarm__gemphonefarm_devices_by_group` | Filter devices by group |
| `mcp__gemphonefarm__gemphonefarm_start_device` | Bring a phone online for automation |
| `mcp__gemphonefarm__gemphonefarm_close_device` | Stop a phone |
| `mcp__gemphonefarm__gemphonefarm_execute_script` | Run a local automation script on one phone |
| `mcp__gemphonefarm__gemphonefarm_cloud_start_automation` | Cloud-routed automation (works when local :1256 API is down) |
| `mcp__gemphonefarm__gemphonefarm_check_script_status` | Poll for script completion |
| `mcp__gemphonefarm__gemphonefarm_kill_script` | Cancel a running script |
| `mcp__gemphonefarm__gemphonefarm_create_group` / `assign_device_to_group` | Organise devices |

**Always call `gemphonefarm_list_devices` first** to confirm fleet state before issuing any automation commands. Treat any device with `status: "offline"` as unavailable until reboot/repair.

## The infrastructure we own

| Asset | Where | Purpose |
|---|---|---|
| Frontend + Backend monorepo | `~/Projects/ui-template/` | Next.js (frontend :3000) + Express/Prisma (backend :2442) |
| GitHub repo | `github.com/ContentsUS/ui-template` (private) | Source of truth |
| Backup (clean) | `~/Projects/ContentsTemplate/` (local) + `ccdev@210.1.1.155:~/backups/ContentsTemplate/` (remote) | Restore point |
| Production server | `210.1.1.155` | Ubuntu, ~80 GB RAM, ~900 GB disk, capacity for Redroid cluster + backend |
| Writer system | `/writer/posts`, `/writer/new` | AI-driven (multi-provider) markdown editor with SEO/AEO auto-gen |
| Headless CMS | `/dashboard/cms`, `/api/cms/*` | Site settings, pages, FAQs, services, pricing, jobs, team, testimonials |
| Webhook system | `/dashboard/webhooks`, `/api/admin/webhooks` | HMAC-signed event delivery on post.published / order.created / contact.received |
| Themes | 8 color presets, admin-only switcher | default, gold, darkblue, skyblue, darkgreen, matrix, greydark, cream |
| Demo admin login | `admin@example.com` / `password123` | For local dev only — rotate in production |

## The 5 revenue lines (ranked by speed-to-cash)

| # | Line | Day-1 readiness | Cash arrival | M3 MRR target |
|---|---|---|---|---|
| 1 | TikTok Shop affiliate (60 phones → 40 active accounts) | High | T+10 | ฿400k |
| 2 | Shopee + Lazada affiliate (same content, second commission stream) | High | T+45 (monthly) | ฿250k |
| 3 | CDS retainers (฿9.9k / ฿29.9k / ฿79.9k tiers) | High | T+14 | ฿300k |
| 4 | LINE OA setup + maintenance (฿20–40k + ฿5–8k/mo) | High | T+21 | ฿80k |
| 5 | Programmatic SEO + tourism affiliate (Klook / Agoda) | Medium | T+60 | ฿50k |

Full operating calendar: `reference/90-day-plan.md` in this skill folder.

## Common operations (copy-paste these)

### 1. Inventory the fleet

```
mcp__gemphonefarm__gemphonefarm_list_devices()
mcp__gemphonefarm__gemphonefarm_list_groups()
```

Confirm: ~60 devices, 3 groups (VN id 1, TH id 2, US id 3), expect 55+ online. Report status to user before suggesting actions.

### 2. Bring a phone online for a posting job

```
mcp__gemphonefarm__gemphonefarm_start_device(id=<device_id>)
# wait until status reflects online
mcp__gemphonefarm__gemphonefarm_execute_script(id=<device_id>, scriptId=<id>, params={...})
mcp__gemphonefarm__gemphonefarm_check_script_status(taskId=<returned id>)
mcp__gemphonefarm__gemphonefarm_close_device(id=<device_id>)
```

### 3. Cloud-route automation when local API is down

The local `:1256` API has been observed returning 404 on `list_scripts`. Fall back to cloud:

```
mcp__gemphonefarm__gemphonefarm_cloud_start_automation(
  workflow_id="<cloud workflow id>",
  device_id=<list of device ids>,
  parameter={...},
)
```

### 4. Generate Thai TikTok scripts (one Gemini batch, ~$0.02 for 200)

Use the backend AI endpoint we built:

```bash
TOKEN=$(curl -s -X POST http://localhost:2442/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@example.com","password":"password123"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')

# One batched call for all 200 scripts
curl -s -X POST http://localhost:2442/api/admin/ai/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"200 Thai TikTok affiliate scripts for category X, mixed hook patterns","style":"how-to","provider":"gemini"}' \
  > /tmp/thai-scripts.json
```

**Token discipline:** always batch (50–200 prompts in one call) and prefer Gemini Flash for volume; reserve Claude/GPT-4 for strategy synthesis.

### 5. Fire an affiliate post from a phone (when scripts are wired up)

Schedule a phone, push a script, poll for completion, log the result to `affiliate_clicks` for tracking.

## Thai viral content rules (always apply)

| Rule | Why |
|---|---|
| Hook in 1.5 seconds, speech first | TikTok algo rewards watch-time ≥75% |
| Direct address: พี่ๆ / เพื่อนๆ / แม่บ้านสาย… | Never "everyone" — kills relatability |
| One product per video, one CTA | Multi-product = 30% retention floor |
| End with a comment-prompter (เคยเจอแบบนี้มั้ย?) | Comments drive 2–3× more reach than likes |
| Numbers in Thai digits (๑๒๓) for older audiences | Trust signal in beauty/wellness |
| Soft suggesting > hard selling (ลองดูได้ค่ะ vs ซื้อเลย!) | ~40% conversion uplift |
| End-particles นะคะ / นะครับ | Feels personal, not corporate |
| ≤90 char captions for TikTok | 2 lines + 3 hashtags + ✨ |
| Wai gesture in opener frame | Cultural trust marker |

Hook library: `templates/thai-hooks.json` (80 templates across 8 categories).

## Cultural don'ts (instant unfollows / bans)

- Feet pointing at faces, monks, or the king
- Mocking food (cricket/fermented fish jokes flop with mainstream audiences)
- Western red "SALE!" overlays — looks spammy; use pastel + cute icons
- Hard-sell within first 5 seconds
- Self-purchases through your own affiliate link (instant Shopee claw-back)
- Cashback rebates to buyers ("buy via my link, I'll send back ฿20") — explicitly banned
- Posting the same content from 40 phones within 5 minutes — content-similarity classifier flags

## Decision triggers (pre-committed; don't deliberate live)

| If, by | Then |
|---|---|
| Day 14, TikTok Shop cash < ฿5k | Audit content; cut bottom 50% of accounts; re-script with sharper hooks |
| Day 30, CDS clients < 3 | Switch outbound channel from DM to Facebook Group cold-posting |
| Day 30, no LINE OA closed | Pitch existing CDS clients on LINE OA as an add-on |
| Day 45, cumulative cash < ฿300k | Strategy reset — fix or kill, don't add |
| Day 60, MRR < ฿400k | Cut bottom 25% of CDS clients (lowest margin) |
| Day 60, MRR > ฿700k | Hire CDS account manager + content editor immediately |
| Day 90, MRR > ฿1M | Begin play #5 (cross-border drop-ship) |
| Day 90, MRR < ฿500k | Honest debrief; pick 1 play to keep, kill the rest |

## Reference files in this skill

| File | Contents |
|---|---|
| `reference/90-day-plan.md` | Full execution calendar, P&L model, cost structure, risk register |
| `reference/fast-growth-2026.md` | The original 5-play strategy memo with macro Thai market data |
| `reference/phone-farm-ops.md` | gemphonefarm tool reference + cloud automation fallback |
| `reference/thai-market-data.md` | Hard data points: 71.85M pop, 88% internet, 49M Facebook, 44M TikTok, GDP $580B |
| `templates/thai-hooks.json` | 80 viral hook templates across 8 categories |
| `templates/cds-pricing.md` | Productized service tiers and elevator pitches |
| `sops/phone-onboarding.md` | Flash + root + warm-account procedure |
| `sops/weekly-review.md` | Monday morning 60-min checklist |

## When to use this skill

- Any user message about Thailand market, fast-growth plays, Shopee/Lazada/TikTok affiliate
- Any operation involving the phone farm (gemphonefarm MCP)
- Any work on the CDS service line or contentsdigital.us writer/CMS
- Any decision-trigger evaluation (where are we in the 90-day plan?)
- Any time the user mentions "Box", "Boxphone", "phone farm", "fleet", or device counts

## When NOT to use this skill

- Generic Claude Code questions
- Work unrelated to Thai market or our specific infrastructure
- Pure software engineering tasks without business context

## Citations + source of truth

All strategic claims trace back to:
- DataReportal Digital 2024 Thailand report (public)
- Wikipedia Economy of Thailand article (public)
- Live `gemphonefarm_list_devices` output (your fleet)
- The `ui-template` repository at `github.com/ContentsUS/ui-template`
- The two markdown deliverables in `state/research/`

Update this skill quarterly. Phone farm inventory drifts; market numbers shift; the operating principles stay the same.
