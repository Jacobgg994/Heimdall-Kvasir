# Facebook — Cross-Account XPath Reference

ใช้ได้กับทุกบัญชี — ไม่มีชื่อเฉพาะ ใช้ `starts-with()` / `contains()` เท่านั้น
เรียนรู้จาก drum 2 ครั้งบน News Feed (110 XPaths) — 2026-07-17

---

## Navigation (ใช้ได้ทุกบัญชี ไม่เปลี่ยน)

| Element | XPath |
|---|---|
| Logo/Facebook | `//a[@aria-label="Facebook"]` |
| Home | `//a[@aria-label="Home"]` |
| Reels | `//a[@aria-label="Reels"]` |
| Friends | `//a[@aria-label="Friends"]` |
| Marketplace | `//a[@aria-label="Marketplace"]` |
| Gaming | `//a[@aria-label="Gaming"]` |
| Groups | `//a[normalize-space(.)="Groups"]` |
| Your profile | `//div[@aria-label="Your profile"]` |
| Facebook menu | `//div[@aria-label="Facebook menu"]` |
| Shortcuts | `//div[@aria-label="Shortcuts"]` |
| Search | `//input[@aria-label="Search Facebook"]` |
| Messenger | `//div[@aria-label="New message"]` |
| Account settings | `//div[@aria-label="Account Controls and Settings"]` |
| Back | `//div[@aria-label="Back to previous page"]` |
| More links | `//div[@aria-label="More footer links"]` |

---

## Post Composer (ใช้ได้ทุกบัญชี)

| Element | XPath |
|---|---|
| Create post box | `//div[@aria-label="Create a post"]` |
| Photo/video | `//div[@aria-label="Photo/video"]` |
| Live video | `//div[@aria-label="Live video"]` |
| Feeling/activity | `//div[@aria-label="Feeling/activity"]` |

---

## Post Interactions (ใช้ starts-with — ไม่ต้องรู้ชื่อเพจ)

| Element | XPath |
|---|---|
| **Actions menu** (ทุกโพสต์) | `//div[starts-with(@aria-label, "Actions for this post")]` |
| **Hide post** | `//a[starts-with(@aria-label, "Hide post by")]` |
| **Like count** | `//div[starts-with(@aria-label, "Like:")]` |
| **Love count** | `//div[starts-with(@aria-label, "Love:")]` |
| **Haha count** | `//div[starts-with(@aria-label, "Haha:")]` |
| **Comment** | ต้อง click เข้าโพสต์ก่อน → `//div[@role="textbox" and starts-with(@aria-label, "Write a comment")]` |

---

## Stories (ใช้ contains)

| Element | XPath |
|---|---|
| **View story** (ทุกคน) | `//a[contains(@aria-label, ", view story")]` |
| **Create story** | `//a[contains(@aria-label, "Create story")]` |

---

## Reels

| Element | XPath |
|---|---|
| **Reel link** (ทุกคลิป) | `//a[starts-with(@aria-label, "Reel by")]` |

---

## Sponsored Content

| Element | XPath |
|---|---|
| **Sponsored menu** | `//div[contains(@aria-label, "sponsored")]` |
| **Sponsored content (full)** | `//div[starts-with(@aria-label, "Open menu for") and contains(@aria-label, "sponsored")]` |

---

## Reactions (ใช้ใน dialog)

| Element | XPath |
|---|---|
| **Open reaction menu** | `//div[@role="button" and (@aria-label="React" or starts-with(@aria-label, "Change "))]` |
| **Like** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Like"]` |
| **Love** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Love"]` |
| **Care** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Care"]` |
| **Haha** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Haha"]` |
| **Wow** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Wow"]` |
| **Sad** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Sad"]` |
| **Angry** | `//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Angry"]` |

---

## Footer

| Element | XPath |
|---|---|
| Footer | `//footer[@aria-label="Facebook"]` |
| Ad Choices | `//a[normalize-space(.)="Ad Choices"]` |
| Advertising | `//a[normalize-space(.)="Advertising"]` |
| Cookies | `//a[normalize-space(.)="Cookies"]` |
| Privacy | `//a[normalize-space(.)="Privacy"]` |
| Terms | `//a[normalize-space(.)="Terms"]` |

---

## Carousel / Slider

| Element | XPath |
|---|---|
| Next items | `//div[@aria-label="Next items"]` |
| Previous items | `//div[@aria-label="Previous items"]` |
| More | `//div[@aria-label="More"]` |
| See more | `//div[@aria-label="See more explore items"]` |

---

## หลักการเลือก XPath สำหรับ Multi-Account

### ❌ ห้ามใช้ (เปลี่ยนตามบัญชี/เพจ)
```xpath
//a[@aria-label="Big C"]                          ← ชื่อเพจเปลี่ยน
//a[normalize-space(.)="อามานี พูลชนะ"]            ← ชื่อคนเปลี่ยน
//div[@aria-label="Actions for this post by Big C"] ← ชื่อเพจอยู่ใน string
```

### ✅ ใช้แทน
```xpath
//div[starts-with(@aria-label, "Actions for this post")]   ← ครอบคลุมทุกโพสต์
//a[starts-with(@aria-label, "Hide post by")]               ← ครอบคลุมทุกเพจ
//a[contains(@aria-label, ", view story")]                   ← ครอบคลุมทุกสตอรี่
//a[starts-with(@aria-label, "Reel by")]                    ← ครอบคลุมทุก Reel
//div[contains(@aria-label, "sponsored")]                   ← ครอบคลุมทุกสปอนเซอร์
```

###  правило
1. **Static elements** → ใช้ `@aria-label="..."` ตรงๆ ได้เลย (Home, Friends, Search...)
2. **Dynamic elements** (มีชื่อคน/เพจ) → ใช้ `starts-with()` หรือ `contains()`
3. **Reactions** → scope ใน `//div[@role="dialog" and @aria-label="Reactions"]` เสมอ
4. **Comments** → ต้องเปิดโพสต์ก่อน แล้ว scope ใน dialog

---

## สรุป: XPath ที่ใช้จริงสำหรับ Multi-Account Automation

```xpath
# Navigation
//a[@aria-label="Home"]
//input[@aria-label="Search Facebook"]
//div[@aria-label="Your profile"]

# Feed Actions
//div[starts-with(@aria-label, "Actions for this post")]
//a[starts-with(@aria-label, "Hide post by")]
//div[contains(@aria-label, "sponsored")]

# Post Composer
//div[@aria-label="Create a post"]
//div[@aria-label="Photo/video"]

# Stories
//a[contains(@aria-label, ", view story")]

# Reels
//a[starts-with(@aria-label, "Reel by")]

# Reactions
//div[@role="button" and @aria-label="React"]
//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Like"]

# Engagement
//div[starts-with(@aria-label, "Like:")]
//div[starts-with(@aria-label, "Love:")]
```
