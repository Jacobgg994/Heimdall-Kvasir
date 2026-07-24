#!/usr/bin/env bash
# setup-termux.sh — bring a fresh Android phone (Termux installed) up to
# "headless coding agent" status in ~25 minutes.
#
# Run this INSIDE Termux on the target phone (e.g. via `adb shell`):
#   curl -fsSL <your-host>/setup-termux.sh | bash
# Or copy this file into ~/setup.sh and run `bash ~/setup.sh`.

set -e

green() { printf '\033[32m%s\033[0m\n' "$*"; }
cyan()  { printf '\033[36m%s\033[0m\n' "$*"; }
hr()    { printf '%.0s─' {1..60}; echo; }

cyan "▶ Termux agent-coder bootstrap"

# 1. Package manager refresh
hr
cyan "1/7 · apt update + base packages"
pkg update -y && pkg upgrade -y
pkg install -y nodejs git openssh curl which python build-essential jq termux-api

# 2. Storage access (one-time consent prompt on the phone)
hr
cyan "2/7 · Storage access"
termux-setup-storage || true

# 3. Project dir + dependency install
hr
cyan "3/7 · Agent runtime"
mkdir -p ~/agent
cd ~/agent
if [ ! -f package.json ]; then
  npm init -y >/dev/null
fi
npm install --silent @anthropic-ai/sdk dotenv pg yargs

# 4. Env template
hr
cyan "4/7 · Environment file"
if [ ! -f ~/agent/.env ]; then
  cat > ~/agent/.env <<'EOF'
# Per-phone API key from Anthropic Console — set a $5/day cap on this key
ANTHROPIC_API_KEY=sk-ant-replace-me

# Orchestrator Postgres on 210.1.1.155 (or wherever)
PG_HOST=210.1.1.155
PG_PORT=5432
PG_USER=agent
PG_PASSWORD=replace-me
PG_DATABASE=agentpool

# Per-phone identity
PHONE_ID=auto       # leave 'auto' to read from `hostname`
DEFAULT_MODEL=claude-haiku-4-5-20251001
EOF
  chmod 600 ~/agent/.env
fi

# 5. sshd for orchestrator remote-control
hr
cyan "5/7 · OpenSSH"
sshd >/dev/null 2>&1 || true
green "  sshd listening on port 8022 (Termux default)"
echo "  Drop orchestrator's public key into ~/.ssh/authorized_keys to skip passwords."

# 6. Wake-lock helper
hr
cyan "6/7 · Wake-lock"
termux-wake-lock || true
green "  Termux will keep CPU/network awake. Disable battery-optimisation for Termux in Android Settings."

# 7. Boot script
hr
cyan "7/7 · Boot persistence"
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-agent.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
sshd
cd ~/agent && nohup node agent-runner.js >> ~/agent/agent.log 2>&1 &
EOF
chmod +x ~/.termux/boot/start-agent.sh
green "  Boot script installed — install the Termux:Boot APK to make it run automatically."

hr
green "✓ Termux agent-coder bootstrap complete"
echo ""
echo "Next steps:"
echo "  · Edit ~/agent/.env with your real ANTHROPIC_API_KEY + Postgres creds"
echo "  · Drop agent-runner.js into ~/agent/ (see templates/agent-runner.js in skill)"
echo "  · Test with:  cd ~/agent && node agent-runner.js --once --dry-run"
echo "  · Orchestrator can SSH in:  ssh -p 8022 <phone-ip>"
