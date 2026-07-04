# 📘 GemLogin Facebook Script Suite — 7 สคริปต์

> ออกแบบโดย JIMMY 🌊 | 4 ก.ค. 2026
> สร้างโดย: GEMMY 💎 | ตรวจสอบ: JIMMY 🌊
> อ้างอิงจาก: 801 corpus, GEMMY block-reference, workflow-patterns
> ยังไม่ commit — รอ Jacob อนุมัติ

---

## 🎯 ภาพรวม — Facebook Script Suite

| # | สคริปต์ | ใช้ใน Broadcast Plan | ความซับซ้อน | Nodes |
|---|---------|---------------------|------------|-------|
| 1 | 📝 FB Auto Post | อ-ศ โพสต์ข้อความ+รูป | ⭐⭐⭐ สูง | ~35 |
| 2 | 👍 FB Like & Follow | จ-ส ไลค์+ติดตาม | ⭐⭐ กลาง | ~30 |
| 3 | 💬 FB Comment | อ-พฤ คอมเมนต์ | ⭐⭐ กลาง | ~25 |
| 4 | 🔄 FB Share | จ-ศ แชร์โพสต์ | ⭐⭐ กลาง | ~25 |
| 5 | 🔥 FB Profile Warm | จ-อ Warm-up profile ใหม่ | ⭐⭐⭐⭐ สูงมาก | ~70 |
| 6 | 👥 FB Join Group | พฤ เข้ากลุ่ม+แนะนำตัว | ⭐ ง่าย | ~15 |
| 7 | 🩺 FB Status Check | อา เช็คสถานะ+Metrics | ⭐ ง่าย | ~12 |

---

## 📐 Script 1: FB Auto Post

**ชื่อไฟล์:** `[Demo] FB Auto Post 1.0.gemlogin`
**Pattern:** Pattern 2 (Loop)
**Nodes:** ~35

### 🎮 Trigger Parameters

```
📝 ตั้งค่าการโพสต์
  ├─ filepath  captionFolder   "โฟลเดอร์แคปชั่น (.txt)"
  ├─ filepath  mediaFolder     "โฟลเดอร์รูปภาพ"
  ├─ checkbox  postToWall      "โพสต์บน Wall"            default: true
  ├─ checkbox  postToGroup     "โพสต์ใน Group"           default: false
  ├─ filepath  groupLinksFile  "ไฟล์ลิงก์ Group (.txt)"   (แสดงเมื่อ postToGroup=true)
  ├─ checkbox  postWithImage   "โพสต์พร้อมรูป"            default: true
  ├─ checkbox  postWithVideo   "โพสต์วิดีโอ"              default: false
  ├─ number    postCount       "จำนวนโพสต์"               default: 5
  └─ checkbox  deleteUsed      "ลบไฟล์ที่ใช้แล้ว"          default: false

⏱️ ตั้งค่าเวลา
  ├─ number    minDelay        "หน่วงเวลาต่ำสุด (วิ)"      default: 3
  └─ number    maxDelay        "หน่วงเวลาสูงสุด (วิ)"      default: 8
```

### 🔄 Flow

```
trigger
  → random: สุ่ม delay
  → read-file-text: อ่านแคปชั่น
  → loop-data: mainloop (1 ถึง postCount)
    → conditions: postToGroup?
      ├─ match: read-file-text: อ่าน group link
      │         open-url: หน้ากลุ่ม
      └─ fallback: open-url: facebook.com
    → tab-loaded
    → element-exists: ตรวจ login
    → conditions: need login?
      ├─ match: login flow (email → password → submit)
      └─ fallback: ไปต่อ
    → conditions: postToWall?
      ├─ match: event-click: "What's on your mind"
      └─ fallback: event-click: "Write something..." (group)
    → delay: {{variables.delay}}000
    → conditions: postWithImage?
      ├─ match: event-click: "Photo/video"
      │         get-file-path: สุ่มรูป
      │         upload-file: {{variables.mediaFile}}
      │         delay: 5000 (รออัปโหลด)
      └─ fallback: skip
    → conditions: postWithVideo?
      ├─ match: (similar flow สำหรับวิดีโอ)
      └─ fallback: skip
    → forms: เขียนแคปชั่น (text-field, typingDelay: 50)
    → delay: 2000
    → event-click: ปุ่ม Post
    → delay: 5000
    → element-exists: ตรวจโพสต์สำเร็จ
    → conditions: success?
      ├─ match: clipboard: เก็บลิงก์โพสต์
      │         file-action: บันทึก output.txt
      │         insert-data: บันทึกลง data table
      │         increase-variable: successCount
      └─ fallback: insert-data: โพสต์ไม่สำเร็จ
    → loop-breakpoint
  → end
```

