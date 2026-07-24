# 🎨 Design Reference — JACOB Command Center

> เรียนรู้จาก Webflow + Figma Templates

---

## 🔥 Design Trends 2025-2026

### จาก Webflow Templates
| Trend | นำมาปรับใช้ |
|-------|-----------|
| **Dark-first design** | พื้นหลัง #0a0a0a หลัก ไม่ใช่ afterthought |
| **Minimal navigation** | Top bar 40px — ไม่มี sidebar ใหญ่ |
| **Monospace typography** | JetBrains Mono ทั้งหมด |
| **Flat design** | ไม่มี shadow, ไม่มี gradient, ไม่มี rounded corners |
| **High contrast text** | #e5e5e5 บน #0a0a0a |
| **Single accent color** | เขียว #22c55e สำหรับ interactive elements |

### จาก Figma Dashboard Templates
| Template | สิ่งที่ได้ |
|----------|----------|
| **Dashbrd X** | Dark dashboard, clean typography, minimal cards |
| **Horizon UI** | 300+ components, dark/light modes |
| **Sneat Admin** | Atomic design, flat, modern |
| **Glow DS** | Dark-first — dark mode เป็น primary |

---

## 🎯 JACOB CC Design System

### Colors
```
Background:     #080808  (ดำสนิท)
Surface:        #0d0d0d  (เทาดำ สำหรับ panels)
Border:         #1a1a1a  (บางๆ แทบมองไม่เห็น)
Text Primary:   #e5e5e5  (ขาว-เทา อ่านสบายตา)
Text Secondary: #808080  (เทากลาง สำหรับ metadata)
Accent Green:   #22c55e  ( prompt, success, system )
Accent Blue:    #3b82f6  ( links, sparingly )
Error:          #ef4444  ( errors )
Warning:        #eab308  ( warnings )
```

### Typography
```
Font: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace
Size: 13px base / 11px small / 16px headings
Weight: 400 normal / 500 medium / 700 bold
Line Height: 1.6
```

### Layout
```
Top Bar: 40px height, #0d0d0d bg, 1px border-bottom #1a1a1a
Content: flex 1, #080808 bg, padding 16px
Input: 40px height, #0d0d0d bg, 1px border #1a1a1a
Button: #1a1a1a bg, #e5e5e5 text, 4px radius MAX
```

### Component Style (FLAT)
```
❌ NO: shadows, gradients, rounded > 4px, cards with borders
✅ YES: flat backgrounds, subtle separators, monospace, minimal
```

---

## 📱 Terminal Chat — The Key Feature

Chat should look EXACTLY like Claude Code CLI:

```
┌─────────────────────────────────────────────┐
│ JACOB CC · localhost · deepseek-v4-pro[1m] │ top bar 40px
├─────────────────────────────────────────────┤
│                                             │
│  JIMMY 🌊 พร้อมทำงาน                        │ system msg
│  ทีม 22 คน · RAM 19% · CPU 5%              │
│                                             │
│  > ให้ SALMON เขียนบทความ TikTok Shop       │ user input (green)
│                                             │
│  ✅ รับทราบ — กำลังส่ง SALMON...            │ system response
│                                             │
│  SALMON 🎨 รายงาน:                          │ agent response
│  บทความเสร็จแล้ว — 1,800 คำ                 │
│  📂 /content/blog-tiktok-shop.md            │
│                                             │
│  > ▌                                        │ cursor blinking
└─────────────────────────────────────────────┘
```

---
> 📅 2026-06-30
