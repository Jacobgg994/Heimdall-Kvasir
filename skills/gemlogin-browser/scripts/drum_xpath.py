#!/usr/bin/env python3
"""
🥁 drum_xpath.py — Extract ALL interactive XPaths from a Facebook page via GemLogin CDP.

เชื่อมต่อ GemLogin browser profile ผ่าน Chrome DevTools Protocol (CDP)
แล้วเข้าไปที่ URL ที่กำหนด, scroll โหลด lazy content,
จากนั้น inject JavaScript ดึงทุก element ที่ interact ได้
พร้อม XPath, ข้อความ, ตำแหน่ง, และ attributes ต่างๆ

Requires:
    pip install requests websockets

Usage:
    # แบบ basic — ใช้ profile แรกที่หาเจอ
    python3 drum_xpath.py "https://www.facebook.com/groups/123456"

    # ระบุ profile
    python3 drum_xpath.py "https://www.facebook.com/marketplace" --profile "Facebook 2"

    # ระบุ profile ด้วย ID
    python3 drum_xpath.py "https://www.facebook.com/profile.php?id=xxx" --profile-id 3

    # ปรับจำนวน scroll + output path
    python3 drum_xpath.py "https://www.facebook.com/groups/123" --scroll 8 -o group_page.json

    # ดูว่ามี profile อะไรบ้าง
    python3 drum_xpath.py --list-profiles

    # เปิด profile ค้างไว้หลัง extract (สำหรับ debug)
    python3 drum_xpath.py "https://..." --keep-open
"""

import argparse
import asyncio
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import requests
import websockets

# ── Paths ──────────────────────────────────────────────────
SKILL_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = SKILL_DIR / "active"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── GemLogin API ───────────────────────────────────────────
GEMLOGIN_BASE = os.environ.get("GEMLOGIN_BASE", "http://localhost:1010")


def _api(method: str, path: str, **kw) -> dict:
    """Call GemLogin local REST API. Raises on failure."""
    url = f"{GEMLOGIN_BASE}{path}"
    timeout = kw.pop("timeout", 15)
    if method == "GET":
        r = requests.get(url, timeout=timeout, **kw)
    else:
        r = requests.post(url, timeout=timeout, **kw)
    r.raise_for_status()
    return r.json()


def gemlogin_status() -> dict:
    """Check if GemLogin is reachable."""
    try:
        return _api("GET", "/api/status", timeout=5)
    except Exception as e:
        return {"error": str(e)}


def gemlogin_list_profiles() -> list[dict]:
    """Return all browser profiles as a flat list of dicts."""
    data = _api("GET", "/api/profiles")
    # Normalise various response shapes
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("profiles", "data", "items"):
            if key in data and isinstance(data[key], list):
                return data[key]
    return []


def gemlogin_find_profile(name_or_id: str) -> dict | None:
    """Fuzzy-match a profile by id or name substring. Returns None if not found."""
    needle = name_or_id.strip().lower()
    for p in gemlogin_list_profiles():
        pid = str(p.get("id", ""))
        pname = str(p.get("name", ""))
        if needle == pid or needle == pid.lstrip("0"):
            return p
        if needle in pname.lower():
            return p
    return None


def gemlogin_start_profile(profile_id) -> dict:
    """Start a browser profile; returns {remote_debugging_address, ...}."""
    return _api("POST", f"/api/profiles/{profile_id}/start", timeout=60)


def gemlogin_stop_profile(profile_id) -> dict:
    """Stop a running browser profile."""
    try:
        return _api("POST", f"/api/profiles/{profile_id}/stop", timeout=30)
    except Exception as e:
        return {"error": str(e)}


# ── CDP Helpers ────────────────────────────────────────────

