# (Facebook) View Live 2.0 — Workflow Knowledge Reference

Learned from: `(Facebook) View Live 2.0.gemlogin` on 2026-07-17
114 nodes · 186 edges · 27 unique XPaths · GemLogin extVersion 2

## Overview

เข้า Facebook Live → ดูตามเวลาที่กำหนด → ทำ Reaction (เลือกแบบเดี่ยว/สุ่ม) → คอมเมนต์ → แชร์

รองรับทั้ง **Profile Live** (V1) และ **Page Live** (V2) ซึ่งมี DOM structure ต่างกัน

## Architecture Flow

```
TRIGGER (params)
  → File Read (Page UID, comment, share caption)
  → Identity Management
    → Validate (personal XOR page)
    → Open facebook.com/profile
    → Inspect current identity
    → Switch if needed (Page: Switch Now / Personal: Switch to {name})
    → Verify identity
  → Open Live URL
  → reaction-checkbox-resolver (JS: เลือก reaction จาก checkbox + ตรวจจับ Page/Profile)
  → page-live-check (branch: /watch/live/ = page, else = profile)
    ├─ Page Live (V2): enter live → confirm viewer → reactions → comment → share
    └─ Profile Live (V1): play video (fallback=already playing) → reactions → comment → share
  → Live watch delay ({{liveStreamViewDuration}} seconds)
  → END
```

## Identity Management — XPaths

| # | XPath | Use |
|---|---|---|
| 1 | `//div[@role='button' and @aria-label='Switch Now']` | Switch to Page หลังจากเปิด `profile.php?id={{pageUid}}` |
| 2 | `//div[@role='button' and @aria-label='Your profile']` | เปิด menu profile ส่วนตัว |
| 3 | `//div[@role='dialog' and @aria-label='Your profile']//div[@role='button' and starts-with(@aria-label,'Switch to ')]` | **อ่านชื่อ** personal profile จาก DOM (ไม่ hardcode) |
| 4 | `//div[@role='button' and @aria-label='Switch to {{variables.personalProfileName}}']` | กดสลับกลับไป personal profile |

### Identity Check JS Logic
```javascript
// ตรวจจับว่าเป็น Page ไหมจาก body text
const isPage = text.includes('Manage Page') || text.includes('จัดการเพจ');
const currentUid = new URL(location.href).searchParams.get('id') || '';
// route: 'ready' | 'switch-page' | 'switch-personal'
```

---

## Page vs Profile Detection

```javascript
// reaction-checkbox-resolver
live_layout = location.pathname.startsWith('/watch/live/') ? 'page' : 'profile';
```

- `/watch/live/` → **Page Live** → ใช้ V2 selectors (scope ใน `Video Viewer` dialog)
- อื่นๆ → **Profile Live** → ใช้ V1 selectors (scope ในหน้าหลัก)

---

## Live Video Entry — XPaths

| # | XPath | Context |
|---|---|---|
| 5 | `//div[@role='group' and @aria-label='Video player']/div[@role='presentation']` | **Enter Live** — กดที่ video player เพื่อเข้า (V2) |
| 6 | `//div[@role='dialog' and @aria-label='Video Viewer']` | **Confirm** — เช็คว่า Video Viewer dialog เปิดแล้ว (V2) |
| 7 | `//div[@role="group" and @aria-label="Video player"]//div[@role="button" and @aria-label="Play video"]` | **Play video** — Profile Live ที่ยังไม่เล่น; fallback = เล่นอยู่แล้ว |

---

## Reactions — XPaths

### V1 (Profile Live) — scope ไม่มี Video Viewer container

| Action | XPath |
|---|---|
| **Hover** (เปิด reaction menu) | `//div[@role="button" and not(ancestor::*[@role="article"]) and (@aria-label="React" or (starts-with(@aria-label,"Change ") and contains(@aria-label," reaction")))]` |
| **Click Like** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Like"]` |
| **Click Love** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Love"]` |
| **Click Care** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Care"]` |
| **Click Haha** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Haha"]` |
| **Click Wow** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Wow"]` |
| **Click Sad** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Sad"]` |
| **Click Angry** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Angry"]` |

### V2 (Page Live) — scope starts from Video Viewer dialog → complementary sidebar

| Action | XPath |
|---|---|
| **Hover** (เปิด reaction menu) | `//div[@role="dialog" and @aria-label="Video Viewer"]//*[@role="complementary"]//div[@role="button" and @aria-label="Send this to friends or post it on your profile."]/ancestor::div[2]//div[@role="button" and (@aria-label="React" or (starts-with(@aria-label,"Change ") and contains(@aria-label," reaction")))]` |
| **Click reactions** | Same as V1 — `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="..."]` |

### Reaction Selection Logic
```javascript
// reaction-checkbox-resolver
const all = ['like', 'love', 'care', 'haha', 'wow', 'sad', 'angry'];
const selected = all.filter(name => isChecked(RefData('variables', `reaction_${name}`)));
const pool = selected.length ? selected : all;  // ถ้าไม่เลือกเลย = สุ่มทั้งหมด
const reaction = pool.length === 1 ? pool[0] : pool[Math.floor(Math.random() * pool.length)];
```

### Random Reaction (เมื่อเลือก random)
- สุ่มเลข 1-6 → match กับ reaction ใน random-reaction-cond
- ใช้ V1/V2 hover + click ตาม context

---

## Comment — XPaths

