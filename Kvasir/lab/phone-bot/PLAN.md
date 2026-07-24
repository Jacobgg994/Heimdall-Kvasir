# Phone Bot v2 — Multi-Device Android Control Desktop App

> 🪸 Architecture Plan — Updated 2026-07-11 from research findings

## Context

JACOB ต้องการโปรแกรม Desktop สำหรับควบคุมมือถือ Android 15+ เครื่อง (Samsung Note 8) 
ผ่าน ADB — ดูหน้าจอ, ควบคุมคลิก/แตะ, สร้าง automation flows สำหรับ TikTok Shop + Shopee Affiliate

### Key Insight from Research

**แผนเดิมใช้ `adb screencap` + `adb shell input tap` — จากการวิจัยพบว่าใช้จริงไม่ได้:**
- `screencap`: 6-7 FPS, 150ms latency, 8MB/frame → ใช้ได้แค่ screenshot รายครั้ง
- `input tap`: 700ms/tap เพราะ spawn Java process ทุกคำสั่ง
- `shell` เปิด/ปิดต่อคำสั่ง: CPU หนักมากที่ scale 15+ เครื่อง

**แนวทางใหม่**: ใช้ scrcpy-style custom Java server (MediaCodec H.264 streaming + InputManager injection)

---

## 🏗️ Architecture v2

