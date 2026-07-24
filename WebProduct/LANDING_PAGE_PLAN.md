# 🎨 Landing Page Design Plan — GemLogin

> **Product:** GemLogin — Antidetect Browser + No-Code Automation Platform
> **Key Message:** "Process First. Automate Next."
> **Target:** นักการตลาด, SMM, Affiliate, เจ้าของธุรกิจออนไลน์, Agency
> **Color Palette:** ขาว + ส้ม (White + Orange)
> **Date:** 2026-07-22

---

## 1. 🎨 Design Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--primary` | `#F97316` | ปุ่ม CTA, เน้นข้อความสำคัญ, icons |
| `--primary-hover` | `#EA580C` | Hover state |
| `--primary-light` | `#FFF7ED` | Background section, cards |
| `--primary-gradient` | `#F97316 → #FB923C` | Hero gradient accents |
| `--bg-white` | `#FFFFFF` | พื้นหลังหลัก |
| `--bg-warm` | `#FFFBEB` | Secondary background (สลับ section) |
| `--text-dark` | `#1C1917` | Headings, body text |
| `--text-muted` | `#78716C` | Subtitle, description |
| `--border` | `#FED7AA` | Card borders, dividers |
| `--success` | `#22C55E` | Check marks, status |
| `--shadow` | `0 1px 3px rgba(249, 115, 22, 0.1)` | Card shadows |

### Typography
- **Headings:** Kanit (Thai-friendly, modern)
- **Body:** Sarabun (อ่านง่าย, รองรับไทยสมบูรณ์)
- **Fallback:** system-ui, sans-serif

---

## 2. 🏗️ Page Structure (9 Sections)

```
┌─────────────────────────────────────────┐
│  SECTION 1: HERO                        │
│  "งานไม่ได้เยอะ คุณแค่กำลังเสียเวลา     │
│   กับงานเดิมๆ ที่ซ้ำซาก"                │
│  CTA: "เริ่มสร้าง Workflow แรก"         │
├─────────────────────────────────────────┤
│  SECTION 2: PAIN POINTS                 │
│  3 อาการที่บอกว่าคุณกำลังติดกับดัก Manual│
├─────────────────────────────────────────┤
│  SECTION 3: SOLUTION                    │
│  "Process First. Automate Next."        │
│  GemLogin คืออะไร — 1 ประโยค           │
├─────────────────────────────────────────┤
│  SECTION 4: 3 ตัวช่วยหลัก               │
│  📌 แยกบัญชี  📌 ปลอดภัย  📌 Automation │
├─────────────────────────────────────────┤
│  SECTION 5: HOW IT WORKS                │
│  3 Steps: ออกแบบ Process → ลากและวาง → │
│  ระบบทำงานให้คุณ                        │
├─────────────────────────────────────────┤
│  SECTION 6: USE CASES                   │
│  "ใครใช้ GemLogin แล้วชีวิตเปลี่ยน"      │
│  4 Persona Cards                        │
├─────────────────────────────────────────┤
│  SECTION 7: SOCIAL PROOF                │
│  ตัวเลข + Testimonials                  │
├─────────────────────────────────────────┤
│  SECTION 8: PRICING                     │
│  Soft Sell — "เริ่มต้นวันนี้"           │
├─────────────────────────────────────────┤
│  SECTION 9: FOOTER + FINAL CTA          │
│  "Process First. Automate Next."        │
└─────────────────────────────────────────┘
```

---

## 3. 📐 Detailed Section Specs

