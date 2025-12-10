#!/bin/bash
# Build script for creating standalone executable for macOS

echo "Building Photography Deployment App for macOS..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Python found: $PYTHON_VERSION"

# Install dependencies
echo "Installing dependencies in a local virtualenv..."

# Determine script directory (so venv is created next to this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR"
    python3 -m venv "$VENV_DIR" || { echo "Failed to create virtualenv"; exit 1; }
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Upgrade pip and install required packages into venv
python -m pip install --upgrade pip
python -m pip install pyinstaller "PySide6>=6.6.0"

# Use the venv python for the rest of the script (PyInstaller will be available)
PYTHON_EXEC=python

echo ""
echo "Building executable with PyInstaller..."
echo ""

# Build the executable for macOS
# Ensure we run PyInstaller from the script directory so relative paths resolve
cd "$SCRIPT_DIR"

$PYTHON_EXEC -m PyInstaller \
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
