# PULSE Advanced Learning — Phone Automation Mastery

> **วันที่**: 2026-07-01
> **ผู้เรียน**: PULSE 📳
> **6 หัวข้อ**: Android Internals → Proxy/Network → Anti-Detect → Automation Frameworks → Bulk Management → APK Analysis

---

## 1. Android Internals — สิ่งที่ GPF ควบคุมอยู่เบื้องหลัง

### Android Architecture (5 Layers)

```
Layer 5: Apps (TikTok, FB, LINE, Chrome)
Layer 4: Java Framework (ActivityManager, PackageManager, WindowManager)
Layer 3: Native C/C++ (WebKit, OpenGL, SQLite)
Layer 2: HAL (Hardware Abstraction Layer)
Layer 1: Linux Kernel (drivers, network, file system)
```

GPF ทำงานหลักที่ **Layer 4** — ผ่าน ADB → `input tap`, `am start`, `pm install`

### 3 Services สำคัญที่ GPF ใช้

| Service | GPF ใช้ทำอะไร | ADB Command |
|---------|-------------|-------------|
| **ActivityManager (AMS)** | เปิด/ปิด app, ตรวจว่า app foreground อยู่ไหม | `am start`, `am force-stop`, `dumpsys activity` |
| **PackageManager (PMS)** | ติดตั้ง/ถอน app, เช็ค version, list packages | `pm install`, `pm list packages`, `pm path` |
| **WindowManager (WMS)** | รู้ resolution, orientation, display info | `wm size`, `wm density` |

### AMS Deep Dive — ทำไม Touch บางทีถึงพลาด

AMS จัดการ **Activity Stack** — กองของ Activities ที่เปิดอยู่:

```
mTaskHistory[0]: Launcher (idle)
mTaskHistory[1]: TikTok (Foreground)
mTaskHistory[2]: Chrome (Background — killed)
```

**ปัญหา**: ถ้า app อยู่ใน background เกิน 30 นาที → Android LMK (Low Memory Killer) kill process → GPF touch ลงไปที่หน้าจอเปล่า → timeout

**วิธีแก้**: 
- `dumpsys activity activities | grep mResumedActivity` — เช็คว่า app foreground จริง
- `adb shell am start -n <pkg>/<activity>` — เปิด app ใหม่ทุก N actions
- ตั้ง `android:persistent="true"` บน custom ROM

### Key Dumpsys Commands สำหรับ GPF

```bash
# เช็คว่า app foreground อยู่ไหม
adb shell dumpsys activity activities | grep -E "mResumedActivity|topResumedActivity"

# ดู memory — app ถูก LMK kill หรือไม่
adb shell dumpsys meminfo com.zhiliaoapp.musically | grep TOTAL

# ดู CPU — app ค้าง / ANR หรือไม่
adb shell dumpsys cpuinfo | grep <package>

# เช็คการหมุนจอ — landscape/portrait
adb shell dumpsys window | grep mOrientation
```

---

## 2. Proxy & Network Stack — หัวใจของ Phone Farm

### Proxy Types

| Type | Protocol | ใช้กับอะไร | ข้อควรระวัง |
|------|----------|----------|------------|
| **HTTP Proxy** | HTTP/HTTPS CONNECT | Browser traffic | ไม่ cover UDP |
| **SOCKS5** | TCP + UDP | App-level traffic (TikTok, FB) | ช้ากว่า HTTP นิดหน่อย |
| **IPv6 Proxy** | All TCP/UDP | Full device traffic | ต้อง config ที่ device level |
| **Reverse Proxy** | — | ซ่อน backend | ไม่เกี่ยวกับ device |

### GPF Proxy Architecture

```
[Android Device]
    ↓ (SOCKS5 proxy config via ProxyDroid/Drony)
[IPv6 Proxy :8080]
    ↓
[Target Server — TikTok/FB/etc.]
```

### Device-Level Proxy Config

```bash
# ตั้ง Global Proxy (Android 5.0+)
adb shell settings put global http_proxy 192.168.1.100:8080

# ปิด Proxy
adb shell settings put global http_proxy :0

# ตรวจสอบ proxy ปัจจุบัน
adb shell settings get global http_proxy
```

