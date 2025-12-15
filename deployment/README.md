# 📸 Photography Portfolio - Deployment Tool

> Automated deployment tool for managing and deploying your photography portfolio with ease.

## 🚀 Quick Start

Get up and running in seconds after cloning the repository:

```bash
cd deployment
chmod +x setup.sh run-deploy.sh
./setup.sh       # One-time setup
./run-deploy.sh  # Launch the app
```

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- **pip** (comes with Python)
- Internet connection (for initial setup)

## 🔧 What Does Setup Do?

The setup script automatically:

1. ✅ Verifies Python installation
2. ✅ Creates isolated virtual environment (`.venv`)
3. ✅ Upgrades pip to latest version
4. ✅ Installs all required dependencies
5. ✅ Confirms successful installation

## 📦 Dependencies

All dependencies are installed automatically via `requirements.txt`:

| Package | Version | Purpose |
|---------|---------|---------|
| **PyInstaller** | 6.0.0+ | Build standalone executables |
| **Requests** | 2.31.0+ | HTTP operations and API calls |
| **PySide6** | 6.0.0+ | Modern Qt-based GUI framework |

## 🛠️ Manual Installation

Prefer to do it yourself? Follow these steps:

```bash
# 1. Navigate to deployment folder
cd deployment

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run the application
python deploy-app.py
```

## 📂 Project Structure

```
deployment/
├── deploy-app.py          # Main deployment application
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
├── run-deploy.sh         # Run script
├── build.sh              # Build executable script
├── .venv/                # Virtual environment (auto-generated)
└── README.md             # This file
```

## 🐛 Troubleshooting

### Python not found
Install Python via package manager:
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# macOS
brew install python3
```

### Permission denied
```bash
chmod +x setup.sh run-deploy.sh
```

### Dependencies fail to install
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then retry
pip install -r requirements.txt
```

### Virtual environment issues
```bash
# Remove and recreate
rm -rf .venv

# Run setup again
./setup.sh
```

## 💡 Usage Tips

- **First time?** Run `./setup.sh` once
- **Subsequent runs:** Use `./run-deploy.sh`
- **Building executable:** Run `./build.sh`
- **Clean install:** Delete `.venv` folder and re-run setup

## 🤝 Contributing

Found a bug or want to improve something? Feel free to open an issue or submit a pull request!

## 📄 License

This deployment tool is part of the Photography Portfolio project.