```
┌──────────────────────────────────────────────────────────────┐
│                    🖥️  Phone Bot                              │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Renderer Process (React + Canvas)                   │   │
│  │                                                      │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  TopBar: [Grid] [Flows] [Health] [Content]  │    │   │
│  │  ├─────────┬─────────┬─────────┬─────────┬──────┤    │   │
│  │  │ 📱 N8-1 │ 📱 N8-2 │ 📱 N8-3 │ 📱 ...  │      │    │   │
│  │  │ 35°C ██ │ 38°C ██ │ 42°C ██ │         │      │    │   │
│  │  │ TikTok  │ Shopee  │ TikTok  │  DEVICE  │      │    │   │
│  │  │ ┌────┐  │ ┌────┐  │ ┌────┐  │  GRID    │      │    │   │
│  │  │ │live│  │ │live│  │ │live│  │          │      │    │   │
│  │  │ └────┘  │ └────┘  │ └────┘  │ (click→) │      │    │   │
│  │  ├─────────┴─────────┴─────────┴──────────┤      │    │   │
│  │  │       SINGLE DEVICE VIEW                │      │    │   │
│  │  │  ┌─────────────────────────────────┐    │      │    │   │
│  │  │  │  H.264 Stream Canvas (30 FPS)   │    │      │    │   │
│  │  │  │  ← click → InputManager (5ms)   │    │      │    │   │
│  │  │  │  📍 (540, 1200) [TikTok:Like]   │    │      │    │   │
│  │  │  └─────────────────────────────────┘    │      │    │   │
│  │  │  [Home] [Back] [🔍 UI Inspect] [Flow]   │      │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  └──────────────┬──────────────────────────────────────┘   │
│                 │ IPC (contextBridge)                       │
│  ┌──────────────┴──────────────────────────────────────┐   │
│  │  Main Process (Node.js)                             │   │
│  │                                                     │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  DeviceManager                               │    │   │
│  │  │  - ADB device registry (track-devices)      │    │   │
│  │  │  - Connection pool (persistent shells)      │    │   │
│  │  │  - Auto-reconnect + keepalive               │    │   │
│  │  │  - Wireless ADB discovery (LAN scan)        │    │   │
│  │  │  - Device grouping (tags/labels)            │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  ScrcpyServer (scrcpy-server.jar wrapper)   │    │   │
│  │  │  - Push JAR → shell app_process launch      │    │   │
│  │  │  - Video: VirtualDisplay→MediaCodec H.264   │    │   │
│  │  │  - Control: InputManager.injectInputEvent() │    │   │
│  │  │  - 3 sockets per device: video/audio/ctrl   │    │   │
│  │  │  - Coordinate calibration (virtual display) │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  InputController                             │    │   │
│  │  │  - Direct (InputManager via control socket) │    │   │
│  │  │  - Fallback (adb shell input tap)           │    │   │
│  │  │  - Broadcast mode (same input→N devices)    │    │   │
│  │  │  - Randomized jitter (tap ±3px, delay ±15%) │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  UIAutomator                                 │    │   │
│  │  │  - uiautomator dump → XML parse             │    │   │
│  │  │  - Element query (text/resource-id/desc)    │    │   │
│  │  │  - Coordinate extraction for UI elements    │    │   │
│  │  │  - Cache hierarchy (avoid re-dumping)       │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  DeviceHealth                                │    │   │
│  │  │  - Battery level + temp + charging status   │    │   │
│  │  │  - Storage monitor (TikTok cache alert)     │    │   │
│  │  │  - App crash detection (foreground check)   │    │   │
│  │  │  - Anomaly alerts + uptime tracking         │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  FlowEngine                                  │    │   │
│  │  │  - Load/save flows (JSON + new schema)      │    │   │
│  │  │  - Execute with randomized delays           │    │   │
│  │  │  - Conditional branching (UI element state)  │    │   │
│  │  │  - Loops with counters + break conditions   │    │   │
│  │  │  - Cron scheduler (per-device, per-group)   │    │   │
│  │  │  - Per-device job queue (survive reconnect) │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  ContentManager                              │    │   │
│  │  │  - Media library (videos/images/audio)      │    │   │
│  │  │  - Batch push to devices/groups             │    │   │
│  │  │  - Scheduled content delivery               │    │   │
│  │  │  - Video re-encode (fingerprint diversity)  │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  GPFBridge (optional)                        │    │   │
│  │  │  - Sync device list from GemphoneFarm       │    │   │
│  │  │  - Import/export flows                      │    │   │
│  │  │  - Dual-control coordination                │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  IPC Channels (Main ↔ Renderer)                     │   │
│  │                                                      │   │
│  │  devices:list, device:frame, device:status           │   │
│  │  device:health (battery/temp/storage)                │   │
│  │  input:command, input:broadcast                      │   │
│  │  ui:dump, ui:query, ui:element                       │   │
│  │  flow:execute, flow:save, flow:progress              │   │
│  │  content:push, content:list                          │   │
│  │  screen:subscribe, screen:calibrate                  │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
/home/admin_jacob/phone-bot/
├── package.json
├── electron-builder.yml
├── tsconfig.json
├── vite.config.ts
│
├── electron/                       # Main Process
│   ├── main.ts                     # Entry: BrowserWindow, IPC
│   ├── preload.ts                  # contextBridge
│   ├── device-manager.ts           # ADB registry + connection pool
│   ├── scrcpy-server.ts            # JAR push, launch, socket management
│   ├── screencap-legacy.ts         # Fallback method (low FPS)
│   ├── input-controller.ts         # Direct + broadcast + jitter
│   ├── ui-automator.ts             # uiautomator XML parsing
│   ├── device-health.ts            # Battery/temp/storage/crash
│   ├── flow-engine.ts              # Flow execution + scheduler
│   ├── content-manager.ts          # Media library + batch push
│   ├── gpf-bridge.ts               # GemphoneFarm integration
│   └── config.ts                   # Paths, settings, presets
│
├── src/                            # Renderer (React)
│   ├── main.tsx
│   ├── App.tsx
│   ├── types.ts                    # Shared types
│   ├── hooks/
│   │   ├── useIPC.ts
│   │   ├── useDevices.ts           # Zustand device store
│   │   └── useFlow.ts              # Flow state
│   ├── components/
│   │   ├── layout/
│   │   │   ├── TopBar.tsx          # Custom title bar + nav
│   │   │   └── StatusBar.tsx       # ADB status, device count
│   │   ├── grid/
│   │   │   ├── DeviceGrid.tsx      # Multi-device grid
│   │   │   ├── DeviceCard.tsx      # Card: thumbnail + health
│   │   │   └── GroupPanel.tsx      # Group filter sidebar
│   │   ├── device/
│   │   │   ├── DeviceView.tsx      # Single device full view
│   │   │   ├── ScreenCanvas.tsx    # H.264 stream + click
│   │   │   ├── QuickActions.tsx    # Home/Back/Recents/Screenshot
│   │   │   ├── UIInspector.tsx     # Element tree viewer
│   │   │   └── CoordinateDisplay.tsx # Live x,y + element info
│   │   ├── health/
│   │   │   ├── HealthOverlay.tsx   # Battery/temp on card
│   │   │   ├── HealthPanel.tsx     # Full health dashboard
│   │   │   └── AlertBadge.tsx      # Warning indicators
│   │   ├── flow/
│   │   │   ├── FlowBuilder.tsx     # Create/edit flows
│   │   │   ├── FlowRunner.tsx      # Execute + progress
│   │   │   ├── FlowLibrary.tsx     # Saved flows browser
│   │   │   ├── FlowStepEditor.tsx  # Edit individual steps
│   │   │   └── Scheduler.tsx       # Cron-style scheduling
│   │   ├── content/
│   │   │   ├── ContentLibrary.tsx  # Media browser
│   │   │   └── PushDialog.tsx      # Push to devices dialog
│   │   └── settings/
│   │       ├── SettingsPanel.tsx
│   │       ├── ProxyConfig.tsx     # Per-device proxy
│   │       └── DeviceProfile.tsx   # Tags, notes, groups
│   └── styles/
│       ├── index.css               # Dark theme base
│       └── variables.css           # Design tokens
│
├── server/                         # scrcpy-server resources
│   └── scrcpy-server.jar           # Bundled JAR (v3.x)
│
├── flows/                          # Saved flows
│   └── examples/
│       ├── tiktok-warmup.json
│       ├── tiktok-post.json
│       └── shopee-search.json
│
├── resources/                      # App assets
│   └── icon.png
│
└── scripts/
    ├── connect-all.sh
    ├── health-check.sh
    └── tune-tcp.sh                 # sysctl tuning for multi-device
```

