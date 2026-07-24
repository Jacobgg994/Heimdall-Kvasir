---
name: gemlogin-workflow-patterns
description: แพทเทิร์นการสร้าง Workflow GemLogin ที่ใช้บ่อย — structure, edge routing, loop design
metadata:
  type: skill
  category: gemlogin
  owner: gemmy
---

# 🔄 GemLogin Workflow Patterns — Real Patterns จาก 801

> อัปเดตล่าสุด: 2026-06-29 — ถอดจากสคริปต์จริง 8 ไฟล์
> แหล่งที่มา: `/mnt/d/skills/WorkflowGemlogin/801/`

---

## Pattern 1: Open Page → Actions → End (Simple Flow)

ใช้กับ: งานง่ายๆ ที่ไม่ต้อง loop

**Real example จาก:** Add Friends from Groups or Page 1.0 (13 nodes)

```
[trigger] → [open-url] → [tab-loaded] → [event-click/element-exists] → ... → [end]
```

**Node types ที่ใช้:** BlockBasic × 2, BlockBasicWithFallback × 8, BlockRepeatTask × 2, BlockConditions × 1

---

## Pattern 2: Loop with Data Processing (Core Pattern)

ใช้กับ: Warm Facebook, Like & Comment, Post Page, Share

> นี่คือ pattern ที่พบบ่อยที่สุดใน 801 — เกือบทุกสคริปต์ใช้ loop เป็นแกนหลัก

```
[trigger]
  ↓
[random] ← สุ่มค่า delay ไว้ใช้
  ↓
[read-file-text] ← อ่านข้อมูลจากไฟล์
  ↓
[loop-data (mainloop)]
  ↓
[loop-breakpoint (mainloop)]
  ↓
[open-url → tab-loaded] ← เปิดหน้าเว็บ
  ↓
[element-exists → conditions] ← ตรวจสอบ condition
  ↓  ┌─ match → [event-click → mouse-move → delay → event-click...]
     └─ fallback → [event-click → delay ...]
  ↓
[... actions ...]
  ↓
[increase-variable] ← เพิ่ม counter
  ↓
[insert-data] ← บันทึกผลลัพธ์
  ↓
[loop-breakpoint] ← กลับไป loop ถ้ายังไม่ครบ
  ↓
[end]
```

**Real examples:**
| สคริปต์ | Nodes | Edges | Loops |
|---------|-------|-------|-------|
| Warm Facebook | 70 | 85 | 8 repeat-task + 5 loop-breakpoint |
| Like && Comment 1.6 | 83 | 102 | 63 BlockBasicWithFallback, 5 loop-breakpoint |
| Post Page 1.9 | 230 | 298 | 11 repeat-task + 6 loop-breakpoint, 18 delay |
| Share 1.6 | 61 | 74 | 4 loop-breakpoint |

---

## Pattern 3: Repeat-Task Wrapper

ใช้กับ: ทำซ้ำ block เดิมหลายๆ ครั้ง

```
[trigger] → [open-url] → [tab-loaded]
  ↓
[repeat-task] ← กำหนดจำนวนรอบ
  ↓
[event-click] → [delay] → [event-click] → [delay] → [loop-breakpoint]
```

**ข้อสังเกต:** `repeatFor` ใช้ `{{variables.count}}` หรือตัวเลขตรงก็ได้

---

## Pattern 4: Conditions Branch (Value Check)

ใช้กับ: เช็คค่า variable เพื่อเลือก path การทำงาน

```
[element-exists] ← ตรวจ element
  ↓
[conditions]
  ├─ output-{group_id} → [event-click → ...]
  └─ output-fallback → [delay → skip-action]
```

**ตัวอย่าง conditions structure จาก Like & Comment 1.6:**
```
Group "Like":
  └─ value: {{variables.enableLike}} == eq == true
      └─ element#exists: //span[text()="Add to story"]

Group "comment":
  └─ value: {{variables.enableComment}} == eq == true
      └─ value: {{variables.deleteUsedComments}} == eq == true

Group "RandomLike" (3 options):
  └─ {{variables.RandomLike}} == eq == 1
  └─ {{variables.RandomLike}} == eq == 2
  └─ {{variables.RandomLike}} == eq == 3
```

---

## Pattern 5: Environment Branch (OS Detection)

ใช้กับ: เลือก実行 method ตาม OS (จาก Post Status v.6)

```
[conditions]
  ├─ output-MacOS → [commandPro: curl + osascript] → [delay]
  └─ output-fallback → [commandPro: powershell] → [delay]
```

---

## Pattern 6: Multi-Phase Processing

ใช้กับ: Post Page 1.9 (230 nodes — ใหญ่ที่สุด)

สคริปต์ Post Page 1.9 มีหลาย phase ที่เรียงกัน:
1. **Phase 1:** ตั้งค่า — random delay, read variables
2. **Phase 2:** Content selection — เลือกประเภทโพสต์ (ภาพ/วิดีโอ/GIF/ผสม)
3. **Phase 3:** Navigation — เปิด Facebook → login check → navigate to wall/group
4. **Phase 4:** Posting loop — loop-data → write content → upload media → post
5. **Phase 5:** Interaction — react to post (like) → comment on post
6. **Phase 6:** Save results — clipboard → file-action (save link) → insert-data
7. **Phase 7:** Location — select location (Thailand regions) via conditions

