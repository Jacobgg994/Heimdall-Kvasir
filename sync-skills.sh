#!/bin/bash
# ============================================================
# AIProject Auto-Sync + Git Push
# ============================================================
# Syncs ALL important data into AIProject, then commits & pushes:
#   1. ~/.claude/skills/          → AIproject/skills/
#   2. ~/.claude/projects/*/memory/ → AIproject/Memory/
#   3. git add -A → commit → push
#
# Triggered by: Claude Code hooks, cron, or manual
# ============================================================

set -e

AIPROJECT="$HOME/Jacob-Office"
CLAUDE_SKILLS="$HOME/.claude/skills"
AUTO_MEMORY="$HOME/.claude/projects/-home-admin-jacob/memory"
LOCK_FILE="/tmp/ai-fullsync.lock"
LOG_FILE="$AIPROJECT/sync-log.txt"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }

# Prevent concurrent runs
if [ -f "$LOCK_FILE" ]; then
    lock_age=$(($(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || echo 0)))
    [ "$lock_age" -lt 60 ] && exit 0
fi
touch "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

case "${1:-sync}" in
    sync|full|to-aiproject)
        changed=false

        # === 1. Sync Skills ===
        if [ -d "$CLAUDE_SKILLS" ]; then
            newer=$(find "$CLAUDE_SKILLS" -newer "$AIPROJECT/skills/.last-sync" -type f 2>/dev/null | wc -l)
            if [ "$newer" -gt 0 ]; then
                log "Syncing skills ($newer changed files)..."
                rsync -aq --delete \
                    --exclude='sync-skills.sh' --exclude='sync-log.txt' \
                    --exclude='.last-sync' --exclude='.git' \
                    "$CLAUDE_SKILLS/" "$AIPROJECT/skills/"
                touch "$AIPROJECT/skills/.last-sync"
                changed=true
                log "Skills synced"
            fi
        fi

        # === 2. Sync Auto-Memory ===
        if [ -d "$AUTO_MEMORY" ]; then
            newer=$(find "$AUTO_MEMORY" -newer "$AIPROJECT/Memory/.last-sync" -type f 2>/dev/null | wc -l)
            if [ "$newer" -gt 0 ] || [ ! -f "$AIPROJECT/Memory/.last-sync" ]; then
                log "Syncing auto-memory ($newer changed files)..."
                mkdir -p "$AIPROJECT/Memory"
                rsync -aq --delete \
                    --exclude='.last-sync' \
                    "$AUTO_MEMORY/" "$AIPROJECT/Memory/"
                touch "$AIPROJECT/Memory/.last-sync"
                changed=true
                log "Auto-memory synced"
            fi
        fi

        # === 3. Sync Claude config ===
        if [ -f "$HOME/.claude/settings.json" ]; then
            if ! diff -q "$HOME/.claude/settings.json" "$AIPROJECT/.claude/settings.local.json" 2>/dev/null; then
                mkdir -p "$AIPROJECT/.claude"
                cp "$HOME/.claude/settings.json" "$AIPROJECT/.claude/settings.local.json"
                changed=true
                log "Claude config synced"
            fi
        fi

        # === 4. Git: commit + push ALL changes in AIProject ===
        if [ "${AUTO_GIT:-true}" = "true" ]; then
            cd "$AIPROJECT"

            # Stage ALL changes (new files, modifications, deletions)
            git add -A 2>&1 | tail -1 | tee -a "$LOG_FILE"

            if git diff --cached --quiet; then
                log "Git: no changes to commit"
            else
                count=$(git diff --cached --name-only | wc -l)
                git commit -m "auto: sync all data ($(date '+%Y-%m-%d %H:%M')) — $count files" \
                    2>&1 | tail -1 | tee -a "$LOG_FILE"
                git push origin main 2>&1 | tail -1 | tee -a "$LOG_FILE"
                log "Git: pushed $count files to origin"
            fi
        fi

        [ "$changed" = true ] && log "Sync + push complete!" || log "Nothing to sync"
        ;;

    to-claude|restore)
        log "Restoring from AIProject..."
        rsync -aq --delete "$AIPROJECT/skills/" "$CLAUDE_SKILLS/"
        rsync -aq --delete "$AIPROJECT/Memory/" "$AUTO_MEMORY/"
        log "Restored skills + memory to Claude Code"
        ;;

    status)
        echo "=== AIProject Sync Status ==="
        echo "Skills:    $CLAUDE_SKILLS ($(find $CLAUDE_SKILLS -maxdepth 1 -type d 2>/dev/null | wc -l) skills)"
        echo "Memory:    $AUTO_MEMORY ($(ls $AUTO_MEMORY 2>/dev/null | wc -l) files)"
        echo "AIProject: $AIPROJECT"
        [ -f "$AIPROJECT/skills/.last-sync" ] && echo "Last sync: $(stat -c '%y' $AIPROJECT/skills/.last-sync)"
        echo ""
        echo "Recent log:"
        tail -5 "$LOG_FILE" 2>/dev/null || echo "  (no log)"
        ;;

    *)
        echo "Usage: $0 {sync|to-claude|status}"
        echo "  sync       Sync all → AIProject → git push"
        echo "  to-claude  Restore from AIProject → Claude Code"
        echo "  status     Show sync status"
        ;;
esac