### 🔑 XPath

| จุด | XPath |
|-----|-------|
| ปุ่มสร้างโพสต์ (Wall) | `//div[@role="button"]//span[contains(text(),"What's on your mind")]/ancestor::div[@role="button"]` |
| ปุ่มสร้างโพสต์ (Group) | `//div[@role="button"]//span[contains(text(),"Write something")]/ancestor::div[@role="button"]` |
| ช่องเขียนโพสต์ | `//div[@role="textbox" and starts-with(@aria-placeholder,"What's on your mind") or @contenteditable="true"]` |
| ปุ่ม Photo/Video | `//div[@aria-label="Photo/video"]` |
| ปุ่ม Post | `//div[@role="button"]//span[text()="Post"]/ancestor::div[@role="button"]` |
| ตรวจโพสต์สำเร็จ | `//span[contains(text(),"Shared") or contains(text(),"posted") or contains(text(),"แชร์แล้ว")]` |
| ช่อง Email (login) | `//input[@id="email" or @name="email" or @aria-label="Email"]` |
| ช่อง Password | `//input[@id="pass" or @name="pass" or @aria-label="Password"]` |
| ปุ่ม Log In | `//button[@name="login" or @id="loginbutton"]` |

---

## 📐 Script 2: FB Like & Follow

**ชื่อไฟล์:** `[Demo] FB Like & Follow 1.0.gemlogin`
**Pattern:** Pattern 2 (Loop) + Pattern 4 (Conditions Branch)
**Nodes:** ~30

### 🎮 Trigger Parameters

```
🎯 ตั้งค่าเป้าหมาย
  ├─ filepath  targetsFile     "ไฟล์ลิงก์เป้าหมาย (.txt)"
  ├─ checkbox  enableLike      "เปิด Like"               default: true
  ├─ checkbox  enableFollow    "เปิด Follow"             default: true
  ├─ checkbox  randomReact     "สุ่ม Reaction (Love/Care/Wow)" default: true
  ├─ number    actionsCount    "จำนวน action"            default: 10
  └─ checkbox  scrollFirst     "เลื่อนฟีดก่อนเริ่ม"        default: true

⏱️ ตั้งค่าเวลา
  ├─ number    minDelay        "หน่วงต่ำสุด (วิ)"         default: 2
  └─ number    maxDelay        "หน่วงสูงสุด (วิ)"         default: 5
```

### 🔄 Flow

```
trigger
  → random: สุ่ม delay
  → read-file-text: อ่านไฟล์เป้าหมาย (aline, random, deleteLine)
  → loop-data: mainloop (1 ถึง actionsCount)
    → read-file-text: ดึงลิงก์ถัดไป → {{variables.currentTarget}}
    → open-url: {{variables.currentTarget}}
    → tab-loaded
    → delay: {{variables.delay}}000
    → conditions: scrollFirst?
      ├─ match: element-scroll: เลื่อน 300-600px
      └─ fallback: skip
    → element-exists: ตรวจว่าเจอปุ่ม Like หรือ Follow
    → conditions: enableFollow?
      ├─ match:
      │   element-exists: ปุ่ม Follow
      │   conditions: เจอปุ่ม Follow?
      │   ├─ match: event-click: กด Follow
      │   │         delay: {{variables.delay}}000
      │   └─ fallback: insert-data: ไม่พบปุ่ม Follow → ข้าม
      └─ fallback: skip
    → conditions: enableLike?
      ├─ match:
      │   element-exists: ปุ่ม Like
      │   conditions: เจอปุ่ม Like?
      │   ├─ match:
      │   │   conditions: randomReact?
      │   │   ├─ match:
      │   │   │   random: สุ่ม 1-4 → {{variables.reactType}}
      │   │   │   conditions: reactType
      │   │   │   ├─ 1: event-click: Like ปกติ
      │   │   │   ├─ 2: hover-element → delay → event-click: Love
      │   │   │   ├─ 3: hover-element → delay → event-click: Care
      │   │   │   └─ 4: hover-element → delay → event-click: Like (normal)
      │   │   └─ fallback: event-click: กด Like ปกติ
      │   │   delay: {{variables.delay}}000
      │   └─ fallback: insert-data: ไม่พบปุ่ม Like → ข้าม
      └─ fallback: skip
    → insert-data: บันทึก — targetUrl, actionType, profileName, date
    → delay: {{variables.delay}}000
    → loop-breakpoint
  → end
```