### Proxy Validation Script (Scapy)

```python
from scapy.all import *

def validate_proxy(device_ip, proxy_ip, proxy_port):
    """
    1. เช็คว่า device online
    2. ส่ง SYN ไปที่ proxy → วัด RTT
    3. ส่ง request ผ่าน proxy → sniff traffic → ตรวจว่าไม่ leak
    """
    # Step 1: Device online?
    ping = IP(dst=device_ip) / ICMP()
    r = sr1(ping, timeout=2, verbose=0)
    if not r:
        return "❌ Device offline"
    
    # Step 2: Proxy reachable?
    syn = IP(dst=proxy_ip) / TCP(dport=proxy_port, flags="S")
    r = sr1(syn, timeout=2, verbose=0)
    if not (r and r[TCP].flags & 0x12):
        return "❌ Proxy unreachable"
    
    # Step 3: DNS Leak?
    # Sniff DNS traffic from device → must go through proxy
    dns_leak = sniff(filter=f"src host {device_ip} and udp port 53", timeout=5)
    if len(dns_leak) > 0:
        print(f"⚠️  DNS Leak: {len(dns_leak)} direct DNS queries detected")
    
    return f"✅ Proxy {proxy_ip}:{proxy_port} — OK"

# Usage
print(validate_proxy("192.168.1.50", "proxy.example.com", 8080))
```

### Proxy Rotation Strategy

```python
# proxy-rotation.py — สำหรับ GPF
import random

class ProxyRotator:
    def __init__(self, proxy_file="proxies.txt"):
        with open(proxy_file) as f:
            self.proxies = [line.strip() for line in f if line.strip()]
        self.assignments = {}  # device_serial → proxy
    
    def assign(self, device_serial):
        """หนึ่ง device = หนึ่ง proxy sticky"""
        if device_serial not in self.assignments:
            self.assignments[device_serial] = random.choice(self.proxies)
        return self.assignments[device_serial]
    
    def rotate(self, device_serial):
        """เปลี่ยน proxy (เช่นหลังโดน rate limit)"""
        old = self.assignments.get(device_serial)
        available = [p for p in self.proxies if p != old]
        self.assignments[device_serial] = random.choice(available)
        return self.assignments[device_serial]
    
    def health_check(self):
        """ทดสอบทุก proxy"""
        for proxy in self.proxies:
            ip, port = proxy.split(":")
            syn = IP(dst=ip) / TCP(dport=int(port), flags="S")
            r = sr1(syn, timeout=2, verbose=0)
            status = "✅" if (r and r[TCP].flags & 0x12) else "❌"
            print(f"{status} {proxy}")
```

---

## 3. Anti-Detect & Fingerprinting — ทำให้ Device ไม่ดูเหมือน Robot

### 4 Layers of Detection

```
Layer 4: Behavioral — mouse/touch pattern, scroll, keystroke timing
Layer 3: Browser/App Fingerprint — Canvas, WebGL, fonts, screen
Layer 2: Protocol (TLS/HTTP2) — JA3/JA4, cipher suites, headers
Layer 1: Network/IP — IP reputation, ASN type, geo consistency
```

### Layer 1: IP-Level (สำคัญสุดสำหรับ GPF)

```
✅ Residential IP > Mobile IP > Datacenter IP
✅ IPv6 /64 subnet — แต่ละ device ได้ IP ไม่ซ้ำ
✅ Geo consistent — IP ไทย = device ไทย
✅ Rate limit — <1 request/second/device
❌ Datacenter IP ใช้กับ FB/TikTok = แบนทันที
```

### Layer 2: TLS Fingerprint (Android Apps)

Android apps ส่ง TLS ผ่าน:
- **OkHttp** (แอพส่วนใหญ่) — มี fingerprint ตายตัว
- **Cronet/Chromium** — Chrome-based
- **Custom TLS** — หายาก

