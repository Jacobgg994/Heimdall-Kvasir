"""
Test Facebook Reels posting flow via CDP
=========================================
Connects to GemLogin browser profile via CDP,
navigates Facebook, captures selectors for [FB] Post Reels workflow.

Usage (run on Windows):
  python test_reels_flow.py 127.0.0.1:51426
"""

import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path

CDP_URL = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1:51426"

# ── Setup Playwright connection ────────────────────────────────────
from playwright.sync_api import sync_playwright

print(f"[*] Connecting to CDP: {CDP_URL}")
print(f"[*] Time: {datetime.now(timezone.utc).isoformat()}")

results = {
    "profile": {"id": "6a5b462f6d10315762e194bf", "name": "100091713686649"},
    "cdp_url": CDP_URL,
    "captured_at": datetime.now(timezone.utc).isoformat(),
    "steps": [],
    "selectors": [],
}

def log_step(name, status, detail=""):
    entry = {"step": name, "status": status, "detail": detail, "time": datetime.now(timezone.utc).isoformat()}
    results["steps"].append(entry)
    print(f"  [{status}] {name} {detail}")

def capture_selector(name, xpath, css="", tag="", role="", aria_label="", text="",
                     match_count=0, visible=False, enabled=False, verified=False,
                     note=""):
    sel = {
        "name": name, "xpath": xpath, "css": css,
        "tag": tag, "role": role, "aria_label": aria_label, "text": text,
        "match_count": match_count, "visible": visible, "enabled": enabled,
        "verified": verified, "note": note,
    }
    results["selectors"].append(sel)
    return sel

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://{CDP_URL}")
    contexts = browser.contexts
    if not contexts:
        print("[!] No browser contexts found")
        sys.exit(1)

    context = contexts[0]
    pages = context.pages
    if not pages:
        page = context.new_page()
    else:
        page = pages[0]

    print(f"[*] Current URL: {page.url}")
    print(f"[*] Current title: {page.title()}")

    # ═══════════════════════════════════════════════════════════════
    # STEP 1: Navigate to Facebook
    # ═══════════════════════════════════════════════════════════════
    print("\n─── STEP 1: Navigate to Facebook ───")
    try:
        page.goto("https://www.facebook.com/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle", timeout=30000)
        log_step("navigate-home", "ok", f"URL={page.url[:80]}")
    except Exception as e:
        log_step("navigate-home", "error", str(e)[:100])

    time.sleep(3)
    title = page.title()
    url = page.url
    print(f"  Title: {title}")
    print(f"  URL: {url}")

    # Check if logged in
    if "login" in url.lower() or "Log In" in title:
        log_step("login-check", "warn", "NOT LOGGED IN - need manual login")
        print("[!] Profile may not be logged into Facebook.")
        print("[!] Stopping test — login required first.")
        browser.close()
        sys.exit(0)

    log_step("login-check", "ok", "Logged in")

    # ═══════════════════════════════════════════════════════════════
    # STEP 2: Inspect current identity (profile vs page)
    # ═══════════════════════════════════════════════════════════════
    print("\n─── STEP 2: Identity Inspection ───")
    page.goto("https://www.facebook.com/profile", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(3)

    identity_url = page.url
    identity_title = page.title()
    print(f"  Profile URL: {identity_url}")
    print(f"  Profile Title: {identity_title}")

    # Capture account name from profile
    try:
        # Try getting the profile name from the page
        name_el = page.locator("h1").first
        if name_el.is_visible():
            account_name = name_el.text_content().strip()
            print(f"  Account name: {account_name}")
            capture_selector("profile-name", "//h1", tag="h1", text=account_name,
                           match_count=1, visible=True, verified=True)
    except:
        pass

    # Check if this is a page
    is_page = "profile.php" in identity_url and "id=" in identity_url
    log_step("identity-check", "ok", f"is_page={is_page} url={identity_url[:80]}")

    # ═══════════════════════════════════════════════════════════════
    # STEP 3: Navigate to Reels creator
    # ═══════════════════════════════════════════════════════════════
    print("\n─── STEP 3: Reels Creator ───")
    try:
        page.goto("https://www.facebook.com/reels/create/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle", timeout=20000)
        time.sleep(5)
        reels_url = page.url
        reels_title = page.title()
        print(f"  Reels URL: {reels_url}")
        print(f"  Reels Title: {reels_title}")
        log_step("reels-create-url", "ok", f"URL={reels_url[:80]}")
    except Exception as e:
        log_step("reels-create-url", "error", str(e)[:100])
        reels_url = page.url

    # ═══════════════════════════════════════════════════════════════
    # STEP 4: Capture Reels creator selectors
    # ═══════════════════════════════════════════════════════════════
    print("\n─── STEP 4: Capture Selectors ───")

    # --- 4a: Upload button / file input ---
    file_inputs = page.locator("input[type='file']")
    file_count = file_inputs.count()
    print(f"  File inputs found: {file_count}")
    for i in range(min(file_count, 5)):
        try:
            inp = file_inputs.nth(i)
            accept = inp.get_attribute("accept") or ""
            visible = inp.is_visible()
            print(f"    [{i}] accept={accept} visible={visible}")
        except:
            pass

    # Look for upload triggers
    for selector_name, xpath in [
        ("reels-upload-input-video", "//input[@type='file' and contains(@accept,'video')]"),
        ("reels-upload-input-all", "//input[@type='file']"),
        ("reels-upload-wrapper", "//div[@role='dialog']//input[@type='file']"),
        ("reels-create-area", "//div[@aria-label='Create a post']"),
        ("reels-photo-video-btn", "//div[@aria-label='Photo/video']"),
    ]:
        try:
            loc = page.locator(f"xpath={xpath}")
            count = loc.count()
            vis = loc.first.is_visible() if count > 0 else False
            print(f"  {selector_name}: count={count} visible={vis}")
            capture_selector(selector_name, xpath, match_count=count, visible=vis,
                           verified=count == 1 and vis)
        except Exception as e:
            print(f"  {selector_name}: error={str(e)[:50]}")

    # --- 4b: Reels navigation via sidebar ---
    for selector_name, xpath in [
        ("nav-reels", "//a[@aria-label='Reels']"),
        ("nav-home", "//a[@aria-label='Home']"),
        ("composer-create-post", "//div[@aria-label='Create a post']"),
        ("composer-photo-video", "//div[@aria-label='Photo/video']"),
    ]:
        try:
            loc = page.locator(f"xpath={xpath}")
            count = loc.count()
            vis = loc.first.is_visible() if count > 0 else False
            print(f"  {selector_name}: count={count} visible={vis}")
            capture_selector(selector_name, xpath, match_count=count, visible=vis,
                           verified=count == 1 and vis)
        except Exception as e:
            print(f"  {selector_name}: error={str(e)[:50]}")

    # --- 4c: What's actually on the page ---
    print("\n  --- Page analysis ---")
    page_text = page.text_content()[:2000]
    # Check for key indicators
    indicators = ["Reel", "reel", "Create", "Upload", "Share", "Publish",
                  "Video", "video", "Post", "Compose", "What's on your mind"]
    for ind in indicators:
        if ind.lower() in page_text.lower():
            print(f"    Found: '{ind}' on page")

    # ═══════════════════════════════════════════════════════════════
    # STEP 5: Save results
    # ═══════════════════════════════════════════════════════════════
    output_dir = Path(r"D:\skills\WorkflowGemlogin\Edit")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "fb_reels_test_results.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Results saved to: {output_file}")

    # Don't close browser — user wants to inspect
    print("[*] Browser stays open for inspection.")
    print("[*] Press Ctrl+C when done...")
    try:
        input()
    except:
        pass
    browser.close()


if __name__ == "__main__":
    main()