### 🔑 XPath

| จุด | XPath |
|-----|-------|
| ปุ่ม Like (ยังไม่กด) | `//div[@aria-label="Like" and not(contains(@aria-label,"Unlike"))]` |
| ปุ่ม Unlike (กดแล้ว) | `//div[contains(@aria-label,"Unlike")]` |
| ปุ่ม Love (หลัง hover) | `//div[@aria-label="Love" or @aria-label="หลงรัก"]` |
| ปุ่ม Care (หลัง hover) | `//div[@aria-label="Care" or @aria-label="ใส่ใจ"]` |
| ปุ่ม Follow (เพจ) | `//div[@role="button"]//span[contains(text(),"Follow") or contains(text(),"ติดตาม")]/ancestor::div[@role="button"]` |
| ปุ่ม Following (follow แล้ว) | `//div[@role="button"]//span[contains(text(),"Following") or contains(text(),"ติดตามอยู่")]` |
| ปุ่ม Add Friend | `//div[@role="button"]//span[contains(text(),"Add Friend") or contains(text(),"เพิ่มเพื่อน")]` |

---

## 📐 Script 3: FB Comment

**ชื่อไฟล์:** `[Demo] FB Comment 1.0.gemlogin`
**Pattern:** Pattern 2 (Loop)
**Nodes:** ~25

### 🎮 Trigger Parameters

```
💬 ตั้งค่าคอมเมนต์
  ├─ filepath  targetsFile     "ไฟล์ลิงก์โพสต์เป้าหมาย (.txt)"
  ├─ filepath  commentsFile    "ไฟล์ข้อความคอมเมนต์ (.txt)"
  ├─ number    commentsPerPost "คอมเมนต์ต่อโพสต์"         default: 3
  ├─ number    postsCount      "จำนวนโพสต์ที่คอมเมนต์"     default: 10
  └─ checkbox  deleteUsed      "ลบคอมเมนต์ที่ใช้แล้ว"      default: false

⏱️ ตั้งค่าเวลา
  ├─ number    minDelay        "หน่วงต่ำสุด (วิ)"         default: 3
  └─ number    maxDelay        "หน่วงสูงสุด (วิ)"         default: 7
```

### 🔄 Flow

```
trigger
  → random: delay
  → read-file-text: คอมเมนต์ (aline, random)
  → loop-data: mainloop (1 ถึง postsCount)
    → read-file-text: ลิงก์โพสต์ → {{variables.postUrl}}
    → open-url: {{variables.postUrl}}
    → tab-loaded
    → delay: {{variables.delay}}000
    → element-scroll: เลื่อนไปช่องคอมเมนต์
    → repeat-task: innerLoop (1 ถึง commentsPerPost)
      → read-file-text: คอมเมนต์ → {{variables.comment}}
      → element-exists: ช่องคอมเมนต์
        selector: //div[@role="textbox" and @contenteditable="true" and contains(@aria-label,"Comment")]
      → conditions: เจอช่องคอมเมนต์?
        ├─ match:
        │   event-click: คลิกช่องคอมเมนต์
        │   delay: 1000
        │   press-key: พิมพ์ {{variables.comment}}
        │   delay: 1500
        │   event-click: กด Enter (ส่งคอมเมนต์)
        │   delay: {{variables.delay}}000
        │   insert-data: commentText, postUrl, profileName, date
        └─ fallback: insert-data: ไม่พบช่องคอมเมนต์
      → loop-breakpoint: innerLoop
    → loop-breakpoint: mainloop
  → end
```

### 🔑 XPath

| จุด | XPath |
|-----|-------|
| ช่องคอมเมนต์ (ใต้โพสต์) | `//div[@role="article"]//div[@role="textbox" and @contenteditable="true"]` |
| ช่องคอมเมนต์ (popup view) | `//div[@role="dialog"]//div[@contenteditable="true"]` |
| ปุ่มส่งคอมเมนต์ (Enter) | กด Enter โดยตรงที่ช่อง |
| คอมเมนต์ที่มีอยู่แล้ว | `//div[@role="article"]//div[contains(@aria-label,"Comment")]` |
| โหลดคอมเมนต์เพิ่ม | `//span[contains(text(),"View more comments") or contains(text(),"ดูความคิดเห็นเพิ่มเติม")]` |

---

## 📐 Script 4: FB Share

