# PULSE เรียนรู้: ADB + Scapy — Phone Automation Network Stack

> **วันที่**: 2026-07-01
> **ผู้เรียน**: PULSE 📳
> **คำสั่งจาก**: JACOB 👤
> **จัดการโดย**: JIMMY 🌊

---

## Part 1: ADB (Android Debug Bridge)

### ADB คืออะไร

ADB คือสะพานเชื่อมระหว่างคอมพิวเตอร์กับอุปกรณ์ Android — เป็นเครื่องมือพื้นฐานที่สุดสำหรับ Phone Automation

```
[คอมคุณ] ←→ [ADB Server :5037] ←→ [ADB Daemon บนมือถือ]
```

**ทำไม PULSE ต้องรู้**: ทุกคำสั่งที่ GPF ส่งไปที่มือถือ — ล้วนผ่าน ADB ทั้งสิ้น การเข้าใจ ADB = การเข้าใจว่า GPF ทำงานยังไงในระดับล่าง

---

### 1.1 ติดตั้ง ADB

```bash
# Linux (WSL/Ubuntu)
sudo apt install android-tools-adb

# macOS
brew install android-platform-tools

# ตรวจสอบ
adb version
```

---

### 1.2 การเชื่อมต่อDevice

#### USB

```bash
adb devices                    # แสดงรายการ device ที่เชื่อมต่อ
# Output: R5CT1234ABCD    device

adb kill-server               # รีสตาร์ท ADB (กรณี device หาย)
adb start-server
```

#### Wi-Fi (Android 11+)

```bash
# 1. ต่อ USB ก่อน
adb tcpip 5555

# 2. ดู IP มือถือ
adb shell ip addr show wlan0 | grep "inet "

# 3. เชื่อมต่อ Wi-Fi
adb connect 192.168.1.100:5555

# 4. ถอด USB — ยังเชื่อมต่ออยู่
```

> 💡 **GPF Context**: GPF ใช้ ADB over TCP ในการควบคุมมือถือหลายเครื่องพร้อมกัน — WiFi ADB คือ backbone ของ phone farm

#### Multi-Device

```bash
adb devices -l                 # แสดงรายละเอียด device (model, transport)
adb -s <serial> shell          # ส่งคำสั่งไป device เฉพาะ
adb -s R5CT1234ABCD shell ls   # ตัวอย่าง
```

---

### 1.3 คำสั่งพื้นฐาน

#### App Management

```bash
adb install app.apk                    # ติดตั้ง APK
adb install -r app.apk                 # ติดตั้งทับ (keep data)
adb uninstall com.example.app          # ถอนการติดตั้ง
adb shell pm list packages -3          # รายชื่อแอปที่ติดตั้ง (3rd party)
adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main
adb shell am force-stop com.example.app
```

> 💡 **GPF Context**: GPF ใช้ `am start` เปิดแอป, `am force-stop` ปิดแอป, `pm list packages` ตรวจว่าแอปติดตั้งหรือยัง

#### การจำลอง Input

```bash
adb shell input tap 500 800           # แตะที่พิกัด (x, y)
adb shell input swipe 100 100 400 400 # ปัดจาก (100,100) ไป (400,400)
adb shell input text "Hello"          # พิมพ์ข้อความ
adb shell input keyevent 3            # Home button
adb shell input keyevent 4            # Back
adb shell input keyevent 26           # Power
adb shell input keyevent 66           # Enter
```

> 💡 **GPF Context**: Touch Block ใน GPF แปลงเป็น `input tap`, Swipe Block → `input swipe`, Type Text → `input text`

#### Screenshot & บันทึกหน้าจอ

```bash
adb exec-out screencap -p > screen.png           # ภาพนิ่ง
adb shell screenrecord --time-limit 10 /sdcard/demo.mp4  # วิดีโอ 10 วิ
adb pull /sdcard/demo.mp4 ./                     # ดึงไฟล์
```

