#!/bin/bash

# Auto Git Deploy Script
# This script automatically adds, commits, and pushes changes to the repository

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  Auto Git Deploy Script${NC}"
echo -e "${BLUE}================================${NC}"
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

# Get current branch
BRANCH=$(git branch --show-current)
echo -e "${BLUE}Current branch:${NC} $BRANCH"
echo ""

# Add only JSON files and images folder
echo -e "${BLUE}Adding JSON files and images folder...${NC}"
git add *.json
git add images/

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
