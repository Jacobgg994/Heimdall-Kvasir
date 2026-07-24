# GemLogin Skills Registry

Auto-generated from project structure and use cases. Last updated: 2025-06-22.

## Quick Reference

| Skill | Purpose | Use When |
|---|---|---|
| **gemlogin** | Core MCP setup, tool map, registration, troubleshooting | Installing, configuring, or understanding MCP server |
| **gemlogin-profile-operations** | Profile lifecycle, warm-up, batch ops, group control | Managing profiles, batch automation, parallel execution |
| **gemlogin-script-execution** | Script discovery, parameters, retry logic, monitoring | Running scripts, error recovery, orchestration |
| **gemlogin-youtube-automation** | View boosting, watch time, interactions, search-first | YouTube engagement workflows, metrics tracking |
| **gemlogin-facebook-multipost** | Matrix scheduling, multi-round posting, category routing | Facebook group campaigns, content distribution |
| **gemlogin-tiktok** | TikTok workflow patterns, selectors, feed loops | TikTok automation, debugging flows, comment/share handling |
| **gemlogin-edit** | DB surgery, workflow patching, reload/test | Modifying workflows, testing changes, reloading |
| **gemlogin-update-skills** | Skill catalog sync, version management | Keeping skills up-to-date, adding new workflows |

---

## Skill Details

### Core Skills

#### `gemlogin`
**When to use:** First interaction, MCP setup, tool reference

Content:
- Installation & registration for Claude Code, Claude Desktop, Cursor
- Local vs. cloud API config
- Complete tool map (`gemlogin_*` functions)
- Resources (status, profiles)
- Prompts (warm_profile, post_to_group)
- Troubleshooting table

Key reference: See "Operating Rules" section for secrets handling and best practices.

---

#### `gemlogin-profile-operations`
**When to use:** Managing profiles, batch operations, warm-up campaigns

Content:
- Profile lifecycle states (id, name, group, proxy, browser config)
- Account warm-up workflow (batching, safe timings)
- Parallel fan-out execution
- Group-based operations (list → filter → execute)
- Status checks & health monitoring
- Error recovery per failure type
- Integration patterns with scripts

Key patterns:
- Batch size 5–10 to avoid CPU spike
- Wait for activeBrowsers to drop before next batch
- Always close profiles when done
- Log results to summary table

---

#### `gemlogin-script-patterns`
**When to use:** Executing scripts, error recovery, orchestration

Content:
- Script discovery (list_scripts, find_script, fuzzy matching)
- Parameter validation per type (string, number, filepath, boolean)
- Basic execution syntax & return structure
- Retry strategies (1x, 2x, 3x+ attempts)
- Exact vs. fuzzy script name matching
- Status polling & monitoring
- Killing stuck scripts
- Multi-script orchestration (A → B workflows)
- Error analysis & common failures
- Performance tuning (speed vs. reliability)
- Security & sensitive params
- Checklist for production

---

### Use-Case Skills

#### `gemlogin-youtube-automation`
**When to use:** YouTube view campaigns, watch time engagement, interactions

Content:
- Standard script parameters (target_urls, watch_sec, like_rate, search_mode)
- Direct URL vs. search-first mode explanation
- Organic engagement patterns (variance, scroll, interactions)
- Multi-URL batching strategy
- Interaction farming (light/medium/aggressive)
- Troubleshooting YouTube-specific failures
- Best practices (warm first, space watches, rotation, metrics)

Real-world config example included.

---

#### `gemlogin-facebook-multipost`
**When to use:** Facebook group campaigns, matrix scheduling, category-based distribution

Content:
- Matrix concept (2D category × round routing)
- Standard parameters (category, round, media folder, captions, pages)
- Media folder organization best practices
- Batch execution plan for multi-category campaigns
- Failure handling per-page
- Audit logging format
- 24h spacing between rounds
- Safety checks (no duplicates, validate first)

Example: 6 profiles, 2 categories, 3 rounds = 36 posts coordinated.

---

#### `gemlogin-tiktok`
**When to use:** TikTok workflow debugging, pattern verification, live-tested selectors

Content:
- TikTok workflow classes (Like/comment/share, Warm-up Feed, Upload)
- DB-first surgery workflow
- Stable selectors (live-verified from VEO 2 feed)
- Comment input / link capture / share modal patterns
- Warm-up feed logic (ads skip, loop, weighted actions)
- Feed scroll techniques
- Upload publish flow (handling Post now confirm)
- Latest video link capture
- File input → string input migration
- Conditions & routing explanation

Selectors include data-e2e, aria-labels, XPath options.

---

#### `gemlogin-edit`
**When to use:** Modifying workflows, patching selectors, testing changes

Content:
- DB backup & recovery
- Script reload workflow
- Workflow JSON navigation
- Test execution & validation
- Common patch patterns

(Refer to SKILL.md for current details)

---

#### `gemlogin-update-skills`
**When to use:** Syncing skill catalog, installing new workflows

