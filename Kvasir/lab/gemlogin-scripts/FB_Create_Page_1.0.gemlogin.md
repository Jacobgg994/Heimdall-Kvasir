# [Demo] Facebook Create Page 1.0

> ออกแบบโดย JIMMY 🌊 | 4 ก.ค. 2026
> อ้างอิงจาก: 801 corpus (Create Page 1.1), GEMMY block-reference, real-examples
> สร้างโดย: GEMMY 💎

---

## ภาพรวม

- **ชื่อ:** [Demo] Facebook Create Page 1.0
- **วัตถุประสงค์:** สร้าง Facebook Page ใหม่ พร้อมตั้งชื่อ, รูปโปรไฟล์, รูปปก, และ Bio
- **Pattern:** Pattern 2 (Loop with Data Processing)
- **Nodes:** ~45
- **Edges:** ~52

---

## Trigger Parameters

```
📝 ตั้งค่าเพจ
  ├─ filepath  pageNameFile       "ไฟล์ชื่อเพจ (.txt)"
  ├─ filepath  categoryFile       "ไฟล์หมวดหมู่ (.txt)"
  ├─ filepath  profilePicFolder   "โฟลเดอร์รูปโปรไฟล์"
  ├─ filepath  coverPicFolder     "โฟลเดอร์รูปปก"
  ├─ filepath  bioFile            "ไฟล์ Bio/Description (.txt)"
  ├─ number    pagesToCreate      "จำนวนเพจที่สร้าง"        default: 1
  └─ checkbox  deleteUsedNames    "ลบชื่อที่ใช้แล้ว"         default: true

⏱️ ตั้งค่าเวลา
  ├─ number    minDelay           "หน่วงต่ำสุด (วิ)"        default: 3
  └─ number    maxDelay           "หน่วงสูงสุด (วิ)"        default: 7
```

---

## Flow Diagram

