# Photography Portfolio Deployment Tool

## Quick Start

After cloning this repository, follow these steps:

### Windows
1. **Install Dependencies:**
   ```bash
   cd deployment
   setup.bat
   ```

2. **Run Deployment App:**
   ```bash
   run-deploy.bat
   ```

### Linux/Mac
1. **Install Dependencies:**
   ```bash
   cd deployment
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Run Deployment App:**
   ```bash
   chmod +x run-deploy.sh
   ./run-deploy.sh
   ```

## Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python deploy-app.py
```

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## What Gets Installed?

- **PyInstaller** - For building standalone executables
- **Requests** - For HTTP operations

All dependencies are listed in `requirements.txt`
