@echo off
chcp 65001 >nul
title Wednesday Portal
cd /d "%~dp0"

echo.
echo  Starting Wednesday Portal...
echo  Open http://localhost:5000 in your browser
echo.

.venv\Scripts\python.exe -X utf8 portal.py
pause