**วิธีเช็ค TLS fingerprint จาก device**:
```python
# tls-check.py — เช็คว่า TLS ดูเหมือน Android จริงไหม
from scapy.all import *

def check_tls_fingerprint(device_ip):
    """Sniff TLS ClientHello จาก device"""
    def analyze_tls(pkt):
        if TCP in pkt and pkt.haslayer(Raw):
            payload = bytes(pkt[Raw])
            if payload[0:3] == b'\x16\x03\x01':  # TLS ClientHello
                # Extract cipher suites
                ciphers_len = int.from_bytes(payload[7:9], 'big')
                ciphers = payload[9:9+ciphers_len]
                print(f"TLS from {pkt[IP].src}: {len(ciphers)//2} cipher suites")
    
    sniff(filter=f"src host {device_ip} and tcp port 443", prn=analyze_tls, count=5)
```

### Layer 3: Device Fingerprint — สิ่งที่ TikTok/FB ตรวจ

| Signal | วิธีเช็ค | ต้อง match |
|--------|---------|----------|
| Screen Resolution | `wm size` | Model จริง |
| Android Version | `getprop ro.build.version.release` | Model + ปี |
| Build Fingerprint | `getprop ro.build.fingerprint` | Official ROM |
| Language | `getprop persist.sys.locale` | TH (th-TH) |
| Timezone | `getprop persist.sys.timezone` | Asia/Bangkok |
| Device Model | `getprop ro.product.model` | จริง — ไม่ใช่ emulator |

```bash
# Quick Fingerprint Check
adb shell "echo 'Model: '$(getprop ro.product.model); \
  echo 'Android: '$(getprop ro.build.version.release); \
  echo 'Fingerprint: '$(getprop ro.build.fingerprint); \
  echo 'Locale: '$(getprop persist.sys.locale); \
  echo 'TZ: '$(getprop persist.sys.timezone)"
```

### Touch Humanization

```python
import random, time

def human_tap(x, y):
    """จำลอง touch แบบมนุษย์ — ไม่ใช่จุดเดียวเป๊ะ"""
    jitter_x = random.randint(-3, 3)
    jitter_y = random.randint(-3, 3)
    duration = random.randint(50, 150)  # ms
    return f"input swipe {x} {y} {x+jitter_x} {y+jitter_y} {duration}"

def human_swipe(x1, y1, x2, y2):
    """ปัดแบบมี micro-pause"""
    mid_x = (x1 + x2) // 2 + random.randint(-20, 20)
    mid_y = (y1 + y2) // 2 + random.randint(-20, 20)
    # 2-stage swipe — ไม่ใช่เส้นตรง
    cmd = f"input swipe {x1} {y1} {mid_x} {mid_y} 300 && \
           input swipe {mid_x} {mid_y} {x2} {y2} {random.randint(200,400)}"
    return cmd
```

---

## 4. Automation Frameworks — GPF vs ทางเลือก

### Comparison

| Framework | Speed | Stability | Cross-Platform | ใช้กับ GPF |
|-----------|-------|-----------|----------------|-----------|
| **GPF (atx-agent)** | ⚡ เร็วมาก | ⭐⭐⭐ | Android only | ✅ หลัก |
| **uiautomator2** | ⚡ เร็ว | ⭐⭐⭐ | Android only | ✅ เสริม |
| **Appium** | 🐢 ช้า | ⭐⭐ | Android + iOS | ⚠️ ทับซ้อน |
| **Espresso** | ⚡⚡ เร็วสุด | ⭐⭐⭐ | Android only | ❌ White-box |

### เมื่อไหร่ควรใช้ uiautomator2 แทน GPF

```python
# uiautomator2 — ดีกว่า GPF เมื่อ:
# 1. ต้องการหา element ด้วย XPath (GPF ใช้พิกัด)
# 2. ต้องการ wait จน element โผล่ (GPF ใช้ delay)
# 3. ต้องการอ่าน text จากหน้าจอ (GPF ใช้ screenshot)

import uiautomator2 as u2

d = u2.connect("192.168.1.50:5555")

# Wait for element — GPF ทำไม่ได้
d(text="Follow").wait(timeout=10)

# อ่านข้อความบนจอ — GPF ต้องใช้ OCR
title = d(resourceId="title").get_text()

# XPath — ยืดหยุ่นกว่าพิกัด
d.xpath('//android.widget.Button[@content-desc="Like"]').click()
```

### Hybrid Approach สำหรับ GPF