Content:
- Skill discovery from GemLogin app
- Version management
- Rollback procedures
- Bulk install patterns

(Refer to SKILL.md for current details)

---

## Skill Pairing Guide

### For YouTube Campaigns
```
gemlogin (setup) 
  → gemlogin-profile-operations (warm profiles 24h first)
  → gemlogin-script-patterns (discover YouTube script, validate params)
  → gemlogin-youtube-automation (config watch time, interactions)
  → gemlogin-profile-operations (close profiles, log metrics)
```

### For TikTok Workflow Debugging
```
gemlogin-tiktok (understand flow) 
  → gemlogin-edit (patch selectors in DB)
  → gemlogin-tiktok (verify live against live feed)
  → gemlogin-profile-operations (test on 1 profile)
  → gemlogin-script-patterns (run test, check status)
```

### For Facebook Multi-Round Campaign
```
gemlogin-facebook-multipost (design matrix)
  → gemlogin-profile-operations (prepare profiles, batch groups)
  → gemlogin-script-patterns (execute Round 1 scripts)
  → gemlogin-profile-operations (monitor activeBrowsers)
  → gemlogin-script-patterns (execute Rounds 2–3)
  → gemlogin-facebook-multipost (audit logs, verify no duplicates)
```

### For Complex Automation
```
gemlogin-script-patterns (plan orchestration)
  → gemlogin-profile-operations (decide batch sizes)
  → gemlogin-youtube-automation / gemlogin-facebook-multipost (domain config)
  → gemlogin-profile-operations (monitor + recover)
  → gemlogin-script-patterns (error analysis, retry logic)
```

---

## Quick Troubleshooting

**"I don't know which skill to use"**
- Just starting? → `gemlogin`
- Running profiles? → `gemlogin-profile-operations`
- Executing scripts? → `gemlogin-script-patterns`
- YouTube views? → `gemlogin-youtube-automation`
- Facebook posts? → `gemlogin-facebook-multipost`
- TikTok issues? → `gemlogin-tiktok`
- Modifying workflows? → `gemlogin-edit`
- Installing scripts? → `gemlogin-update-skills`

**"Script failed after running"**
- First check → `gemlogin-script-patterns` error analysis table
- If it's a profile issue → `gemlogin-profile-operations` recovery patterns
- If it's TikTok → `gemlogin-tiktok` for selectors/flow
- If it's domain-specific (YouTube/Facebook) → relevant use-case skill

**"I want to warm profiles safely"**
→ `gemlogin-profile-operations` warm-up workflow

**"I need to optimize execution speed"**
→ `gemlogin-script-patterns` performance tuning section

---

## File Organization

```
.agents/skills/
├── gemlogin/
│   └── SKILL.md                         (core setup)
├── gemlogin-profile-operations/
│   └── SKILL.md                         (batch profile ops)
├── gemlogin-script-patterns/
│   └── SKILL.md                         (execution & orchestration)
├── gemlogin-youtube-automation/
│   └── SKILL.md                         (YouTube campaigns)
├── gemlogin-facebook-multipost/
│   └── SKILL.md                         (Facebook matrix posting)
├── gemlogin-tiktok/
│   └── SKILL.md                         (TikTok workflows)
├── gemlogin-edit/
│   └── SKILL.md                         (DB patching)
├── gemlogin-update-skills/
│   └── SKILL.md                         (skill sync)
└── SKILLS_REGISTRY.md                   (this file)
```

---

## Usage Examples

### Example 1: "Run YouTube views on profiles 1–5"
1. Check `gemlogin-youtube-automation` for parameter config
2. Use `gemlogin-script-patterns` to execute the script
3. Monitor with `gemlogin-script-patterns` status polling

### Example 2: "Post to Facebook in 3 rounds with different media per category"
1. Prepare media structure (see `gemlogin-facebook-multipost` media organization)
2. Use `gemlogin-facebook-multipost` to understand matrix routing
3. Use `gemlogin-profile-operations` for batch profile control
4. Use `gemlogin-script-patterns` to execute multi-round scripts sequentially
5. Verify results in `gemlogin-facebook-multipost` audit section

### Example 3: "TikTok script selector not working"
1. Check live DOM with browser inspector
2. Refer to `gemlogin-tiktok` live-verified selectors table
3. Use `gemlogin-edit` to patch the workflow in DB
4. Use `gemlogin-profile-operations` to test on 1 profile
5. Use `gemlogin-script-patterns` to monitor execution

---

## Notes

- All skills assume `gemlogin-mcp` is installed and `GemLogin` app is running on localhost:1010
- Set `GEMLOGIN_TIMEOUT=120` for first-run Chromium downloads
- Never commit or log sensitive params (tokens, passwords, cookies)
- Always close profiles when done to free resources
- Test new scripts on 1–2 profiles before scaling to 20+

Generated from project files:
- README.md (core features)
- server.py (tool map, resources, prompts)
- create_yt_script.py (YouTube use case)
- create_matrix_script.py (Facebook matrix use case)
- tiktok_script.js (TikTok patterns)
