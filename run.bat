@echo off
chcp 65001 >nul
title Wednesday AI Assistant

echo.
echo ========================================
echo  Wednesday AI Assistant
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo Error: .venv not found. Run setup.py first.
    pause
    exit /b 1
)

if not exist ".env" (
    echo Error: .env file not found. Add your ANTHROPIC_API_KEY.
    pause
    exit /b 1
)

echo Starting Wednesday...
echo.
.venv\Scripts\python.exe -X utf8 main.py
pause
