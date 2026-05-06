# Wednesday AI Assistant - PowerShell Startup Script
# Usage: .\run.ps1

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Wednesday AI Assistant" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-Not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Error: .venv not found. Run setup.py first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-Not (Test-Path ".env")) {
    Write-Host "Error: .env not found. Add your ANTHROPIC_API_KEY." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting Wednesday..." -ForegroundColor Green
Write-Host ""

& ".venv\Scripts\python.exe" -X utf8 main.py

Write-Host ""
Write-Host "Wednesday session ended." -ForegroundColor Cyan
