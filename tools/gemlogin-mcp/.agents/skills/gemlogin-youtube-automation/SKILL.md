---
name: gemlogin-youtube-automation
description: YouTube automation patterns for GemLogin — view boosting, watch time engagement, search-first mode, like/sub interactions, and metrics tracking. Use when optimizing YouTube content discovery, simulating organic viewing patterns, or automating channel engagement workflows.
---

# GemLogin YouTube Automation

Use this skill for YouTube-specific workflows like view boosting, watch time padding, and interaction farming.

Pair with:
- `$gemlogin` for profile/script management
- `$gemlogin-profile-operations` for batch profile warm-up before YouTube runs

## YouTube Script Parameters

Standard YouTube automation script signature:

| Parameter | Type | Range | Purpose |
|---|---|---|---|
| `target_urls` | string (multiline) | URLs or keywords | Links to watch or search terms for keywords |
| `min_watch_sec` | number | 30–600 | Minimum watch time (seconds) per video |
| `max_watch_sec` | number | 60–1800 | Maximum watch time (seconds) per video |
| `interaction_rate` | number | 0–100 | Percent chance to like/subscribe (%) |
| `search_mode` | boolean | true/false | If true, search first; if false, direct URL |
| `min_scroll_clicks` | number | 1–10 | Min clicks while video plays |
| `max_scroll_clicks` | number | 2–20 | Max clicks while video plays |
| `comment_chance` | number | 0–100 | Percent chance to add comment (%) |

## Search-First Mode vs. Direct URL

**Direct URL mode:**
- User provides: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Script opens URL directly
- Faster, deterministic, useful for targeted video boosts
- Fingerprint risk: many views from same profile on same URL can flag automation

**Search-First mode:**
- User provides: `"how to make bread"` or `"cute cats compilation"`
- Script searches on YouTube
- Clicks a random result (top 3–5)
- Slower but more organic-looking
- Randomizes video selection, reduces detection risk
- Better for channel-level warm-up (not specific video boost)

## Configuring YouTube Scripts

Example: "Run YouTube Booster on profiles 1–5, watch 2–5 min per video, 20% like chance"

1. **Find the script**
   ```
   gemlogin_find_script("YouTube View Booster Elite")
   → Returns script_id, parameter schema
   ```

2. **Execute with parameters**
   ```
   gemlogin_execute_local_script(
     profile_id=[1,2,3,4,5],
     script_name="YouTube View Booster Elite",
     parameters={
       "target_urls": "https://youtube.com/watch?v=VIDEO_ID_1\nhttps://youtube.com/watch?v=VIDEO_ID_2",
       "min_watch_sec": 120,
       "max_watch_sec": 300,
       "interaction_rate": 20,
       "search_mode": false
     }
   )
   ```

3. **Monitor execution**
   ```
   Loop: call gemlogin_check_local_script_status(script_id, profile_id)
   Until is_running == false for all profiles
   Collect results and report
   ```

## Organic-Looking Engagement Pattern

To avoid bot detection, use:

- **Random watch time variance**
  - Min/Max gap = 60–120 sec spread (e.g., 120–240 sec)
  - Randomizes within that window
  - Avoid exact same watch times across profiles

- **Scroll & click during play**
  - Min 2–3 clicks per video
  - Max 5–8 clicks per video
  - Click randomly on video recommendations/comments while video plays
  - Spread clicks across video length

- **Like/Subscribe chance** (not 100%)
  - Set to 15–40% for natural engagement
  - 100% likes = obvious automation
  - Skip likes on some videos = human behavior

- **Comment insertion** (low %, optional)
  - Comment on maybe 1 in 10 videos
  - Comment pool: rotate generic replies ("Great content!", "Thanks!", "🔥")
  - Avoid repetitive comments

- **Search variation**
  - Use 5–10 different keyword searches per profile per session
  - Randomize search term selection from provided list
  - Mix branded + generic keywords

## Multi-URL Batching

When `target_urls` contains many links:

**Batch pattern:**
- Provide 3–5 URLs per execution
- Run multiple executions across multiple profiles
- Rotate URL sets so no two profiles watch identical sequence
- Example: 12 videos, 4 profiles
  - Profile 1: videos 1–3
  - Profile 2: videos 4–6
  - Profile 3: videos 7–9
  - Profile 4: videos 10–12

**Command:**
```
Execution 1: profiles=[1,2], urls=["vid1","vid2","vid3"]
Execution 2: profiles=[3,4], urls=["vid4","vid5","vid6"]
```

This distributes load and makes engagement look less coordinated.

## Interaction Farming Rules

| Goal | Config | Risk Level |
|---|---|---|
| Light warm-up | min_watch=30s, like_rate=5%, no comments | Low |
| Medium engagement | min_watch=120s, like_rate=20%, rare comments | Medium |
| Aggressive boost | min_watch=300s, like_rate=80%, many comments | High — flag risk |

**Recommendation:**
- For new channels: start Low, run weekly
- For established channels: Medium, run 2–3× per week
- Never run Aggressive on same video/channel repeatedly

## Troubleshooting YouTube Automation

| Symptom | Cause | Fix |
|---|---|---|
| All videos play 0 sec | YouTube blocks profile | Warm profile 24h first, retry |
| Like/Sub buttons don't register | Not logged in or session stale | Ensure profile has active YouTube session before run |
| Search mode opens wrong video | YouTube reranked results | Explicitly provide video URLs instead of keywords |
| Script times out | Video can't load (region block, deleted) | Check URL is accessible in browser, remove bad URLs |
| Comment fails to post | Shadowban or rate limit | Skip comment mode, try again in 24h |

## Best Practices

1. **Warm profiles first** — run account warm-up 24–48 hours before YouTube automation
2. **Space out watches** — wait 1–3 hours between executions on same profile
3. **Rotate profiles** — don't have same profile watch same video twice in 7 days
4. **Monitor channel metrics** — use YouTube Analytics to track organic lift after automation
5. **Avoid subscriber buttons** — subscribe bots are highly detected; focus on views + likes instead
6. **Real-time watches** — if possible, watch at realistic times (not 3 AM in batches)
7. **Log URLs + profiles** — keep audit trail of which profile watched which video for accountability

## Metrics Collection

After execution, report:

```
Script: YouTube View Booster Elite
Execution ID: 20250622_batch1
Profiles: [1, 2, 3, 4, 5]
Videos watched: 5 URLs × 5 profiles = 25 total views
Success rate: 24/25 (1 timeout on profile 3)
Avg watch time: 156 seconds
Likes recorded: ~5 (20% rate)
Estimated impact: +25 views, +5 likes, 5 subscription prompts
Next run: 2025-06-24 (48h gap)
```

## Integration with GemLogin Prompts

Use the built-in prompt for custom YouTube warm-up:

```
/warm_profile(profile_id, minutes)
```

This prompt suggests a gentle browse flow that prepares profiles for YouTube automation without triggering detection.
