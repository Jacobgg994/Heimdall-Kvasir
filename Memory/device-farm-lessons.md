---
name: device-farm-lessons
description: Device farm operation lessons — ADB, WiFi, Note 8 specs, common pitfalls
metadata:
  type: reference
  created: 2026-07-24
  originSessionId: 99ca41cb-3229-41ef-8b4c-1541286d772f
  modified: 2026-07-24T09:59:08.337Z
---

# Device Farm — Lessons Learned

## Device Inventory (confirmed 2026-07-24)

- **19x Samsung Galaxy Note 8 (SM-N950F)** — Android 10, 8-core, 5.4GB RAM (~3.6GB available), 53GB storage, Magisk root
- **1x Samsung Galaxy S21 FE 5G (SM-G990U)** — Android 14
- **Total: 20 devices**

## ADB Rules

- **WSL2 ADB ≠ Windows ADB**: device ต่อกับ Windows ผ่าน USB ต้องใช้ `powershell.exe -Command "adb ..."` เสมอ
- **WiFi ADB (port 5555)**: ต้องเปิดผ่าน USB ก่อนด้วย `adb tcpip 5555` — ถ้าหลุด USB แล้ว WiFi ADB ยังไม่เปิด จะต่อไม่ได้
- **Fast scan**: ใช้ .NET sockets runspace parallel scan (200ms timeout) — เร็วกว่า Test-NetConnection มาก
- **Network**: WiFi 192.168.0.x, machine 192.168.0.72

## On-Device LLM

- **ChatterUI** — APK install via `adb install`, package: `com.Vali98.ChatterUI`
- **llama.cpp** — ARM64 binary from GitHub releases, push to `/data/local/tmp/llama/`
- **SmolLM2 135M** — ~100MB, 28 t/s generation on Note 8
- **Model loading**: ~60-90s on Note 8 (slow flash storage)

## Termux

- **ADB เข้า Termux ไม่ได้**: คนละ UID, `run-as` ใช้ไม่ได้ (ไม่ใช่ debug build), `su` โดน Termux block
- **พิมพ์ผ่าน ADB**: `adb shell input text` + `adb shell input keyevent 62` (space) + `keyevent 66` (enter)
- **ต้อง reconnect ก่อน**: `adb reconnect` แล้วค่อย `input text`

**Why:** Don't repeat device farm mistakes
**How to apply:** Check this before working with devices
