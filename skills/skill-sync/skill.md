# Skill Sync

Auto-sync skills between `~/.claude/skills/` and `~/AIproject/skills/`

## How it works

1. **Auto-sync on session end**: Hook `Stop` in `~/.claude/settings.json` runs sync
2. **Status on session start**: Shows sync status
3. **Manual**: `bash ~/AIproject/skills/sync-skills.sh {to-aiproject|to-claude|status|watch}`

## Commands

- `to-aiproject` — backup .claude/skills → AIproject
- `to-claude` — restore AIproject → .claude/skills (on new machine)
- `status` — show sync status
- `watch` — monitor .claude/skills for changes (background)

## Files

- `~/AIproject/skills/sync-skills.sh` — sync script
- `~/.claude/settings.json` — hooks config
- `~/AIproject/skills/sync-log.txt` — sync log
- `~/AIproject/skills/.last-sync` — timestamp

## New machine setup

```bash
cd ~/AIproject
git pull
bash skills/sync-skills.sh to-claude
```