```
[trigger]
  ↓
[random: delay 3-7] → {{variables.delay}}
  ↓
[read-file-text: ชื่อเพจ] → {{variables.pageName}} (aline, random)
  ↓
[read-file-text: หมวดหมู่] → {{variables.category}} (aline, random)
  ↓
[read-file-text: Bio] → {{variables.bio}} (aline, random)
  ↓
[get-file-path: รูปโปรไฟล์] → {{variables.profilePic}}
  ↓
[get-file-path: รูปปก] → {{variables.coverPic}}
  ↓
[loop-data: mainloop, numbers, 1 to {{variables.pagesToCreate}}]
  ↓
[read-file-text: ชื่อเพจ] → {{variables.pageName}} (aline, random, deleteLine)
  ↓
  ===== STEP 1: เปิด Facebook + ไปที่หน้า Pages =====
  ↓
[open-url: https://www.facebook.com/pages/?category=your_pages]
  ↓
[tab-loaded]
  ↓
[delay: {{variables.delay}}000]
  ↓
  ===== STEP 2: คลิกปุ่ม Create Page =====
  ↓
[element-exists: ปุ่ม Create Page]
  selector: //span[contains(text(),"Create") or contains(text(),"สร้าง")]/ancestor::a[@role="link"]
  หรือ: //a[@aria-label="Create new Page"]
  ↓
[conditions: เจอปุ่ม Create?]
  ├─ match: → [event-click: ปุ่ม Create Page]
  │           [delay: 3000]
  └─ fallback: → [open-url: https://www.facebook.com/pages/create]
                  [tab-loaded]
                  [delay: 3000]
  ↓
  ===== STEP 3: กรอกชื่อเพจ =====
  ↓
[element-exists: ช่องกรอกชื่อเพจ]
  selector (Left side panel): //span[text()="Page name (required)"]/following-sibling::input
  หรือ: //input[@aria-label="Page name (required)"]
  ↓
[conditions: เจอช่องชื่อ?]
  ├─ match:
  │   [press-key: พิมพ์ชื่อเพจ]
  │   selector: //span[text()="Page name (required)"]/following-sibling::input
  │   keysToPress: {{variables.pageName}}
  │   action: multiple-keys
  │   pressTime: 100
  │   delay: 2000
  └─ fallback: → [insert-data: ไม่พบช่องกรอกชื่อเพจ — FAIL]
                  [end]
  ↓
  ===== STEP 4: เลือกหมวดหมู่ =====
  ↓
[element-exists: ช่องกรอกหมวดหมู่]
  selector: //span[text()="Category (required)"]/following-sibling::input
  หรือ: //input[@aria-label="Category"]
  ↓
[conditions: เจอช่องหมวดหมู่?]
  ├─ match:
  │   [event-click: คลิกช่องหมวดหมู่]
  │   delay: 1000
  │   [press-key: พิมพ์หมวดหมู่]
  │   keysToPress: {{variables.category}}
  │   delay: 2000
  │   [element-exists: dropdown ผลลัพธ์]
  │   selector: //ul[@role="listbox"]//li[1]
  │   [conditions: เจอ dropdown?]
  │   ├─ match: → [event-click: เลือกอันแรกจาก dropdown]
  │   └─ fallback: → [press-key: กด Enter]
  │   delay: 1500
  └─ fallback: → [insert-data: ไม่พบช่องหมวดหมู่ — FAIL]
  ↓
  ===== STEP 5: กรอก Bio / Description =====
  ↓
[element-exists: ช่อง Bio]
  selector: //span[text()="Description" or text()="Bio"]/following-sibling::textarea
  หรือ: //textarea[@aria-label="Description"] หรือ //div[@contenteditable="true" and contains(@aria-label,"Description")]
  ↓
[conditions: เจอช่อง Bio?]
  ├─ match:
  │   [event-click: คลิกช่อง Bio]
  │   delay: 1000
  │   [forms: กรอก Bio]
  │   type: text-field
  │   value: {{variables.bio}}
  │   typingDelay: 30
  │   clearValue: true
  │   delay: 2000
  └─ fallback: → skip (Bio อาจเป็น optional)
  ↓
  ===== STEP 6: กด Create Page =====
  ↓
[event-click: ปุ่ม "Create Page"]
  selector: //div[@role="button"]//span[text()="Create Page" or text()="Create"]/ancestor::div[@role="button"]
  ↓
[delay: 5000] → รอระบบสร้างเพจ
  ↓
[tab-loaded] → รอหน้าโหลดสมบูรณ์
  ↓
  ===== STEP 7: ตรวจสอบว่าเพจถูกสร้างแล้ว =====
  ↓
[element-exists: ตรวจว่าเข้า page ใหม่แล้ว]
  selector (มีปุ่ม Edit Page หรือ See Page): //span[contains(text(),"Edit") or contains(text(),"Switch")]
  หรือ: //div[@aria-label="Switch Now" or @aria-label="Edit Page"]
  ↓
[conditions: สร้างเพจสำเร็จ?]
  ├─ match:
  │   ===== STEP 8: อัปโหลดรูปโปรไฟล์ =====
  │   ↓
  │   [element-exists: ปุ่ม Add Profile Picture]
  │   selector: //span[contains(text(),"Add profile picture") or contains(text(),"Add picture")]
  │   หรือ: //div[@aria-label="Add profile picture"]
  │   ↓
  │   [conditions: เจอปุ่มรูปโปรไฟล์?]
  │   ├─ match:
  │   │   [event-click: ปุ่ม Add Profile Picture]
  │   │   delay: 2000
  │   │   [upload-file: {{variables.profilePic}}]
  │   │   selector: //span[contains(text(),"Add profile picture")]
  │   │   delay: 5000 → รออัปโหลด
  │   │   [element-exists: ปุ่ม Save/Crop]
  │   │   selector: //div[@role="button"]//span[text()="Save"]
  │   │   [conditions: เจอปุ่ม Save?]
  │   │   ├─ match: → [event-click: Save] → delay: 3000
  │   │   └─ fallback: → skip (ไม่มี crop dialog)
  │   └─ fallback: → skip
  │   ↓
  │   ===== STEP 9: อัปโหลดรูปปก =====
  │   ↓
  │   [element-exists: ปุ่ม Add Cover Photo]
  │   selector: //span[contains(text(),"Add cover photo") or contains(text(),"Add a cover")]
  │   หรือ: //div[@aria-label="Add cover photo"]
  │   ↓
  │   [conditions: เจอปุ่มรูปปก?]
  │   ├─ match:
  │   │   [event-click: ปุ่ม Add Cover Photo]
  │   │   delay: 2000
  │   │   [event-click: "Upload Photo" ถ้ามี popup]
  │   │   delay: 1000
  │   │   [upload-file: {{variables.coverPic}}]
  │   │   delay: 5000 → รออัปโหลด
  │   │   [element-exists: ปุ่ม Save]
  │   │   selector: //div[@role="button"]//span[text()="Save changes"]
  │   │   [conditions: เจอปุ่ม Save?]
  │   │   ├─ match: → [event-click: Save] → delay: 3000
  │   │   └─ fallback: → skip
  │   └─ fallback: → skip
  │   ↓
  │   ===== STEP 10: เก็บข้อมูลเพจ =====
  │   ↓
  │   [clipboard: เก็บ URL ปัจจุบัน] → {{variables.pageUrl}}
  │   type: get
  │   assignVariable: true
  │   variableName: pageUrl
  │   ↓
  │   [file-action: บันทึกเพจที่สร้างแล้ว]
  │   filePath: {{variables.outputFolder}}/created_pages.txt
  │   inputData: {{variables.pageName}}|{{variables.pageUrl}}|{{variables.category}}|{{profileName}}|{{$date}}
  │   writeMode: append
  │   ↓
  │   [insert-data: บันทึกลง data table]
  │   dataList:
  │     - type: variable, name: pageName, value: {{variables.pageName}}
  │     - type: variable, name: pageUrl, value: {{variables.pageUrl}}
  │     - type: variable, name: category, value: {{variables.category}}
  │     - type: variable, name: profileName, value: {{profileName}}
  │     - type: variable, name: result, value: SUCCESS
  │   ↓
  └─ fallback: → [insert-data: สร้างเพจไม่สำเร็จ — {{variables.pageName}}]
                  [file-action: บันทึก failed — {{variables.pageName}}|FAILED|{{$date}}]
  ↓
[loop-breakpoint: mainloop]
  ↓
[end]
```

