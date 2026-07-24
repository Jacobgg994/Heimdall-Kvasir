# Phone Bot — Feature Research Results

> Research date: 2026-07-11
> Sources: Escrcpy, QtScrcpy, ScrcpyGUI v4, guiscrcpy, Total Control, AirDroid Business, STF, Ghost in the Droid, TikMatrix, TikTok Warmup, GeeLark, Vysor, and others.

---

## Category 1: Screen Mirroring & Remote Control

| Feature | Reasoning |
|---|---|
| **Real-time screen streaming (30-60 FPS via MediaCodec)** | Core requirement. scrcpy's native approach (ADB tunnel + hardware-accelerated H.264) outperforms Vysor's approach by 2-3x in latency. Use scrcpy binary directly, not `adb screencap` polling — screencap is ~100-300ms per frame; scrcpy delivers 16-30ms. |
| **Screen-off operation** | Critical for phone farms running 24/7. Saves battery, reduces heat. Every major tool supports this. Without it, you destroy screens with burn-in. |
| **Audio forwarding (recent scrcpy builds)** | Needed for TikTok video audition, Shopee live stream monitoring. |
| **Camera mode (front/rear)** | ScrcpyGUI v4 has a dedicated "Pro Camera Mode." Useful for TikTok video preview without touching the phone. |
| **Virtual display / desktop mode** | Create a separate Android desktop separate from the phone's physical screen. Useful for running long tasks without interrupting what's on the phone's main display. |
| **Clipboard sync (bidirectional)** | Copy text on PC, paste into any device (and vice versa). Huge time-saver when managing multiple accounts. |

---

## Category 2: Multi-Device Grid & Batch Operations

This is where Phone Bot can differentiate significantly from basic mirroring tools.

| Feature | Reasoning |
|---|---|
| **Customizable grid layouts (1x1, 2x2, 3x3, 4x4, list)** | Every pro tool has this. Escrcpy supports it. The key insight: users need to see 9-16 phones simultaneously, not just 4. |
| **Device grouping with tags/labels** | Total Control and AirDroid Business support this. Let users group phones by purpose (e.g., "TikTok warmup group A," "Shopee CS group," "test batch"). Execute operations per group. |
| **Broadcast input mode (one keystroke → all selected devices)** | **This is a killer feature.** Total Control calls it "synchronized control." Send the same tap/swipe/text to N phones simultaneously. Essential for installing the same app or logging into the same service across many phones. |
| **Object-based sync (not coordinate-based)** | Total Control's smartest feature. Instead of "tap (x,y)," use UI node queries. This works across different screen resolutions. Tap the "Login" button, not position (540, 1200). |
| **Batch APK install (drag & drop)** | QtScrcpy and AirDroid Business support this. Drop one APK → installs on all selected devices. |
| **Batch file push/pull (per device or group)** | Push config files, media content, scripts. Pull screenshots, logs, recordings. |
| **Batch screenshot on timer** | Take screenshots of all devices every N minutes. Useful for monitoring what's happening during unattended automation runs. |
| **Batch screen recording** | Record all devices simultaneously. Essential for debugging failed automation runs. |

---

## Category 3: Automation & Scripting

Your MVP plan includes "flow automation (tap/swipe/text sequences)." Here's what pro-level looks like:

| Feature | Reasoning |
|---|---|
| **Visual workflow builder (block-based)** | GeeLark's no-code RPA builder and Total Control's AAIS scripting represent two ends. A visual builder (drag blocks: Tap, Swipe, Type, Wait, Loop, Condition) lowers the barrier. Even if you ship a script-based system first, plan the visual builder for v2. |
| **UI element detection (not just coordinate taps)** | Apps change layouts. Coordinate-based scripts break on next TikTok update. Use `adb shell uiautomator dump` to get XML hierarchy, then query by text/resource-id. OpenCV template matching for icon detection. |
| **OCR / screen text reading** | TikTok warmup scripts need to detect "Following" vs "Follow" button state. Without OCR, your flow automation is blind. Tesseract or Google ML Kit. |
| **Condition / branch logic in scripts** | "If 'Follow' button visible → tap it. Else → swipe up." Without conditions, automation can't handle variability. |
| **Loop with counters and break conditions** | "Repeat 50 times: like, pause 3-5s, swipe up, pause 2-4s." Real TikTok warming follows this pattern. |
| **Cron-style scheduler** | Most phone farm work is time-based. "Every day at 08:00, warm up accounts." "Every 2 hours, check for messages." TikMatrix, Ghost in the Droid, and AirDroid Business all support scheduling. |
| **Script recording (record & replay)** | Let users perform an action once, record the sequence, and replay it. Total Control and QtScrcpy support this. Massively reduces scripting effort. |
| **Randomized delays and coordinates** | Platforms detect robotic timing. Scripts must randomize tap coordinates within a small radius and delays within ranges. This is what separates farmable accounts from banned accounts. |
| **Per-device job queue** | Ghost in the Droid has this. Each device has its own queue of automation jobs. Jobs persist across disconnections. Critical for unattended operation. |

