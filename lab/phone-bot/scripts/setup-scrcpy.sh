#!/usr/bin/env bash
# Download and set up scrcpy-server.jar for Phone Bot
# This is required for Phase 1 — 30 FPS H.264 streaming

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVER_DIR="$PROJECT_DIR/server"

echo "Phone Bot — scrcpy-server.jar Setup"
echo "===================================="
echo ""

# Check if already present
if [ -f "$SERVER_DIR/scrcpy-server.jar" ]; then
  echo "✅ scrcpy-server.jar already present at $SERVER_DIR/scrcpy-server.jar"
  ls -lh "$SERVER_DIR/scrcpy-server.jar"
  exit 0
fi

# Option 1: Copy from system scrcpy installation
SYSTEM_JAR=""
for path in /usr/share/scrcpy/scrcpy-server.jar /usr/local/share/scrcpy/scrcpy-server.jar /opt/scrcpy/scrcpy-server.jar; do
  if [ -f "$path" ]; then
    SYSTEM_JAR="$path"
    break
  fi
done

if [ -n "$SYSTEM_JAR" ]; then
  echo "📋 Found system scrcpy: $SYSTEM_JAR"
  mkdir -p "$SERVER_DIR"
  cp "$SYSTEM_JAR" "$SERVER_DIR/scrcpy-server.jar"
  echo "✅ Copied to $SERVER_DIR/scrcpy-server.jar"
  ls -lh "$SERVER_DIR/scrcpy-server.jar"
  exit 0
fi

# Option 2: Download from GitHub
echo "📥 Downloading scrcpy-server.jar from GitHub..."
SCRCPY_VERSION="3.3.1"  # Update as new versions release
DOWNLOAD_URL="https://github.com/Genymobile/scrcpy/releases/download/v${SCRCPY_VERSION}/scrcpy-server-v${SCRCPY_VERSION}.jar"

mkdir -p "$SERVER_DIR"
if command -v wget &>/dev/null; then
  wget -q --show-progress -O "$SERVER_DIR/scrcpy-server.jar" "$DOWNLOAD_URL"
elif command -v curl &>/dev/null; then
  curl -L --progress-bar -o "$SERVER_DIR/scrcpy-server.jar" "$DOWNLOAD_URL"
else
  echo "❌ Neither wget nor curl found. Please install scrcpy: sudo apt install scrcpy"
  exit 1
fi

echo "✅ Downloaded scrcpy-server.jar v${SCRCPY_VERSION}"
ls -lh "$SERVER_DIR/scrcpy-server.jar"
