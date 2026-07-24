# GemLogin Brand Guide

> จัดทำโดย SALMON 🎨 — Content Creator · ตระกูล KOMHAS 📈
> อัปเดตล่าสุด: 2026-06-29 · ที่มา: https://gemlogin.io (Live Website Analysis)

---

## 🎨 โทนสี (Color Palette)

### สีหลัก (Primary Colors)

| ชื่อ | Hex Code | Tailwind | ใช้ที่ |
|------|----------|----------|--------|
| **Blue-500** (Primary) | `#3b82f6` | `blue-500` | Hover states, icons, องค์ประกอบทั่วไป |
| **Blue-600** (Primary Dark) | `#2563eb` | `blue-600` | ปุ่มหลัก, CTA, gradient start, accent |
| **Blue-700** (Primary Deep) | `#1d4ed8` | `blue-700` | Gradient end, hover สุด |

### Gradient หลักของแบรนด์
```css
--gradient-primary: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
```
**ใช้กับ:**
- `.btn-primary` — ปุ่ม CTA ทุกปุ่ม
- `.gradient-text` — ข้อความไฮไลต์ (เช่น "Automation Platform")
- Hero section, feature card icons

### สีรอง (Secondary Colors)

| ชื่อ | Hex Code | ใช้ที่ |
|------|----------|--------|
| **Purple-500** | `#a855f7` | Accent gradient (ในบางส่วน) |
| **Purple-600** | `#9333ea` | Purple hover |
| **Pink-500** | `#ec4899` | Accent gradient (ในบางส่วน) |
| **Orange-500** | `#f97316` | Highlight/Alert |
| **Green-500** | `#22c55e` | Success, check marks |

### สีพื้นหลัง (Background Colors)

| ชื่อ | Hex Code | ใช้ที่ |
|------|----------|--------|
| **White** | `#ffffff` | พื้นหลังหลัก, การ์ด |
| **Slate-50** | `#f8fafc` | ส่วน Testimonials section |
| **Blue-50** | `#eff6ff` | Badge, icon container, feature bg |
| **Blue-50/30** | `#eff6ff4d` | Hero gradient |
| **Slate-900** | `#0f172a` | Footer background |
| **Slate-800** | `#1e293b` | Footer input bg |

### สีข้อความ (Text Colors)

| ชื่อ | Hex Code | Tailwind | ใช้ที่ |
|------|----------|----------|--------|
| **Slate-900** | `#0f172a` | `text-slate-900` | Heading หลัก |
| **Slate-800** | `#1e293b` | `text-slate-800` | Heading รอง, ชื่อการ์ด |
| **Slate-600** | `#475569` | `text-slate-600` | Body text, nav links |
| **Slate-500** | `#64748b` | `text-slate-500` | Subtitle, คำอธิบาย |
| **Slate-400** | `#94a3b8` | `text-slate-400` | Footer text, metadata |
| **White** | `#ffffff` | `text-white` | Text on dark bg |
| **White/80** | `#fffc` | `text-white/80` | CTA section subtitle |
| **White/70** | `#ffffffb3` | `text-white/70` | CTA section bullet |

### สีขอบ (Border Colors)

| ชื่อ | Hex Code | ใช้ที่ |
|------|----------|--------|
| **Slate-100** | `#f1f5f9` | Card border ปกติ |
| **Blue-200** | `#bfdbfe` | Card border hover |
| **Slate-800** | `#1e293b` | Footer divider |
| **White/20** | `#ffffff33` | CTA section border |

### สี Shadows

| ชื่อ | Hex Code | ใช้ที่ |
|------|----------|--------|
| Blue-500/30 shadow | `#3b82f633` | ปุ่มหลัก, avatar |
| Blue-500/5 shadow | `#3b82f60d` | Card hover |
| Blue-500/10 shadow | `#3b82f61a` | Hover shadow |

---

## 📝 Typography

### ฟอนต์หลัก

