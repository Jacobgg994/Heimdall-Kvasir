# PULSE Mastery Batch 2 — Advanced Phone Farm Ops

> **วันที่**: 2026-07-01
> **ผู้เรียน**: PULSE 📳
> **6 หัวข้อ**: Frida → Magisk → MQTT → SQLite → Ansible/Fleet → Platform Anti-Bot

---

## 7. Frida — Dynamic Instrumentation

### Frida คืออะไร

Frida คือ toolkit สำหรับ **inject code เข้าไปใน app ตอนรัน** — โดยไม่ต้องมี source code

**ใช้กับ GPF**:
- 🔓 Bypass SSL Pinning → ดู traffic ที่เข้ารหัส
- 🕵️ Hook API calls → รู้ว่า app เรียกอะไร ตอนไหน
- 🛡️ Bypass root detection → app คิดว่าไม่ได้ root
- 🐛 Debug automation failure → ดูว่า app ส่ง request อะไรก่อน timeout

### ติดตั้ง

```bash
pip install frida-tools objection

# บน Android — ติดตั้ง frida-server
adb push frida-server-16.x.x-android-arm64 /data/local/tmp/
adb shell chmod 755 /data/local/tmp/frida-server-16.x.x-android-arm64
adb shell /data/local/tmp/frida-server-16.x.x-android-arm64 &
```

### Bypass SSL Pinning

```javascript
// ssl-bypass.js — ใช้กับ GPF ตอน debug network
Java.perform(function() {
    var TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    TrustManager.checkServerTrusted.implementation = function(chain, authType) {
        console.log('[+] SSL Pinning BYPASSED');
        return; // Accept all certs
    };
});
```

```bash
frida -U -l ssl-bypass.js -f com.zhiliaoapp.musically
```

### Objection — เร็วกว่าเขียน Frida เอง

```bash
# Bypass SSL ทันที — ไม่ต้องเขียนโค้ด
objection -g com.zhiliaoapp.musically explore
# ใน objection console:
> android sslpinning disable
> android root disable
```

### Hook API — เห็นว่า app ทำอะไร

```javascript
// Hook OkHttp — เห็นทุก HTTP request
Java.perform(function() {
    var OkHttpClient = Java.use('okhttp3.OkHttpClient');
    var Request = Java.use('okhttp3.Request');
    
    Request.newBuilder.implementation = function() {
        console.log('[+] New HTTP Request');
        return this.newBuilder();
    };
});
```

### GPF Use Case — Debug Automation Failure

```
1. GPF tap "ติดตาม" → Timeout 15 วิ
2. เปิด Frida → Hook OkHttp
3. เห็นว่า app ส่ง POST /api/follow → response 403
4. สรุป: ไม่ใช่ UI bug — โดน rate limit
5. Fix: เพิ่ม delay / เปลี่ยน proxy
```

---

## 8. Magisk + Root + Hide

### The Stack — Root โดยที่ app ไม่รู้

```
Layer 1: Magisk (root manager)
Layer 2: Zygisk (inject into Zygote)
Layer 3: Shamiko (hide root from apps)
Layer 4: PIFork / PIF Inject (pass Play Integrity)
Layer 5: Tricky Store (hardware attestation bypass)
```

### Magisk Modules ที่ GPF ต้องใช้

| Module | Purpose |
|--------|---------|
| **Shamiko** | ซ่อน root จาก TikTok/FB/Banking apps |
| **PIF Inject** | Pass DEVICE_INTEGRITY |
| **Sensitive Props** | ล้าง custom ROM traces |
| **Systemless Hosts** | Block tracking domains |

### ติดตั้ง Magisk

```bash
# 1. ดึง boot.img จาก device
adb shell su -c "dd if=/dev/block/by-name/boot of=/sdcard/boot.img"
adb pull /sdcard/boot.img

# 2. Patch ด้วย Magisk app
# (ทำบน device: Magisk → Install → Select and Patch a File → boot.img)

# 3. Flash กลับ
adb reboot bootloader
fastboot flash boot magisk_patched.img
fastboot reboot

# 4. ตรวจสอบ
adb shell su -c "magisk -c"
```

