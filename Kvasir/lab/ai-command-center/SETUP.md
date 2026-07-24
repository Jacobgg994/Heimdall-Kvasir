# 🖥️ JACOB Command Center — Setup Guide

> รันบน WSL Ubuntu · tmux · DeepSeek API

---

## 🏗️ สภาพแวดล้อมจริง

```
Windows 11
  └─ WSL2: Ubuntu
       ├─ tmux session (persistent)
       │    └─ Claude CLI (deepseek-v4-pro[1m])
       ├─ FastAPI server (:8000) ← ตัวใหม่
       └─ React frontend (:3000) ← ตัวใหม่
```

## 🔑 Env Vars (ที่ใช้อยู่แล้ว)

```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=sk-94c2309a3eeb46a48b169739a87a0c55
export ANTHROPIC_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
export CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
export CLAUDE_CODE_EFFORT_LEVEL=max
```

## 🚀 วิธีรัน Claude CLI

```bash
claude --dangerously-skip-permissions
```

---

## 🧱 Architecture (ปรับตามจริง)

```
Windows Browser (Chrome/Edge)
  └─ http://localhost:3000 (WSL auto-forwards)
       │
WSL Ubuntu ─────────────────────────────
       │
  ┌────┴────────────────────────────┐
  │  FastAPI Server (:8000)         │
  │  • loads ~/.bashrc env vars     │
  │  • subprocess → Claude CLI      │
  │  • subprocess → Agent spawn     │
  │  • file system access           │
  └─────────────────────────────────┘
       │
  ┌────┴────────────────────────────┐
  │  tmux session                   │
  │  • JIMMY session (persistent)   │
  │  • env vars loaded              │
  └─────────────────────────────────┘
```

---

## 🔧 วิธีรัน Server

```bash
# 1. โหลด env vars
source ~/.bashrc

# 2. เข้าโปรเจกต์
cd /home/admin_jacob/AIproject/Kvasir/lab/ai-command-center

# 3. ติดตั้ง dependencies
pip install fastapi uvicorn websockets

# 4. รัน server (ใน tmux session ใหม่)
uvicorn server:app --host 0.0.0.0 --port 8000

# 5. รัน frontend (อีก terminal)
cd frontend && npm run dev -- --port 3000

# 6. เปิด Windows browser
# http://localhost:3000
```

---

## 🔌 API (ปรับให้ใช้ env vars จริง)

```python
# server.py — ใช้ env vars เดียวกับ Claude CLI

import os
import subprocess
import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS — allow localhost frontend
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# โหลด env vars จาก shell
ENV = {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": os.environ.get("ANTHROPIC_AUTH_TOKEN", ""),
    "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_EFFORT_LEVEL": "max",
    "HOME": os.environ["HOME"],
    "PATH": os.environ["PATH"],
}

def run_claude(prompt: str, cwd: str = None) -> str:
    """รัน Claude CLI แบบเดียวกับที่ใช้ใน tmux"""
    cmd = ["claude", "--dangerously-skip-permissions", "-p", prompt]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd or os.environ["HOME"] + "/AIproject",
        env={**os.environ, **ENV},
        timeout=300
    )
    return result.stdout

def spawn_agent(agent_file: str, prompt: str, cwd: str = None):
    """Spawn Claude agent แบบเดียวกับที่ JIMMY ใช้"""
    cmd = [
        "claude", "--dangerously-skip-permissions",
        "--agent", agent_file,
        "-p", prompt
    ]
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd or os.environ["HOME"] + "/AIproject",
        env={**os.environ, **ENV}
    )

@app.post("/api/chat")
async def chat(request: dict):
    prompt = request.get("prompt", "")
    cwd = request.get("cwd", None)
    result = run_claude(prompt, cwd)
    return {"response": result}

@app.post("/api/agent/spawn")
async def agent_spawn(request: dict):
    agent_name = request.get("agent", "gemmy")
    prompt = request.get("prompt", "")
    agent_file = f"/home/admin_jacob/AIproject/Kvasir/team/{agent_name}/CLAUDE.md"
    proc = spawn_agent(agent_file, prompt)
    return {"status": "spawned", "agent": agent_name, "pid": proc.pid}

@app.get("/api/system")
async def system_info():
    return {
        "wsl": True,
        "tmux": "JIMMY session active",
        "model": "deepseek-v4-pro[1m]",
        "subagent_model": "deepseek-v4-flash"
    }
```

---

## 📝 ข้อควรรู้

- WSL2 forward localhost อัตโนมัติ → `localhost:3000` ใน Windows ไปถึง WSL ได้เลย
- ต้องรันใน tmux เพื่อให้ session อยู่ต่อเนื่อง (แม้ปิด terminal)
- ใช้ env vars ชุดเดียวกับ Claude CLI — ไม่ต้อง config เพิ่ม
- DeepSeek API เป็น backend — base URL ตั้งไว้แล้ว
- `--dangerously-skip-permissions` ต้องใช้เพราะรันแบบ non-interactive

---

> 📅 2026-06-30 · JACOB Team
