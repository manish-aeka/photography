#!/bin/bash

###############################################################################
# Photography Portfolio Deployment App - Build Script
# Creates standalone executable using PyInstaller
###############################################################################

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📸 Photography Deployment App Builder${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${YELLOW}📁 Project Root: ${PROJECT_ROOT}${NC}"
echo -e "${YELLOW}📁 Build Directory: ${SCRIPT_DIR}${NC}\n"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"

# Navigate to project root
cd "$PROJECT_ROOT" || exit 1

# Check if virtual environment exists, create if not
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}🔄 Activating virtual environment...${NC}"
source .venv/bin/activate || source .venv/Scripts/activate

# Upgrade pip
echo -e "${BLUE}🔄 Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip install PySide6 pyinstaller

echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Navigate to deployment directory
cd "$SCRIPT_DIR" || exit 1

# Clean previous builds
if [ -d "build" ]; then
    echo -e "${YELLOW}🧹 Cleaning previous build files...${NC}"
    rm -rf build
fi

if [ -d "dist" ]; then
    rm -rf dist
fi

if [ -f "PhotoDeploymentApp.spec" ]; then
    rm -f PhotoDeploymentApp.spec
fi

echo -e "${GREEN}✓ Build directory cleaned${NC}\n"

# Build executable
echo -e "${BLUE}🔨 Building executable with PyInstaller...${NC}\n"
python -m PyInstaller \
    --onefile \
    --windowed \
    --name="PhotoDeploymentApp" \
    --icon=NONE \
    deploy-app.py

# Check if build was successful
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}✅ BUILD SUCCESSFUL!${NC}"
    echo -e "${GREEN}========================================${NC}\n"
    
    echo -e "${GREEN}📦 Executable created at:${NC}"
    echo -e "${BLUE}   ${SCRIPT_DIR}/dist/PhotoDeploymentApp${NC}\n"
    
    # Show file size
    if [ -f "dist/PhotoDeploymentApp" ]; then
        FILE_SIZE=$(du -h "dist/PhotoDeploymentApp" | cut -f1)
        echo -e "${GREEN}📊 File size: ${FILE_SIZE}${NC}\n"
    elif [ -f "dist/PhotoDeploymentApp.exe" ]; then
        FILE_SIZE=$(du -h "dist/PhotoDeploymentApp.exe" | cut -f1)
        echo -e "${GREEN}📊 File size: ${FILE_SIZE}${NC}\n"
    fi
    
    echo -e "${YELLOW}💡 To run the application:${NC}"
    echo -e "   ${BLUE}./dist/PhotoDeploymentApp${NC}\n"
    
else
    echo -e "\n${RED}========================================${NC}"
    echo -e "${RED}❌ BUILD FAILED!${NC}"
    echo -e "${RED}========================================${NC}\n"
    echo -e "${RED}Please check the error messages above.${NC}\n"
    exit 1
fi

# Deactivate virtual environment
deactivate 2>/dev/null

echo -e "${GREEN}✨ Build process completed!${NC}\n"