**ชื่อไฟล์:** `[Demo] FB Share 1.0.gemlogin`
**Pattern:** Pattern 2 (Loop)
**Nodes:** ~25

### 🎮 Trigger Parameters

```
🔄 ตั้งค่าแชร์
  ├─ filepath  targetsFile     "ไฟล์ลิงก์โพสต์ (.txt)"
  ├─ checkbox  shareToWall     "แชร์ไป Wall ตัวเอง"       default: true
  ├─ checkbox  shareToGroup    "แชร์ไป Group"            default: false
  ├─ filepath  groupLinksFile  "ไฟล์ลิงก์ Group (.txt)"   (แสดงเมื่อ shareToGroup=true)
  ├─ checkbox  addCaption      "เพิ่มแคปชั่นตอนแชร์"       default: false
  ├─ filepath  captionFile     "ไฟล์แคปชั่น (.txt)"       (แสดงเมื่อ addCaption=true)
  ├─ number    shareCount      "จำนวนครั้งที่แชร์"         default: 10
  └─ checkbox  deleteUsed      "ลบลิงก์ที่ใช้แล้ว"         default: true

⏱️ ตั้งค่าเวลา
  ├─ number    minDelay        "หน่วงต่ำสุด (วิ)"         default: 3
  └─ number    maxDelay        "หน่วงสูงสุด (วิ)"         default: 7
```

### 🔄 Flow

```
trigger
  → random: delay
  → loop-data: mainloop (1 ถึง shareCount)
    → read-file-text: ลิงก์โพสต์ → {{variables.postUrl}}
    → open-url: {{variables.postUrl}}
    → tab-loaded
    → delay: {{variables.delay}}000
    → event-click: ปุ่ม Share
      selector: //div[@aria-label="Share" or @aria-label="แชร์" or contains(@aria-label,"Send this")]
    → delay: 2000
    → conditions: shareToWall?
      ├─ match:
      │   event-click: "Share to Feed" หรือ "Share now"
      │   selector: //span[contains(text(),"Share now") or contains(text(),"แชร์ตอนนี้")]/ancestor::div[@role="button"]
      │   delay: 2000
      └─ fallback: skip
    → conditions: shareToGroup?
      ├─ match:
      │   event-click: "Share to a group"
      │   read-file-text: group link
      │   press-key: พิมพ์ชื่อกลุ่ม
      │   delay: 1000
      │   event-click: เลือกกลุ่มจาก dropdown
      │   delay: 1000
      └─ fallback: skip
    → conditions: addCaption?
      ├─ match:
      │   read-file-text: แคปชั่น
      │   press-key: พิมพ์แคปชั่น
      │   delay: 1000
      └─ fallback: skip
    → event-click: "Post" หรือ "Share"
    → delay: 5000
    → element-exists: ตรวจแชร์สำเร็จ
    → conditions: success?
      ├─ match: insert-data: postUrl, sharedTo, profileName, date
      │         file-action: condition: deleteUsed? → ลบลิงก์ออกจากไฟล์
      └─ fallback: insert-data: แชร์ไม่สำเร็จ
    → loop-breakpoint
  → end
```

### 🔑 XPath

| จุด | XPath |
|-----|-------|
| ปุ่ม Share (ใต้โพสต์) | `//div[@aria-label="Send this to friends or post it on your profile."]` |
| ปุ่ม Share (ตัวย่อ) | `//div[@aria-label="Share" or @aria-label="แชร์"]` |
| Share Now (Wall) | `//span[contains(text(),"Share now") or contains(text(),"แชร์ตอนนี้")]/ancestor::div[@role="button"]` |
| Share to Group | `//span[contains(text(),"Share to a group") or contains(text(),"แชร์ไปยังกลุ่ม")]` |
| ช่องค้นหากลุ่ม | `//input[@aria-label="Search for groups" or @placeholder="Search for groups"]` |
| ผลการค้นหากลุ่ม | `//ul[@role="listbox"]//li[1]` |
| ยืนยันแชร์ | `//div[@role="button"]//span[text()="Post"]/ancestor::div[@role="button"]` |

---

## 📐 Script 5: FB Profile Warm

**ชื่อไฟล์:** `[Demo] FB Warm Profile 1.0.gemlogin`
**Pattern:** Pattern 6 (Multi-Phase Processing)
**Nodes:** ~70
**⚠️ ซับซ้อนที่สุด — 7 phases**

### 🎮 Trigger Parameters

