# 💎 แผนออกแบบสคริปต์ GemLogin — Demo Scripts

> ออกแบบโดย JIMMY 🌊 | 4 ก.ค. 2026
> สร้างโดย: GEMMY 💎 | ตรวจสอบ: JIMMY 🌊
> อ้างอิงจาก: 801 corpus, block-reference, real-examples, workflow-patterns
> ยังไม่ commit — รอ Jacob อนุมัติ

---

## 🎯 ภาพรวม — 4 สคริปต์

| # | ชื่อสคริปต์ | Platform | ใช้สำหรับ | ความซับซ้อน | Nodes |
|---|-----------|----------|----------|------------|-------|
| 1 | Facebook Auto Post | Facebook | Demo + Broadcast | ⭐⭐ กลาง | ~30 |
| 2 | Facebook Like & Follow | Facebook | Warm-up + Broadcast | ⭐⭐ กลาง | ~40 |
| 3 | TikTok Like & Comment | TikTok | Demo + Engagement | ⭐⭐⭐ สูง | ~45 |
| 4 | Shopee Price Monitor | Shopee | Demo E-commerce | ⭐ ง่าย | ~20 |

---

## 📐 Script 1: Facebook Auto Post

**ชื่อไฟล์:** `[Demo] Facebook Auto Post 1.0.gemlogin`
**วัตถุประสงค์:** โพสต์ข้อความ + รูปภาพบน Facebook Wall โดยอัตโนมัติ
**ใช้สำหรับ:** สาธิตการขาย + Broadcast plan
**Pattern:** Pattern 2 (Loop with Data Processing)
**ประมาณ Nodes:** 30 nodes, 35 edges

### 🎮 Trigger Parameters

```
Section: "📝 ตั้งค่าการโพสต์"
  └─ filepath: captionFolderPath — "โฟลเดอร์แคปชั่น" (default: C:\Users\Admin\Downloads\captions)
  └─ filepath: mediaFolderPath — "โฟลเดอร์รูปภาพ" (default: C:\Users\Admin\Downloads\media)
  └─ checkbox: postWithImage — "โพสต์พร้อมรูปภาพ" (default: true)
  └─ checkbox: postWithText — "โพสต์ข้อความ" (default: true)
  └─ number: postCount — "จำนวนโพสต์ที่ต้องการ" (default: 5)
  └─ checkbox: deleteUsedFiles — "ลบไฟล์ที่ใช้แล้ว" (default: false)

Section: "⏱️ การตั้งค่าเวลา"
  └─ number: minDelay — "หน่วงเวลาต่ำสุด (วิ)" (default: 3)
  └─ number: maxDelay — "หน่วงเวลาสูงสุด (วิ)" (default: 8)

Section: "📊 บันทึกผลลัพธ์"
  └─ string: outputFolderPath — "โฟลเดอร์บันทึกผล" (default: C:\Users\Admin\Downloads\output)
```

### 🔄 Flow Diagram