---

## XPath Selectors

| ขั้นตอน | Element | XPath |
|---------|---------|-------|
| Step 2 | ปุ่ม Create Page | `//span[contains(text(),"Create")]/ancestor::a[@role="link"]` |
| Step 2 alt | หรือ | `//a[@aria-label="Create new Page"]` |
| Step 3 | ช่องชื่อเพจ | `//span[text()="Page name (required)"]/following-sibling::input` |
| Step 3 alt | หรือ | `//input[contains(@aria-label,"Page name")]` |
| Step 4 | ช่องหมวดหมู่ | `//span[text()="Category (required)"]/following-sibling::input` |
| Step 4 dropdown | เลือกหมวดหมู่ | `//ul[@role="listbox"]//li[1]` |
| Step 5 | ช่อง Bio | `//span[text()="Description"]/following-sibling::textarea` |
| Step 5 alt | หรือ | `//textarea[@aria-label="Description"]` |
| Step 6 | ปุ่ม Create Page | `//div[@role="button"]//span[text()="Create Page"]/ancestor::div[@role="button"]` |
| Step 6 alt | หรือ | `//div[@role="button"]//span[text()="Create"]/ancestor::div[@role="button"]` |
| Step 7 | ตรวจเพจสร้างแล้ว | `//span[contains(text(),"Switch Now") or contains(text(),"Edit Page")]` |
| Step 8 | ปุ่มรูปโปรไฟล์ | `//span[contains(text(),"Add profile picture") or contains(text(),"Add picture")]` |
| Step 8 Save | ปุ่มเซฟรูป | `//div[@role="button"]//span[text()="Save"]` |
| Step 9 | ปุ่มรูปปก | `//span[contains(text(),"Add cover photo") or contains(text(),"Add a cover")]` |
| Step 9 Save | ปุ่มเซฟปก | `//div[@role="button"]//span[text()="Save changes"]` |

