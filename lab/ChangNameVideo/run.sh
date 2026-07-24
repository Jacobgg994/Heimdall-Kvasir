#!/bin/bash
# ChangNameVideo Launcher (Linux/Mac)

echo "╔══════════════════════════════════════════╗"
echo "║     ChangNameVideo                       ║"
echo "║     เปลี่ยนชื่อวิดีโอแบบสุ่ม                ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# เช็ค Python
if ! command -v python3 &> /dev/null; then
    echo "[❌] ไม่พบ Python3 กรุณาติดตั้ง Python3 ก่อน"
    exit 1
fi

echo "[✅] พบ Python3"
echo "[🚀] กำลังเปิดโปรแกรม..."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/ChangNameVideo.py"
