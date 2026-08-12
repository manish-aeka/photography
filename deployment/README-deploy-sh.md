# 🚀 Deploy.sh - Auto Git Deploy Script

> Automated Git deployment script for pushing portfolio data changes to your repository.

## 📖 Overview

`deploy.sh` is a bash script that automatically handles the Git workflow for deploying changes to your photography portfolio data. It specifically targets JSON files in the `data/` folder, making it easy to update your portfolio content and push changes to GitHub Pages or other Git-based hosting.

## ✨ Features

- ✅ **Automatic Change Detection** - Only deploys if JSON files in `data/` have changes
- ✅ **Selective File Inclusion** - Deploys only portfolio data, excludes deployment tools and docs
- ✅ **Custom Commit Messages** - Supports user-defined or auto-generated commit messages
- ✅ **Branch Management** - Works with current branch or configured target branch
- ✅ **Color-Coded Output** - Clear visual feedback with colorized terminal output
- ✅ **Error Handling** - Validates directory structure and handles push failures gracefully

## 🚀 Quick Start

### Basic Usage

```bash
# Navigate to deployment folder
cd deployment

# Make the script executable (first time only)
chmod +x deploy.sh

# Run with default commit message
./deploy.sh

# Run with custom commit message
./deploy.sh "Updated portfolio with new photos"
```

The script will:
1. Check for changes in `data/*.json` files
2. Stage only the JSON files from the data folder
3. Commit with your message (or auto-generated timestamp)
4. Push to the current branch

## 🎯 Use Cases

- **Portfolio Updates** - After editing `anupam-dutta-photography-data-set.json`
- **Quick Deployments** - One command to commit and push data changes
- **Automated Workflows** - Integrate into larger deployment pipelines
- **CI/CD Integration** - Use in automated deployment scripts

## ⚙️ Configuration

Edit these variables at the top of `deploy.sh`:

### Target Branch

```bash
# Leave empty to use current branch
TARGET_BRANCH=""

# Or specify a branch
TARGET_BRANCH="main"
```

### Include Files

Files/patterns to include in deployment:

```bash
INCLUDE_FILES=(
    "data/*.json"
)
```

### Exclude Files

Files/patterns to exclude (for reference, not actively used in add operation):

```bash
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
```

## 📝 Examples

### Example 1: Deploy with Auto-Generated Message

```bash
./deploy.sh
# Commits with: "Auto commit: 2026-04-09 14:30:45"
```

### Example 2: Deploy with Custom Message

```bash
./deploy.sh "Added 15 new photos from Japan trip"
```

### Example 3: Deploy to Specific Branch

```bash
# First, configure TARGET_BRANCH in the script
# Then run:
./deploy.sh "Publishing new gallery"
```

## 🔍 What It Does

1. **Directory Validation**
   - Changes to repository root
   - Verifies `data/` folder exists
   - Checks for JSON files

2. **Change Detection**
   - Runs `git status` on `data/*.json`
   - Exits gracefully if no changes found
   - Shows what files have changed

3. **Git Operations**
   - Adds only JSON files from `data/` folder
   - Creates commit with provided or auto-generated message
   - Pushes to origin (sets upstream if needed)

4. **Success Confirmation**
   - Displays color-coded progress
   - Shows successful deployment message
   - Reports branch where changes were pushed

## 📋 Output Examples

### No Changes

```
================================
  Auto Git Deploy Script
================================

Working directory: /Users/photographer/portfolio

No changes to .json files in data/ folder.
Working directory clean for deployment files.
```

### Successful Deployment

```
================================
  Auto Git Deploy Script
================================

Working directory: /Users/photographer/portfolio

Changes in data/ folder:
 M data/anupam-dutta-photography-data-set.json

Using default commit message: Auto commit: 2026-04-09 14:30:45
Using current branch: main

Adding .json files from data/ folder...
  Including: data/*.json
✓ Successfully added 1 file(s)

Committing changes...
✓ Committed successfully

Pushing to origin/main...
✓ Pushed successfully to origin/main

================================
  Deployment Complete!
================================
```

## ⚠️ Prerequisites

- **Git** - Must be installed and configured
- **Bash** - Unix/Linux shell (macOS/Linux/WSL/Git Bash)
- **Repository** - Must be run from within a Git repository
- **Remote** - Repository must have a configured `origin` remote

## 🐛 Troubleshooting

### "Permission denied" Error

```bash
chmod +x deploy.sh
```

### "data/ folder not found" Error

Make sure you're running the script from the `deployment/` folder:

```bash
cd deployment
./deploy.sh
```

### "Failed to push" Error

Check your Git credentials and remote configuration:

```bash
# Verify remote is configured
git remote -v

# Test authentication
git fetch origin
```

### Script Runs But Nothing Happens

This means there are no changes to JSON files in the `data/` folder. The script exits gracefully when the working directory is clean.

## 🔒 What Gets Deployed

**Included:**
- ✅ `data/*.json` - All JSON files in the data folder

**Excluded (not actively filtered, but not added):**
- ❌ Deployment scripts and tools
- ❌ Documentation files
- ❌ Python and PowerShell scripts
- ❌ Test files
- ❌ `.git/` directory

## 💡 Tips

- **Test First**: Use `git status` to see what will be deployed
- **Review Changes**: Run `git diff data/` before deploying
- **Branch Safety**: Create a new branch for major changes
- **Commit Messages**: Use descriptive messages for better history
- **Automation**: Consider adding to package.json scripts or Makefile

## 🔗 Related Scripts

- **setup.sh** - Set up Python environment for deployment app
- **run-deploy.sh** - Launch the GUI deployment application
- **build.sh** - Build standalone deployment executable
- **deploy-app.py** - Python-based deployment GUI

## 📚 Additional Resources

- **Main README**: [README.md](README.md) - Deployment app documentation
- **Cloudinary Setup**: [../docs/CLOUDINARY_SETUP.md](../docs/CLOUDINARY_SETUP.md)
- **Implementation Docs**: [../docs/IMPLEMENTATION_SUMMARY.md](../docs/IMPLEMENTATION_SUMMARY.md)

## 🤝 Contributing

To improve this script:
1. Test your changes thoroughly
2. Update this README if functionality changes
3. Follow existing code style and error handling patterns

---

**Note**: This script is designed for the Photography Portfolio project and specifically targets JSON data files. Modify the `INCLUDE_FILES` array to adapt it for other use cases.