| # | XPath | Use |
|---|---|---|
| 8 | `//div[@role="textbox" and (@aria-label="Write a comment…" or starts-with(@aria-label,"Comment as "))]` | **ช่องพิมพ์คอมเมนต์** — รองรับทั้ง Write a comment… และ Comment as {name} |
| 9 | `//div[@role="button" and @aria-label="Post comment"]` | **โพสต์คอมเมนต์** |

### Comment Flow
1. `delay-comment` (random)
2. `file-read-comment` → อ่านจาก text file
3. `file-normalize-comment` → validate + normalize
4. `comment-type` → พิมพ์ลง textbox (`press-key`, multiple-keys)
5. `comment-post` → กด Post

---

## Share — XPaths

| # | XPath | Use |
|---|---|---|
| 10 | `//div[@role="button" and @aria-label="Send this to friends or post it on your profile."]` | **เปิด share dialog** (Profile Live) |
| 11 | `//div[@role="dialog" and @aria-label="Video Viewer"]//*[@role="complementary"]//div[@role="button" and @aria-label="Send this to friends or post it on your profile."]` | **เปิด share dialog** (Page Live fallback — scope ใน sidebar) |
| 12 | `//div[@role="dialog" and .//div[@role="button" and @aria-label="Share now"]]//div[@role="textbox"]` | **พิมพ์ share caption** — scope ใน dialog ที่มีปุ่ม Share now |
| 13 | `//div[@role='button' and starts-with(@aria-label,'Edit privacy. Sharing with Public')]` | **ตรวจสอบ** ว่า audience เป็น Public อยู่แล้ว |
| 14 | `//div[@role='dialog']//div[@role='button' and @aria-label='Share now']` | **กด Share now** — scope ใน dialog |

### Public Audience Fallback (ถ้าไม่ใช่ Public)
| # | XPath | Use |
|---|---|---|
| 15 | `//div[@role='button' and starts-with(@aria-label,'Edit privacy. Sharing with')]` | เปิด audience selector |
| 16 | `//div[@role='dialog']//span[normalize-space(.)='Public']` | เลือก Public |
| 17 | `//div[@role='button' and @aria-label='Done with privacy audience selection and close dialog']` | กด Done |

### Share Flow
1. `delay-share` (random)
2. `file-read-share-caption` → อ่าน caption จาก text file
3. `share-open` (Profile) หรือ `share-open-page-fallback` (Page)
4. `share-caption` → พิมพ์ caption ลง textbox
5. `share-public-check` → เช็คว่าเป็น Public ไหม
   - **ใช่**: `share-now`
   - **ไม่ใช่**: `public-open-fallback` → `public-select-fallback` → `public-done-fallback` → `share-now`

---

## Key Patterns & Techniques

### 1. Hover-then-Click Pattern (ทุก reaction)
```
hover-element → event-click
```
- Hover ที่ปุ่ม React/Change reaction เพื่อเปิด reaction menu
- แล้ว click reaction ที่ต้องการใน dialog `@aria-label="Reactions"`

### 2. Main + Fallback Edge
ทุก `BlockBasicWithFallback` มี 2 outputs:
- `output-1`: success
- `output-fallback`: fail → fallback path (หรือ skip)

### 3. ไม่ Hardcode ชื่อ Person
```xpath
//div[@role='button' and @aria-label='Switch to {{variables.personalProfileName}}']
```
ใช้ `get-text` block อ่านชื่อจาก aria-label `Switch to {name}` แล้วเก็บลง variable `personalProfileName`

### 4. Random Delays
ทุกขั้นตอนหลักมี random delay เพื่อเลียนแบบมนุษย์:
- Identity switch: 2-4s / 2.5-5s
- Reaction: delay ก่อน reaction
- Comment: delay ก่อน comment
- Share: delay ก่อน share
- Live watch: `{{liveStreamViewDuration}}` (ตั้งค่าจาก parameter, default 20s)

### 5. File Input Pattern
```
read-file-text → JS normalize/validate → variable
```
- อ่านไฟล์ → เก็บลง `raw_xxx`
- JS block validate + normalize → เก็บลง `xxx`
- Throw error ถ้า invalid

### 6. Condition Branching
ทุก action (reaction/comment/share) มี checkbox `enable_xxx` + conditions block:
- `do-xxx`: ทำ action
- `skip-xxx`: ข้าม
- `fallback`: ข้าม (default)

---

## Trigger Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePersonalProfile` | checkbox | true | ใช้โปรไฟล์ส่วนตัว |
| `usePageProfile` | checkbox | false | ใช้เพจ |
| `pageUidFilePath` | filepath | Page UID.txt | ไฟล์ Page UID (ตัวเลข) |
| `live_url` | string | facebook.com/Reuters/videos/... | Live URL |
| `liveStreamViewDuration` | number | 20 | ระยะเวลาดู Live (วินาที) |
| `enable_reaction` | checkbox | true | ทำแสดงความรู้สึก |
| `reaction_like` ~ `reaction_angry` | checkbox | love=true | เลือก reaction |
| `enable_comment` | checkbox | true | ทำคอมเมนต์ |
| `commentTextFilePath` | filepath | Comment.txt | ไฟล์ข้อความคอมเมนต์ |
| `enable_share` | checkbox | true | ทำแชร์ |
| `shareCaptionFilePath` | filepath | Caption Share.txt | ไฟล์แชร์แคปชั่น |

---

## Files Referenced
- Page UID: `/Users/pajipan/Documents/YuYu/Live/Page UID.txt`
- Comment: `/Users/pajipan/Documents/YuYu/Live/Comment.txt`
- Share Caption: `/Users/pajipan/Documents/YuYu/Live/Caption Share.txt`
