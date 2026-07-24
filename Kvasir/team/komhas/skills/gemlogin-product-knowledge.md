---
name: gemlogin-product-knowledge
description: ความรู้เกี่ยวกับผลิตภัณฑ์ GemLogin และ GemPhoneFarm — Anti-Detect Browser, Mobile Automation, GemStore Marketplace
metadata:
  type: skill
  category: marketing
  product: gemlogin
---

# GemLogin Product Knowledge

## 1. ภาพรวมผลิตภัณฑ์

### 1.1 GemLogin — Anti-Detect Browser
GemLogin เป็น **Anti-Detect Browser (ADB)** ที่พัฒนาโดยบริษัท ควิล ซอฟต์แวร์ จำกัด (Quill Software Co., Ltd.) จากประเทศไทย ออกแบบมาเพื่อ:
- จัดการหลายบัญชีบนแพลตฟอร์มต่าง ๆ พร้อมกัน (Facebook, TikTok, Instagram, Lazada)
- ปกปิดลายนิ้วมือดิจิทัล (Digital Fingerprint) ป้องกันการถูกตรวจจับ
- ทำงานอัตโนมัติผ่านระบบ Workflow แบบลากแล้ววาง (No-Code Visual Builder)
- รองรับทั้ง Local Storage และ Cloud Storage