### ซ่อน Root

```bash
# 1. เปิด Zygisk (Magisk settings)
# 2. ติดตั้ง Shamiko module
# 3. Configure DenyList — เลือก app ที่ต้องการซ่อน root
# 4. อย่า enforce DenyList — Shamiko จัดการให้
```

### Fingerprint Spoofing

```bash
# PIF Inject — ใช้ autopif.sh หา fingerprint ที่ใช้ได้
# 1. ติดตั้ง PIF Inject module
# 2. adb shell
# 3. su -c "autopif2.sh"
# 4. รีบูท → เช็ค Play Store → Settings → About → Play Protect certification
```

### GPF Checklist ต่อ Device

```
✅ Magisk + Zygisk
✅ Shamiko (hide root)
✅ PIF Inject (pass integrity)
✅ DenyList: TikTok, FB, LINE, Banking apps
✅ Play Store → Certified
✅ SafetyNet/Play Integrity → PASS
```

---

## 9. MQTT + Webhook — Cloud Trigger

### MQTT Architecture สำหรับ GPF

```
[Cloud Dashboard] → MQTT Publish → [MQTT Broker (EMQX/HiveMQ)]
                                          ↓
                              [Device 1] [Device 2] ... [Device N]
                              (subscribe)  (subscribe)    (subscribe)
```

**MQTT 5.0 Features (2026)**:
- Shared Subscriptions — load balance งานให้ devices
- Request-Response — สั่งงาน + รอผล
- TLS 1.3 — encryption

### GPF Cloud Webhook Integration

GPF มี cloud webhook ผ่าน MQTT — device รับคำสั่งจาก cloud ได้ real-time:

```python
# pulse-cloud-trigger.py
import paho.mqtt.client as mqtt
import json

BROKER = "broker.emqx.io"
TOPIC_PREFIX = "gpf/farm-01"

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    device = payload.get("device")
    action = payload.get("action")
    
    if action == "start_automation":
        print(f"📱 Starting {payload['workflow']} on {device}")
        # Trigger GPF via local API หรือ ADB
    elif action == "stop":
        print(f"🛑 Stopping {device}")
    elif action == "health_check":
        print(f"🩺 Health check {device}")

client = mqtt.Client(client_id="pulse-controller")
client.on_message = on_message
client.connect(BROKER, 1883)
client.subscribe(f"{TOPIC_PREFIX}/+/command")
client.loop_forever()
```

### Webhook → LINE Notification

```python
# เมื่อ device เจอปัญหา → แจ้ง LINE
import requests

def notify_line(message):
    webhook_url = "https://hooks.slack.com/..."  # หรือ LINE Notify
    requests.post(webhook_url, json={"text": message})

# ใน MQTT handler:
if payload.get("error"):
    notify_line(f"🚨 Device {device}: {payload['error']}")
```

### Real-Time Dashboard via MQTT

```python
# MQTT → SQLite → Streamlit Dashboard (Real-time)
# ทุก device report status ทุก 30 วิ via MQTT
# Pulse Dashboard แสดงผล real-time

# Device reports:
{
    "device": "R5CT1234ABCD",
    "status": "running",
    "workflow": "tiktok-like-share",
    "battery": 78,
    "cpu": 35,
    "memory": 1200,
    "last_action": "tap_follow",
    "timestamp": "2026-07-01T12:00:00Z"
}
```

---

## 10. SQLite — ฐานข้อมูลเบื้องหลัง GPF

### GPF ใช้ SQLite ยังไง

GPF ใช้ SQLite สำหรับ:
- **Workflow Storage** — ทุก .GemPhoneFarm workflow
- **Execution Log** — ทุก action ที่เคยรัน
- **Device State** — variables, counters
- **Cookie/Token Storage** — session data