```
🔥 Phase: ทั่วไป
  ├─ number    warmDays        "จำนวนวันวอร์ม"            default: 4
  └─ number    dailyActions    "จำนวน action ต่อวัน"       default: 20

🔥 Phase 1: ตั้งค่าโปรไฟล์
  ├─ checkbox  updateProfile   "อัปเดตโปรไฟล์"            default: true
  ├─ filepath  profilePicFolder "โฟลเดอร์รูปโปรไฟล์"
  ├─ filepath  coverPicFolder  "โฟลเดอร์รูปปก"
  └─ checkbox  addBio          "เพิ่ม Bio"               default: false

🔥 Phase 2: สร้างเครือข่าย
  ├─ checkbox  addFriends      "เพิ่มเพื่อน"              default: true
  ├─ filepath  friendLinksFile "ไฟล์ลิงก์โปรไฟล์เพื่อน"
  └─ number    friendsPerDay   "เพิ่มเพื่อนต่อวัน"         default: 5

🔥 Phase 3: ติดตามเพจ
  ├─ checkbox  followPages     "ติดตามเพจ"               default: true
  ├─ filepath  pageLinksFile   "ไฟล์ลิงก์เพจ"
  └─ number    pagesPerDay     "ติดตามเพจต่อวัน"           default: 5

🔥 Phase 4: เอ็นเกจ
  ├─ checkbox  engageFeed      "ไลค์+คอมเมนต์ฟีด"         default: true
  ├─ filepath  commentsFile    "ไฟล์คอมเมนต์"
  └─ number    engagePerDay    "เอ็นเกจต่อวัน"             default: 10

🔥 Phase 5: เข้ากลุ่ม (วันที่ 3-4)
  ├─ checkbox  joinGroups      "เข้าร่วมกลุ่ม"             default: false
  ├─ filepath  groupLinksFile  "ไฟล์ลิงก์กลุ่ม"
  └─ number    groupsPerDay    "เข้ากลุ่มต่อวัน"            default: 2

⏱️ ตั้งค่าเวลา
  ├─ number    minDelay        "หน่วงต่ำสุด (วิ)"          default: 5
  └─ number    maxDelay        "หน่วงสูงสุด (วิ)"          default: 15
```

### 🔄 Flow (7 Phases)

