# Wednesday AI Assistant - GUI Mode Launcher (PowerShell)
# Right-click and select "Run with PowerShell"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Wednesday AI - JARVIS-Style GUI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found" -ForegroundColor Red
    pause
    exit 1
}

# Create venv if needed
if (-Not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate venv
& "venv\Scripts\Activate.ps1"

# Check PyQt6
Write-Host "Checking PyQt6..." -ForegroundColor Yellow
python -c "import PyQt6" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing PyQt6..." -ForegroundColor Yellow
    pip install PyQt6 -q
}

# Launch GUI
Write-Host ""
Write-Host "Starting Wednesday GUI..." -ForegroundColor Green
Write-Host ""

python gui_launcher.py

Read-Host "Press Enter to exit"
