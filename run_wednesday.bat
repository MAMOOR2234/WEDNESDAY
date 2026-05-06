@echo off
REM Wednesday AI Assistant - Simple Launcher
REM Just double-click this file!

echo.
echo ========================================
echo  WEDNESDAY - AI Assistant
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found!
    echo Please install Python from: https://python.org
    pause
    exit /b 1
)

REM Activate venv if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run Wednesday
python start_wednesday.py

pause
