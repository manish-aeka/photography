#!/bin/bash
# Build script for creating standalone executable for Linux (Ubuntu/Debian)

echo "Building Photography Deployment App for Linux..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Python found: $PYTHON_VERSION"

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install pyinstaller "PySide6>=6.6.0"

echo ""
echo "Building executable with PyInstaller..."
echo ""

# Build the executable for Linux
python3 -m PyInstaller \
    --name "PhotoDeploymentApp" \
    --onefile \
    --windowed \
    --hidden-import "PySide6.QtCore" \
    --hidden-import "PySide6.QtGui" \
    --hidden-import "PySide6.QtWidgets" \
    --clean \
    deploy-app-pyside6.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Build completed successfully!"
    echo ""
    echo "Executable location: dist/PhotoDeploymentApp"
    echo ""
    echo "You can now run the executable from anywhere!"
    echo ""
    echo "To make it executable, run:"
    echo "chmod +x dist/PhotoDeploymentApp"
else
    echo ""
    echo "Build failed. Check the error messages above."
    exit 1
fi
