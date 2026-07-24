---
name: gemlogin-workflow-rules
description: Rules for creating GemLogin workflows — always check these before building
metadata:
  type: reference
  created: 2026-07-24
  originSessionId: 99ca41cb-3229-41ef-8b4c-1541286d772f
  modified: 2026-07-24T09:58:58.319Z
---

# GemLogin Workflow Creation Rules

## ก่อนสร้าง workflow ทุกครั้ง

1. **อ่านของจริงก่อน**: query `apps` table ดู workflow ที่มีอยู่แล้ว ใช้เป็น template
2. **Clone structure**: copy ของจริงแล้วแก้ไข อย่าสร้างจากศูนย์
3. **Edge format**: ทุก edge ต้องมี `type: "bezier"`, `markerEnd: "arrowclosed"`, `updatable: true`, `selectable: true`, `data: {}`, `animated: false`
4. **Condition handles**: `{nodeId}-output-{conditionId}` — ห้ามใช้ `output-cond-`
5. **Fallback edges**: เพิ่ม `"style": "stroke: #ff6b6b"`
6. **script ใน DB**: เก็บเป็น JSON **STRING** ไม่ใช่ object
7. **ID**: MongoDB ObjectId format (24 hex chars)
8. **Timestamps**: `YYYY-MM-DD HH:MM:SS.000 +00:00` (มี timezone)
9. **description/version**: ห้ามเป็น NULL — ต้องมีค่า
10. **Cloud mode**: GemLogin sync จาก cloud → local DB ทับข้อมูลเรา ถ้าจะเพิ่ม workflow ต้อง import ผ่าน UI หรือ inject ผ่าน DevTools

## วิธีที่ดีที่สุด

- **DB-first**: เขียน workflow ลง `db.db` โดยตรง (เร็วกว่า API)
- **Backup ก่อน**: copy `db.db` ทุกครั้งก่อนเขียน
- **Verify หลังเขียน**: query กลับมาดูว่า edges/nodes ถูกต้อง
- **Restart GemLogin**: ต้องปิดแล้วเปิดใหม่ ไม่ใช่แค่ Ctrl+R

## Team

- ARKA 🔧 — Workflow Creator (ใต้ GEMMY 💎)
- GEMMY 💎 — Automation Lead

**Why:** Prevent repeating same mistakes across sessions
**How to apply:** Read this BEFORE creating any GemLogin workflow JSON
