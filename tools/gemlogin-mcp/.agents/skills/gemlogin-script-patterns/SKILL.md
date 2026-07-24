---
name: gemlogin-script-patterns
description: GemLogin script execution patterns — retry strategies, error handling, parameter validation, monitoring, and advanced orchestration. Use when building reliable automation workflows, debugging script failures, optimizing execution performance, or coordinating complex multi-script campaigns.
---

# GemLogin Script Execution Patterns

Use this skill for robust script execution, error recovery, and orchestration.

Pair with:
- `$gemlogin` for script discovery and tool reference
- `$gemlogin-profile-operations` for profile health and batch management

## Script Discovery & Selection

Find the right script before execution:

```
gemlogin_list_scripts()
→ Returns: [
    { "id": "abc123", "name": "YouTube View Booster", "parameters": [...] },
    { "id": "def456", "name": "TikTok Feed Warmer", "parameters": [...] },
    ...
  ]
```

Search by name (fuzzy):
```
gemlogin_find_script("YouTube")
→ Returns top 5 matches ranked by similarity
→ Use for user input (e.g., "boost youtube views")
```

Use exact script_id when programmatic, script_name when interactive:
```
Exact: script_id = "abc123"
Fuzzy: script_name = "YouTube Booster" (will find best match)
```

## Parameter Validation

Always inspect script schema before executing:

```
Call gemlogin_list_scripts(include_sensitive_defaults=false)
Check each script parameter:
  - "name": internal identifier
  - "label": UI label (what user sees)
  - "type": string, number, boolean, filepath, etc.
  - "required": true/false
  - "defaultValue": fallback if not provided
  - "description": usage hint

Validate user input against type:
  - type="number": must be int or float, not string
  - type="filepath": file must exist on local disk
  - type="string": split by newline if list expected
  - type="checkbox": accept true/false, yes/no, 1/0
```

Example: YouTube script parameters

```
Parameter: target_urls
  - type: string
  - description: "One per line"
  - validation: must be valid URLs or keywords
  - error if: empty or malformed

Parameter: min_watch_sec
  - type: number
  - validation: must be 30–3600, min < max
  - error if: negative or min_watch_sec > max_watch_sec
```

## Basic Execution Command

Minimal syntax:

```
gemlogin_execute_local_script(
  profile_id=[1, 2, 3],           # required: list of profile IDs
  script_name="YouTube Booster",  # required: script_name OR script_id
  parameters={                    # optional: param dict
    "target_urls": "https://youtube.com/watch?v=ABC",
    "min_watch_sec": 120
  }
)
```

Returns:
```
{
  "script_id": "abc123",
  "requested_profiles": [1, 2, 3],
  "success_count": 3,             # completed successfully
  "running_count": 0,             # still running
  "results": [
    {
      "profile_id": 1,
      "attempts": 1,
      "execute_success": true,
      "execute_response": {"success": true, ...},
      "is_running": false,
      "status_response": {"is_running": false, ...}
    },
    ...
  ]
}
```

## Retry Strategy

Use `retries` parameter for resilience:

```
gemlogin_execute_local_script(
  profile_id=[1, 2, 3],
  script_name="My Script",
  retries=3,                    # try up to 3 times
  retry_delay_seconds=2.0       # wait 2 sec between retries
)
```

Built-in retry flow per profile:
1. Attempt 1: start script
2. If fail → wait 2 sec → Attempt 2
3. If fail → wait 2 sec → Attempt 3
4. If fail → mark as failed, continue to next profile

**Recommendation:**
- Default: `retries=1` (no retry; fast)
- For flaky networks: `retries=2` (1 retry)
- For critical runs: `retries=3` (2 retries)
- For very critical: `retries=5` (4 retries) + increase `GEMLOGIN_TIMEOUT=120`

## Exact Script Name Matching

By default, `script_name` matches fuzzy:

```
User provides: "YouTube Booster"
Candidates:
  - "YouTube View Booster Elite" (score: 0.95) ← picked
  - "YouTube Channel Warmer" (score: 0.60)
  - "YouTube Playlist Viewer" (score: 0.55)
```

To enforce exact name match:

```
gemlogin_execute_local_script(
  profile_id=[1],
  script_name="YouTube View Booster Elite",
  require_exact_script_name=true   # disable fuzzy, must match exactly
)
```

If not found: raises error with candidates.

**When to use:**
- Interactive mode: `require_exact_script_name=false` (user-friendly fuzzy)
- Automated pipelines: `require_exact_script_name=true` (safe, explicit)

## Monitoring Script Status

Check if script is still running:

```
gemlogin_check_local_script_status(script_id="abc123", profile_id=1)
→ {
    "is_running": true,
    "progress": 0.45,              # 45% done
    "elapsed_seconds": 120,
    "estimated_remaining_sec": 150,
    "current_step": "Watching video..."
  }
```

Polling pattern (for long-running scripts):

```
for attempt in range(60):  # poll for up to 60 × 5sec = 5 min
  status = gemlogin_check_local_script_status(script_id, profile_id)
  if not status.get("is_running"):
    print(f"Script finished at step: {status.get('current_step')}")
    break
  print(f"Progress: {status.get('progress', 0)*100:.0f}%")
  sleep(5)
```