| รายละเอียด | ค่า |
|------------|-----|
| **Primary Font** | `Noto Sans Thai` (Variable Font) |
| **Fallback Stack** | `ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif` |
| **Font Source** | Google Fonts (self-hosted woff2) |
| **น้ำหนักที่ใช้** | 400 (Normal), 500 (Medium), 600 (Semibold), 700 (Bold), 800 (Extrabold) |

### ขนาดตัวอักษร

| ระดับ | Tailwind Class | ขนาด | Line Height | ใช้กับ |
|------|----------------|------|-------------|--------|
| **Display** | `text-4xl sm:text-5xl lg:text-6xl` | 2.25rem → 3.75rem | 1.25 (tight) | H1 Hero Title |
| **H2** | `text-3xl sm:text-4xl` | 1.875rem → 2.25rem | 1.25 (tight) | Section heading |
| **H3** | `text-2xl sm:text-3xl` | 1.5rem → 1.875rem | 1.25 (tight) | Feature title |
| **H4** | `text-xl` | 1.25rem | — | Card title, pricing |
| **Section Label** | `text-sm uppercase tracking-wide` | 0.875rem | — | "ทำไมต้อง GemLogin" |
| **Body** | `text-lg sm:text-xl` | 1.125rem → 1.25rem | 1.625 (relaxed) | Subtitle |
| **Body Regular** | `text-base` | 1rem | — | เนื้อหาทั่วไป |
| **Body Small** | `text-sm` | 0.875rem | — | Nav link, description |
| **Caption** | `text-xs` | 0.75rem | — | Badge, small labels |

### ฟอนต์คลาสใน Tailwind

| Class | ใช้ที่ |
|-------|--------|
| `font-display` | Heading ทุกขนาด (ใช้ Noto Sans Thai) |
| `font-sans` | Body text ทั่วไป (ใช้ Noto Sans Thai) |
| `font-bold` | Heading หลัก (700) |
| `font-semibold` | Heading รอง (600) |
| `font-medium` | Nav, button (500) |
| `font-normal` | Body text (400) |
| `antialiased` | ทุก text element |

---

## 📐 Layout & Structure

### โครงสร้างหน้าเว็บ (Page Architecture)

```
├── Navigation (fixed top, transparent → blur on scroll)
│   ├── Logo + Brand Name
│   ├── Menu: ผลิตภัณฑ์ | ราคา | Marketplace | คู่มือ | ดาวน์โหลด | บทความ
│   ├── Language Switcher (TH/EN)
│   ├── เข้าสู่ระบบ
│   └── CTA: เริ่มต้นใช้งาน
│
├── Hero Section
│   ├── Badge: "ใหม่: GemCloudPhone"
│   ├── H1: "No-Code Mobile Automation Platform"
│   ├── Subtitle
│   ├── 2 CTAs: "ทดลองใช้ฟรี" + "ตัวอย่างการทำงาน"
│   ├── Trust bullets (3 รายการ)
│   └── Hero Image (Banner screenshot)
│
├── Features Section
│   ├── 3 Feature Cards (Marketplace / No-Code / Privacy)
│   └── 3 Feature Rows (ซ้าย-สลับ-ขวา)
│       ├── Smart Account Manager
│       ├── Anonymous Technology
│       └── Cross-Device Automation
│
├── Testimonials Section
│   ├── 3 Testimonial Cards
│   └── CTA Banner: "สร้างรายได้กับ GemLogin"
│       ├── Affiliate CTA
│       └── Developer CTA
│
├── CTA Section (Blue Background)
│   ├── "ทดลองฟรี 14 วัน" badge
│   ├── H2: "เริ่มต้นใช้ Antidetect Browser + Automation วันนี้"
│   ├── Trust bullets
│   └── Primary CTA
│
└── Footer (Dark - Slate-900)
    ├── Logo + Description + Email Subscribe
    ├── 4 Columns: ผลิตภัณฑ์ | ทรัพยากร | บัญชี | โซเชียลมีเดีย
    ├── Social icons (7 ช่องทาง)
    └── Copyright
```

### Grid & Container