```
[trigger]
  ↓
[random: delay 3-8 sec] → ตั้งค่า {{variables.delay}}
  ↓
[read-file-text: captions.txt] → {{variables.caption}} (aline mode, random)
  ↓
[get-file-path: media folder] → {{variables.mediaFile}} (สุ่มรูปจากโฟลเดอร์)
  ↓
[loop-data: mainloop, numbers, 1 to {{variables.postCount}}]
  ↓
[open-url: https://www.facebook.com/]
  ↓
[tab-loaded]
  ↓
[element-exists: ตรวจว่า login แล้วหรือยัง]
  ↓
[conditions: Login Check]
  ├─ match (ยังไม่ login): → [event-click: login button] → [press-key: email] → [press-key: password] → [event-click: login submit] → [tab-loaded]
  └─ fallback (login แล้ว): → ไปขั้นตอนต่อไป
  ↓
[event-click: "What's on your mind" — //div[@role="button" and contains(., "What's on your mind")]
  ↓
[delay: {{variables.delay}}000]
  ↓
[conditions: postWithImage]
  ├─ match: → [event-click: "Photo/video" button] → [upload-file: {{variables.mediaFile}}] → [delay: 3000]
  └─ fallback: → skip
  ↓
[forms: เขียนแคปชั่น]
  selector: //div[@role="textbox" and starts-with(@aria-placeholder, "What's on your mind")]
  value: {{variables.caption}}
  type: text-field
  clearValue: true
  typingDelay: 50
  ↓
[delay: 2000]
  ↓
[event-click: "Post" button — //div[@role="button" and contains(., "Post")]
  ↓
[delay: 5000] → รอโพสต์สำเร็จ
  ↓
[element-exists: ตรวจ "Your post has been shared"]
  ↓
[conditions: Post Success]
  ├─ match: → [clipboard: get current URL] → {{variables.LinkPost}}
  │          → [file-action: บันทึกลงไฟล์ output.txt — "{{variables.LinkPost}}|{{variables.caption}}|{{profileName}}|{{$date}}"]
  │          → [insert-data: บันทึกลง data table — postLink, caption, profileName, date]
  │          → [increase-variable: successCount]
  └─ fallback: → [insert-data: บันทึกว่าโพสต์ไม่สำเร็จ]
  ↓
[loop-breakpoint: mainloop]
  ↓
[end]
```

### 🔑 XPath Selectors สำคัญ

| Element | XPath |
|---------|-------|
| ปุ่ม "What's on your mind" | `//div[@role="button" and contains(normalize-space(), "What's on your mind")]` |
| ช่องเขียนโพสต์ | `//div[@role="textbox" and starts-with(@aria-placeholder, "What's on your mind")]` |
| ปุ่ม Post | `//div[@role="button"]//span[text()="Post"]/ancestor::div[@role="button"]` |
| ปุ่ม Photo/Video | `//div[@aria-label="Photo/video"]` |
| โพสต์สำเร็จ | `//span[contains(text(), "shared") or contains(text(), "posted")]` |
| ปุ่ม Login | `//button[@name="login"]` |
| ช่อง Email | `//input[@id="email" or @name="email"]` |

### 📊 Data Recording

```
ไฟล์ output.txt: {{LinkPost}}|{{caption}}|{{profileName}}|{{$date}}
data table insert: postLink, caption, profileName, date, status
```

---

## 📐 Script 2: Facebook Like & Follow

**ชื่อไฟล์:** `[Demo] Facebook Like & Follow 1.0.gemlogin`
**วัตถุประสงค์:** ไลค์โพสต์ + ติดตามเพจเป้าหมาย
**ใช้สำหรับ:** Warm-up profiles + Broadcast plan
**Pattern:** Pattern 2 (Loop with Data Processing)
**ประมาณ Nodes:** 40 nodes, 48 edges

### 🎮 Trigger Parameters

```
Section: "🎯 ตั้งค่าเป้าหมาย"
  └─ filepath: targetLinksPath — "ไฟล์ลิงก์เป้าหมาย (.txt)" (default: C:\Users\Admin\Downloads\targets.txt)
  └─ checkbox: enableLike — "เปิดใช้งาน Like" (default: true)
  └─ checkbox: enableFollow — "เปิดใช้งาน Follow" (default: true)
  └─ number: actionsPerProfile — "จำนวน action ต่อโปรไฟล์" (default: 10)
  └─ checkbox: randomScrollFirst — "สุ่มเลื่อนฟีดก่อนเริ่ม" (default: true)

Section: "⏱️ การตั้งค่าเวลา"
  └─ number: minDelay — "หน่วงเวลาต่ำสุด (วิ)" (default: 2)
  └─ number: maxDelay — "หน่วงเวลาสูงสุด (วิ)" (default: 6)
  └─ number: scrollCount — "จำนวนครั้งที่เลื่อนฟีด" (default: 3)

Section: "📊 บันทึกผลลัพธ์"
  └─ string: outputFolderPath — "โฟลเดอร์บันทึกผล" (default: C:\Users\Admin\Downloads\output)
```

### 🔄 Flow Diagram

