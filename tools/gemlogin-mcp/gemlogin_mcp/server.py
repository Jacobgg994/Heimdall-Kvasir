"""GemLogin MCP server.

Wraps the GemLogin antidetect browser's local Express API (default
http://localhost:1010) as MCP tools, resources, and prompts so Claude Code,
Claude Desktop, Cursor, and any other MCP-compatible client can drive
browser profiles by natural language.
"""
from __future__ import annotations

import asyncio
import copy
from difflib import SequenceMatcher
import json
import os
import unicodedata
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

BASE: str = os.environ.get("GEMLOGIN_BASE", "http://localhost:1010")
TIMEOUT: float = float(os.environ.get("GEMLOGIN_TIMEOUT", "60"))

# Cloud webhook config (app.gemlogin.io/api/v2/execscript).
# Auth is the per-device `token` field IN the request body — not a Bearer
# header. Each device's webhook page on the dashboard shows the four
# customer-specific values: device_id, soft_id, token (+ workflow_id per
# script you want to fire). Bearer is optional and ignored by the server.
CLOUD_BASE: str = os.environ.get("GEMLOGIN_CLOUD_BASE", "https://app.gemlogin.io")
CLOUD_BEARER: str = os.environ.get("GEMLOGIN_CLOUD_BEARER", "")   # optional
CLOUD_DEVICE_ID: str = os.environ.get("GEMLOGIN_CLOUD_DEVICE_ID", "")
CLOUD_SOFT_ID: str = os.environ.get("GEMLOGIN_CLOUD_SOFT_ID", "")
CLOUD_TOKEN: str = os.environ.get("GEMLOGIN_CLOUD_TOKEN", "")

mcp = FastMCP("gemlogin")

_client: httpx.AsyncClient | None = None
_cloud_client: httpx.AsyncClient | None = None

_SCRIPT_ID_KEYS = ("id", "workflow_id", "workflowId", "_id")
_SCRIPT_NAME_KEYS = ("name", "label", "title", "script_name")
_SENSITIVE_HINTS = (
    "token",
    "secret",
    "password",
    "pass",
    "apikey",
    "api_key",
    "bearer",
    "auth",
    "session",
    "cookie",
    "key",
    "api",
)


def _client_get() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(base_url=BASE, timeout=TIMEOUT)
    return _client


def _cloud_client_get() -> httpx.AsyncClient:
    global _cloud_client
    if _cloud_client is None:
        headers = {"Content-Type": "application/json"}
        if CLOUD_BEARER:
            headers["Authorization"] = f"Bearer {CLOUD_BEARER}"
        _cloud_client = httpx.AsyncClient(
            base_url=CLOUD_BASE, timeout=TIMEOUT, headers=headers
        )
    return _cloud_client


async def _get(path: str) -> Any:
    r = await _client_get().get(path)
    r.raise_for_status()
    return r.json()


async def _post(path: str, body: dict[str, Any]) -> Any:
    r = await _client_get().post(path, json=body)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return {"success": False, "status_code": r.status_code, "text": r.text[:500]}


def _normalize_text(s: str) -> str:
    return " ".join((s or "").strip().lower().split())


def _tokens(s: str) -> list[str]:
    buf = []
    for ch in _normalize_text(s):
        cat = unicodedata.category(ch)
        keep = cat[0] in ("L", "N", "M")
        buf.append(ch if keep else " ")
    return [tok for tok in "".join(buf).split() if tok]


def _script_id(script: dict[str, Any]) -> str | None:
    for k in _SCRIPT_ID_KEYS:
        v = script.get(k)
        if v:
            return str(v)
    return None