```
PHASE 1: ตั้งค่าโปรไฟล์ (วันแรกเท่านั้น)
  trigger → conditions: updateProfile?
    ├─ match: open-url: facebook.com/profile → tab-loaded
    │         get-file-path: สุ่มรูปโปรไฟล์
    │         event-click: ปุ่มแก้ไขรูปโปรไฟล์
    │         upload-file: {{variables.profilePic}}
    │         delay: 5000
    │         event-click: Save
    │         
    │         get-file-path: สุ่มรูปปก
    │         event-click: ปุ่มแก้ไขรูปปก
    │         upload-file: {{variables.coverPic}}
    │         delay: 5000
    │         event-click: Save
    └─ fallback: skip

PHASE 2: ยืนยันตัวตน (ถ้ามี checkpoint)
  open-url: facebook.com → tab-loaded
  element-exists: ตรวจ checkpoint (ยืนยันตัวตน)
  conditions: มี checkpoint?
    ├─ match: 
    │   element-exists: ตรวจประเภท checkpoint
    │   conditions: 
    │   ├─ ขอยืนยันรูป: event-click: "Not now" หรือ "Skip"
    │   ├─ ขอยืนยันเบอร์: (skip — manual required)
    │   └─ อื่นๆ: insert-data: checkpoint type → end (หยุด)
    └─ fallback: ไปต่อ

PHASE 3: ท่องฟีด (ทุกวัน)
  open-url: facebook.com → tab-loaded
  loop-data: feedLoop (1 ถึง dailyActions)
    element-scroll: เลื่อนฟีด 500-800px
    delay: {{variables.delay}}000
    random: สุ่ม 1-3 → {{variables.feedAction}}
    conditions: feedAction
      ├─ 1 (Like): 
      │   element-exists: ปุ่ม Like ในฟีด
      │   event-click: กด Like
      ├─ 2 (Scroll): 
      │   element-scroll: เลื่อนเพิ่ม
      └─ 3 (Read): 
          delay: 3000 (จำลองอ่าน)
    loop-breakpoint: feedLoop

PHASE 4: เพิ่มเพื่อน
  conditions: addFriends?
    ├─ match:
    │   loop-data: friendLoop (1 ถึง friendsPerDay)
    │     read-file-text: profile link → {{variables.friendUrl}}
    │     open-url: {{variables.friendUrl}} → tab-loaded
    │     element-exists: ปุ่ม Add Friend
    │     conditions: เจอปุ่ม?
    │       ├─ match: event-click: Add Friend → delay → insert-data
    │       └─ fallback: skip (อาจเป็นเพื่อนแล้ว)
    │     loop-breakpoint
    └─ fallback: skip

PHASE 5: ติดตามเพจ
  conditions: followPages?
    ├─ match:
    │   loop-data: pageLoop (1 ถึง pagesPerDay)
    │     read-file-text: page link → open-url → tab-loaded
    │     element-exists: ปุ่ม Follow/Like เพจ
    │     conditions: เจอปุ่ม?
    │       ├─ match: event-click: Follow/Like → delay → insert-data
    │       └─ fallback: skip
    │     delay: {{variables.delay}}000
    │     loop-breakpoint
    └─ fallback: skip

PHASE 6: ไลค์+คอมเมนต์ฟีด
  conditions: engageFeed?
    ├─ match:
    │   open-url: facebook.com → tab-loaded
    │   loop-data: engageLoop (1 ถึง engagePerDay)
    │     element-scroll: เลื่อนฟีด 300-500px
    │     delay: 2000
    │     random: สุ่ม 1-2 → {{variables.engageType}}
    │     conditions: engageType
    │       ├─ 1 (Like): event-click: Like บนโพสต์ในฟีด
    │       └─ 2 (Comment):
    │           read-file-text: คอมเมนต์
    │           event-click: ช่องคอมเมนต์
    │           press-key: {{variables.comment}}
    │           event-click: ส่ง (Enter)
    │     delay: {{variables.delay}}000
    │     loop-breakpoint
    └─ fallback: skip

PHASE 7: เข้ากลุ่ม (วันที่ 3-4)
  conditions: joinGroups? AND dayCount >= 3
    ├─ match:
    │   loop-data: groupLoop (1 ถึง groupsPerDay)
    │     read-file-text: group link → open-url → tab-loaded
    │     element-exists: ปุ่ม Join Group
    │     conditions: เจอปุ่ม?
    │       ├─ match: event-click: Join Group → delay: 3000
    │       │         conditions: มีคำถามสมาชิก?
    │       │           ├─ match: press-key: ตอบคำถาม → event-click: Submit
    │       │           └─ fallback: skip
    │       └─ fallback: skip (เข้ากลุ่มแล้วหรือปิดรับ)
    │     loop-breakpoint
    └─ fallback: skip

END: บันทึกสรุป
  insert-data: warmDay, actionsToday, friendsAdded, pagesFollowed, engagesCount, groupsJoined
  → end
```

### 🔑 XPath สำหรับ Warm Script

| จุด | XPath |
|-----|-------|
| ปุ่มแก้ไขรูปโปรไฟล์ | `//div[@aria-label="Update profile picture" or @aria-label="อัปเดตรูปโปรไฟล์"]` |
| ปุ่มแก้ไขรูปปก | `//div[@aria-label="Edit Cover Photo" or @aria-label="แก้ไขรูปปก"]` |
| ปุ่ม Add Friend | `//div[@role="button"]//span[contains(text(),"Add Friend") or contains(text(),"เพิ่มเพื่อน")]` |
| ปุ่ม Like Page | `//div[@role="button"]//span[contains(text(),"Like") or contains(text(),"ถูกใจ")]` |
| ปุ่ม Join Group | `//div[@role="button"]//span[contains(text(),"Join Group") or contains(text(),"เข้าร่วมกลุ่ม")]` |
| Checkpoint (verify) | `//span[contains(text(),"Verify") or contains(text(),"ยืนยัน")]` |
| ปุ่ม Not Now (checkpoint) | `//span[contains(text(),"Not now") or contains(text(),"ไม่ใช่ตอนนี้")]` |

### ⏱️ Warming Schedule (4 วัน — จาก Broadcast Plan)

```
Day 1 (จันทร์): Phase 1+2+3 — ตั้งค่าโปรไฟล์ + ท่องฟีด
  actions: 10-15

Day 2 (อังคาร): Phase 3+4+5 — ฟีด + เพิ่มเพื่อน + ติดตามเพจ
  actions: 15-20

Day 3 (พุธ): Phase 3+5+6 — ฟีด + เพจ + เอ็นเกจ
  actions: 15-20

Day 4 (พฤหัส): Phase 3+6+7 — ฟีด + เอ็นเกจ + เข้ากลุ่ม
  actions: 15-20
```