```
[trigger]
  ↓
[random: delay 2-6 sec] → {{variables.delay}}
  ↓
[read-file-text: targets.txt] → {{variables.targetUrl}} (aline mode, random)
  ↓
[loop-data: mainloop, numbers, 1 to {{variables.actionsPerProfile}}]
  ↓
[read-file-text: targets.txt] → {{variables.currentTarget}} (aline mode, random, deleteLine)
  ↓
[open-url: {{variables.currentTarget}}]
  ↓
[tab-loaded]
  ↓
[element-exists: ตรวจว่าเป็นเพจหรือโพสต์]
  ↓
[conditions: Page or Post]
  ├─ match (เป็นเพจ — มีปุ่ม Follow): 
  │   ↓
  │   [conditions: enableFollow]
  │   ├─ match:
  │   │   [element-exists: ปุ่ม Follow — //div[@role="button"]//span[contains(text(), "Follow") or contains(text(), "ติดตาม")]]
  │   │   [conditions: Follow Button Found]
  │   │   ├─ match: → [event-click: ปุ่ม Follow] → [delay: {{variables.delay}}000]
  │   │   └─ fallback: → [insert-data: ไม่พบปุ่ม follow]
  │   └─ fallback: skip
  │
  └─ fallback (เป็นโพสต์):
      ↓
      [conditions: enableLike]
      ├─ match:
      │   [element-exists: ปุ่ม Like — //div[@aria-label="Like" or @aria-label="ถูกใจ"]]
      │   [conditions: Like Button Found]
      │   ├─ match: 
      │   │   [random: randomLike 1-4] → {{variables.RandomLike}}
      │   │   [conditions: RandomLike]
      │   │   ├─ match (RandomLike == 1): → [event-click: ปุ่ม Like] (normal like)
      │   │   ├─ match (RandomLike == 2): → [hover-element: ปุ่ม Like] → [delay: 1000] → [event-click: //div[@aria-label="Love" or @aria-label="หลงรัก"]]
      │   │   ├─ match (RandomLike == 3): → [hover-element: ปุ่ม Like] → [delay: 1000] → [event-click: //div[@aria-label="Care"]]
      │   │   └─ match (RandomLike == 4): → [event-click: ปุ่ม Like] (normal like)
      │   └─ fallback: → [insert-data: ไม่พบปุ่ม like] → [element-scroll: scroll 500px]
      └─ fallback: skip
  ↓
[element-scroll: เลื่อนฟีด 300-800px]
  ↓
[delay: {{variables.delay}}000]
  ↓
[insert-data: บันทึกผล — targetUrl, action (like/follow), status, profileName, date]
  ↓
[loop-breakpoint: mainloop]
  ↓
[end]
```

### 🔑 XPath Selectors สำคัญ

| Element | XPath |
|---------|-------|
| ปุ่ม Like (ยังไม่กด) | `//div[@aria-label="Like" and not(contains(@aria-label, "Unlike"))]` |
| ปุ่ม Unlike (กดแล้ว) | `//div[contains(@aria-label, "Unlike")]` |
| เมนู Reaction (hover) | `//div[@aria-label="Love" or @aria-label="Care" or @aria-label="Haha"]` |
| ปุ่ม Follow เพจ | `//div[@role="button"]//span[contains(text(), "Follow") or contains(text(), "ติดตาม")]/ancestor::div[@role="button"]` |
| ปุ่ม Following (follow แล้ว) | `//div[@role="button"]//span[contains(text(), "Following") or contains(text(), "ติดตามอยู่")]` |
| Feed container | `//div[@role="feed"]` |

---

## 📐 Script 3: TikTok Like & Comment

**ชื่อไฟล์:** `[Demo] TikTok Like & Comment 1.0.gemlogin`
**วัตถุประสงค์:** ไลค์ + คอมเมนต์บนวิดีโอ TikTok FYP
**ใช้สำหรับ:** Demo ขาย + TikTok engagement
**Pattern:** Pattern 2 (Loop with Data Processing) + Pattern 4 (Conditions Branch)
**ประมาณ Nodes:** 45 nodes, 55 edges
**⚠️ ความซับซ้อน:** TikTok มี dynamic UI — ปุ่ม share/comment มักซ่อนอยู่ ต้องหาให้เจอ

