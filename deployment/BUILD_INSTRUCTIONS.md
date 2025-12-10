# 📦 Building Standalone Executable

This guide explains how to build a standalone executable of the Photography Deployment App that can run anywhere on any OS.

## 🎯 Features

- **Portable**: Single executable file, no Python installation required
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Universal File Access**: Can select and deploy JSON files from anywhere on your system
- **No Dependencies**: All required libraries bundled into the executable

## 🏗️ Build Instructions

### Windows

1. Open PowerShell in the `deployment` folder
2. Run the build script:
   ```powershell
   .\build-exe.ps1
   ```
3. Find the executable at: `dist\PhotoDeploymentApp.exe`

### macOS / Linux

1. Open Terminal in the `deployment` folder
2. Make the script executable (first time only):
   ```bash
   chmod +x build-exe.sh
   ```
3. Run the build script:
   ```bash
   ./build-exe.sh
   ```
4. Find the executable at: `dist/PhotoDeploymentApp`

## 📋 Requirements

The build script will automatically install:
- PyInstaller (for creating executables)
- PySide6 (if not already installed)

You only need Python installed on your system to build the executable.

## 🚀 Using the Executable

### Running the App

**Windows:**
```
dist\PhotoDeploymentApp.exe
```

**macOS/Linux:**
```
./dist/PhotoDeploymentApp
```

### Deploying Files

1. Launch the executable
2. Click "Browse" to select any JSON file from anywhere on your computer
3. The app will automatically:
   - Detect the repository location (must be in a git repository)
   - Validate the JSON file
   - Show deployment controls
4. Click "Deploy" to commit and push changes

## 📁 Distribution

You can copy the executable to any location:
- **Windows**: `PhotoDeploymentApp.exe` - ~100-150 MB
- **macOS**: `PhotoDeploymentApp` - ~100-150 MB  
- **Linux**: `PhotoDeploymentApp` - ~100-150 MB

The executable includes all dependencies and can run on any machine with the same OS, even without Python installed.

## ⚙️ Advanced Build Options

### Custom Icon

To add a custom icon, create an `.ico` (Windows) or `.icns` (macOS) file and modify the build script:

```powershell
# In build-exe.ps1 or build-exe.sh, replace:
--icon=NONE
# with:
--icon=path/to/your/icon.ico
```

### Reduce File Size

To create a directory-based executable (smaller but multiple files):

```powershell
# Remove the --onefile flag from the build script
# This creates: dist/PhotoDeploymentApp/ folder with multiple files
```

### Debug Mode

For troubleshooting, remove `--windowed` flag to see console output:

```powershell
python -m PyInstaller --name "PhotoDeploymentApp" --onefile deploy-app-pyside6.py
```

## 🔧 Troubleshooting

### Build Fails

1. Ensure Python 3.8+ is installed
2. Update pip: `python -m pip install --upgrade pip`
3. Clear build cache: Delete `build/` and `dist/` folders, then rebuild

### Executable Won't Run

1. **Windows**: Check Windows Defender/antivirus - may flag unknown executables
2. **macOS**: Right-click → Open (first time only) to bypass Gatekeeper
3. **Linux**: Ensure executable permissions: `chmod +x PhotoDeploymentApp`

### Missing Dependencies

If you see import errors, add hidden imports to the build script:

```powershell
--hidden-import "module_name"
```

## 📊 File Sizes

Approximate executable sizes:
- **Windows**: 120-150 MB (includes PySide6, Qt libraries)
- **macOS**: 130-160 MB (includes frameworks)
- **Linux**: 100-140 MB (includes shared libraries)

## 🔄 Updating the Executable

After making changes to `deploy-app-pyside6.py`:

1. Delete the `build/` and `dist/` folders
2. Run the build script again
3. The new executable will include your changes

## 📝 Notes

- The executable must still be run inside a git repository to perform deployments
- File selection works from anywhere, but deployment requires git
- The app automatically detects the repository root from the selected file's path
- First run may be slower as Qt libraries are extracted to temp directory