---

## Pattern 7: Variable Pipeline

ใช้กับ: เตรียมค่าตัวแปรก่อนเข้าสู่ main processing loop

```
[random (number)] → สุ่ม delay
[read-file-text (aline)] → อ่านข้อมูลจากไฟล์
[split-data] → split string เป็น array
[loop-data (numbers)] → วนลูปตามจำนวน
```

---

## Important: Node Label Distribution (จาก 8 ไฟล์จริง)

| Label | จำนวน | ใช้ทำอะไร |
|-------|-------|-----------|
| `event-click` | 128 | คลิก element ต่างๆ |
| `press-key` | 49 | พิมพ์ข้อความ |
| `insert-data` | 35 | บันทึกข้อมูลลง data table |
| `open-url` | 34 | เปิด URL |
| `element-exists` | 28 | ตรวจ element |
| `read-file-text` | 21 | อ่านไฟล์ .txt |
| `element-scroll` | 19 | scroll หน้า |
| `random` | 18 | สุ่มค่า |
| `loop-data` | 15 | วนลูป |
| `javascript-code` | 15 | รัน JS |
| `increase-variable` | 12 | ++ตัวแปร |
| `tab-loaded` | 11 | รอโหลด |
| `upload-file` | 11 | อัปโหลด |
| `delete-data` | 7 | ลบ variable |
| `mouse-move` | 7 | เลื่อนเมาส์ |
| `commandPro` | 5 | รัน shell |
| `hover-element` | 4 | hover |
| `reload-tab` | 4 | reload |
| `file-action` | 3 | เขียนไฟล์ |
| `split-data` | 3 | split string |
| `get-file-path` | 2 | เลือกไฟล์ |
| `forms` | 2 | กรอก form |
| `clipboard` | 2 | คัดลอก |

---

## Edge ID Format (Real)

```json
{
  "id": "vueflow__edge-{source}-output-{n}-{target}-input-1",
  "type": "bezier",
  "source": "node-id",
  "target": "target-node-id",
  "sourceHandle": "{source-node-id}-output-1",
  "targetHandle": "{target-node-id}-input-1",
  "updatable": true,
  "selectable": true,
  "data": {},
  "label": "",
  "markerEnd": {"type": "arrowclosed", "width": 20, "height": 20, "color": "#b1b1b7"}
}
```

---

## Trigger Parameters Pattern

Real trigger parameters ใช้หลาย type ร่วมกัน:

```
divider    → แบ่ง section (มี label)
label      → ข้อความอธิบาย
checkbox   → boolean option
string     → path หรือ folder
filepath   → path ไฟล์ .txt
number     → จำนวน
inline     → spacing
```

**ตัวอย่าง parameter definition ที่สมบูรณ์:**
```json
{
  "id": "random-id",
  "name": "pageIdFolderPath",
  "label": "Page ID Folder",
  "type": "string",
  "description": "คำอธิบายภาษาไทย",
  "defaultValue": "C:\\Users\\Admin\\Downloads\\UID",
  "placeholder": "Enter path to page ID folder",
  "data": {
    "required": true,
    "masks": false,
    "useMask": false,
    "unmaskValue": ""
  }
}
```

---

## Loop Design Rules (จากของจริง)

1. **loopId** ใช้ชื่อซ้ำกันระหว่าง `loop-data` และ `loop-breakpoint` (เช่น `"mainloop"`)
2. **loop-data** ใช้ `loopThrough: "numbers"` + `fromNumber`/`toNumber` หรือ `loopThrough: "data"` + `loopData` array
3. **loop-breakpoint** edges วิ่งออกไปยัง node ถัดไปใน loop (ไม่ใช่กลับ)
4. **repeat-task** ใช้สำหรับ repeating actions ภายใน loop
5. **increase-variable** ใช้เป็น counter แทนการใช้ loop-data index

---

## การสร้าง Workflow — ขั้นตอน (แก้ไขจากของจริง)

1. **วางโครงสร้าง** — เลือก pattern (ส่วนใหญ่ใช้ Pattern 2: Loop)
2. **สร้าง trigger node** — type: manual, พร้อม parameters
3. **สร้าง variable pipeline** — random → read-file → split-data
4. **สร้าง loop** — loop-data → loop-breakpoint
5. **สร้าง actions** — open-url → element-exists → event-click → delay
6. **สร้าง conditions** — สำหรับ branch logic
7. **สร้าง data recording** — clipboard → file-action → insert-data
8. **Validate**:
   - [ ] ทุก node มี label (top-level)
   - [ ] label ต้องเป็นค่าที่ GL รองรับ (event-click, open-url, ฯลฯ)
   - [ ] trigger parameters ครบ
   - [ ] edges sourceHandle ถูก pattern
   - [ ] conditions ใช้ nested schema 3-level
   - [ ] delay ใช้ correct format
   - [ ] javascript-code ไม่มี IIFE
   - [ ] มี trigger + end node
