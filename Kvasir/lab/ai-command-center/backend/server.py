"""
JACOB Command Center — Backend Server
FastAPI server with chat, agent management, file operations, bash, team, and system endpoints.

Usage:
    python server.py              # runs on 0.0.0.0:8000
    PORT=9000 python server.py    # override port
"""

import os
import subprocess
import json
import time
import signal
import glob
import uuid
import hashlib
import shlex
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, List, Any

import psutil
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

# ─── Configuration ───────────────────────────────────────────────────────────
# These are baked into the binary so they cannot be changed at runtime.
# They are used as the base environment for every Claude CLI subprocess.

BASE_DIR = os.path.expanduser("~/AIproject")
TEAM_DIR = os.path.join(BASE_DIR, "Kvasir/team")

ENV = {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "sk-94c2309a3eeb46a48b169739a87a0c55",
    "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_EFFORT_LEVEL": "max",
    "HOME": os.environ.get("HOME", "/home/admin_jacob"),
    "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
}

# Commands allowed through /api/bash
WHITELIST_COMMANDS = {
    "git", "ls", "cat", "grep", "find", "python", "python3", "node", "npm",
    "curl", "mkdir", "cp", "mv", "pwd", "whoami", "df", "free", "ps",
    "wget", "nano", "vim", "head", "tail", "wc", "sort", "uniq", "echo",
    "date", "which", "file", "du", "touch", "chmod", "chown", "tar", "gzip",
    "gunzip", "zip", "unzip", "ssh", "scp", "rsync", "diff", "comm",
    "pip", "pip3", "make", "cmake", "env", "printenv", "xargs", "tee",
}

# Simple token-based auth
PASSWORD_HASH = (
    "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
)  # sha256("password")
valid_tokens: Dict[str, float] = {}  # token -> creation_time (unix ts)

# Track spawned agent processes
running_agents: Dict[int, Dict[str, Any]] = {}

# ─── App Setup ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="JACOB Command Center",
    version="1.0.0",
    description="Backend API for the JACOB AI Command Center — chat, agents, files, bash, team, and system monitoring.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
logger = logging.getLogger("jacob-cc")

# ─── Auth Helpers ────────────────────────────────────────────────────────────


def verify_token(token: str) -> bool:
    """Check token validity with 24-hour expiry."""
    if token in valid_tokens:
        age = time.time() - valid_tokens[token]
        if age < 86400:
            return True
        del valid_tokens[token]
    return False


def check_auth_header(request: Request) -> bool:
    """Extract and verify Bearer token from Authorization header."""
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return verify_token(auth[7:])
    return False