### 🎮 Trigger Parameters

```
Section: "🎯 ตั้งค่า TikTok"
  └─ checkbox: enableLike — "เปิด Like" (default: true)
  └─ checkbox: enableComment — "เปิด Comment" (default: true)
  └─ filepath: commentFilePath — "ไฟล์คอมเมนต์ (.txt)" (default: C:\Users\Admin\Downloads\comments.txt)
  └─ number: actionCount — "จำนวนวิดีโอที่ทำ action" (default: 15)
  └─ checkbox: deleteUsedComments — "ลบคอมเมนต์ที่ใช้แล้ว" (default: false)

Section: "⏱️ การตั้งค่าเวลา"
  └─ number: minDelay — "หน่วงเวลาต่ำสุด (วิ)" (default: 2)
  └─ number: maxDelay — "หน่วงเวลาสูงสุด (วิ)" (default: 5)
  └─ number: watchTimePerVideo — "เวลาดูวิดีโอ (วิ)" (default: 8)

Section: "📊 การตั้งค่าอื่นๆ"
  └─ number: scrollPerRound — "เลื่อนกี่ครั้งต่อรอบ" (default: 3)
```

### 🔄 Flow Diagram

```
[trigger]
  ↓
[random: delay 2-5 sec] → {{variables.delay}}
  ↓
[read-file-text: comments.txt] → {{variables.comment}} (aline mode, random)
  ↓
[open-url: https://www.tiktok.com/foryou]
  ↓
[tab-loaded]
  ↓
[wait: 5000] → รอ TikTok โหลด FYP
  ↓
[element-exists: ตรวจว่าอยู่หน้า FYP — //div[@data-e2e="recommend-list"]]
  ↓
[conditions: On FYP]
  ├─ match: → continue
  └─ fallback: → [open-url: https://www.tiktok.com/foryou] → [tab-loaded] → [wait: 5000]
  ↓
[loop-data: mainloop, numbers, 1 to {{variables.actionCount}}]
  ↓
[element-scroll: เลื่อนฟีดลง 800px] → เลื่อนไปวิดีโอถัดไป
  ↓
[delay: 3000] → รอวิดีโอโหลด
  ↓
[conditions: enableLike]
  ├─ match:
  │   ↓
  │   [element-exists: ปุ่ม Like (หัวใจข้างขวา)]
  │   selector: //span[@data-e2e="like-icon"]/ancestor::button
  │   ↓
  │   [conditions: Like Button Found]
  │   ├─ match: → [event-click: ปุ่ม Like] → [delay: {{variables.delay}}000]
  │   └─ fallback: → [insert-data: ไม่พบปุ่ม like]
  └─ fallback: skip
  ↓
[conditions: enableComment]
  ├─ match:
  │   ↓
  │   [element-exists: ปุ่ม Comment]
  │   selector: //span[@data-e2e="comment-icon"]/ancestor::button
  │   ↓
  │   [conditions: Comment Button Found]
  │   ├─ match: 
  │   │   [event-click: ปุ่ม Comment]
  │   │   ↓
  │   │   [delay: 2000] → รอ comment panel เปิด
  │   │   ↓
  │   │   [element-exists: ช่องใส่คอมเมนต์]
  │   │   selector: //div[@data-e2e="comment-input"]//div[@contenteditable="true"]
  │   │   ↓
  │   │   [conditions: Comment Input Found]
  │   │   ├─ match:
  │   │   │   [read-file-text: comments.txt] → {{variables.comment}} (aline mode, random, deleteLine: {{variables.deleteUsedComments}})
  │   │   │   ↓
  │   │   │   [press-key: พิมพ์คอมเมนต์]
  │   │   │   selector: //div[@data-e2e="comment-input"]//div[@contenteditable="true"]
  │   │   │   keysToPress: {{variables.comment}}
  │   │   │   ↓
  │   │   │   [delay: 1500]
  │   │   │   ↓
  │   │   │   [event-click: ปุ่มส่งคอมเมนต์]
  │   │   │   selector: //div[@data-e2e="comment-input"]//button[contains(@class, "submit")]
  │   │   │   ↓
  │   │   │   [delay: {{variables.delay}}000]
  │   │   └─ fallback: → [insert-data: ไม่พบช่องคอมเมนต์]
  └─ fallback: skip
  ↓
[delay: {{variables.watchTimePerVideo}}000] → จำลองการดูวิดีโอ
  ↓
[insert-data: บันทึกผล — action (like/comment/both), commentText, status, profileName, date]
  ↓
[loop-breakpoint: mainloop]
  ↓
[end]
```

