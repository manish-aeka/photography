# Photography Portfolio Deployment Tool (PySide6)

Professional GUI application for deploying photography portfolio data to Git repositories.

## Features

### Modern UI Design
- **Dark Theme**: Professional dark theme with gradient buttons
- **Responsive Layout**: Adaptive interface with proper spacing and alignment
- **Real-time Feedback**: Live console output with color-coded messages
- **Progress Tracking**: Visual progress bar with step-by-step status

### Deployment Capabilities
- **Git Integration**: Automatic commit and push to remote repository
- **JSON File Management**: Deploy data files to production
- **Branch Control**: Target specific branches or use current branch
- **Error Handling**: Comprehensive error detection and reporting

### User Experience
- **File Browser**: Easy file selection with native dialogs
- **Confirmation Dialogs**: Safety checks before deployment
- **Status Messages**: Color-coded console output (success/warning/error)
- **Loading States**: Clear visual feedback during operations

## Installation

### Prerequisites
- Python 3.8 or higher
- Git installed and configured
- Internet connection for remote push

### Setup Steps

1. **Install Dependencies**
   ```powershell
   cd deployment
   .\setup-pyside6.ps1
   ```

   Or manually:
   ```powershell
   pip install PySide6>=6.6.0
   ```

2. **Verify Installation**
   ```powershell
   python -c "from PySide6 import QtWidgets; print('PySide6 installed successfully')"
   ```

## Usage

### Launch Application
```powershell
python deploy-app-pyside6.py
```

### Deployment Process

1. **Select File**
   - Click "Browse Files" button
   - Navigate to your JSON data file
   - Select the file to deploy

2. **Review Configuration**
   - Check target branch displayed
   - Verify file path is correct

3. **Deploy**
   - Click "Deploy to Production" button
   - Confirm deployment in dialog
   - Monitor progress in console

4. **Monitor Progress**
   - Watch real-time console output
   - Track progress bar (0-100%)
   - View current step indicator

### Deployment Steps

The deployment process includes:

1. **Update JSON File** (0-10%)
   - Copy selected file to `data/` folder
   - Verify file integrity

2. **Check Git Status** (10-20%)
   - Verify Git installation
   - Check repository status

3. **Stage Changes** (20-35%)
   - Add modified files to Git
   - Detect changes in data folder

4. **Commit Changes** (35-50%)
   - Create commit with timestamp
   - Generate descriptive message

5. **Push to Remote** (50-75%)
   - Push to configured branch
   - Handle authentication

6. **Verify Deployment** (75-100%)
   - Final status check
   - Confirm successful deployment

## Configuration

Edit the constants at the top of `deploy-app-pyside6.py`:

```python
# Target branch (empty = current branch)
TARGET_BRANCH = ""

# Files to include in deployment
INCLUDE_FILES = ["data/*.json"]
```

## UI Components

### Header Section
- Application title with icon
- Professional subtitle
- Clear branding

### File Selection
- File path display (monospace font)
- Browse button with icon
- Visual feedback on selection

### Deployment Controls
- Branch information display
- Current step indicator
- Progress bar with percentage
- Primary action button

### Console Output
- Dark terminal-style background
- Color-coded messages:
  - 🟢 Green: Success messages
  - 🔵 Blue: Information
  - 🟡 Yellow: Warnings
  - 🔴 Red: Errors
- Auto-scroll to latest output
- Monospace font for readability

## Color Scheme

### Theme Colors
- **Background**: `#0f172a` (Dark slate)
- **Surface**: `#1e293b` (Lighter slate)
- **Primary**: `#3b82f6` (Blue)
- **Success**: `#10b981` (Green)
- **Warning**: `#fbbf24` (Amber)
- **Error**: `#ef4444` (Red)

### Text Colors
- **Primary Text**: `#f1f5f9` (Light)
- **Secondary Text**: `#cbd5e1` (Medium)
- **Muted Text**: `#94a3b8` (Gray)

## Threading Architecture

### Worker Thread Pattern
- Separate thread for Git operations
- Signal-based communication with UI
- Non-blocking UI updates

### Signals
- `log`: Console message with color
- `progress`: Progress bar value (0-100)
- `step`: Current step description
- `finished`: Completion status and message

## Error Handling

### Common Issues

**Git Not Found**
- Console shows: "Git is not installed"
- Solution: Install Git and add to PATH

**No Changes to Commit**
- Console shows: "No changes to commit"
- This is normal if file unchanged

**Push Failed**
- Check network connection
- Verify Git credentials
- Ensure branch exists on remote

**File Access Error**
- Check file permissions
- Ensure file is not locked
- Verify path is correct

## Advantages Over Tkinter Version

### Visual Design
- ✅ Modern gradient buttons
- ✅ Professional dark theme
- ✅ Better font rendering
- ✅ Native look and feel

### Performance
- ✅ Better signal/slot mechanism
- ✅ More efficient rendering
- ✅ Smoother animations

### Features
- ✅ Built-in dialog system
- ✅ Better file dialogs
- ✅ Rich text formatting
- ✅ Professional widgets

### Code Quality
- ✅ Cleaner signal handling
- ✅ Better separation of concerns
- ✅ Type-safe connections
- ✅ More maintainable

## Development

### Project Structure
```
deployment/
├── deploy-app-pyside6.py      # Main application
├── requirements-pyside6.txt    # Dependencies
├── setup-pyside6.ps1          # Installation script
└── README-PYSIDE6.md          # This file
```

### Key Classes

**WorkerSignals**
- Qt signal container
- Thread-safe communication

**DeploymentWorker**
- Background thread for Git operations
- Emits signals for UI updates

**ModernButton**
- Custom styled button
- Primary/secondary variants
- Hover effects

**DeploymentApp**
- Main window class
- UI setup and event handling
- Signal/slot connections

## License

Part of the Photography Portfolio project.

## Support

For issues or questions:
1. Check console output for error details
2. Verify Git configuration
3. Ensure proper file permissions
4. Review deployment logs
