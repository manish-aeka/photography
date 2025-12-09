# Build Script for Creating Executable
# Run this script to create the .exe file

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Photography Portfolio Deployment Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "✓ $pythonVersion found" -ForegroundColor Green
Write-Host ""

# Install PyInstaller if not already installed
Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install pyinstaller
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install PyInstaller" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "✓ PyInstaller installed successfully" -ForegroundColor Green
Write-Host ""

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }
Write-Host "✓ Cleaned" -ForegroundColor Green
Write-Host ""

# Build the executable
Write-Host "Building executable..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Yellow
Write-Host ""

pyinstaller --name="Photography-Portfolio-Deployment" `
    --onefile `
    --windowed `
    --icon=NONE `
    --add-data="anupam-dutta-photography-data-set.json;." `
    --add-data="deploy.sh;." `
    deploy-app.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executable created at:" -ForegroundColor Cyan
Write-Host "  dist\Photography-Portfolio-Deployment.exe" -ForegroundColor White
Write-Host ""
Write-Host "You can now distribute this .exe file!" -ForegroundColor Green
Write-Host ""
pause