def _get_ws_url(debugger_address: str) -> str:
    """Query the HTTP debug endpoint to discover the page's WebSocket URL."""
    http_url = f"http://{debugger_address}/json"
    req = urllib.request.Request(http_url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        targets = json.loads(resp.read())

    # Prefer a real page target
    for t in targets:
        if t.get("type") == "page" and t.get("url", "").startswith("http"):
            return t["webSocketDebuggerUrl"]

    # Fallback to any page-type target
    for t in targets:
        if t.get("type") == "page":
            return t["webSocketDebuggerUrl"]

    # Desperate fallback
    if targets:
        return targets[0]["webSocketDebuggerUrl"]

    raise RuntimeError(f"No CDP page target found at {debugger_address}. Targets: {len(targets)}")


async def _cdp(ws, method: str, params: dict | None = None, timeout: int = 30) -> dict:
    """Send a CDP command and await its result. Events received in between are silently dropped."""
    params = params or {}
    msg_id = hash((method, time.monotonic())) & 0x7FFFFFFF
    payload = json.dumps({"id": msg_id, "method": method, "params": params})
    await ws.send(payload)

    deadline = time.monotonic() + timeout
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"CDP call {method!r} timed out after {timeout}s")
        raw = await asyncio.wait_for(ws.recv(), timeout=min(remaining, 5))
        data = json.loads(raw)
        if data.get("id") == msg_id:
            if "error" in data:
                err = data["error"]
                raise RuntimeError(f"CDP {method}: {err.get('message', err)}")
            return data.get("result", {})
        # else: event — ignore


async def _js(ws, expression: str, timeout: int = 15) -> object:
    """Evaluate JavaScript in the page and return the result value."""
    result = await _cdp(ws, "Runtime.evaluate", {
        "expression": expression,
        "returnByValue": True,
        "awaitPromise": True,
    }, timeout=timeout)
    obj = result.get("result", {})
    if obj.get("type") == "string":
        return obj["value"]
    return obj.get("value")


async def _wait_for_page_ready(ws, timeout: int = 45) -> None:
    """Wait until Page.loadEventFired, then give SPA an extra settle."""
    await _cdp(ws, "Page.enable")
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("Page load timeout")
        raw = await asyncio.wait_for(ws.recv(), timeout=min(remaining, 5))
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if data.get("method") == "Page.loadEventFired":
            break
    await asyncio.sleep(3)  # SPA settle


async def _scroll_reveal(ws, count: int = 5, delay: float = 1.5) -> None:
    """Progressive scroll to trigger lazy loading, then scroll back to top."""
    for i in range(count):
        pct = (i + 1) / (count + 1)
        await _js(ws, f"window.scrollTo(0, document.body.scrollHeight * {pct})")
        await asyncio.sleep(delay)
    await _js(ws, "window.scrollTo(0, 0)")
    await asyncio.sleep(1)


# ── Element Extraction (JS injected into the page) ─────────