### Quick SQLite Commands

```bash
# เช็ค database
sqlite3 /path/to/gpf.db

# ดูตารางทั้งหมด
.tables

# Schema
.schema workflows

# Stats
SELECT COUNT(*) FROM workflows;
SELECT COUNT(*) FROM execution_logs WHERE created_at > date('now', '-7 days');

# Health Check
PRAGMA integrity_check;
PRAGMA quick_check;
PRAGMA journal_mode;     # ควรเป็น 'wal'
PRAGMA foreign_key_check;
```

### WAL Mode — ต้องเปิด

```sql
-- WAL = Write-Ahead Logging
-- ดีกว่า default 'delete' mode เพราะ:
-- readers ไม่ block writers, writers ไม่ block readers
PRAGMA journal_mode=WAL;

-- ตั้งค่า performance
PRAGMA cache_size = -64000;  -- 64MB cache
PRAGMA mmap_size = 268435456; -- 256MB memory-mapped I/O
PRAGMA synchronous = NORMAL;  -- ปลอดภัยพอ เร็วขึ้น
PRAGMA temp_store = MEMORY;
PRAGMA busy_timeout = 5000;   -- รอ 5 วิแทน crash
```

### Query Optimization

```sql
-- ดูว่าใช้ index หรือไม่
EXPLAIN QUERY PLAN SELECT * FROM execution_logs WHERE device_id = 'xxx';

-- ถ้าเห็น SCAN TABLE → สร้าง index
CREATE INDEX IF NOT EXISTS idx_exec_device ON execution_logs(device_id);
CREATE INDEX IF NOT EXISTS idx_exec_created ON execution_logs(created_at);

-- วิเคราะห์ query performance
ANALYZE;
PRAGMA optimize;
```

### Repair Corrupted DB

```bash
# ถ้า GPF database corrupt
# Step 1: Backup
cp gpf.db gpf.db.backup

# Step 2: Export all data
sqlite3 gpf.db ".dump" > gpf_dump.sql

# Step 3: Import ไป database ใหม่
sqlite3 gpf_new.db < gpf_dump.sql

# Step 4: ตรวจสอบ
sqlite3 gpf_new.db "PRAGMA integrity_check;"

# Step 5: Replace
mv gpf_new.db gpf.db
```

### GPF-Specific SQL Queries

```sql
-- ดู workflow ที่ fail บ่อยสุด
SELECT workflow_name, COUNT(*) as fails
FROM execution_logs
WHERE status = 'failed' AND created_at > date('now', '-7 days')
GROUP BY workflow_name
ORDER BY fails DESC
LIMIT 10;

-- ดู device ที่ timeout บ่อยสุด
SELECT device_id, COUNT(*) as timeouts
FROM execution_logs
WHERE error_type = 'timeout' AND created_at > date('now', '-3 days')
GROUP BY device_id
ORDER BY timeouts DESC;

-- Average execution time ต่อ workflow
SELECT workflow_name, AVG(execution_time_ms) as avg_ms
FROM execution_logs
WHERE status = 'success'
GROUP BY workflow_name;
```

---

## 11. Fleet Provisioning — Infrastructure as Code

### Ansible + ADB = Fleet at Scale

```yaml
# pulse-fleet-playbook.yml
- name: Provision Android Fleet
  hosts: phone_farm
  vars:
    apps_to_install:
      - tiktok
      - facebook
      - line
      - proxy_droid
    proxy_server: "proxy.example.com:8080"
    
  tasks:
    - name: Check device online
      command: adb -s {{ inventory_hostname }} shell echo "online"
      register: device_check
      
    - name: Set proxy
      command: adb -s {{ inventory_hostname }} shell settings put global http_proxy {{ proxy_server }}
      when: device_check.stdout == "online"
      
    - name: Install apps
      command: adb -s {{ inventory_hostname }} install -r /apps/{{ item }}.apk
      loop: "{{ apps_to_install }}"
      when: device_check.stdout == "online"
      
    - name: Disable animations (speed up)
      command: adb -s {{ inventory_hostname }} shell settings put global window_animation_scale 0.0
      
    - name: Set locale to Thai
      command: adb -s {{ inventory_hostname }} shell "setprop persist.sys.locale th-TH"
```

