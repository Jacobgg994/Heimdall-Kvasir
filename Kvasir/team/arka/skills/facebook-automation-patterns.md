---
name: facebook-automation-patterns
description: Facebook profile/cover photo change, post, share, comment automation patterns พร้อม XPath selectors ที่ verified
metadata:
  type: skill
  category: gemlogin
  owner: arka
---

# 📘 Facebook Automation Patterns

> Automation patterns สำหรับ Facebook บน GemLogin — XPath selectors แบบ cross-account (ใช้ `starts-with()` / `contains()` ไม่มีชื่อบัญชีตายตัว)
> อัปเดตล่าสุด: 2026-06-29

---

## Pattern 1: Profile & Cover Photo Change

### Profile Photo Change

```
trigger → open-url (profile) → tab-loaded → event-click (avatar) → delay
  → upload-file (select image) → delay → event-click (save) → delay → end
```

**XPath Selectors:**
| Step | Main Selector | Fallback Selector |
|------|--------------|-------------------|
| เปิด profile | `//a[@aria-label="Facebook"]` | `//a[contains(@href,"/photo/?fbid=")]` |
| คลิก avatar | `//div[@aria-label="Your profile"]` | `//a[contains(@aria-label,"profile")]` |
| Update photo | `//span[text()="Update profile picture"]` | `//div[@aria-label="Update profile picture"]` |
| Upload photo | `//span[text()="Upload photo"]` | `//div[@aria-label="Upload photo"]` |
| Save | `//div[@aria-label="Save"]` | `//span[text()="Save"]` |
| Cancel | `//div[@aria-label="Cancel"]` | `//span[text()="Cancel"]` |

### Cover Photo Change

```
trigger → open-url (profile) → tab-loaded → event-click (cover) → delay
  → event-click (upload) → delay → upload-file → delay → event-click (position)
  → event-click (save) → delay → end
```

**XPath Selectors:**
| Step | Main Selector | Fallback Selector |
|------|--------------|-------------------|
| Cover photo area | `//div[@aria-label="Cover photo"]` | `//div[contains(@style,"cover")]` |
| Update cover | `//span[text()="Update cover photo"]` | `//div[@aria-label="Update cover photo"]` |
| Upload photo | `//span[text()="Upload photo"]` | `//div[text()="Upload photo"]` |
| Save changes | `//div[@aria-label="Save changes"]` | `//span[text()="Save changes"]` |

---

## Pattern 2: Post to Facebook (Page/Profile)

### Post — Text Only

```
trigger → open-url (facebook) → tab-loaded → event-click (create post) → delay
  → press-key (write content) → delay → event-click (post button) → delay
  → wait-for-publish → end
```

### Post — With Media

```
trigger → open-url → tab-loaded → event-click (create post) → delay
  → event-click (photo/video) → delay → upload-file → delay
  → press-key (write caption) → delay → event-click (post button) → delay
  → event-click (close) → end
```

**XPath Selectors:**
| Step | Main Selector | Fallback Selector |
|------|--------------|-------------------|
| Create a post | `//div[@aria-label="Create a post"]` | `//span[text()="Create a post"]` |
| Photo/video | `//div[@aria-label="Photo/video"]` | `//span[text()="Photo/video"]` |
| Feeling/activity | `//div[@aria-label="Feeling/activity"]` | `//span[text()="Feeling/activity"]` |
| Live video | `//div[@aria-label="Live video"]` | `//span[text()="Live video"]` |
| Post button | `//div[@aria-label="Post"]` | `//span[text()="Post"]` |
| Text input (new) | `//div[@role="textbox" and @aria-label="Create a post"]` | `//div[@role="textbox"][1]` |
| Close composer | `//div[@aria-label="Close"]` | `//div[contains(@aria-label,"close")]` |

---

## Pattern 3: Share Post

```
trigger → open-url (target post) → tab-loaded → event-click (share button) → delay
  → event-click (share destination) → delay → press-key (add caption) → delay
  → event-click (share now) → delay → end
```

**XPath Selectors:**
| Step | Main Selector | Fallback Selector |
|------|--------------|-------------------|
| Share button | `//div[@aria-label="Send this to friends or post on your timeline."]` | `//span[text()="Share"]` |
| Share now | `//div[@aria-label="Share now"]` | `//span[text()="Share now"]` |
| Share to News Feed | `//span[text()="Share to News Feed"]` | `//div[contains(text(),"News Feed")]` |
| Share to Group | `//span[text()="Share to a group"]` | `//div[contains(text(),"group")]` |
| Share to Page | `//span[text()="Share to a Page"]` | `//div[contains(text(),"Page")]` |
| Write a comment (share) | `//div[@role="textbox" and @aria-label="Write a comment..."]` | `//div[@role="textbox"][1]` |

---

## Pattern 4: Comment on Post

```
trigger → open-url (post) → tab-loaded → event-click (comment box) → delay
  → press-key (write comment) → delay → press-key (Enter) → delay → end
```

