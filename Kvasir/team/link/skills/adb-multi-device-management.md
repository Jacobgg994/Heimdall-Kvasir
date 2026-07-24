---
name: adb-multi-device-management
description: จัดการ 20+ Android devices ผ่าน USB hub — topology, auto-reconnect, parallel commands
metadata:
  type: skill
  category: device-control
  owner: link
---

# ADB Multi-Device Management — 20+ Device Fleet

> "Every device, always reachable."

## Architecture Overview

```
Windows Host (USB Hub Physical)
  │
  ├── USB 3.0 Powered Hub (12-port × 2 daisy-chain)
  │   ├── Port 01-10 → Note 8 #01-10 (USB-A → USB-C cable)
  │   ├── Port 11-19 → Note 8 #11-19 (USB-A → USB-C cable)
  │   └── Port 20    → S21 FE #20
  │
  └── PowerShell ADB Bridge
      └── powershell.exe -Command "adb ..."
              │
        WSL2 Linux (Ubuntu)
              │
          LINK Scripts → REST API → WebSocket → Teams
```

## Critical Rule: WSL2 ADB Bridge

**WSL2 cannot see USB devices directly.** The ADB server runs on Windows.
Always use `powershell.exe` to execute ADB commands:

```bash
# WRONG — WSL2 ADB sees nothing
adb devices
# → List of devices attached
# → (empty)

# CORRECT — via PowerShell bridge
powershell.exe -Command "adb devices"
# → List of devices attached
# → 192.168.0.101:5555   device
# → 192.168.0.102:5555   device
```

### Alias for daily use
Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias adb="powershell.exe -Command \"adb \$@\""
alias fastboot="powershell.exe -Command \"fastboot \$@\""
```

Then use `adb` normally — it routes through PowerShell transparently.

## Device Naming Convention

Assign static hostnames per device for clarity:

```bash
# /etc/hosts on Windows or WSL2
192.168.0.101  note8-01
192.168.0.102  note8-02
192.168.0.103  note8-03
# ... up to note8-19
192.168.0.120  s21fe-20
```

## Auto-Reconnect Script

Every device must be monitored and reconnected automatically.

```bash
#!/bin/bash
# link-reconnect.sh — Run every 30s via cron / systemd timer

HOSTS=(
  "note8-01:192.168.0.101:5555"
  "note8-02:192.168.0.102:5555"
  # ... all 20 devices
)

for entry in "${HOSTS[@]}"; do
  NAME="${entry%%:*}"
  REST="${entry#*:}"
  IP="${REST%%:*}"
  PORT="${REST##*:}"

  # Check if device is already connected
  if ! powershell.exe -Command "adb devices" | grep -q "${IP}"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $NAME ($IP) OFFLINE — reconnecting..."

    # Try WiFi ADB connect
    powershell.exe -Command "adb connect ${IP}:${PORT}"

    # If that fails, log critical (needs USB intervention)
    if ! powershell.exe -Command "adb devices" | grep -q "${IP}"; then
      echo "[CRITICAL] $NAME ($IP) — WiFi ADB failed. USB intervention needed."
      # Optionally send alert
      # curl -X POST http://localhost:9090/alert -H "Content-Type: application/json" \
      #   -d '{"device":"'"$NAME"'","status":"offline","ip":"'"$IP"'","action":"needs_usb"}'
    fi
  fi
done
```

## Parallel Command Execution

Execute ADB commands on all devices simultaneously:

```bash
#!/bin/bash
# link-broadcast.sh — Run command on all devices

CMD="$@"
DEVICES=$(powershell.exe -Command "adb devices" | grep "device$" | awk '{print $1}')

for DEVICE in $DEVICES; do
  powershell.exe -Command "adb -s $DEVICE shell \"$CMD\"" &
done
wait
echo "[DONE] Command broadcast to $(echo "$DEVICES" | wc -l) devices."
```

### Debug parallel output (keep device identity)

```bash
#!/bin/bash
# link-broadcast-labelled.sh

CMD="$@"
TMPDIR="/tmp/link-broadcast-$$"
mkdir -p "$TMPDIR"
DEVICES=$(powershell.exe -Command "adb devices" | grep "device$" | awk '{print $1}')

for DEVICE in $DEVICES; do
  (
    OUTPUT=$(powershell.exe -Command "adb -s $DEVICE shell \"$CMD\"" 2>&1)
    echo "=== $DEVICE ===" > "$TMPDIR/$DEVICE.log"
    echo "$OUTPUT" >> "$TMPDIR/$DEVICE.log"
  ) &
done
wait