---

## 📐 Key Technical Decisions

### 1. Screen Streaming: scrcpy Server Mode

**ไม่ใช้ adb screencap loop — ใช้ scrcpy-server.jar ที่ push เข้า device**

```
Architecture per device:
┌──────────────────────────────────────────────┐
│  Main Process                                │
│  ┌──────────────────────────────────────┐    │
│  │ 1. adb push scrcpy-server.jar        │    │
│  │ 2. adb shell CLASSPATH=...           │    │
│  │    app_process / scrcpy.Server       │    │
│  │ 3. adb forward tcp:27183 → video     │    │
│  │ 4. adb forward tcp:27184 → control   │    │
│  │ 5. TCP socket → FFmpeg decode → IPC  │    │
│  └──────────────────────────────────────┘    │
└──────────────────────────────────────────────┘
         │ USB or TCP/IP
    ┌────▼────────────────────────────┐
    │  Device (Samsung Note 8)         │
    │  scrcpy-server.jar running as    │
    │  shell user via app_process      │
    │                                  │
    │  VirtualDisplay → Surface →      │
    │  MediaCodec H.264 → TCP socket   │
    │                                  │
    │  InputManager.injectInputEvent() │
    │  ← control socket commands       │
    └──────────────────────────────────┘
```

**Performance:**
| Metric | screencap (Old) | scrcpy (New) |
|--------|----------------|--------------|
| FPS | 6-7 | 30-60 |
| Latency | 150ms | 25-50ms |
| Bandwidth | 8MB/frame | ~2KB delta frame |
| CPU (host) | High (PNG decode) | Low (HW decode) |
| Input latency | 700ms | 5ms |

**Fallback**: screencap mode สำหรับ devices ที่ JAR ใช้ไม่ได้ (Android 5.x หรือ ARM32)

### 2. Input: Dual-Mode

```
Primary:  scrcpy control socket → InputManager.injectInputEvent()
          - Tap, swipe, text, keyevent → 5ms latency
          - Text via ADBKeyBoard broadcast for instant typing
          - Random jitter: tap ±3px, delay ±10-20%

Fallback: adb shell input tap (700ms)
          - สำหรับ devices ที่ JAR ไม่ได้
          - Broadcast mode: fork N commands parallel
```

### 3. Shell Sessions: Persistent Pool

