# 📦 Photography Deployment App - Standalone Executable

## ✅ Build Complete!

Your standalone executable has been successfully created!

**Location:** `dist\PhotoDeploymentApp.exe`  
**Size:** ~45 MB  
**Platform:** Windows (x64)

## 🚀 How to Use

### Running the Executable

Simply double-click `PhotoDeploymentApp.exe` or run from command line:

```powershell
.\dist\PhotoDeploymentApp.exe
```

### Deploying Files

1. **Launch the app** - Double-click the executable
2. **Browse for JSON file** - Click "Browse" and select your portfolio JSON file from anywhere
3. **Validate** - The app automatically validates your JSON file structure
4. **Review** - Check the Quick Stats panel for validation status and any missing fields
5. **Deploy** - Click "Deploy" to commit and push changes to your repository

### Key Features

✨ **Portable** - No Python installation required on target machine  
✨ **Universal File Access** - Select JSON files from any location  
✨ **Smart Validation** - Checks portfolio structure and lists missing fields  
✨ **Git Integration** - Automatically commits only `.json` files from `data/` folder  
✨ **Progress Tracking** - Real-time deployment progress with 6-step process

## 📁 Distribution

You can copy `PhotoDeploymentApp.exe` to:
- Any folder on your computer
- USB drive for portable use
- Network share for team access
- Different Windows machines (no installation needed)

### System Requirements

- **OS:** Windows 10/11 (64-bit)
- **Git:** Must be installed and in PATH
- **Repository:** Must be run inside a git repository for deployment features

## 🔧 Important Notes

### What Gets Committed

The app will **ONLY** commit `.json` files from the `data/` folder:
- ✅ `data/*.json` - All JSON files in data folder
- ❌ Other files - Ignored
- ❌ Other folders - Ignored

### Repository Detection

- The app automatically detects the git repository from the selected file's path
- You can select JSON files from anywhere, but they should be part of a git repository
- Deployment requires the repository to have a remote origin configured

### Validation

The app validates three JSON structures:

1. **Portfolio Dictionary:**
   - `about.title`, `about.description`
   - `slider-content.heading`, `slider-content.description`
   - `categories[]`, `slider-images[]`, `gallery-images[]`

2. **Photo Items Array:**
   - Each item: `id`, `title`, `category`, `imageUrl`, `description`

3. **Single Photo Item:**
   - Required: `id`, `title`, `category`, `imageUrl`, `description`
   - Optional: `date`, `location`, `camera`, `lens`, `settings`, `tags`, `featured`

Missing optional fields will show as warnings (yellow) but won't block deployment.

## 🛠️ Rebuilding the Executable

If you make changes to `deploy-app-pyside6.py`, rebuild with:

```powershell
.\build-exe.ps1
```

Or manually:

```powershell
python -m PyInstaller --name PhotoDeploymentApp --onefile --noconfirm deploy-app-pyside6.py
```

### Build Options

**Console Mode (default):**
```powershell
--onefile --noconfirm
```
Shows console window for debugging

**Windowed Mode (no console):**
```powershell
--onefile --windowed --noconfirm
```
Hides console window (production mode)

**With Custom Icon:**
```powershell
--onefile --windowed --icon=icon.ico --noconfirm
```
Adds custom icon to executable

## 📊 File Structure

```
deployment/
├── dist/
│   └── PhotoDeploymentApp.exe    ← Your standalone executable
├── build/                         ← Build artifacts (can be deleted)
├── deploy-app-pyside6.py         ← Source code
├── build-exe.ps1                 ← Build script (Windows)
├── build-exe.sh                  ← Build script (Unix)
└── PhotoDeploymentApp.spec       ← PyInstaller configuration
```

## ⚡ Quick Start Guide

1. **First Time Setup:**
   - No setup needed! Just run the .exe file

2. **Select JSON File:**
   - Click "Browse" button
   - Navigate to your JSON file (can be anywhere)
   - File is automatically validated

3. **Check Validation:**
   - Green ✓ = All good, ready to deploy
   - Yellow ⚠️ = Missing optional fields (can still deploy)
   - Red ✗ = Invalid structure (fix required)

4. **Deploy:**
   - Click "Deploy" button
   - Confirm the action
   - Watch progress (6 steps)
   - Get success notification

## 🐛 Troubleshooting

### Executable Won't Run

**Windows Defender/Antivirus:**
- First-time executables may trigger security warnings
- Click "More info" → "Run anyway"
- Or add exception in Windows Defender

**Missing Git:**
```
❌ Git is not installed or not in PATH
```
- Install Git: https://git-scm.com/download/win
- Ensure Git is added to PATH during installation

### Deployment Issues

**Not a Git Repository:**
```
❌ fatal: not a git repository
```
- Ensure the JSON file is inside a git repository
- Navigate to repository root and initialize: `git init`

**No Remote Origin:**
```
❌ fatal: 'origin' does not appear to be a git repository
```
- Add remote: `git remote add origin <repository-url>`

**Permission Denied:**
- Check git credentials
- Ensure you have push access to the repository

### Validation Errors

**Invalid JSON:**
- Check JSON syntax with a validator
- Ensure proper formatting and no trailing commas

**Missing Required Fields:**
- Review validation warnings in Quick Stats panel
- Add required fields to JSON structure

## 🎯 Production Deployment

For end users, provide:

1. **PhotoDeploymentApp.exe** - The executable
2. **Brief instructions:**
   ```
   1. Double-click PhotoDeploymentApp.exe
   2. Click Browse and select your JSON file
   3. Click Deploy
   ```

No Python, no dependencies, no installation required!

## 📝 Version Information

- **App Version:** 1.0.0
- **Python:** 3.12.10
- **PySide6:** 6.10.1
- **PyInstaller:** 6.12.0
- **Platform:** Windows x64

---

**Built with ❤️ using PySide6 and PyInstaller**
