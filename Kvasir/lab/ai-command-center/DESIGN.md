# 🖥️ AI Command Center — Design Document

> "สั่ง AI ได้จากเว็บ — ทุกความสามารถที่มีตอนนี้ แต่อยู่ในเบราว์เซอร์"

---

## 🎯 วิสัยทัศน์

**AI Command Center** = Claude Code เวอร์ชันเว็บ รันบนเครื่องตัวเอง localhost เท่านั้น
- 💬 แชทกับ AI เหมือน Claude Code
- 🤖 สั่ง Agent หลายๆ ตัวพร้อมกัน
- 📂 จัดการไฟล์ (อ่าน/เขียน/แก้)
- 🔀 Git integration
- 📊 Dashboard เห็นสถานะทีม JACOB Team
- 🔒 localhost only — ไม่ expose สู่เน็ต

---

## 🧱 Architecture

```
┌─────────────────────────────────────────────────┐
│              Browser (localhost:3000)             │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │  Chat    │ │  Agents  │ │  File Explorer   │ │
│  │  Panel   │ │  Panel   │ │  Panel           │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │  Git     │ │  Team    │ │  Settings        │ │
│  │  Panel   │ │  Status  │ │  Panel           │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
└──────────────────┬──────────────────────────────┘
                   │ WebSocket + REST API
┌──────────────────┴──────────────────────────────┐
│           Backend (FastAPI :8000)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │  Chat    │ │  Agent   │ │  File System     │ │
│  │  Service │ │  Manager │ │  Service         │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │  Git     │ │  MCP     │ │  Auth (local)    │ │
│  │  Service │ │  Bridge  │ │  Service         │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────┐
│              AI Layer                            │
│  ┌──────────────────┐ ┌──────────────────────┐  │
│  │  LiteLLM Proxy   │ │  Local Ollama        │  │
│  │  (:4000)         │ │  (:11434)            │  │
│  └──────────────────┘ └──────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

| Layer | Technology | เพราะ |
|-------|-----------|-------|
| **Frontend** | React + Tailwind CSS + shadcn/ui | เร็ว สวย CANVAS ออกแบบ |
| **State** | Zustand | เบา เร็ว ไม่ซับซ้อน |
| **Realtime** | WebSocket (FastAPI) | Streaming chat |
| **Backend** | FastAPI + Uvicorn | Python, async, CORAL ถนัด |
| **AI Gateway** | LiteLLM | รวมหลาย provider |
| **Local AI** | Ollama (qwen3, llama) | ออฟไลน์ได้ |
| **Auth** | Simple password (local) | localhost ไม่ต้องซับซ้อน |
| **Database** | SQLite | เบา ไม่ต้อง setup |
| **File Ops** | Python pathlib + watchdog | จัดการไฟล์ในเครื่อง |

---

## 📱 UI Layout

```
┌──────────────────────────────────────────────────┐
│  🤖 AI Command Center        [⚙️] [🌙] [📊]     │
├────────────┬─────────────────────────────────────┤
│  📁 Files  │  💬 Chat                            │
│            │                                     │
│  📂 /home/ │  You: สร้างไฟล์ test.py             │
│  ├─AIproject│  AI: ✅ สร้างแล้ว!                  │
│  ├─Docs    │  ```python                         │
│  ├─Images  │  def hello():                      │
│  │         │      print("Hello")                │
│  ├─...     │  ```                               │
│            │                                     │
│  [New File]│  ─────────────────────────────      │
│  [Upload]  │  📎 [แนบไฟล์] [🤖 Agent] [🌐 Git] │
│            │  [💬 พิมพ์ข้อความ...]    [ส่ง ▶]    │
├────────────┴─────────────────────────────────────┤
│  🤖 Agents: IDLE │ 🟢 System: OK │ 📚 RAM: 4.2GB │
└──────────────────────────────────────────────────┘
```

### Sidebar Tabs
| Tab | Icon | เนื้อหา |
|-----|------|--------|
| **Chat** | 💬 | หน้าหลัก — คุยกับ AI |
| **Agents** | 🤖 | สร้าง/จัดการ agent ย่อย |
| **Files** | 📂 | File explorer — อ่าน/เขียน/แก้ |
| **Git** | 🔀 | Commit, diff, branch, push |
| **Team** | 👥 | สถานะ JACOB Team 23 คน |
| **Settings** | ⚙️ | Model, API keys, config |

---

## 🔧 Features

### 💬 Chat Panel (หลัก)
- [x] Streaming text (เหมือน Claude Code)
- [x] Markdown render + syntax highlight
- [x] แนบไฟล์ + รูปภาพ
- [x] Code blocks — click to copy / apply to file
- [x] Chat history (SQLite)
- [x] Multi-session — กี่แชทก็ได้ สลับได้

### 🤖 Agent Panel
- [x] สร้าง agent ย่อย — พร้อม prompt
- [x] เลือก agent type (general, explore, plan)
- [x] รัน parallel agents
- [x] ดูผล agent แต่ละตัว
- [x] หยุด/ restart agent

### 📂 File Panel
- [x] Tree view — เหมือน VS Code
- [x] คลิกดูเนื้อหา
- [x] แก้ไข + save
- [x] สร้างไฟล์/โฟลเดอร์ใหม่
- [x] Drag & drop upload

### 🔀 Git Panel
- [x] `git status` — เห็นไฟล์ที่เปลี่ยน
- [x] `git diff` — ดู diff สีสวย
- [x] Commit + push (no force)
- [x] Branch list + switch
- [x] PR preview

### 👥 Team Panel
- [x] ตาราง 23 คน — ดูสถานะ
- [x] กดที่ชื่อ → ดูโปรไฟล์ + learnings
- [x] ดูว่าใครกำลังทำอะไร
- [x] Quick spawn — สร้าง agent ให้ทีม

---

## 🔌 API Endpoints

```
POST   /api/chat              → ส่งข้อความ + streaming response
GET    /api/chat/history      → ประวัติแชท
POST   /api/agent/spawn       → สร้าง agent ใหม่
GET    /api/agent/:id         → ดูผล agent
POST   /api/agent/:id/stop    → หยุด agent
GET    /api/files             → list ไฟล์ (tree)
GET    /api/files/:path       → อ่านเนื้อหาไฟล์
POST   /api/files/:path       → เขียนไฟล์
PUT    /api/files/:path       → แก้ไขไฟล์
DELETE /api/files/:path       → ลบไฟล์
GET    /api/git/status        → git status
GET    /api/git/diff          → git diff
POST   /api/git/commit        → commit
POST   /api/git/push          → push
GET    /api/team/list         → รายชื่อทีม
GET    /api/system/stats      → CPU, RAM, Disk
POST   /api/auth/login        → เข้าสู่ระบบ (simple password)
```

---

## 🚀 แผนพัฒนา

| Phase | เนื้อหา | คน | เวลา |
|-------|--------|-----|------|
| **P1** | Backend core + Chat API | TIDE 🌊, CORAL 🪸 | 2-3 วัน |
| **P2** | Frontend UI + Chat Panel | PYKE 🐟, CANVAS 🎨 | 2-3 วัน |
| **P3** | Agent + File + Git | TIDE, PYKE | 2 วัน |
| **P4** | Team Dashboard | PYKE | 1 วัน |
| **P5** | Test + Deploy | SHELL 🐚, DRIFT 🌫️ | 1 วัน |

---

## 🔒 Security (PHANTOM 🛡️)

- [x] localhost only — firewall บล็อก external access
- [x] Simple password (SHA256 hash ใน SQLite)
- [x] API key encryption at rest
- [x] No telemetry / no external calls ยกเว้น AI API
- [x] File access — จำกัดเฉพาะ ~/AIproject และ subdirectories
- [x] Rate limiting — กัน spam

---

## 🎨 Design Specs (CANVAS)

- **สีหลัก**: Blue gradient `#3b82f6 → #1d4ed8` (ตาม brand GemLogin)
- **พื้นหลัง**: `#0f172a` (dark mode default) / `#ffffff` (light mode)
- **Font**: JetBrains Mono (code), Noto Sans Thai (UI)
- **Card**: `#1e293b` bg, `#334155` border, radius 12px
- **Input**: `#1e293b` bg, `#3b82f6` focus border
- **Button**: Blue gradient, white text, radius 8px
- **Animation**: Smooth transitions, streaming cursor blink

---

> 📅 2026-06-30 · JACOB Team · Ready when you are
