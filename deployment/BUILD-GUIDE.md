# Photo Deployment App - Multi-Platform Build Guide

This guide explains how to build the Photo Deployment App executable for Windows, macOS, and Linux.

## Prerequisites

All platforms require:
- Python 3.8 or higher
- Git installed and accessible from command line
- Internet connection for dependency installation

## Building for Windows

### Using PowerShell Script

1. Open PowerShell in the `deployment` folder
2. Run the build script:
   ```powershell
   .\build-exe.ps1
   ```
3. The executable will be created at: `dist\PhotoDeploymentApp.exe`

### Manual Build (Windows)

```powershell
# Install dependencies
python -m pip install pyinstaller "PySide6>=6.6.0"

# Build executable
python -m PyInstaller --name PhotoDeploymentApp --onefile --windowed --clean deploy-app-pyside6.py
```

## Building for macOS

### Using Bash Script

1. Open Terminal in the `deployment` folder
2. Make the script executable (first time only):
   ```bash
   chmod +x build-macos.sh
   ```
3. Run the build script:
   ```bash
   ./build-macos.sh
   ```
4. Make the output executable:
   ```bash
   chmod +x dist/PhotoDeploymentApp
   ```
5. The executable will be at: `dist/PhotoDeploymentApp`

### Manual Build (macOS)

```bash
# Install dependencies
python3 -m pip install pyinstaller "PySide6>=6.6.0"

# Build executable
python3 -m PyInstaller --name PhotoDeploymentApp --onefile --windowed --clean deploy-app-pyside6.py

# Make executable
chmod +x dist/PhotoDeploymentApp
```

## Building for Linux (Ubuntu/Debian)

### Using Bash Script

1. Open Terminal in the `deployment` folder
2. Make the script executable (first time only):
   ```bash
   chmod +x build-linux.sh
   ```
3. Run the build script:
   ```bash
   ./build-linux.sh
   ```
4. Make the output executable:
   ```bash
   chmod +x dist/PhotoDeploymentApp
   ```
5. The executable will be at: `dist/PhotoDeploymentApp`

### Manual Build (Linux)

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3-pip libxcb-xinerama0 libxcb-cursor0

# Install Python dependencies
python3 -m pip install pyinstaller "PySide6>=6.6.0"

# Build executable
python3 -m PyInstaller --name PhotoDeploymentApp --onefile --windowed --clean deploy-app-pyside6.py

# Make executable
chmod +x dist/PhotoDeploymentApp
```

## Usage After Building

### Windows
1. Copy `PhotoDeploymentApp.exe` to your git repository root
2. Double-click to run or execute from command line
3. The app will auto-detect the repository and work from there

### macOS / Linux
1. Copy `PhotoDeploymentApp` to your git repository root
2. Run from terminal:
   ```bash
   ./PhotoDeploymentApp
   ```
   Or double-click if your system allows
3. The app will auto-detect the repository and work from there

## Features

All platform versions include:
- ✅ Auto-detects git repository from executable location
- ✅ Creates `data/` folder if missing
- ✅ Only commits `.json` files from `data/` folder
- ✅ Clear error messages with solutions
- ✅ Works in ANY git repository when copied there
- ✅ No Python installation required on target machine

## Executable Sizes

Approximate sizes:
- **Windows**: ~43 MB (.exe)
- **macOS**: ~45-50 MB (app bundle or binary)
- **Linux**: ~45-50 MB (binary)

## Troubleshooting

### macOS: "App is damaged and can't be opened"
Run this command to allow the app:
```bash
xattr -cr dist/PhotoDeploymentApp
```

### Linux: Missing libraries error
Install required libraries:
```bash
sudo apt-get install -y libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0
```

### All Platforms: Git not found
Ensure Git is installed and accessible from command line:
- Windows: Install Git from git-scm.com
- macOS: Install via Homebrew or Xcode Command Line Tools
- Linux: `sudo apt-get install git`

## Cross-Platform Notes

⚠️ **Important**: Executables are platform-specific!
- Windows `.exe` only works on Windows
- macOS executable only works on macOS
- Linux executable only works on Linux

To distribute your app to all platforms, you must build on each platform separately or use a CI/CD service like GitHub Actions.

## Building on GitHub Actions (Advanced)

For automated cross-platform builds, see the repository's GitHub Actions workflow (if configured).

---

**Support**: For issues, check the repository's issue tracker or documentation.