**XPath Selectors:**
| Step | Main Selector | Fallback Selector |
|------|--------------|-------------------|
| Comment box | `//div[@role="textbox" and starts-with(@aria-label, "Write a comment")]` | `//div[@role="textbox"][@aria-label="Comment"]` |
| Submit comment | `//div[@aria-label="Press enter to post your comment"]` | `//div[@role="button" and @aria-label="Post"]` |
| Comment count | `//div[starts-with(@aria-label, "Comment:")]` | `//a[contains(@href,"comment")]` |

---

## Pattern 5: Like / React to Post

```
trigger → open-url (post) → tab-loaded → element-exists (like button)
  → match: event-click (like) → delay → end
  → fallback: → end
```

**XPath Selectors:**
| Step | Main Selector | Fallback Selector |
|------|--------------|-------------------|
| Like button (active: unlike) | `//div[@aria-label="Like" and @aria-pressed="true"]` | `//div[contains(@aria-label,"Like")]` |
| Like button (inactive: like) | `//div[@aria-label="Like" and @aria-pressed="false"]` | `//div[contains(@aria-label,"Like")]` |
| Like count | `//div[starts-with(@aria-label, "Like:")]` | `//span[contains(text(),"Like")]` |
| Love react | `//div[@aria-label="Love"]` | `//div[contains(@aria-label,"Love")]` |
| Haha react | `//div[@aria-label="Haha"]` | `//div[contains(@aria-label,"Haha")]` |
| Care react | `//div[@aria-label="Care"]` | `--` |

---

## Pattern 6: Navigation (Cross-Account)

ใช้ได้กับทุกบัญชี — ไม่มีชื่อเฉพาะ

| Element | XPath |
|---------|-------|
| Facebook logo | `//a[@aria-label="Facebook"]` |
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

## Pattern 7: Warm Facebook Activity

ใช้สำหรับ warming profile — ค่อยๆ เพิ่มกิจกรรมให้ดูเป็นธรรมชาติ

```
loop (cycle: 5-10 rounds per session)
  → random (3-7 second delay between actions)
  → open-url → tab-loaded
  → scroll → delay
  → element-exists (find likeable post) → event-click (like) → delay
  → scroll → event-click (comment) → press-key → delay → submit
  → scroll → event-click (share) → delay
  → element-exists (check notification) → event-click (notif) → delay
  → loop-breakpoint

per session:
  day 1-3: like only (5-10 likes)
  day 4-7: like + 1-2 comments
  day 8-14: like + comment + 1 share per session
  day 15+: full activity — like + comment + share + post
```

---

## Pattern 8: Group Post Collection

```
trigger → read-file-text (group UIDs) → open group → tab-loaded
  → event-click (Manage posts) → delay
  → event-click (Published) → delay
  → event-click (View in group) → delay
  → tab-url (get URL) → validate URL → file-action (save)
  → end
```

**XPath Selectors:**
| Step | Main Selector | Fallback Selector |
|------|--------------|-------------------|
| Manage posts | `//*[self::a or self::button or @role='button'][normalize-space(.)='Manage posts']` | `//*[self::a or self::button or @role='button'][contains(normalize-space(.),'Manage your content')]` |
| Published tab | `//*[self::a or self::button or @role='button'][normalize-space(.)='Published']` | `//a[normalize-space(.)='Published']` |
| View in group | `//*[self::a or self::button or @role='button'][normalize-space(.)='View in group']` | `//*[self::a or self::button or @role='button'][contains(normalize-space(.),'View in group')]` |

---

## Pattern 9: Reels Interaction

```
trigger → open-url (reels) → tab-loaded → delay
  → element-exists (reel link) → match: event-click → delay
  → event-click (like) → delay → event-click (comment) → delay
  → event-click (share) → delay
  → end
```

**XPath Selectors:**
| Element | XPath |
|---------|-------|
| Reel link | `//a[starts-with(@aria-label, "Reel by")]` |
| Reel like | `//div[@aria-label="Like"]` |
| Reel comment | `//div[@aria-label="Comment"]` |
| Reel share | `//div[@aria-label="Share"]` |
| Create story | `//a[contains(@aria-label, "Create story")]` |
| View story | `//a[contains(@aria-label, ", view story")]` |

---

## General XPath Best Practices

1. **Cross-account first** — ใช้ `starts-with()`, `contains()`, `normalize-space()` เสมอ — ไม่ hardcode ชื่อบัญชี
2. **`@aria-label` > `normalize-space(.)` > `@data-*` > `contains(@class)`** — เรียงลำดับ priority
3. **Fallback is mandatory** — ทุก selector หลักต้องมี selector สำรอง
4. **Wait for selector** — ใช้ `waitForSelector: true` + `waitSelectorTimeout: 5000` เสมอกับ click
5. **Scope selectors** — จำกัด scope ไปยัง dialog หรือ section ที่ active — avoid page-wide indexes
6. **Test on real profile** — selector ที่ใช้ได้ใน dev อาจใช้ไม่ได้ใน production environment
7. **Update when Facebook changes UI** — Facebook อัปเดต selector เป็นระยะ — ต้อง validate เป็นประจำ