> 💡 **GPF Context**: ใช้ตรวจสอบว่า automation ทำอะไรอยู่ — screenshot ก่อน/หลังแต่ละ step

#### ระบบ & Shell

```bash
adb shell                                   # เข้า shell บน device
adb shell getprop ro.build.version.sdk      # Android SDK version
adb shell getprop ro.product.model          # รุ่นมือถือ
adb shell wm size                           # ความละเอียดหน้าจอ
adb shell dumpsys battery                   # สถานะแบตเตอรี่
adb shell dumpsys meminfo com.example.app   # การใช้ RAM ของแอป
adb shell dumpsys cpuinfo | grep com.example # การใช้ CPU ของแอป
```

> 💡 **GPF Context**: `wm size` สำคัญมาก — GPF ต้องรู้ความละเอียดเพื่อคำนวณพิกัด `input tap`

#### ไฟล์

```bash
adb push local/file.txt /sdcard/            # ส่งไฟล์เข้า device
adb pull /sdcard/file.txt ./                # ดึงไฟล์ออกจาก device
adb shell ls /sdcard/Download/              # list ไฟล์
adb shell rm /sdcard/somefile.txt           # ลบไฟล์
```

---

### 1.4 Logcat — หัวใจการ Debug

```bash
adb logcat                                  # Log แบบ real-time (เยอะมาก)
adb logcat -v threadtime > log.txt          # บันทึกพร้อม timestamp
adb logcat -s TAG:I *:S                     # กรองเฉพาะ tag (I=Info)
adb logcat --pid=12345                      # กรองตาม PID
adb logcat -c                               # เคลียร์ buffer เก่า
adb logcat -b crash                         # ดู crash log
```

**ระดับ Log (จากละเอียดไปหยาบ)**:
```
V = Verbose (ทุกอย่าง)
D = Debug
I = Info
W = Warning
E = Error
F = Fatal
S = Silent (ไม่แสดงอะไร)
```

> 💡 **GPF Context**: Timeout ใน automation? เช็ค logcat ดูก่อน — รู้ทันทีว่าแอพ crashed, ANR, หรือ network error

---

### 1.5 การ Debug ขั้นสูง

#### ดูหน้าจอแบบ Real-time (scrcpy)

```bash
# ติดตั้ง
sudo apt install scrcpy

# ใช้งาน
scrcpy -s <serial>
scrcpy --max-size 1024     # ลดความละเอียด (เร็วขึ้น)
```

#### Port Forwarding

```bash
adb forward tcp:8080 tcp:8080    # Forward local:8080 → device:8080
adb reverse tcp:8080 tcp:8080    # Reverse: device:8080 → local:8080
```

> 💡 **GPF Context**: Forward ใช้ tunnel HTTP traffic — เช่น forward proxy port หรือ debug webview

---

### 1.6 ADB Cheatsheet สำหรับ GPF

| Task | Command |
|------|---------|
| เช็ค device ออนไลน์ | `adb devices` |
| เชื่อมต่อ Wi-Fi | `adb tcpip 5555 && adb connect IP:5555` |
| เปิดแอป | `adb shell am start -n <package>/<activity>` |
| แตะพิกัด | `adb shell input tap X Y` |
| ปัด | `adb shell input swipe X1 Y1 X2 Y2` |
| พิมพ์ข้อความ | `adb shell input text "..."` |
| Screenshot | `adb exec-out screencap -p > file.png` |
| ดูความละเอียด | `adb shell wm size` |
| รีบูท | `adb reboot` |
| ดู log ล่าสุด | `adb logcat -v time -d \| tail -100` |
| ติดตั้ง APK | `adb install -r app.apk` |
| เช็คแอพที่ลง | `adb shell pm list packages -3` |

---

## Part 2: Scapy — Python Packet Manipulation

### Scapy คืออะไร

Scapy คือ Python library สำหรับ **สร้าง, ส่ง, ดักจับ, วิเคราะห์** network packets — แทนที่เครื่องมืออย่าง nmap, tcpdump, Wireshark ด้วย Python code

