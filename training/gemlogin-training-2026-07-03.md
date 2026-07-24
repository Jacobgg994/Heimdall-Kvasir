---
title: "Gemlogin Training — การใช้งานโปรไฟล์และสคริปต์อย่างมืออาชีพ"
date: "วันศุกร์ที่ 3 กรกฎาคม 2026 เวลา 14:00 น."
author: "ทีม Gemlogin"
lang: th
toc: true
papersize: a4
geometry: margin=1in
fontsize: 12pt
---

# 🚀 Gemlogin Training

## การใช้งานโปรไฟล์และสคริปต์อย่างมืออาชีพ

**วันศุกร์ที่ 3 กรกฎาคม 2026 | เวลา 14:00 น.**

---

# 📋 Agenda — สิ่งที่จะได้เรียนรู้วันนี้

| ลำดับ | หัวข้อ | เวลา (นาที) |
|-------|--------|-------------|
| 1 | วิธีใช้งาน PROXY + การผูก + เช็คโลเคชั่น | 15 |
| 2 | การ Run สคริปต์โดยใช้ PROXY + ฟังก์ชันที่ถูกต้อง | 15 |
| 3 | เทคนิคการล็อกอิน Facebook | 15 |
| 4 | แก้ปัญหา Captcha | 10 |
| 5 | เทคนิคทำให้การทำงานราบรื่น | 10 |
| 6 | แหล่งวิดีโอสอนและ Troubleshooting | 5 |
| 7 | การหน่วงเวลา (Delay) กับ Script | 10 |
| 8 | เทคนิคเพิ่มเติม + การ Warm Facebook | 10 |
| — | **ถาม-ตอบ (Q&A)** | 15 |

**รวม: ~105 นาที**

---

# PART 1

# 🔐 วิธีใช้งาน PROXY
# การผูกที่ถูกต้อง และเช็คโลเคชั่น

---

## PROXY คืออะไร — ทำไมต้องใช้?

- **Proxy** = ตัวกลางระหว่างคุณกับอินเทอร์เน็ต
- Facebook มองเห็น IP ของ Proxy → ไม่ใช่ IP จริงของคุณ
- แต่ละโปรไฟล์ควรมี **1 Proxy ต่อ 1 โปรไฟล์** (ห้ามแชร์)
- Proxy แต่ละตัวต้องตรงกับ **ประเทศของบัญชี Facebook**

```
[Gemlogin Profile] ──▶ [Proxy IP: 1.2.3.4] ──▶ [Facebook]
                             🇺🇸 USA
```

---

## ประเภทของ Proxy ที่แนะนำ

| ประเภท | ความน่าเชื่อถือ | ราคา | เหมาะกับ |
|--------|:---:|:---:|----------|
| **Residential (ISP)** | ⭐⭐⭐⭐⭐ | สูง | Facebook หลัก, เพจสำคัญ |
| **Residential (Rotating)** | ⭐⭐⭐⭐ | กลาง | Warm-up, ไถฟีด |
| **Mobile 4G/5G** | ⭐⭐⭐⭐⭐ | สูงมาก | บัญชีใหม่, กู้บัญชี |
| **Datacenter** | ⭐⭐ | ต่ำ | ❌ ไม่แนะนำสำหรับ Facebook |

> ⚠️ **ข้อควรระวัง:** Datacenter IP ถูก Facebook บล็อคง่ายมาก หลีกเลี่ยง!

---

## วิธีผูก PROXY ใน Gemlogin

### Step-by-Step:

1. เปิด **Gemlogin** → ไปที่แท็บ **Profiles**
2. เลือกโปรไฟล์ที่ต้องการ → คลิก **⚙️ Settings** (หรือคลิกขวา → Edit)
3. ไปที่แท็บ **Proxy**
4. เลือกประเภท Proxy:
   - `HTTP` / `HTTPS` / `SOCKS5`
5. กรอกข้อมูล:
   ```
   Host: proxy.example.com
   Port: 12345
   Username: your_username
   Password: your_password
   ```
6. คลิก **Check Proxy** — รอให้ขึ้น `✅ Connected`
7. คลิก **Save**

---

## การเช็คโลเคชั่น — ทำให้แน่ใจว่า Proxy ทำงานถูกต้อง

### วิธีที่ 1: เช็คผ่าน Gemlogin
- เปิด Browser Profile → ไปที่ `https://ipinfo.io`
- ดูว่า **Country**, **City**, **ISP** ตรงกับที่ Proxy ระบุ

### วิธีที่ 2: เช็คใน Facebook
- ไปที่ Facebook → Settings → Security → **Where You're Logged In**
- ดูว่าตำแหน่งที่แสดงตรงกับ Proxy

