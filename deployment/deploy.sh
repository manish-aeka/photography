#!/bin/bash

# Auto Git Deploy Script
# This script automatically adds, commits, and pushes changes to the repository

# ================================
# CONFIGURATION
# ================================
# Branch name (will use current branch if empty)
TARGET_BRANCH=""

# Specific files/folders to include in deployment (relative to repository root)
INCLUDE_FILES=(
    "data/*.json"
)

# Files/folders to exclude from deployment (space-separated)
EXCLUDE_FILES=(
    "deployment/"
    "docs/"
    ".git/"
    ".gitignore"
    "*.md"
    "*.ps1"
    "*.py"
    "test-*.html"
)

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  Auto Git Deploy Script${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Change to repository root
cd "$(dirname "$0")/.." || exit 1
echo -e "${BLUE}Working directory:${NC} $(pwd)"
echo ""

# Check if data folder exists
if [ ! -d "data" ]; then
    echo -e "${RED}✗ Error: data/ folder not found in root directory${NC}"
    exit 1
fi

# Check if any JSON files exist in data folder
JSON_FILES=(data/*.json)
if [ ! -e "${JSON_FILES[0]}" ]; then
    echo -e "${RED}✗ Error: No .json files found in data/ folder${NC}"
    exit 1
fi

# Check if there are any changes to JSON files in data folder
DATA_JSON_CHANGES=$(git status --short data/*.json 2>/dev/null)
if [[ -z "$DATA_JSON_CHANGES" ]]; then
    echo -e "${GREEN}No changes to .json files in data/ folder.${NC}"
    echo -e "${BLUE}Working directory clean for deployment files.${NC}"
    exit 0
fi

# Show current status of data JSON files
echo -e "${BLUE}Changes in data/ folder:${NC}"
git status --short data/*.json
echo ""

# Get commit message from user or use default
if [ -z "$1" ]; then
    COMMIT_MSG="Auto commit: $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${BLUE}Using default commit message:${NC} $COMMIT_MSG"
else
    COMMIT_MSG="$1"
    echo -e "${BLUE}Commit message:${NC} $COMMIT_MSG"
fi
echo ""

# Determine target branch
if [ -z "$TARGET_BRANCH" ]; then
    BRANCH=$(git branch --show-current)
    echo -e "${BLUE}Using current branch:${NC} $BRANCH"
else
    BRANCH="$TARGET_BRANCH"
    echo -e "${BLUE}Using configured branch:${NC} $BRANCH"
    
    # Switch to target branch if not already on it
    CURRENT_BRANCH=$(git branch --show-current)
    if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
        echo -e "${BLUE}Switching to branch:${NC} $BRANCH"
        git checkout "$BRANCH"
        if [ $? -ne 0 ]; then
            echo -e "${RED}✗ Failed to switch to branch $BRANCH${NC}"
            exit 1
        fi
        echo -e "${GREEN}✓ Switched to $BRANCH${NC}"
    fi
fi
echo ""

# Add specific files
echo -e "${BLUE}Adding .json files from data/ folder...${NC}"

# Add only the JSON files from data folder
ADDED_COUNT=0
for file in "${INCLUDE_FILES[@]}"; do
    # Check if file pattern matches any files
    if ls $file 1> /dev/null 2>&1; then
        echo -e "  ${GREEN}Including:${NC} $file"
        git add $file
        if [ $? -eq 0 ]; then
            ADDED_COUNT=$((ADDED_COUNT + 1))
        else
            echo -e "${RED}✗ Failed to add $file${NC}"
            exit 1
        fi
    else
        echo -e "  ${RED}Warning: No files matching $file${NC}"
    fi
done

if [ $ADDED_COUNT -eq 0 ]; then
    echo -e "${RED}✗ No files were added${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Successfully added $ADDED_COUNT file(s)${NC}"
echo ""

# Commit changes
echo -e "${BLUE}Committing changes...${NC}"
git commit -m "$COMMIT_MSG"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Committed successfully${NC}"
else
    echo -e "${RED}✗ Failed to commit${NC}"
    exit 1
fi
echo ""

# Push to remote
echo -e "${BLUE}Pushing to origin/$BRANCH...${NC}"
git push origin "$BRANCH"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Pushed successfully to origin/$BRANCH${NC}"
else
    echo -e "${RED}✗ Failed to push${NC}"
    echo -e "${BLUE}Trying to set upstream...${NC}"
    git push -u origin "$BRANCH"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Pushed successfully with upstream set${NC}"
    else
        echo -e "${RED}✗ Failed to push${NC}"
        exit 1
    fi
fi
echo ""

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}================================${NC}"
