#!/bin/bash
# Setup script for Photography Portfolio Deployment App
# This script installs all required dependencies

echo "==============================================="
echo "Photography Portfolio - Deployment Setup"
echo "==============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[1/3] Python found!"
python3 --version
echo ""

# Check if we're in a virtual environment, if not create one
if [ ! -d ".venv" ]; then
    echo "[2/3] Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created!"
else
    echo "[2/3] Virtual environment already exists"
fi
echo ""

# Activate virtual environment and install dependencies
echo "[3/3] Installing dependencies..."
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "==============================================="
    echo "Setup completed successfully!"
    echo "==============================================="
    echo ""
    echo "To run the deployment app:"
    echo "  1. Activate environment: source .venv/bin/activate"
    echo "  2. Run: python deploy-app.py"
    echo ""
    echo "Or simply run: ./run-deploy.sh"
    echo "==============================================="
else
    echo ""
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