### inventory.ini

```ini
[phone_farm]
192.168.1.101
192.168.1.102
192.168.1.103
# ... 60 devices
```

### Zero-Touch Provisioning Script

```python
#!/usr/bin/env python3
"""pulse-provision.py — ตั้งค่า device ใหม่ภายใน 3 นาที"""

STEPS = [
    ("Root Check", "adb shell su -c id"),
    ("Set Proxy", "adb shell settings put global http_proxy {proxy}"),
    ("Disable Animations", "adb shell settings put global window_animation_scale 0.0"),
    ("Set Thai Locale", "adb shell setprop persist.sys.locale th-TH"),
    ("Set Timezone", "adb shell settings put global time_zone Asia/Bangkok"),
    ("Install TikTok", "adb install -r apps/tiktok.apk"),
    ("Install Facebook", "adb install -r apps/facebook.apk"),
    ("Install ProxyDroid", "adb install -r apps/proxydroid.apk"),
    ("Disable OTA", "adb shell pm disable-user com.google.android.gms/.chimera.GmsIntentOperationService"),
    ("Verify", "adb shell getprop ro.product.model"),
]

def provision(serial, proxy):
    print(f"📱 Provisioning {serial}...")
    for name, cmd in STEPS:
        cmd = cmd.format(proxy=proxy)
        result = subprocess.run(
            ['adb', '-s', serial] + cmd.split(),
            capture_output=True, timeout=30
        )
        status = "✅" if result.returncode == 0 else "❌"
        print(f"  {status} {name}")
```

---

## 12. Platform Anti-Bot — TikTok / Shopee / Lazada

### TikTok Shop Detection (2026)

| Layer | สิ่งที่ตรวจ | GPF ต้องทำ |
|-------|-----------|-----------|
| **Device** | IMEI, MAC, Android ID, build fingerprint | Fingerprint ตรงกับ model จริง |
| **Network** | IP segment, DNS timezone, ASN, exit node | Static residential IP ตรงประเทศ |
| **Location** | GPS, base station, Wi-Fi fingerprint | GPS mock ให้ตรง IP |
| **Behavioral** | Browse path, click rhythm, post timing | Randomized delay, varied path |

**กฎเหล็ก**: ถ้า behavioral similarity >60% ระหว่าง 2 accounts → flagged as associated

### Shopee Detection

| Layer | สิ่งที่ตรวจ | GPF ต้องทำ |
|-------|-----------|-----------|
| **Network** | IP, DNS, router MAC | 1 device = 1 IP |
| **Registration** | เลขทะเบียนพาณิชย์, บัตรประชาชน, เบอร์, อีเมล | ไม่ซ้ำข้ามร้าน |
| **Operations** | CS script, operating time overlap | Randomize ทุกอย่าง |

### Anti-Bot Defense Strategy

