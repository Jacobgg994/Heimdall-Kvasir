# Facebook News Feed — XPath Reference

Learned from: Drum XPath on 2026-07-17
Source: `drum-xpath-20260717-184953.json` + `drum-xpath-20260717-184424.json`
Profile: 61561202806339 (50-profile farm)
Total unique XPaths: 110

---

## Pattern Summary

| Pattern | Count | Stability | Usage |
|---|---|---|---|
| `//a[@aria-label="..."]` | 32 | ⭐ High | Links with accessible names |
| `//a[normalize-space(.)="..."]` | 37 | Medium | Links by exact visible text |
| `//div[@aria-label="..."]` | 39 | ⭐ High | Interactive containers, actions menus, nav items |
| `//input[@aria-label="..."]` | 1 | ⭐ High | Search input |
| `//footer[@aria-label="..."]` | 1 | ⭐ High | Footer |

---

## 1. Navigation (Left Sidebar)

| Element | XPath |
|---|---|
| Facebook logo | `//a[@aria-label="Facebook"]` |
| Home | `//a[@aria-label="Home"]` |
| Reels | `//a[@aria-label="Reels"]` / `//a[normalize-space(.)="Reels"]` |
| Friends | `//a[@aria-label="Friends"]` / `//a[normalize-space(.)="Friends"]` |
| Marketplace | `//a[@aria-label="Marketplace"]` / `//a[normalize-space(.)="Marketplace"]` |
| Groups | `//a[normalize-space(.)="Groups"]` |
| Gaming | `//a[@aria-label="Gaming"]` |
| Your profile | `//div[@aria-label="Your profile"]` |
| Facebook menu | `//div[@aria-label="Facebook menu"]` |

### Pattern insight:
Facebook navigation uses **BOTH** `@aria-label` and `normalize-space(.)` patterns for the same links. The `@aria-label` version is more stable (matches exactly what the accessibility tree exposes). The `normalize-space(.)` version is a fallback when `aria-label` is not present.

---

## 2. News Feed — Post Actions

### Actions menu per post
Each post has an actions menu identified by post author:

```
//div[@aria-label="Actions for this post by {page_name}"]
```

Examples from real data:
```
//div[@aria-label="Actions for this post by 20th Century Studios"]
//div[@aria-label="Actions for this post by Big C"]
//div[@aria-label="Actions for this post by Iran International - English"]
//div[@aria-label="Actions for this post by Middle East Monitor"]
//div[@aria-label="Actions for this post by People's Spring"]
//div[@aria-label="Actions for this post by Phapok Eco Resort"]
//div[@aria-label="Actions for this post by ทันโลก กับ Thai PBS"]
```

### Hide post
```
//a[@aria-label="Hide post by {page_name}"]
```

Examples:
```
//a[@aria-label="Hide post by 20th Century Studios"]
//a[@aria-label="Hide post by Big C"]
//a[@aria-label="Hide post by Ubonrat Thaonoi - อุบลรัตน์ เถาว์น้อย"]
```

### Open menu for sponsored content
```
//div[@aria-label="Open menu for {sponsor} sponsored content"]
```
Examples:
```
//div[@aria-label="Open menu for AIS sponsored content"]
//div[@aria-label="Open menu for LINE for Business sponsored content"]
```

---

## 3. Stories

### View story
```
//a[@aria-label="{page_name}, view story"]
```
Examples: `Big C, view story`, `ทันโลก กับ Thai PBS, view story`

### Create story
```
//a[normalize-space(.)="Create storyShare a photo, video or write something"]
```
Note: Facebook concatenates "Create story" with "Share a photo..." — use `contains()`:
```
//a[contains(@aria-label, "Create story")] 
```

---

## 4. Reels

```
//a[@aria-label="Reel by {creator}"]
```
Examples:
```
//a[@aria-label="Reel by Boy Tattoo2.0"]
//a[@aria-label="Reel by Dreamy ASMR"]
//a[@aria-label="Reel by Media Queen"]
//a[@aria-label="Reel by Trip To Africa"]
```

---

## 5. Post Composer

| Element | XPath |
|---|---|
| Live video | `//div[@aria-label="Live video"]` |
| Photo/video | `//div[@aria-label="Photo/video"]` |
| Create story link | `//a[contains(normalize-space(.), "Create story")]` |

---

## 6. Search

```xpath
//input[@aria-label="Search Facebook"]
```

---

## 7. Footer Links

| Element | XPath |
|---|---|
| Footer container | `//footer[@aria-label="Facebook"]` |
| Ad Choices | `//a[normalize-space(.)="Ad Choices"]` |
| Advertising | `//a[normalize-space(.)="Advertising"]` |
| Cookies | `//a[normalize-space(.)="Cookies"]` |

---

## 8. Page/Profile Links in Feed

Every page/post author in the feed has clickable name links:

```xpath
//a[@aria-label="{page_name}"]
//a[normalize-space(.)="{page_name}"]
```

From this drum (50-profile feed), detected pages:
- 20th Century Studios
- Az-Zubair Van Leesten
- Big C
- Iran International - English
- Middle East Monitor
- People's Spring
- Phapok Eco Resort
- Ubonrat Thaonoi - อุบลรัตน์ เถาว์น้อย
- ทันโลก กับ Thai PBS
- LINE for Business
- AIS
- Media Queen
- Boy Tattoo2.0
- Dreamy ASMR
- JEJAK SI ADEN REAL
- RS fashion
- Trip To Africa

---

## Key Learnings for Automation

### 1. Always prefer `@aria-label` over `normalize-space(.)`
- `aria-label` is more stable (Facebook's accessibility layer)
- `normalize-space(.)` is a fallback when aria-label is absent

### 2. Dynamic content in selectors
Facebook feeds are dynamic — page names change constantly.
Use patterns with variables:
```xpath
//a[@aria-label="{target_page_name}"]
//div[@aria-label="Actions for this post by {target_page_name}"]
```

### 3. Sponsored content detection
```xpath
//div[starts-with(@aria-label, "Open menu for ") and contains(@aria-label, "sponsored")]
```

### 4. Thai-language content
Facebook preserves Thai names in `aria-label` — XPath must handle Unicode:
```xpath
//a[@aria-label="ทันโลก กับ Thai PBS, view story"]
```

### 5. Long text normalization
Some text like `"Create storyShare a photo..."` is concatenated.
Use `contains()`:
```xpath
//a[contains(@aria-label, "Create story")]
//a[contains(normalize-space(.), "Create story")]
```

### 6. Input elements
Only one input was found on the News Feed: `//input[@aria-label="Search Facebook"]`
Comment textboxes only appear inside posts/dialogs (not on the main feed).

---

## For ARKA 🔧 (Workflow Creation)

When building Feed-interaction workflows:
- **Scroll trigger**: Use incremental scroll to load more posts
- **Post detection**: `//div[starts-with(@aria-label, "Actions for this post by")]`
- **Hide sponsored**: `//a[starts-with(@aria-label, "Hide post by")]`
- **React**: Must hover first, then select from `//div[@role="dialog" and @aria-label="Reactions"]`
- **Comment**: Only available after clicking into a post (opens dialog)

## For LUMI 📖 (Analysis)

This drum confirms:
- Facebook News Feed **does not use `data-testid`** — all selectors rely on `aria-label`
- The feed is **infinite scroll** — drum with scroll=5 captured 110 unique XPaths
- Most XPaths are **person/page-specific** — reusable patterns use `starts-with()` or `contains()`
- **No `role="article"`** was captured — Facebook may have removed this