---

## Category 4: Device Health & Monitoring

**Most underrated category in basic tools.** Pro phone farm operators NEED this.

| Feature | Reasoning |
|---|---|
| **Battery level & temperature dashboard** | Display all devices' battery % and temp in the grid header. AirDroid Business and ControlUp do this. Overheating kills phone batteries in ~6 months. Alert when any device exceeds 42°C. |
| **Device online/offline status with reconnect** | ADB connections drop. Phones crash. Your app should auto-reconnect and show connection status clearly. STF and AirDroid Business both do this. |
| **Storage monitoring (internal + SD)** | TikTok caches video data. Devices can fill up silently and stop working. Alert at 85% / 95% capacity. |
| **App crash detection** | TikTok/Shopee apps crash. Your tool should detect when the target app is no longer in the foreground and auto-restart it. |
| **Anomaly alert system** | "Device X battery dropped 30% in 10 minutes" = app stuck in a video-render loop. "Device Y has been offline for 2 hours" = dead phone. |
| **Uptime tracking** | Track how long each device has been running without reboot. Phones need periodic reboots (every 48-72h) to maintain stability. |
| **Screen recording of failed automation runs** | When an automation script errors, save the last 30 seconds of screen recording for debugging. Massive time-saver. |

---

## Category 5: Input & Interaction

| Feature | Reasoning |
|---|---|
| **Customizable keyboard mapping** | Map PC keys to phone actions. Escrcpy, QtScrcpy, guiscrcpy all support this. Example: F1 = Home, F2 = Back, F3 = App Switch, Space = Tap center. |
| **Mouse gesture support** | Swipe gestures mapped to mouse drag + modifier key. Speeds up common scrolling patterns. |
| **Virtual navigation bar** | guiscrcpy's "bottom panel" has Home/Back/Recents buttons for each device. Small but daily-used feature. |
| **HID keyboard/mouse (OTG mode)** | ScrcpyGUI v4's standout feature. Simulates a physical keyboard connected via USB. Avoids Android's input injection restrictions on some apps. |
| **Multi-touch / pinch-zoom** | Some TikTok creator actions need pinch gestures. Not supported by basic input tap. |
| **Type text at full speed** | ADB `input text` is slow. Use ADBKeyBoard (broadcast-based input) or `am broadcast -a ADB_INPUT_TEXT` for near-instant text input across all devices. |

---

## Category 6: Content & File Management

| Feature | Reasoning |
|---|---|
| **Centralized media library** | AirDroid Business has this. A library of videos/images/audio that can be pushed to any device or group. For TikTok content farms — push the day's videos to all phones at once. |
| **Bulk content push with scheduling** | "Push content/ folder to all TikTok phones every day at 07:00." |
| **APK version management** | Track which version of TikTok/Shopee is installed on each device. Batch update when needed. |
| **Log aggregation** | All automation run logs from all devices → searchable single view. Ghost in the Droid does this. |

---

## Category 7: Network & Connectivity

| Feature | Reasoning |
|---|---|
| **Wireless ADB connection with auto-discovery** | Escrcpy has auto-discovery. Scan LAN for ADB-enabled devices. Also: save known devices list for quick reconnect. |
| **Proxy management per device** | **Critical for TikTok/Shopee.** Each account needs a different IP. Your app should let you assign a proxy (HTTP/SOCKS5) per device and apply it via ADB (WiFi proxy settings or VPN config). |
| **USB hub management** | Real phone farms use USB hubs. Detect which USB port a device is connected to, label it, and warn if it disconnects from that port. |
| **Reverse tethering (Gnirehtet)** | Escrcpy supports this. Share PC's internet connection to phones that can't use WiFi. Useful for phones in Faraday cages or USB-only setups. |

---

## Category 8: AI & Intelligent Features

