# Build script for creating standalone executable

Write-Host "Building Photography Deployment App Executable..." -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCheck) {
    Write-Host "Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

$pythonVersion = python --version 2>&1
Write-Host "Python found: $pythonVersion" -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install pyinstaller "PySide6>=6.6.0"

Write-Host ""
Write-Host "Building executable with PyInstaller..." -ForegroundColor Cyan
Write-Host ""

# Build the executable
python -m PyInstaller --name "PhotoDeploymentApp" --onefile --windowed --icon=NONE --hidden-import "PySide6.QtCore" --hidden-import "PySide6.QtGui" --hidden-import "PySide6.QtWidgets" --clean deploy-app-pyside6.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location: dist\PhotoDeploymentApp.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now run the executable from anywhere!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Build failed. Check the error messages above." -ForegroundColor Red
    exit 1
}