---

## 📐 Script 6: FB Join Group

**ชื่อไฟล์:** `[Demo] FB Join Group 1.0.gemlogin`
**Pattern:** Pattern 1 (Simple Flow)
**Nodes:** ~15

### 🎮 Trigger Parameters

```
👥 ตั้งค่าเข้ากลุ่ม
  ├─ filepath  groupLinksFile  "ไฟล์ลิงก์กลุ่ม (.txt)"
  ├─ number    groupsPerRun    "จำนวนกลุ่มต่อรอบ"          default: 5
  ├─ checkbox  answerQuestions "ตอบคำถามเข้ากลุ่ม"         default: true
  ├─ filepath  answerFile      "ไฟล์คำตอบ (.txt)"         (แสดงเมื่อ answerQuestions=true)
  └─ checkbox  postIntro       "โพสต์แนะนำตัวหลังเข้ากลุ่ม"  default: false

⏱️ ตั้งค่าเวลา
  ├─ number    minDelay        "หน่วงต่ำสุด (วิ)"          default: 5
  └─ number    maxDelay        "หน่วงสูงสุด (วิ)"          default: 10
```

### 🔄 Flow

```
trigger → random: delay → read-file-text: groups
  → loop-data (1 ถึง groupsPerRun)
    → read-file-text: group link
    → open-url: group → tab-loaded → delay
    → element-exists: ปุ่ม Join Group
    → conditions: เจอปุ่ม Join?
      ├─ match:
      │   event-click: Join Group
      │   delay: 3000
      │   conditions: answerQuestions?
      │     ├─ match:
      │     │   element-exists: popup คำถาม
      │     │   conditions: มีคำถาม?
      │     │     ├─ match: read-file-text: คำตอบ
      │     │     │         press-key: พิมพ์คำตอบ
      │     │     │         event-click: Submit
      │     │     └─ fallback: skip
      │     └─ fallback: skip
      │   delay: 2000
      │   conditions: postIntro?
      │     ├─ match:
      │     │   element-exists: ช่องโพสต์ในกลุ่ม
      │     │   press-key: แนะนำตัว
      │     │   event-click: Post
      │     └─ fallback: skip
      │   insert-data: groupUrl, joined, profileName, date
      └─ fallback: insert-data: เข้าไม่ได้ — groupUrl
    → loop-breakpoint
  → end
```

---

## 📐 Script 7: FB Status Check

**ชื่อไฟล์:** `[Demo] FB Status Check 1.0.gemlogin`
**Pattern:** Pattern 1 (Simple Flow — no loop)
**Nodes:** ~12

### 🎮 Trigger Parameters

```
🩺 ตั้งค่าตรวจสอบ
  ├─ checkbox  checkLogin      "ตรวจสอบ Login"           default: true
  ├─ checkbox  checkBan        "ตรวจสอบการแบน"           default: true
  ├─ checkbox  checkFriends    "นับจำนวนเพื่อน"            default: false
  └─ checkbox  checkGroups     "นับจำนวนกลุ่มที่อยู่"        default: false

📊 บันทึกผลลัพธ์
  └─ string    outputPath      "โฟลเดอร์บันทึกผล"          default: C:\Users\Admin\Downloads\status
```

### 🔄 Flow

```
trigger
  → open-url: https://www.facebook.com/
  → tab-loaded
  → delay: 3000
  
  → conditions: checkLogin?
    ├─ match:
    │   element-exists: ตรวจ element ที่แสดงว่า login แล้ว
    │   (เช่น: //div[@aria-label="Home"], //input[@aria-label="Search Facebook"])
    │   conditions: login?
    │     ├─ match: insert-data: status=LOGGED_IN
    │     └─ fallback: insert-data: status=NOT_LOGGED_IN → end (หยุด)
    └─ fallback: skip

  → conditions: checkBan?
    ├─ match:
    │   element-exists: ตรวจข้อความแบน
    │   (เช่น: //span[contains(text(),"Your account has been disabled")],
    │          //span[contains(text(),"You can't use Facebook")],
    │          //span[contains(text(),"account has been suspended")])
    │   conditions: banned?
    │     ├─ match: insert-data: banStatus=BANNED → file-action: บันทึกไฟล์ banned_profiles.txt
    │     └─ fallback: insert-data: banStatus=OK
    └─ fallback: skip

  → conditions: checkFriends?
    ├─ match:
    │   open-url: https://www.facebook.com/friends → tab-loaded
    │   javascript-code: scrape friend count
    │   code: |
    │     const countEl = document.querySelector('[role="main"] a[href*="friends"] span');
    │     // fallback: check profile page
    │     SetVariable("friendCount", countEl ? countEl.textContent : "N/A");
    │   insert-data: friendCount, profileName, date
    └─ fallback: skip

  → conditions: checkGroups?
    ├─ match:
    │   open-url: https://www.facebook.com/groups/?seemore → tab-loaded
    │   javascript-code: scrape group count
    │   insert-data: groupCount, profileName, date
    └─ fallback: skip

  → file-action: บันทึกสรุป status report
    format: "{{profileName}}|{{status}}|{{banStatus}}|{{friendCount}}|{{groupCount}}|{{$date}}"
  → end
```

