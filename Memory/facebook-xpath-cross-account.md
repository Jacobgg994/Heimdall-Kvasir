---
name: facebook-xpath-cross-account
description: "Facebook XPath patterns for multi-account automation — no hardcoded names, uses starts-with/contains only"
metadata: 
  node_type: memory
  type: reference
  created: 2026-07-17
  originSessionId: 82da365e-1d73-4bba-a0d0-1f1b5afed909
---

# Facebook Cross-Account XPath Knowledge

## Source
Drum XPath: News Feed (2 sessions, 110 unique XPaths) + View Live 2.0 workflow (27 XPaths)
Saved to: `skills/gemlogin-facebook/references/facebook-cross-account-xpaths.md`

## Key Principle
**Never hardcode page/person names in XPaths.** Use `starts-with()` or `contains()`.

## Core Reusable Patterns

### Navigation (static - safe to use exact match)
`//a[@aria-label="Home"]`, `//a[@aria-label="Reels"]`, `//a[@aria-label="Friends"]`, `//div[@aria-label="Your profile"]`, `//input[@aria-label="Search Facebook"]`

### Posts (dynamic - use starts-with)
- Actions: `//div[starts-with(@aria-label, "Actions for this post")]`
- Hide: `//a[starts-with(@aria-label, "Hide post by")]`
- Engagement: `//div[starts-with(@aria-label, "Like:")]`, `//div[starts-with(@aria-label, "Love:")]`

### Stories/Reels (dynamic - use contains/starts-with)
- Story: `//a[contains(@aria-label, ", view story")]`
- Reel: `//a[starts-with(@aria-label, "Reel by")]`

### Sponsored
`//div[contains(@aria-label, "sponsored")]`

### Reactions (in dialog)
`//div[@role="dialog" and @aria-label="Reactions"]//div[@role="button" and @aria-label="Like"]`

## Files
- `facebook-cross-account-xpaths.md` — full reference (no hardcoded names)
- `facebook-newsfeed-xpaths.md` — raw drum data with specific names
- `facebook-view-live-workflow.md` — View Live 2.0 workflow analysis (27 XPaths)

**Why:** Facebook uses dynamic content — page names, person names, and post authors change per account. Hardcoded XPaths break across accounts.
**How to apply:** When building GemLogin workflows for Facebook, only use XPaths from the cross-account reference. For new pages, drum first, then extract patterns using starts-with/contains.