### 🔑 XPath/CSS Selectors สำหรับ TikTok (Dynamic UI)

| Element | Selector | หมายเหตุ |
|---------|----------|---------|
| FYP Container | `//div[@data-e2e="recommend-list"]` | ตรวจว่าอยู่หน้า FYP |
| ปุ่ม Like (หัวใจ) | `//span[@data-e2e="like-icon"]/ancestor::button` | หรือ `//button[@data-e2e="like-icon"]` |
| ปุ่ม Comment | `//span[@data-e2e="comment-icon"]/ancestor::button` | อีกแบบ: `//button[@data-e2e="comment-icon"]` |
| ช่องใส่คอมเมนต์ | `//div[@data-e2e="comment-input"]//div[@contenteditable="true"]` | ใช้ `contenteditable` |
| ปุ่มส่งคอมเมนต์ | `//div[@data-e2e="comment-input"]//button` | หรือ `//button[contains(@class, "submit")]` |
| ปุ่ม Share | `//span[@data-e2e="share-icon"]/ancestor::button` | สำหรับ repost |
| ปุ่ม Close comment | `//*[@data-e2e="comment-close"]` | ปิด comment panel |
| แถบ progress วิดีโอ | `//div[@data-e2e="video-progress"]` | ตรวจว่าวิดีโอกำลังเล่น |

### ⚠️ TikTok-Specific Issues

1. **Shadow DOM:** ปุ่ม Like/Comment อาจอยู่ใน shadow DOM → ใช้ `findBy: "cssSelector"` แทน xpath ในบางกรณี
2. **Dynamic attributes:** TikTok มักเปลี่ยน CSS class → ใช้ `data-e2e` attributes
3. **Comment panel overlay:** ต้องปิด comment panel ก่อนเลื่อนวิดีโอถัดไป
4. **Login popup:** TikTok มักเด้ง popup ให้ login → ต้องมี condition ดัก
5. **Rate limit:** Like/Comment มากเกิน → temporary block → ต้องตั้ง delay ให้เหมาะสม

---

## 📐 Script 4: Shopee Price Monitor

**ชื่อไฟล์:** `[Demo] Shopee Price Monitor 1.0.gemlogin`
**วัตถุประสงค์:** ตรวจสอบราคาสินค้า Shopee และบันทึกการเปลี่ยนแปลง
**ใช้สำหรับ:** Demo ขายกลุ่ม E-commerce
**Pattern:** Pattern 2 (Loop with Data Processing)
**ประมาณ Nodes:** 20 nodes, 22 edges

### 🎮 Trigger Parameters

```
Section: "🔍 ตั้งค่าการติดตาม"
  └─ filepath: productLinksPath — "ไฟล์ลิงก์สินค้า (.txt)" (default: C:\Users\Admin\Downloads\products.txt)
  └─ number: checkInterval — "รอบการตรวจสอบ (นาที)" (default: 60)
  └─ checkbox: alertOnPriceDrop — "แจ้งเตือนเมื่อราคาลด" (default: true)
  └─ checkbox: saveScreenshot — "บันทึกภาพหน้าจอ" (default: false)

Section: "⏱️ การตั้งค่าเวลา"
  └─ number: minDelay — "หน่วงเวลาต่ำสุด (วิ)" (default: 3)
  └─ number: maxDelay — "หน่วงเวลาสูงสุด (วิ)" (default: 7)
```

### 🔄 Flow Diagram

