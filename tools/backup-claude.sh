#!/bin/bash
# 🚚 Backup Claude Code + Skills + Memory — สำหรับย้ายเครื่อง
# วิธีใช้: bash backup-claude.sh

BACKUP_DIR="${HOME}/backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "╔══════════════════════════════════════╗"
echo "║   🚚 Claude Backup for Migration    ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "Backup to: $BACKUP_DIR"
echo ""

# 1. Skills
echo "[1/5] Backing up skills..."
cp -r ~/.claude/skills "$BACKUP_DIR/skills"
echo "       $(find "$BACKUP_DIR/skills" -name 'SKILL.md' | wc -l) skills"

# 2. Memory & Projects
echo "[2/5] Backing up memory..."
cp -r ~/.claude/projects "$BACKUP_DIR/projects"
echo "       $(find "$BACKUP_DIR/projects" -name '*.md' | wc -l) memory files"

# 3. Settings & Config
echo "[3/5] Backing up config..."
cp ~/.claude/settings.json "$BACKUP_DIR/settings.json" 2>/dev/null
cp ~/.claude/mcp.json "$BACKUP_DIR/mcp.json" 2>/dev/null
[ -d ~/.claude/agents ] && cp -r ~/.claude/agents "$BACKUP_DIR/agents"
[ -d ~/.claude/workflows ] && cp -r ~/.claude/workflows "$BACKUP_DIR/workflows"
echo "       done"

# 4. List installed pip packages
echo "[4/5] Saving pip list..."
pip3 list --user 2>/dev/null | grep -iE "gemlogin|mcp|websocket|httpx|playwright|selenium" > "$BACKUP_DIR/pip-packages.txt"
echo "       $(cat "$BACKUP_DIR/pip-packages.txt" | wc -l) key packages"

# 5. Create tar
echo "[5/5] Creating tar.gz..."
ARCHIVE="${HOME}/claude-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf "$ARCHIVE" -C "$BACKUP_DIR" .
rm -rf "$BACKUP_DIR"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║        ✅ Backup Complete!          ║"
echo "╠══════════════════════════════════════╣"
echo "║  $(printf '%-34s' "$ARCHIVE") ║"
echo "║  $(printf '%-34s' "Size: $(du -h "$ARCHIVE" | cut -f1)") ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "📋 Next steps on NEW machine:"
echo ""
echo "  # 1. Copy this file to new machine"
echo "  scp $ARCHIVE user@new-machine:~/"
echo ""
echo "  # 2. On new machine, restore:"
echo "  tar -xzf ~/$(basename "$ARCHIVE") -C ~/ --overwrite"
echo ""
echo "  # 3. Install pip packages:"
echo "  pip install -r <(tar -xzf ~/$(basename "$ARCHIVE") --to-stdout pip-packages.txt | awk '{print \$1}')"
echo ""
echo "🪟 Windows side (ทำบน Windows):"
echo "  Copy C:\\Users\\Admin\\.gemlogin\\ → เครื่องใหม่"
echo "  Copy C:\\Users\\Admin\\Documents\\Lab\\DrumXPath\\ → เครื่องใหม่"
echo "  Copy D:\\Owen\\Lab\\gemlogin-mcp\\ → เครื่องใหม่ (หรือ git clone)"
