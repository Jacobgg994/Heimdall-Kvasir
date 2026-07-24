---
name: device-health-monitoring
description: ตรวจสอบสุขภาพ device — battery, temperature, storage, CPU, network alert
metadata:
  type: skill
  category: device-control
  owner: link
---

# Device Health Monitoring — Fleet Dashboard

> "A device you don't monitor is a device you don't own."

## Monitoring Architecture

```
Every Device (heartbeat every 30s)
  │
  ├── Battery: level, temperature, voltage, health, plugged
  ├── Storage: internal, external (if any), system
  ├── CPU: load, frequency, throttling
  ├── Memory: total, available, low-memory killer stats
  ├── Network: WiFi RSSI, IP, connectivity test
  └── ADB: connection state, latency, last seen
        │
        v
Central Collector (Python/Node.js)
  │
  ├── InfluxDB / SQLite (time-series)
  ├── Alert Engine (thresholds → Slack/Webhook)
  └── Dashboard (Streamlit/Grafana)
        │
        v
Public API → All Teams
```

## Core Monitoring Script

```bash
#!/bin/bash
# link-health-check.sh — Collect health metrics from all devices
# Run every 60s via cron or systemd timer

LOG_DIR="/var/log/link/health"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE_FILE=$(date '+%Y-%m-%d')
DEVICES=$(powershell.exe -Command "adb devices" | grep "device$" | awk '{print $1}')

SUMMARY_FILE="$LOG_DIR/summary-$DATE_FILE.log"

for DEVICE in $DEVICES; do
  (
    NAME=$(echo "$DEVICE" | tr -d ':')

    # Battery
    BATTERY=$(powershell.exe -Command "adb -s $DEVICE shell dumpsys battery" 2>/dev/null)
    LEVEL=$(echo "$BATTERY" | grep "level:" | awk '{print $2}')
    TEMP=$(echo "$BATTERY" | grep "temperature:" | awk '{print $2}')
    STATUS=$(echo "$BATTERY" | grep "status:" | awk '{print $2}')
    HEALTH=$(echo "$BATTERY" | grep "health:" | awk '{print $2}')
    PLUGGED=$(echo "$BATTERY" | grep "AC powered:" | awk '{print $3}')

    # Temperature in Celsius (raw value / 10)
    TEMP_C=$(echo "scale=1; $TEMP / 10" | bc)

    # Storage
    STORAGE=$(powershell.exe -Command "adb -s $DEVICE shell df /data/media/0" 2>/dev/null | tail -1)
    STORAGE_USED=$(echo "$STORAGE" | awk '{print $3}')
    STORAGE_TOTAL=$(echo "$STORAGE" | awk '{print $2}')
    STORAGE_PCT=$(echo "$STORAGE" | awk '{print $5}' | tr -d '%')

    # CPU load
    CPU_LOAD=$(powershell.exe -Command "adb -s $DEVICE shell cat /proc/loadavg" 2>/dev/null | awk '{print $1,$2,$3}')

    # Memory
    MEMINFO=$(powershell.exe -Command "adb -s $DEVICE shell cat /proc/meminfo" 2>/dev/null)
    MEM_TOTAL=$(echo "$MEMINFO" | grep "MemTotal:" | awk '{print $2}')
    MEM_AVAIL=$(echo "$MEMINFO" | grep "MemAvailable:" | awk '{print $2}')
    MEM_PCT=$(echo "scale=1; ($MEM_TOTAL - $MEM_AVAIL) * 100 / $MEM_TOTAL" | bc)

    # Network ping test
    PING=$(ping -c 1 -W 2 "$DEVICE" 2>/dev/null | grep "time=" | sed 's/.*time=\([0-9.]*\).*/\1/')
    [ -z "$PING" ] && PING="999"

    # Connection latency (adb shell echo)
    ADB_LATENCY=$(powershell.exe -Command "adb -s $DEVICE shell echo ok" 2>/dev/null | tail -1)

    # Write device log
    cat > "$LOG_DIR/${NAME}-${TIMESTAMP//[: ]/-}.log" << EOF
{
  "device": "$DEVICE",
  "timestamp": "$TIMESTAMP",
  "battery": {
    "level": $LEVEL,
    "temperature_c": $TEMP_C,
    "status": $STATUS,
    "health": $HEALTH,
    "plugged": $PLUGGED
  },
  "storage": {
    "used_mb": $STORAGE_USED,
    "total_mb": $STORAGE_TOTAL,
    "used_pct": $STORAGE_PCT
  },
  "cpu": {
    "load": "$CPU_LOAD"
  },
  "memory": {
    "total_kb": $MEM_TOTAL,
    "available_kb": $MEM_AVAIL,
    "used_pct": $MEM_PCT
  },
  "network": {
    "ping_ms": $PING
  }
}
EOF

    # Check thresholds — log alerts
    if [ "$LEVEL" -lt 20 ]; then
      echo "[ALERT] $DEVICE battery low: $LEVEL%" >> "$SUMMARY_FILE"
    fi
    if [ "$TEMP_C" -gt 45 ]; then
      echo "[ALERT] $DEVICE overheating: ${TEMP_C}C" >> "$SUMMARY_FILE"
    fi
    if [ "$STORAGE_PCT" -gt 90 ]; then
      echo "[WARN] $DEVICE storage nearly full: ${STORAGE_PCT}%" >> "$SUMMARY_FILE"
    fi
    if [ "$MEM_PCT" -gt 90 ]; then
      echo "[WARN] $DEVICE memory critical: ${MEM_PCT}%" >> "$SUMMARY_FILE"
    fi
    if [ "$PING" = "999" ]; then
      echo "[CRITICAL] $DEVICE network unreachable" >> "$SUMMARY_FILE"
    fi

  ) &
done
wait
```