### วิธีที่ 3: ใช้ Browser Extension
- ติดตั้ง Extension `IP Address and Domain Information`
- หรือ `What is my IP` ใน Chrome Web Store

---

## 📋 Checklist — ก่อนเริ่มงานทุกครั้ง

```
☐ Proxy Status: ✅ Connected
☐ Country ตรงกับบัญชี Facebook
☐ ISP เป็น Residential (ไม่ใช่ Datacenter)
☐ WebRTC Leak ปิดแล้ว (สำคัญ!)
☐ Timezone ตรงกับ Proxy Location
☐ Language ตรงกับประเทศ
☐ Geolocation API ถูกบล็อก
```

---

## WebRTC Leak — ศัตรูตัวร้าย!

> WebRTC สามารถ**รั่วไหล IP จริง**ของคุณแม้จะใช้ Proxy แล้ว

### วิธีปิด WebRTC ใน Gemlogin:
1. Profile Settings → **Advanced**
2. เปิด `WebRTC IP Handling`
3. เลือก: **Disable non-proxied UDP**
4. หรือ: **Use proxy IP for WebRTC**

✅ เช็คว่าไม่มี Leak: ไปที่ `https://browserleaks.com/webrtc`

---

# PART 2

# 🖥️ การ Run สคริปต์โดยใช้ PROXY
# ฟังก์ชันที่ถูกต้อง

---

## หลักการพื้นฐาน — ก่อนกด Run

> 🎯 **กฎเหล็ก:** ต้อง Start Profile ด้วย Proxy ที่ถูกต้องก่อนรันสคริปต์เสมอ!

ลำดับที่ถูกต้อง:
```
1. ตั้งค่า Proxy ใน Profile  →  2. Start Profile  →  3. ตรวจสอบ IP  →  4. Run Script
```

**ห้าม:**
- ❌ เปลี่ยน Proxy กลางคันขณะ Profile กำลังทำงาน
- ❌ รันสคริปต์ก่อนเช็คว่า Proxy ใช้งานได้
- ❌ ใช้ Proxy ตัวเดียวกันกับหลายโปรไฟล์พร้อมกัน

---

## ฟังก์ชันสำคัญใน Gemlogin Scripts

### 1. `start_profile` — เปิดโปรไฟล์
```
- เปิดเบราว์เซอร์ด้วย Profile + Proxy ที่ตั้งไว้
- รอจนเบราว์เซอร์พร้อมใช้งาน
```

### 2. `navigate` — ไปยังหน้าเว็บ
```
- ไปที่ URL ที่ต้องการ (เช่น facebook.com)
- รอจนหน้าโหลดเสร็จ
```

### 3. `wait` / `delay` — หน่วงเวลา
```
- หน่วงเวลาเป็นวินาที (เช่น wait 3000 = 3 วิ)
- ใช้ระหว่างขั้นตอนเพื่อจำลองมนุษย์
```

### 4. `click` / `type` — คลิกและพิมพ์
```
- คลิกปุ่ม / พิมพ์ข้อความ
- ใช้ CSS Selector หรือ XPath
```

### 5. `screenshot` — จับหน้าจอ
```
- บันทึกภาพหน้าจอเพื่อตรวจสอบภายหลัง
- มีประโยชน์สำหรับ Debug
```

---

## ตัวอย่าง Workflow — การโพสต์ในกลุ่มด้วย PROXY

```
1. start_profile("profile_facebook_thai_01")
2. navigate("https://facebook.com")
3. wait(3000)
4. check_login_status()
5. navigate("https://facebook.com/groups/123456")
6. wait(2000)
7. click("#create-post-button")
8. type("#post-input", "ข้อความที่ต้องการโพสต์")
9. wait(1000)
10. click("#submit-post")
11. wait(5000)
12. screenshot("result.png")
13. stop_profile()
```

> 💡 **Tip:** ใส่ `wait` ระหว่างทุกขั้นตอน — Facebook จะมองว่าเป็นมนุษย์ ไม่ใช่บอท

---

## การใช้ Cloud Script Execution

Gemlogin รองรับการรันสคริปต์ผ่าน Cloud:

```
- ส่ง Workflow ผ่าน Gemlogin SaaS
- รันบน Cloud Device โดยไม่ต้องเปิดเครื่องตัวเอง
- เหมาะสำหรับการรันจำนวนมากแบบ Batch
```

### สิ่งที่ต้องเตรียม:
```
☐ Device ID
☐ Soft ID
☐ Cloud Token
☐ Workflow ID
```

> ⚠️ เก็บ Token ไว้เป็นความลับ — ห้ามแชร์หรือ Commit ขึ้น Git!

---

## การจัดการข้อผิดพลาดในสคริปต์