| องค์ประกอบ | ค่า |
|------------|-----|
| **Max width** | `max-w-7xl` (1280px) |
| **Horizontal padding** | `px-4 sm:px-6 lg:px-8` |
| **Section padding Y** | `py-24` (96px) |
| **Feature cards grid** | `grid md:grid-cols-3 gap-6` |
| **Feature rows grid** | `grid lg:grid-cols-2 gap-12 lg:gap-20` |
| **Testimonial grid** | `grid md:grid-cols-3 gap-6` |
| **Footer columns** | `grid grid-cols-2 md:grid-cols-4 gap-8 lg:gap-12` |

### ระยะห่าง (Spacing)

| องค์ประกอบ | ค่า |
|------------|-----|
| **Nav padding** | `py-5` (20px) |
| **Section margin** | `mb-16` (64px) บน heading |
| **Card padding** | `p-8` (32px) |
| **Card gap** | `gap-6` (24px) |
| **Row spacing** | `mb-24` (96px) ระหว่าง feature rows |
| **CTA section** | `gap-4` ระหว่างปุ่ม |
| **Icon container** | `mb-6` (24px) |
| **Heading spacing** | `mb-4` (16px) ถึง subtitle |
| **Section spacing** | `space-y-32` (128px) ระหว่าง sections |

### Border Radius

| ระดับ | Tailwind | ค่า |
|------|----------|-----|
| **Button** | `rounded-lg` | 0.5rem |
| **Card** | `rounded-xl` | 0.75rem |
| **Image container** | `rounded-2xl` | 1rem |
| **Logo** | `rounded-lg` | 0.5rem |
| **Badge** | `rounded-full` | 9999px |
| **Icon container** | `rounded-xl` | 0.75rem |

---

## 🖼️ Visual Elements

### โลโก้

| รายละเอียด | ค่า |
|------------|-----|
| **ไฟล์** | `/Logo-2.png` |
| **ขนาดใน Nav** | 40x40px (w-10 h-10) |
| **ขนาดใน Footer** | 36x36px |
| **Border Radius** | rounded-lg (0.5rem) |
| **ข้อความข้างโลโก้** | "GemLogin" — `text-xl font-bold font-display` |
| **สี (Nav)** | `text-slate-800` |
| **สี (Footer)** | `text-white` |

### Favicon Set
- `/favicon.ico`
- `/favicon-16x16.png`
- `/favicon-32x32.png`
- `/apple-touch-icon.png`
- `/site.webmanifest`

