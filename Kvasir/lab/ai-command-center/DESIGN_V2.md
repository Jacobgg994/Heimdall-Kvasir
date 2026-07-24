# 🖥️ JACOB Command Center — Design V2

> "ไม่ใช่ AI ทั่วไป — คือหน้าจอสำหรับสั่งงาน JACOB Team 23 คน แบบเดียวกับที่ JIMMY ใช้"

---

## 🎯 วิสัยทัศน์

**JACOB Command Center** = หน้าจอเว็บที่ให้ JACOB สั่งงานทีม 23 คนได้เอง โดยไม่ต้องผ่าน JIMMY
- 💬 คุยกับ JIMMY โดยตรง (รับคำสั่ง → กระจายงานให้ทีม)
- 👥 เลือกส่งงานให้ทีมไหนก็ได้
- 📂 เห็นไฟล์โปรเจกต์
- 🔀 Git ทุกอย่าง
- ⚡ ใช้ระบบเดียวกับที่ JIMMY ใช้ตอนนี้ (Claude Agent SDK, MCP, Bash)
- 🔒 localhost — รันบนเครื่องนี้เท่านั้น

---

## 🧱 Architecture

```
┌──────────────────────────────────────────────┐
│         Browser (localhost:3000)              │
│                                              │
│  💬 Chat (คุยกับ JIMMY)                      │
│  👥 Team Panel (ดู 23 คน, ส่งงานให้ใครก็ได้)   │
│  📂 Files (ดูไฟล์, แก้ไข)                    │
│  📊 Dashboard (งานที่กำลังทำ, ผลลัพธ์)        │
└──────────────────┬───────────────────────────┘
                   │ WebSocket
┌──────────────────┴───────────────────────────┐
│       Backend (FastAPI :8000)                 │
│                                              │
│  POST /chat → ส่งข้อความ → Claude CLI        │
│  POST /agent → spawn agent → Claude Agent    │
│  GET  /files → อ่านไฟล์ในเครื่อง              │
│  POST /git   → รัน git commands               │
│  POST /bash  → รัน shell commands             │
│  GET  /team  → ข้อมูลทีมจาก memory/           │
└──────────────────┬───────────────────────────┘
                   │ subprocess
┌──────────────────┴───────────────────────────┐
│         Claude Code CLI (ที่มีอยู่แล้ว)         │
│         /home/admin_jacob/AIproject           │
│                                              │
│  • Claude Agent SDK                           │
│  • MCP Servers (gemlogin, gemphonefarm)       │
│  • Git, Bash, Filesystem                      │
│  • Memory System (.claude/memory/)            │
│  • Team Files (Kvasir/team/*/CLAUDE.md)       │
└──────────────────────────────────────────────┘
```

**ไม่ใช้ AI API ภายนอกเลย — ใช้ Claude Code CLI ที่มีอยู่แล้ว 100%**

---

## 📱 UI Layout

```
┌──────────────────────────────────────────────────┐
│  🖥️ JACOB Command Center        [🌙] [⚙️]       │
├────────────┬─────────────────────────────────────┤
│            │  💬 JIMMY                            │
│  👥 Team   │  ─────────────────────────────      │
│            │  JACOB: ให้ SALMON เขียนบทความ       │
│  🌊 JIMMY  │         TikTok Shop 2026             │
│  🔭 JASPER │                                     │
│  🔬 SCOPE  │  JIMMY: ✅ รับทราบครับ                │
│  🔍 PRISM  │         จะส่ง SALMON จัดการทันที      │
│  🪸 CORAL  │         ...                          │
│  💎 GEMMY  │                                     │
│  📈 KOMHAS │  ─────────────────────────────      │
│  🎨 SALMON │  [📎 ไฟล์] [🤖 สร้าง Agent] [⚡ Bash]│
│  🦅 KAMU   │  [💬 พิมพ์...]              [▶ ส่ง]  │
│  🤝 CILA   │                                     │
│  🛡️ PHANTOM│                                     │
│  🆕 + อีก  │                                     │
│            │                                     │
│  [ส่งงาน]  │                                     │
├────────────┴─────────────────────────────────────┤
│  ⚡ Agents: 1 running │ 📊 RAM: 4.2GB │ 💾 Disk: 45% │
└──────────────────────────────────────────────────┘
```