```javascript
// ตัวอย่าง Pseudo-code
try {
  start_profile("profile_01");  // ← เปิดด้วย Proxy
  login();                      // ← ล็อกอิน
  do_task();                    // ← ทำงาน
} catch (proxy_error) {
  log("❌ Proxy ล้มเหลว → หยุด, เปลี่ยน Proxy");
  stop_profile();
} catch (captcha_error) {
  log("⚠️ Captcha → แก้ก่อนดำเนินการต่อ");
  solve_captcha();
} catch (login_error) {
  log("❌ ล็อกอินไม่สำเร็จ → เช็คบัญชี");
  stop_profile();
}
```

---

# PART 3

# 👤 สอนวิธีและเทคนิค
# ในการล็อกอิน Facebook

---

## ขั้นตอนการล็อกอินที่ถูกต้อง

### Step 1: ตรวจสอบสภาพแวดล้อมก่อนล็อกอิน

```
☐ Proxy Connected & Location Verified
☐ Cookie/Cache ถูกล้างหรือไม่? (แนะนำให้มีอยู่บ้าง)
☐ Browser Fingerprint ตรงกับข้อมูลบัญชี
☐ Timezone = Timezone ของ Proxy
☐ Screen Resolution ตั้งค่าสมจริง
```

---

## Step 2: วิธีการล็อกอินที่ปลอดภัย

### วิธี A — ล็อกอินแบบค่อยเป็นค่อยไป (แนะนำ)

```
1. เปิด facebook.com → อยู่หน้าแรก 2-3 นาที (ไถฟีดนิดหน่อย)
2. คลิก "Log In" → ใส่ Email/Phone
3. Wait 2-3 วินาที → พิมพ์ช้าๆ เหมือนมนุษย์
4. ใส่ Password → Wait → กด Enter
5. ถ้ามี 2FA → รอ 30 วิ ก่อนกรอกรหัส
6. หลังจากล็อกอินสำเร็จ → อยู่บนหน้า Feed 5 นาที
   ก่อนทำอะไรต่อ
```

### วิธี B — ใช้ Cookie Login (เร็ว)

```
1. Export Cookie จากบัญชีที่เคยล็อกอินแล้ว
2. Import Cookie เข้า Profile ใน Gemlogin
3. เปิด Profile → Facebook จะเห็นว่าเป็นอุปกรณ์เดิม
```

---

## Step 3: การจัดการ 2FA (Two-Factor Authentication)

### ประเภท 2FA และวิธีแก้:

| ประเภท | วิธีแก้ |
|--------|--------|
| **SMS Code** | ใช้เบอร์ที่ผูกไว้ — รอรับ SMS |
| **Authenticator App** | ใช้ Google Authenticator / Authy |
| **Email Code** | เช็คอีเมลที่ผูกกับ Facebook |
| **Trusted Contacts** | ให้เพื่อนที่ตั้งไว้ส่ง code |
| **Login Alert (Approve)** | กด "This was me" ในแอพ Facebook |

> 💡 **คำแนะนำ:** ถ้าเป็นไปได้ ให้ปิด 2FA สำหรับบัญชีที่ใช้กับ Automation — หรือใช้ Authenticator App ที่เข้าถึงได้ง่าย

---

## เทคนิคการล็อกอินให้รอด (ไม่โดน Checkpoint)

### 🎯 กฎ 3 ข้อ:

1. **เลียนแบบมนุษย์ — เสมอ**
   - อย่ากดเร็วเกินไป
   - เลื่อนเมาส์แบบไม่เป็นเส้นตรง
   - เว้นจังหวะระหว่างคลิก

2. **รักษาสภาพแวดล้อม**
   - ใช้ Proxy เดิมทุกครั้ง
   - ใช้ Browser Fingerprint เดิม
   - อย่าเปลี่ยนอุปกรณ์บ่อย

3. **สะสมประวัติก่อน**
   - หลังจากล็อกอินครั้งแรก → ไถฟีด 10-15 นาที
   - Like 1-2 โพสต์
   - Logout → Login ใหม่ใน 1-2 ชั่วโมง
   - ทำแบบนี้ 2-3 รอบ → Facebook เริ่มเชื่อถืออุปกรณ์นี้

---

## การผูก Facebook เข้ากับโปรไฟล์ — วิธีที่ถูกต้อง

### 🆕 การสร้างบัญชีใหม่ + Warm-up:

```
วันที่ 1-3:   ล็อกอินอย่างเดียว + ไถ Feed + Like 2-3 โพสต์
วันที่ 4-5:   เพิ่มเพื่อน 1-2 คน + แชร์ 1 โพสต์
วันที่ 6-7:   คอมเมนต์ 1-2 โพสต์ + เข้ากลุ่ม
วันที่ 8-14:  เพิ่มเพื่อน 3-5 คน/วัน + โพสต์ 1 ครั้ง/วัน
วันที่ 15+:   เริ่ม Automation เบาๆ (ห้ามหนัก!)
```