# Print collated results
for f in "$TMPDIR"/*.log; do
  cat "$f"
  echo ""
done
rm -rf "$TMPDIR"
```

## USB Hub Topology Mapping

Maintain a topology map for troubleshooting:

```python
# link-topology.py

HUB_CONFIG = {
    "hub1": {
        "usb_port": "3-1",
        "ports": {
            1: "note8-01 (192.168.0.101)",
            2: "note8-02 (192.168.0.102)",
            3: "note8-03 (192.168.0.103)",
            4: "note8-04 (192.168.0.104)",
            5: "note8-05 (192.168.0.105)",
            6: "note8-06 (192.168.0.106)",
            7: "note8-07 (192.168.0.107)",
            8: "note8-08 (192.168.0.108)",
            9: "note8-09 (192.168.0.109)",
            10: "note8-10 (192.168.0.110)",
        }
    },
    "hub2": {
        "usb_port": "3-2",
        "ports": {
            1: "note8-11 (192.168.0.111)",
            2: "note8-12 (192.168.0.112)",
            3: "note8-13 (192.168.0.113)",
            4: "note8-14 (192.168.0.114)",
            5: "note8-15 (192.168.0.115)",
            6: "note8-16 (192.168.0.116)",
            7: "note8-17 (192.168.0.117)",
            8: "note8-18 (192.168.0.118)",
            9: "note8-19 (192.168.0.119)",
            10: "s21fe-20 (192.168.0.120)",
        }
    }
}

def print_topology():
    for hub_name, hub in HUB_CONFIG.items():
        print(f"\n🔌 {hub_name} (USB {hub['usb_port']})")
        for port_num, device in hub["ports"].items():
            print(f"  ├── Port {port_num:02d}: {device}")
```

## Connection Logging

Every connect/disconnect must be logged:

```bash
#!/bin/bash
# link-log-connection.sh — Log connection changes
# Run every 30s in a loop

PREV_DEVICES=""

while true; do
  CURRENT=$(powershell.exe -Command "adb devices" 2>/dev/null | grep "device$" | sort)

  if [ "$CURRENT" != "$PREV_DEVICES" ]; then
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

    # Devices gone offline
    while IFS= read -r line; do
      if ! echo "$CURRENT" | grep -q "$line"; then
        DEVICE_ID=$(echo "$line" | awk '{print $1}')
        echo "[$TIMESTAMP] DISCONNECT: $DEVICE_ID" >> /var/log/link/connections.log
      fi
    done <<< "$PREV_DEVICES"

    # Devices come online
    while IFS= read -r line; do
      if ! echo "$PREV_DEVICES" | grep -q "$line"; then
        DEVICE_ID=$(echo "$line" | awk '{print $1}')
        echo "[$TIMESTAMP] CONNECT: $DEVICE_ID" >> /var/log/link/connections.log
      fi
    done <<< "$CURRENT"

    PREV_DEVICES="$CURRENT"
  fi

  sleep 30
done
```

## USB Hub Status API (Public)

Expose hub status for all teams via REST:

```python
# FastAPI endpoint

@app.get("/link/devices")
def get_all_devices():
    devices = []
    raw = subprocess.run(
        ["powershell.exe", "-Command", "adb devices"],
        capture_output=True, text=True
    ).stdout

    for line in raw.strip().split("\n")[1:]:  # skip header
        if "device" in line:
            device_id = line.split()[0]
            status = line.split()[1]
            devices.append({
                "id": device_id,
                "status": status,
                "reachable": status == "device",
                "last_seen": get_last_seen(device_id),
                "usb_port": get_usb_port(device_id),
                "hub": get_hub(device_id),
            })

    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "total": len(devices),
        "online": sum(1 for d in devices if d["reachable"]),
        "offline": sum(1 for d in devices if not d["reachable"]),
        "devices": devices
    }
```

## Common Issues & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `adb devices` empty on WSL2 | ADB server on Windows not running | `powershell.exe -Command "adb start-server"` |
| Device shows `unauthorized` | RSA key not accepted on device | Check device screen → allow USB debugging |
| Device keeps disconnecting | USB cable loose or hub port failing | Try different port, check cable |
| `device offline` after WiFi ADB | Device went to sleep | `adb reconnect` or wake with `input keyevent 26` |
| ADB command hangs | Device busy or ANR | `adb kill-server` → `adb start-server` |
| Parallel commands race condition | Multiple adb -s to same device | Use mutex/lock per device serial |

## Device Farm Specs (Reference)

| Property | Value |
|----------|-------|
| Device count | 20 (19 Note 8 + 1 S21 FE) |
| Note 8 SoC | Exynos 8895 (8-core) |
| Note 8 RAM | 5.4 GB (~3.6 GB available) |
| Note 8 Storage | 53 GB internal |
| Note 8 Root | Magisk (systemless) |
| Network | WiFi 192.168.0.x, host 192.168.0.72 |
| Hub | Powered USB 3.0 via Windows host |
| Bridge | `powershell.exe -Command "adb ..."` from WSL2 |
