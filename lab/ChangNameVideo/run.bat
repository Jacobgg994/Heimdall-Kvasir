@echo off
chcp 65001 >nul
title ChangNameVideo
echo.
echo ╔══════════════════════════════════════════╗
echo ║     ChangNameVideo                       ║
echo ║     เปลี่ยนชื่อวิดีโอแบบสุ่ม                ║
echo ╚══════════════════════════════════════════╝
echo.

:: เช็คว่ามี Python ไหม
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [❌] ไม่พบ Python กรุณาติดตั้ง Python ก่อน
    echo      ดาวน์โหลด: https://www.python.org/downloads/
    echo      *** สำคัญ: ติ๊กถูก "Add Python to PATH" ตอนติดตั้ง ***
    pause
    exit /b 1
)

echo [✅] พบ Python
echo [🚀] กำลังเปิดโปรแกรม...
echo.

python "%~dp0ChangNameVideo.py"

if %errorlevel% neq 0 (
    echo.
    echo [❌] เกิดข้อผิดพลาด
    pause
)