> ⚠️ **ห้าม:** สร้างบัญชี → เพิ่มเพื่อน 50 คน → โพสต์ 10 กลุ่ม ในวันเดียว = **แบนแน่นอน 100%**

---

# PART 4

# 🤖 แก้ปัญหาเรื่อง Captcha
# เวลาล็อกอินหรือ Run Script

---

## Captcha คืออะไร — ทำไมถึงเจอ?

- Facebook ใช้ Captcha เพื่อตรวจสอบว่าเป็นมนุษย์
- **สาเหตุที่เจอบ่อย:**
  - เปลี่ยน IP/Proxy บ่อย
  - กดเร็วเกินไป (เหมือนบอท)
  - เข้าสู่ระบบจากอุปกรณ์ใหม่
  - ทำกิจกรรมผิดปกติ (สแปม, เพิ่มเพื่อนเร็วเกิน)
  - Proxy คุณภาพต่ำ (Datacenter)

---

## ประเภท Captcha ที่เจอใน Facebook

| ประเภท | ลักษณะ | ระดับความยาก |
|--------|--------|:---:|
| **Checkbox** | "I am not a robot" ☑️ | ⭐ |
| **Image Challenge** | เลือกรูปที่มีรถเมล์/ไฟจราจร | ⭐⭐ |
| **Photo ID** | อัพโหลดรูปบัตรประชาชน | ⭐⭐⭐⭐⭐ |
| **Video Selfie** | อัดวิดีโอหน้าตัวเอง | ⭐⭐⭐⭐⭐ |
| **Phone Verify** | ยืนยันเบอร์โทรศัพท์ | ⭐⭐⭐ |

---

## วิธีแก้ Captcha — จากง่ายไปยาก

### วิธีที่ 1: แก้ด้วยมือ (Manual Solve)

```
1. เมื่อเจอ Captcha → หยุดสคริปต์ทันที
2. แก้ Captcha ด้วยมือในเบราว์เซอร์
3. เมื่อผ่านแล้ว → รอ 1-2 นาที → รันสคริปต์ต่อ
```

### วิธีที่ 2: ใช้บริการแก้ Captcha อัตโนมัติ

| บริการ | ราคา | ความแม่นยำ |
|--------|------|:---:|
| **2Captcha** | ~$0.50/1000 | 90%+ |
| **Anti-Captcha** | ~$0.50/1000 | 90%+ |
| **CapSolver** | ~$0.80/1000 | 95%+ |
| **CapsMonster** | ใช้ AI | 85%+ |

---

## การตั้งค่า Captcha Solver ใน Gemlogin

```
1. สมัครบัญชีกับ 2Captcha / Anti-Captcha
2. รับ API Key
3. ใส่ใน Gemlogin Settings → Captcha Solver
4. เลือกประเภท: reCAPTCHA v2 / v3 / hCaptcha
5. ตั้งค่า Timeout: 120 วิ
6. ทดสอบด้วยปุ่ม Test
```

---

## 🛡️ ป้องกัน Captcha — ดีกว่าแก้

### Checklist ลดโอกาสเจอ Captcha:

```
☐ ใช้ Residential/Mobile Proxy (ไม่ใช่ Datacenter)
☐ ใช้ Proxy เดิมกับโปรไฟล์เดิมตลอด
☐ ตั้ง Delay ระหว่าง actions (5-15 วิ)
☐ เลียนแบบ Mouse Movement แบบมนุษย์
☐ ไม่เปิดหลายโปรไฟล์พร้อมกันบน IP เดียว
☐ มี Cookie/Cache สะสม (อย่าล้างทุกครั้ง)
☐ จำกัดจำนวน Action ต่อวัน (ค่อยๆ เพิ่ม)
☐ สุ่มเวลาในการทำ Activity (ไม่ทำตรงเวลาเป๊ะทุกวัน)
```

---

# PART 5

# ✨ เทคนิคและวิธีอื่นๆ
# ที่ทำให้การทำงานราบรื่นขึ้น

---

## เทคนิคที่ 1: Browser Fingerprint — ให้สมจริง

### ตั้งค่า Fingerprint ให้ตรงกับบัญชี:

