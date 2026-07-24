#!/usr/bin/env python3
"""JIMMY Notification — ส่งข้อความผ่าน Telegram Bot"""

import requests
import sys
import os

TOKEN = "8658191125:AAF0OfS_EvWISikksjpuWmO-vbH2MyIyZR0"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Jacob's chat ID (จะถูกตั้งอัตโนมัติหลังจาก Jacob คุยกับบอทครั้งแรก)
JACOB_CHAT_ID_FILE = os.path.join(os.path.dirname(__file__), ".chat_id")


def get_chat_id():
    """Get latest chat ID from updates"""
    try:
        resp = requests.get(f"{BASE_URL}/getUpdates", timeout=5).json()
        if resp["ok"] and resp["result"]:
            chat_ids = set()
            for update in resp["result"]:
                if "message" in update:
                    chat_ids.add(update["message"]["chat"]["id"])
                elif "callback_query" in update:
                    chat_ids.add(update["callback_query"]["message"]["chat"]["id"])
            if chat_ids:
                return max(chat_ids)  # Return most recent
    except Exception:
        pass
    return None


def send_message(text: str, chat_id: int = None):
    """Send a message via Telegram bot"""
    if not chat_id:
        # Try cached
        if os.path.exists(JACOB_CHAT_ID_FILE):
            with open(JACOB_CHAT_ID_FILE) as f:
                chat_id = int(f.read().strip())
        else:
            chat_id = get_chat_id()
            if chat_id:
                with open(JACOB_CHAT_ID_FILE, "w") as f:
                    f.write(str(chat_id))

    if not chat_id:
        print("❌ ไม่พบ chat_id — กรุณาคุยกับ @Jimmycore_bot ก่อน")
        sys.exit(1)

    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    resp = requests.post(url, json=payload, timeout=10).json()
    if resp.get("ok"):
        print(f"✅ ส่งแล้ว — chat_id={chat_id}")
    else:
        print(f"❌ ส่งไม่สำเร็จ: {resp.get('description')}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_message(" ".join(sys.argv[1:]))
    else:
        text = sys.stdin.read().strip()
        if text:
            send_message(text)
        else:
            print("วิธีใช้: python notify.py <ข้อความ>")
            print("หรือ: echo 'ข้อความ' | python notify.py")
