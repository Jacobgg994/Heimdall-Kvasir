@echo off
title YumClip (ยำรวมคลิป)
cd /d "%~dp0"

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH.  Please install Python 3.
    echo          https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check for ffmpeg
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] ffmpeg not found in PATH.
    echo           Please install ffmpeg: https://ffmpeg.org/download.html
    echo           Or via winget:  winget install ffmpeg
    echo.
)

:: Launch GUI by default; pass args to CLI
if "%~1"=="" (
    python "%~dp0yumclip.py" --gui
) else (
    python "%~dp0yumclip.py" %*
)

pause