```
☐ User Agent → ตรงกับ OS/Browser ที่สมจริง
☐ Screen Resolution → 1920x1080 หรือ 1366x768
☐ Language → ตรงกับประเทศ (เช่น th-TH สำหรับไทย)
☐ Timezone → ตรงกับ Proxy Location
☐ Fonts → ติดตั้ง Font ที่จำเป็น
☐ WebGL → Renderer ตรงกับ GPU ที่สมจริง
☐ Canvas Fingerprint → Unique แต่สมจริง
☐ AudioContext → ไม่ถูกบล็อก (สมจริง)
```

> 💡 ใน Gemlogin: Profile → Advanced → Fingerprint Settings

---

## เทคนิคที่ 2: Cookie Management

### กลยุทธ์การจัดการ Cookie:

```
✅ เก็บ Cookie ไว้ — Facebook เห็นว่าเป็นอุปกรณ์เดิม = น่าเชื่อถือ
✅ Export Cookie สำรอง — เผื่อ Profile เสีย
✅ อายุ Cookie ปกติ ~30-90 วัน — ต่ออายุโดยล็อกอินก่อนหมด
❌ อย่าล้าง Cookie ทุกครั้ง — ยิ่งล้าง ยิ่งดูน่าสงสัย
```

### วิธีย้าย Cookie ระหว่างโปรไฟล์:
```
1. Profile A → Export Cookies (JSON)
2. Profile B → Import Cookies
3. ใช้ Proxy เดียวกับ Profile A
4. ✅ Facebook มองว่าเป็นอุปกรณ์เดิม
```

---

## เทคนิคที่ 3: Activity Pattern — เหมือนมนุษย์

### ❌ รูปแบบที่บอททำ → โดนแบน:

```
08:00:00 → Login
08:00:05 → Post ในกลุ่ม 1
08:00:10 → Post ในกลุ่ม 2
08:00:15 → Post ในกลุ่ม 3
... (ทุกอย่างเป๊ะตรงเวลา, ไม่มีพัก)
```

### ✅ รูปแบบที่มนุษย์ทำ → ปลอดภัย:

```
08:03:21 → Login
08:05:47 → ไถ Feed
08:12:33 → Like โพสต์ 1
08:18:09 → Post ในกลุ่ม 1
08:25:42 → ไถ Feed
08:31:18 → Comment
... (เวลาไม่เป๊ะ, มีพัก, มีไถ Feed)
```

---

## เทคนิคที่ 4: Profile Rotation — ผลัดกันทำงาน

```
อย่าใช้โปรไฟล์เดียวทำงานหนักทั้งวัน!

โปรไฟล์ A → ทำงาน 08:00-10:00 → พัก (ไถ Feed)
โปรไฟล์ B → ทำงาน 10:00-12:00 → พัก
โปรไฟล์ C → ทำงาน 13:00-15:00 → พัก
โปรไฟล์ A → ทำงาน 15:00-17:00 → พัก
```

**Benefits:**
- ✅ Facebook เห็นแต่ละโปรไฟล์ Active แค่ช่วงสั้น
- ✅ ลดความเสี่ยงการโดน Rate Limit
- ✅ ลดโอกาสเจอ Captcha
- ✅ ถ้าโปรไฟล์ใดมีปัญหา โปรไฟล์อื่นยังทำงานได้

---

## เทคนิคที่ 5: Error Handling — รับมือเมื่อพัง

```javascript
// Flow การรับมือข้อผิดพลาดที่ดี

if (login_failed) {
  → Stop ทันที → Log Error → ลองใหม่ใน 30 นาที
}

if (captcha_detected) {
  → Pause Script → Notify Admin → Manual Solve
}

if (proxy_dead) {
  → Stop Profile → Switch to Backup Proxy → Retry
}

if (facebook_checkpoint) {
  → Stop ทุก Activity → Manual Recovery → Wait 24 Hrs
}

if (rate_limited) {
  → Wait 1-2 Hrs → ลด Activity ลง 30%
}
```

---

## เทคนิคที่ 6: การตั้งค่า Browser

```yaml
แนะนำการตั้งค่าใน Gemlogin:
  WebRTC: Disable non-proxied UDP
  Canvas: Noise (สุ่มเล็กน้อย)
  WebGL: Disable / Use Proxy Info
  Audio: Real (ไม่ Disable)
  Fonts: Default + Locale fonts
  Geolocation: Use Proxy Location
  Do Not Track: Enable
  Flash: Disable (ตายแล้ว)
```

---

# PART 6

# 🎬 แหล่งวิดีโอสอน
# และการ Troubleshooting

---

## แหล่งวิดีโอ — Youtube & Tutorials

### แนะนำช่อง / Playlists:

| แหล่ง | เนื้อหา | ลิงก์ |
|-------|--------|-------|
| **Gemlogin Official** | สอนใช้งานพื้นฐาน-ขั้นสูง | [รอใส่ลิงก์] |
| **Multi-Login Tips** | เทคนิค Anti-Detect Browser | [รอใส่ลิงก์] |
| **Facebook Automation** | สอนเขียน Script + Workflow | [รอใส่ลิงก์] |

