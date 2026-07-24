---
name: qccap-farm-ops
description: Use when Codex needs to explore, explain, or operate inside the QCCAP-FARM repository, especially for finding the right entry point, routing work between ops and automation code, following Boss/Secretary control-plane rules, tracing persona/account/manifest flows, or avoiding path and state-management mistakes.
---

# QCCAP-FARM Ops

Use this skill when the task is about the `qccap-farm` repo as a whole, not just one isolated script.

Pair it with:
- `$gemlogin` when GemLogin MCP, local API, or profile runtime state matters
- `$gemlogin-edit` when the task becomes direct GemLogin workflow DB surgery

## Quick Start

Confirm the repo path first. Typical location seen so far:
- macOS: `/Users/pajipan/Desktop/Paji/Gemlogin/qccap-farm`

Do not assume every machine uses that exact path.

Read in this order:
1. `README.md`
2. `CLAUDE.md`
3. `ops/README.md`
4. `ops/CLAUDE.md`
5. Then route to flow-specific files below

## Repo Map

- `ops/`: Boss/Secretary control plane, briefs, gates, reminders, roles
- `scripts/qccap/`: core Python automation for personas, assignment, manifests, and signup flows
- `scripts/`: shell helpers for fleet bootstrap, proxy setup, install, dashboard, and phone ops
- `state/`: live runtime data such as phones, bindings, checkpoints, probes, and research handoffs
- `skills/`: project-local playbooks for Thai growth and phone-agent patterns
- `docs/`: operator-facing notes, design docs, incident notes
- `vault/`: knowledge base and handoff material

## Task Routing

### Read the repo / find the right entry point

Start at:
- `README.md`
- `CLAUDE.md`
- `ops/README.md`

Then classify the task:
- Repo governance, briefing, approvals, reporting: `ops/`
- Persona import/binding/credential shape: `scripts/qccap/persona_loader.py`
- Phone/account pairing and sticky identity rules: `scripts/qccap/account_assigner.py`
- Campaign YAML to runnable manifest: `scripts/qccap/manifest_builder.py`
- Facebook registration through GemLogin + Playwright: `scripts/qccap/fb_register.py`
- Android-device signup flow through ADB/Jelly: `scripts/qccap/platform_signup.py`

### Persona and account work

Read:
- `scripts/qccap/persona_loader.py`
- `state/phones.json`

Use this path when the task mentions:
- persona import
- bind persona to phone
- Outlook age/state
- account state under `accounts.*`

### Campaign and assignment work

Read:
- `scripts/qccap/account_assigner.py`
- `scripts/qccap/manifest_builder.py`
- `scripts/qccap/schemas.py`
- `campaigns/*.yaml`

Use this path when the task mentions:
- campaign YAML
- run manifest
- cooldown
- sticky phone/account pairing
- proxy or tier filters

### Facebook or GemLogin register flow

Read:
- `scripts/qccap/fb_register.py`
- `scripts/qccap/platform_signup.py`
- `scripts/qccap/outlook_bulk.py` when signup primitives or ADB helpers matter

Expect:
- GemLogin local API on `localhost:1010`
- Playwright attachment for GemLogin profile-based flows
- persona JSON under `state/personas/`

### Boss brief / control-plane work

Read:
- `ops/README.md`
- `ops/CLAUDE.md`
- `ops/controls/approval-gates.md`
- `ops/controls/decision-log.md`
- relevant `ops/reports/` or `ops/reminders/` index files

Use this path when the task mentions:
- Boss
- Secretary S1 or S2
- approval gates
- daily brief
- decision log

## Operating Rules

1. Boss receives filtered decisions, not raw staff output.
2. Check `ops/controls/approval-gates.md` before cost-incurring, irreversible, or sensitive actions.
3. Treat `state/` as live operational data. Read carefully before writing.
4. Watch for hardcoded workspace paths such as `/Users/ccdev/QCCAP-FARM` in Python scripts. Flag path mismatch before trying to run them elsewhere.
5. This repo is a script-and-state workspace, not a normal packaged app. Do not assume one entrypoint, one test command, or one install command.

## Common Pitfalls

- Reading only `vault/` or `docs/` and missing the actual automation in `scripts/qccap/`
- Treating `ops/` as optional when the task is really about Boss/Secretary workflow
- Running scripts without checking hardcoded `WORKSPACE` paths
- Ignoring `state/bindings.sqlite`, `state/phones.json`, or persona JSON when debugging assignment behavior
- Summarizing raw operational output directly to the Boss instead of converting it into decisions and blockers

## Good Trigger Phrases

Use this skill when the user says things like:
- `read qccap-farm`
- `learn this repo`
- `where is the entry point in qccap-farm`
- `trace the facebook register flow`
- `how does manifest_builder work`
- `summarize this repo for Boss`
- `what file handles persona binding`