# This JS runs in the browser. It walks every interactive element and builds
# the most stable XPath possible, tagged with a stability tier.
EXTRACT_JS = r"""
(function() {
    const TARGETS = [
        // Real interactive elements
        'a[href]:not([href="#"]):not([href^="javascript"])',
        'button',
        'input:not([type="hidden"])',
        'select',
        'textarea',
        // ARIA widgets
        '[role="button"]',
        '[role="link"]',
        '[role="menuitem"]',
        '[role="tab"]',
        '[role="checkbox"]',
        '[role="radio"]',
        '[role="combobox"]',
        '[role="searchbox"]',
        '[role="switch"]',
        '[role="option"]',
        '[role="listbox"]',
        '[role="textbox"]',
        '[role="menu"]',
        '[role="menubar"]',
        '[role="toolbar"]',
        '[role="dialog"]',
        // Rich text
        '[contenteditable="true"]',
        // Labelled / test-attributed
        '[aria-label]',
        '[data-testid]'
    ];

    function stableXPath(el) {
        if (!el || el.nodeType !== 1) return {xpath:'', stability:'error', reason:'not-an-element'};
        if (el === document.body) return {xpath:'/html/body', stability:'high', reason:'body'};

        const tag = el.tagName.toLowerCase();
        const $ = el.getAttribute.bind(el);
        const esc = (s) => s.replace(/"/g, '&quot;').replace(/\n/g, ' ');

        function unique(s) {
            try {
                const r = document.evaluate(s, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                return r.snapshotLength === 1;
            } catch(e) { return false; }
        }

        // --- Tier 1: data-testid ---
        let v = $('data-testid');
        if (v) {
            const x = `//${tag}[@data-testid="${esc(v)}"]`;
            return {xpath: x, stability: 'high', reason: 'data-testid'};
        }

        // --- Tier 2: unique aria-label ---
        v = $('aria-label');
        if (v && v.trim()) {
            const x = `//${tag}[@aria-label="${esc(v.trim())}"]`;
            if (unique(x)) return {xpath: x, stability: 'high', reason: 'unique-aria-label'};
        }

        // --- Tier 3: unique name ---
        v = $('name');
        if (v && v.trim()) {
            const x = `//${tag}[@name="${esc(v.trim())}"]`;
            if (unique(x)) return {xpath: x, stability: 'medium', reason: 'unique-name'};
        }

        // --- Tier 4: unique placeholder ---
        v = $('placeholder');
        if (v && v.trim()) {
            const x = `//${tag}[@placeholder="${esc(v.trim())}"]`;
            if (unique(x)) return {xpath: x, stability: 'medium', reason: 'unique-placeholder'};
        }

        // --- Tier 5: unique title ---
        v = $('title');
        if (v && v.trim()) {
            const x = `//${tag}[@title="${esc(v.trim())}"]`;
            if (unique(x)) return {xpath: x, stability: 'medium', reason: 'unique-title'};
        }

        // --- Tier 6: button/link with unique visible text ---
        const text = (el.textContent || el.innerText || '').trim().substring(0, 150);
        if (text && text.length < 100 && ['a','button','span','div','li','label'].includes(tag)) {
            const x = `//${tag}[normalize-space(.)="${esc(text)}"]`;
            if (unique(x)) return {xpath: x, stability: 'medium', reason: 'unique-text'};
        }

        // --- Tier 7: structural path from body ---
        const parts = [];
        let cur = el;
        while (cur && cur.nodeType === 1 && cur !== document.body) {
            const t = cur.tagName.toLowerCase();
            const parent = cur.parentNode;
            let idx = 1;
            if (parent) {
                const sibs = parent.children;
                for (let i = 0; i < sibs.length; i++) {
                    if (sibs[i] === cur) break;
                    if (sibs[i].tagName === cur.tagName) idx++;
                }
            }
            parts.unshift(t + '[' + idx + ']');
            cur = parent;
        }
        return {xpath: '/html/body/' + parts.join('/'), stability: 'low', reason: 'structural'};
    }

    // ── Collect ────────────────────────────────────────
    const seen = new Set();
    const results = [];

    TARGETS.forEach(function(sel) {
        try {
            document.querySelectorAll(sel).forEach(function(el) {
                if (seen.has(el)) return;
                seen.add(el);

                const tag = el.tagName.toLowerCase();
                const rect = el.getBoundingClientRect();
                let style;
                try { style = window.getComputedStyle(el); } catch(e) { style = null; }
                const visible = (
                    rect.width > 0 && rect.height > 0 &&
                    (!style || (style.display !== 'none' && style.visibility !== 'hidden'))
                );

                const xp = stableXPath(el);

                // Build CSS selector as well (best-effort)
                let css = null;
                const testId = el.getAttribute('data-testid');
                const ariaLab = el.getAttribute('aria-label');
                if (testId) css = tag + '[data-testid="' + testId.replace(/"/g,'\\"') + '"]';
                else if (ariaLab) css = tag + '[aria-label="' + ariaLab.replace(/"/g,'\\"') + '"]';
                else if (el.id && /^[a-zA-Z]/.test(el.id)) css = '#' + el.id;

                results.push({
                    tag: tag,
                    role: el.getAttribute('role') || null,
                    aria_label: ariaLab || null,
                    data_testid: testId || null,
                    name: el.getAttribute('name') || null,
                    placeholder: el.getAttribute('placeholder') || null,
                    title: el.getAttribute('title') || null,
                    type: el.getAttribute('type') || null,
                    href: el.getAttribute('href') || null,
                    id: el.id || null,
                    css: css,
                    xpath: xp.xpath,
                    stability: xp.stability,
                    stability_reason: xp.reason,
                    text: (el.textContent || el.innerText || '').trim().substring(0, 200),
                    visible: visible,
                    x: Math.round(rect.x),
                    y: Math.round(rect.y),
                    w: Math.round(rect.width),
                    h: Math.round(rect.height)
                });
            });
        } catch(_) {}
    });

    return JSON.stringify({total: results.length, elements: results});
})()
"""