### หัวข้อวิดีโอที่กำลังจะทำเพิ่ม:
```
📹 เริ่มต้น Gemlogin ใน 10 นาที
📹 การตั้งค่า Proxy แบบ Step-by-Step
📹 สร้าง Workflow อัตโนมัติสำหรับ Facebook
📹 แก้ปัญหา Captcha ที่เจอบ่อย
📹 วิธีกู้บัญชี Facebook ที่โดน Checkpoint
📹 เทคนิค Warm-up บัญชีใหม่ให้รอด
📹 การใช้ Cookie เพื่อให้ Facebook ไว้ใจ
```

---

## Common Errors & Solutions

### 🔴 "Proxy Connection Failed"

```
สาเหตุ: Proxy ตาย / Proxy หมดอายุ / ตั้งค่าผิด
วิธีแก้:
  1. เช็ค Proxy ว่าใช้งานได้ที่ ipinfo.io
  2. ติดต่อผู้ให้บริการ Proxy
  3. เปลี่ยน Backup Proxy
  4. เช็ค Firewall/Antivirus ไม่บล็อก Port
```

### 🔴 "Login Checkpoint — Confirm Your Identity"

```
สาเหตุ: Facebook สงสัยว่าบัญชีถูกแฮ็ก
วิธีแก้:
  1. หยุดกิจกรรมทั้งหมด (สำคัญมาก!)
  2. ยืนยันตัวตนตามที่ Facebook กำหนด
  3. หลังจากผ่าน Checkpoint → Wait 24-48 ชม.
  4. กลับมาแบบเบาๆ — ไถ Feed 1-2 วันก่อน
```

### 🔴 "Profile Failed to Start"

```
สาเหตุ: Port ทับซ้อน / Chromium พัง / Memory ไม่พอ
วิธีแก้:
  1. ปิด Profile อื่นๆ → Restart Gemlogin
  2. ลองเปิดด้วย Port อื่น
  3. ล้าง Cache Chromium
  4. Restart เครื่องคอม
```

---

## Tools แนะนำสำหรับ Troubleshooting

```
🔧 BrowserLeaks — browserleaks.com
   → เช็ค WebRTC, Canvas, Font, WebGL

🔧 IPInfo — ipinfo.io
   → เช็ค IP, Location, ISP

🔧 Pixelscan — pixelscan.net
   → เช็ค Browser Fingerprint โดยรวม

🔧 F.vision — f.vision
   → เช็ค Facebook Trust Score (แนวทาง)

🔧 CreepJS — abrahamjuliot.github.io/creepjs
   → เช็ค Fingerprint ระดับลึก
```

---

# PART 7

# ⏱️ การหน่วงเวลา (Delay) กับ Script
# แนะนำการตั้งค่าที่ถูกต้อง

---

## ทำไม Delay ถึงสำคัญ?

> 🎯 Facebook มี AI ที่ตรวจจับ Bot จาก **จังหวะการทำงานที่เป๊ะเกินไป**

```
มนุษย์: คลิก → 0.8วิ → พิมพ์ → 1.2วิ → คลิก → 3.5วิ → เลื่อน
บอท:   คลิก → 0.1วิ → พิมพ์ → 0.1วิ → คลิก → 0.1วิ → เลื่อน
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        Facebook AI: "THIS IS A BOT 🤖" → บล็อก!
```

---

## ตาราง Delay แนะนำ — แยกตาม Activity

| Activity | Delay (วินาที) | หมายเหตุ |
|----------|:---:|----------|
| Login → Feed | 3000-5000ms | รอนาน — หน้า Feed หนัก |
| Feed Scroll | 2000-4000ms | เลื่อนช้าๆ เหมือนคนอ่าน |
| Like Post | 1000-3000ms | สุ่ม — บางทีมองนาน บางทีเร็ว |
| Comment | 3000-8000ms | ต้องอ่านก่อนเมนต์ |
| Post in Group | 5000-10000ms | Facebook เช็คเข้มกลุ่ม |
| Add Friend | 3000-6000ms | ห้ามรัว — เพิ่มเร็ว = แบน |
| Send Message | 2000-5000ms | พิมพ์ + รอคนอ่าน |
| Share Post | 3000-5000ms | Share เร็ว = สแปม |

---

## 🎲 สุ่ม Delay — กุญแจสำคัญ!

### ❌ ไม่ควรทำ:
```javascript
wait(3000);  // wait 3 วิเป๊ะๆ ทุกครั้ง ❌
wait(3000);  // Facebook จับ Pattern ได้!
wait(3000);
```