SKIP_AUTH_PATHS = {"/", "/docs", "/openapi.json", "/redoc", "/health"}


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Global auth middleware — skip auth & WebSocket upgrade requests."""
    path = request.url.path

    # Always allow auth endpoints, docs, health, static assets, and CORS preflight
    if path.startswith("/api/auth") or path in SKIP_AUTH_PATHS:
        return await call_next(request)
    if path.startswith("/assets") or path.startswith("/favicon"):
        return await call_next(request)

    # Allow CORS preflight (OPTIONS) without auth
    if request.method == "OPTIONS":
        return await call_next(request)

    # Skip WebSocket upgrade requests (auth is handled inside the WS handler)
    connection = request.headers.get("connection", "").lower()
    if "upgrade" in connection:
        return await call_next(request)

    # All other REST endpoints require a valid Bearer token
    if not check_auth_header(request):
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Unauthorized. Provide a valid Bearer token. Use POST /api/auth/login to obtain one."
            },
        )

    return await call_next(request)


# ─── Path Helpers ────────────────────────────────────────────────────────────


def sanitize_path(relative_path: str) -> str:
    """Resolve a path relative to BASE_DIR with directory-traversal protection.

    Raises HTTPException(403) if traversal is detected, HTTPException(404)
    if the target does not exist on read operations (caller decides writes).
    """
    clean = relative_path.lstrip("/")
    target = (Path(BASE_DIR) / clean).resolve()
    base = Path(BASE_DIR).resolve()

    if not str(target).startswith(str(base)):
        raise HTTPException(status_code=403, detail="Path traversal detected")

    return str(target)


# ─── Claude CLI Helpers ──────────────────────────────────────────────────────


def run_claude(prompt: str, cwd: Optional[str] = None, timeout: int = 300) -> subprocess.CompletedProcess:
    """Run Claude CLI synchronously.

    Args:
        prompt: The text prompt to send.
        cwd: Working directory (defaults to BASE_DIR).
        timeout: Max seconds to wait (default 300).

    Returns:
        subprocess.CompletedProcess with stdout, stderr, returncode.

    Raises:
        HTTPException(504) on timeout.
        HTTPException(500) on other failures.
    """
    cmd = ["claude", "--dangerously-skip-permissions", "-p", prompt]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd or BASE_DIR,
            env={**os.environ, **ENV},
            timeout=timeout,
        )
        return result
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=504, detail=f"Claude CLI timed out after {timeout}s"
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Claude CLI not found. Is it installed and on PATH?",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Claude CLI error: {e}")


# ─── Team CLAUDE.md Parser ───────────────────────────────────────────────────


def parse_team_member(name: str, content: str) -> Dict[str, Any]:
    """Extract structured info from a team member's CLAUDE.md.

    Expected format:

        # NAME — Role Title
        > "quote / description"
        ## Identity
        **ฉันคือ**: NAME — description
        **พี่เลี้ยง**: MENTOR
        **มนุษย์**: JACOB
        **เกิด**: YYYY-MM-DD
        **ธีม**: 🎨 Theme Name
    """
    lines = content.split("\n")
    result: Dict[str, Any] = {
        "slug": name,
        "name": name,
        "title": "",
        "role": "",
        "theme": "",
        "human": "JACOB",
        "mentor": "",
        "description": "",
        "birth": "",
    }

    # Parse title line: # NAME — Role
    for line in lines:
        if line.startswith("# ") and "—" in line:
            parts = line[2:].split("—", 1)
            result["name"] = parts[0].strip()
            result["role"] = parts[1].strip()
            break
    else:
        # Fallback: just read first heading line
        for line in lines:
            if line.startswith("# "):
                result["title"] = line[2:].strip()
                break

    # Scan Identity / key-value lines
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("> ") and not result["description"]:
            result["description"] = stripped[2:].strip().strip('"').strip("'")
            continue

        if ":" not in stripped:
            continue

        key, _, value = stripped.partition(":")
        key_lower = key.strip().lower().replace("*", "")
        val = value.strip()

        if key_lower in ("ธีม", "theme"):
            result["theme"] = val
        elif key_lower in ("มนุษย์", "human"):
            result["human"] = val
        elif key_lower in ("พี่เลี้ยง", "mentor"):
            result["mentor"] = val
        elif key_lower in ("เกิด", "birth"):
            result["birth"] = val

    return result


# ─── Directory Tree ──────────────────────────────────────────────────────────


def build_directory_tree(path: str, prefix: str = "", max_items: int = 2000, max_depth: int = 5, depth: int = 0) -> List[str]:
    """Build a text-based directory tree (like ``tree``).

    Args:
        path: Directory to walk.
        prefix: Line prefix for nesting (used recursively).
        max_items: Cap on returned lines.
        max_depth: Maximum recursion depth.
        depth: Current depth (used recursively).

    Returns:
        List of strings representing the tree.
    """
    if depth > max_depth:
        return [f"{prefix}└── ... (max depth {max_depth} reached)"]

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return [f"{prefix}└── (permission denied)"]

    tree: List[str] = []
    for i, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        tree.append(f"{prefix}{connector}{entry}")

        if os.path.isdir(full_path) and not entry.startswith("."):
            ext = "    " if is_last else "│   "
            subtree = build_directory_tree(full_path, prefix + ext, max_items, max_depth, depth + 1)
            if len(tree) + len(subtree) > max_items:
                remaining = max_items - len(tree)
                if remaining > 0:
                    tree.extend(subtree[:remaining])
                tree.append(f"{prefix}{ext}... (truncated, >{max_items} items)")
                break
            tree.extend(subtree)

    return tree


# ═══════════════════════════════════════════════════════════════════════════
#  AUTH ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════


@app.post("/api/auth/login")
async def login(request: Request):
    """Simple password-based login.

    Body: {"password": "..."}
    Returns: {"token": "...", "message": "..."}
    The token is a UUID valid for 24 hours.
    """
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    password = body.get("password", "")
    if not password:
        raise HTTPException(status_code=400, detail="password is required")

    hashed = hashlib.sha256(password.encode()).hexdigest()
    if hashed != PASSWORD_HASH:
        raise HTTPException(status_code=401, detail="Invalid password")

    token = str(uuid.uuid4())
    valid_tokens[token] = time.time()

    return {"token": token, "message": "Login successful"}


@app.post("/api/auth/verify")
async def verify(request: Request):
    """Check whether the provided Bearer token is still valid."""
    valid = check_auth_header(request)
    return {"valid": valid, "message": "Token is valid" if valid else "Token is invalid or expired"}


# ═══════════════════════════════════════════════════════════════════════════
#  CHAT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════


@app.post("/api/chat")
async def chat(request: Request):
    """Synchronous chat with JIMMY via Claude CLI.

    Body: {"prompt": "...", "cwd": "/optional/working/dir"}
    Returns: {"response": "...", "error": "...", "returncode": 0}
    """
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    prompt = body.get("prompt", "")
    cwd = body.get("cwd")

    if not prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    # Validate optional cwd
    resolved_cwd = None
    if cwd:
        try:
            resolved_cwd = str(Path(cwd).resolve())
        except Exception:
            resolved_cwd = BASE_DIR

    result = run_claude(prompt, resolved_cwd)

    # Truncate response if very large
    stdout = result.stdout
    stderr = result.stderr
    truncated = False
    if len(stdout) > 50000:
        stdout = stdout[:50000] + "\n\n... [truncated at 50000 chars]"
        truncated = True

    return {
        "response": stdout,
        "error": stderr[:5000] if stderr else "",
        "returncode": result.returncode,
        "truncated": truncated,
    }


# ─── SSE Streaming Chat ────────────────────────────────────────────────────


@app.post("/api/chat/stream")
async def chat_stream_sse(request: Request):
    """SSE streaming chat via POST.

    Returns a Server-Sent Events stream of Claude CLI output.
    Useful for frontends that prefer SSE over WebSocket.

    Body: {"prompt": "..."}
    Auth: Bearer token in Authorization header.
    """
    if not check_auth_header(request):
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    try:
        body = await request.json()
    except json.JSONDecodeError:
        return JSONResponse(status_code=400, content={"detail": "Invalid JSON body"})

    prompt = body.get("prompt", "")
    if not prompt:
        return JSONResponse(status_code=400, content={"detail": "prompt is required"})

    async def generate():
        cmd = ["claude", "--dangerously-skip-permissions", "-p", prompt]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=BASE_DIR,
            env={**os.environ, **ENV},
        )

        try:
            while True:
                line = await proc.stdout.readline()
                if not line:
                    break
                yield f"data: {json.dumps({'token': line.decode('utf-8', errors='replace')})}\n\n"
        except Exception:
            if proc.returncode is None:
                proc.kill()

        await proc.wait()
        yield f"data: {json.dumps({'done': True, 'code': proc.returncode})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.websocket("/api/chat/stream")
async def chat_stream(websocket: WebSocket):
    """WebSocket streaming chat.

    Protocol:
        1. Client connects.
        2. Client sends:  {"token": "<uuid>"}
        3. Server validates token. If invalid, sends error and closes.
        4. Loop:
           Client sends:  {"prompt": "..."}  OR  plain text
           Server streams:  {"type": "token", "content": "...word..."}
           Server finishes:  {"type": "done", "full_output": "...", ...}
        5. Client disconnects or sends {"type": "close"} to end.
    """
    await websocket.accept()
    logger.info("WebSocket client connected to /api/chat/stream")

    # -- Step 1: Auth --
    try:
        auth_msg = await asyncio.wait_for(websocket.receive_text(), timeout=10.0)
    except asyncio.TimeoutError:
        await websocket.send_json({"type": "error", "message": "Authentication timeout. Send token within 10s."})
        await websocket.close(1008)
        return
    except WebSocketDisconnect:
        return

    try:
        auth_data = json.loads(auth_msg)
        token = auth_data.get("token", "")
    except (json.JSONDecodeError, AttributeError):
        token = ""

    if not verify_token(token):
        await websocket.send_json({"type": "error", "message": "Unauthorized. Invalid or expired token."})
        await websocket.close(1008)
        return

    await websocket.send_json({"type": "auth_ok", "message": "Authenticated. Send prompts to chat."})

    # -- Step 2: Chat loop --
    try:
        while True:
            raw = await websocket.receive_text()

            # Allow graceful close
            if raw.strip() == '{"type":"close"}' or raw.strip() == "close":
                break

            try:
                msg = json.loads(raw)
                prompt = msg.get("prompt", raw)
            except json.JSONDecodeError:
                prompt = raw

            if not prompt:
                await websocket.send_json({"type": "error", "message": "Empty prompt"})
                continue

            # Spawn Claude CLI as an async subprocess and stream stdout
            cmd = ["claude", "--dangerously-skip-permissions", "-p", prompt]
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=BASE_DIR,
                    env={**os.environ, **ENV},
                )
            except FileNotFoundError:
                await websocket.send_json({"type": "error", "message": "Claude CLI not found on server."})
                continue
            except Exception as e:
                await websocket.send_json({"type": "error", "message": f"Failed to spawn Claude: {e}"})
                continue

            # Stream stdout tokens
            full_output = ""
            try:
                while True:
                    line_bytes = await asyncio.wait_for(proc.stdout.readline(), timeout=300.0)
                    if not line_bytes:
                        break
                    decoded = line_bytes.decode("utf-8", errors="replace")
                    full_output += decoded
                    await websocket.send_json({"type": "token", "content": decoded})
            except asyncio.TimeoutError:
                await websocket.send_json({"type": "error", "message": "Claude CLI timed out (300s)"})
                proc.kill()
            except Exception as e:
                await websocket.send_json({"type": "error", "message": f"Stream error: {e}"})
                if proc.returncode is None:
                    proc.kill()

            # Collect stderr
            stderr_output = ""
            try:
                if proc.stderr:
                    stderr_data = await proc.stderr.read()
                    stderr_output = stderr_data.decode("utf-8", errors="replace")
            except Exception:
                pass

            await proc.wait()

            await websocket.send_json({
                "type": "done",
                "full_output": full_output,
                "stderr": stderr_output[:5000] if stderr_output else "",
                "returncode": proc.returncode,
            })

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({"type": "error", "message": f"Internal error: {e}"})
        except Exception:
            pass


# ─── File Quick View ──────────────────────────────────────────────────────


@app.post("/api/chat/file")
async def chat_file(request: Request):
    """Quick view a file's contents (like `cat` in chat).

    Body: {"path": "relative/path/to/file"}
    Path is relative to BASE_DIR (~/AIproject).
    Content is limited to 50KB for performance.
    """
    if not check_auth_header(request):
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    try:
        body = await request.json()
    except json.JSONDecodeError:
        return JSONResponse(status_code=400, content={"detail": "Invalid JSON body"})

    filepath = body.get("path", "")
    if not filepath:
        return JSONResponse(status_code=400, content={"error": "path is required"})

    full_path = Path(BASE_DIR) / filepath
    if not str(full_path.resolve()).startswith(str(Path(BASE_DIR).resolve())):
        return JSONResponse(status_code=403, content={"error": "Path traversal blocked"})

    if not full_path.exists():
        return JSONResponse(status_code=404, content={"error": "File not found"})

    try:
        content = full_path.read_text()[:50000]  # max 50KB
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error reading file: {e}"})

    return {"path": filepath, "content": content, "size": len(content)}


# ═══════════════════════════════════════════════════════════════════════════
#  AGENT MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════


@app.post("/api/agent/spawn")
async def agent_spawn(request: Request):
    """Spawn a team member as a background Claude agent process.

    Body: {"agent": "salmon", "prompt": "write a TikTok script about ..."}

    The agent's CLAUDE.md is injected as system context so Claude
    adopts the correct persona.

    Returns: {"pid": 12345, "agent": "salmon", "status": "running", "started": ...}
    """
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    agent_name = body.get("agent", "").lower().strip()
    prompt = body.get("prompt", "").strip()

    if not agent_name:
        raise HTTPException(status_code=400, detail="agent name is required")
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt is required")

    agent_file = os.path.join(TEAM_DIR, agent_name, "CLAUDE.md")
    if not os.path.exists(agent_file):
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_name}' not found. Available: {get_available_agents()}",
        )

    # Load agent context for persona injection
    try:
        with open(agent_file, "r", encoding="utf-8") as f:
            agent_context = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading agent profile: {e}")

    full_prompt = (
        f"[SYSTEM: You are {agent_name.upper()}.\n"
        f"Your identity and expertise:\n\n{agent_context}\n\n"
        f"Respond as {agent_name.upper()} would — stay in character, use your expertise.\n"
        f"---\n\nUSER: {prompt}]"
    )

    cmd = ["claude", "--dangerously-skip-permissions", "-p", full_prompt]
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=BASE_DIR,
            env={**os.environ, **ENV},
        )
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Claude CLI not found on server.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to spawn agent: {e}")

    now = time.time()
    running_agents[proc.pid] = {
        "name": agent_name,
        "prompt": prompt,
        "started": now,
        "proc": proc,
    }

    logger.info(f"Spawned agent '{agent_name}' (PID {proc.pid}): {prompt[:80]}...")

    return {
        "pid": proc.pid,
        "agent": agent_name,
        "status": "running",
        "started": now,
        "started_iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now)),
        "prompt": prompt,
        "prompt_preview": prompt[:100] + ("..." if len(prompt) > 100 else ""),
        "model": ENV.get("ANTHROPIC_MODEL", "unknown"),
        "cwd": BASE_DIR,
        "running_for_seconds": 0.0,
        "message": f"{agent_name.upper()} (PID {proc.pid}) is now running in the background. Use GET /api/agent/list or GET /api/agent/status to check status.",
    }


def get_available_agents() -> List[str]:
    """Return a list of team member slugs that have CLAUDE.md profiles."""
    if not os.path.isdir(TEAM_DIR):
        return []
    agents = []
    for entry in sorted(os.listdir(TEAM_DIR)):
        if os.path.isdir(os.path.join(TEAM_DIR, entry)) and os.path.exists(
            os.path.join(TEAM_DIR, entry, "CLAUDE.md")
        ):
            agents.append(entry)
    return agents


@app.get("/api/agent/list")
async def agent_list():
    """List all tracked agents with their status and partial output.

    Dead processes are cleaned from the tracking dict automatically.
    """
    results = []
    dead_pids = []

    for pid, info in dict(running_agents).items():
        proc: subprocess.Popen = info["proc"]
        alive = proc.poll() is None

        # Double-check with psutil
        if alive:
            try:
                p = psutil.Process(pid)
                alive = p.is_running() and p.status() not in (
                    psutil.STATUS_ZOMBIE,
                    psutil.STATUS_DEAD,
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                alive = False

        entry = {
            "pid": pid,
            "name": info["name"],
            "prompt": info["prompt"],
            "started": info["started"],
            "running_for_seconds": round(time.time() - info["started"], 1),
        }

        if alive:
            # Attempt non-blocking read of available output
            partial_out = ""
            partial_err = ""
            try:
                if proc.stdout and hasattr(proc.stdout, "readable") and proc.stdout.readable():
                    import select
                    if hasattr(select, "poll"):
                        poll = select.poll()
                        poll.register(proc.stdout, select.POLLIN)
                        if poll.poll(0):
                            partial_out = proc.stdout.read(2000)
            except Exception:
                pass
            try:
                if proc.stderr and hasattr(proc.stderr, "readable") and proc.stderr.readable():
                    import select
                    if hasattr(select, "poll"):
                        poll = select.poll()
                        poll.register(proc.stderr, select.POLLIN)
                        if poll.poll(0):
                            partial_err = proc.stderr.read(1000)
            except Exception:
                pass

            entry["status"] = "running"
            entry["partial_output"] = partial_out
            entry["partial_error"] = partial_err
        else:
            dead_pids.append(pid)
            entry["status"] = "completed"
            entry["returncode"] = proc.poll()

        results.append(entry)

    # Clean up dead processes
    for pid in dead_pids:
        del running_agents[pid]

    return {"agents": results, "count": len(results), "dead_cleaned": len(dead_pids)}


@app.get("/api/agent/status")
async def agent_status():
    """Return all running agents with detailed status info.

    Shows only currently-running agents (completed ones are excluded).
    Includes PID, name, prompt, started time, running duration,
    and partial output preview.
    """
    results = []
    dead_pids = []

    for pid, info in dict(running_agents).items():
        proc: subprocess.Popen = info["proc"]
        alive = proc.poll() is None

        # Double-check with psutil
        if alive:
            try:
                p = psutil.Process(pid)
                alive = p.is_running() and p.status() not in (
                    psutil.STATUS_ZOMBIE,
                    psutil.STATUS_DEAD,
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                alive = False

        duration = round(time.time() - info["started"], 1)

        entry = {
            "pid": pid,
            "name": info["name"],
            "prompt": info["prompt"],
            "prompt_preview": info["prompt"][:100] + ("..." if len(info["prompt"]) > 100 else ""),
            "started": info["started"],
            "started_iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(info["started"])),
            "running_for_seconds": duration,
        }

        if alive:
            # Non-blocking read of available output
            partial_out = ""
            partial_err = ""
            try:
                if proc.stdout and hasattr(proc.stdout, "readable") and proc.stdout.readable():
                    import select
                    if hasattr(select, "poll"):
                        poll = select.poll()
                        poll.register(proc.stdout, select.POLLIN)
                        if poll.poll(0):
                            partial_out = proc.stdout.read(2000)
            except Exception:
                pass
            try:
                if proc.stderr and hasattr(proc.stderr, "readable") and proc.stderr.readable():
                    import select
                    if hasattr(select, "poll"):
                        poll = select.poll()
                        poll.register(proc.stderr, select.POLLIN)
                        if poll.poll(0):
                            partial_err = proc.stderr.read(1000)
            except Exception:
                pass

            entry["status"] = "running"
            entry["partial_output"] = partial_out
            entry["partial_output_preview"] = partial_out[:500] + ("..." if len(partial_out) > 500 else "")
            entry["partial_error"] = partial_err
            results.append(entry)
        else:
            dead_pids.append(pid)

    # Clean up dead processes
    for pid in dead_pids:
        del running_agents[pid]

    return {
        "agents": results,
        "count": len(results),
        "dead_cleaned": len(dead_pids),
    }


@app.post("/api/agent/{agent_id}/stop")
async def agent_stop(agent_id: int):
    """Stop a running agent by PID.

    Sends SIGTERM first, then SIGKILL after 5s if still alive.
    Also terminates child processes.
    """
    pid = agent_id

    if pid in running_agents:
        info = running_agents[pid]
        proc = info["proc"]
    else:
        # Try to kill by PID even if untracked
        try:
            p = psutil.Process(pid)
            p.terminate()
            gone, alive = psutil.wait_procs([p], timeout=3)
            if alive:
                for ap in alive:
                    ap.kill()
            return {
                "pid": pid,
                "status": "killed",
                "note": "Process was not tracked by the server but has been terminated.",
            }
        except psutil.NoSuchProcess:
            raise HTTPException(status_code=404, detail=f"No process or agent found with PID {pid}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    try:
        duration = round(time.time() - info["started"], 1)

        # Try graceful termination
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=3)

        # Kill child processes via psutil
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            parent.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

        del running_agents[pid]
        logger.info(f"Stopped agent '{info['name']}' (PID {pid}) after {duration}s")

        return {
            "pid": pid,
            "name": info["name"],
            "status": "stopped",
            "running_duration_seconds": duration,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping agent: {e}")


# ═══════════════════════════════════════════════════════════════════════════
#  BASH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════


@app.post("/api/bash")
async def bash_execute(request: Request):
    """Execute a whitelisted shell command.

    Body: {"command": "git status", "cwd": "/home/admin_jacob/AIproject", "timeout": 30}

    Only the *first word* of the command must be in the whitelist.
    Timeout is capped at 120 seconds.

    Note: shell=True is used to support pipes and redirects.
    The whitelist check on the first word provides a basic safety layer.
    """
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    command = body.get("command", "").strip()
    cwd = body.get("cwd", BASE_DIR)
    timeout = min(int(body.get("timeout", 30)), 120)

    if not command:
        raise HTTPException(status_code=400, detail="command is required")

    # Parse first word for whitelist check
    try:
        parts = shlex.split(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Cannot parse command: {e}")

    cmd_base = parts[0] if parts else ""
    if cmd_base not in WHITELIST_COMMANDS:
        allowed = ", ".join(sorted(WHITELIST_COMMANDS))
        raise HTTPException(
            status_code=403,
            detail=f"Command '{cmd_base}' is not whitelisted. Allowed: {allowed}",
        )

    # Resolve working directory
    try:
        resolved_cwd = str(Path(cwd).expanduser().resolve())
        if not resolved_cwd.startswith(str(Path(BASE_DIR).resolve())) and cmd_base not in (
            "pwd", "whoami", "echo", "date", "df", "free", "which"
        ):
            # Allow reading system info but restrict file operations
            if cmd_base in ("ls", "cat", "find", "grep", "git", "du", "head", "tail", "wc", "sort", "mkdir", "cp", "mv", "touch", "chmod", "chown"):
                # For these commands, restrict to BASE_DIR
                pass  # Will enforce below with resolved_cwd check
            resolved_cwd = BASE_DIR
    except Exception:
        resolved_cwd = BASE_DIR

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=resolved_cwd,
            timeout=timeout,
            env={**os.environ, "PATH": ENV["PATH"], "HOME": ENV["HOME"]},
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail=f"Command timed out after {timeout}s")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Truncate large outputs
    stdout = result.stdout
    stderr = result.stderr
    truncated = False
    if len(stdout) > 50000:
        stdout = stdout[:50000] + "\n\n... [truncated at 50000 chars]"
        truncated = True
    if len(stderr) > 10000:
        stderr = stderr[:10000] + "\n\n... [truncated at 10000 chars]"
        truncated = True

    return {
        "command": command,
        "cwd": resolved_cwd,
        "stdout": stdout,
        "stderr": stderr,
        "returncode": result.returncode,
        "truncated": truncated,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  FILE OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════


@app.get("/api/files")
async def files_list_root():
    """List ~/AIproject as a directory tree."""
    tree = build_directory_tree(BASE_DIR)
    return {
        "path": BASE_DIR,
        "type": "directory",
        "tree": tree,
        "count": len(tree),
    }


@app.get("/api/files/{file_path:path}")
async def files_read(file_path: str):
    """Read a file or list a directory.

    If the path points to a file, returns its content.
    If the path points to a directory, returns a tree listing.
    Path is relative to ~/AIproject.
    """
    if not file_path:
        return await files_list_root()

    full_path = sanitize_path(file_path)

    if os.path.isdir(full_path):
        tree = build_directory_tree(full_path)
        return {
            "path": file_path,
            "type": "directory",
            "tree": tree,
            "count": len(tree),
        }

    if os.path.isfile(full_path):
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except PermissionError:
            raise HTTPException(status_code=403, detail="Permission denied reading this file")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file: {e}")

        stat = os.stat(full_path)
        return {
            "path": file_path,
            "type": "file",
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "content": content,
        }

    raise HTTPException(status_code=404, detail=f"Path '{file_path}' not found")


@app.put("/api/files/{file_path:path}")
async def files_write(file_path: str, request: Request):
    """Write or create a file. Creates parent directories if needed.

    Body: {"content": "file content here"}
    Path is relative to ~/AIproject.
    """
    if not file_path:
        raise HTTPException(status_code=400, detail="file_path is required")

    full_path = sanitize_path(file_path)

    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    content = body.get("content", "")
    if content is None:
        content = ""

    # If writing binary, support base64
    is_binary = body.get("binary", False)
    if is_binary:
        import base64
        try:
            content = base64.b64decode(content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 content: {e}")

    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        mode = "wb" if is_binary else "w"
        encoding_kw = {} if is_binary else {"encoding": "utf-8"}
        with open(full_path, mode, **encoding_kw) as f:
            f.write(content)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied writing this file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing file: {e}")

    file_size = len(content)
    logger.info(f"Wrote {file_size} bytes to {full_path}")

    return {"path": file_path, "written": True, "size": file_size, "binary": is_binary}


@app.delete("/api/files/{file_path:path}")
async def files_delete(file_path: str):
    """Delete a file or an empty directory.

    Non-empty directories cannot be deleted through this endpoint.
    Path is relative to ~/AIproject.
    """
    if not file_path:
        raise HTTPException(status_code=400, detail="file_path is required")

    full_path = sanitize_path(file_path)

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail=f"Path '{file_path}' not found")

    try:
        if os.path.isfile(full_path) or os.path.islink(full_path):
            os.remove(full_path)
            logger.info(f"Deleted file: {full_path}")
            return {"path": file_path, "deleted": True, "type": "file"}

        if os.path.isdir(full_path):
            children = os.listdir(full_path)
            if not children:
                os.rmdir(full_path)
                logger.info(f"Deleted empty directory: {full_path}")
                return {"path": file_path, "deleted": True, "type": "empty_directory"}
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Directory not empty ({len(children)} items). Delete files individually or use 'rm -rf' via /api/bash.",
                )

        raise HTTPException(status_code=400, detail=f"Unsupported path type: {type(full_path)}")

    except HTTPException:
        raise
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied deleting this path")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════════════
#  TEAM ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════


@app.get("/api/team")
async def team_list():
    """Return parsed team data from Kvasir/team/*/CLAUDE.md files.

    Each team member's CLAUDE.md is parsed for name, role, theme, mentor,
    human, birth date, and description. The result is sorted alphabetically.
    """
    if not os.path.isdir(TEAM_DIR):
        raise HTTPException(status_code=404, detail="Team directory not found")

    team_members: List[Dict[str, Any]] = []
    errors: List[Dict[str, str]] = []

    for entry in sorted(os.listdir(TEAM_DIR)):
        member_dir = os.path.join(TEAM_DIR, entry)
        claude_file = os.path.join(member_dir, "CLAUDE.md")

        if not os.path.isdir(member_dir) or not os.path.isfile(claude_file):
            continue

        try:
            with open(claude_file, "r", encoding="utf-8") as f:
                content = f.read()
            member = parse_team_member(entry, content)
            team_members.append(member)
        except Exception as e:
            logger.warning(f"Error parsing team member '{entry}': {e}")
            errors.append({"slug": entry, "error": str(e)})
            team_members.append({
                "slug": entry,
                "name": entry,
                "role": "Unknown",
                "error": str(e),
            })

    return {
        "team": team_members,
        "count": len(team_members),
        "errors": errors if errors else None,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  MEMORY SEARCH
# ═══════════════════════════════════════════════════════════════════════════


@app.get("/api/memory/search")
async def memory_search(request: Request, q: str = ""):
    """Search across team learnings.

    Searches Kvasir/team/*/learnings/*.md for the query string.
    Returns matching files with up to 5 context lines per file.
    Limited to 20 results per query.
    """
    if not check_auth_header(request):
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    if not q:
        return {"query": q, "count": 0, "results": []}

    results = []
    learnings_dir = Path(BASE_DIR) / "Kvasir" / "team"

    if not learnings_dir.exists():
        return {"query": q, "count": 0, "results": [], "note": "Team directory not found"}

    for md_file in learnings_dir.rglob("learnings/*.md"):
        try:
            content = md_file.read_text()
            if q.lower() in content.lower():
                lines = content.split('\n')
                matches = [l.strip() for l in lines if q.lower() in l.lower()][:5]
                results.append({
                    "file": str(md_file.relative_to(Path(BASE_DIR))),
                    "team": md_file.parent.parent.name,
                    "matches": matches,
                })
        except Exception:
            pass

    return {"query": q, "count": len(results), "results": results[:20]}


# ═══════════════════════════════════════════════════════════════════════════
#  SYSTEM ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════


@app.get("/api/system")
async def system_info():
    """Return system metrics: CPU, RAM, disk, model config, platform info."""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        load_avg = psutil.getloadavg()

        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()

        disk = psutil.disk_usage("/")

        # Network I/O (summary)
        net = psutil.net_io_counters()

        # Processes
        proc_count = len(psutil.pids())

        return {
            "cpu": {
                "percent": cpu_percent,
                "count": {"physical": psutil.cpu_count(logical=False), "logical": cpu_count},
                "freq_mhz": round(cpu_freq.current, 1) if cpu_freq else None,
                "load_avg": {
                    "1min": round(load_avg[0], 2),
                    "5min": round(load_avg[1], 2),
                    "15min": round(load_avg[2], 2),
                },
            },
            "ram": {
                "total_gb": round(ram.total / (1024**3), 2),
                "used_gb": round(ram.used / (1024**3), 2),
                "available_gb": round(ram.available / (1024**3), 2),
                "percent": ram.percent,
                "swap_total_gb": round(swap.total / (1024**3), 2),
                "swap_used_gb": round(swap.used / (1024**3), 2),
                "swap_percent": swap.percent,
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent": disk.percent,
            },
            "model": {
                "default": ENV["ANTHROPIC_MODEL"],
                "opus": ENV["ANTHROPIC_DEFAULT_OPUS_MODEL"],
                "sonnet": ENV["ANTHROPIC_DEFAULT_SONNET_MODEL"],
                "haiku": ENV["ANTHROPIC_DEFAULT_HAIKU_MODEL"],
                "subagent": ENV["CLAUDE_CODE_SUBAGENT_MODEL"],
                "effort": ENV["CLAUDE_CODE_EFFORT_LEVEL"],
            },
            "platform": {
                "hostname": os.uname().nodename,
                "system": os.uname().sysname,
                "release": os.uname().release,
                "machine": os.uname().machine,
                "python": sys.version.split()[0],
            },
            "network": {
                "bytes_sent_mb": round(net.bytes_sent / (1024**2), 1),
                "bytes_recv_mb": round(net.bytes_recv / (1024**2), 1),
                "packets_sent": net.packets_sent,
                "packets_recv": net.packets_recv,
            },
            "server": {
                "started_at": time.time(),
                "running_agents_count": len(running_agents),
                "total_processes": proc_count,
                "base_dir": BASE_DIR,
            },
        }
    except Exception as e:
        logger.exception("Error collecting system info")
        raise HTTPException(status_code=500, detail=f"Error collecting system info: {e}")


# ═══════════════════════════════════════════════════════════════════════════
#  HEALTH & ROOT
# ═══════════════════════════════════════════════════════════════════════════


# ─── Static Frontend ───────────────────────────────────────────────────────────
# Serve the built frontend at root. API routes take priority over static files.
@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": time.time()}


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════

# Static frontend — must be LAST (after all routes)
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    import sys

    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    logger.info("=" * 60)
    logger.info("JACOB Command Center starting...")
    logger.info(f"  Host: {host}")
    logger.info(f"  Port: {port}")
    logger.info(f"  Base dir: {BASE_DIR}")
    logger.info(f"  Team dir: {TEAM_DIR}")
    logger.info(f"  Default model: {ENV['ANTHROPIC_MODEL']}")
    logger.info(f"  Auth: {'ENABLED' if PASSWORD_HASH else 'DISABLED (no hash set)'}")
    logger.info(f"  API docs: http://{host}:{port}/docs")
    logger.info("=" * 60)

    uvicorn.run(app, host=host, port=port, log_level="info")
