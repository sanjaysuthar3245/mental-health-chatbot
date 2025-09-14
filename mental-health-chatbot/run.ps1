# Mental Health ChatBot - PowerShell Launcher
Write-Host "🚀 Starting Mental Health ChatBot..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "🐍 Python version: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "ℹ️  No virtual environment found. Using system Python." -ForegroundColor Yellow
}

# Run the application
try {
    Write-Host "🌐 Starting Flask application..." -ForegroundColor Green
    python run.py
} catch {
    Write-Host "❌ Error running application: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}