---

## Facebook Create Page UI Variations

⚠️ Facebook มี 2 รูปแบบหน้าสร้างเพจ:

### แบบ A: Classic Create (common)
```
Left Panel: ชื่อเพจ + หมวดหมู่ + Bio
Right Panel: Preview แสดงผลลัพธ์
```

### แบบ B: New Create Flow (AB test)
```
Full-page wizard ทีละขั้นตอน
Step 1: ชื่อเพจ → Next
Step 2: หมวดหมู่ → Next
Step 3: Bio → Next
Step 4: รูปโปรไฟล์ → Next
Step 5: รูปปก → Done
```

สคริปต์นี้ใช้ **แบบ A** เป็นหลัก — ถ้าเจอแบบ B ให้ใช้ `element-exists` เช็คปุ่ม "Next" และเปลี่ยน flow

---

## Error Handling

| สถานการณ์ | การจัดการ |
|-----------|----------|
| เจอหน้า login | login flow (email → password → submit) → กลับไปที่ Step 1 |
| เจอ checkpoint | insert-data: checkpoint detected → end (manual intervention needed) |
| Page name ซ้ำ | element-exists: ตรวจ error message → insert-data: name taken → read-file-text: ชื่อใหม่ → retry |
| Category ไม่ขึ้น dropdown | press-key: Enter → ใช้ข้อความที่พิมพ์ตรงๆ |
| อัปโหลดรูปล้มเหลว | insert-data: upload failed → ไปต่อโดยไม่มีรูป |
| สร้างเพจไม่สำเร็จ | file-action: บันทึก failed → loop-breakpoint → ไปสร้างเพจต่อไป |

---

## Data Recording

```
ไฟล์ created_pages.txt:
  format: {{pageName}}|{{pageUrl}}|{{category}}|{{profileName}}|{{$date}}

ไฟล์ failed_pages.txt:
  format: {{pageName}}|FAILED|{{reason}}|{{profileName}}|{{$date}}

data table insert:
  - pageName, pageUrl, category, bio, profileName, result (SUCCESS/FAILED), date
```

---

## Schema Validation Checklist

- [ ] trigger มี type: "manual" + parameters ครบ
- [ ] ทุก node มี label ที่ top-level (n['label'])
- [ ] fields ครบตาม label (check field matrix)
- [ ] conditions ใช้ nested schema 3-level
- [ ] edges sourceHandle ถูกต้อง (output-{group_id} / output-fallback)
- [ ] delay ใช้ number หรือ "N,M" format
- [ ] javascript-code (ถ้ามี) ไม่มี IIFE
- [ ] press-key ไม่มี $breakpoint (ยกเว้นต้องการ break loop)
- [ ] upload-file มี filePaths array
- [ ] forms type: "text-field", มี typingDelay
- [ ] มี trigger + end node

---

## Notes

1. **Page name requirements:** Facebook กำหนดชื่อเพจต้องไม่ซ้ำ และห้ามใช้คำต้องห้าม — แนะนำให้เตรียมชื่อสำรองไว้ในไฟล์
2. **Category requirements:** ต้องเป็นหมวดหมู่ที่มีใน Facebook — ทดสอบ dropdown ก่อน scale
3. **Rate limit:** สร้างเพจมากเกิน → Facebook อาจบล็อค — แนะนำ 1-3 เพจต่อวันต่อ profile
4. **New Page UI:** Facebook เปลี่ยน UI บ่อย — ต้อง test XPath ก่อน deploy จริง
5. **Profile warm:** profile ใหม่สร้างเพจอาจติด checkpoint — ควร warm 2-3 วันก่อน

---

*🤖 JIMMY 🌊 — Kvasir AI Companion*