```
// BAD (Old plan): opens/closes ADB per command
adb -s <serial> shell input tap 500 800    // ~700ms
adb -s <serial> shell input tap 600 900    // ~700ms

// GOOD (New): persistent shell per device
const shell = await deviceManager.getShell(serial)  // open once
shell.exec("input tap 500 800")                     // ~50ms
shell.exec("input tap 600 900")                     // ~50ms
shell.close()                                       // close when done
```

**Benefit**: ลด CPU 80% เมื่อเทียบกับ open/close per command

### 4. Coordinate Calibration

scrcpy อาจสร้าง virtual display ที่ความละเอียดต่างจาก display จริง:

```
┌─────────────────────┐
│ Physical Display 0  │  1080x2340
│                     │
│  ┌───────────────┐  │
│  │ Virtual Disp   │  │  332x720 (scrcpy)
│  │                │  │
│  └───────────────┘  │
└─────────────────────┘

Solution:
- Auto-detect actual touch target display via dumpsys
- Map canvas coordinates → display coordinates via scale factor
- Test tap at known anchor → verify with screenshot → adjust
```

### 5. Anti-Detection: Randomized Everything

```
Flow Step BEFORE (old - detectable):
  {"action": "tap", "x": 300, "y": 1200, "desc": "Like"}
  {"action": "wait", "ms": 500}

Flow Step AFTER (new - human-like):
  {"action": "tap", "x": 300, "xRandom": 5, "y": 1200, "yRandom": 5, "desc": "Like"}
  {"action": "wait", "ms": 500, "msRandom": 150}
```

**All actions get:** coordinate jitter ±N pixels, time jitter ±X%, variable pause between actions

---

## 🔌 IPC Channels

| Channel | Direction | Purpose |
|---------|-----------|---------|
| `devices:list` | Main → Renderer | Push device registry (track-devices) |
| `device:frame` | Main → Renderer | H.264 frame for active device |
| `device:health` | Main → Renderer | Battery/temp/storage update |
| `device:status` | Main → Renderer | Online/offline/busy status |
| `input:command` | Renderer → Main | Single-device input |
| `input:broadcast` | Renderer → Main | Broadcast to group |
| `input:typing` | Renderer → Main | Text via ADBKeyBoard |
| `ui:dump` | Renderer → Main | Request UI hierarchy |
| `ui:query` | Renderer → Main | Find element by query |
| `flow:execute` | Renderer → Main | Start flow execution |
| `flow:save` | Renderer → Main | Save flow JSON |
| `flow:progress` | Main → Renderer | Step-by-step progress |
| `content:push` | Renderer → Main | Push media to devices |
| `content:list` | Renderer → Main | List media library |
| `screen:subscribe` | Renderer → Main | Start/stop stream |
| `screen:calibrate` | Renderer → Main | Coordinate calibration |

---

## 📝 Flow Format v2

```json
{
  "name": "TikTok Warm-Up Day 3",
  "version": 2,
  "platform": "tiktok",
  "orientation": "portrait",
  "resolution": "1080x1920",
  "randomization": {
    "coordinateJitter": 5,
    "delayVariation": 0.15,
    "startTimeWindow": [3600000, 7200000]
  },
  "steps": [
    {
      "action": "open_app",
      "package": "com.zhiliaoapp.musically",
      "desc": "Open TikTok"
    },
    {
      "action": "wait_for_element",
      "selector": {"text": "Following"},
      "timeout": 10000,
      "desc": "Wait for TikTok to load"
    },
    {
      "action": "swipe",
      "x1": 540, "y1": 1600,
      "x2": 540, "y2": 400,
      "duration": 300,
      "durationRandom": 100,
      "desc": "Swipe to next video"
    },
    {
      "action": "wait",
      "ms": 3000,
      "msRandom": 2000,
      "desc": "Watch video"
    },
    {
      "action": "tap_element",
      "selector": {"resourceId": "com.zhiliaoapp.musically:id/like"},
      "fallback": {"action": "tap", "x": 900, "y": 1200, "xRandom": 5, "yRandom": 5},
      "probability": 0.3,
      "desc": "Like (30% chance)"
    },
    {
      "action": "swipe",
      "x1": 540, "y1": 1600,
      "x2": 540, "y2": 400,
      "repeat": {"min": 10, "max": 25},
      "repeatInterval": {"min": 2000, "max": 8000},
      "desc": "Browse FYP 10-25 videos"
    },
    {
      "action": "keyevent",
      "code": 3,
      "desc": "Home"
    }
  ]
}
```

