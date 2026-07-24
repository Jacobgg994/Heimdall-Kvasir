# SOP — Phone Onboarding

How to take a fresh / wiped phone from box → farm-ready account-holder in 90 minutes per device.

## Prerequisites

- ADB installed on the controller machine
- gemphonefarm agent installed
- An IPv6 /64 block reserved for this device
- Optional: a Thai 4G SIM if this device will touch payment apps

## Step 1 — Hardware prep (5 min)

1. Factory reset the device (Settings → Reset → Factory data reset)
2. Boot, skip the setup wizard, decline all opt-ins
3. Disable lock screen (Settings → Lock screen → None)
4. Enable Developer Options (tap Build Number 7×)
5. Enable USB Debugging
6. Connect via USB to the controller; confirm `adb devices` shows it

## Step 2 — ROM + root (45 min)

**For Samsung S7 / Note 8 (Android 9 stock → LineageOS 18.1 / 19.1):**

1. Unlock bootloader via Samsung Developer Mode (OEM Unlock toggle)
2. Flash TWRP recovery via Odin
3. Boot into recovery, wipe / format data
4. Sideload LineageOS image
5. Sideload Magisk Delta (newer fork — passes Play Integrity Basic on these models)
6. Boot, complete LineageOS setup, decline Google sign-in for now

**For newer Samsung A series / Pixel:**

- Skip root unless the phone will be the controller — newer Android caps benefit less

## Step 3 — Bloat removal (10 min)

```bash
adb shell pm uninstall --user 0 com.samsung.android.app.spage
adb shell pm uninstall --user 0 com.samsung.android.bixby.agent
adb shell pm uninstall --user 0 com.samsung.android.app.galaxyfinder
adb shell pm uninstall --user 0 com.sec.android.app.samsungapps
adb shell pm uninstall --user 0 com.samsung.android.app.health
adb shell pm uninstall --user 0 com.sec.android.app.sbrowser
```

Reclaims ~200 MB RAM. Verify with `adb shell dumpsys meminfo`.

## Step 4 — Network config (15 min)

1. Connect phone to lab Wi-Fi (same as gemphonefarm host)
2. Set DHCP reservation for this MAC so device_id stays stable
3. Apply IPv6 /64 proxy in `Settings → Network → Proxy` (or via gemphonefarm device config)
4. Verify outbound IP: open Chrome → `whatismyip.com` — confirm it matches the assigned /64
5. If using a 4G SIM: insert, confirm carrier (AIS / dtac / TrueMove), no PIN lock

## Step 5 — App stack install (10 min)

Minimum install set:
- TikTok (TH region)
- LINE
- Shopee
- Lazada
- Facebook + Messenger
- Termux + Frida server (for advanced automation)

For privacy: install Aurora Store (FOSS), not Google Play. Avoids tying every install to a Google account.

## Step 6 — Account warm cycle (Days 1–7, no posting)

**Day 1:** Create TikTok account. Use a Thai phone number from your prepaid SIM. Set profile pic + bio in Thai. Browse home feed 20 minutes.

**Days 2–3:** Watch ~30 min/day of Thai TikTok content matching the persona. Follow 10–15 accounts in the niche.

**Days 4–5:** Like 50 videos / day. Comment 2–3 times in Thai (genuine reactions, not links).

**Day 6:** Save 5 videos. Share 1 video via DM (to a buddy account on another phone).

**Day 7:** Account is "warm." First affiliate post on Day 8.

## Step 7 — Register in gemphonefarm

1. In gemphonefarm UI: Add Device → select USB / OTG / Cloud
2. Confirm `device_id` matches ADB serial
3. Assign to correct group (TH for Thai-targeted, etc.)
4. Set displayName: `{country}-{node}-{persona}` (e.g. `TH-12-Anna`)
5. Test: send "open TikTok" script; confirm success in gemphonefarm logs

## Step 8 — Document the persona

Each phone gets a one-line file in `state/personas/{device_id}.md`:

```
device_id: ce051715aa8ae13b027e
displayName: TH-12-Anna
group: TH
proxy: ipv6 /64 fe80::abcd:1234/64
sim: AIS 081-234-5678
persona:
  age: 32
  city: Bangkok
  interests: skincare, productivity, cooking
  voice: housewife-savvy
created_at: 2026-05-22
```

This file lets any team member pick up the phone tomorrow without re-deciding personality.

## Quality gates

A device is "production ready" only if:

- [ ] Boots in < 30s
- [ ] adb devices recognizes it
- [ ] gemphonefarm shows it online for ≥5 min uninterrupted
- [ ] WhatIsMyIP returns the expected proxy IP
- [ ] TikTok account survived 7-day warm without verification challenge
- [ ] Persona file written

If any check fails → rerun the failing step or set the phone aside as a spare.

## Common pitfalls

| Problem | Fix |
|---|---|
| ADB device shown as "unauthorized" | Tap "Allow USB debugging" prompt on phone screen |
| Bootloop after Magisk install | Boot into recovery, uninstall Magisk via official zip |
| TikTok asks for ID verification immediately | Warm slower (14 days), use higher-quality proxy |
| Proxy works on browser but not in apps | Many apps ignore Android proxy — use the Mikrotik gateway approach |
| Account banned in <48h | Your fingerprint clusters with a flagged device. Switch IPv6 /64 + factory reset |
