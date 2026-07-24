---
name: wifi-adb-setup
description: เปิด ADB over WiFi สำหรับ device fleet — setup, persist, troubleshoot
metadata:
  type: skill
  category: device-control
  owner: link
---

# WiFi ADB Setup — Fleet Configuration

> "One USB cable to rule them all, then cut the cord."

## Overview

WiFi ADB lets us control all 20 devices without physical USB connection after initial setup. Essential for a device farm — devices stay on charging stands, reachable over network.

## Prerequisites

- Device already connected via USB
- USB debugging enabled (Developer Options)
- All devices on same network (192.168.0.x)
- Host machine at 192.168.0.72

## Step 1: Enable ADB over WiFi (via USB)

Connect each device via USB **one at a time** and run:

```bash
# MUST use PowerShell bridge on WSL2
powershell.exe -Command "adb tcpip 5555"

# Verify
powershell.exe -Command "adb devices"
# → 192.168.0.101:5555   device
```

**Important:** `adb tcpip 5555` restarts the ADB daemon on the device in TCP mode on port 5555. After this, the USB connection is released.

## Step 2: Connect via WiFi

```bash
# Replace with actual device IP
powershell.exe -Command "adb connect 192.168.0.101:5555"

# Verify connection
powershell.exe -Command "adb devices"
# → 192.168.0.101:5555   device
```

### Bulk connect script (all devices)

```bash
#!/bin/bash
# link-wifi-connect-all.sh

IPS=(
  "192.168.0.101"
  "192.168.0.102"
  "192.168.0.103"
  # ... all 20 devices up to .120
)

for IP in "${IPS[@]}"; do
  echo "Connecting $IP:5555..."
  powershell.exe -Command "adb connect ${IP}:5555" 2>/dev/null
done

echo "--- Connected devices ---"
powershell.exe -Command "adb devices"
```

## Step 3: Fast Parallel Scan (Find All Devices)

When you don't know which IPs are active, scan the subnet:

```powershell
# Windows PowerShell — parallel scan with .NET sockets
$subnet = "192.168.0"
$port = 5555
$timeout = 200  # milliseconds

$scriptBlock = {
  param($ip, $port, $timeout)
  $client = New-Object System.Net.Sockets.TcpClient
  $connect = $client.BeginConnect($ip, $port, $null, $null)
  $wait = $connect.AsyncWaitHandle.WaitOne($timeout, $false)
  if ($wait -and $client.Connected) {
    "$ip online"
  }
  $client.Close()
}

1..254 | ForEach-Object {
  Start-Job -ScriptBlock $scriptBlock -ArgumentList "$subnet.$_", $port, $timeout
} | Receive-Job -Wait -AutoRemoveJob | Sort-Object
```

From WSL2, run this as:
```bash
powershell.exe -File /mnt/c/scripts/scan-adb.ps1
```

## Step 4: Persist Across Reboots

### Problem
After device reboot, ADB daemon defaults back to USB mode. `adb tcpip 5555` needs to run again via USB — or we automate it on-device.

### Solution: Magisk Boot Script

Create a script that runs on device boot via Magisk:

```bash
#!/bin/bash
# /data/adb/service.d/wifi-adb.sh
# This runs at boot on Magisk-rooted devices

# Enable ADB over WiFi on boot
setprop service.adb.tcp.port 5555
stop adbd
start adbd

# Log to verify
echo "[$(date)] WiFi ADB enabled on boot" >> /data/local/tmp/wifi-adb-boot.log
```

**Install:**
```bash
# Push to Magisk service.d
powershell.exe -Command "adb push wifi-adb.sh /data/adb/service.d/"
powershell.exe -Command "adb shell chmod 755 /data/adb/service.d/wifi-adb.sh"
powershell.exe -Command "adb shell su -c 'restorecon /data/adb/service.d/wifi-adb.sh'"
```

### Alternative: Termux Boot (for non-root)
```bash
# Install Termux:Boot add-on
# Add to ~/.termux/boot/wifi-adb.sh
adb tcpip 5555
```

**Note:** Termux cannot run `adb` natively (sandbox). This approach only works if Termux has ADB access somehow — not recommended for our fleet. Use Magisk method.