```
[Python Script] → [Scapy] → [Raw Socket] → [Network Interface]
                                      ↓
                              [Packet Crafting]
                              [Sniffing]
                              [Analysis]
```

**ทำไม PULSE ต้องรู้**:
- 🔍 ตรวจสอบ traffic จากมือถือว่าวิ่งผ่าน proxy ถูกต้องไหม
- 🛡️ ตรวจจับ network-level blocking/bans
- 🧪 ทดสอบ proxy servers ก่อน deploy กับ farm
- 📊 วิเคราะห์ว่า automation ถูก block เพราะ network pattern หรือไม่

---

### 2.1 ติดตั้ง

```bash
pip install scapy

# Linux: ต้องมี libpcap
sudo apt install libpcap-dev
```

---

### 2.2 การ Craft & Send Packets

#### สร้าง Packet

```python
from scapy.all import *

# IP Packet
ip = IP(dst="8.8.8.8")

# TCP SYN (พื้นฐานของ port scan)
tcp = TCP(dport=80, flags="S")

# HTTP Request
http = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"

# Layer stacking: IP / TCP / Data
packet = IP(dst="93.184.216.34") / TCP(dport=80, flags="S") / http

# ส่ง packet และรอ response
response = sr1(packet, timeout=3)
if response:
    response.show()
```

**การ Stack Layers**:
```
Ether() / IP() / TCP() / "payload"
   ↓        ↓      ↓        ↓
  L2       L3     L4      L7
```

#### Craft Packet แบบต่างๆ

```python
# ICMP Ping
ping = IP(dst="8.8.8.8") / ICMP()
reply = sr1(ping, timeout=2)

# UDP
udp = IP(dst="192.168.1.1") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com"))

# ARP (หา MAC address)
arp = ARP(pdst="192.168.1.0/24")
result = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / arp, timeout=2)
```

---

### 2.3 Sniffing — ดักจับ Traffic

```python
from scapy.all import sniff

# จับทุก packet ที่ผ่าน eth0
sniff(iface="eth0", count=10)

# จับเฉพาะ HTTP
sniff(filter="tcp port 80", count=5)

# จับพร้อม callback — ประมวลผล real-time
def handle_packet(pkt):
    if IP in pkt:
        print(f"{pkt[IP].src} → {pkt[IP].dst}")

sniff(iface="eth0", prn=handle_packet, count=100)

# จับแล้วบันทึกเป็น pcap
packets = sniff(timeout=30)
wrpcap("capture.pcap", packets)

# อ่าน pcap กลับมา
packets = rdpcap("capture.pcap")
for pkt in packets:
    pkt.show()
```

---

### 2.4 การวิเคราะห์ Traffic จาก Phone Farm

#### ตรวจสอบว่า Traffic ผ่าน Proxy ไหม

```python
from scapy.all import *

def check_proxy_traffic(interface="eth0", target_port=8080):
    """ตรวจสอบว่ามี traffic วิ่งผ่าน proxy จริงหรือไม่"""
    
    def analyze(pkt):
        if IP in pkt and TCP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            dst_port = pkt[TCP].dport
            
            if dst_port == target_port:
                print(f"✅ Proxy Traffic: {src_ip} → {dst_ip}:{dst_port}")
            elif dst_port in [80, 443]:
                non_proxy = pkt.summary()
                print(f"⚠️  Direct Traffic: {src_ip} → {dst_ip}:{dst_port}")
    
    print(f"🔍 Monitoring traffic on {interface}...")
    sniff(iface=interface, prn=analyze, count=50)

# ใช้งาน
check_proxy_traffic("eth0", 8080)
```

#### ตรวจจับ Connection Reset (Block Detection)

