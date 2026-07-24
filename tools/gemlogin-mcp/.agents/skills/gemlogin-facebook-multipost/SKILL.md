---
name: gemlogin-facebook-multipost
description: Facebook/Matrix group posting automation — multi-round scheduling, category-based content routing, media management, and batch page distribution. Use when coordinating content distribution across multiple groups/pages, managing complex category matrices, or automating multi-phase posting campaigns.
---

# GemLogin Facebook MultiPost & Matrix Scheduling

Use this skill for coordinated Facebook group posting across multiple rounds and categories.

Pair with:
- `$gemlogin` for profile/script management
- `$gemlogin-profile-operations` for batch profile operations

## Matrix Posting Concept

"Matrix" routing is a 2D content distribution strategy:

```
        1st Round    2nd Round    3rd Round
SLOT:   2P + 1V      2P + 1V      2P + 1V      (P=photo, V=video)
UFABRO: 1P           1P           1V
FB:     1P           1P           1V
CASINO: 1P           1P           1V
```

Each **category** (SLOT, UFABRO, FOOTBALL, CASINO) has different media requirements per round.

**Goals:**
- Fan-out same content type to multiple pages in parallel
- Different content mix for each category × round combination
- Track which page + category + round was posted to avoid repeats

## Script Parameters for Matrix Posting

Standard Facebook multipost script signature:

| Parameter | Type | Purpose |
|---|---|---|
| `category` | string | One of: `SLOT`, `UFABRO`, `FOOTBALL`, `CASINO` |
| `round` | string | One of: `1st`, `2nd`, `3rd` |
| `media_folder` | path | Root folder containing category subfolders |
| `caption_file` | path | `.txt` file with line-separated captions |
| `pages_list` | path | `.txt` file with target page IDs or URLs |

Example folder structure:
```
C:\Media\
├── SLOT\
│   ├── video1.mp4
│   ├── photo1.jpg
│   └── photo2.jpg
├── UFABRO\
│   ├── photo_a.jpg
│   └── video_b.mp4
└── FOOTBALL\
    ├── promo.jpg
    └── ...
```

Example `captions.txt`:
```
🎰 Best slot game ever! Try now!
Win big today! 💰
Don't miss out - play now!
```

Example `pages.txt`:
```
100001234567890
https://facebook.com/groups/slot-traders
Page Slot Community
```

## Matrix Routing Logic

Before posting, script calculates media count:

```javascript
category = "SLOT"
round = "2nd"
→ media_count = { photos: 2, videos: 1 }
→ Select 2 random photos + 1 video from SLOT folder
→ Select random caption
→ Post to first page in pages_list
→ Repeat for all pages in list
```

For category **SLOT** (hardest):
- 1st round: 2 photos + 1 video
- 2nd round: 2 photos + 1 video
- 3rd round: 2 photos + 1 video

For categories **UFABRO, FOOTBALL, CASINO** (lighter):
- 1st round: 1 photo
- 2nd round: 1 photo
- 3rd round: 1 video

## Multi-Round Execution

Typical posting campaign:

1. **Day 1 → Round 1**
   ```
   Execute for each category: SLOT, UFABRO, FOOTBALL, CASINO
   Each calls script with round="1st"
   Distributes across profiles in batches
   ```

2. **Day 2 → Round 2**
   ```
   Same profiles, same categories, round="2nd"
   Uses different media mix (2nd round media set)
   Posts to same or different page set
   ```

3. **Day 3 → Round 3**
   ```
   Final round, round="3rd"
   SLOT still posts media, others post 1 video
   Wrap-up phase
   ```

## Execution Pattern

Real command:

```
gemlogin_execute_local_script(
  profile_id=[1, 2, 3],
  script_name="FB Smart Scheduler (Matrix Edition)",
  parameters={
    "category": "SLOT",
    "round": "1st",
    "media_folder": "C:\\Media",
    "caption_file": "C:\\captions.txt",
    "pages_list": "C:\\slot_pages.txt"
  },
  close_browser=false
)
```

Execution flow per profile:
1. Start profile
2. Load caption file (read all lines)
3. Load pages list (read all lines)
4. For each page:
   - Navigate to page
   - Open post composer
   - Calculate media count from category × round
   - Select random media from folder
   - Fill caption (random line)
   - Post
   - Log result to output file
5. Close profile

## Media File Organization

Keep media clean and consistent:

```
C:\Media\
├── SLOT\
│   ├── round1_photos\     (2 photos here)
│   ├── round2_photos\     (2 photos here)
│   ├── round3_videos\     (1 video here)
│   └── shared_video.mp4
├── UFABRO\
│   ├── round1_photos\     (1 photo here)
│   ├── round2_photos\     (1 photo here)
│   └── round3_videos\     (1 video here)
└── ... (FOOTBALL, CASINO)
```

Or flat folder per category:
```
C:\Media\SLOT\
  photo_a.jpg, photo_b.jpg, photo_c.jpg, video_1.mp4, video_2.mp4
```
Script randomly picks correct count and type.

## Pages List Format

One entry per line. Format variations allowed:

```
100001234567890
https://facebook.com/groups/my-slot-group
https://facebook.com/pages/about?id=123456
My Group Name (as displayed in browser)
12345 https://facebook.com/groups/123
```

Script tries to navigate to each entry as-is or infers Facebook URL pattern.

## Caption Rotation

Captions file: one per line

```
🎰 Best slot game! Click link below 👇
Win HUGE! Don't miss this chance 💰
MEGA SLOTS - PLAY NOW
```

Script picks random caption for each page post. Rotation spreads keywords across posts.

## Batch Profiling for Multi-Category Campaigns

Real workflow: "Post SLOT + UFABRO to 20 pages each, all rounds"

1. Profiles: [1, 2, 3, 4, 5, 6]
2. Categories: SLOT, UFABRO
3. Rounds: 1st, 2nd, 3rd

**Execution plan:**
```
Round 1 (Day 1):
  Profiles [1,2,3]: SLOT 1st round → pages 1–10
  Profiles [4,5,6]: UFABRO 1st round → pages 11–20

Round 2 (Day 2, 24h later):
  Profiles [1,2,3]: SLOT 2nd round → pages 1–10
  Profiles [4,5,6]: UFABRO 2nd round → pages 11–20

Round 3 (Day 3, 24h later):
  Profiles [1,2,3]: SLOT 3rd round → pages 1–10
  Profiles [4,5,6]: UFABRO 3rd round → pages 11–20
```

Total posts: 6 profiles × 2 categories × 3 rounds = 36 total posts

## Failure Handling

Per-page recovery:

| Failure | Action |
|---|---|
| Page URL invalid | Skip page, log error, continue next page |
| Caption load fails | Use default caption, continue |
| Media folder missing | Error out entire execution, report path |
| Post composer won't open | Retry 1× after reload, skip if still fails |
| Network timeout | Retry 1× with 5sec delay, fail to next page |

Command: use retries and close_browser=false to keep profile warm between pages.

## Audit & Logging

Output file format (auto-generated):

```
Execution: FB Smart Scheduler (Matrix Edition)
Timestamp: 2025-06-22T14:30:00Z
Category: SLOT
Round: 1st
Profile: 1
Pages: 20
Results:
  ✓ https://facebook.com/groups/slot-1 (caption: "Best slots...")
  ✓ https://facebook.com/groups/slot-2 (caption: "Win big...")
  ✗ https://facebook.com/groups/slot-3 (composer timeout)
  ✓ https://facebook.com/groups/slot-4 (caption: "🎰 Amazing...")
...
Summary: 19/20 posts successful
```

Keep log files for post-campaign analysis and replay if needed.

## Operating Rules

- **No duplicate posts**: verify page × category × round combination not in audit log before executing
- **24h spacing between rounds** to avoid spam flags
- **Batch size 3–5 profiles** per round to avoid overload
- **Test with 1–2 pages first** before fanning out to 20+
- **Media files must exist** — validate folder structure before execution
- **Keep captions fresh** — rotate or update captions file between rounds to avoid repetition detection
- **Monitor page health** — if pages start rejecting posts, pause 48h

## Integration Tips

Real end-to-end:

```
Step 1: Prepare media folders and caption files
Step 2: Create pages_list.txt with target pages
Step 3: For round in [1st, 2nd, 3rd]:
  For category in [SLOT, UFABRO, FOOTBALL, CASINO]:
    For profiles in [1,2,3,4,5,6]:
      Call gemlogin_execute_local_script(
        profile_id=[profiles],
        script_name="FB Smart Scheduler",
        parameters={category, round, media_folder, caption_file, pages_list}
      )
      Wait for completion
      Log results
    Sleep 30 min between categories
  Sleep 24h before next round
```
