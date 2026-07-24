#!/bin/bash
# ============================================================
# Skill Sync — Auto-sync between ~/.claude/skills/ and AIproject
# ============================================================
# Triggered by: Claude Code hooks, manual, or cron
# Direction:    Bidirectional (controlled by --to flag)
# Git:          Auto-commit + push (when --git flag used)
# ============================================================
AUTO_GIT=true  # Set to false to disable auto git push

set -e

CLAUDE_SKILLS="$HOME/.claude/skills"
AIPROJECT_SKILLS="$HOME/AIproject/skills"
LOCK_FILE="/tmp/skill-sync.lock"
LOG_FILE="$HOME/AIproject/skills/sync-log.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Prevent concurrent syncs
if [ -f "$LOCK_FILE" ]; then
    # Check if lock is stale (> 60 seconds)
    lock_age=$(($(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || echo 0)))
    if [ "$lock_age" -lt 60 ]; then
        exit 0  # Another sync is running
    fi
fi
touch "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

case "${1:-sync}" in
    to-aiproject|backup|sync)
        # Backup: ~/.claude/skills → AIproject
        log "Syncing: .claude/skills → AIproject"

        # Check if source has changes
        if [ -f "$AIPROJECT_SKILLS/.last-sync" ]; then
            newer=$(find "$CLAUDE_SKILLS" -newer "$AIPROJECT_SKILLS/.last-sync" -type f 2>/dev/null | wc -l)
            if [ "$newer" -eq 0 ]; then
                log "No changes detected, skipping sync"
                exit 0
            fi
            log "Detected $newer changed files"
        fi

        rsync -av --delete \
            --exclude='sync-skills.sh' \
            --exclude='sync-log.txt' \
            --exclude='.last-sync' \
            --exclude='.git' \
            "$CLAUDE_SKILLS/" "$AIPROJECT_SKILLS/"

        touch "$AIPROJECT_SKILLS/.last-sync"
        count=$(find "$AIPROJECT_SKILLS" -maxdepth 1 -type d | wc -l)
        log "Done! $count skills synced to AIproject"

        # Auto git push
        if [ "${AUTO_GIT:-true}" = "true" ]; then
            cd "$AIPROJECT_SKILLS/.."
            if git diff --quiet && git diff --cached --quiet; then
                log "Git: no changes to commit"
            else
                git add -A
                git commit -m "auto: sync skills ($(date '+%Y-%m-%d %H:%M'))" 2>&1 | tail -1 | tee -a "$LOG_FILE"
                git push origin main 2>&1 | tail -1 | tee -a "$LOG_FILE"
                log "Git: pushed to origin"
            fi
        fi
        ;;

    to-claude|restore)
        # Restore: AIproject → ~/.claude/skills
        log "Syncing: AIproject → .claude/skills"

        rsync -av --delete \
            --exclude='sync-skills.sh' \
            --exclude='sync-log.txt' \
            --exclude='.last-sync' \
            --exclude='.git' \
            "$AIPROJECT_SKILLS/" "$CLAUDE_SKILLS/"

        count=$(find "$CLAUDE_SKILLS" -maxdepth 1 -type d | wc -l)
        log "Done! $count skills restored to .claude/skills"
        ;;

    watch)
        # Watch mode — monitor .claude/skills for changes
        log "Starting watch mode..."
        while true; do
            inotifywait -r -e create,modify,delete --exclude '/\.' "$CLAUDE_SKILLS" 2>/dev/null
            sleep 2  # Debounce
            bash "$0" to-aiproject
        done
        ;;

    status)
        # Show sync status
        echo "=== Skill Sync Status ==="
        echo "Source:  $CLAUDE_SKILLS ($(find "$CLAUDE_SKILLS" -maxdepth 1 -type d | wc -l) skills)"
        echo "Target:  $AIPROJECT_SKILLS ($(find "$AIPROJECT_SKILLS" -maxdepth 1 -type d | wc -l) skills)"
        if [ -f "$AIPROJECT_SKILLS/.last-sync" ]; then
            echo "Last sync: $(stat -c '%y' "$AIPROJECT_SKILLS/.last-sync")"
        else
            echo "Last sync: Never"
        fi
        echo ""
        echo "Recent log:"
        tail -5 "$LOG_FILE" 2>/dev/null || echo "  (no log yet)"
        ;;

    *)
        echo "Usage: $0 {to-aiproject|to-claude|watch|status}"
        echo ""
        echo "  to-aiproject  Save skills to AIproject (backup)"
        echo "  to-claude     Restore skills from AIproject"
        echo "  watch         Auto-watch and sync on changes"
        echo "  status        Show sync status"
        ;;
esac