```python
def detect_blocks(interface="eth0"):
    """ตรวจจับ RST packets — สัญญาณของ block/ban"""
    
    def check_rst(pkt):
        if TCP in pkt and pkt[TCP].flags & 0x4:  # RST flag
            print(f"🚨 RST Detected: {pkt[IP].src}:{pkt[TCP].sport} → {pkt[IP].dst}:{pkt[TCP].dport}")
    
    sniff(iface=interface, prn=check_rst, filter="tcp[tcpflags] & tcp-rst != 0")

# ใช้งาน
detect_blocks("eth0")
```

#### วิเคราะห์ TLS Handshake

```python
def analyze_tls():
    """ดูว่า TLS handshake สำเร็จหรือไม่"""
    
    def check_tls(pkt):
        if TCP in pkt and pkt.haslayer(Raw):
            payload = bytes(pkt[Raw])
            # TLS ClientHello เริ่มด้วย 0x16 0x03
            if len(payload) > 2 and payload[0] == 0x16 and payload[1] == 0x03:
                print(f"🔐 TLS: {pkt[IP].src} → {pkt[IP].dst}")
                if hasattr(pkt[TCP], 'dport') and pkt[TCP].dport == 443:
                    print(f"   ✅ Standard HTTPS")
    
    sniff(prn=check_tls, count=20)
```

---

### 2.5 Use Cases สำหรับ Phone Farm

| Use Case | ใช้ Scapy ยังไง | ทำไมสำคัญ |
|----------|---------------|----------|
| **Proxy Validation** | Sniff traffic → เช็คว่าทุก packet ไปผ่าน proxy | มือถือหลุด proxy = IP จริงหลุด = แบนทั้ง farm |
| **Block Detection** | ตรวจจับ RST / Timeout pattern | รู้ก่อนว่ากำลังจะโดนแบน → หยุด automation |
| **Latency Monitoring** | วัด RTT จาก SYN → SYN-ACK | Proxy ช้า → automation timeout |
| **DNS Analysis** | ตรวจจับ DNS leak | DNS รั่ว = ISP เห็นว่ามาจาก farm |
| **Traffic Pattern** | ดู interval ระหว่าง packets | Pattern เหมือนคนจริง = ไม่โดนจับ |

---

### 2.6 ForwardMachine (ใหม่! v2.7.0)

ForwardMachine คือ TCP proxy ที่แก้ไข packet ได้แบบ real-time — มีประโยชน์มากสำหรับ GPF:

```python
from scapy.all import *

class GPFProxy(ForwardMachine):
    """TCP Proxy สำหรับ phone farm — 
    แก้ไข User-Agent, ตรวจสอบ traffic pattern"""
    
    def server_parse(self, data, s2c=None):
        # ดักจับ response จาก server → phone
        # ตรวจสอบว่า server ส่ง block page กลับมาไหม
        if b"Access Denied" in data or b"429" in data:
            print(f"🚨 BLOCK DETECTED: {self.addr}")
            # หยุด automation ใน device นี้
        return data
    
    def client_parse(self, data, s2c=None):
        # ดักจับ request จาก phone → server
        # แก้ไข User-Agent, headers
        if b"User-Agent: Dalvik" in data:
            data = data.replace(b"Dalvik/2.1.0", b"Chrome/120.0")
            print(f"🔧 Modified UA for {self.addr}")
        return data

# ใช้งาน
proxy = GPFProxy()
proxy.serve(("0.0.0.0", 8888))
```

---

### 2.7 Scapy Tools สำหรับ GPF Ops