## Step 5: Auto-Reconnect on Network Change

Device may lose WiFi connection or change IP. Handle with:

```bash
#!/bin/bash
# link-wifi-monitor.sh — Run every 60s via cron

KNOWN_IPS=(
  "192.168.0.101" "192.168.0.102" "192.168.0.103"
  # ... all 20
)

CONNECTED=$(powershell.exe -Command "adb devices" | grep ":5555" | awk '{print $1}' | cut -d: -f1)

for IP in "${KNOWN_IPS[@]}"; do
  if ! echo "$CONNECTED" | grep -q "$IP"; then
    echo "[CHECK] $IP not connected — attempting reconnect..."
    powershell.exe -Command "adb connect ${IP}:5555" 2>/dev/null

    # Verify
    sleep 1
    if powershell.exe -Command "adb devices" | grep -q "$IP"; then
      echo "[OK] $IP reconnected"
    else
      echo "[FAIL] $IP unreachable — maybe offline or IP changed"
      # Check if device is on network at all
      ping -c 1 -W 1 "$IP" &>/dev/null
      if [ $? -ne 0 ]; then
        echo "[INFO] $IP not responding to ping — device may be off or disconnected from WiFi"
      fi
    fi
  fi
done
```

## Troubleshooting Common Issues

### Device shows "offline" after WiFi connect
```
192.168.0.101:5555   offline
```

**Cause:** ADB daemon on device not ready or connection timed out.

**Fix:**
```bash
# Disconnect and reconnect
powershell.exe -Command "adb disconnect 192.168.0.101:5555"
sleep 2
powershell.exe -Command "adb connect 192.168.0.101:5555"

# If still offline, reconnect ADB on device side
powershell.exe -Command "adb reconnect"
```

### "Connection refused" on port 5555
```
failed to connect to '192.168.0.101:5555': Connection refused
```

**Cause:** `adb tcpip 5555` was not run (device still in USB mode), or ADB daemon crashed.

**Fix:** Must connect via USB temporarily:
```bash
# Plug USB → wait for device to appear
powershell.exe -Command "adb devices"
# → <serial>    device

# Enable TCP mode
powershell.exe -Command "adb -s <serial> tcpip 5555"

# Now connect via WiFi
powershell.exe -Command "adb connect 192.168.0.101:5555"
```

### Device disconnects every few minutes
**Cause:** WiFi power saving or screen-off disconnects.

**Fix:**
```bash
# Keep WiFi awake (run on device)
powershell.exe -Command "adb shell svc wifi stay-while-awake 1"  # or 'always'

# Prevent sleep
powershell.exe -Command "adb shell settings put global stay_on_while_plugged_in 3"  # USB + wireless charging

# Turn off battery optimization for ADB
powershell.exe -Command "adb shell dumpsys deviceidle whitelist +com.android.shell"
```

### IP changed (DHCP)
Devices may get new IP from DHCP. Best practices:
1. Set static IP per device in router DHCP reservation (by MAC address)
2. OR use mDNS: `adb connect note8-01.local` if mDNS is available
3. OR run the Fast Parallel Scan (Step 3) periodically

## Security Considerations

| Risk | Mitigation |
|------|-----------|
| WiFi ADB open on port 5555 | Only enable on internal network (192.168.0.x) |
| Unauthorized ADB access | Remove RSA keys on device disconnect |
| Man-in-the-middle | ADB connections are plain TCP — use SSH tunnel for sensitive ops |
| Device lost on network | Disable ADB over WiFi remotely: `adb shell setprop service.adb.tcp.port 0` |

## Fleet Reference

| Property | Value |
|----------|-------|
| Number of devices | 20 |
| Primary models | 19x Note 8 (SM-N950F), 1x S21 FE (SM-G990U) |
| ADB port | 5555 (default) |
| Network | 192.168.0.0/24 |
| Host | 192.168.0.72 |
| Persistence method | Magisk service.d boot script |
| Fallback | USB hub direct connection via `powershell.exe` |
| Monitor interval | 30s heartbeat check |
| Reconnect threshold | 60s offline → alert |