### Sidebar — 3 โหมด

| โหมด | เนื้อหา |
|------|--------|
| **💬 Chat** | คุยกับ JIMMY โดยตรง |
| **👥 Team** | เลือกคน → พิมพ์คำสั่ง → ส่งงานให้คนนั้นเลย |
| **📂 Files** | ดูไฟล์โปรเจกต์ |

### วิธีใช้

**แบบที่ 1 — คุยกับ JIMMY:**
```
JACOB: "ให้ SALMON เขียนบทความ TikTok Shop 2026"
  → JIMMY ได้รับ → กระจายงานให้ SALMON → รายงานผลกลับ
```

**แบบที่ 2 — ส่งงานให้ใครก็ได้โดยตรง:**
```
คลิก SALMON 🎨 → พิมพ์ "เขียนบทความ TikTok Shop 2026" → ส่ง
  → Claude spawn SALMON agent → ทำงาน → ผลกลับมา
```

**แบบที่ 3 — สั่ง Bash ตรงๆ:**
```
พิมพ์ bash: git status
  → รันในเครื่อง → แสดงผล
```

---

## 🔌 API Endpoints

```
POST   /api/chat              → ส่งข้อความหา JIMMY → Claude CLI
POST   /api/chat/stream       → WebSocket streaming
POST   /api/agent/spawn       → สร้าง agent (ใช้ team member CLAUDE.md)
       body: { agent: "salmon", prompt: "เขียนบทความ..." }
GET    /api/agent/list        → agents ที่กำลังรัน
POST   /api/agent/:id/stop    → หยุด agent
POST   /api/bash              → รัน shell command
       body: { command: "git status", cwd: "/home/admin_jacob/AIproject" }
GET    /api/files             → list ไฟล์ (tree)
GET    /api/files/:path       → อ่านไฟล์
POST   /api/files/:path       → เขียน/แก้ไขไฟล์
GET    /api/team              → ข้อมูลทีมจาก Kvasir/team/
GET    /api/system            → CPU, RAM, disk
```

---

## 👷 แผนพัฒนา

| Phase | เนื้อหา | ใคร | เครื่องมือ |
|-------|--------|-----|-----------|
| **P1** | Backend — Chat API + Agent Spawn + Bash | TIDE, CORAL | FastAPI, subprocess |
| **P2** | Frontend — Chat UI + Team Panel | PYKE, CANVAS | React, Tailwind |
| **P3** | File Explorer + Git Panel | PYKE, TIDE | Tree view |
| **P4** | Dashboard + Agent Monitor | PYKE | WebSocket |
| **P5** | Polish + Deploy localhost | SHELL, DRIFT | Docker, nginx |

### Technical Notes

- **Agent Spawn**: ใช้ `subprocess` เรียก Claude CLI แบบเดียวกับที่ JIMMY ใช้ตอนนี้
- **Chat**: WebSocket เชื่อมต่อกับ Claude CLI session
- **Files**: อ่าน/เขียนไฟล์ผ่าน Python `pathlib` — จำกัดเฉพาะ `~/AIproject`
- **Bash**: `subprocess.run()` — sandboxed, whitelist commands
- **ไม่ใช้ external API key ใดๆ** — ใช้ Claude Code ที่ติดตั้งในเครื่องแล้ว

---

## 🔒 Security

- localhost:3000 เท่านั้น — firewall block external
- Password login (sha256 ใน SQLite)
- Bash: whitelist เท่านั้น (git, ls, cat, grep, find, python, node)
- File access: จำกัดเฉพาะ ~/AIproject และ subdirectories
- Agent spawn: ใช้ Claude Agent SDK ที่มีอยู่ — ไม่ต้องใช้ API key ใหม่

---

> 📅 2026-06-30 · JACOB Team
