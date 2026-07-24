#!/usr/bin/env python3
"""JIMMY 🌊 Telegram Bot — @Jimmycore_bot"""

import asyncio
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Config
TOKEN = "8658191125:AAF0OfS_EvWISikksjpuWmO-vbH2MyIyZR0"
CHAT_ID_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".chat_id")
JACOB_CHAT_ID = None

# Load saved chat_id
if os.path.exists(CHAT_ID_FILE):
    with open(CHAT_ID_FILE) as f:
        JACOB_CHAT_ID = int(f.read().strip())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message"""
    global JACOB_CHAT_ID
    JACOB_CHAT_ID = update.effective_chat.id
    # Save chat_id for notification system
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(JACOB_CHAT_ID))

    await update.message.reply_text(
        "🌊 *JIMMY พร้อมทำงาน*\n\n"
        "ผมคือ JIMMY — Ocean Kvasir ผู้ช่วยของ JACOB\n\n"
        "📋 *คำสั่งที่มี:*\n"
        "/start — เริ่มต้น\n"
        "/status — สถานะทีม\n"
        "/team — รายชื่อทีม\n"
        "/help — วิธีใช้\n"
        "/notify <ข้อความ> — ส่งแจ้งเตือนหา JACOB",
        parse_mode=ParseMode.MARKDOWN
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Report team status"""
    await update.message.reply_text(
        "👥 *สถานะทีม Kvasir — 15 คน*\n\n"
        "🌊 JIMMY — Manager ✅\n"
        "🔭 JASPER — Trend Lead ✅\n"
        "  🔬 SCOPE — OSINT ✅\n"
        "  🔍 PRISM — OSINT ✅\n"
        "🪸 CORAL — Dev Lead ✅\n"
        "  🐟 PYKE — Frontend ✅\n"
        "  🌊 TIDE — Junior ✅\n"
        "  🌫️ DRIFT — DevOps ✅\n"
        "  🐚 SHELL — QA ✅\n"
        "  ⚡ SURGE — AI/ML ✅\n"
        "💎 GEMMY — Auto ✅\n"
        "📈 KOMHAS — Marketing ✅\n"
        "🎨 SALMON — Content ✅\n"
        "🦅 KAMU — Sales ✅\n"
        "🤝 CILA — HR ✅\n\n"
        f"🕐 _{datetime.now().strftime('%Y-%m-%d %H:%M ICT')}_",
        parse_mode=ParseMode.MARKDOWN
    )

async def team_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List team members"""
    await update.message.reply_text(
        "📋 *Team Roster — 15 คน*\n\n"
        "1. JIMMY 🌊 — Manager\n"
        "2. JASPER 🔭 — Trend Scout\n"
        "3. SCOPE 🔬 — Senior OSINT\n"
        "4. PRISM 🔍 — OSINT Researcher\n"
        "5. CORAL 🪸 — Dev Lead\n"
        "6. PYKE 🐟 — Frontend\n"
        "7. TIDE 🌊 — Junior Dev\n"
        "8. DRIFT 🌫️ — DevOps\n"
        "9. SHELL 🐚 — QA\n"
        "10. SURGE ⚡ — AI/ML\n"
        "11. GEMMY 💎 — Automation\n"
        "12. KOMHAS 📈 — Marketing\n"
        "13. SALMON 🎨 — Content\n"
        "14. KAMU 🦅 — Sales\n"
        "15. CILA 🤝 — HR",
        parse_mode=ParseMode.MARKDOWN
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help"""
    await update.message.reply_text(
        "🤖 *JIMMY Bot — วิธีใช้*\n\n"
        "*คำสั่ง:*\n"
        "`/start` — เริ่มต้นการทำงาน\n"
        "`/status` — ดูสถานะทีม\n"
        "`/team` — รายชื่อทีมทั้งหมด\n"
        "`/help` — ดูวิธีใช้\n\n"
        "*การแจ้งเตือน:*\n"
        "JIMMY จะส่งแจ้งเตือนอัตโนมัติเมื่อ:\n"
        "• มีงานเสร็จ\n"
        "• มีปัญหาต้องตัดสินใจ\n"
        "• รายงานประจำวัน\n\n"
        "📂 *ไฟล์:* `Kvasir/lab/telegram_bot/`",
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages — save chat_id on any message"""
    global JACOB_CHAT_ID
    JACOB_CHAT_ID = update.effective_chat.id
    # Save immediately on any message
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(JACOB_CHAT_ID))

    text = update.message.text
    user = update.effective_user.first_name

    if "สวัสดี" in text or "hello" in text.lower():
        await update.message.reply_text(f"สวัสดีครับ {user}! 🌊\nJIMMY พร้อมให้บริการ\n\nใช้ /help เพื่อดูคำสั่ง")
    elif "ขอบคุณ" in text or "thank" in text.lower():
        await update.message.reply_text("ด้วยความยินดีครับ 🙏")
    else:
        await update.message.reply_text(
            f"รับทราบครับ {user} 📝\nใช้ /help เพื่อดูคำสั่ง",
            parse_mode=ParseMode.MARKDOWN
        )

def main():
    """Start the bot"""
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("team", team_list))
    app.add_handler(CommandHandler("help", help_cmd))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🌊 JIMMY Bot started — @Jimmycore_bot")
    app.run_polling()

if __name__ == "__main__":
    main()