## Killing Long-Running Scripts

Stop a script before completion:

```
gemlogin_kill_local_script(script_id="abc123", profile_id=1)
→ { "success": true, "killed": true }
```

Use when:
- Script hangs or loops infinitely
- User cancels
- Timeout exceeded

## Advanced: Close Browser Flag

Option to close the browser after script finishes:

```
gemlogin_execute_local_script(
  profile_id=[1, 2],
  script_name="My Script",
  close_browser=true    # auto-close browser after script ends
)
```

Default: `close_browser=false` (browser stays open for inspection).

**Use cases:**
- `close_browser=false` → keep browser for debugging, multiple sequential scripts
- `close_browser=true` → clean shutdown, next profile ready immediately

## Multi-Script Orchestration

Real workflow: "Run Script A, then Script B on same profiles"

```
# Step 1: Execute Script A
result_a = gemlogin_execute_local_script(
  profile_id=[1, 2, 3],
  script_name="Warm Up",
  close_browser=false
)

if result_a["success_count"] < 3:
  print("Warm up failed on some profiles, but continuing...")

# Step 2: Execute Script B (profiles still open)
result_b = gemlogin_execute_local_script(
  profile_id=[1, 2, 3],
  script_name="Post to Feed",
  close_browser=true    # now close after this
)

# Step 3: Report combined results
print(f"Warm-up: {result_a['success_count']}/3")
print(f"Post: {result_b['success_count']}/3")
```

## Error Analysis

When script fails, check the response:

```
result = gemlogin_execute_local_script(...)

for r in result["results"]:
  if not r["execute_success"]:
    print(f"Profile {r['profile_id']} failed:")
    print(f"  Attempts: {r['attempts']}")
    print(f"  Error: {r['execute_response']}")
    print(f"  Status: {r['status_response']}")
```

Common errors:

| Error | Cause | Fix |
|---|---|---|
| `script_name not found` | Script doesn't exist locally | Run `gemlogin_list_scripts()`, check exact name |
| `profile_id not found` | Profile closed or doesn't exist | Check profile still exists, may need to restart |
| `timeout` | Script took too long (>60 sec default) | Increase `GEMLOGIN_TIMEOUT=120` env var |
| `browser crash` | Script crashed the browser | Review script logs, may need to patch script |
| `ambiguous script_name` | Multiple scripts have same exact name | Use `script_id` instead of `script_name` |

## Performance Tuning

Optimize for speed or reliability:

**Speed-focused (quick jobs like screenshots):**
```
gemlogin_execute_local_script(
  profile_id=[1, 2, 3, 4, 5],
  script_name="Quick Screenshot",
  retries=1,            # no retries
  close_browser=true    # close immediately
)
```

**Reliability-focused (complex workflows):**
```
gemlogin_execute_local_script(
  profile_id=[1, 2, 3],
  script_name="Complex Warm-up",
  retries=3,                      # retry 3x
  retry_delay_seconds=5.0,        # wait 5sec between
  close_browser=false             # keep for inspection
)
```

**Batch-focused (many profiles):**
```
# Split into smaller batches
batch_size = 10
for batch in chunk(profile_ids, batch_size):
  result = gemlogin_execute_local_script(
    profile_id=batch,
    script_name="Batch Script",
    retries=1             # lower retry for speed
  )
  print(f"Batch {batch}: {result['success_count']}/{len(batch)}")
  sleep(30)  # cool-down between batches
```

## Sensitive Parameters & Security

Script parameters may contain secrets:

```
gemlogin_list_scripts(include_sensitive_defaults=false)  # default
→ Masks defaultValue for fields like "token", "password", "apikey"

gemlogin_list_scripts(include_sensitive_defaults=true)   # unmasked
→ Shows real defaults (use carefully, don't log/print)
```

**Rule:** Never print or commit script output containing:
- Tokens, API keys, bearer auth
- Passwords, session IDs
- Cookies, fingerprint data
- Private URLs or identifiers

When passing secrets via `parameters`:
```
# ✗ Bad: don't print result
result = gemlogin_execute_local_script(
  ...,
  parameters={"api_token": "secret123"}
)
print(result)  # may leak token

# ✓ Good: handle sensitively
result = gemlogin_execute_local_script(
  ...,
  parameters={"api_token": "secret123"}
)
if result["success_count"] > 0:
  print("Executed successfully")  # don't print params
else:
  print("Failed (not showing error details for security)")
```

## Best Practices Checklist

- ✓ Validate parameters before execution
- ✓ Use `retries=2` for production workflows
- ✓ Monitor with `gemlogin_check_local_script_status`
- ✓ Log results but not sensitive parameters
- ✓ Close profiles after batch to free resources
- ✓ Use `require_exact_script_name=true` in automated pipelines
- ✓ Test with 1–2 profiles first, then scale
- ✓ Set `GEMLOGIN_TIMEOUT=120` for first-time script runs (slow)
- ✓ Space batches 30–60 sec apart to avoid overload
- ✓ Kill stuck scripts after 10 min timeout
