# บันทึกการประชุมทีม Dev — GemLogin Landing Page Review

**วันที่:** 22 กรกฎาคม 2026
**ผู้เข้าร่วม:** 🌊 JIMMY (Facilitator), 🖥️ PHOOM (Frontend), 🎨 PIM (UI/UX), ⚙️ OAT (Tech Lead), 🐛 MINT (QA)

---

## 📋 DECISION LOG (15 ข้อ)

| # | หัวข้อ | ตัดสินใจ | เหตุผล |
|---|--------|---------|--------|
| 1 | **Tech Stack** | HTML + Tailwind + IntersectionObserver + Custom JS | 3:1 โหวต; เร็ว, เบา, deploy ใน 3 วัน |
| 2 | **Animation** | IntersectionObserver + CSS transitions (ตัด AOS) | AOS deprecation, zero dependency |
| 3 | **Icons** | Lucide Icons (CDN + tree-shake) | เบา, community maintained |
| 4 | **Section 4 Cards** | Static (ไม่ expandable) | Content สั้น 2-3 บรรทัด ไม่ต้องซ่อน |
| 5 | **Section Structure** | Merge Section 2+3 (Pain → Solution) | ลด redundancy, flow ลื่นขึ้น |
| 6 | **Section 5** | Keep ไว้ standalone | Essential สำหรับ non-technical users |
| 7 | **สีส้มบนขาว** | #F97316 ใช้เฉพาะ decorative + CTA; body ใช้ #1C1917 | WCAG AA — contrast 3.0:1 ไม่ผ่าน 4.5:1 |
| 8 | **Border contrast** | เปลี่ยนจาก #FED7AA → #FDBA74 | เพิ่ม contrast กับพื้นหลัง |
| 9 | **Mobile Hero Font** | 32px (เพิ่มจาก 28px) | วรรณยุกต์ไทยต้องการ px มากกว่า |
| 10 | **Counter Animation** | IntersectionObserver + rAF + prefers-reduced-motion | ประสิทธิภาพดี, accessible |
| 11 | **Mobile Stats Layout** | 3-column ลด gap + 14px font (ไม่ใช้ carousel) | Credibility > interaction |
| 12 | **ฟอนต์ไทย** | Kanit (headings) + Sarabun (body), woff2, subset | ดีไซน์ถูกแล้ว, subset ลด payload |
| 13 | **Font Loading** | font-display: swap + preload critical font | กัน CLS, optimize FCP |
| 14 | **Phase 2 Migration** | Next.js ใน Q4 2026 | PHOOM ยื่นคำขาด |
| 15 | **Floating CTA** | ปุ่ม sticky CTA ตอน mobile scroll | กัน user หลุดจาก page ยาวๆ |

---

## 🎯 ACTION ITEMS (11 ข้อ)

| # | Task | Owner | Due |
|---|------|-------|-----|
| A1 | Set up project scaffold (HTML + Tailwind + CSS variables) | 🖥️ PHOOM | 23 ก.ค. |
| A2 | Update color palette ตาม PIM spec | 🎨 PIM | 23 ก.ค. |
| A3 | Implement merged Section 2+3 (Problem → Solution) | 🖥️ PHOOM | 24 ก.ค. |
| A4 | Build counter animation utility | 🖥️ PHOOM | 24 ก.ค. |
| A5 | QA checklist — accessibility | 🐛 MINT | 23 ก.ค. |
| A6 | Font subset + preload setup | ⚙️ OAT | 23 ก.ค. |
| A7 | Mobile layout mockups (320/640/1024px) | 🎨 PIM | 24 ก.ค. |
| A8 | Floating CTA component | 🖥️ PHOOM | 25 ก.ค. |
| A9 | Deploy staging → ส่ง SALMON review | ⚙️ OAT | 26 ก.ค. |
| A10 | Schedule Phase 2 Next.js planning | 🌊 JIMMY | 30 ก.ค. |
| A11 | Lighthouse audit (target 90+) | 🐛 MINT | 27 ก.ค. |

---

## 🗣️ Closing Statements

- **PHOOM:** "Next.js ไม่ผ่าน แต่เข้าใจ — จะ deliver static HTML ให้เร็วที่สุด ขออย่าเปลี่ยน requirement กลางทาง"
- **PIM:** "ดีใจที่ทีมรับ accessibility issue — จะส่ง color mapping ให้ PHOOM พรุ่งนี้เช้า"
- **OAT:** "Deadline 26 ก.ค. ต้องมีของให้ SALMON review — PHOOM มีอะไรให้ช่วยบอก"
- **MINT:** "จะเข้าทำ accessibility audit ทีละ section หลัง PHOOM สร้างเสร็จ แก้ทีละส่วน"
- **JIMMY:** "Productive meeting — 15 decisions, 11 action items, deadline ชัดเจน ขอบคุณทุกคน"

---

*Meeting: 10:04–11:27 น. | Duration: 83 นาที*