### ไอคอน
**Icon Library:** Lucide React Icons (https://lucide.dev)

| ไอคอนที่ใช้ | Context |
|------------|---------|
| `Package` | Marketplace card |
| `Layers` | No-Code feature |
| `Fingerprint` | Privacy feature |
| `Quote` | Testimonial |
| `Globe` | Language switcher |
| `Menu` | Mobile hamburger |
| `ChevronDown` | Dropdown indicator |
| `ArrowRight` | Link, CTA |
| `Play` | Video demo button |
| `Check` | Trust bullets, feature list |
| `MessageCircle` | Chat widget |
| `MessageSquare` | LINE icon |
| `Facebook` | Facebook icon |
| `Instagram` | Instagram icon |
| `Youtube` | YouTube icon |
| `Send` | Email subscribe, Telegram |
| `Search` | Search (ในบางหน้า) |

### ภาพประกอบ

| ไฟล์ | ขนาด | ใช้ที่ |
|------|------|--------|
| `/GemPhoneFarm-Banner-1024x446.png` | 1024x446 | Hero section banner |
| `/s1.png` | ~600x400 | Smart Account Manager row |
| `/s2.png` | ~600x400 | Anonymous Technology row |
| `/s3.png` | ~600x400 | Cross-Device Automation row |

### Animation & Effects

| Effect | วิธีใช้ | รายละเอียด |
|--------|--------|------------|
| **Scroll Reveal** | fade-in + translateY | ทุก section ค่อยๆปรากฏเมื่อ scroll |
| **Button Hover** | `hover:scale-102` | ปุ่มหลักขยาย 1.02x |
| **Card Hover** | `-translate-y-1` + shadow | การ์ดยกขึ้น 4px |
| **Gradient Animation** | 200% bg position | Mesh background movement |
| **Ping Badge** | `animate-ping` | "ใหม่" badge สั่น |
| **Rotate Hover** | `rotate(5deg)` | เอฟเฟกต์บนรูป hover |
| **Blur Decoration** | `blur-3xl` | Floating blur circles ตกแต่ง |
| **Link Hover** | `translate-x-1` | ลูกศรขยับขวา |
| **Grid Pattern** | CSS repeating gradient | พื้นหลังลายตารางโปร่ง |
| **Background Gradient** | `bg-gradient-to-b from-white via-blue-50/30 to-white` | Hero gradient background |

### Card Design Pattern
```css
.card-base {
  @apply bg-white rounded-xl p-8 border border-slate-100 
         hover:border-blue-200 hover:shadow-xl 
         hover:shadow-blue-500/5 transition-all duration-300;
}
```

### ปุ่ม (Button System)

#### `.btn-primary` — CTA ปุ่มหลัก
| State | สี | Effect |
|-------|-----|--------|
| **Normal** | Gradient `#2563eb → #1d4ed8` | Shadow `#3b82f633` |
| **Hover** | Gradient `#3b82f6 → #2563eb` | Scale 1.02, shadow เข้ม |
| **Active** | — | Scale 0.98 |

#### `.btn-secondary` — CTA ปุ่มรอง
| State | พื้นหลัง | ขอบ | Text |
|-------|---------|-----|------|
| **Normal** | White | `#e2e8f080` | `#334155` |
| **Hover** | `#f8fafc` | `#cbd5e1` | — |

---

## 🗣️ Brand Voice

### โทนภาษา
- **Content ภาษา:** ไทย (รองรับอังกฤษ)
- **Software UI:** อังกฤษ — **ไม่มี UI ภาษาไทย**
- **การซัพพอร์ต:** มีคู่มือภาษาไทย และทีมซัพพอร์ตคนไทย (LINE OA)
- **ระดับ:** Professional แต่เป็นกันเอง — ทางการพอสมควรแต่ไม่แข็งทื่อ
- **ลักษณะ:** เน้นประโยชน์ ใช้งานได้จริง ชัดเจน ไม่เวอร์วังอลังการ

### Key Messages

| หัวข้อ | ข้อความหลัก (TH) | ข้อความหลัก (EN) |
|--------|-----------------|-----------------|
| **Value Prop** | No-Code Mobile Automation Platform | Build automation without coding |
| **Tagline** | สร้าง workflow อัตโนมัติด้วยการลากและวาง ไม่ต้องเขียนโค้ด | Build powerful automation workflows with drag-and-drop simplicity |
| **Headline** | โซลูชัน Automation ครบวงจร | All-in-One Automation Solution |
| **Feature 1** | แอปพลิเคชันพร้อมใช้งาน — ทุก automation ที่คุณต้องการมีใน Marketplace | Ready-to-Use Applications |
| **Feature 2** | ไม่ต้องเขียนโปรแกรม — สร้าง automation ด้วยการลากและวาง | No Programming Required |
| **Feature 3** | ปกป้องสูงสุด — เทคโนโลยี anti-detection ที่ทรงพลัง | Maximum Protection |
| **Trust** | ชำระเงินได้หลายช่องทาง · ทดลองฟรี 14 วัน · ยกเลิกได้ทุกเมื่อ | Multiple payment options · 14-day free trial · Cancel anytime |

### จุดขายที่เน้น (USPs)

1. **No-Code Drag & Drop** — สร้าง automation โดยไม่ต้องเขียนโค้ด
2. **Anti-Detection** — เทคโนโลยีปกปิดตัวตน / เปลี่ยนพารามิเตอร์อุปกรณ์
3. **ข้ามอุปกรณ์** — รองรับ BoxPhoneFarm, Emulator, Cloud Phone
4. **50+ Modules** — พร้อมใช้งานบน store
5. **Multithread** — รัน tasks พร้อมกัน
6. **ใช้งานง่าย** — เชี่ยวชาญใน 30 นาที
7. **Community Marketplace** — แอปจาก开发者 ชุมชน

### CTA Phrases

| ภาษาไทย | ภาษาอังกฤษ | ใช้ที่ |
|---------|------------|-------|
| ทดลองใช้ฟรี | Start Free Trial | ปุ่มหลักทุกจุด |
| ตัวอย่างการทำงาน | Watch Demo Video | Hero secondary |
| เริ่มต้นใช้งาน | Get Started | Nav bar CTA |
| เข้าสู่ระบบ | Log In | Nav bar |
| เรียนรู้เพิ่มเติม | Learn More | Feature card link |
| เข้าร่วม Affiliate | Join Affiliate | Testimonial CTA |
| เป็น Developer | Become Developer | Testimonial CTA |
| ดาวน์โหลด | Download | Nav menu |
| ราคา | Pricing | Nav menu |

### คำศัพท์ที่ใช้ในแบรนด์ (Brand Vocabulary)

| คำไทยที่ใช้ | คำอังกฤษ |
|------------|---------|
| การลากและวาง | Drag & Drop |
| โปรไฟล์เบราว์เซอร์ | Browser Profile |
| ต่อต้านการตรวจจับ | Anti-Detection |
| ระบบอัตโนมัติ | Automation |
| เวิร์กโฟลว์ | Workflow |
| อุปกรณ์ | Device |
| บัญชี | Account |

---

## 📦 Product Portfolio

### ผลิตภัณฑ์หลัก

| ผลิตภัณฑ์ | คำอธิบาย | กลุ่มเป้าหมาย |
|----------|---------|-------------|
| **GemLogin** | Antidetect Browser + No-Code Automation Platform | บุคคลทั่วไป, Affiliate, Marketer |
| **GemPhoneFarm** | Phone farm management — ควบคุมมือถือหลายเครื่อง | เจ้าของ phone farm, Enterprise |
| **GemCloudPhone** | Cloud Phone (Coming Soon) | ทีม, Remote work |
| **Marketplace/GemStore** | ซื้อ-ขาย Script automation | Developer, Creator |

### แพ็กเกจราคา (Local Storage)

> ราคาอ้างอิงจาก gemlogin.io

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

> ลด 50% เมื่อจ่ายรายปี

### แพ็กเกจราคา (Cloud Storage)

| แพ็กเกจ | ราคา/เดือน (USD) | โปรไฟล์ | Concurrent Threads |
|---------|------------------|---------|-------------------|
| **Starter** | $19 | 10 | 5 |
| **Professional** | $99 | 100 | 25 |
| **Enterprise** | Custom | ไม่จำกัด | 50 |

### ผลิตภัณฑ์เสริม

| รายการ | รายละเอียด |
|--------|------------|
| **GemStore Scripts** | $1 - $100+ (พัฒนาโดย community, revenue share 70/30) |
| **Affiliate Program** | Commission structure สำหรับแนะนำลูกค้า |
| **Mini App Developer** | Revenue share สำหรับนักพัฒนาที่สร้าง Script / Mini App |

---

## 💡 ข้อแนะนำสำหรับ Content Creation

### 1. สีที่ใช้ใน Content
- **สีหลักของแบรนด์:** `#2563eb` (Blue-600) และ `#3b82f6` (Blue-500)
- **Gradient:** จาก `#2563eb` ไป `#1d4ed8`
- **พื้นหลัง:** ใช้ภาพพื้นหลัง gradient จาก white → blue-50 → white
- **Accent:** ใช้ blue เป็นหลัก, purple/pink เป็น accent ในโอกาสพิเศษ
- **บนพื้นหลังสีเข้ม (CTA):** ใช้ `#2563eb` bg + white text
- **ข้อความสำคัญ:** ใช้ gradient-text effect สำหรับหัวข้อที่ต้องการเน้น

### 2. ฟอนต์ที่ใช้ใน Content
- ใช้ **Noto Sans Thai** สำหรับภาษาไทยและอังกฤษ
- ใช้ `font-bold` (700) สำหรับหัวข้อ
- ใช้ `font-medium` (500) หรือ `font-normal` (400) สำหรับเนื้อความ
- หลีกเลี่ยงฟอนต์ Serif หรือฟอนต์ตกแต่งอื่น ๆ

### 3. รูปแบบ Content ที่แนะนำ
- **Thumbnail:** ใช้สีหลัก 3b82f6 และข้อความ gradient
- **Card Design:** ใช้ white card + border สี slate-100 + shadow เล็กน้อย
- **Highlight:** ใช้ blue badge (bg-blue-50, text-blue-600, rounded-full)
- **Feature list:** ใช้ icon container สี blue-600 และ check mark

### 4. Brand Voice Tips
- **น้ำเสียง:** Professional เป็นกันเอง — เหมือนเพื่อนที่ expert
- **การอธิบาย:** เน้นประโยชน์ ไม่เน้น spec
- **ตัวอย่าง:** "ไม่ต้องเขียนโปรแกรม" > "ใช้ drag-and-drop editor"
- **ตัวเลข:** ใช้ตัวเลขเสมอเมื่อพูดถึง performance ("50+ Modules", "30 นาที")
- **ความน่าเชื่อถือ:** เน้น Trust signals ตลอด ("14 วันทดลองฟรี", "ยกเลิกได้ทุกเมื่อ")

### 5. Template Elements สำหรับ Content
```
Header:
├── Font: Noto Sans Thai, Bold, Size ใหญ่
├── Color: Slate-900 (#0f172a) หรือ Gradient (#3b82f6 → #1d4ed8)
└── Alignment: Center

Button:
├── Gradient: #2563eb → #1d4ed8
├── Border Radius: rounded-lg (0.5rem)
├── Text: White, size 14px, weight 500
├── Padding: 12px 24px (py-3 px-6)
└── Hover: scale 1.02, deeper shadow

Card:
├── Bg: White
├── Border: Slate-100 (#f1f5f9)
├── Radius: rounded-xl (0.75rem)
├── Hover: Blue-200 border (#bfdbfe), shadow-xl
└── Padding: p-8 (32px)

Section Label:
├── Text: Blue-600 (#2563eb)
├── Size: text-sm (14px)
├── Weight: font-medium
└── Transform: uppercase tracking-wide
```

### 6. DOs and DON'Ts

**DO:**
- ใช้ Gradient (blue-600 → blue-700) สำหรับปุ่ม CTA
- ใช้ Noto Sans Thai สำหรับทุกข้อความ
- ใช้ White card + subtle border สำหรับ content blocks
- ใช้ Blue-600 icons ใน bg-blue-50 container
- ใช้ "ทดลองใช้ฟรี" เป็น CTA หลักตลอด
- ใช้ Trust signals 3 ข้อใน content ทุกชิ้น

**DON'T:**
- อย่าใช้สีสดจาก palette อื่นนอกจาก blue tones
- อย่าใช้ฟอนต์ Serif
- อย่าใช้พื้นหลังสีเข้มจัด (ยกเว้น footer / CTA section)
- อย่าใช้ Drop shadow หนักเกินไป
- อย่าเปลี่ยน Gradient direction จาก 135deg
- อย่าใช้รูปภาพที่ไม่มีขอบมน

### 7. Social Media Profile Reference

| Platform | Username |
|----------|----------|
| LINE | @909kaiyh (@gemlogin) |
| Facebook | GemLogin (Page) |
| Instagram | @gemlogin |
| TikTok | @gemloginthailand |
| X (Twitter) | @GemloginTH |
| YouTube | @Gemlogin-TH |
| Telegram | @GemLogin_TH |

---

> **SALMON's Note:** เว็บไซต์ Gemlogin.io สร้างด้วย Next.js + Tailwind CSS, hosted on Vercel ใช้ฟอนต์ Noto Sans Thai เป็นหลัก โทนสีเน้น Blue gradient เป็น signature ของแบรนด์ มีระบบ CMS (Manage Content) สำหรับแก้ไข content ทุก section โดยไม่ต้อง deploy ใหม่
