# PULSE Learning Plan: GemphoneFarm Comprehensive Knowledge

> **ผู้เรียน**: PULSE 📳 — Phone Automation Specialist
> **วันที่**: 2026-07-01
> **แหล่งความรู้**: Block Catalog, Execution Model, MCP Server, Reference Learning (89 workflows), Source Code Analysis, Boxphone Thai Growth Skill, Phone Farm Ops, 90-Day Plan, Phone Onboarding SOP

---

## สารบัญ

1. [GemphoneFarm คืออะไร](#1-gemphonefarm-คืออะไร)
2. [Block Catalog](#2-block-catalog)
3. [Execution Model](#3-execution-model)
4. [MCP Server](#4-mcp-server)
5. [Workflow Patterns](#5-workflow-patterns)
6. [Source Code Architecture](#6-source-code-architecture)
7. [Operations](#7-operations)
8. [Critical Rules](#8-critical-rules)
9. [90-Day Learning Path](#9-90-day-learning-path)

---

## 1. GemphoneFarm คืออะไร

### 1.1 ภาพรวม

GemphoneFarm เป็น platform สำหรับ **Android Automation** แบบ visual workflow editor ที่ใช้ควบคุมสมาร์ทโฟน Android จำนวนมากจากเครื่องเดียว สร้างด้วย **Electron + Vue 3** โดยมี backend เป็น Node.js Express server

**ชื่อเต็ม**: GemphoneFarm (สะกดแบบนี้เสมอ)
**Extension ไฟล์ workflow**: `.GemPhoneFarm` (ตัว G, P, F พิมพ์ใหญ่ ห้ามใช้ `.json` หรือ `.GemPhoneFarm.json`)
**API Port**: `:1256`
**Current Version**: v3.0.8
**Total LOC**: ~25,000 (backend 15k, frontend 10k)

### 1.2 สถาปัตยกรรมรวม

```
┌─────────────────────────────────────────────────────┐
│                  GemphoneFarm App                     │
│  ┌───────────────────────┐  ┌─────────────────────┐  │
│  │   Backend (Electron)   │  │   Frontend (Vue 3)  │  │
│  │   - Express API :1256  │  │   - Vue Flow Editor │  │
│  │   - ADB Server         │  │   - Device Dashboard│  │
│  │   - SQLite Database    │  │   - Inspector Tool  │  │
│  │   - Workflow Engine    │  │   - Account Manager  │  │
│  └───────────┬───────────┘  └──────────┬──────────┘  │
│              │                         │              │
│              └──────────┬──────────────┘              │
│                         │ IPC                          │
└─────────────────────────┼─────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │ Phone 1 │      │ Phone 2 │      │ Phone N │
   │ :7912   │      │ :7912   │      │ :7912   │
   │ atx-agent│     │ atx-agent│     │ atx-agent│
   └─────────┘      └─────────┘      └─────────┘
```

### 1.3 ระบบ 60+ เครื่องที่ใช้งานจริง

- **60 devices**: ส่วนใหญ่ Samsung Note 8 (N950F/N) + Samsung S7 (G930F)
- **3 Groups**: TH (id 2), VN (id 1), US (id 3)
- **Online ปกติ**: 55+ devices
- **การใช้งานหลัก**: TikTok Shop Affiliate, Shopee/Lazada Affiliate, LINE OA, CDS Content

---

## 2. Block Catalog

### 2.1 ภาพรวม 9 หมวดหมู่ (~70 blocks)

| หมวดหมู่ | Blocks |
|----------|--------|
| **General** | Start, End, Resource Status, Delay, HTTP Request, Block Group, Note |
| **UI Interaction** | Press Back, Press Home, Press Menu, Touch, Swipe/Scroll, Screenshot, Type Text, Image Search, Swipe & Check Screen, Clear Text, Find Text |
| **Device Management** | Set Clipboard, Get Clipboard, Reconnect, Transfer File, Screen Action, Toggle Service, Change Device, Get Property Device, Check Network, Dump XML, Proxy |
| **App Management** | Is Open App, Start App, Stop App, Install App, Uninstall App, Is Installed App, Backup/Restore, Backup/Restore Device, Clear Data App, Close All App |
| **System Commands** | JavaScript code, Element exists, Press Key, ADB Command |
| **Data** | Read file text, Insert data, Delete data, Get log data, Slice variable, Increase variable, RegEx variable, Data mapping, Split Data, Sort data, Get Attribute, Random, IMAP (Read Mail), Read Hotmail, Refresh Hotmail AccessToken, File Action, Generate 2FA |
| **Online Services** | Excel, Google Sheets, Gemini AI, Chat GPT, DeepSeek, BlackBox AI |
| **Control Flow** | Repeat Task, Conditions, While Loop, Loop Data, Loop Breakpoint |

### 2.2 Block สำคัญและ Semantic โดยละเอียด

#### Start (Trigger)
- โหมด Manual: กด ▶️ ที่ node โดยตรง — **เส้นทางที่น่าเชื่อถือที่สุด** เพราะ bypass IPC ทั้งหมด
- โหมด Interval: ทำงานทุก N วินาที (มี initial delay)
- โหมด Date: ทำงานครั้งเดียวตาม timestamp
- โหมด Context menu: ลงทะเบียนเป็น right-click target
- **CRITICAL**: schema ต้องซ้ำกันที่ TWO places ใน JSON:
  - `drawflow.nodes[0].data` (เมื่อ node แรกมี label: "trigger")
  - `workflow.trigger` (root) — **REQUIRED** ถ้า root เป็น null จะล้มเหลวทันที

#### Conditions
- Type prefixes: `string::`, `json::`, `number::`, `boolean::`
- Operators: Equal (case-sens/insens), Not equal, >, >=, <, <=, Contains (sens/insens), Not contains, Starts with, Ends with, Match with RegEx, Is truthy, Is falsy
- Combine groups: And/Or
- Output handles: `output-<group_id>` (match) และ `output-fallback` (else)
- การทำงาน: two-stage evaluation (XML cache + reuse)

#### JavaScript Code
- **ทำงานบน Browser runtime** (ไม่ใช่บน phone)
- Helpers: `NextBlock()` (continue), `RefData(source, path)` (read), `SetVariable(name, value)` (write)
- **GemLogin's "no IIFE" rule ไม่เกี่ยวข้อง** เพราะเป็น invocation context คนละแบบ
- Cookie/HTTP state แยกจาก phone โดยสิ้นเชิง

#### Touch
- Match: XPath OR coordinates
- Tap type: Normal / Double / Long press
- Delay: `"1500"` (fixed ms) หรือ `"800,1500"` (random range)
- **Selector Hierarchy ที่ใช้ในการผลิต**: @content-desc, @text, resource IDs (99% hit) → XPath substring, position-based, image OCR (70% hit fallback)
- **ห้ามใช้ hardcoded coordinates** เพราะพังทันทีเมื่อ device หมุน

#### Repeat Task
- Connect output 2 กลับไปยัง node ก่อนหน้าเพื่อ loop
- Count ตั้งที่ block
- `repeatFor: "<n>"` (string-typed integer)

#### Inspector Tool
- UI feature (ไม่ใช่ block)
- Extract XPath / Id / Name / ClassName / package
- Capabilities: search-for-element, screenshot download, tap-by-coords, swipe-by-coords, reload
- **เป็น authoring loop ที่ load-bearing ที่สุด** — ถ้าไม่มี Inspector การเขียน selectors ด้วยมือแทบเป็นไปไม่ได้

#### IMAP / Hotmail
- Token-based auth (refresh-token → access-token flow)
- IMAP filters: sender/recipient/subject/body/time-window
- Regex extract: capture groups เข้า variables
- ใช้ **Generate 2FA** block สำหรับ TOTP จาก shared secret

### 2.3 Block Distribution จาก 89 Production Workflows (3,803 blocks)

| Block Type | จำนวน | สัดส่วน |
|------------|-------|---------|
| touch | 1,057 | 27.8% |
| delay | 340 | 8.9% |
| image-search | 219 | 5.8% |
| BlockBasicWithFallback | 2,829 | 74.4% (device/element interaction ทั้งหมด) |
| BlockConditions | 268 | 7.0% |
| BlockRepeatTask | 93 | 2.4% |

---

## 3. Execution Model

### 3.1 Dual-Runtime Architecture

นี่คือ concept ที่สำคัญที่สุดในการทำความเข้าใจ GemphoneFarm — มันคือ automation engine **สองตัว** ที่ทำงานพร้อมกันใน Electron renderer คนละตัว:

| Engine | ทำงานบน | Block Families |
|--------|---------|----------------|
| **Phone Runtime** | Android device UI (via atx-agent :7912) | Touch, Swipe/Scroll, Type Text, Screenshot, Press Back/Home/Menu/Key, App Management, Clear Text, Find Text/OCR, Image Search, Inspector, Element Exists, Dump XML, Get Attribute, ADB Command |
| **Browser Runtime** | Hidden BrowserWindow ต่อ profile | HTTP Request, JavaScript Code, Read Hotmail, IMAP, Online Services (ChatGPT, Gemini AI, DeepSeek, BlackBox AI), Excel, Google Sheets |

**นัยยะที่สำคัญ:**
- JS Code block "runs in the active tab" — เป็น browser tab **ไม่ใช่** JS บน phone
- `settings.executedBlockOnWeb` (boolean ใน workflow root) เป็นตัวบ่งชี้ว่า runtime ไหนทำงาน workflow นี้
- Hotmail/IMAP blocks มีไว้สำหรับ email verification — รันบน browser โดยไม่ต้องแตะ phone
- Generate 2FA (TOTP) กับ Touch อยู่ด้วยกันใน workflow เดียวกันได้ — prep credentials ใน browser แล้วขับ app login บน phone

**Debugging First Question**: "block นี้ต้องการ runtime ไหน?"
- ถ้า phone → verify atx-agent
- ถ้า browser → verify BrowserWindow context

### 3.2 Variables vs Tables

| | Variables | Tables |
|--|-----------|--------|
| **Type** | scalar / JSON | column-oriented, multi-row |
| **Persist** | transient ต่อ workflow run | persistent ข้าม runs |
| **Template** | `{{variables.X}}` | `{{tables.<name>.<col>}}` |
| **Use case** | intermediate computations, counters | account lists, logged outcomes |

**ทำไมต้องมีทั้งสองแบบ**: งาน farming เป็น relational workload — มี list ของ accounts, results ที่ต้องบันทึก, retry candidates ที่ต้อง track

- Variables: per-step micro-state
- Tables: macro-state ข้าม campaign
- Loop Data over a table → iterate หนึ่ง row ต่อรอบ
- Import จาก Google Sheets / Excel → ใช้ table primitive โดยอัตโนมัติ: `{{googleSheets.<refKey>.0.<col>}}`

### 3.3 Implicit Profile Context

ในทุก block field ที่รับ template expression มี context ต่อไปนี้เสมอ:
- `profileId` / `profileName` — account/identity row ที่ active อยู่
- `deviceId` — ADB serial (string), runtime injection โดย `WorkflowWorker.js:237`
- `globalData` — installation-wide globals (license, settings, account pool)

**นี่คือสาเหตุที่** workflow JSON ไม่มี hardcoded device serials — runtime injection

### 3.4 Resource Status — Farm-as-CRM Idiom

Resource Status block (General category) ทำสองอย่าง:
1. **Update status** ของ profile/resource row: `Active` / `Inactive` / `Invalid` / `Unknown`
2. **Update data** fields (name, email, phone, avatar)

**นี่คือ primitive ที่รับน้ำหนักมากที่สุดของ farming lifecycle**:
- workflow จบด้วยการ mark row เป็น Invalid (login failed), Active (working), หรือ Inactive (rate-limited)
- runs ถัดไป filter โดย status เพื่อ skip dead accounts และ resume failed ones
- **Workflow ที่ไม่มี Resource Status calls = workflow ที่ไม่มี operational memory ข้าม runs**

### 3.5 Block Group เป็นแค่ organizational

ไม่มี variable scoping, ไม่มี execution barrier, ไม่มี error containment แค่ collapse/expand-region sugar

### 3.6 Trigger Modes Encode Dispatch Policy

**Local**: Manual ▶️ (bypass IPC ทั้งหมด → น่าเชื่อถือที่สุด), Interval, Date, Context menu

**Cloud**: `POST /api/v2/startAutomation` → MQTT → `App.vue:667` `onExecuteWorkflow` listener → `executeWorkflow()`

**Broken path**: `POST /api/scripts/execute/:id` — `main.js:980` เรียก `startServer()` โดยไม่ส่ง `mainWindow` → `mainWindow.webContents.send(...)` crash

### 3.7 atx-agent Dependency Chain

ทุก phone-runtime block HTTP ไปที่ `http://127.0.0.1:<forwarded-port>/...` → forward ไปที่ `tcp:7912` บน device → atx-agent (Go daemon) → uiautomator (com.github.uiautomator + .test)

**Bug สำคัญ**: `startAtxAgent()` ใน `checkAppStart.js:209` ตรวจสอบ success ด้วย `result.includes('background') || result.includes(':7912')` แต่ Go logs ไป stderr ขณะที่ `runShellCommandAdb` capture stdout → ตลอดไปไม่เจอ → หลังจาก 10 retries (27.5s) → return `'Failed after max attempts'`

**Workaround**: `bash /Users/ccdev/QCCAP-FARM/scripts/start-atx-agent.sh` หลัง reconnect phone หรือ relaunch GemphoneFarm

### 3.8 The Inspector Authoring Loop

1. Connect phone → enter device-screen view
2. Open Inspector → dump UI tree
3. Click node → copy XPath / Id / Name / ClassName
4. Paste ลงใน Touch / Element Exists / Find Text block
5. Repeat สำหรับแต่ละ step
6. กด ▶️ ที่ Start node เพื่อ test

---

## 4. MCP Server

### 4.1 ภาพรวม

**gemphonefarm-mcp** v0.1.0 — Python package, pipx-installable, MCP server 12 tools

| | |
|---|---|
| Source on disk | `/Users/ccdev/gemphonefarm-mcp/` |
| Git remote | `https://forgejo.contentsdigital.us/ccdev/gemphonefarm-mcp.git` |
| License | MIT |

### 4.2 การติดตั้ง

```bash
pipx install git+https://forgejo.contentsdigital.us/ccdev/gemphonefarm-mcp.git
claude mcp add gemphonefarm /Users/ccdev/.local/bin/gemphonefarm-mcp --scope user
```

### 4.3 12 Tools

**Device Management (4)**
1. `gemphonefarm_list_devices` — device ทั้งหมด (id, name, ADB serial, status, isCloud, isOtg)
2. `gemphonefarm_devices_by_group` — filter ตาม group
3. `gemphonefarm_start_device` — **LOCAL API** (ดู warning ด้านล่าง)
4. `gemphonefarm_close_device`

**Groups (3)**
5. `gemphonefarm_list_groups`
6. `gemphonefarm_create_group`
7. `gemphonefarm_assign_device_to_group`

**Scripts (4)**
8. `gemphonefarm_list_scripts`
9. `gemphonefarm_execute_script` — **LOCAL API** (ดู warning ด้านล่าง)
10. `gemphonefarm_check_script_status`
11. `gemphonefarm_kill_script`

**Cloud Webhook (1)**
12. `gemphonefarm_cloud_start_automation` — **เส้นทางเดียวที่เชื่อถือได้สำหรับ remote dispatch**

### 4.4 Known Limitation — Local API Down

`POST /api/scripts/execute/:id` และ endpoints device-runtime อื่นๆ dispatch ผ่าน IPC `scriptAction` / `deviceAction` แต่ `main.js:980` เรียก `startServer()` โดยไม่ส่ง renderer's mainWindow → `mainWindow.webContents.send(...)` throw → timeout 5s

**เส้นทางที่ใช้งานได้จริงมีแค่:**
- UI ▶️ play button บน Start node
- `gemphonefarm_cloud_start_automation` (cloud → MQTT → working renderer listener)

### 4.5 Cloud Webhook Setup

ต้องการ environment variables:
- `GEMPHONEFARM_CLOUD_TOKEN`
- `GEMPHONEFARM_DEVICE_ID`
- `GEMPHONEFARM_SOFT_ID`

### 4.6 MCP Tools in Boxphone Skill (prefix `mcp__gemphonefarm__`)

ใช้ใน Claude Code ผ่าน skill boxphone-thai-growth:
- `mcp__gemphonefarm__gemphonefarm_list_devices` — เรียกเป็นอันดับแรกเสมอเพื่อตรวจ fleet state
- `mcp__gemphonefarm__gemphonefarm_cloud_start_automation` — fallback เมื่อ local API down

---

## 5. Workflow Patterns

### 5.1 ภาพรวมจาก 89 Production Workflows

**Source corpus**: `/Users/ccdev/Downloads/Gemphonefarm/` (99 files, 89 production workflows)
**ทีมผู้เขียน**: 6 Thai team folders (Jacob, Boom, Jed, PAT, Boss, Paji)
**34 workflow types**: TikTok, FB, Instagram, Twitter, Shopee, YouTube, Lemon8, LINE

### 5.2 Platform Coverage

| Platform | Variants | การใช้งานหลัก |
|----------|----------|---------------|
| **TikTok** | 21 | auto-like, comment, engagement, affiliate post |
| **Facebook** | 14 | login, farming, posting, warm-up |
| **Instagram** | 11 | engagement, stories |
| **Twitter/X** | 11 | retweet, like, follow |
| **Shopee** | ~5-8 | browse, add-to-cart, affiliate |
| **YouTube** | ~3-5 | watch, subscribe, comment |
| **Lemon8, LINE** | ~3-5 | niche automation |

### 5.3 Timing Strategy (Human-Like Behavior)

| Input Type | Speed | เหตุผล |
|------------|-------|--------|
| Email | 10–50 ms/char | Slow, observable |
| Password | 50–130 ms/char | Realistic variability |
| 2FA | 0 ms | Instant injection |
| Login delay | 4.5s + random variance | เลียนแบบมนุษย์ |

**หลักการ**: ทุก delay มี ±20–30% randomization เพื่อ defeat detection

### 5.4 Selector Hierarchy

```
Primary (@content-desc, @text, resource IDs) → 99% hit rate
    ↓ (เมื่อ primary ล้มเหลว)
XPath substring, position-based, image OCR → ~70% hit rate
```

**Absolute Rule**: Never use hardcoded coordinates — breaks on rotation
**Condition retry**: 10 attempts ต่อ selector, 1s interval
**Fallback edges**: Primary + fallback path ทุก block

### 5.5 Authentication Patterns

| Pattern | Nodes | วิธี |
|---------|-------|------|
| Simple | 8–10 nodes | email + password + submit |
| 2FA | 20–30 nodes | credentials + TOTP generation + code injection |
| Checkpoint | 13+ branches | detection → screenshot → recovery |

**TOTP**: Base32 secret → HMAC-SHA1 → 6-digit code (30s window)
**Warning**: timing drift >30s = invalid code

### 5.6 Error Resilience Pattern

- Condition retry: 10 attempts per selector, 1s interval
- Fallback edges: ทุก block มี primary + fallback path
- Screenshot verification: state validation ก่อน transition
- Loop breakpoints: escape infinite loops (50-iteration limit)
- **ต่อ block มี BlockBasicWithFallback** — design pattern หลัก

### 5.7 Deployment Model

- 1:1 device ↔ proxy ↔ account mapping
- Stagger launches: 8–10s เพื่อ avoid batch detection
- Screenshot verification: proof-of-work ก่อน next action
- Session duration: 10–30 min ต่อ workflow
- Success rate: 85–95% (varies by platform)

### 5.8 Production Gotchas (Hard-Learned)

| Gotcha | ผลกระทบ |
|--------|---------|
| IIFE wrappers ใน JS blocks | Handler crash |
| `random()` ใน delay fields | Fails to evaluate |
| Condition edges ต้องการ exact ID matching (`output-<group_id>`) | Edge fails silently |
| Hardcoded coordinates | พังเมื่อ rotation |
| TOTP timing drift >30s | Invalid code |
| Workflow.trigger ไม่ได้ replicate ที่ root | Block แรกไม่ทำงาน |

---

## 6. Source Code Architecture

### 6.1 Dual-Layer Design

```
┌─────────────────────────────────────────────────────────┐
│                    GemphoneFarm v3.0.8                   │
│                                                         │
│  ┌───────────────────────┐  ┌─────────────────────────┐ │
│  │  Backend (Electron)    │  │  Frontend (Vue 3+Vite)  │ │
│  │  ~15,000 LOC           │  │  ~10,000 LOC            │ │
│  │                       │  │                         │ │
│  │  main.js — bootstrap  │  │  App.vue — root         │ │
│  │  expressServer.js     │  │  Workflow.vue — editor  │ │
│  │  adbFunctions.js (88K)│  │  Device.vue — dashboard │ │
│  │  handlerBlock.js      │  │  Account.vue — manager  │ │
│  │  models/ (SQLite)     │  │  stores/ — Pinia        │ │
│  │  handlerConditions.js │  │  utils/api.js — client  │ │
│  └───────────┬───────────┘  └──────────┬──────────────┘ │
│              │                         │                 │
│              └──────────┬──────────────┘                 │
│                         │ IPC                             │
└─────────────────────────┼────────────────────────────────┘
                          │
                    ┌─────▼─────┐
                    │ :1256 API  │
                    │ Express.js │
                    └─────┬─────┘
                          │
              ┌───────────┼────────────┐
              │           │            │
         ┌────▼───┐ ┌────▼───┐ ┌────▼───┐
         │Phone 1 │ │Phone 2 │ │Phone N │
         │atx-agnt│ │atx-agnt│ │atx-agnt│
         └────────┘ └────────┘ └────────┘
```

### 6.2 Backend Core Components

#### main.js — Electron Bootstrap (Priority #1)
- สร้าง Electron main process + BrowserWindow
- เรียก `startServer()` (แต่ BUG: ไม่ส่ง mainWindow → IPC crash)
- IPC channels สำหรับ backend-frontend communication

#### expressServer.js — REST API 40+ Endpoints
- Port **1256**
- Routes: Device Management, Device Control, Account Management, Workflow Execution, App Management, Cloud Integration
- **Error responses เป็นภาษาเวียดนาม**

#### adbFunctions.js — Core ADB (88KB, 70+ Operations)
- Promise-wrapped callbacks (never rejects)
- Polling retry loops (1s intervals) with timeout
- Concurrency: p-limit max 40 concurrent ops
- 70+ operations: screen capture, tap, swipe, app control, file transfer
- Cloud fork: adbFunctionsCloud.js (52KB)

#### handlerBlock.js — Block Dispatcher
- 80+ block types
- Single dispatcher: `handleBlock(device_id, data, port, isCloud)`
- Block routing by type string
- Web Worker สำหรับ async isolation

#### handlerConditions.js — Condition Evaluation
- Two-stage: XML cache + reuse
- XPath support via xmldom library

#### SQLite Database — ผ่าน Sequelize ORM
- Models: Device, Account, Scripts, Groups, AccountGroups
- File storage: Workflows (JSON), Accounts (CSV/JSON), Screenshots
- Variable extraction via regex with flags

#### email.js — IMAP Multi-Service
- Gmail, Outlook, Yahoo, custom IMAP
- Regex extraction from email subjects/body
- Configurable flags (case-insensitive, global)
- Variable injection into workflows

### 6.3 Frontend Core Components

#### Vue Flow Editor (Workflow.vue)
- Drag-and-drop visual workflow designer
- Node types map to block types
- Edge routing สำหรับ control flow

#### Device.vue — Dashboard
- Real-time device status
- Resource Status visualization
- Screen capture preview

#### Inspector Tool
- UI tree dump
- XPath/ID extraction
- Coordinate tap/swipe

### 6.4 Concurrency & Performance

| Metric | Value |
|--------|-------|
| Max concurrent ADB ops | 40 (p-limit) |
| Sequential device control | No parallel taps |
| Parallel screen capture | 3 requests |
| Script execution timeout | 5s |
| Device connection retry | 60 attempts (1s intervals) |
| Device ports range | 50000+ |

### 6.5 Cloud Integration

- Device ID format: JSON `{ order_id, phone_id }`
- Endpoints: VN vs Global (conditional)
- Bearer token authentication
- WebRTC สำหรับ real-time video streaming
- Caching: Request metadata, cache token + URL

### 6.6 Security (Current State)

| Aspect | สถานะปัจจุบัน | ควรปรับปรุง |
|--------|---------------|-------------|
| Cloud auth | Bearer token | OK for now |
| Local API | No JWT | Add JWT + rate limiting |
| Credentials | Plaintext in SQLite | Add encryption |
| IPC | Trust (Electron same-process) | Acceptable for desktop |

### 6.7 Extensibility Patterns

**Adding Block Types:**
1. Define schema in frontend
2. Add handler ใน `handlerBlock.js`
3. Register in action map
4. Test locally

**Adding Platforms:**
1. Update `defaultPlatform.js`
2. Create UI selectors
3. Implement account CRUD
4. Wire into block dispatcher

---

## 7. Operations

### 7.1 Fleet Snapshot (ปรับปรุง 2026-05-21)

| Bucket | จำนวน | Notes |
|--------|-------|-------|
| Total devices | 60 | Samsung Note 8 (N950F/N), S7 (G930F), A15/A16, A55/A56 |
| Online | 58 | Default healthy state |
| Offline | ~2 | ต้อง reboot/re-pair |
| Group TH (id 2) | 4 | Hong Kong residential proxy |
| Group VN (id 1) | 4 | Singapore residential proxy |
| Group US (id 3) | 4 | US residential proxy |
| Ungrouped | 48 | **ต้อง fix — no proxy assigned** |

### 7.2 Hardware Roles

| Model | Best Role | Why |
|-------|-----------|-----|
| Samsung Note 8 (Android 9) | Mid-tier posting + warming | Bulk of fleet, reliable |
| Samsung S7 (rooted) | Engagement farm + LINE | Cheap, expendable |
| Samsung A15/A16 5G | Tier-1 TikTok posting | Fresh fingerprint = better reach |
| Samsung A55/A56 | Buyer farm | Premium fingerprint |
| Pixel 6a/7a | Dev/sensitive accounts | Cleanest Android |
| iPhone XR/11 | iOS slice; LINE TH | 60% TH LINE traffic is iOS |
| Redroid emulators | Warming + scrape | Free hardware on 210.1.1.155 |

### 7.3 Phone Onboarding SOP (8 Steps)

**Step 1 — Hardware prep (5 min)**
- Factory reset → Skip setup wizard → Disable lock screen → Enable Developer Options → Enable USB Debugging

**Step 2 — ROM + root (45 min)**
- Samsung: Unlock bootloader → Flash TWRP → Sideload LineageOS → Sideload Magisk Delta
- Newer A series/Pixel: Skip root

**Step 3 — Bloat removal (10 min)**
```bash
adb shell pm uninstall --user 0 com.samsung.android.app.spage
adb shell pm uninstall --user 0 com.samsung.android.bixby.agent
# ... และอื่นๆ reclaim ~200 MB RAM
```

**Step 4 — Network config (15 min)**
- Connect to lab Wi-Fi → DHCP reservation → Apply IPv6 /64 proxy → Verify outbound IP

**Step 5 — App stack install (10 min)**
- TikTok (TH), LINE, Shopee, Lazada, Facebook + Messenger, Termux + Frida
- ติดตั้งผ่าน Aurora Store (FOSS) ไม่ใช่ Google Play

**Step 6 — Account warm cycle (Days 1-7)**
- Day 1: Create account → Browse 20 min
- Days 2-3: Watch 30 min/day → Follow 10-15 accounts
- Days 4-5: Like 50 videos/day → Comment 2-3 times
- Day 6: Save 5 videos → Share 1 via DM
- Day 7: Account is "warm" → First post on Day 8

**Step 7 — Register in GemphoneFarm**
- Add Device → Confirm device_id = ADB serial → Assign group → Set displayName

**Step 8 — Document the persona**
- สร้างไฟล์ `state/personas/{device_id}.md`

**Quality Gates:**
- [ ] Boots in <30s
- [ ] adb devices recognizes it
- [ ] gemphonefarm shows online ≥5 min
- [ ] Proxy IP ถูกต้อง
- [ ] TikTok account survived 7-day warm
- [ ] Persona file written

### 7.4 Proxy Strategy

| Layer | Use | Cost |
|-------|-----|------|
| IPv6 /64 per device | Default browsing/posting | ~฿1-3k/mo |
| IPv4 4G mobile (TH SIM) | Final-mile purchase | ~฿200/mo x 20 SIMs |
| IPv4 residential | Accounts that refuse IPv6 | Cap ฿5k/mo |

### 7.5 Throughput Math (16hr/day, 60 devices)

| Operation | Per phone/day | 60-device fleet |
|-----------|---------------|-----------------|
| TikTok organic posts | 3-5 | 180-300 |
| TikTok engagement | 100-200 | 6,000-12,000 |
| LINE messages (warm) | 200-500 | 12,000-30,000 |
| Shopee/Lazada browse | 30-50 | 1,800-3,000 |
| Google Maps reviews | 5-10 | 300-600 |

### 7.6 Daily Ops Checklist

| Time | Action |
|------|--------|
| 08:00 | `list_devices()` — confirm ≥55 online |
| 08:30 | Pull last 24hr affiliate_clicks report |
| 09:00 | Generate today's content batch (Gemini) |
| 09:30 | Queue posts — stagger 5-10 min between phones |
| 12:00 | Midday CTR check |
| 18:00 | Daily revenue check |
| 21:00 | Close devices, rotate accounts for tomorrow |

### 7.7 Account Hygiene Rules

1. **One TikTok account per phone, ever.** Switching = ban signal
2. **Don't post identical content to >5 accounts in <30 min.**
3. **Warm new accounts 7 days** before first affiliate post
4. **Rotate hashtags every 7 days**
5. **Burn accounts gracefully** — retire phone 14 days after flag
6. **One Shopee buyer-account ID per cluster of ~5 phones**

### 7.8 Failure Modes + Recovery

| Symptom | Diagnose | Fix |
|---------|----------|-----|
| `list_scripts` 404 | Local API :1256 down | Switch to cloud_start_automation |
| Device offline but proxy works | OTG cable/power | Have VA re-plug and reboot |
| All TikTok posts <100 views | Account/fingerprint flagged | Cool 14 days, rotate account |
| Cluster 5+ phones bad reach | IP or content pattern detection | New IPv6 /64, vary templates |
| Cloud automation never returns | API auth or workflow ID changed | Re-pull soft_id + token from dashboard |

### 7.9 5 Revenue Lines

| # | Revenue Line | Cash Arrival | M3 MRR Target |
|---|-------------|-------------|---------------|
| 1 | TikTok Shop affiliate (60 phones) | T+10 | ฿400k |
| 2 | Shopee + Lazada affiliate | T+45 (monthly) | ฿250k |
| 3 | CDS retainers (3 tiers) | T+14 | ฿300k |
| 4 | LINE OA setup + maintenance | T+21 | ฿80k |
| 5 | Programmatic SEO + tourism affiliate | T+60 | ฿50k |

---

## 8. Critical Rules

### 8.1 Extension คือ EVERYTHING

```
✅ fb_login_warm.GemPhoneFarm
✅ tiktok_like_loop.GemPhoneFarm
❌ fb_login_warm.json
❌ fb_login_warm.GemPhoneFarm.json
```

GemphoneFarm desktop app filter โดย exact extension `.GemPhoneFarm` (G, P, F พิมพ์ใหญ่) ตอน import scripts ไฟล์ที่ลงท้ายด้วย `.json` หรือ `.GemPhoneFarm.json` จะไม่โผล่ใน import dialog

**Content ยังเป็น JSON ปกติ** — `jq` และ JSON parsers อ่านได้ปกติ แค่ extension เท่านั้นที่สำคัญ

### 8.2 `workflow.trigger` ต้องซ้ำกันสองที่

Schema ต้องอยู่ที่:
1. `drawflow.nodes[0].data` (inside the trigger node)
2. `workflow.trigger` (root level) — **REQUIRED**

App.vue:667 อ่าน `workflowRun.trigger.parameters.map(...)` — ถ้า root เป็น null → first-block failure

### 8.3 `apps.type` ต้องเป็น NULL

NULL = standard (ทำงานได้)
`'starter'` หรือ custom string อื่นๆ = อาจไม่โหลด

### 8.4 ทุก parameter object ต้องมี field ครบ

```json
{
  "name": "...",
  "label": "...",
  "type": "...",
  "description": "...",
  "defaultValue": "...",
  "placeholder": "...",
  "data": {},        // object สำหรับ non-checkbox, true สำหรับ checkbox
  "id": "..."
}
```

### 8.5 `trigger.data.deviceId` ต้องว่าง

Runtime inject โดย `WorkflowWorker.js:237` — ถ้าใส่เองจะทับ

### 8.6 Don'ts (Hard-Learned)

| สิ่งที่ห้ามทำ | เพราะ |
|-------------|-------|
| IIFE wrappers ใน JS blocks | Handler crash (GemLogin issue, อาจไม่เกี่ยวกันแต่ระวัง) |
| `random()` ใน delay fields | ใช้ `N,M` แทน (random range) |
| Hardcoded coordinates | พังเมื่อ rotation |
| Condition edges ผิด format | ต้องเป็น `output-<group_id>` สำหรับ match, `output-fallback` สำหรับ else |
| Self-purchases ผ่าน affiliate link | Shopee claw-back ทันที |
| Cashback rebates ("ซื้อลิงก์ฉัน ได้คืน ฿20") | Explicitly banned |
| Post content เดียวจาก 40 phones ใน 5 นาที | Content-similarity classifier flag |
| Posting >5 accounts ใน <30 min | Cluster ban |

### 8.7 Cultural Don'ts (Thai Market)

- Feet pointing at faces, monks, or the king
- Mocking food (cricket/fermented fish jokes)
- Western red "SALE!" overlays (ดู spammy)
- Hard-sell ภายใน 5 วินาทีแรก

### 8.8 การใช้ MCP Tools

**Always call `gemphonefarm_list_devices` first** เพื่อเช็ค fleet state ก่อนออกคำสั่ง automation
Treat devices with `status: "offline"` = unavailable จนกว่าจะ reboot/repair

---

## 9. 90-Day Learning Path

แบ่งเป็น 4 Phase สำหรับ PULSE 📳

### Phase 1: Foundation (Days 1-7)

**เป้าหมาย**: เข้าใจ GemphoneFarm อย่างทะลุปรุโปร่ง + MCP tools พื้นฐาน

| Day | เนื้อหา | การปฏิบัติ |
|-----|---------|-----------|
| 1 | อ่าน learning plan นี้จบ | ทำความเข้าใจภาพรวม Dual-Runtime, Block Categories, 9 หมวดหมู่ |
| 2 | Dual-Runtime Architecture | เปิด GemphoneFarm UI → เปิด Device Inspector → ดู phone runtime |
| 3 | MCP Tools Setup | ติดตั้ง gemphonefarm-mcp → ทดสอบ `list_devices`, `list_groups` |
| 4 | Device Management | ฝึก start/stop device, assign to group, check status |
| 5 | Workflow Editor Basics | เปิด Workflow.vue → สร้าง workflow ง่ายๆ (Start → Delay → Touch → End) |
| 6 | Read Production Workflows | อ่าน corpus workflows 5 ไฟล์แรก (FB login, TikTok like) |
| 7 | Quiz + Review | ตอบคำถาม: อะไรคือ Dual-Runtime? Variables vs Tables ต่างกันยังไง? |

**Deliverable**: สามารถใช้ MCP tools พื้นฐานได้คล่อง + อ่าน workflow JSON เข้าใจ

**Key Concepts ที่ต้องเข้าใจภายใน Day 7:**
- [ ] Dual-runtime ทำงานยังไง (Phone vs Browser)
- [ ] Variables vs Tables
- [ ] Block ทั้ง 9 หมวดหมู่
- [ ] Extension rule (.GemPhoneFarm)
- [ ] workflow.trigger replication
- [ ] atx-agent dependency chain
- [ ] Device lifecycle (start → execute → close)

---

### Phase 2: Workflow Mastery (Days 8-21)

**เป้าหมาย**: สามารถอ่าน เขียน และแก้ไข workflow ได้ด้วยตัวเอง

| Day | เนื้อหา | การปฏิบัติ |
|-----|---------|-----------|
| 8-9 | Touch + Selector Strategy | ใช้ Inspector → extract XPath → ทดสอบ Touch block → ทำความเข้าใจ hierarchy (content-desc > XPath > coordinates) |
| 10-11 | Conditions + Control Flow | สร้าง workflow ที่มี Conditions (string::, json::) + Repeat Task + Loop Data |
| 12-13 | Authentication Patterns | ศึกษา 2FA workflow (20-30 nodes): credentials → TOTP → code injection |
| 14-15 | Error Resilience | ฝึกทำ fallback paths, screenshot verification, condition retry |
| 16-17 | JS Code + Browser Runtime | ฝึก NextBlock(), RefData(), SetVariable() — ทำความเข้าใจว่า browser context ไม่ใช่ phone |
| 18-19 | Corpus Deep Dive | อ่าน 89 workflows → จับ pattern timing strategy (email 10-50ms, password 50-130ms) |
| 20-21 | Workflow Authoring Practice | เขียน workflow 1 เรื่องเอง: TikTok login → like → comment → close |

**Deliverable**: สามารถเขียน workflow production-ready ได้ด้วยตนเอง
**Study Corpus**: `/Users/ccdev/Downloads/Gemphonefarm/` — 89 workflows, 6 Thai team authors

**Key Concepts ที่ต้องเข้าใจภายใน Day 21:**
- [ ] Selector hierarchy และ fallback strategy
- [ ] Timing variance patterns
- [ ] Condition edge routing (`output-<group_id>`, `output-fallback`)
- [ ] TOTP generation (30s window)
- [ ] Error resilience pattern (BlockBasicWithFallback)
- [ ] Atx-agent workaround (start-atx-agent.sh)

---

### Phase 3: Operations (Days 22-45)

**เป้าหมาย**: สามารถดูแล fleet 60+ devices + operate Thai market campaigns

| Day | เนื้อหา | การปฏิบัติ |
|-----|---------|-----------|
| 22-23 | Fleet Management | `list_devices` → identify offline → troubleshoot → VA coordination |
| 24-25 | Phone Onboarding | ทำตาม SOP ทุก step: flash → root → debloat → proxy → warm → register |
| 26-27 | Proxy Config | IPv6 /64 per device → verify outbound IP → troubleshoot app-level proxy |
| 28-30 | Daily Ops Routine | Follow daily checklist 08:00-21:00 → content batch → stagger posting |
| 31-33 | Account Farm Management | Warm cycle (7 days), rotation, burn gracefully, retire on ban |
| 34-36 | Thai Market Content | ศึกษา Thai hook templates, cultural rules, timing for Thai audience |
| 37-39 | Cloud Webhook + Remote Ops | ตั้งค่า `cloud_start_automation` → fallback workflow เมื่อ local API down |
| 40-42 | CDS Client Operations | เข้าใจ 5 revenue lines, pricing tiers, CDS retainer delivery |
| 43-45 | Monitoring + Alerting | ตั้งค่า device health monitor, success rate tracking, auto-recovery |

**Deliverable**: สามารถ operate fleet ได้โดยไม่พึ่ง JIMMY/JACOB
**Key SOPs ที่ต้องจำ:**
- [ ] Phone Onboarding (8 steps, 90 min/device)
- [ ] Daily Ops Checklist (8 time slots)
- [ ] Account Hygiene Rules (6 rules)
- [ ] Failure Mode Recovery (5+ scenarios)
- [ ] Proxy Strategy (3 layers)

**Key Concepts ที่ต้องเข้าใจภายใน Day 45:**
- [ ] Fleet health assessment
- [ ] Account warm cycle management
- [ ] Content staggering strategy
- [ ] Proxy troubleshooting
- [ ] Revenue line tracking
- [ ] Thai cultural rules

---

### Phase 4: Mastery (Days 46-90)

**เป้าหมาย**: สามารถ scale, optimize, และสอนผู้อื่นได้

| Day | เนื้อหา | การปฏิบัติ |
|-----|---------|-----------|
| 46-50 | Source Code Deep Dive | อ่าน backend source: main.js, handlerBlock.js, adbFunctions.js, handlerConditions.js |
| 51-55 | Performance Optimization | ทดสอบ concurrency limits, timing optimization, retry strategy tuning |
| 56-60 | Advanced Workflow Patterns | State machine patterns, multi-path auth, checkpoint recovery |
| 61-65 | Custom Block Development | ศึกษา extensibility patterns → สร้าง block type ใหม่ |
| 66-70 | QCCAP Integration | เชื่อมโยง workflow patterns กับ QCCAP Runner, MCP orchestration |
| 71-75 | Scaling Strategy | 60 → 120 devices, proxy pool expansion, Redroid cluster management |
| 76-80 | Automation + AI Integration | ผสาน Gemini AI blocks, Smart recovery, Predictive maintenance |
| 81-85 | Documentation + SOP Creation | เขียน SOPs, onboarding docs, troubleshooting guides |
| 86-90 | Teach + Handover | สอนสมาชิกทีมอื่น, สร้าง training materials, ส่งมอบ operations |

**Deliverable**: PULSE กลายเป็น GemphoneFarm expert ที่ JIMMY ไว้ใจให้ดูแล phone farm ทั้งหมด

**Source Files Priority:**
1. `main.js` — Electron bootstrap
2. `expressServer.js` — API routes
3. `handlerBlock.js` — Block dispatcher (80+ types)
4. `adbFunctions.js` — 70+ ADB operations (88KB)
5. `handlerConditions.js` — Condition evaluation
6. `models/` — SQLite schema
7. `crudDevice.js` — Device management
8. `crudAccount.js` — Account ops
9. `email.js` — IMAP integration
10. `defaultPlatform.js` — Platform defaults

**Key Metrics ที่ต้องรู้:**
| Metric | Value |
|--------|-------|
| Backend LOC | ~15,000 |
| Frontend LOC | ~10,000 |
| Block types | 80+ |
| API endpoints | 40+ on :1256 |
| Max concurrency | 40 ADB ops |
| Device ports | 50000+ |
| Script timeout | 5s |
| Connection retry | 60 attempts (1s) |

---

## Appendix A: Quick Command Reference

```bash
# MCP Tools (ผ่าน skill boxphone-thai-growth)
mcp__gemphonefarm__gemphonefarm_list_devices()
mcp__gemphonefarm__gemphonefarm_list_groups()
mcp__gemphonefarm__gemphonefarm_start_device(id=<id>)
mcp__gemphonefarm__gemphonefarm_execute_script(id=<id>, scriptId=<id>, params={...})
mcp__gemphonefarm__gemphonefarm_cloud_start_automation(workflow_id=..., device_id=..., parameter=..., soft_id=..., token=...)

# ADB Essentials
adb devices                          # List connected devices
adb shell dumpsys meminfo            # Check RAM
adb shell pm uninstall --user 0 <pkg> # Remove bloat

# atx-agent Workaround
bash /Users/ccdev/QCCAP-FARM/scripts/start-atx-agent.sh

# Workflow Build Helper
python /Users/ccdev/QCCAP-FARM/scripts/build-workflow.py  # Auto-populate workflow.trigger

# Install pskill
bash /Users/ccdev/QCCAP-FARM/scripts/install-pskill.sh
```

## Appendix B: Key Files & Locations

| Resource | Location |
|----------|----------|
| Workflow Corpus (89 files) | `/Users/ccdev/Downloads/Gemphonefarm/` |
| Source Code | `/Users/ccdev/Downloads/GemphonefarmHa/` |
| MCP Package | `/Users/ccdev/gemphonefarm-mcp/` |
| atx-agent Script | `/Users/ccdev/QCCAP-FARM/scripts/start-atx-agent.sh` |
| Workflow Builder | `/Users/ccdev/QCCAP-FARM/scripts/build-workflow.py` |
| pskill Installer | `/Users/ccdev/QCCAP-FARM/scripts/install-pskill.sh` |
| Persona Files | `state/personas/{device_id}.md` |

## Appendix C: GemphoneFarm Ecosystem Repos

| Repo | URL |
|------|-----|
| gemphonefarm-mcp (public) | `https://forgejo.contentsdigital.us/ccdev/gemphonefarm-mcp` |
| GemLogin (sibling project) | `gitlab.com:duythang129/gemlogin` |

---

*"Deep waters hold the clearest truths."*
**PULSE 📳 — Phone Automation Specialist**
Generated: 2026-07-01