### SECTION 1: HERO
```
┌──────────────────────────────────────────────────┐
│  [LOGO]                           [เข้าใช้งาน]   │
│                                                  │
│         ┌────────────────────────────┐           │
│         │ 🟠 ใหม่! No-Code Automation│ (pill)    │
│         └────────────────────────────┘           │
│                                                  │
│    งานไม่ได้เยอะ                                 │
│    คุณแค่กำลังเสียเวลา                            │
│    กับงานเดิมๆ ที่ซ้ำซาก                         │
│                                                  │
│    สร้าง Automation ของตัวเอง                    │
│    ด้วยการลากและวาง — ไม่ต้องเขียนโค้ด           │
│                                                  │
│    [✨ เริ่มสร้าง Workflow แรก]  [📺 ดูวิธีใช้]  │
│                                                  │
│    ✅ ไม่ต้องติดตั้ง  ✅ ใช้ฟรี 7 วัน             │
│                                                  │
│         [Product Screenshot / Mockup]            │
│         (dashboard แสดง workflow + profiles)     │
└──────────────────────────────────────────────────┘
```
- **Background:** White + subtle orange gradient wave at bottom
- **Headline:** 36-48px, Kanit Bold, text-dark
- **Subheadline:** 18-20px, text-muted
- **Primary CTA:** Orange button (#F97316), white text, 16px bold, rounded-xl
- **Secondary CTA:** White button, orange border, orange text
- **Pill badge:** Light orange bg (#FFF7ED), orange text, small

### SECTION 2: PAIN POINTS — "คุณกำลังรู้สึกแบบนี้อยู่หรือเปล่า?"
```
┌──────────────────────────────────────────────────┐
│  3 Cards (horizontal, icon-top)                   │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ 😫       │  │ ⏰       │  │ 🔄       │       │
│  │          │  │          │  │          │       │
│  │ เปิดทีละ │  │ หมดเวลา  │  │ กลัว     │       │
│  │ Profile  │  │ กับงาน   │  │ โพสต์ผิด │       │
│  │ ทุกเช้า  │  │ ซ้ำๆ     │  │ Profile  │       │
│  │          │  │          │  │          │       │
│  │ "เสีย 2  │  │ "กว่าจะ  │  │ "แค่     │       │
│  │ ชม. กับ  │  │ เสร็จก็  │  │ สลับผิด │       │
│  │ การเปิด  │  │ หมดวัน"  │  │ ก็หายนะ" │       │
│  │ ปิด"     │  │          │  │          │       │
│  └──────────┘  └──────────┘  └──────────┘       │
└──────────────────────────────────────────────────┘
```
- **Cards:** White bg, orange top-border (4px), shadow
- **Emoji:** 40px
- **Title:** 18px Kanit Bold
- **Quote:** 14px Sarabun, text-muted, italic

### SECTION 3: SOLUTION — "Process First. Automate Next."
```
┌──────────────────────────────────────────────────┐
│                                                  │
│    เมื่อ Process ชัด                               │
│    การเปลี่ยนงาน Manual ให้เป็น Workflow           │
│    จะง่ายขึ้นมาก                                  │
│                                                  │
│    GemLogin ให้คุณ                                │
│    ✅ ลากและวางสร้าง Automation                  │
│    ✅ คุมทุกโปรไฟล์ในระบบเดียว                    │
│    ✅ ไม่ต้องเขียนโค้ดสักบรรทัด                  │
│                                                  │
│    [⚡ เริ่มต้นตอนนี้]                            │
└──────────────────────────────────────────────────┘
```
- **Background:** Warm (#FFFBEB)
- **Layout:** Two-column — Left: Text, Right: Illustration/animation showing drag-drop
- **Feature checks:** Green checkmarks, each on separate line

### SECTION 4: 3 ตัวช่วยหลัก (Feature Cards)
```
┌──────────────────────────────────────────────────┐
│  📌 3 ตัวช่วยระบบอัจฉริยะ                          │
│                                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │ 🔒          │ │ 🌐          │ │ 🤖          │ │
│  │             │ │             │ │             │ │
│  │ แยกบัญชี   │ │ หมดปัญหา    │ │ Automation  │ │
│  │ ชัดเจน     │ │ IP ซ้ำ      │ │ อัจฉริยะ    │ │
│  │ ปลอดภัย    │ │ ลดความเสี่ยง│ │ ไม่ต้องเขียน │ │
│  │ ไม่ปนกัน   │ │ โดนแบน      │ │ โค้ด        │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ │
└──────────────────────────────────────────────────┘
```
- **Cards:** 3-column, white bg, orange icon circle, shadow-sm
- **Icon circle:** 64px, orange bg (#FFF7ED), icon inside
- **Title:** 20px Kanit Bold
- **Description:** 14px, text-muted

### SECTION 5: HOW IT WORKS — 3 Steps
```
┌──────────────────────────────────────────────────┐
│  เริ่มใช้ GemLogin ใน 3 ขั้นตอน                    │
│                                                   │
│    ①                  ②                  ③       │
│   🧠                 🖱️                 🚀       │
│   ออกแบบ            ลากและวาง          ระบบทำงาน  │
│   Process           สร้าง Workflow     ให้คุณ      │
│                                                     │
│   "คิดก่อนว่าจะ      "ใช้เมาส์ลาก        "กลับไปทำ  │
│   ให้ระบบทำอะไร"     Action มาวาง       อย่างอื่น   │
│                      เรียงกัน"          ได้เลย"     │
│                                                     │
│   ────────●──────────●──────────────────●───────    │
│   (timeline with orange dots and connecting line)   │
└──────────────────────────────────────────────────┘
```
- **Background:** White
- **Steps:** Numbered circles (orange), connected by orange dotted line
- **Icons:** Inside circles (🧠🖱️🚀)
- **Title:** 20px Kanit Bold per step
- **Quote:** 14px italic Sarabun under each

### SECTION 6: USE CASES — "ใครใช้ GemLogin แล้วชีวิตเปลี่ยน"
```
┌──────────────────────────────────────────────────┐
│                                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐│
│  │ 👤       │ │ 🛒       │ │ 📱       │ │ 🏢  ││
│  │          │ │          │ │          │ │      ││
│  │ SMM &    │ │ E-Com    │ │ Affiliate│ │Agency││
│  │ Creator  │ │merce     │ │          │ │      ││
│  │          │ │          │ │          │ │      ││
│  │"บริหาร   │ │"เปิด     │ │"30      │ │"ทีม  ││
│  │100 Page │ │ร้านครบ  │ │บัญชี    │ │20 คน││
│  │ด้วยคน   │ │ทุกแพลต  │ │รายได้×3 │ │ทำงาน ││
│  │เดียว"   │ │ฟอร์ม"   │ │ใน 3 ด." │ │พร้อม" ││
│  └──────────┘ └──────────┘ └──────────┘ └──────┘│
└──────────────────────────────────────────────────┘
```
- **Cards:** 4-column grid, white bg, orang border-left accent
- **Avatar:** Circle with emoji/icon, 48px
- **Persona title:** 16px Kanit Bold
- **Quote:** 13px Sarabun, text-muted

### SECTION 7: SOCIAL PROOF
```
┌──────────────────────────────────────────────────┐
│  (Orange warm background #FFF7ED)                 │
│                                                   │
│     10,000+         5,000+         98%            │
│     ผู้ใช้รายเดือน   Workflows      พึงพอใจ       │
│                                                   │
│  ┌───────────────────────────────────────────┐   │
│  │ "ตั้งแต่ใช้ GemLogin ชีวิตเปลี่ยนมาก —     │   │
│  │  จากที่เคยใช้ 6 ชม./วัน เปิดปิด Profile    │   │
│  │  ตอนนี้เหลือแค่เช็คระบบ 30 นาที"           │   │
│  │                                            │   │
│  │  — คุณเอก, เจ้าของ Agency การตลาด         │   │
│  └───────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```
- **Stats:** Large orange numbers, counter animation on scroll
- **Testimonial card:** White bg, orange left-border, rounded-lg
- **Quote:** 16px Sarabun
- **Attribution:** 13px, text-muted

### SECTION 8: PRICING (Soft Sell)
```
┌──────────────────────────────────────────────────┐
│                                                  │
│  ┌─────────────────────────┐                    │
│  │ 🚀 เริ่มต้นวันนี้        │                    │
│  │                         │                    │
│  │ ทดลองใช้ฟรี 7 วัน       │                    │
│  │ ไม่ต้องกรอกบัตรเครดิต   │                    │
│  │                         │                    │
│  │ ✅ 10 Profiles          │                    │
│  │ ✅ Basic Automation     │                    │
│  │ ✅ Community Support    │                    │
│  │                         │                    │
│  │ [✨ สร้าง Workflow แรก] │                    │
│  └─────────────────────────┘                    │
│                                                  │
│  (ดูแพ็กเกจทั้งหมด →)                            │
└──────────────────────────────────────────────────┘
```
- **Card:** Centered, white bg, orange border (2px), shadow-lg
- **"ฟรี 7 วัน":** Large, orange text, bold
- **"ไม่ต้องกรอกบัตร":** Green checkmark + text
- **CTA:** Full-width orange button
- **Link:** Small text link below card

### SECTION 9: FOOTER
```
┌──────────────────────────────────────────────────┐
│                                                  │
│       Process First. Automate Next.              │
│                                                  │
│       [✨ เริ่มสร้าง Workflow แรกของคุณ]          │
│                                                  │
│  ──────────────────────────────────────────────  │
│                                                  │
│  GemLogin  |  Features  |  Use Cases  |  Blog   │
│                                                  │
│  © 2026 GemLogin. All rights reserved.          │
└──────────────────────────────────────────────────┘
```
- **Background:** Dark text (#1C1917) on white
- **Tagline:** 24px Kanit Bold, orange
- **Final CTA:** Orange button
- **Footer links:** 4 columns, 14px

---

## 4. 📱 Responsive Breakpoints

| Breakpoint | Layout |
|-----------|--------|
| **Mobile (320-640px)** | Single column, stacked cards, hamburger menu, reduced hero font (28px) |
| **Tablet (641-1024px)** | 2-column grids, normal nav, medium hero font (36px) |
| **Desktop (1025px+)** | Full 3-4 column grids, full nav, large hero (48px) |

---

## 5. 🎬 Micro-interactions & Animation

| Element | Animation |
|---------|-----------|
| Hero headline | Fade-in + slide-up on load |
| Stat numbers | Counter animation on scroll into view |
| Feature cards | Staggered fade-in on scroll |
| CTA button | Scale pulse on hover (scale: 1.02) |
| Step timeline | Draw connecting line on scroll |
| Testimonial card | Subtle parallax on scroll |

---

## 6. 🔧 Tech Stack Recommendation

| Layer | Option A (Simple) | Option B (Advanced) |
|-------|-------------------|---------------------|
| **Framework** | HTML + Tailwind CSS | Next.js + Tailwind |
| **Animation** | AOS (Animate on Scroll) | Framer Motion |
| **Icons** | Lucide Icons | Heroicons |
| **Fonts** | Google Fonts (Kanit + Sarabun) | Same |
| **Hosting** | Vercel / Cloudflare Pages | Same |
| **Analytics** | Plausible (privacy-first) | Mixpanel |

**Recommendation:** Option A — Simple static HTML + Tailwind + AOS. Fast to deploy, easy to iterate, no build complexity. Move to Next.js when we need dynamic content or i18n.

---

## 7. 📋 Dev Checklist

- [ ] Set up project scaffold (HTML + Tailwind)
- [ ] Implement design tokens (CSS variables)
- [ ] Build Section 1: Hero
- [ ] Build Section 2: Pain Points
- [ ] Build Section 3: Solution
- [ ] Build Section 4: Feature Cards
- [ ] Build Section 5: How It Works
- [ ] Build Section 6: Use Cases
- [ ] Build Section 7: Social Proof
- [ ] Build Section 8: Pricing
- [ ] Build Section 9: Footer
- [ ] Add AOS animations
- [ ] Responsive QA (mobile, tablet, desktop)
- [ ] Lighthouse audit (target: 90+)
- [ ] Deploy to staging
- [ ] Thai copy review by SALMON 🎨
- [ ] Final deploy

---

## 8. 🎯 Success Metrics

| Metric | Target |
|--------|--------|
| Page load time | < 2.5s |
| Lighthouse Performance | 90+ |
| CTA click rate | 5%+ |
| Mobile bounce rate | < 40% |
| Conversion (trial signup) | 3%+ |

---

*Design Plan by JIMMY 🌊 — พร้อมให้ทีม dev ประชุมต่อ*