### 🔑 XPath สำหรับ Status Check

| จุด | XPath |
|-----|-------|
| ตรวจ Login สำเร็จ | `//div[@aria-label="Home" or @role="navigation"]//a[@aria-label="Home"]` |
| ตรวจ Login สำเร็จ (อีกแบบ) | `//input[@aria-label="Search Facebook" or @placeholder="Search Facebook"]` |
| ข้อความแบน | `//span[contains(text(),"disabled") or contains(text(),"suspended") or contains(text(),"ถูกระงับ")]` |
| ข้อความ Checkpoint | `//span[contains(text(),"Verify") or contains(text(),"Upload") or contains(text(),"ยืนยัน")]` |
| จำนวนเพื่อน (profile) | `//a[contains(@href,"friends")]//span` |

---

## 📊 สรุป — 7 สคริปต์ Facebook

| # | สคริปต์ | Nodes | ใช้กับ Broadcast Plan | Priority | เวลาสร้าง |
|---|---------|-------|----------------------|----------|----------|
| 1 | FB Auto Post | ~35 | โพสต์ทุกวัน อ-ศ | 🔴 P0 | 1.5 ชม. |
| 2 | FB Like & Follow | ~30 | ไลค์+ติดตาม จ-ส | 🔴 P0 | 1.5 ชม. |
| 3 | FB Comment | ~25 | คอมเมนต์ อ-พฤ | 🟡 P1 | 1 ชม. |
| 4 | FB Share | ~25 | แชร์ จ-ศ | 🟡 P1 | 1 ชม. |
| 5 | FB Profile Warm | ~70 | อุ่นเครื่อง จ-พฤ | 🔴 P0 | 3 ชม. |
| 6 | FB Join Group | ~15 | เข้ากลุ่ม พฤ | 🟢 P2 | 30 นาที |
| 7 | FB Status Check | ~12 | เช็คสถานะ อา | 🟡 P1 | 30 นาที |

---

## ✅ Checklist ก่อนสร้างทุกสคริปต์

### Schema
- [ ] label อยู่ที่ top-level (n['label']) — ไม่ใช่ data.label
- [ ] ทุก BlockBasicWithFallback มี field ครบตาม label (ตาม field matrix)
- [ ] trigger มี type: "manual" + parameters ครบ
- [ ] conditions ใช้ nested schema 3-level
- [ ] edges sourceHandle: conditions → output-{group_id}/output-fallback
- [ ] delay time: number หรือ "N,M" string
- [ ] javascript-code: top-level statements, ไม่มี IIFE, ไม่มี return;
- [ ] loopId ตรงกันระหว่าง loop-data และ loop-breakpoint

### Functional
- [ ] ทดสอบ 1 profile (Jacob_1) ก่อน scale
- [ ] ตรวจ XPath selector บน Facebook จริง
- [ ] ทดสอบทุก branch (match + fallback)
- [ ] ตรวจ error handling — element ไม่เจอต้องไม่พัง
- [ ] backup db.db ก่อน import

### FB-Specific
- [ ] เช็ค login state ก่อนทำ action
- [ ] ดัก checkpoint/verify popup
- [ ] delay ไม่ต่ำกว่า 2-3 วิ (กัน FB detect bot)
- [ ] ใช้ humanClick: false (default) แต่ random delay
- [ ] ไม่ spam — dailyActions ไม่เกิน 50 ต่อวันต่อ profile

---

*🤖 ออกแบบโดย JIMMY 🌊 — Kvasir AI Companion*
*อ้างอิงจาก: GEMMY block-reference, 801 corpus, workflow-patterns, real-examples*
*ยังไม่ commit — รอ Jacob อนุมัติ*
