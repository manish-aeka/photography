# Setup script for PySide6 Deployment Tool
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Photography Deployment Tool - Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing PySide6..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements-pyside6.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host "Setup completed successfully!" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To run the application, use:" -ForegroundColor Cyan
    Write-Host "  python deploy-app-pyside6.py" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Setup failed!" -ForegroundColor Red
    exit 1
}
