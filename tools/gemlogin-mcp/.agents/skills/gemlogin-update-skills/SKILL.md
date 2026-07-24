---
name: gemlogin-update-skills
description: Update and install bundled GemLogin Codex skills from the gemlogin-skills repository on Forgejo. Use when the user asks to refresh, sync, pull, reinstall, or update local GemLogin skills from `https://forgejo.contentsdigital.us/zirz1911/gemlogin-skills.git`, including requests such as `$gemlogin-update-skills`, "update gemlogin skills", or "sync gemlogin skills".
---

# GemLogin Update Skills

## Overview

Refresh the local GemLogin skill set from the Forgejo source repository and install the bundled skills into a target Codex skills directory. The default source checkout is `~/Desktop/Paji/project/gemlogin-skills`. The default target is the current workspace `.agents/skills` when present, otherwise `~/.codex/skills`.

## Workflow

1. Use `scripts/update_gemlogin_skills.py` from this skill.
2. Let the script clone the source repo if missing.
3. Pull the repo with `git pull --ff-only` when the checkout is clean.
4. Run the source repo's `install.py` so bundled skills are installed consistently.
5. Report the installed skill list and any dirty-repo blocker.

## Commands

Update all GemLogin skills into the default target:

```bash
python3 .agents/skills/gemlogin-update-skills/scripts/update_gemlogin_skills.py
```

Update a specific target skills directory:

```bash
python3 .agents/skills/gemlogin-update-skills/scripts/update_gemlogin_skills.py --target /path/to/.agents/skills
```

Install from an already-updated local checkout without pulling:

```bash
python3 .agents/skills/gemlogin-update-skills/scripts/update_gemlogin_skills.py --skip-pull
```

Install only selected bundled skills:

```bash
python3 .agents/skills/gemlogin-update-skills/scripts/update_gemlogin_skills.py --only gemlogin gemlogin-edit
```

## Safety

- Do not use destructive git commands.
- If the source repository has uncommitted changes, stop and show `git status --short` instead of pulling.
- Use the source repo's `install.py` as the only install path so bundled skills and `skills-lock.json` stay consistent.
