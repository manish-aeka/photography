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

# Check if there are any changes
if [[ -z $(git status -s) ]]; then
    echo -e "${GREEN}No changes to commit. Working directory clean.${NC}"
    exit 0
fi

# Show current status
echo -e "${BLUE}Current Status:${NC}"
git status --short
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
echo -e "${BLUE}Adding specific files to deployment...${NC}"

for file in "${INCLUDE_FILES[@]}"; do
    echo -e "  ${GREEN}Including:${NC} $file"
    git add $file
done

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Files added successfully${NC}"
else
    echo -e "${RED}✗ Failed to add files${NC}"
    exit 1
fi
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
