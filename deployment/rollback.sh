#!/bin/bash

# Git Rollback Script
# This script rolls back to the previous commit

# ================================
# CONFIGURATION
# ================================
# Branch name (will use current branch if empty)
TARGET_BRANCH=""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  Git Rollback Script${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Change to repository root
cd "$(dirname "$0")/.." || exit 1
echo -e "${BLUE}Working directory:${NC} $(pwd)"
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

# Show last 5 commits
echo -e "${YELLOW}Last 5 commits:${NC}"
git log --oneline -5
echo ""

# Confirm rollback
echo -e "${RED}WARNING: This will undo the last commit and push to remote!${NC}"
read -p "Are you sure you want to rollback? (yes/no): " confirmation

if [ "$confirmation" != "yes" ]; then
    echo -e "${YELLOW}Rollback cancelled.${NC}"
    exit 0
fi
echo ""

# Reset to previous commit (keep changes in working directory)
echo -e "${BLUE}Rolling back to previous commit...${NC}"
git reset --soft HEAD~1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Reset to previous commit successfully${NC}"
else
    echo -e "${RED}✗ Failed to reset${NC}"
    exit 1
fi
echo ""

# Force push to remote
echo -e "${BLUE}Force pushing to origin/$BRANCH...${NC}"
git push origin "$BRANCH" --force

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Rollback pushed successfully to origin/$BRANCH${NC}"
else
    echo -e "${RED}✗ Failed to push rollback${NC}"
    echo -e "${YELLOW}You may need to manually resolve this.${NC}"
    exit 1
fi
echo ""

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  Rollback Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${CYAN}Note: Your changes are still in the working directory.${NC}"
echo -e "${CYAN}Use 'git status' to see the uncommitted changes.${NC}"