**ข้อเท็จจริง:** จาก GemLogin Manual หน้าแรก ระบุว่า GemLogin คือ "เครื่องมือ Anti-Detect Browser ที่ช่วยให้การทำงานออนไลน์ของคุณเป็นไปอย่างราบรื่นและปลอดภัย ด้วยการปรับแต่ง User-Agent และใช้ Proxy IP" (ที่มา: https://manual.gemlogin.io/)

**ข้อมูลจำเพาะทางเทคนิค:**
| Metric | ค่า |
|--------|-----|
| CPU ต่อโปรไฟล์ | ~2.3% |
| RAM ต่อโปรไฟล์ | ~180 MB |
| เวลาเปิดโปรไฟล์ | ~2.1 วินาที |
| Concurrent threads | 5-50 (ขึ้นอยู่กับแพ็กเกจ) |
| OS ที่รองรับ | Windows, macOS |

### ราคา (Local Storage) — อ้างอิงจาก gemlogin.io

| แพ็กเกจ | ราคา | โปรไฟล์ | อายุ |
|---------|------|---------|------|
| **Free** | ฿0 | 5 | ตลอดชีพ |
| **GEM50** | ฿280 | 50 | 30 วัน |
| **GEM200** | ฿450 | 200 | 30 วัน |
| **GEM500** | ฿490 | 500 | 30 วัน |
| **GEM1000** | ฿520 | 1,000 | 30 วัน |
| **Unlimited 1M** | ฿700 | ไม่จำกัด | 1 เดือน |
| **Unlimited 6M** | ฿3,500 | ไม่จำกัด | 6 เดือน |
| **Unlimited 1Y** | ฿4,200 | ไม่จำกัด | 1 ปี |
| **Forever** | ฿4,900 | ไม่จำกัด | ตลอดชีพ |

> จ่ายรายปีลด 50%

### ราคา (Cloud Storage)

| แพ็กเกจ | ราคา USD/เดือน | โปรไฟล์ | Threads |
|---------|----------------|---------|---------|
| **Starter** | $19 | 10 | 5 |
| **Professional** | $99 | 100 | 25 |
| **Enterprise** | Custom | ไม่จำกัด | 50 |

### ภาษา

| ด้าน | รายละเอียด |
|------|-----------|
| **Software UI** | อังกฤษ — **ไม่มี UI ภาษาไทย** |
| **คู่มือ** | มีคู่มือภาษาไทย (manual.gemlogin.io) |
| **ทีมซัพพอร์ต** | คนไทย — ติดต่อผ่าน LINE OA (@gemlogin) |
| **Content การตลาด** | ภาษาไทย — Facebook, TikTok, LINE, YouTube |

### 1.2 GemPhoneFarm — Mobile Automation
GemPhoneFarm เป็นเครื่องมือสำหรับ:
- ควบคุมมือถือ Android แบบอัตโนมัติ
- รองรับ LDPlayer (Android Emulator), มือถือ Android จริง, และ BoxPhone
- จัดการหลายบัญชีบนแพลตฟอร์มมือถือ (Facebook App, TikTok App, Instagram App, Lazada App)
- ใช้ ATX-Agent Server เป็นตัวกลางในการควบคุมอุปกรณ์ผ่าน ADB

**ข้อเท็จจริง:** จาก GemLogin Manual หน้าแรก GemPhoneFarm คือ "เครื่องมือที่ช่วยในการทำงานอัตโนมัติบนแพลตฟอร์มต่างๆ โดยรองรับการจัดการหลายบัญชีพร้อมกันผ่านการควบคุม LDPlayer, มือถือแอนดรอย หรือ BoxPhone" (ที่มา: https://manual.gemlogin.io/)

### 1.3 Automation Companion Suite
ชุดเครื่องมือเสริมสำหรับการทำงานอัตโนมัติ:
- **90+ Command Blocks** สำหรับ GemLogin (Browser, Web Interaction, Data, Control Flow, General, Online Services)
- **80+ Command Blocks** สำหรับ GemPhoneFarm (UI Interaction, Device Management, App Management, System Command)
- **Gem Agent** — AI-assisted automation
- **Record Function** — บันทึกการกระทำและแปลงเป็น Workflow
- **Multiple Profile Runner** — รันสคริปต์พร้อมกันหลายโปรไฟล์

**การตีความทางการตลาด:** GemLogin ไม่ใช่แค่ Anti-Detect Browser ทั่วไป แต่เป็น "Platform Complete" ที่รวมทั้ง Browser Fingerprint Protection + Automation Engine + Marketplace + Cloud Sync ในที่เดียว คู่แข่งส่วนใหญ่มีแค่ Anti-Detect อย่างเดียว

---

## 2. กลุ่มเป้าหมาย (Target Personas)

### PERSONA 1: นักการตลาด Affiliate (Affiliate Marketer)
- **ลักษณะ:** ทำ CPA Marketing, สร้างแคมเปญโฆษณาหลายบัญชี
- **ความต้องการ:** จัดการ 50-500+ บัญชี, หลบ Detection, ทำงานอัตโนมัติ
- **痛点:** ถูกแบนบ่อย, ใช้เวลาเปิด/ปิดบัญชีนาน
- **แพ็กเกจที่เหมาะ:** GEM200 (฿450/เดือน) ถึง Unlimited (฿700/เดือน)
- **GemPhoneFarm:** ควบคุมบัญชีบนมือถือ, คอมเมนต์อัตโนมัติ

### PERSONA 2: เจ้าของธุรกิจ E-Commerce (E-commerce Operator)
- **ลักษณะ:** ขายของหลายร้านบน Shopee/Lazada/TikTok Shop
- **ความต้องการ:** จัดการหลายร้าน, ตรวจสอบราคาคู่แข่ง, รีวิวปลอม
- **痛点:** โดนแบนร้าน, ติดตามราคาคู่แข่งไม่ทัน
- **แพ็กเกจที่เหมาะ:** GEM500 หรือ Cloud Storage (ทีม)
- **ฟีเจอร์ที่ใช้:** Automation Workflow, Data Mapping, Loop

### PERSONA 3: นักพัฒนา Script (Developer)
- **ลักษณะ:** เขียนโค้ด ทำ Automation Script ขาย
- **ความต้องการ:** SDK ที่ดี, ขายของบน Marketplace ได้
- **痛点:** ไม่มีช่องทางขายสคริปต์, ต้องหาลูกค้าเอง
- **รายได้:** 70% Revenue Share จาก GemStore
- **จุดขาย:** Developer Friendly, Free SDK, มี Docs ครบ

### PERSONA 4: ทีมเอเจนซี่ (Enterprise Team)
- **ลักษณะ:** เอเจนซี่ดิจิทัลที่ดูแลลูกค้าหลายราย, มีพนักงานหลายคน
- **ความต้องการ:** Role-Based Access, Audit Log, Profile Sharing
- **痛点:** จัดการทีมไม่สะดวก, ไม่มี Cloud Sync
- **แพ็กเกจที่เหมาะ:** Cloud Storage (ทีม), Enterprise
- **ฟีเจอร์ที่ใช้:** ระบบ Cloud, RBAC, Encrypted Profile Sharing

### PERSONA 5: นักเล่นเกม/ฟาร์มเกม (Gamer/Farmer)
- **ลักษณะ:** ฟาร์มไอเทมในเกม, ทำ RMT, หลายบัญชี (BoxPhone)
- **ความต้องการ:** ควบคุมมือถือหลายเครื่องพร้อมกัน
- **แพ็กเกจที่เหมาะ:** GemPhoneFarm + BoxPhone
- **ฟีเจอร์ที่ใช้:** 80+ มือถือ Command Blocks

---

## 3. ช่องทางการติดต่อ GemLogin

| ช่องทาง | รายละเอียด |
|---------|-----------|
| LINE Official | @gemlogin หรือ @909kaiyh |
| Facebook | facebook.com/profile.php?id=61579265128834 |
| Instagram | @gemlogin.th |
| TikTok | @gemloginthailand |
| X (Twitter) | @GemloginTH |
| YouTube | @Gemlogin-TH |
| Telegram | @GemLogin_TH |
| เว็บไซต์ | https://gemlogin.io |
| License Manager | https://app.gemlogin.io |
| GemStore | https://store.gemlogin.io |
| Manual | https://manual.gemlogin.io |
| Blog | https://blog.gemlogin.io |

(ที่มา: https://manual.gemlogin.io/information/contact-us.md)

---

## 4. Feature Matrix: GemLogin vs ฟรี

| ฟีเจอร์ | Free Plan | Paid Plan |
|---------|-----------|-----------|
| จำนวนโปรไฟล์ | 5 | 50 - ไม่จำกัด |
| Anti-Detect Fingerprint | ใช่ | ใช่ (ครบถ้วนกว่า) |
| Proxy ต่่อโปรไฟล์ | ใช่ | ใช่ |
| Cloud Sync | ไม่ | ใช่ (Cloud Storage) |
| Automation | Limited | Full 90+ Blocks |
| GemStore | เฉพาะฟรี | ซื้อ-ขายได้ |
| Multiple Profile Running | ไม่ | ใช่ |
| Team Collaboration | ไม่ | ใช่ (Cloud) |
| Support | Email | Email + Priority |

### Language Support

| ด้าน | รายละเอียด |
|------|-----------|
| **Software UI** | อังกฤษ — **ไม่มี UI ภาษาไทย** |
| **คู่มือ** | มีคู่มือภาษาไทย (manual.gemlogin.io) |
| **ทีมซัพพอร์ต** | คนไทย — ติดต่อผ่าน LINE OA (@gemlogin) |
| **Content การตลาด** | ภาษาไทย — Facebook, TikTok, LINE, YouTube |

> ⚠️ ห้ามเขียนว่า "GemLogin รองรับภาษาไทย" ในบทความ — UI ไม่มีภาษาไทย สิ่งที่มีคือคู่มือภาษาไทยและทีมซัพพอร์ตคนไทย

---

## 5. ระบบ Automation

### 5.1 ประเภท Command Blocks ใน GemLogin (90+ Blocks)

**Browser (27+ Blocks):**
- Open URL, New Tab, Close Tab, Switch Tab
- Cookie Management, HTTP Request
- Take Screenshot, Handle Download
- Emulate Device, Zoom Page
- Release RAM, Wait Tab Load

**Web Interaction (17+ Blocks):**
- Mouse Click, Mouse Move, Input Text
- Get Text, Hover Element, Scroll Element
- JavaScript Code, Attribute Value
- Switch Frame, Upload File, Press Key

**Control Flow (6 Blocks):**
- Conditions, Loop Data, Loop Elements
- While Loop, Repeat Task, Loop Breakpoint

**Data (16+ Blocks):**
- Insert Data, Delete Data, Sort Data
- Split Data, Data Mapping, Random
- Regex Variable, Slice Variable, Increase Variable
- Read File Text, Read Hotmail, Refresh Hotmail Token
- File Action, Get File Path, Get Log Data

**Online Services (8+ Blocks):**
- ChatGPT, Gemini AI, DeepSeek, Blackbox AI, Grok
- Google Sheets, Google Drive, Excel
- IMAP Read Mail

### 5.2 ประเภท Command Blocks ใน GemPhoneFarm (80+ Blocks)

**UI Interaction (12+ Blocks):**
- Touch, Type Text, Swipe Scroll
- Screenshot, Image Search, Find Text (OCR)
- Clear Text, Press Back/Home/Menu

**Device Management (10+ Blocks):**
- Proxy, Reconnect, Get Property Device
- Dump XML, Get/Set Clipboard
- Check Network, Change Device

**App Management (10+ Blocks):**
- Start App, Stop App, Install App, Uninstall App
- Clear Data App, Close All App
- Is Installed App, Is Open App

(ที่มา: https://manual.gemlogin.io/software-manual/gemlogin/automation-command-blocks.md)

---

## 6. ระบบ Cloud Storage

| คุณสมบัติ | Local Storage | Cloud Storage |
|-----------|---------------|---------------|
| การเก็บข้อมูล | ในเครื่อง | บนเซิร์ฟเวอร์ |
| การเข้าถึง | เครื่องเดียว | ทุกที่ ทุกเครื่อง |
| การซิงค์ | แบ็กอัปเอง | อัตโนมัติ |
| ความเร็ว | เร็วกว่า | ขึ้นกับอินเทอร์เน็ต |
| ทีม | ไม่เหมาะ | เหมาะมาก |
| GemPhoneFarm | ใช้ได้ | กำลังพัฒนา (ยังไม่พร้อม) |

(ที่มา: https://manual.gemlogin.io/get-start/storage-type.md)

---

## 7. การรับประกัน (Warranty)

สำหรับฮาร์ดแวร์ BoxPhone / มือถือ:
- **ระยะเวลา:** 6 เดือนนับจากวันที่ซื้อ
- **ระยะซ่อม:** 7-14 วันทำการ
- **ครอบคลุม:** ความผิดพลาดจากกระบวนการผลิต, อุปกรณ์บกพร่อง
- **ไม่ครอบคลุม:** การตกกระแทก, น้ำ, ซ่อมโดยไม่ได้รับอนุญาต
- ไม่สามารถโอนย้ายการรับประกัน

(ที่มา: https://manual.gemlogin.io/information/faqs.md — เงื่อนไขการรับประกันสินค้า)

---

**Why:** จำเป็นต้องรู้รายละเอียดผลิตภัณฑ์ทุกด้านเพื่อตอบคำถามลูกค้า สร้างเนื้อหาการตลาด และวางกลยุทธ์
**How to apply:** ใช้เป็นฐานความรู้ตอนคุยกับลูกค้า, สร้าง Content Marketing, ออกแบบ Campaign