## Alert Thresholds

| Metric | Warn | Critical | Action |
|--------|------|----------|--------|
| Battery level | < 30% | < 15% | Notify to charge / rotate devices |
| Battery temperature | > 40 C | > 48 C | Force shutdown to prevent swelling |
| Storage used | > 85% | > 93% | Clean logs, cached APKs, old data |
| Memory available | < 500 MB | < 200 MB | Kill cached processes, check for leaks |
| CPU load (15min avg) | > 4.0 | > 6.0 | Investigate rogue process |
| Network ping | > 100ms | > 500ms | Check WiFi quality, reconnect ADB |
| Device offline | > 60s | > 300s | Alert operator, mark for USB intervention |

## Streamlit Dashboard

```python
# link-dashboard.py — Streamlit health dashboard
import streamlit as st
import json
import glob
import os
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="LINK Device Farm", page_icon="🔌", layout="wide")
st.title("🔌 LINK — Device Health Dashboard")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

LOG_DIR = "/var/log/link/health"

# Load latest data for each device
device_data = {}
for f in sorted(glob.glob(f"{LOG_DIR}/*.log"), reverse=True):
    dev_name = os.path.basename(f).split("-")[0]
    if dev_name not in device_data:
        try:
            with open(f) as fh:
                device_data[dev_name] = json.load(fh)
        except:
            pass

if not device_data:
    st.warning("No device data collected yet. Run link-health-check.sh first.")
    st.stop()

# Summary metrics
df = pd.DataFrame([
    {
        "device": d["device"],
        "battery": d["battery"]["level"],
        "temp": d["battery"]["temperature_c"],
        "storage_pct": d["storage"]["used_pct"],
        "ram_pct": d["memory"]["used_pct"],
        "ping": d["network"]["ping_ms"],
    }
    for d in device_data.values()
])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Devices", len(df))
col2.metric("Online", len(df[df["ping"] < 500]))
col3.metric("Avg Battery", f'{df["battery"].mean():.0f}%')
col4.metric("Avg Temp", f'{df["temp"].mean():.1f} C')

# Battery gauge
st.subheader("Battery Levels")
for _, row in df.iterrows():
    color = "green" if row["battery"] > 50 else "orange" if row["battery"] > 20 else "red"
    st.markdown(
        f'<div style="display:flex;margin:2px"><div style="width:120px">{row["device"]}</div>'
        f'<div style="flex:1;background:#eee;border-radius:4px">'
        f'<div style="width:{row["battery"]}%;background:{color};height:20px;border-radius:4px;'
        f'text-align:center;color:white;font-size:12px">{row["battery"]:.0f}%</div></div></div>',
        unsafe_allow_html=True
    )

# Detailed table
st.subheader("Detailed Metrics")
st.dataframe(
    df.style.background_gradient(subset=["battery"], cmap="RdYlGn")
      .background_gradient(subset=["temp"], cmap="YlOrRd")
      .format({"temp": "{:.1f} C", "ping": "{:.0f} ms"})
)
```