```
GPF: 80% ของ flows (tap, swipe, type — เร็ว ง่าย)
uiautomator2: 20% (element wait, text extraction, dynamic UI)
```

---

## 5. Bulk Device Management — จัดการ 60+ Devices

### Parallel ADB Framework

```python
#!/usr/bin/env python3
"""pulse-fleet.py — PULSE Fleet Manager"""

import subprocess
import concurrent.futures
import sys

def get_devices():
    """รายชื่อ devices ทั้งหมด"""
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    devices = []
    for line in result.stdout.strip().split('\n')[1:]:
        if '\tdevice' in line:
            serial = line.split('\t')[0]
            devices.append(serial)
    return devices

def run_on_device(serial, command, timeout=30):
    """รันคำสั่งบน device เดียว"""
    try:
        result = subprocess.run(
            ['adb', '-s', serial] + command.split(),
            capture_output=True, text=True, timeout=timeout
        )
        return {'serial': serial, 'ok': True, 'output': result.stdout.strip()}
    except Exception as e:
        return {'serial': serial, 'ok': False, 'output': str(e)}

def run_on_all(command, max_workers=10):
    """รันคำสั่งบนทุก device พร้อมกัน — 10 threads"""
    devices = get_devices()
    print(f"📱 Running on {len(devices)} devices: {command}")
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(run_on_device, d, command): d for d in devices}
        for f in concurrent.futures.as_completed(futures):
            results.append(f.result())
    
    ok = [r for r in results if r['ok']]
    fail = [r for r in results if not r['ok']]
    print(f"✅ {len(ok)} success | ❌ {len(fail)} failed")
    return results

# Quick Commands
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "shell getprop ro.product.model"
    results = run_on_all(cmd)
```

### Bulk Operations Cheatsheet

```bash
# ติดตั้ง APK ทั้ง farm
for D in $(adb devices | awk 'NR>1{print $1}'); do
  adb -s $D install -r app.apk &
done
wait

# รีบูททั้ง farm
for D in $(adb devices | awk 'NR>1{print $1}'); do
  adb -s $D reboot &
done

# เช็คสุขภาพ — ทุก device
for D in $(adb devices | awk 'NR>1{print $1}'); do
  MODEL=$(adb -s $D shell getprop ro.product.model 2>/dev/null)
  BATT=$(adb -s $D shell dumpsys battery 2>/dev/null | grep "level" | awk '{print $2}')
  WIFI=$(adb -s $D shell dumpsys wifi 2>/dev/null | grep "Wi-Fi is" | awk '{print $3}')
  echo "$D | $MODEL | Battery: $BATT% | WiFi: $WIFI"
done

# ลบ cache ทุก device (แก้ app freeze)
for D in $(adb devices | awk 'NR>1{print $1}'); do
  adb -s $D shell pm trim-caches 1G &
done
```

### Device Health Dashboard (Streamlit)

```python
# pulse-dashboard.py
import streamlit as st
import subprocess

st.title("📳 PULSE — GemphoneFarm Fleet Dashboard")
st.metric("Total Devices", "60")

devices = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
online = [d for d in devices.stdout.split('\n') if 'device' in d and 'List' not in d]

for d in online:
    serial = d.split('\t')[0]
    model = subprocess.run(
        ['adb', '-s', serial, 'shell', 'getprop', 'ro.product.model'],
        capture_output=True, text=True
    ).stdout.strip()
    battery = subprocess.run(
        ['adb', '-s', serial, 'shell', 'dumpsys', 'battery'],
        capture_output=True, text=True
    ).stdout
    
    level = "N/A"
    for line in battery.split('\n'):
        if 'level' in line:
            level = line.strip().split(':')[1].strip()
    
    col1, col2, col3 = st.columns(3)
    col1.metric(serial, model)
    col2.metric("Battery", f"{level}%")
    col3.metric("Status", "✅ Online" if level != "N/A" else "⚠️")
```

---

## 6. APK Analysis — ตรวจสอบ App ก่อนลง Farm

### Quick APK Triage

```bash
# 1. ดู package name + version
aapt dump badging app.apk | grep -E "package:|versionCode|versionName"

# 2. ดู permissions
aapt dump permissions app.apk

# 3. ดู activities
aapt dump badging app.apk | grep "launchable-activity"

# 4. ดู certificate
jarsigner -verify -verbose -certs app.apk | head -20
```

