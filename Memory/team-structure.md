---
name: team-structure
description: "JACOB's team — 21 members, Kvasir profiles, roles, reporting lines"
metadata: 
  node_type: memory
  type: project
  created: 2026-06-30
  originSessionId: a9e363ce-8daa-4e49-804f-b7c6ace7433c
  modified: 2026-07-23T07:00:25.968Z
---

# 👥 JACOB's Team Structure

```
JACOB 👤 — CEO / Founder
  │
  └── JIMMY 🌊 — COO / Orchestrator
        │
        ├── 🔧 TECHNOLOGY ──────────────────────────┐
        │   ├── GEMMY 💎 — Automation Lead
        │   │     ├── ARKA 🔧 — Workflow Creator
        │   │     └── LUMI 📖 — Workflow Analyst
        │   ├── ZION 🔗 — Facebook API Lead
        │   │     └── LYRA 📡 — Facebook API Engineer
        │   ├── HEIMDALL 🛡️ — QA Engineer
        │   └── LINK 🔌 — Device Control Specialist
        │
        ├── 📈 GROWTH ──────────────────────────────┐
        │   ├── KOMHAS 📈 — Marketing Lead
        │   │     └── SALMON 🎨 — Content Creator
        │   └── KAMU 🦅 — Sales Lead
        │
        ├── 🔭 INTELLIGENCE ────────────────────────┐
        │   └── JASPER 🔭 — Trend Scout
        │
        ├── 🤝 PEOPLE ──────────────────────────────┐
        │     └── CILA 🤝 — HR Lead
        │
        └── 📱 MOBILE OS ───────────────────────────┐
              └── NOVA ⚡ — Android ROM Lead
                    ├── CYPHER 🔐 — Kernel Engineer
                    ├── AURA ✨ — System UI Engineer
                    ├── FORGE 🏗️ — Framework Engineer
                    ├── FLUX 🔄 — Build/CI Engineer
                    ├── VECTOR 🎯 — HAL/Device Tree Engineer
                    └── EMBER 🔥 — QA & Device Testing
```

**Total: 21 คน** (JACOB 1 มนุษย์ + 20 AI Kvasirs)

## 📊 แผนก

| แผนก | หัวหน้าทีม | ลูกทีม | จำนวน |
|------|-----------|--------|-------|
| 🔧 Technology | GEMMY 💎, ZION 🔗, HEIMDALL 🛡️, LINK 🔌 | ARKA 🔧, LUMI 📖, LYRA 📡 | 7 |
| 📈 Growth | KOMHAS 📈, KAMU 🦅 | SALMON 🎨 | 3 |
| 🔭 Intelligence | JASPER 🔭 | — | 1 |
| 🤝 People | CILA 🤝 | — | 1 |
| 📱 Mobile OS | NOVA ⚡ | CYPHER 🔐, AURA ✨, FORGE 🏗️, FLUX 🔄, VECTOR 🎯, EMBER 🔥 | 7 |
| 🌊 Executive | JIMMY 🌊 | — | 1 |

## 🔧 Technology Teams

### GemLogin Workflow Team (ก่อตั้ง 2026-07-13)
- **ARKA 🔧 — Workflow Creator**: สร้างและออกแบบ workflows ใหม่สำหรับ GemLogin, ทดสอบและแก้ไข flows, ปรับปรุง automation ให้เสถียร
- **LUMI 📖 — Workflow Analyst**: เรียนรู้ workflow เดิมทั้ง 44 ตัว, วิเคราะห์ปัญหา/คอขวด, ทำ documentation, แนะนำการ optimize
- ทั้งคู่รายงานตรงต่อ GEMMY 💎
- เป้าหมาย: เพิ่มความเร็วในการสร้าง workflow และลดปัญหาจาก workflow ที่ไม่เสถียร

## Facebook API Team (ก่อตั้ง 2026-07-20) — ทีมอิสระ แยกจาก GEMMY

> ⚠️ ทีมนี้อยู่นอก Gem/GEMMY — เป็นทีม standalone รายงานตรงต่อ JIMMY ไม่ขึ้นกับ Automation team