| Feature | Reasoning |
|---|---|
| **LLM-powered UI understanding** | Escrcpy's "AI Copilot" (AutoGLM) lets you type "go to my profile and change bio" and it figures out the taps. Ghost in the Droid's LLM Skill Creator auto-generates workflows from screenshots. This is the future. |
| **Shadow ban / account health detection** | TikTok Warmup checks every 20 videos. Detect "shadow banned" state (0 views, restricted features) and alert. |
| **Intelligent delay randomization** | AI picks realistic human-like delays based on time of day. Morning = faster scrolls, late night = slower. |
| **Content uniqueness verification** | Before posting a video, verify it hasn't been posted from another account in the same farm. Duplicate content triggers platform bans. |

---

## Category 9: Anti-Detection & Environment (TikTok/Shopee Specific)

| Feature | Reasoning |
|---|---|
| **Device fingerprint viewer** | Show IMEI, Android ID, MAC, serial, build fingerprint for each device. Operators need to ensure diversity. |
| **GPS spoofing manager** | Set per-device GPS location that matches the proxy IP's geography. Essential for Shopee's location-based verification. |
| **WiFi SSID spoofing** | Phones broadcasting the same WiFi name triggers association flags. |
| **Language/locale batch config** | Set all devices to Thai (for Thai market). Batch-change system language and Google account locale. |
| **SIM / eSIM status viewer** | Know which devices have active SIMs (for OTP). Flag devices whose SIM has been dormant > 30 days. |
| **Account login state monitor** | Track which accounts are logged in on each device and their session state. TikTok needs re-login every ~7-14 days. |

---

## Category 10: Team Collaboration (For Future Scale)

| Feature | Reasoning |
|---|---|
| **Device locking / checkout** | STF's device booking system. "Operator A is using device 7." Prevents two people controlling the same phone. |
| **Permission roles** | Admin (full access) vs Operator (use assigned devices only) vs Viewer (monitor only). |
| **Remote team access** | Web-based control panel (like STF) so team members don't need to be on the same LAN. |

---

## Quick Wins — What to Add to MVP First

These are the highest-impact, lowest-effort additions relative to your current MVP plan:

1. **Battery/temp overlay on each device card** (ADB `dumpsys battery` — trivial to implement)
2. **Proxy assignment per device** (critical for TikTok/Shopee)
3. **Device grouping with tag/label system**
4. **Broadcast input mode** (send same tap to all devices in a group)
5. **UI element detection** (uiautomator dump instead of raw coordinates)
6. **Auto-reconnect on ADB disconnect**
7. **Screenshot on demand + batch screenshot**
8. **Randomized delays in flow scripts** (without this, accounts will be banned)
9. **APK drag-drop install**
10. **Offline/online status with visual indicator**

---

## Sources

- [Escrcpy](https://github.com/viarotel-org/escrcpy) — Electron + Vue 3 multi-device scrcpy GUI with AI Copilot
- [ScrcpyGUI v4](https://github.com/AsithaKanchana1/scrcpy-gui) — Tauri + React scrcpy GUI with HID input, camera mode
- [QtScrcpy](https://github.com/barry-ran/QtScrcpy) — Qt-based multi-device control with batch operations
- [guiscrcpy](https://github.com/srevinsaju/guiscrcpy) — PyQt5 scrcpy GUI with color-coded multi-device
- [Total Control](https://www.sigma-rt.com/en/tc) — Commercial multi-device control with 200+ phone support
- [AirDroid Business](https://www.airdroid.com/business/) — Enterprise MDM with kiosk, bulk deployment, health monitoring
- [STF (Smartphone Test Farm)](https://github.com/DeviceFarmer/stf) — Open-source browser-based phone farm (13.7k stars)
- [VK DeviceHub](https://github.com/VKCOM/devicehub) — STF fork with iOS support
- [Ghost in the Droid](https://github.com/ghost-in-the-droid/android-agent) — Python phone farm framework with LLM-powered skills
- [TikMatrix](https://github.com/tikmatrix/tikmatrix-desktop) — TikTok-specific phone farm automation desktop app
- [TikTok Warmup](https://github.com/Hormold/tiktok-warmup) — TypeScript TikTok account warming via ADB + Gemini Vision
- [GeeLark](https://www.geelark.com) — Cloud phone farm with no-code RPA builder
- [OpenPocket](https://github.com/pockebot/openpocket) — AI-agent Android control framework
- [MoreLogin / Phone Farm Cost Comparison](https://k.morelogin.com/blog/cloudphone-vs-phone-farm) — 2026 cost analysis
- [DeepADB](https://www.npmjs.com/package/deepadb) — MCP server with 204 ADB tools for AI agents
