# Phone Farm Operations Reference

Quick reference for operating the Boxphone (`gemphonefarm`) fleet.

## Fleet snapshot (as of 2026-05-21)

| Bucket | Count | Notes |
|---|---|---|
| Total devices | 60 | Mostly Samsung Note 8 (N950F/N), some S7 (G930F, rooted), 2 newer (A155F, A366B) |
| Online | 58 | Healthy default state |
| Offline | 2 | `USB-A155F-MAIN`, `SM-G930F` id 24 — reboot/re-pair |
| Group TH (id 2) | 4 | Hong Kong residential proxy |
| Group VN (id 1) | 4 | Singapore residential proxy |
| Group US (id 3) | 4 | US residential proxy |
| Ungrouped | 48 | No proxy assigned — egress is your home IP **(fix this in week 1)** |

## Hardware roles (mixed-fleet doctrine)

| Model | Best role | Why |
|---|---|---|
| Samsung Note 8 (N950F/N) on Android 9 | Mid-tier posting + warming | Bulk of the fleet; reliable; mid-trust signal |
| Samsung S7 (G930F, rooted) | Engagement farm + LINE | Cheap; rooted; expendable for cold-DM bans |
| Samsung A15/A16 5G *(buy in W1)* | Tier-1 TikTok posting (top accounts) | Fresh Android 14+ fingerprint = better algo reach |
| Samsung A55/A56 *(buy in M2)* | Buyer farm — real purchases for trust signal | Premium fingerprint required for some payment apps |
| Pixel 6a/7a *(buy in M2)* | Dev/sensitive accounts | Cleanest Android, easiest root |
| iPhone XR/11 *(buy in M2)* | iOS slice; LINE TH | 60% of TH LINE traffic is iOS |
| Redroid emulators on 210.1.1.155 | Warming + scrape + non-payment | Free hardware on existing server |

## Proxy strategy

| Layer | Use | Spend |
|---|---|---|
| IPv6 /64 per device | Default; all browsing/posting | ~฿1–3k/mo for 1,000 /64s |
| IPv4 4G mobile (TH SIM) | Final-mile purchase, banking app touch | ~฿200/mo × 20 SIMs |
| IPv4 residential | Only for accounts that refuse IPv6 | Cap ฿5k/mo |

**Wire it:** assign IPv6 directly in gemphonefarm device config, or NAT at the gateway (Mikrotik / pfSense) so every connection gets a fresh /128 from a /64 pool.

## Tool reference (gemphonefarm MCP)

```python
# Inventory
list_devices()             # → list of devices with status/proxy/group
list_groups()              # → [{id, name}]
devices_by_group(group_id) # → devices in one group

# Lifecycle
start_device(id)           # bring online
close_device(id)           # power off / disconnect

# Automation (local API)
list_scripts()             # ⚠️ has returned 404 — local API may be down
execute_script(id, script_id, params)
check_script_status(task_id)
kill_script(task_id)

# Automation (cloud — works when local is down)
cloud_start_automation(workflow_id, device_id, parameter, soft_id, token)

# Organisation
create_group(name)
assign_device_to_group(device_id, group_id)
```

## Throughput math (conservative, 16hr/day)

| Operation | Per phone / day | 60-device fleet |
|---|---|---|
| TikTok organic posts | 3–5 | 180–300 |
| TikTok engagement (likes/comments/views) | 100–200 | 6,000–12,000 |
| LINE messages (warm accounts) | 200–500 | 12,000–30,000 |
| Shopee/Lazada browse + add-to-cart | 30–50 | 1,800–3,000 |
| Google Maps reviews | 5–10 | 300–600 |

## Daily ops checklist

| Time | Action |
|---|---|
| 08:00 | Call `list_devices()` — confirm ≥55 online; flag offline ones for VA repair |
| 08:30 | Pull last 24hr `affiliate_clicks` report; rank products by CTR |
| 09:00 | Generate today's content batch via `/api/admin/ai/generate` (Gemini batch) |
| 09:30 | Queue posts via cloud automation; stagger 5–10 min between phones |
| 12:00 | Midday CTR check; double-down hero products |
| 18:00 | Daily revenue check — TikTok Shop dashboard + our `/r/<slug>` redirect logs |
| 21:00 | Close devices that completed their post cycle; rotate which accounts post tomorrow |

## Account hygiene rules

1. **One TikTok account per phone, ever.** Switching = ban signal.
2. **Don't post identical content to >5 accounts in <30 min.** Stagger across hours.
3. **Warm new accounts 7 days before first affiliate post.** Watch / like / follow only.
4. **Rotate hashtags every 7 days.** Same hashtag stack across 40 accounts = visible cluster.
5. **Burn accounts gracefully.** When TikTok flags one, retire that phone for 14 days before re-using its hardware fingerprint.
6. **One Shopee buyer-account ID per cluster of ~5 phones.** Don't link a single Shopee ID to 40 devices.

## Failure modes + recovery

| Symptom | Diagnose | Fix |
|---|---|---|
| `list_scripts` 404 | Local API `:1256` is down on the controller box | Switch to `cloud_start_automation`; investigate `:1256` separately |
| Device shows offline but proxy ip works | OTG cable / power | Have VA re-plug and reboot |
| All TikTok posts from one phone get <100 views | Account or fingerprint flagged | Cool that phone for 14 days; rotate to a different account |
| Cluster of 5+ phones all bad reach | Pattern detection on IP or content | Switch the cluster to a new IPv6 /64; vary content templates |
| Cloud automation never returns | API auth or workflow ID changed | Re-pull `soft_id` + `token` from gemphonefarm cloud dashboard |