### Decompile APK (jadx)

```bash
# Install jadx
sudo apt install jadx

# Decompile
jadx -d output_dir/ app.apk

# ดู AndroidManifest.xml
cat output_dir/AndroidManifest.xml | grep -E "permission|activity|service|receiver"
```

### APK Security Checklist

```python
"""pulse-apk-check.py — Quick APK Safety Check"""

import os, subprocess, json

def check_apk(apk_path):
    report = {"file": apk_path, "risk": "LOW", "findings": []}
    
    # 1. Unknown sources?
    cert = subprocess.run(
        ['jarsigner', '-verify', '-verbose', apk_path],
        capture_output=True, text=True
    )
    if "certificate is not trusted" in cert.stderr or "unsigned" in cert.stdout:
        report["findings"].append("⚠️ Unsigned/self-signed certificate")
        report["risk"] = "HIGH"
    
    # 2. Excessive permissions
    perms = subprocess.run(
        ['aapt', 'dump', 'permissions', apk_path],
        capture_output=True, text=True
    ).stdout
    
    dangerous_perms = [
        'READ_SMS', 'SEND_SMS', 'READ_CONTACTS', 'ACCESS_FINE_LOCATION',
        'RECORD_AUDIO', 'CAMERA', 'READ_CALL_LOG', 'PROCESS_OUTGOING_CALLS'
    ]
    for p in dangerous_perms:
        if p in perms:
            report["findings"].append(f"🔴 Dangerous: {p}")
            report["risk"] = "MEDIUM"
    
    # 3. Signature
    aapt = subprocess.run(
        ['aapt', 'dump', 'badging', apk_path],
        capture_output=True, text=True
    ).stdout
    
    if 'package:' in aapt:
        pkg_line = [l for l in aapt.split('\n') if 'package:' in l][0]
        report["package"] = pkg_line.split("name='")[1].split("'")[0]
    
    # 4. Size
    size_mb = os.path.getsize(apk_path) / (1024*1024)
    report["size_mb"] = round(size_mb, 1)
    if size_mb > 500:
        report["findings"].append("⚠️ APK > 500MB — huge, could be bloated/malicious")
    
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        report = check_apk(sys.argv[1])
        print(json.dumps(report, indent=2))
```

### Malware Detection (Quick Rules)

```
🚨 Red Flags:
- Package: com.whatsapp.* but not signed by WhatsApp Inc
- Contains dexguard/obfuscation on a simple app
- Requests RECORD_AUDIO + CAMERA + SEND_SMS + READ_CONTACTS simultaneously
- Does NOT have launchable-activity (headless malware)
- Native libraries (.so) in a simple "flashlight" app
- Connects to known-bad IPs in strings.xml
```

---

## 📊 PULSE Knowledge Map — Complete

```
                    PULSE 📳
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   📱 Device       🌐 Network       🛡️ Security
   ─────────       ─────────       ─────────
   ADB             Scapy           Anti-Detect
   Android AMS     Proxy Rotate    TLS Fingerprint
   uiautomator2    SOCKS5/IPv6     Behavior Humanize
   APK Analysis    DNS Leak        APK Malware
        │               │               │
        └───────────────┼───────────────┘
                        │
                 GPF Operations
                 Fleet Management
                 Streamlit Dashboard
```

---

## 🎯 Learning Path

| Week | หัวข้อ | ฝึกกับ |
|------|--------|--------|
| 1 | Android Internals + ADB Advanced | ดู AMS/PMS, เขียน dumpsys scripts |
| 2 | Proxy Stack + Scapy | สร้าง proxy rotator, validate fleet |
| 3 | Anti-Detect ทั้ง 4 Layers | เช็ค fingerprint ทุก device, TLS sniff |
| 4 | Appium/uiautomator2 vs GPF | เขียน hybrid automation |
| 5 | Bulk Management | เขียน fleet manager + dashboard |
| 6 | APK Analysis | ตรวจ 10 APPs ล่าสุดใน farm |

---

_End of PULSE Advanced Learning — Phone Automation Mastery_