## REST API (Health Check)

```python
# FastAPI endpoint

@app.get("/link/health")
def get_fleet_health():
    """Return aggregated health summary for all devices."""
    devices = []
    raw_devices = subprocess.run(
        ["powershell.exe", "-Command", "adb devices"],
        capture_output=True, text=True
    ).stdout

    for line in raw_devices.strip().split("\n")[1:]:
        if not line.strip() or "device" not in line:
            continue
        device_id = line.split()[0]

        # Get battery
        battery_out = subprocess.run(
            ["powershell.exe", "-Command", f"adb -s {device_id} shell dumpsys battery"],
            capture_output=True, text=True
        ).stdout

        level = None
        temp_c = None
        for bline in battery_out.split("\n"):
            if "level:" in bline:
                level = int(bline.split()[1])
            if "temperature:" in bline:
                temp_c = int(bline.split()[1]) / 10

        devices.append({
            "id": device_id,
            "battery_level": level,
            "temperature_c": temp_c,
            "healthy": level is not None and level > 20 and (temp_c is None or temp_c < 45)
        })

    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "total": len(devices),
        "healthy": sum(1 for d in devices if d.get("healthy")),
        "devices": devices
    }


@app.get("/link/health/device/{device_id}")
def get_device_health(device_id: str):
    """Return detailed health for one device."""
    # ... full details for one device
    pass
```

## Slack Alerts

```python
# link-alert-slack.py

import requests
import json
import subprocess
import sys

WEBHOOK_URL = "https://hooks.slack.com/services/..."

def send_alert(message, color="danger"):
    payload = {
        "attachments": [{
            "color": color,
            "title": "🔌 LINK Alert",
            "text": message,
            "footer": f"Device Farm • {datetime.now().strftime('%H:%M:%S')}"
        }]
    }
    requests.post(WEBHOOK_URL, json=payload)

# Integration with health check
CRITICAL_ALERTS = [
    ("Overheating", lambda d: d["battery"]["temperature_c"] > 48, "danger"),
    ("Battery Critical", lambda d: d["battery"]["level"] < 15, "danger"),
    ("Battery Low", lambda d: d["battery"]["level"] < 30, "warning"),
    ("Storage Full", lambda d: d["storage"]["used_pct"] > 93, "danger"),
    ("Device Offline", lambda d: d["network"]["ping_ms"] == 999, "danger"),
]

def check_and_alert(device_data):
    for label, condition, severity in CRITICAL_ALERTS:
        if condition(device_data):
            send_alert(
                f"[{severity.upper()}] {label} on {device_data['device']}: "
                f"{json.dumps(device_data, indent=2)}",
                color=severity
            )
```

## Maintenance Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Full health check | Every 60s | `link-health-check.sh` |
| Auto-reconnect | Every 30s | `link-reconnect.sh` |
| Log rotation | Daily | `logrotate /etc/logrotate.d/link` |
| Deep battery cycle | Monthly | Drain to 10% → full charge |
| Storage cleanup | Weekly | Remove old APKs, clear caches |
| Dashboard restart | On crash | systemd `Restart=always` |