```
[trigger]
  ↓
[random: delay 3-7 sec] → {{variables.delay}}
  ↓
[read-file-text: products.txt] → {{variables.productUrl}} (aline mode)
  ↓
[loop-data: mainloop, data, toNumber: 1000] → วนไม่จำกัด
  ↓
[read-file-text: products.txt] → {{variables.currentProduct}} (aline mode, random)
  ↓
[open-url: {{variables.currentProduct}}]
  ↓
[tab-loaded]
  ↓
[delay: {{variables.delay}}000] → รอหน้าโหลดเต็ม
  ↓
[element-exists: ตรวจว่าเป็นหน้าสินค้า — //div[contains(@class, "product-detail")]
  ↓
[conditions: Product Page]
  ├─ match:
  │   ↓
  │   [element-exists: ชื่อสินค้า]
  │   selector: //div[contains(@class, "product-title")]//span  หรือ  //h1[contains(@class, "title")]
  │   ↓
  │   [clipboard: get page title] → {{variables.productName}}
  │   ↓
  │   [element-exists: ราคาสินค้า]
  │   selector: //div[contains(@class, "product-price")]//span  หรือ  //div[text()="฿"]/following-sibling::*
  │   ↓
  │   [javascript-code: ดึงราคาจาก DOM]
  │   code: |
  │     const priceEl = document.querySelector('[class*="product-price"] span') || 
  │                     document.querySelector('[class*="price"]');
  │     const price = priceEl ? priceEl.textContent.trim().replace(/[^0-9.]/g, '') : '0';
  │     SetVariable("currentPrice", price);
  │   ↓
  │   [insert-data: บันทึกราคา — productName, currentPrice, productUrl, date]
  │   ↓
  │   [conditions: alertOnPriceDrop]
  │   ├─ match:
  │   │   [javascript-code: เทียบราคา]
  │   │   code: |
  │   │     const currentPrice = Number(RefData("variables", "currentPrice"));
  │   │     const lastPrice = Number(RefData("variables", "lastPrice")) || Infinity;
  │   │     if (currentPrice < lastPrice) {
  │   │       SetVariable("priceDropped", "true");
  │   │       SetVariable("priceDiff", String(lastPrice - currentPrice));
  │   │     } else {
  │   │       SetVariable("priceDropped", "false");
  │   │     }
  │   │     SetVariable("lastPrice", String(currentPrice));
  │   │   ↓
  │   │   [conditions: Price Dropped]
  │   │   ├─ match: → [file-action: บันทึก alert — "🔥 ราคาลด! {{variables.productName}} จาก ฿{{variables.lastPrice}} → ฿{{variables.currentPrice}} (ลด {{variables.priceDiff}} บาท)"]
  │   │   └─ fallback: → continue
  │   └─ fallback: skip
  │   ↓
  │   [delay: {{variables.delay}}000]
  └─ fallback: → [insert-data: ไม่พบหน้าสินค้า — {{variables.currentProduct}}]
  ↓
[delay: {{variables.checkInterval}}000] → รอรอบถัดไป (นาที)
  ↓
[loop-breakpoint: mainloop]
  ↓
[end]
```

### 🔑 XPath/CSS Selectors สำหรับ Shopee

| Element | Selector |
|---------|----------|
| หน้าสินค้า | `//div[contains(@class, "product-detail")]` |
| ชื่อสินค้า | `//div[contains(@class, "attM6y")]//span` หรือ `//h1` |
| ราคาสินค้า | `//div[contains(@class, "YabPLa")]` หรือ `//div[text()="฿"]` |
| ราคาเดิม (ขีดฆ่า) | `//div[contains(@class, "original-price")]` หรือ `//del` |
| สถานะสินค้า (มี/หมด) | `//button[contains(text(), "ซื้อ") or contains(text(), "Buy")]` |
| จำนวนที่ขาย | `//div[contains(text(), "ขายแล้ว") or contains(text(), "sold")]` |

### ⚠️ Shopee-Specific Issues