# ── Main Drum Operation ────────────────────────────────────

async def drum_page(url: str, debugger_address: str, scroll_count: int = 5) -> dict:
    """
    Connect to an already-running browser via CDP, navigate, scroll, and extract.

    Returns {"url": final_url, "title": page_title, "data": {total, elements}}
    """
    ws_url = _get_ws_url(debugger_address)
    print(f"  CDP WebSocket: {ws_url[:60]}...")

    async with websockets.connect(ws_url, max_size=20 * 1024 * 1024) as ws:  # 20 MB
        await _cdp(ws, "Runtime.enable")
        await _cdp(ws, "Page.enable")

        # ── Navigate ──
        print(f"  Navigating → {url}")
        await _cdp(ws, "Page.navigate", {"url": url})
        await _wait_for_page_ready(ws, timeout=45)

        title = await _js(ws, "document.title") or "Unknown"
        current_url = await _js(ws, "window.location.href") or url

        print(f"  Title : {title}")
        print(f"  URL   : {current_url}")

        # ── Dismiss common Facebook popups ──
        await _js(ws, """
            // Try to dismiss cookie / login-wall / "see more" popups
            const btns = document.querySelectorAll('[aria-label="Close"], [aria-label="Decline optional cookies"], [aria-label="Allow essential and optional cookies"]');
            btns.forEach(b => { try { b.click(); } catch(e){} });
        """)
        await asyncio.sleep(1)

        # ── Scroll to reveal lazy-loaded content ──
        if scroll_count > 0:
            print(f"  Scrolling x{scroll_count} to reveal lazy content ...")
            await _scroll_reveal(ws, count=scroll_count)

        # ── Extract ──
        print("  Extracting interactive elements ...")
        raw = await _js(ws, EXTRACT_JS, timeout=30)
        data = json.loads(raw) if isinstance(raw, str) else raw

        total = data.get("total", len(data.get("elements", [])))
        print(f"  Found {total} interactive elements")

        # ── Stability breakdown ──
        by_stability = {"high": 0, "medium": 0, "low": 0, "error": 0}
        for el in data.get("elements", []):
            s = el.get("stability", "error")
            by_stability[s] = by_stability.get(s, 0) + 1
        print(f"  Stability: high={by_stability['high']} medium={by_stability['medium']} low={by_stability['low']}")

        return {"url": current_url, "title": title, "data": data}


# ── Output Helpers ─────────────────────────────────────────

def build_artifact(url: str, title: str, data: dict) -> dict:
    """Wrap raw extraction data into the standard artifact shape."""
    return {
        "source": "drum_xpath.py",
        "captured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "url": url,
        "title": title,
        "total_elements": data.get("total", 0),
        "elements": data.get("elements", []),
    }


def save_artifact(artifact: dict, output_path: str | Path | None, source_url: str) -> Path:
    """Write artifact to disk. Auto-generates filename if output_path is None."""
    if output_path:
        p = Path(output_path)
    else:
        domain = urllib.parse.urlparse(source_url).netloc.replace(".", "-") or "page"
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        p = OUTPUT_DIR / f"drum-{domain}-{ts}.json"

    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(artifact, f, ensure_ascii=False, indent=2)
    return p