```python
#!/usr/bin/env python3
"""gpf-network-tools.py — Network diagnostics for GemphoneFarm"""

from scapy.all import *
import sys

def test_proxy(proxy_ip, proxy_port, test_url="google.com"):
    """ทดสอบว่า proxy ทำงานหรือไม่"""
    syn = IP(dst=proxy_ip) / TCP(dport=proxy_port, flags="S")
    response = sr1(syn, timeout=3, verbose=0)
    
    if response and response.haslayer(TCP) and response[TCP].flags & 0x12:  # SYN-ACK
        print(f"✅ Proxy {proxy_ip}:{proxy_port} is UP")
        # ส่ง RST เพื่อปิด connection
        rst = IP(dst=proxy_ip) / TCP(dport=proxy_port, flags="R")
        send(rst, verbose=0)
        return True
    else:
        print(f"❌ Proxy {proxy_ip}:{proxy_port} is DOWN")
        return False

def dns_leak_test(dns_server="8.8.8.8"):
    """ตรวจสอบ DNS Leak — DNS request ควรไปผ่าน proxy ไม่ใช่ตรงๆ"""
    print(f"🔍 Sending test DNS query to {dns_server}...")
    dns_req = IP(dst=dns_server) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="whoami.dnsleaktest.com"))
    response = sr1(dns_req, timeout=3, verbose=0)
    
    if response:
        print(f"⚠️  DNS Leak Possible — response from {dns_server}")
    else:
        print(f"✅ DNS blocked — traffic likely going through proxy")

def device_connectivity_check(device_ip):
    """เช็คว่า device ออนไลน์ผ่าน Wi-Fi ADB หรือไม่"""
    tcp_syn = IP(dst=device_ip) / TCP(dport=5555, flags="S")
    response = sr1(tcp_syn, timeout=2, verbose=0)
    
    if response and response.haslayer(TCP) and response[TCP].flags & 0x12:
        print(f"✅ Device {device_ip}:5555 — ADB reachable")
        send(IP(dst=device_ip) / TCP(dport=5555, flags="R"), verbose=0)  # RST
        return True
    else:
        print(f"❌ Device {device_ip}:5555 — ADB unreachable")
        return False

if __name__ == "__main__":
    # ตัวอย่าง: python gpf-network-tools.py proxy 192.168.1.1 8080
    if sys.argv[1] == "proxy":
        test_proxy(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "dns":
        dns_leak_test()
    elif sys.argv[1] == "device":
        device_connectivity_check(sys.argv[2])
```

---

## 📊 สรุป: ADB + Scapy = Phone Automation Stack

```
┌─────────────────────────────────────────────┐
│                  PULSE 📳                    │
│                                              │
│  ADB Layer          Scapy Layer              │
│  ─────────          ───────────              │
│  • device control   • traffic sniffing       │
│  • input simulate   • proxy validation       │
│  • app management   • block detection        │
│  • logcat debug     • DNS leak check         │
│  • file push/pull   • latency monitoring     │
│  • screen capture   • packet crafting        │
│       ↓                    ↓                 │
│  [Android Phones]   [Network/Proxy Layer]    │
│       ↓                    ↓                 │
│  GPF High-Level Automation                   │
└─────────────────────────────────────────────┘
```

---

## 🎯 ขั้นตอนเรียนรู้

| ขั้น | หัวข้อ | ใช้เวลา | ฝึกกับ |
|------|--------|--------|--------|
| 1 | ADB — ติดตั้ง + เชื่อมต่อ device | 1 ชม. | มือถือจริง 1 เครื่อง |
| 2 | ADB — input tap/swipe/text | 2 ชม. | เขียน script เปิด TikTok |
| 3 | ADB — logcat + debugging | 2 ชม. | จับ log ตอน automation รัน |
| 4 | Scapy — ติดตั้ง + สร้าง packet แรก | 1 ชม. | ping, TCP SYN |
| 5 | Scapy — sniff + วิเคราะห์ traffic | 2 ชม. | จับ traffic จากมือถือ |
| 6 | Scapy — proxy validation tool | 2 ชม. | ทดสอบกับ proxy farm |
| 7 | Integration — ADB + Scapy debug | 3 ชม. | Debug automation จริง |

---

## 🔗 แหล่งเรียนรู้

- **ADB Official**: https://developer.android.com/studio/command-line/adb
- **ADB Cheatsheet**: https://devhints.io/adb
- **Scapy Docs**: https://scapy.readthedocs.io/
- **Scapy GitHub**: https://github.com/secdev/scapy
