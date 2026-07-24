# 📱 Phone Bot

**Multi-Device Android Control Desktop App** — TikTok Shop & Shopee Affiliate Automation

Built with Electron + Vite + React + TypeScript · 15 Samsung Note 8 phones · Thai-market affiliate operations

---

## Quick Start

```bash
# Install
cd phone-bot
npm install

# Development (Electron + hot reload)
npm run dev

# Production build
npm run build

# Connect devices
bash scripts/connect-all.sh
```

## Architecture

```
Renderer (React + Canvas)
    ↕ IPC (contextBridge)
Main Process (Node.js)
  ├── DeviceManager    — ADB registry + connection pool
  ├── ScreencapLegacy  — Fallback screen capture (Phase 0)
  ├── InputController  — ADB input (tap/swipe/text/keyevent)
  └── (Phase 1) ScrcpyServer — 30 FPS H.264 streaming
```

## Current Status

**Phase 0 Complete** ✅ — Project scaffolded, TypeScript compiles clean, Vite builds successfully

- [x] Electron + Vite + React + TypeScript setup
- [x] ADB executor + DeviceManager
- [x] Screencap legacy mode
- [x] Input controller (tap/swipe/text/keyevent)
- [x] Device grid UI with health indicators
- [x] Single device view with click-to-tap
- [x] Quick actions (Home, Back, Recents, Screenshot)
- [x] Coordinate display + tap flash

**Next: Phase 1** — scrcpy server integration (30 FPS H.264 streaming)

## Project Structure

```
phone-bot/
├── electron/                # Main Process
│   ├── main.ts              # Entry point, window, IPC handlers
│   ├── preload.ts           # contextBridge API
│   ├── device-manager.ts    # ADB device registry
│   ├── adb-executor.ts      # Low-level ADB wrapper
│   ├── screencap-legacy.ts  # Screencap via exec-out
│   ├── input-controller.ts  # Input via adb shell
│   └── config.ts            # Paths, settings
├── src/                     # Renderer (React)
│   ├── api.ts               # IPC bridge wrapper
│   ├── types.ts             # Shared TypeScript types
│   ├── hooks/useDevices.ts  # Zustand device store
│   └── components/
│       ├── layout/TopBar.tsx
│       ├── grid/DeviceGrid.tsx, DeviceCard.tsx
│       └── device/DeviceView.tsx, ScreenCanvas.tsx, QuickActions.tsx
├── flows/examples/          # Sample automation flows
├── scripts/                 # Utility scripts
└── server/                  # scrcpy-server.jar (Phase 1)
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Desktop | Electron 33 |
| UI | React 19 + TypeScript 5.6 |
| Build | Vite 6 + vite-plugin-electron |
| State | Zustand 5 |
| Style | Tailwind CSS 3.4 |
| ADB | System ADB via child_process |

---

> 🪸 Built by CORAL + TIDE · 2026-07-11