def print_summary(artifact: dict) -> None:
    """Human-readable summary of extracted elements."""
    elements = artifact.get("elements", [])

    # Group by tag
    by_tag = {}
    for e in elements:
        t = e["tag"]
        by_tag[t] = by_tag.get(t, 0) + 1

    print("\n📊 By tag (top 20):")
    for tag, n in sorted(by_tag.items(), key=lambda x: -x[1])[:20]:
        bar = "█" * min(40, n // 2)
        print(f"  {tag:18s} {n:5d}  {bar}")

    # Group by role
    by_role = {}
    for e in elements:
        r = e.get("role") or "(none)"
        by_role[r] = by_role.get(r, 0) + 1
    print("\n🎭 By role (top 15):")
    for role, n in sorted(by_role.items(), key=lambda x: -x[1])[:15]:
        print(f"  {role:25s} {n:5d}")

    # High-stability elements with visible text
    high_text = [e for e in elements if e["stability"] == "high" and e["text"] and e["visible"]]
    if high_text:
        print(f"\n⭐ High-stability visible elements with text ({len(high_text)} total, showing first 30):")
        for e in high_text[:30]:
            txt = e["text"][:90].replace("\n", "⏎")
            print(f"  [{e['tag']:8s}] {txt}")
            print(f"   ↳ {e['xpath']}")

    # Elements grouped by approximate Y position (sections)
    print("\n📐 Page sections (by Y position):")
    sections = {}
    for e in elements:
        if not e["visible"]:
            continue
        y = e["y"]
        # Group into 300px vertical bands
        band = (y // 300) * 300
        if band not in sections:
            sections[band] = []
        sections[band].append(e)

    for band in sorted(sections.keys()):
        el_band = sections[band]
        texts = [e["text"] for e in el_band if e["text"] and len(e["text"]) < 80]
        sample = " | ".join(texts[:5])
        print(f"  y={band}-{band+300}: {len(el_band)} elements — {sample[:120]}")

    print(f"\n💾 Total: {artifact['total_elements']} elements saved.")


# ── CLI Entry Point ────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="🥁 Drum XPath — Extract all interactive XPaths from a Facebook page via GemLogin CDP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 drum_xpath.py "https://www.facebook.com/groups/123456"
  python3 drum_xpath.py "https://www.facebook.com/marketplace" --profile "Facebook 2"
  python3 drum_xpath.py --url "https://..." --profile-id 3 --scroll 8
  python3 drum_xpath.py --list-profiles
        """,
    )
    parser.add_argument(
        "url", nargs="?",
        help="Facebook URL to extract XPaths from",
    )
    parser.add_argument(
        "--url", dest="url_flag",
        help="Facebook URL (named form)",
    )
    parser.add_argument(
        "--profile", "-p",
        help="Profile name or substring (e.g. 'Facebook 2')",
    )
    parser.add_argument(
        "--profile-id", "-P",
        help="Exact profile ID number",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file path (auto-generated if omitted)",
    )
    parser.add_argument(
        "--scroll", "-s", type=int, default=5,
        help="Number of scroll passes for lazy content (default: 5)",
    )
    parser.add_argument(
        "--keep-open", "-k", action="store_true",
        help="Leave browser profile running after extraction",
    )
    parser.add_argument(
        "--list-profiles", "-l", action="store_true",
        help="List available GemLogin browser profiles and exit",
    )
    parser.add_argument(
        "--no-summary", action="store_true",
        help="Skip the summary printout",
    )

    args = parser.parse_args()
    target_url = args.url or args.url_flag

    # ── list-profiles ──
    if args.list_profiles:
        print("📋 Available GemLogin profiles:\n")
        profiles = gemlogin_list_profiles()
        if not profiles:
            print("  (none found — is GemLogin running?)")
            return
        for p in profiles:
            pid = p.get("id", "?")
            pname = p.get("name", "(unnamed)")
            group = p.get("group", p.get("groupName", ""))
            info = f"  group={group}" if group else ""
            print(f"  ID={pid:5s}  {pname}{info}")
        print(f"\n  Total: {len(profiles)} profile(s)")
        return

    # ── URL required beyond here ──
    if not target_url:
        parser.error("Must provide a URL to drum. Use --list-profiles to see available profiles.")

    # Normalise URL
    parsed = urllib.parse.urlparse(target_url)
    if not parsed.scheme:
        target_url = "https://" + target_url

    # ── GemLogin health ──
    print("🔍 Checking GemLogin API ...")
    status = gemlogin_status()
    if "error" in status:
        print(f"❌ GemLogin unreachable: {status['error']}")
        print("   Start GemLogin first, then retry.")
        sys.exit(1)
    print(f"   ✅ API ok — {status}")

    # ── Resolve profile ──
    profile_id = args.profile_id
    profile_name = None

    if not profile_id and args.profile:
        print(f"🔎 Searching profile: {args.profile}")
        match = gemlogin_find_profile(args.profile)
        if match:
            profile_id = match.get("id")
            profile_name = match.get("name", str(profile_id))
            print(f"   ✅ Found ID={profile_id}  name={profile_name}")
        else:
            print(f"❌ No profile matching '{args.profile}'")
            print("   Use --list-profiles to see available profiles.")
            sys.exit(1)

    if not profile_id:
        # Auto-pick first available
        profiles = gemlogin_list_profiles()
        if not profiles:
            print("❌ No profiles. Create one in GemLogin first.")
            sys.exit(1)
        profile_id = profiles[0].get("id")
        profile_name = profiles[0].get("name", str(profile_id))
        print(f"ℹ️  Auto-selected first profile: ID={profile_id}  name={profile_name}")
        print("   Use --profile <name> or --profile-id <id> to pick a different one.")
    elif not profile_name:
        # Look up name for the given ID
        for p in gemlogin_list_profiles():
            if str(p.get("id")) == str(profile_id):
                profile_name = p.get("name", str(profile_id))
                break
        if not profile_name:
            profile_name = str(profile_id)

    # ── Start profile ──
    print(f"\n🚀 Starting profile {profile_id} ({profile_name}) ...")
    try:
        start_result = gemlogin_start_profile(profile_id)
    except Exception as e:
        print(f"❌ Failed to start profile: {e}")
        sys.exit(1)

    debugger_address = start_result.get("remote_debugging_address")
    if not debugger_address:
        print(f"❌ No remote_debugging_address returned: {json.dumps(start_result, indent=2)}")
        sys.exit(1)

    print(f"   ✅ Started — CDP at {debugger_address}")
    time.sleep(2)  # Let Chromium finish initialising

    # ── Drum ──
    print(f"\n🥁 Drumming: {target_url}")
    error_occurred = False
    try:
        result = asyncio.run(drum_page(target_url, debugger_address, args.scroll))
    except Exception as e:
        print(f"\n❌ Drum failed: {e}")
        import traceback
        traceback.print_exc()
        result = None
        error_occurred = True

    # ── Stop profile ──
    if not args.keep_open:
        print("\n🛑 Stopping profile ...")
        stop_r = gemlogin_stop_profile(profile_id)
        if "error" in stop_r:
            print(f"   ⚠️  Stop warning: {stop_r['error']}")
        else:
            print("   ✅ Stopped")
    else:
        print(f"\n⚠️  Profile {profile_id} left running (--keep-open). Remember to stop it manually.")

    if error_occurred or not result:
        sys.exit(1)

    # ── Build & save artifact ──
    artifact = build_artifact(result["url"], result["title"], result["data"])
    output_path = save_artifact(artifact, args.output, result["url"])
    print(f"\n✅ Artifact saved → {output_path}")

    # ── Summary ──
    if not args.no_summary:
        print_summary(artifact)

    print("\n🎉 Done!")
    return output_path


if __name__ == "__main__":
    main()
