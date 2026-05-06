@echo off
REM Wednesday AI Assistant - GUI Mode Launcher
REM Just double-click this file to start the GUI!

echo.
echo ========================================
echo  Wednesday AI - JARVIS-Style GUI
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found
    pause
    exit /b 1
)

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Check PyQt6
python -c "import PyQt6" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyQt6...
    pip install PyQt6 -q
)

REM Launch GUI
echo.
echo Starting Wednesday GUI...
echo.
python gui_launcher.py

pause