### New Action Types

| Action | Description |
|--------|-------------|
| `tap` | Coordinate tap with jitter |
| `tap_element` | UI element tap (uiautomator selector) with coordinate fallback |
| `swipe` | Swipe with duration randomization |
| `text` | Type text (via ADBKeyBoard) |
| `wait` | Delay with randomization |
| `wait_for_element` | Wait until UI element appears |
| `keyevent` | Android key event |
| `open_app` | Launch app by package name |
| `close_app` | Force-stop app |
| `screenshot` | Capture screenshot |
| `shell` | Raw ADB shell command |
| `condition` | Branch based on UI state |
| `loop` | Repeat sub-steps N times |
| `if_element` | Conditional: does element exist? |
| `notification_check` | Check for specific notification |

### Selector Format (for UI element actions)

```json
{
  "selector": {
    "text": "Following",
    "resourceId": "com.zhiliaoapp.musically:id/tab_text",
    "contentDesc": "Following tab",
    "className": "android.widget.TextView"
  }
}
```

---

## 🎨 Design System

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-primary` | `#080808` | Main background |
| `--bg-surface` | `#0d0d0d` | Cards, panels |
| `--bg-elevated` | `#141414` | Dialogs, tooltips |
| `--border` | `#1a1a1a` | Borders, separators |
| `--text-primary` | `#e5e5e5` | Primary text |
| `--text-secondary` | `#8a8a8a` | Secondary text |
| `--text-muted` | `#525252` | Muted/hint text |
| `--accent` | `#22c55e` | Primary action, online |
| `--accent-warning` | `#eab308` | Warning, Shopee |
| `--accent-danger` | `#ef4444` | Error, offline, alert |
| `--accent-info` | `#3b82f6` | Info, TikTok |
| `--font` | `JetBrains Mono` | Monospace code |
| `--font-ui` | `Inter` | UI text |
| `--font-th` | `Sarabun` | Thai text |
| `--radius` | `6px` | Border radius |

**Window**: Frameless, custom title bar, dark theme, `minWidth: 1280, minHeight: 720`

---

## 🚀 Implementation Plan

### Phase 0 — Foundation (Week 1)
**Goal**: โปรเจกต์ scaffold + ADB connection + basic screencap

| # | Task | Owner | Est. |
|---|------|-------|------|
| 0.1 | Init Electron + Vite + React + TypeScript project | TIDE | 2h |
| 0.2 | Dark theme + custom title bar + layout shell | PYKE | 3h |
| 0.3 | ADB executor + DeviceManager (track-devices, connection pool) | TIDE | 4h |
| 0.4 | Persistent shell sessions (reuse per device) | TIDE | 3h |
| 0.5 | Screencap legacy mode (adb exec-out screencap → PNG → IPC) | TIDE | 3h |
| 0.6 | DeviceGrid: show connected devices with status | PYKE | 3h |
| 0.7 | DeviceView + ScreenCanvas (screencap mode, click→tap) | PYKE | 4h |
| 0.8 | QuickActions: Home, Back, Recents, Screenshot | TIDE | 2h |
| 0.9 | CoordinateDisplay + calibration | PYKE | 2h |

**Verify**: เปิดโปรแกรม → เห็นมือถือ 15 เครื่องใน grid → คลิกเครื่อง → เห็นหน้าจอ (screencap) → คลิกที่จอ = มือถือตอบสนอง

### Phase 1 — Core Streaming + Input (Week 2)
**Goal**: scrcpy server integration = 30 FPS streaming + 5ms input

| # | Task | Owner | Est. |
|---|------|-------|------|
| 1.1 | Bundle scrcpy-server.jar (v3.x) | DRIFT | 1h |
| 1.2 | ScrcpyServer: push JAR, launch via app_process, socket setup | TIDE | 6h |
| 1.3 | H.264 decoder → Canvas rendering (FFmpeg or MediaSource) | TIDE | 5h |
| 1.4 | InputController via control socket (InputManager) | TIDE | 4h |
| 1.5 | InputController fallback (adb shell input tap) | TIDE | 2h |
| 1.6 | Coordinate calibration (virtual vs physical display) | TIDE | 3h |
| 1.7 | Switch screencap → scrcpy in DeviceView | PYKE | 2h |
| 1.8 | Keyboard shortcuts (F1=Home, F2=Back, Space=Tap center) | PYKE | 2h |