1. **Anti-bot:** Shopee มี Cloudflare + anti-bot → อาจต้องใช้ fingerprint/rotation
2. **Dynamic pricing:** ราคาอาจเปลี่ยนตาม cookie/proxy region
3. **Rate limit:** ตรวจสอบบ่อยเกิน → ต้องตั้ง `checkInterval` ขั้นต่ำ 5-10 นาที
4. **Flash sale:** ราคา flash sale กับราคาปกติใช้ element คนละตัวกัน

---

## 🏗️ โครงสร้าง .gemlogin JSON Template

ทุกสคริปต์ใช้โครงสร้างเดียวกัน:

```json
{
  "name": "[Demo] Facebook Auto Post 1.0",
  "icon": "riFacebookFill",
  "settings": {
    "publicId": "",
    "blockDelay": 0,
    "saveLog": true,
    "debugMode": false,
    "restartTimes": 3,
    "notification": true,
    "execContext": "popup",
    "reuseLastState": false,
    "inputAutocomplete": true,
    "onError": "stop-workflow",
    "executedBlockOnWeb": false
  },
  "nodes": [ ... ],
  "edges": [ ... ],
  "createdAt": "2026-07-04T00:00:00.000Z",
  "updatedAt": "2026-07-04T00:00:00.000Z"
}
```

---

## ✅ Checklist — ก่อนสร้างทุกสคริปต์

### Schema Validation
- [ ] ทุก node มี `label` ที่ top-level (ไม่ใช่ inside data)
- [ ] trigger มี `type: "manual"` + parameters ครบทุกตัว
- [ ] ทุก `BlockBasicWithFallback` มี fields ครบตาม label (ตาม field matrix)
- [ ] conditions ใช้ nested schema 3-level (group → subgroup → items triplet)
- [ ] conditions edge sourceHandle ใช้ `{node-id}-output-{group_id}` และ `-output-fallback`
- [ ] delay `time` field ใช้ number หรือ `"N,M"` string (ไม่ใช่ `"random(N,M)"`)
- [ ] javascript-code ไม่มี IIFE wrapper `(() => {})()`
- [ ] javascript-code ไม่มี early `return;`
- [ ] loop-breakpoint edge ไป node ถัดไป (ไม่กลับ loop-data)
- [ ] มีทั้ง trigger node และ end node

### Functional Testing
- [ ] ทดสอบด้วย 1 profile ก่อน scale
- [ ] ตรวจ XPath/CSS selector บนหน้าจริง
- [ ] ทดสอบทุก branch (match + fallback)
- [ ] ตรวจ data recording (file-action, insert-data)
- [ ] ตรวจ loop ทำงานครบตามจำนวน
- [ ] ทดสอบกับ proxy (ถ้าใช้)
- [ ] ตรวจ error handling — ถ้า element ไม่เจอต้องไม่พัง

### Production Checklist
- [ ] backup db.db ก่อน import
- [ ] ทดสอบบน device จริง
- [ ] ตั้งค่า restartTimes = 3
- [ ] saveLog = true
- [ ] onError = "stop-workflow"
- [ ] ใส่ description ภาษาไทยในทุก node

---

## 📊 Priority & Timeline

| Priority | สคริปต์ | ทำไมต้องก่อน | ผู้รับผิดชอบ | เวลา |
|----------|---------|-------------|-------------|------|
| 🔴 P0 | Facebook Auto Post | ใช้ demo + broadcast สัปดาห์นี้ | GEMMY | 1-2 ชม. |
| 🔴 P0 | Facebook Like & Follow | ใช้ warm-up วันจันทร์นี้ | GEMMY | 1-2 ชม. |
| 🟡 P1 | TikTok Like & Comment | ใช้ demo + engagement | GEMMY | 2-3 ชม. |
| 🟢 P2 | Shopee Price Monitor | Demo ขายกลุ่ม E-commerce | GEMMY | 1 ชม. |

---

*🤖 ออกแบบโดย JIMMY 🌊 — Kvasir AI Companion*
*อ้างอิงจาก: GEMMY block-reference, 801 corpus, workflow-patterns, real-examples, GemLogin v5.0.3 internals*
*ยังไม่ commit — รอ Jacob อนุมัติ*