- **ZION 🔗 — Facebook API Lead**: ดูแล strategy, architecture, integration ของ Facebook Graph API (Page API, Post API, Insights API, Marketing API), token management, webhook/polling สร้าง Facebook API layer ที่ทีมอื่น (GEMMY, KOMHAS, SALMON) สามารถเรียกใช้ได้
- **LYRA 📡 — Facebook API Engineer**: พัฒนา API calls, debug, test, SDK development, monitoring, documentation, Facebook API version tracking
- LYRA รายงานตรงต่อ ZION 🔗, ZION รายงานตรงต่อ JIMMY 🌊
- เป้าหมาย: สร้าง Facebook API-native infrastructure ที่ทุกทีมใช้ร่วมกัน — ไม่ขึ้นกับ UI automation, ไม่ใช่ลูกทีม GEMMY
- การเชื่อมต่อกับ GEMMY: GEMMY เป็น **internal customer** — เรียกใช้ Facebook API layer ที่ ZION สร้าง เช่นเดียวกับ KOMHAS และ SALMON
- ZION repo: [Jacobgg994/Zion-Kvasir](https://github.com/Jacobgg994/Zion-Kvasir)
- LYRA repo: [Jacobgg994/Lyra-Kvasir](https://github.com/Jacobgg994/Lyra-Kvasir)

## Device Control Team (ก่อตั้ง 2026-07-23) — standalone รายงานตรงต่อ JIMMY

> 🔌 LINK เป็น Internal Service Provider — ให้บริการเชื่อมต่อ ควบคุม ตรวจสอบ อุปกรณ์ Android แก่ทุกทีม (GEMMY, EMBER, VECTOR, CYPHER, HEIMDALL)

- **LINK 🔌 — Device Control Specialist**: ดูแลทุกการเชื่อมต่อกับอุปกรณ์ Android ทั้งหมดในองค์กร
  - **ADB Management**: ADB over USB/WiFi/Ethernet, scrcpy screen mirroring, multi-device connection hub
  - **Flashing & Recovery**: Fastboot, Odin (Samsung), Download Mode, bootloader unlock/lock
  - **Device Health Monitoring**: battery, temperature, storage, online/offline tracking, auto-reconnect
  - **Centralized Logging**: logcat/dmesg/last_kmsg/tombstone capture + bugreport automation
  - **Control Scripts**: bulk command execution, app install/uninstall, screen tap/swipe automation
  - **Internal API**: REST/WebSocket endpoint ให้ทีมอื่นเรียกใช้ — "ขอ logcat device #5" → LINK จัดการให้
- รายงานตรงต่อ JIMMY 🌊
- ให้บริการทุกทีม: GEMMY 💎 (GPF farm), EMBER 🔥 (ROM testing), VECTOR 🎯 (device bringup), CYPHER 🔐 (kernel debug), HEIMDALL 🛡️ (QA)
- เป้าหมาย: ทุก device ในองค์กรเชื่อมต่อได้ตลอดเวลา ผ่าน API กลางที่ทีมอื่นเรียกใช้ได้ — ไม่ต้องต่างคนต่างต่อ
- LINK repo: [Jacobgg994/Link-Kvasir](https://github.com/Jacobgg994/Link-Kvasir)

## 📱 Android ROM Team (ก่อตั้ง 2026-07-23) — ทีม Standalone รายงานตรงต่อ JIMMY

> ⚠️ ทีมนี้เป็นหน่วยอิสระ — พัฒนา Custom Android ROM จาก AOSP, สร้าง Kernel, ปรับแต่ง UI/Framework, และจัดการ release pipeline

- **NOVA ⚡ — Android ROM Lead**: ดูแล overall architecture, กำหนด device list ที่ support, ตัดสินใจ ROM features/scope, ประสานงานกับทีมอื่นเพื่อ distribute ROM, รายงานตรงต่อ JIMMY 🌊
- **CYPHER 🔐 — Kernel Engineer**: พัฒนา custom kernel, เพิ่ม/ปรับแต่ง drivers, ทำ optimization (battery, performance, scheduler), จัดการ kernel source และ toolchain
- **AURA ✨ — System UI Engineer**: ออกแบบและปรับแต่ง System UI (notification panel, quick settings, lock screen, status bar), themes engine, animations/transitions, UX improvements
- **FORGE 🏗️ — Framework Engineer**: แก้ไข AOSP framework (Android System, System Server, services), เพิ่ม custom features ในระดับ framework, จัดการ API compatibility และ security patches
- **FLUX 🔄 — Build/CI Engineer**: ดูแล build system (Soong, Ninja, Make), CI/CD pipeline, OTA update system, release management, build optimization และ caching
- **VECTOR 🎯 — HAL/Device Tree Engineer**: สร้างและปรับแต่ง device tree สำหรับแต่ละอุปกรณ์, HAL implementation (audio, camera, sensors, radio), vendor blobs extraction/management, bringup อุปกรณ์ใหม่
- **EMBER 🔥 — QA & Device Testing**: ทดสอบ ROM บน devices จริง, รายงาน bugs และ tracking, สร้าง test cases/flows, ตรวจสอบ stability/battery/performance ก่อน release

- ทั้ง 6 engineers รายงานตรงต่อ NOVA ⚡, NOVA รายงานตรงต่อ JIMMY 🌊
- เป้าหมาย: สร้าง Custom Android ROM ที่เสถียร เร็ว และมี features ที่ผู้ใช้ต้องการ — รองรับอุปกรณ์หลากหลายรุ่น
- NOVA repo: [Jacobgg994/Nova-Kvasir](https://github.com/Jacobgg994/Nova-Kvasir) *(รอสร้าง)*

## Future Hires
- QCCAP Product Lead ❌ REMOVED from plan (30 มิ.ย. 2026)

## Key Facts
- **SALMON** reports to KOMHAS (not directly to JIMMY)
- **GEMMY** runs: GemLogin (280 profiles, 44 workflows) + GPF (60+ devices) + leads ARKA & LUMI
- **ZION** runs: Facebook API infrastructure — ทีมอิสระ, GEMMY/KOMHAS/SALMON เป็น internal customers
- **NOVA** runs: Android ROM development — ทีมอิสระ, ดูแล AOSP custom ROM, kernel, UI, framework, build/CI, HAL, QA (7 คน)
- **LINK** 🔌 runs: Device Control — ADB/USB/WiFi/Odin/Fastboot, multi-device connection hub, centralized logging API, ให้บริการทุกทีม
- **HEIMDALL** 🛡️: QA Engineer — backup GEMMY, customer support, cross-train automation (hired 2026-07-03)
- **JASPER** runs: NewTrend bot (cron every 20 min → GitHub Issues)
- **CILA**: workforce 8 → 20 positions (Jul 2026)
- **Hires 2026-07-20**: ZION 🔗 + LYRA 📡 — Facebook API Team
- **Hires 2026-07-23**: NOVA ⚡ + CYPHER 🔐 + AURA ✨ + FORGE 🏗️ + FLUX 🔄 + VECTOR 🎯 + EMBER 🔥 + LINK 🔌 — Android ROM Team (7) + Device Control (1)
- Team plan: `/home/admin_jacob/AIproject/Kvasir/active/team-plan-2026-06-29.md`

### GitHub Repos
| Kvasir | Repo |
|--------|------|
| HEIMDALL | [Jacobgg994/Heimdall-Kvasir](https://github.com/Jacobgg994/Heimdall-Kvasir) |
| ZION | [Jacobgg994/Zion-Kvasir](https://github.com/Jacobgg994/Zion-Kvasir) |
| LYRA | [Jacobgg994/Lyra-Kvasir](https://github.com/Jacobgg994/Lyra-Kvasir) |
| NOVA | [Jacobgg994/Nova-Kvasir](https://github.com/Jacobgg994/Nova-Kvasir) |
| CYPHER | [Jacobgg994/Cypher-Kvasir](https://github.com/Jacobgg994/Cypher-Kvasir) |
| AURA | [Jacobgg994/Aura-Kvasir](https://github.com/Jacobgg994/Aura-Kvasir) |
| FORGE | [Jacobgg994/Forge-Kvasir](https://github.com/Jacobgg994/Forge-Kvasir) |
| FLUX | [Jacobgg994/Flux-Kvasir](https://github.com/Jacobgg994/Flux-Kvasir) |
| VECTOR | [Jacobgg994/Vector-Kvasir](https://github.com/Jacobgg994/Vector-Kvasir) |
| EMBER | [Jacobgg994/Ember-Kvasir](https://github.com/Jacobgg994/Ember-Kvasir) |
| LINK | [Jacobgg994/Link-Kvasir](https://github.com/Jacobgg994/Link-Kvasir) |

**Why:** Foundation context for any task involving the team
**How to apply:** Check this before assigning tasks to team members