**Verify**: 30 FPS streaming, click latency <50ms, Home/Back responsive, keyboard shortcuts work

### Phase 2 — Device Health + Groups (Week 2-3)
**Goal**: ไม่ให้เครื่องพังโดยไม่รู้ตัว

| # | Task | Owner | Est. |
|---|------|-------|------|
| 2.1 | DeviceHealth: battery %, temp, charging, storage | TIDE | 2h |
| 2.2 | HealthOverlay on DeviceCard (green/yellow/red) | PYKE | 2h |
| 2.3 | AlertBadge: temp>42°C, storage>90%, offline>5min | PYKE | 1h |
| 2.4 | HealthPanel: full dashboard per device | PYKE | 3h |
| 2.5 | Auto-reconnect on ADB disconnect | TIDE | 2h |
| 2.6 | Device groups: create, tag, filter (TikTok/Shopee/All) | PYKE | 3h |
| 2.7 | GroupPanel: sidebar filter | PYKE | 1h |
| 2.8 | Auto-reboot reminder (every 48-72h) + schedule reboot | TIDE | 2h |

**Verify**: เห็น battery/temp ทุกเครื่อง, alert เมื่อร้อน/ใกล้เต็ม, จัดกลุ่มได้, reconnect อัตโนมัติ

### Phase 3 — Flow Engine v2 (Week 3)
**Goal**: Automation ที่ไม่โดนแบน

| # | Task | Owner | Est. |
|---|------|-------|------|
| 3.1 | FlowEngine: load/save v2 format with randomization | TIDE | 4h |
| 3.2 | UIAutomator: dump XML, parse, cache hierarchy | TIDE | 4h |
| 3.3 | UIInspector: element tree viewer in DeviceView | PYKE | 4h |
| 3.4 | FlowBuilder: click screen → add element-based step | PYKE | 5h |
| 3.5 | FlowStepEditor: edit, reorder, delete, test single step | PYKE | 3h |
| 3.6 | FlowRunner: execute with progress + randomization | TIDE | 4h |
| 3.7 | Conditional branching: if_element, loop, condition | TIDE | 3h |
| 3.8 | Cron scheduler: per-device, per-group, per-flow | TIDE | 3h |
| 3.9 | Per-device job queue (persist across disconnect) | TIDE | 2h |
| 3.10 | Example flows: tiktok-warmup, tiktok-post, shopee-search | TIDE | 3h |

**Verify**: สร้าง flow → element-based steps → randomize → รันบน 3 เครื่อง → ทุกเครื่องทำงานไม่เหมือนกันเป๊ะ

### Phase 4 — Broadcast + Batch Ops (Week 4)
**Goal**: ทำครั้งเดียว = ทั้ง farm

| # | Task | Owner | Est. |
|---|------|-------|------|
| 4.1 | Broadcast mode: same tap → all devices in group | TIDE | 3h |
| 4.2 | Broadcast UI: select group, send, see all respond | PYKE | 2h |
| 4.3 | Batch APK install (drag-drop → all devices) | TIDE | 2h |
| 4.4 | Batch screenshot (all devices → one click) | TIDE | 2h |
| 4.5 | Batch screen recording trigger | TIDE | 1h |
| 4.6 | Proxy config per device (settings → ADB) | TIDE | 3h |
| 4.7 | ProxyConfig UI panel | PYKE | 2h |

**Verify**: กด tap บน group → ทุกเครื่องตอบสนอง, ลาก APK → ติดตั้งทุกเครื่อง

### Phase 5 — Content Management (Week 4-5)
**Goal**: จัดการ content 15 เครื่องจากที่เดียว

