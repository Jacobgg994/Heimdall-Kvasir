#!/usr/bin/env bash
# Connect to all Samsung Note 8 devices via WiFi ADB
# Staggered connections to avoid ADB server overload

set -e

DEVICES=(
  "192.168.0.32:5555"
  "192.168.0.48:5555"
  "192.168.0.56:5555"
  "192.168.0.80:5555"
  "192.168.0.81:5555"
  "192.168.0.112:5555"
  "192.168.0.117:5555"
  "192.168.0.122:5555"
  "192.168.0.145:5555"
  "192.168.0.150:5555"
  "192.168.0.159:5555"
  "192.168.0.166:5555"
  "192.168.0.183:5555"
  "192.168.0.197:5555"
  "192.168.0.244:5555"
)

echo "Phone Bot — Connecting to ${#DEVICES[@]} devices..."
echo ""

CONNECTED=0
FAILED=0

for device in "${DEVICES[@]}"; do
  echo -n "  $device ... "
  if adb connect "$device" 2>/dev/null | grep -q "connected"; then
    echo "✅"
    CONNECTED=$((CONNECTED + 1))
  else
    echo "❌"
    FAILED=$((FAILED + 1))
  fi
  sleep 0.5  # Stagger to avoid server overload
done

echo ""
echo "Done: $CONNECTED connected, $FAILED failed"
adb devices -l | grep -v "List of devices"