### ✅ ควรทำ:
```javascript
wait(random(2500, 4200));  // 2.5 - 4.2 วิ
wait(random(1800, 3500));  // 1.8 - 3.5 วิ
wait(random(5000, 8000));  // 5.0 - 8.0 วิ
```

> 💡 **หลักการ:** `random(lower, upper)` — สุ่มเลขระหว่าง lower และ upper ทุกครั้ง

---

## สูตร Delay แยกตามประเภทงาน

### 📝 Content Posting:
```
เปิด Facebook → wait(3000-5000)
เข้ากลุ่ม → wait(2000-4000)
กดสร้างโพสต์ → wait(1000-3000)
พิมพ์ข้อความ → wait(ตัวอักษรละ 50-150ms)
wait ก่อนโพสต์ → wait(2000-5000)
กดโพสต์ → wait(5000-8000)
เช็คผลโพสต์ → wait(3000-5000)
```

### 🧹 Account Warm-up:
```
Login → wait(5000-10000)
Scroll Feed → wait(3000-6000) x 3-5 ครั้ง
Like 1-2 Posts → wait(2000-5000) ต่อครั้ง
Wait → wait(300000-600000)  // พัก 5-10 นาที
Scroll → wait(3000-6000)
Logout → จบ
```

---

## ตั้งค่า Global Delay ใน Gemlogin

```
Settings → Script Settings → Delay

แนะนำ:
  Global Min Delay: 1000ms
  Global Max Delay: 4000ms
  Typing Speed: 100-200ms ต่อตัวอักษร
  Mouse Movement: Human-like (Bezier curve)
  Scrolling: Smooth (ไม่ใช่ Jump Scroll)
```

> 🎯 **Tip:** ถ้าใช้หลายสคริปต์ → ตั้ง Global Delay ให้เผื่อไว้ แล้วปรับใน Script เฉพาะจุดที่ต้องเร็ว/ช้าเป็นพิเศษ

---

# PART 8

# 🔥 เทคนิคเพิ่มเติม
# + การ Warm Facebook อย่างมืออาชีพ

---

## Warm-up Facebook — วิธีที่ดีที่สุด

### 🐣 บัญชีใหม่ (0-7 วัน):
```
Day 1:   Login → ดู Feed 10 นาที → Logout
Day 2:   Login → Like 1-2 Posts → ดู Feed 15 นาที
Day 3:   Login → Like + Comment 1 Post → ดู Feed
Day 4:   Login → Add 1 Friend → ดู Feed + Like
Day 5-7: Login → Add 1-2 Friends/day → Like + Comment
```

### 🐥 บัญชีกลาง (7-30 วัน):
```
Day 8-14:  Add 2-3 Friends/day → 1 Post → Join 1 Group
Day 15-21: Add 3-5 Friends/day → 1-2 Posts → Join 2 Groups
Day 22-30: เริ่ม Automation เบาๆ
  → โพสต์ 1-2 กลุ่ม/วัน
  → Comment 2-3 โพสต์/วัน
```

### 🐓 บัญชีโตแล้ว (30+ วัน):
```
Day 31+:  เพิ่ม Activity ได้
  → โพสต์ 3-5 กลุ่ม/วัน
  → Comment 5-10/วัน
  → Add Friend 5-10/วัน
  → แต่ยังต้องสุ่มเวลา + พักระหว่าง!
```

---

## 🚫 สิ่งที่ห้ามทำเด็ดขาด

```
❌ สร้างบัญชี → โพสต์ 10 กลุ่มในวันแรก
❌ เพิ่มเพื่อน 50+ คนในวันเดียว
❌ ส่งข้อความ 100+ คนใน 1 ชั่วโมง
❌ ใช้ Datacenter Proxy
❌ เปลี่ยน Proxy บัญชีเดิมไปมาตลอดเวลา
❌ รันหลายโปรไฟล์บน IP เดียวกันพร้อมกัน
❌ กด Like/Comment/Share รัวๆ ไม่มีพัก
❌ ใช้ Browser Fingerprint เดิมเป๊ะกับทุกโปรไฟล์
❌ โพสต์เนื้อหาเดียวกันใน 20 กลุ่มพร้อมกัน
❌ ละเลย Delay — "ขอแค่ทำงานได้ก็พอ"
```

---

## 📊 Tracking — เช็คสุขภาพโปรไฟล์

### Daily Checklist:
```
☐ Proxy OK?
☐ Login สำเร็จ?
☐ เจอ Checkpoint/Captcha ไหม?
☐ Activity สำเร็จกี่ %?
☐ มี Error อะไรบ้าง?
☐ Facebook Trust Score (สังเกตจาก: ต้อง verify เบอร์ไหม?
   โดนให้ confirm identity ไหม? เข้ากลุ่มได้ปกติไหม?)
```