def _script_names(script: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for k in _SCRIPT_NAME_KEYS:
        v = script.get(k)
        if isinstance(v, str) and v.strip():
            names.append(v.strip())
    return names


def _best_script_match_score(script_name: str, script: dict[str, Any]) -> tuple[float, str]:
    target = _normalize_text(script_name)
    target_tokens = _tokens(script_name)
    names = _script_names(script)
    if not names:
        return 0.0, ""

    best_name = names[0]
    best_score = 0.0
    for name in names:
        norm_name = _normalize_text(name)
        cand_tokens = _tokens(name)
        if norm_name == target:
            return 1.0, name
        seq_score = SequenceMatcher(None, target, norm_name).ratio()

        token_score = 0.0
        if target_tokens and cand_tokens:
            per_target = []
            for t in target_tokens:
                per_target.append(
                    max(SequenceMatcher(None, t, c).ratio() for c in cand_tokens)
                )
            token_score = sum(per_target) / len(per_target)

        score = max(seq_score, token_score * 0.85 + seq_score * 0.15)

        # If the query contains non-ASCII text (e.g. Thai) but candidate has none,
        # down-rank the candidate to avoid English-only false positives.
        query_has_non_ascii = any(not tok.isascii() for tok in target_tokens)
        cand_has_non_ascii = any(not tok.isascii() for tok in cand_tokens)
        if query_has_non_ascii and not cand_has_non_ascii:
            score *= 0.1

        if score > best_score:
            best_score = score
            best_name = name
    return best_score, best_name


def _looks_sensitive(*hints: str) -> bool:
    hay = " ".join(_normalize_text(h) for h in hints if h)
    return any(token in hay for token in _SENSITIVE_HINTS)


def _mask_script_defaults(script: dict[str, Any], include_sensitive_defaults: bool) -> dict[str, Any]:
    if include_sensitive_defaults:
        return script

    out = copy.deepcopy(script)
    params = out.get("parameters")
    if not isinstance(params, list):
        return out

    for p in params:
        if not isinstance(p, dict):
            continue
        if "defaultValue" not in p:
            continue
        name = str(p.get("name", ""))
        label = str(p.get("label", ""))
        desc = str(p.get("description", ""))
        if _looks_sensitive(name, label, desc):
            p["defaultValue"] = "***masked***"
    return out


async def _list_scripts_raw() -> list[dict[str, Any]]:
    r = await _get("/api/scripts")
    return r.get("data", [])


async def _resolve_script_by_name(
    script_name: str, require_exact_script_name: bool
) -> tuple[str, str, float] | None:
    scripts = await _list_scripts_raw()
    target = _normalize_text(script_name)
    exact_matches: list[tuple[str, str]] = []
    best: tuple[float, str, str] | None = None
    for s in scripts:
        sid = _script_id(s)
        if not sid:
            continue

        names = _script_names(s)
        for n in names:
            if _normalize_text(n) == target:
                exact_matches.append((sid, n))

        score, matched_name = _best_script_match_score(script_name, s)
        if best is None or score > best[0]:
            best = (score, sid, matched_name)

    if len(exact_matches) > 1:
        candidates = ", ".join(f"{sid}:{name}" for sid, name in exact_matches[:10])
        raise RuntimeError(
            "ambiguous script_name exact match; multiple workflows share this name. "
            f"Use script_id instead. Candidates: {candidates}"
        )
    if len(exact_matches) == 1:
        sid, name = exact_matches[0]
        return sid, name, 1.0

    if best is None:
        return None
    if require_exact_script_name:
        raise RuntimeError(
            "script_name exact match not found. Use the exact workflow name or provide script_id."
        )
    return best[1], best[2], best[0]


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
async def gemlogin_status() -> dict:
    """Return the GemLogin server status: type, port, cloudMode, feature flags,
    activeBrowsers count, and uptime in seconds."""
    return await _get("/api/status")


@mcp.tool()
async def gemlogin_list_profiles() -> list[dict]:
    """List every GemLogin browser profile (id, name, browser_type,
    browser_version, group_id, proxy, profile_path, note)."""
    r = await _get("/api/profiles")
    return r.get("data", [])


@mcp.tool()
async def gemlogin_get_profile(profile_id: int) -> dict:
    """Get the full detail for one profile by id, including created_at."""
    r = await _get(f"/api/profile/{profile_id}")
    return r.get("data", {})


@mcp.tool()
async def gemlogin_start_profile(profile_id: int) -> dict:
    """Start a browser profile. Returns a dict with:
      - profile_id
      - browser_location: absolute path to the Chromium binary
      - remote_debugging_address: "127.0.0.1:PORT" — connect Puppeteer,
        Playwright, or Selenium to this for full Chrome DevTools Protocol
        automation.
      - driver_path: bundled WebDriver binary (Selenium-compatible).

    The call may take 5-15 seconds while the browser bootstraps."""
    r = await _get(f"/api/profiles/start/{profile_id}")
    if not r.get("success"):
        raise RuntimeError(f"gemlogin start failed: {r}")
    return r["data"]


@mcp.tool()
async def gemlogin_stop_profile(profile_id: int) -> dict:
    """Close a running browser profile. Idempotent — safe to call on an
    already-closed profile."""
    return await _get(f"/api/profiles/close/{profile_id}")


@mcp.tool()
async def gemlogin_list_groups() -> list[dict]:
    """List profile groups (e.g. 'Hotmail', 'Facebook')."""
    r = await _get("/api/groups")
    return r.get("data", [])


@mcp.tool()
async def gemlogin_list_scripts(include_sensitive_defaults: bool = False) -> list[dict]:
    """List installed GemLogin automation scripts and their parameter
    schemas (name, label, type, defaultValue, required, description).

    By default, likely-secret `defaultValue` fields are masked."""
    scripts = await _list_scripts_raw()
    return [_mask_script_defaults(s, include_sensitive_defaults) for s in scripts]


@mcp.tool()
async def gemlogin_browser_versions() -> list[dict]:
    """List Chromium versions available for creating new profiles."""
    r = await _get("/api/browser_versions")
    return r.get("data", [])


@mcp.tool()
async def gemlogin_find_script(script_name: str, top_k: int = 5) -> list[dict]:
    """Find the closest matching local automation scripts by name."""
    scripts = await _list_scripts_raw()
    ranked: list[tuple[float, dict[str, Any], str]] = []
    for s in scripts:
        score, matched_name = _best_script_match_score(script_name, s)
        ranked.append((score, s, matched_name))

    ranked.sort(key=lambda x: x[0], reverse=True)
    top: list[dict[str, Any]] = []
    for score, script, matched_name in ranked[: max(1, top_k)]:
        top.append(
            {
                "id": _script_id(script),
                "name": script.get("name"),
                "matched_name": matched_name,
                "score": round(score, 4),
                "parameters": _mask_script_defaults(script, False).get("parameters", []),
            }
        )
    return top


@mcp.tool()
async def gemlogin_execute_local_script(
    profile_id: list[int | str],
    script_id: str | None = None,
    script_name: str | None = None,
    parameters: dict | None = None,
    close_browser: bool = False,
    require_exact_script_name: bool = True,
    retries: int = 1,
    retry_delay_seconds: float = 1.0,
) -> dict:
    """Execute a GemLogin local automation script via
    `POST /api/scripts/execute/{id}` with per-profile retries.

    Pass `script_id` directly, or provide `script_name` to resolve.
    With `require_exact_script_name=True` (default), fuzzy fallback is disabled.
    """
    if not profile_id:
        raise RuntimeError("profile_id must include at least one profile id")
    if not script_id and not script_name:
        raise RuntimeError("provide either script_id or script_name")

    resolved_name = None
    matched_score = None
    if not script_id:
        resolved = await _resolve_script_by_name(
            script_name or "", require_exact_script_name=require_exact_script_name
        )
        if not resolved:
            raise RuntimeError(f"no script found for name '{script_name}'")
        script_id, resolved_name, matched_score = resolved

    retries = max(1, retries)
    delay = max(0.0, retry_delay_seconds)

    results: list[dict[str, Any]] = []
    for pid in profile_id:
        pid_str = str(pid)
        last_execute: dict[str, Any] | None = None
        execute_ok = False
        attempts = 0

        for attempts in range(1, retries + 1):
            body: dict[str, Any] = {
                "profileId": [pid_str],
                "closeBrowser": close_browser,
            }
            if parameters is not None:
                body["parameters"] = parameters

            try:
                exec_resp = await _post(f"/api/scripts/execute/{script_id}", body)
                execute_ok = bool(exec_resp.get("success"))
                last_execute = exec_resp
            except Exception as e:
                last_execute = {"success": False, "error": str(e)}
                execute_ok = False

            if execute_ok:
                break
            if attempts < retries and delay > 0:
                await asyncio.sleep(delay)

        status: dict[str, Any] | None
        try:
            status = await _post(f"/api/scripts/check-status/{script_id}", {"profileId": pid_str})
        except Exception as e:
            status = {"error": str(e)}

        results.append(
            {
                "profile_id": pid,
                "attempts": attempts,
                "execute_success": execute_ok,
                "execute_response": last_execute,
                "is_running": bool(status.get("is_running")) if isinstance(status, dict) else None,
                "status_response": status,
            }
        )

    return {
        "script_id": script_id,
        "resolved_script_name": resolved_name,
        "matched_score": matched_score,
        "requested_profiles": profile_id,
        "retries": retries,
        "success_count": sum(1 for r in results if r["execute_success"]),
        "running_count": sum(1 for r in results if r.get("is_running")),
        "results": results,
    }


@mcp.tool()
async def gemlogin_check_local_script_status(script_id: str, profile_id: int | str) -> dict:
    """Check local script status for one profile via
    `POST /api/scripts/check-status/{id}`."""
    return await _post(f"/api/scripts/check-status/{script_id}", {"profileId": str(profile_id)})


@mcp.tool()
async def gemlogin_kill_local_script(script_id: str, profile_id: int | str) -> dict:
    """Stop local script execution for one profile via
    `POST /api/scripts/kill-execute/{id}`."""
    return await _post(f"/api/scripts/kill-execute/{script_id}", {"profileId": str(profile_id)})


# ---------------------------------------------------------------------------
# Cloud webhook tool (app.gemlogin.io/api/v2/execscript)
# ---------------------------------------------------------------------------

@mcp.tool()
async def gemlogin_cloud_execscript(
    profile_id: int | str | list[int | str],
    workflow_id: str,
    device_id: str | None = None,
    soft_id: str | None = None,
    token: str | None = None,
    parameter: dict | None = None,
    close_browser: bool | None = None,
    extra: dict | None = None,
) -> dict:
    """Trigger a cloud workflow on the GemLogin SaaS (app.gemlogin.io).

    Wraps `POST /api/v2/execscript`. Independent of the local :1010 API —
    the cloud routes the trigger to whichever GemLogin device is online
    and matches `device_id`. The body field `token` is the auth credential
    (not a Bearer header).

    Required values (per-customer; from the cloud dashboard's
    Automation / Webhook page):
      - device_id     env: GEMLOGIN_CLOUD_DEVICE_ID
      - soft_id       env: GEMLOGIN_CLOUD_SOFT_ID
      - token         env: GEMLOGIN_CLOUD_TOKEN

    Per-call:
      - profile_id    integer id of the target browser profile
      - workflow_id   script id from `gemlogin_list_scripts`
                      (e.g. `mmgCcRUkRyKPeAfrXeOQg`)
      - extra         dict merged into the body for workflow params

    Rate limit: 300 requests / minute (observed).
    Returns the parsed JSON response.
    """
    # profile_id accepts int, str, or a list — the cloud accepts arrays
    # (e.g. ["3","4","7"]) for fan-out to multiple profiles in one trigger.
    if isinstance(profile_id, list):
        norm_profile_id: Any = [str(p) for p in profile_id]
    else:
        norm_profile_id = profile_id

    body: dict[str, Any] = {
        "profile_id":  norm_profile_id,
        "workflow_id": workflow_id,
        "device_id":   device_id or CLOUD_DEVICE_ID,
        "soft_id":     soft_id   or CLOUD_SOFT_ID,
        "token":       token     or CLOUD_TOKEN,
    }
    if parameter is not None:
        body["parameter"] = parameter
    if close_browser is not None:
        body["close_browser"] = close_browser

    missing = [k for k, v in body.items() if not v and k != "profile_id"]
    if missing:
        raise RuntimeError(
            f"missing required fields: {missing}. Provide via env "
            f"(GEMLOGIN_CLOUD_DEVICE_ID / SOFT_ID / TOKEN) or as tool args."
        )
    if extra:
        body.update(extra)

    r = await _cloud_client_get().post("/api/v2/execscript", json=body)
    try:
        return r.json()
    except Exception:
        return {"success": False, "status_code": r.status_code, "text": r.text[:500]}


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

@mcp.resource("gemlogin://status")
async def res_status() -> str:
    """Current GemLogin server status (read-only snapshot)."""
    return json.dumps(await _get("/api/status"), indent=2)


@mcp.resource("gemlogin://profiles")
async def res_profiles() -> str:
    """Full list of profiles as JSON."""
    return json.dumps(await _get("/api/profiles"), indent=2)


@mcp.resource("gemlogin://profile/{pid}")
async def res_profile(pid: str) -> str:
    """One profile's detail by id."""
    return json.dumps(await _get(f"/api/profile/{pid}"), indent=2)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

@mcp.prompt()
def warm_profile(profile_id: int, minutes: int = 20) -> str:
    """Template prompt: warm-up flow for a single profile."""
    return (
        f"Use gemlogin_start_profile({profile_id}) to open the browser.\n"
        f"Connect Puppeteer (or Playwright) to the returned "
        f"remote_debugging_address.\n"
        f"Browse 3-5 neutral sites for about {minutes} minutes — gentle "
        f"scrolling, 2-5 clicks per session, no logins.\n"
        f"Then call gemlogin_stop_profile({profile_id}) to close cleanly."
    )


@mcp.prompt()
def post_to_group(group_name: str, content: str) -> str:
    """Template prompt: fan out a single piece of content across every
    profile in a named group."""
    return (
        f"1. Call gemlogin_list_groups to find the id of group '{group_name}'.\n"
        f"2. Call gemlogin_list_profiles and filter to that group_id.\n"
        f"3. For each profile id in the group:\n"
        f"   a. gemlogin_start_profile(id)\n"
        f"   b. Connect Puppeteer to remote_debugging_address.\n"
        f"   c. Post this content to the persona's target surface:\n"
        f"      <<<\n{content}\n>>>\n"
        f"   d. Capture the post URL.\n"
        f"   e. gemlogin_stop_profile(id)\n"
        f"4. Return a summary table: profile_id, post_url, status."
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the MCP server over stdio (default Claude Code / Desktop / Cursor
    transport)."""
    mcp.run()


if __name__ == "__main__":
    main()
