---
name: gemlogin-profile-operations
description: GemLogin profile lifecycle workflows — warm profiles, batch startup/shutdown, health checks, group operations, and monitoring. Use when managing account warmup, parallel profile execution, profile state tracking, or coordinating multi-profile operations at scale.
---

# GemLogin Profile Operations

Use this skill for profile management at scale — warming, batch control, and group-based operations.

Pair with:
- `$gemlogin` for tool registration and raw API docs
- `$gemlogin-edit` when profiles need configuration changes

## Profile Lifecycle States

Each profile has:
- `id`: integer profile identifier
- `name`: human-readable name (e.g., "Frilly-Language")
- `group_id`: optional group membership for bulk operations
- `proxy`: proxy config (IP:port or type)
- `browser_type`, `browser_version`: engine config
- `profile_path`: local disk location
- `note`: user comment field

Before running profiles, check:
```bash
gemlogin_status          # activeBrowsers count, feature flags
gemlogin_list_profiles   # full inventory, group assignments
```

## Account Warm-up Workflow

Safe warm-up pattern for new or cold personas:

1. **List and filter**
   ```
   Call gemlogin_list_profiles
   Filter to target_ids (e.g., group == "New Signups")
   ```

2. **Parallel batching** (avoid overload)
   - Start batch 1 (profiles 1–10)
   - Wait for all to reach `remote_debugging_address`
   - Attach Puppeteer / Playwright to each
   - Run gentle browse for 15–30 minutes
   - Scroll 3–5 times per minute, click 1–2 times per page
   - Click neutral links only (no logins, purchases, forms)
   - Close profiles batch 1
   - Repeat for batch 2, 3, etc.

3. **Timing**
   - Each profile start: 5–15 seconds
   - Browse session: 15–30 minutes
   - Profile close: 2–5 seconds
   - Parallel factor: `min(batch_size, available_CPU / 2)`

## Multi-Profile Execution (Parallel Fan-Out)

Use this pattern for script execution across many profiles:

1. **Resolve profiles**
   ```
   If user says "group:Marketing", call gemlogin_list_profiles and filter by group_id
   Otherwise use explicit profile_id list
   ```

2. **Execute with retry**
   ```
   Call gemlogin_execute_local_script(
     profile_id=[1,2,3,...],
     script_name="My Script",
     retries=2,
     retry_delay_seconds=2.0
   )
   ```

3. **Monitor results**
   ```
   success_count = sum of results where execute_success == true
   Report failures per profile
   If success_count < target, propose retry or fallback
   ```

## Group-Based Operations

Pattern for multi-persona content distribution:

1. **List groups**
   ```
   Call gemlogin_list_groups
   Display name, profile_count, description
   ```

2. **Fan-out to a group**
   ```
   Ask: "Which group? Which action? (post, warm, screenshot)"
   Filter profiles by group_id
   Execute action in parallel batches of 5–10
   Report success/failure per profile
   ```

Example: "Post to group Marketing"
- List groups → find "Marketing" group id
- Filter profiles where group_id == "Marketing" → [10, 11, 12, ...]
- For each profile: start, attach browser, run post script, close
- Summary: "Posted to 12 profiles in Marketing. 11 OK, 1 failed (profile 10, retrying...)"

## Profile Status & Health Checks

Call regularly during long-running operations:

```
gemlogin_status
→ activeBrowsers: 5 (running count)
→ uptime_seconds: 3600 (API health)
→ cloudMode: true (cloud fallback enabled)
```

If `activeBrowsers > expected` for 5+ min:
- Check for leaked browser processes
- Manual `gemlogin_stop_profile(stuck_id)` if needed
- Log incident for GemLogin team

## Error Recovery Patterns

| Error | Symptom | Fix |
|---|---|---|
| Profile already running | `start` returns error | Close with `gemlogin_stop_profile` first |
| Timeout on start | takes >20 sec | Set `GEMLOGIN_TIMEOUT=120`, retry once |
| Browser crash during run | script hangs, `is_running` gone false | `gemlogin_kill_local_script`, then retry |
| Group not found | filter returns empty list | Verify group name in `gemlogin_list_groups` |
| All profiles busy | `activeBrowsers` near max | Batch wait: close current batch, then start next |

## Script + Profile + Group Integration

Real workflow: "Warm profiles 1–20 for 25 min each, batches of 5"

1. Resolve profiles → [1,2,3,4,5,6,7,...]
2. Batch 1: Start profiles [1,2,3,4,5]
3. Wait for all 5 to report `remote_debugging_address`
4. Attach Puppeteer to each, run browse script in parallel
5. After 25 min, close batch 1
6. Repeat for batch 2, 3, 4

Command pattern:
```
gemlogin_start_profile(1)  # returns remote_debugging_address
→ Puppeteer.connect(remote_debugging_address)
→ Run 25-min browse
gemlogin_stop_profile(1)
```

If user provides `script_name` instead of manual browse:
```
gemlogin_execute_local_script(
  profile_id=[1,2,3,4,5],
  script_name="Account Warm-up Basic",
  parameters={"duration_minutes": 25}
)
```

## Operating Rules

- **Close profiles when done** unless user explicitly asks to keep open
- **Batch size 5–10** to avoid CPU spike and API overload
- **Check activeBrowsers** before starting next batch — if count doesn't drop, wait 5–10 sec
- **Log all fan-out results** to summary table: profile_id | status | error (if any)
- **For group operations**, always confirm the right group before fan-out
- **Never hardcode profile_ids** — filter from actual `gemlogin_list_profiles` output