### Weekly Review:
```
☐ โปรไฟล์ไหนมีปัญหาบ่อย → พัก, ปรับ Proxy
☐ โปรไฟล์ไหนทำงานดี → วิเคราะห์ว่าทำไมถึงดี
☐ ปรับ Strategy ตามผลลัพธ์
```

---

## 🛟 Recovery — กู้บัญชีเมื่อโดนแบน

### ขั้นตอนการกู้บัญชี:

```
1. หยุดกิจกรรมทันที — ห้ามพยายามล็อกอินซ้ำไปมา
2. รอ 24-48 ชม. — ให้ระบบเย็นลงก่อน
3. ใช้ Proxy เดิม — ห้ามเปลี่ยน!
4. ลองล็อกอินผ่าน m.facebook.com (มือถือ)
5. ถ้าขึ้น Checkpoint → ทำตามขั้นตอน:
   - ยืนยันเบอร์โทรศัพท์
   - อัพโหลดรูป (ถ้าขอ)
   - ยืนยันตัวตนผ่านเพื่อนที่ไว้ใจ
6. หลังจากผ่าน → Wait 48 ชม. → กลับมาแบบเบาๆ
```

> ⚠️ **สำคัญ:** ถ้าบัญชีโดน Permanently Disabled — แทบกู้ไม่ได้ → เริ่มบัญชีใหม่ดีกว่า

---

## 🎯 สรุป — 10 กฎทองของ Gemlogin Automation

```
1️⃣  1 Proxy ต่อ 1 Profile — ห้ามแชร์
2️⃣  ใช้ Residential/Mobile Proxy เท่านั้น
3️⃣  ตั้งค่า Delay ให้สมจริง — สุ่มตลอด
4️⃣  เลียนแบบมนุษย์ — ทุกจังหวะ ทุกการคลิก
5️⃣  Warm-up บัญชีใหม่ — ไม่รีบ ห้ามใจร้อน
6️⃣  หมุนเวียนโปรไฟล์ — อย่าใช้ตัวเดียวหนัก
7️⃣  เก็บ Cookie — อย่าล้างทุกครั้ง
8️⃣  เจอ Captcha/Checkpoint → หยุดก่อน อย่าฝืน
9️⃣  Track & Monitor — รู้ว่าอะไรพังก่อนสาย
🔟  Content Unique — อย่าโพสต์ข้อความเดิมซ้ำๆ
```

---

# ❓ Q&A

## ถาม-ตอบ / แชร์ประสบการณ์

### คำถามที่พบบ่อย:

**Q: Warm-up กี่วันถึงจะใช้ Automation ได้?**
→ อย่างน้อย **30 วัน** — เร็วไป = แบน

**Q: Proxy หมดอายุกลางคัน — ทำไง?**
→ หยุดโปรไฟล์นั้นทันที → ต่ออายุ Proxy → รอ 1 ชม. → ค่อยกลับมาใหม่

**Q: 1 เครื่อง ใช้กี่โปรไฟล์ได้?**
→ ไม่จำกัดจำนวนโปรไฟล์ แต่คำนวณ RAM: ~500MB-1GB ต่อโปรไฟล์

**Q: ทำไมบางบัญชีโดนแบนทั้งที่ทำถูกทุกอย่าง?**
→ Facebook มีปัจจัยหลายอย่าง — IP Reputation, Account Age, Behavior Pattern, Content Quality — ปรับทีละปัจจัย

**Q: ใช้ VPN แทน Proxy ได้ไหม?**
→ ❌ ไม่แนะนำ — VPN IP ถูกแชร์โดยคนจำนวนมาก → Reputation แย่ → Facebook บล็อกง่าย

---

# 📲 ติดต่อ / Support

```
📱 Telegram: [ใส่ลิงก์ Telegram]
📧 Email: [ใส่อีเมล]
📹 Youtube: [ใส่ลิงก์ช่อง]
🖥️ Website: [ใส่เว็บไซต์]
```

## ไฟล์เพิ่มเติม:
- 📄 เอกสารฉบับนี้ (PDF)
- 📊 Checklist รายวัน (Google Sheets)
- 🎬 ลิงก์วิดีโอสอนแบบ Step-by-Step

---

# 🙏 ขอบคุณครับ

## Gemlogin Training
### วันศุกร์ที่ 3 กรกฎาคม 2026

**"ทำให้ Facebook คิดว่าคุณเป็นมนุษย์ — แล้วคุณจะไม่มีวันโดนบล็อก"**

---

> Document generated for Gemlogin Training Session. For questions, contact the Gemlogin team.