```python
# pulse-anti-bot.py — Randomized Operations
import random, time

class AntiBotOps:
    def __init__(self):
        self.last_action_time = {}
        self.action_counts = {}
    
    def random_delay(self, device_id, min_ms=500, max_ms=3000):
        """หน่วงเวลาแบบสุ่ม — ไม่ให้เหมือนกันทุก device"""
        delay = random.randint(min_ms, max_ms) / 1000
        # เพิ่ม jitter ตาม device — แต่ละเครื่องไม่เท่ากัน
        device_jitter = hash(device_id) % 500
        delay += device_jitter / 1000
        time.sleep(delay)
    
    def should_act(self, device_id, max_per_hour=20):
        """Rate limiter — ไม่ให้ action ถี่เกิน"""
        now = time.time()
        if device_id not in self.action_counts:
            self.action_counts[device_id] = []
        
        # ลบ actions เก่า (>1 ชม.)
        self.action_counts[device_id] = [
            t for t in self.action_counts[device_id] if now - t < 3600
        ]
        
        if len(self.action_counts[device_id]) >= max_per_hour:
            return False
        
        self.action_counts[device_id].append(now)
        return True
    
    def varied_path(self, target_action):
        """ทำทางอ้อมก่อนถึงเป้าหมาย — เหมือนคนจริง"""
        paths = [
            [],  # ตรงๆ — 10%
            ["scroll_feed", "pause", "scroll_feed"],  # เลื่อน feed — 40%
            ["scroll_feed", "like_random", "scroll_feed"],  # like ระหว่างทาง — 30%
            ["scroll_feed", "watch_video", "scroll_feed", "pause"],  # ดูคลิป — 20%
        ]
        weights = [10, 40, 30, 20]
        path = random.choices(paths, weights=weights, k=1)[0]
        path.append(target_action)
        return path
    
    def device_fingerprint_check(self, serial):
        """ตรวจ fingerprint ก่อนรัน automation"""
        import subprocess
        model = subprocess.run(
            ['adb', '-s', serial, 'shell', 'getprop', 'ro.product.model'],
            capture_output=True, text=True
        ).stdout.strip()
        
        fingerprint = subprocess.run(
            ['adb', '-s', serial, 'shell', 'getprop', 'ro.build.fingerprint'],
            capture_output=True, text=True
        ).stdout.strip()
        
        # เช็คว่า model กับ fingerprint ตรงกัน
        if model.lower() not in fingerprint.lower():
            return f"⚠️ {serial}: fingerprint mismatch — {model} vs {fingerprint}"
        return f"✅ {serial}: fingerprint OK"
```

### Platform Comparison for GPF

| Factor | TikTok | Shopee | Lazada |
|--------|--------|--------|--------|
| Detection Aggressiveness | 🔴 สูงมาก | 🟡 ปานกลาง | 🟢 ต่ำ |
| IP Sensitivity | 🔴 Static Residential required | 🟡 Residential preferred | 🟢 Proxy OK |
| Behavioral Analysis | 🔴 >60% similarity = ban | 🟡 Moderate | 🟢 Light |
| Account Warm-up | 🔴 7+ วัน | 🟡 3-5 วัน | 🟢 1-2 วัน |
| Best Proxy Type | Static Residential IPv6 | Residential | Datacenter OK |

---

## 📊 PULSE Complete Knowledge Map

```
                           PULSE 📳
                              │
        ┌──────────┬──────────┼──────────┬──────────┐
        │          │          │          │          │
     📱 ADB    🌐 Network  🛡️ Stealth  🔧 Tools  📊 Ops
     ────────  ──────────  ──────────  ────────  ────────
     Android    Scapy      Frida       SQLite    Fleet
     AMS/PMS    Proxy      Magisk      MQTT      Provision
     uiauto2    SOCKS5     TLS/JA4     Streamlit Ansible
     APK        DNS Leak   Platform    Dashboard Platform
     Analysis   Validator  Anti-Bot    GPF DB    Anti-Bot
        │          │          │          │          │
        └──────────┴──────────┴──────────┴──────────┘
                              │
                     GPF Master Operations
```

---

## 🎯 Batch 2 Learning Path

| Week | หัวข้อ | Practice |
|------|--------|----------|
| 7 | Frida | Hook 1 app, bypass SSL, ดู HTTP traffic |
| 8 | Magisk | Root 1 device, hide root from TikTok, pass Integrity |
| 9 | MQTT | Set up broker, pub/sub, trigger workflow from cloud |
| 10 | SQLite | Query GPF db, optimize, create indexes |
| 11 | Fleet Provision | เขียน playbook, provision 3 devices |
| 12 | Platform Anti-Bot | Implement randomization, test detection |

---

_End of PULSE Mastery Batch 2_
