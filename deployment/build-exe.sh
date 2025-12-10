#!/bin/bash
# Build script for creating standalone executable
# Works on macOS and Linux

echo "📦 Building Photography Deployment App Executable..."
echo ""

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python is not installed or not in PATH"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "✓ Python found: $PYTHON_VERSION"

# Check if PyInstaller is installed
if ! $PYTHON_CMD -m pip show pyinstaller &> /dev/null; then
    echo "⚠️ PyInstaller not found. Installing..."
    $PYTHON_CMD -m pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install PyInstaller"
        exit 1
    fi
    echo "✓ PyInstaller installed successfully"
else
    echo "✓ PyInstaller is already installed"
fi

# Check if PySide6 is installed
if ! $PYTHON_CMD -m pip show PySide6 &> /dev/null; then
    echo "⚠️ PySide6 not found. Installing..."
    $PYTHON_CMD -m pip install "PySide6>=6.6.0"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install PySide6"
        exit 1
    fi
    echo "✓ PySide6 installed successfully"
else
    echo "✓ PySide6 is already installed"
fi

echo ""
echo "🔨 Building executable with PyInstaller..."
echo ""

# Build the executable
$PYTHON_CMD -m PyInstaller \
    --name "PhotoDeploymentApp" \
    --onefile \
    --windowed \
    --icon=NONE \
    --hidden-import "PySide6.QtCore" \
    --hidden-import "PySide6.QtGui" \
    --hidden-import "PySide6.QtWidgets" \
    --clean \
    deploy-app-pyside6.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build completed successfully!"
    echo ""
    echo "📍 Executable location:"
    echo "   dist/PhotoDeploymentApp"
    echo ""
    echo "🚀 You can now run the executable from anywhere!"
    echo "   It will open a file browser to select JSON files from any location."
    echo ""
    
    # Make executable on Unix systems
    chmod +x dist/PhotoDeploymentApp
    echo "✓ Executable permissions set"
else
    echo ""
    echo "❌ Build failed. Check the error messages above."
    exit 1
fi