| # | Task | Owner | Est. |
|---|------|-------|------|
| 5.1 | ContentManager: media library scan + index | TIDE | 3h |
| 5.2 | ContentLibrary UI: browse, preview, tag | PYKE | 4h |
| 5.3 | Push to device/group with progress | TIDE | 2h |
| 5.4 | Scheduled push ("every day 07:00 → TikTok group") | TIDE | 2h |
| 5.5 | Video re-encode for fingerprint diversity | TIDE | 3h |
| 5.6 | Drag-drop from desktop → auto-push to selected device | PYKE | 2h |

**Verify**: เลือกวิดีโอ 5 ไฟล์ → push ไป 10 เครื่อง TikTok → ทุกเครื่องได้ไฟล์

### Phase 6 — TikTok/Shopee Automation (Week 5-6)
**Goal**: Flows เฉพาะสำหรับ affiliate marketing

| # | Task | Owner | Est. |
|---|------|-------|------|
| 6.1 | TikTok warm-up pipeline (4-stage, 14-day schedule) | TIDE | 5h |
| 6.2 | TikTok batch video poster (randomized caption + hashtags) | TIDE | 4h |
| 6.3 | TikTok FYP browser (human-like scrolling patterns) | TIDE | 3h |
| 6.4 | Account health monitor: shadowban detection, view tracking | TIDE | 3h |
| 6.5 | Shopee affiliate link generator (via Open API) | SURGE | 3h |
| 6.6 | Shopee price/stock monitor + alert | SURGE | 2h |
| 6.7 | Commission XTRA scanner | SURGE | 2h |
| 6.8 | TikTok → Shopee funnel: auto-update bio link | TIDE | 2h |
| 6.9 | WARM-UP PIPELINE dashboard UI | PYKE | 4h |

**Verify**: Warm-up pipeline รัน 4 วัน → account แข็งแรง, post video batch 10 เครื่อง

### Phase 7 — Polish + Distribution (Week 6-7)
**Goal**: Package + monitor + ship

| # | Task | Owner | Est. |
|---|------|-------|------|
| 7.1 | GPF Bridge: sync device list from GemphoneFarm | TIDE | 3h |
| 7.2 | Dashboard: overview (all devices, health summary, queue) | PYKE | 4h |
| 7.3 | Keyboard shortcut customization | PYKE | 2h |
| 7.4 | electron-builder: package .deb, .AppImage, .exe | DRIFT | 3h |
| 7.5 | Auto-start, tray icon, minimize to tray | DRIFT | 3h |
| 7.6 | TCP tuning script (sysctl for 15+ WiFi devices) | DRIFT | 1h |
| 7.7 | Connect-all script with staggered timing | DRIFT | 1h |
| 7.8 | Log aggregation + export | TIDE | 2h |

**Verify**: Build .deb → ติดตั้ง → เปิดใช้ → 15 เครื่องทำงาน, tray icon minimize

---

## 🧪 Verification Checklist

```bash
# Dev mode
cd /home/admin_jacob/phone-bot
npm run dev          # Electron + React + hot reload

# Test by phase:
# Phase 0: ต่อ ADB → เห็น devices → screencap → click → phone taps
# Phase 1: scrcpy server → 30 FPS stream → 5ms input latency
# Phase 2: battery/temp alerts → group → reconnect
# Phase 3: create flow → randomize → run on 3 devices
# Phase 4: broadcast tap → all respond → batch APK
# Phase 5: push content → all phones get files
# Phase 6: warm-up pipeline → TikTok post batch
# Phase 7: .deb build → install → production use
```

---

## ⚠️ Known Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| scrcpy-server.jar ไม่รองรับ Android 7.1 (Note 8 บางเครื่อง) | ไม่ได้ 30 FPS | Fallback screencap mode |
| Virtual display ทำให้ coordinate เพี้ยน | Tap ผิดตำแหน่ง | Auto-calibration + manual offset |
| WiFi ADB หลุดบ่อยที่ 15 เครื่อง | Device offline | keepalive 15s + auto-reconnect |
| TikTok detect automation pattern | Account ban | Randomize ทุกอย่าง + human-like timing |
| Battery swelling หลังรันต่อเนื่อง | Hardware damage | Temp alert 42°C + auto-pause |
| Socket exhaustion ที่ 15+ streams | Connection fail | TCP tuning + staggered connect |

---

> 📅 Plan created: 2026-07-11 · JIMMY 🌊 + CORAL 🪸 · Based on 3-source deep research
