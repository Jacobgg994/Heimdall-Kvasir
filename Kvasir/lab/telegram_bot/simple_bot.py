#!/usr/bin/env python3
"""JIMMY Simple Bot — no external deps, just requests"""
import requests, json, time, os

TOKEN = "8658191125:AAF0OfS_EvWISikksjpuWmO-vbH2MyIyZR0"
BASE = f"https://api.telegram.org/bot{TOKEN}"
DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_FILE = os.path.join(DIR, ".chat_id")
OFFSET_FILE = os.path.join(DIR, ".offset")

def save_chat_id(cid):
    with open(CHAT_FILE, "w") as f:
        f.write(str(cid))

def get_offset():
    if os.path.exists(OFFSET_FILE):
        return int(open(OFFSET_FILE).read().strip())
    return 0

def save_offset(offset):
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))

def send_message(chat_id, text, parse_mode="Markdown"):
    return requests.post(f"{BASE}/sendMessage", json={
        "chat_id": chat_id, "text": text, "parse_mode": parse_mode
    }).json()

print("🌊 JIMMY Simple Bot started")

offset = get_offset()
while True:
    try:
        resp = requests.get(f"{BASE}/getUpdates", params={
            "offset": offset, "timeout": 30
        }, timeout=35).json()

        if resp.get("ok"):
            for update in resp["result"]:
                offset = update["update_id"] + 1
                save_offset(offset)

                if "message" not in update:
                    continue

                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                user = msg["chat"].get("first_name", "")

                # Save chat_id immediately
                save_chat_id(chat_id)
                print(f"📩 {user}: {text[:50]}")

                # Respond
                if text.startswith("/start"):
                    send_message(chat_id, f"🌊 *JIMMY พร้อมทำงาน*\n\nสวัสดีครับ {user}!\n\n📋 คำสั่ง:\n/start — เริ่มต้น\n/status — สถานะทีม\n/team — รายชื่อทีม\n/help — วิธีใช้")
                    print(f"  ✅ Sent welcome to {chat_id}")
                elif text.startswith("/status"):
                    send_message(chat_id, "👥 *ทีม 15 คน*\n🌊 JIMMY ✅\n🔭 JASPER ✅\n🔬 SCOPE ✅\n🔍 PRISM ✅\n🪸 CORAL ✅\n🐟 PYKE ✅\n🌊 TIDE ✅\n🌫️ DRIFT ✅\n🐚 SHELL ✅\n⚡ SURGE ✅\n💎 GEMMY ✅\n📈 KOMHAS ✅\n🎨 SALMON ✅\n🦅 KAMU ✅\n🤝 CILA ✅")
                elif text.startswith("/team"):
                    send_message(chat_id, """📋 *JACOB Team — 15 คน*

1. 🌊 JIMMY — Manager
2. 🔭 JASPER — Trend Lead
3. 🔬 SCOPE — OSINT Senior
4. 🔍 PRISM — OSINT
5. 🪸 CORAL — Dev Lead
6. 🐟 PYKE — Frontend
7. 🌊 TIDE — Junior Dev
8. 🌫️ DRIFT — DevOps
9. 🐚 SHELL — QA
10. ⚡ SURGE — AI/ML
11. 💎 GEMMY — Automation
12. 📈 KOMHAS — Marketing
13. 🎨 SALMON — Content
14. 🦅 KAMU — Sales
15. 🤝 CILA — HR""")
                else:
                    send_message(chat_id, f"รับทราบครับ {user} ✅\nใช้ /help เพื่อดูคำสั่ง")

    except Exception as e:
        print(f"⚠️ {e}")
        time.sleep(5)
