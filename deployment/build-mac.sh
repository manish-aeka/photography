#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Build script for macOS (.app bundle, optional codesign and dmg)
# Usage:
#   ./build-mac.sh            # build .app
#   CODESIGN_IDENTITY="Your Identity" ./build-mac.sh  # build + codesign
#   CREATE_DMG=1 ./build-mac.sh  # additionally create a DMG
#
###############################################################################

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📦 macOS Build: PhotoDeploymentApp${NC}"
echo -e "${BLUE}========================================${NC}\n"

if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}❌ This script must be run on macOS (Darwin).${NC}"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${YELLOW}📁 Project Root: ${PROJECT_ROOT}${NC}"
echo -e "${YELLOW}📁 Build Directory: ${SCRIPT_DIR}${NC}\n"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"

cd "$PROJECT_ROOT" || exit 1

# Create / activate venv
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

echo -e "${BLUE}🔄 Activating virtual environment...${NC}"
source .venv/bin/activate

echo -e "${BLUE}🔄 Upgrading pip and installing build deps...${NC}"
python -m pip install --upgrade pip
pip install --upgrade pyinstaller PySide6

echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Navigate to deployment dir
cd "$SCRIPT_DIR" || exit 1

# Clean previous build artifacts
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

# Determine icon if present
ICON_ARG=""
if [ -f "icon.icns" ]; then
    ICON_ARG="--icon=icon.icns"
elif [ -f "../assets/icon.icns" ]; then
    ICON_ARG="--icon=../assets/icon.icns"
fi

echo -e "${BLUE}🔨 Building macOS .app with PyInstaller...${NC}\n"

# Create an application bundle (onedir + windowed creates .app on macOS)
python -m PyInstaller \
    --windowed \
    --name="PhotoDeploymentApp" \
    --osx-bundle-identifier="com.photodeployment.app" \
    ${ICON_ARG} \
    deploy-app.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ PyInstaller build failed.${NC}"
    exit 1
fi

APP_PATH="dist/PhotoDeploymentApp.app"

if [ -d "$APP_PATH" ]; then
    echo -e "\n${GREEN}✅ .app bundle created at: ${APP_PATH}${NC}\n"
else
    echo -e "\n${RED}❌ Expected .app bundle not found at ${APP_PATH}${NC}\n"
    exit 1
fi

# Optional codesign
if [ -n "${CODESIGN_IDENTITY-}" ]; then
    echo -e "${BLUE}🔐 Codesigning with identity: ${CODESIGN_IDENTITY}${NC}"
    if ! command -v codesign &> /dev/null; then
        echo -e "${RED}❌ codesign tool not found (Xcode command-line tools required).${NC}"
        exit 1
    fi

    echo -e "${YELLOW}🛡️  Signing...${NC}"
    codesign --timestamp --options runtime --deep --force --sign "$CODESIGN_IDENTITY" "$APP_PATH"
    echo -e "${GREEN}✓ Codesign completed${NC}"
    echo -e "${BLUE}✔ Verifying signature...${NC}"
    codesign --verify --deep --strict --verbose=2 "$APP_PATH" || true
    spctl -a -t exec -vv "$APP_PATH" || true
    echo -e "${GREEN}✓ Codesign verification finished${NC}\n"
fi

# Optional DMG creation
if [ "${CREATE_DMG-}" = "1" ] || [ "${CREATE_DMG-}" = "true" ]; then
    DMG_OUT="dist/PhotoDeploymentApp.dmg"
    echo -e "${BLUE}📦 Creating DMG: ${DMG_OUT}${NC}"
    hdiutil create -volname "PhotoDeploymentApp" -srcfolder "$APP_PATH" -ov -format UDZO "$DMG_OUT"
    echo -e "${GREEN}✓ DMG created at: ${DMG_OUT}${NC}\n"
fi

echo -e "${GREEN}✨ macOS build process completed!${NC}\n"

# Deactivate venv
deactivate 2>/dev/null || true

echo -e "${YELLOW}💡 Next steps:${NC}"
echo -e "  - If you want the app notarized, provide Apple notarization credentials and use xcrun notarytool or altool to submit the DMG/app for notarization."
echo -e "  - Example: CODESIGN_IDENTITY=\"Developer ID Application: Your Name (TEAMID)\" CREATE_DMG=1 ./build-mac.sh"
