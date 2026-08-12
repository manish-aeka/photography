# Photography Portfolio Deployment App

## Overview
A user-friendly GUI application for deploying updates to the Anupam Dutta Photography portfolio website.

## Features
- 📁 **File Upload**: Browse and select JSON data file
- ✅ **Auto Validation**: Validates JSON structure against reference file
- 🚀 **One-Click Deployment**: Executes all deployment commands automatically
- 📊 **Progress Tracking**: Real-time deployment progress with detailed logs
- 💾 **Auto Backup**: Creates backup before updating files
- 🎨 **Modern UI**: Clean, professional interface with color-coded status

## Installation

### Option 1: Run from Source
```bash
# Install Python (if not already installed)
# Download from: https://www.python.org/downloads/

# Run the application
python deploy-app.py
```

### Option 2: Build as Executable
```bash
# Run the build script
.\build-deploy-app.ps1

# The executable will be created in the 'dist' folder
# dist\Photography-Portfolio-Deployment.exe
```

## Usage

1. **Launch the Application**
   - Double-click `Photography-Portfolio-Deployment.exe` (if built)
   - Or run `python deploy-app.py`

2. **Select JSON File**
   - Click "🔍 Browse JSON File"
   - Select your updated `anupam-dutta-photography-data-set.json` file
   - The app will automatically validate it

3. **Deploy**
   - If validation passes, click "🚀 Deploy to Production"
   - Confirm the deployment
   - Monitor progress in the log window

4. **Completion**
   - Success message will appear when deployment is complete
   - Check the logs for detailed information

## Validation
The app validates that your JSON file contains all required fields:
- Settings (name, email, phone, etc.)
- Slider images and content
- Categories with images
- Gallery images
- About section with card details

## Requirements
- Python 3.7+ (for running from source)
- PyInstaller (for building executable)
- `anupam-dutta-photography-data-set.json` (reference file)
- `deploy.sh` (deployment script)

## File Structure
```
photography/
├── deploy-app.py                          # Main application
├── build-deploy-app.ps1                   # Build script
├── anupam-dutta-photography-data-set.json # Reference JSON
├── deploy.sh                              # Deployment commands
└── dist/
    └── Photography-Portfolio-Deployment.exe  # Built executable
```

## Troubleshooting

### "Reference file not found"
- Ensure `anupam-dutta-photography-data-set.json` is in the same directory as the app

### "Validation failed"
- Check that your JSON file has all required fields
- Compare structure with the reference file
- Ensure valid JSON syntax (use a JSON validator)

### "Deploy.sh not found"
- The app will still update the JSON file
- Deployment commands will be skipped

## Security
- Creates automatic backups before deployment
- Validates JSON structure before any changes
- Requires user confirmation before deployment
- Detailed logging for audit trail

## Support
For issues or questions, check the deployment logs in the application window.

---
Made with ❤️ for Anupam Dutta Photography
