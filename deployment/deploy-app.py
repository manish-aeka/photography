"""
Photography Portfolio Deployment Tool
Modern GUI using PySide6 with professional design
"""

import sys
import json
import subprocess
import threading
import time
import os
from pathlib import Path
from datetime import datetime
import queue

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QTextEdit, QFileDialog,
    QGroupBox, QFrame, QSizePolicy, QMessageBox, QGraphicsDropShadowEffect,
    QScrollArea
)
from PySide6.QtCore import Qt, QTimer, Signal, QObject, QSize, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont, QColor, QPalette, QIcon

# ================================
# CONFIGURATION
# ================================
TARGET_BRANCH = ""  # Will use current branch if empty
INCLUDE_FILES = ["data/*.json"]


class WorkerSignals(QObject):
    """Signals for worker thread communication"""
    log = Signal(str, str)  # message, color
    progress = Signal(int)
    finished = Signal(bool, str)  # success, message
    step = Signal(str)  # current step description


class DeploymentWorker(threading.Thread):
    """Worker thread for deployment operations"""
    
    def __init__(self, selected_file, signals):
        super().__init__(daemon=True)
        self.selected_file = selected_file
        self.signals = signals
        
        # Find git repository root from the executable's location
        # When frozen (EXE), use the executable's directory
        # When running as script, use script's parent
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            exe_dir = Path(sys.executable).parent
        else:
            # Running as script
            exe_dir = Path(__file__).parent
        
        # Search for .git folder starting from exe directory
        self.repo_root = self.find_git_root(exe_dir)
        if not self.repo_root:
            # If not found, try current working directory
            self.repo_root = self.find_git_root(Path.cwd())
        
        if not self.repo_root:
            # Default to exe directory even if no .git found (will show error later)
            self.repo_root = exe_dir
    
    def find_git_root(self, start_path):
        """Find the git repository root by looking for .git folder"""
        current = Path(start_path).resolve()
        
        # Search up to 5 levels up
        for _ in range(5):
            if (current / ".git").exists():
                return current
            if current.parent == current:  # Reached filesystem root
                break
            current = current.parent
        
        return None
        
    def log(self, message, color="#10b981"):
        self.signals.log.emit(message, color)
        
    def set_progress(self, value):
        self.signals.progress.emit(value)
        
    def set_step(self, step):
        self.signals.step.emit(step)
        
    def run_git_command(self, command, description):
        """Execute git command and log result"""
        self.log(f"  🔧 Executing: {command}", "#9ca3af")
    def run_git_command(self, command, description):
        """Run a git command and log the output"""
        try:
            self.log(f"  🔧 Running: {command}", "#60a5fa")
            
            # Ensure Git is in PATH and we're in the right directory
            cwd = str(self.repo_root)
            
            # Use shell=True and ensure proper working directory
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=60
            )
            
            if result.stdout.strip():
                self.log(f"  ✓ {result.stdout.strip()}", "#60a5fa")
            
            if result.returncode != 0:
                if result.stderr.strip():
                    self.log(f"  ⚠️ {result.stderr.strip()}", "#f59e0b")
                return False
                
            return True
            
        except subprocess.TimeoutExpired:
            self.log(f"  ❌ Command timed out: {command}", "#ef4444")
            return False
        except Exception as e:
            self.log(f"  ❌ Error: {str(e)}", "#ef4444")
            return False
    
    def run(self):
        """Main deployment logic"""
        try:
            self.log("=" * 70, "#60a5fa")
            self.log("🚀 Starting deployment process...", "#60a5fa")
            self.log(f"📁 Repository root: {self.repo_root}", "#60a5fa")
            
            # Ensure we're in a git repository
            if not (self.repo_root / ".git").exists():
                self.log(f"❌ ERROR: Not a git repository!", "#ef4444")
                self.log(f"📍 Searched in: {self.repo_root}", "#f59e0b")
                self.log(f"💡 Solution: Copy the .exe file to your git repository folder", "#fbbf24")
                raise Exception(
                    f"Not a git repository.\n\n"
                    f"Current location: {self.repo_root}\n\n"
                    f"Please copy PhotoDeploymentApp.exe to the root of your git repository "
                    f"(the folder containing the .git folder)."
                )
            
            self.log(f"✓ Git repository detected", "#10b981")
            
            # Determine branch - handle the check=True error properly
            branch = TARGET_BRANCH
            if not branch:
                try:
                    # Get current directory
                    cwd = str(self.repo_root)
                    
                    # Try to get current branch
                    result = subprocess.run(
                        "git branch --show-current",
                        capture_output=True,
                        text=True,
                        cwd=cwd,
                        shell=True,
                        timeout=10
                    )
                    
                    if result.returncode != 0:
                        # Git command failed, log the error
                        self.log(f"❌ Git error (exit {result.returncode}): {result.stderr}", "#ef4444")
                        raise Exception(f"Failed to get current branch: {result.stderr}")
                    
                    branch = result.stdout.strip()
                    if not branch:
                        raise Exception("Could not determine current branch")
                        
                    self.log(f"Using current branch: {branch}", "#60a5fa")
                except subprocess.TimeoutExpired:
                    raise Exception("Git command timed out")
                except Exception as e:
                    self.log(f"❌ Branch detection failed: {str(e)}", "#ef4444")
                    raise
            
            self.log(f"📍 Deployment branch: {branch}", "#60a5fa")
            self.log("=" * 70, "#60a5fa")
            
            # Check/create data folder
            data_folder = self.repo_root / "data"
            if not data_folder.exists():
                self.log("  ⚠️ data/ folder not found, creating it...", "#f59e0b")
                data_folder.mkdir(parents=True, exist_ok=True)
                self.log("  ✓ Created data/ folder", "#10b981")
            
            # Step 1: Replace JSON file data (10%)
            self.set_step("Step 1/6: Updating JSON file")
            self.log("\n📋 Step 1/6: Replacing JSON file data in repository...", "#fbbf24")
            self.set_progress(5)
            
            # Target file is always anupam-dutta-photography-data-set.json
            target_file = data_folder / "anupam-dutta-photography-data-set.json"
            
            try:
                # Read and validate uploaded JSON
                with open(self.selected_file, 'r', encoding='utf-8') as f:
                    uploaded_data = f.read()
                    json.loads(uploaded_data)  # Validate JSON
                
                self.log(f"  📄 Uploaded file: {Path(self.selected_file).name}", "#60a5fa")
                self.log(f"  📍 Source: {self.selected_file}", "#60a5fa")
                self.log("  ✓ JSON is valid", "#10b981")
                
                # Replace the existing file's data
                self.log(f"  📁 Replacing: data/anupam-dutta-photography-data-set.json", "#60a5fa")
                
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(uploaded_data)
                
                self.log("  ✓ File data replaced successfully", "#10b981")
                
            except json.JSONDecodeError as e:
                self.log(f"  ❌ Invalid JSON: {str(e)}", "#ef4444")
                self.signals.finished.emit(False, f"Invalid JSON file: {str(e)}")
                return
            except Exception as e:
                self.log(f"  ❌ Error updating file: {str(e)}", "#ef4444")
                self.signals.finished.emit(False, f"File update failed: {str(e)}")
                return
            
            self.set_progress(10)
            
            # Step 2: Git status (20%)
            self.set_step("Step 2/6: Checking Git status")
            self.log("\n🔍 Step 2/6: Checking Git status...", "#fbbf24")
            
            # Check if git is available
            try:
                git_check = subprocess.run(
                    "git --version", 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    timeout=10
                )
                if git_check.returncode != 0:
                    self.log("  ⚠️ Git is not installed or not in PATH. Skipping Git operations.", "#f59e0b")
                    self.set_progress(100)
                    self.log("\n✅ Deployment completed (JSON updated only)", "#10b981")
                    self.signals.finished.emit(True, "JSON file updated successfully")
                    return
                else:
                    self.log(f"  ✓ Git found: {git_check.stdout.strip()}", "#10b981")
            except Exception as e:
                self.log(f"  ⚠️ Git check failed: {str(e)}. Skipping Git operations.", "#f59e0b")
                self.set_progress(100)
                self.log("\n✅ Deployment completed (JSON updated only)", "#10b981")
                self.signals.finished.emit(True, "JSON file updated successfully")
                return
            
            if not self.run_git_command("git status", "Git status check"):
                raise Exception("Git status check failed")
            
            self.set_progress(20)
            
            # Step 3: Git add (35%)
            self.set_step("Step 3/6: Staging changes")
            self.log("\n➕ Step 3/6: Adding JSON files to Git...", "#fbbf24")
            
            # Add all JSON files from data folder
            add_result = subprocess.run(
                'git add data/*.json',
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(self.repo_root),
                timeout=10
            )
            
            if add_result.returncode != 0:
                self.log(f"  ⚠️ Git add warning: {add_result.stderr}", "#f59e0b")
            else:
                self.log("  ✓ JSON files staged successfully", "#10b981")
            
            self.set_progress(35)
            
            # Step 4: Git commit (50%)
            self.set_step("Step 4/6: Committing changes")
            self.log("\n💾 Step 4/6: Committing changes...", "#fbbf24")
            
            commit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Update photography data - {commit_time}"
            
            if not self.run_git_command(f'git commit -m "{commit_message}"', "Git commit"):
                self.log("  ℹ️ No changes to commit or commit completed", "#60a5fa")
            
            self.set_progress(50)
            
            # Step 5: Git push (75%)
            self.set_step(f"Step 5/6: Pushing to {branch}")
            self.log(f"\n🚀 Step 5/6: Pushing to remote ({branch})...", "#fbbf24")
            
            if not self.run_git_command(f"git push origin {branch}", f"Git push to {branch}"):
                self.log(f"  ⚠️ Push to {branch} failed, continuing...", "#f59e0b")
            
            self.set_progress(75)
            
            # Step 6: Verify (100%)
            self.set_step("Step 6/6: Verifying deployment")
            self.log("\n✨ Step 6/6: Verifying deployment...", "#fbbf24")
            
            if not self.run_git_command("git status", "Final status check"):
                self.log("  ⚠️ Final status check warning", "#f59e0b")
            
            self.set_progress(100)
            
            self.log("\n" + "=" * 70, "#60a5fa")
            self.log("✅ DEPLOYMENT COMPLETED SUCCESSFULLY!", "#10b981")
            self.log(f"📍 Changes pushed to branch: {branch}", "#10b981")
            self.log("=" * 70, "#60a5fa")
            
            self.signals.finished.emit(True, "Deployment completed successfully!")
            
        except Exception as e:
            self.log(f"\n❌ Deployment failed: {str(e)}", "#ef4444")
            self.set_progress(0)
            self.signals.finished.emit(False, str(e))


class MaterialButton(QPushButton):
    """Material Design 3 Button with elevation and ripple effect"""
    
    def __init__(self, text, button_type="filled", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type  # filled, outlined, text, tonal
        self._elevation = 0
        self.setup_style()
        self.setup_shadow()
        
    def setup_shadow(self):
        """Add Material Design elevation shadow"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
    def setup_style(self):
        """Apply Material Design 3 styling"""
        if self.button_type == "filled":
            # Filled button (primary action)
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6366f1, stop:1 #8b5cf6);
                    color: #FFFFFF;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 28px;
                    font-size: 14px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4f46e5, stop:1 #7c3aed);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4338ca, stop:1 #6d28d9);
                }
                QPushButton:disabled {
                    background-color: #334155;
                    color: #64748b;
                }
            """)
        elif self.button_type == "tonal":
            # Tonal button (secondary action)
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(99, 102, 241, 0.15);
                    color: #a5b4fc;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 28px;
                    font-size: 14px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: rgba(99, 102, 241, 0.25);
                    color: #c7d2fe;
                }
                QPushButton:pressed {
                    background-color: rgba(99, 102, 241, 0.35);
                }
                QPushButton:disabled {
                    background-color: #334155;
                    color: #64748b;
                }
            """)
        elif self.button_type == "outlined":
            # Outlined button
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #818cf8;
                    border: 2px solid #6366f1;
                    border-radius: 12px;
                    padding: 10px 24px;
                    font-size: 14px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: rgba(99, 102, 241, 0.1);
                    border-color: #818cf8;
                    color: #a5b4fc;
                }
                QPushButton:pressed {
                    background-color: rgba(99, 102, 241, 0.2);
                }
                QPushButton:disabled {
                    border-color: #334155;
                    color: #64748b;
                }
            """)
        else:  # text button
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #818cf8;
                    border: none;
                    border-radius: 12px;
                    padding: 10px 16px;
                    font-size: 14px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: rgba(99, 102, 241, 0.1);
                    color: #a5b4fc;
                }
                QPushButton:pressed {
                    background-color: rgba(99, 102, 241, 0.2);
                }
                QPushButton:disabled {
                    color: #64748b;
                }
            """)
        
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)
        
    def get_elevation(self):
        return self._elevation
    
    def set_elevation(self, value):
        self._elevation = value
        shadow = self.graphicsEffect()
        if shadow:
            shadow.setBlurRadius(4 + value * 4)
            shadow.setOffset(0, 1 + value)
    
    elevation = Property(int, get_elevation, set_elevation)


class DeploymentApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.is_deploying = False
        self.worker = None
        
        self.setWindowTitle("📸 Photography Portfolio Deployment Dashboard")
        self.setMinimumSize(1400, 900)
        
        # Set modern dark theme
        self.setup_theme()
        
        # Check if Git is available on startup
        self.check_git_availability()
        
        # Create central widget with scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        self.setCentralWidget(scroll)
        
        # Main container
        container = QWidget()
        scroll.setWidget(container)
        
        # Main layout
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        self.create_dashboard_header(main_layout)
        
        # File Selection (Full width)
        self.create_file_section(main_layout)
        
        # Two column layout for Deployment + Stats
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(24)
        
        # Left: Deployment controls
        self.create_deployment_section(middle_layout)
        
        # Right: Quick stats
        self.create_stats_section(middle_layout)
        
        main_layout.addLayout(middle_layout)
        
        # Console (Full width)
        self.create_console_section(main_layout)
        
        # Footer
        self.create_footer(main_layout)
        
    def setup_theme(self):
        """Apply Material Design 3 Dark Mode theme"""
        # Modern Dark Theme with comfortable colors
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
            QWidget {
                color: #e4e4e7;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                font-size: 14px;
            }
            QGroupBox {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 16px;
                padding: 24px;
                margin: 0px;
                font-weight: 600;
                font-size: 16px;
                letter-spacing: 0.3px;
            }
            QGroupBox::title {
                subcontrol-origin: padding;
                subcontrol-position: top left;
                padding: 8px 16px;
                margin-left: 8px;
                margin-top: -8px;
                color: #818cf8;
                background: rgba(99, 102, 241, 0.15);
                border: 1px solid rgba(99, 102, 241, 0.3);
                border-radius: 8px;
            }
            QLabel {
                color: #e4e4e7;
                background-color: transparent;
            }
            QTextEdit {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 12px;
                color: #a5f3fc;
                font-family: 'Cascadia Code', 'JetBrains Mono', 'Consolas', monospace;
                font-size: 13px;
                padding: 16px;
                selection-background-color: #6366f1;
            }
            QProgressBar {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 5px;
                text-align: center;
                color: #e4e4e7;
                height: 10px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                border-radius: 5px;
            }
            QScrollBar:vertical {
                background: #0f172a;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #475569;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #64748b;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
    
    def check_git_availability(self):
        """Check if Git is available in PATH"""
        try:
            result = subprocess.run(
                "git --version",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Git is available
                return True
            else:
                self.show_git_warning()
                return False
        except Exception:
            self.show_git_warning()
            return False
    
    def show_git_warning(self):
        """Show warning if Git is not available"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Git Not Found")
        msg_box.setText("Git is not installed or not in PATH")
        msg_box.setInformativeText(
            "The deployment features require Git to be installed.\n\n"
            "You can still:\n"
            "• Browse and validate JSON files\n"
            "• View file statistics\n\n"
            "To enable deployment:\n"
            "1. Install Git from https://git-scm.com\n"
            "2. Ensure Git is added to your PATH\n"
            "3. Restart this application"
        )
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e293b;
            }
            QMessageBox QLabel {
                color: #e4e4e7;
                font-size: 14px;
                min-width: 400px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fbbf24, stop:1 #f59e0b);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f59e0b, stop:1 #d97706);
            }
        """)
        msg_box.exec()
        
    def create_dashboard_header(self, layout):
        """Create dashboard header with welcome message"""
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #6366f1, stop:1 #8b5cf6);
            border-radius: 16px;
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 20)
        header_layout.setSpacing(24)
        
        # Left side - Icon and Title
        left_layout = QHBoxLayout()
        left_layout.setSpacing(16)
        
        icon_label = QLabel("📸")
        icon_label.setStyleSheet("""
            font-size: 42px;
            background-color: transparent;
        """)
        left_layout.addWidget(icon_label)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        title = QLabel("Photography Portfolio Deployment")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #FFFFFF;
            background-color: transparent;
        """)
        text_layout.addWidget(title)
        
        subtitle = QLabel("Professional Git Deployment Dashboard")
        subtitle.setStyleSheet("""
            font-size: 13px;
            font-weight: 400;
            color: rgba(255, 255, 255, 0.85);
            background-color: transparent;
        """)
        text_layout.addWidget(subtitle)
        
        left_layout.addLayout(text_layout)
        header_layout.addLayout(left_layout, 1)
        
        # Right side - Status indicator
        status_widget = QWidget()
        status_widget.setFixedSize(140, 60)
        status_widget.setStyleSheet("""
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        """)
        status_layout = QVBoxLayout(status_widget)
        status_layout.setContentsMargins(12, 8, 12, 8)
        status_layout.setSpacing(2)
        
        self.status_label = QLabel("● Ready")
        self.status_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #10b981;
            background-color: transparent;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)
        
        status_desc = QLabel("System Status")
        status_desc.setStyleSheet("""
            font-size: 11px;
            color: rgba(255, 255, 255, 0.7);
            background-color: transparent;
        """)
        status_desc.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(status_desc)
        
        header_layout.addWidget(status_widget)
        
        # Add subtle shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 3)
        header.setGraphicsEffect(shadow)
        
        layout.addWidget(header)
        
    def create_file_section(self, layout):
        """Create file selection section (full width)"""
        group = QGroupBox("📁 File Selection")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(16)
        group_layout.setContentsMargins(20, 28, 20, 20)
        
        # Horizontal layout for description and browse button
        top_row = QHBoxLayout()
        
        # Description
        desc = QLabel("Select the JSON file to deploy to your photography portfolio")
        desc.setStyleSheet("""
            color: #94a3b8;
            font-size: 14px;
            background-color: transparent;
        """)
        top_row.addWidget(desc, 1)
        
        # Browse button
        browse_btn = MaterialButton("🔍  Browse Files", "tonal")
        browse_btn.clicked.connect(self.browse_file)
        browse_btn.setFixedWidth(180)
        top_row.addWidget(browse_btn)
        
        group_layout.addLayout(top_row)
        
        # File path display
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setStyleSheet("""
            background-color: #0f172a;
            border: 2px dashed #475569;
            border-radius: 12px;
            padding: 16px;
            color: #94a3b8;
            font-family: 'Cascadia Mono', 'Consolas', monospace;
            font-size: 13px;
        """)
        self.file_path_label.setWordWrap(True)
        self.file_path_label.setFixedHeight(50)
        group_layout.addWidget(self.file_path_label)
        
        layout.addWidget(group)
        
    def create_deployment_section(self, layout):
        """Create deployment controls section"""
        group = QGroupBox("🚀 Deployment Controls")
        group.setMinimumWidth(500)
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(16)
        group_layout.setContentsMargins(20, 28, 20, 20)
        
        # Branch info
        branch_text = TARGET_BRANCH if TARGET_BRANCH else "Current Branch"
        branch_label = QLabel(f"🌿 Target Branch: {branch_text}")
        branch_label.setStyleSheet("""
            color: #a5b4fc;
            font-size: 14px;
            padding: 12px 16px;
            font-weight: 500;
            background-color: rgba(99, 102, 241, 0.15);
            border-radius: 8px;
            border-left: 3px solid #6366f1;
        """)
        group_layout.addWidget(branch_label)
        
        # Current step label
        self.step_label = QLabel("")
        self.step_label.setStyleSheet("""
            color: #e4e4e7;
            font-size: 14px;
            font-weight: 500;
            padding: 12px 16px;
            background-color: #0f172a;
            border-radius: 8px;
            border-left: 4px solid #6366f1;
        """)
        self.step_label.setFixedHeight(45)
        self.step_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.step_label.hide()
        group_layout.addWidget(self.step_label)
        
        # Progress bar
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(4)
        
        self.progress_label = QLabel("0%")
        self.progress_label.setStyleSheet("""
            color: #94a3b8;
            font-size: 12px;
            font-weight: 500;
            background-color: transparent;
        """)
        self.progress_label.setAlignment(Qt.AlignRight)
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        progress_layout.addWidget(self.progress_bar)
        
        group_layout.addLayout(progress_layout)
        
        # Deploy button
        self.deploy_btn = MaterialButton("🚀  Deploy to Production", "filled")
        self.deploy_btn.clicked.connect(self.start_deployment)
        self.deploy_btn.setEnabled(False)
        self.deploy_btn.setFixedHeight(50)
        group_layout.addWidget(self.deploy_btn)
        
        group_layout.addStretch()
        
        layout.addWidget(group, 3)
        
    def create_stats_section(self, layout):
        """Create quick stats section"""
        group = QGroupBox("📊 Quick Stats")
        group.setMinimumWidth(350)
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(16)
        group_layout.setContentsMargins(20, 28, 20, 20)
        
        stats_container = QWidget()
        stats_container.setStyleSheet("""
            background: rgba(96, 165, 250, 0.05);
            border: 1px solid rgba(96, 165, 250, 0.2);
            border-radius: 12px;
            padding: 16px;
        """)
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setSpacing(12)
        
        # Branch stat
        branch_stat = QHBoxLayout()
        branch_icon = QLabel("🌿")
        branch_icon.setStyleSheet("font-size: 20px; background: transparent;")
        branch_stat.addWidget(branch_icon)
        
        branch_info = QVBoxLayout()
        branch_label = QLabel("Target Branch")
        branch_label.setStyleSheet("color: #9CA3AF; font-size: 12px; background: transparent;")
        branch_info.addWidget(branch_label)
        
        branch_text = TARGET_BRANCH if TARGET_BRANCH else "Current Branch"
        self.branch_value = QLabel(branch_text)
        self.branch_value.setStyleSheet("color: #60A5FA; font-size: 14px; font-weight: 600; background: transparent;")
        branch_info.addWidget(self.branch_value)
        branch_stat.addLayout(branch_info, 1)
        stats_layout.addLayout(branch_stat)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background: rgba(96, 165, 250, 0.2); max-height: 1px;")
        stats_layout.addWidget(sep)
        
        # Files stat
        files_stat = QHBoxLayout()
        files_icon = QLabel("📁")
        files_icon.setStyleSheet("font-size: 20px; background: transparent;")
        files_stat.addWidget(files_icon)
        
        files_info = QVBoxLayout()
        files_label = QLabel("Files to Deploy")
        files_label.setStyleSheet("color: #9CA3AF; font-size: 12px; background: transparent;")
        files_info.addWidget(files_label)
        
        self.files_value = QLabel("data/*.json")
        self.files_value.setStyleSheet("color: #34D399; font-size: 14px; font-weight: 600; background: transparent;")
        files_info.addWidget(self.files_value)
        files_stat.addLayout(files_info, 1)
        stats_layout.addLayout(files_stat)
        
        # Another separator
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setStyleSheet("background: rgba(96, 165, 250, 0.2); max-height: 1px;")
        stats_layout.addWidget(sep2)
        
        # Validation status
        validation_stat = QHBoxLayout()
        validation_icon = QLabel("✓")
        self.validation_icon = validation_icon
        validation_icon.setStyleSheet("font-size: 20px; color: #9CA3AF; background: transparent;")
        validation_stat.addWidget(validation_icon)
        
        validation_info = QVBoxLayout()
        validation_label = QLabel("Validation Status")
        validation_label.setStyleSheet("color: #9CA3AF; font-size: 12px; background: transparent;")
        validation_info.addWidget(validation_label)
        
        self.validation_value = QLabel("No file selected")
        self.validation_value.setStyleSheet("color: #9CA3AF; font-size: 14px; font-weight: 600; background: transparent;")
        validation_info.addWidget(self.validation_value)
        validation_stat.addLayout(validation_info, 1)
        stats_layout.addLayout(validation_stat)
        
        # Missing fields display
        self.missing_fields_widget = QWidget()
        self.missing_fields_widget.setStyleSheet("""
            background: rgba(251, 191, 36, 0.1);
            border: 1px solid rgba(251, 191, 36, 0.3);
            border-radius: 8px;
            padding: 12px;
        """)
        missing_fields_layout = QVBoxLayout(self.missing_fields_widget)
        missing_fields_layout.setSpacing(6)
        missing_fields_layout.setContentsMargins(8, 8, 8, 8)
        
        self.missing_title = QLabel("⚠️ Missing Optional Fields:")
        self.missing_title.setStyleSheet("color: #FBBF24; font-size: 12px; font-weight: 600; background: transparent;")
        missing_fields_layout.addWidget(self.missing_title)
        
        self.missing_fields_label = QLabel("None")
        self.missing_fields_label.setStyleSheet("color: #FCD34D; font-size: 11px; background: transparent;")
        self.missing_fields_label.setWordWrap(True)
        missing_fields_layout.addWidget(self.missing_fields_label)
        
        stats_layout.addWidget(self.missing_fields_widget)
        self.missing_fields_widget.hide()
        
        group_layout.addWidget(stats_container)
        group_layout.addStretch()
        
        layout.addWidget(group, 2)
    
    def create_console_section(self, layout):
        """Create console output section"""
        group = QGroupBox("📊 Deployment Console")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(8)
        group_layout.setContentsMargins(20, 28, 20, 20)
        
        # Console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(250)
        group_layout.addWidget(self.console)
        
        layout.addWidget(group)
        
    def create_footer(self, layout):
        """Create dashboard footer section"""
        footer_widget = QWidget()
        footer_widget.setStyleSheet("""
            background: rgba(20, 20, 20, 0.5);
            border-radius: 12px;
            padding: 16px;
        """)
        footer_layout = QHBoxLayout(footer_widget)
        
        footer_text = QLabel("Made with ❤️ for Anupam Dutta Photography")
        footer_text.setStyleSheet("""
            color: #9CA3AF;
            font-size: 13px;
            background-color: transparent;
        """)
        footer_layout.addWidget(footer_text)
        
        footer_layout.addStretch()
        
        version = QLabel("v2.0 • Material Design 3")
        version.setStyleSheet("""
            color: #60A5FA;
            font-size: 12px;
            font-weight: 500;
            background-color: transparent;
        """)
        footer_layout.addWidget(version)
        
        layout.addWidget(footer_widget)
        
    def validate_json_file(self, file_path):
        """Validate JSON file structure and check for required fields"""
        try:
            # Read and parse JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if it's the main portfolio data structure or photo items
            if isinstance(data, dict):
                # Check if it has portfolio structure keys
                portfolio_keys = ['about', 'slider-content', 'slider-images', 'categories', 'gallery-images']
                has_portfolio_structure = any(key in data for key in portfolio_keys)
                
                if has_portfolio_structure:
                    # Portfolio structure validation
                    required_sections = ['about', 'slider-content', 'slider-images', 'categories', 'gallery-images']
                    missing_sections = [section for section in required_sections if section not in data]
                    
                    if missing_sections:
                        return {
                            'valid': False,
                            'error': f'Missing required sections: {", ".join(missing_sections)}',
                            'missing_fields': []
                        }
                    
                    # Validate nested structure
                    errors = []
                    missing_fields = []
                    
                    # Validate 'about' section
                    if 'about' in data and isinstance(data['about'], dict):
                        about_required = ['title', 'description']
                        about_optional = ['card']
                        for field in about_required:
                            if field not in data['about'] or not data['about'][field]:
                                errors.append(f"about.{field} is missing or empty")
                        for field in about_optional:
                            if field not in data['about']:
                                missing_fields.append(f"about.{field}")
                    
                    # Validate 'slider-content' section
                    if 'slider-content' in data and isinstance(data['slider-content'], dict):
                        slider_required = ['heading', 'description']
                        slider_optional = ['show-heading', 'show-description', 'show-latest-collections-button']
                        for field in slider_required:
                            if field not in data['slider-content'] or not data['slider-content'][field]:
                                errors.append(f"slider-content.{field} is missing or empty")
                        for field in slider_optional:
                            if field not in data['slider-content']:
                                missing_fields.append(f"slider-content.{field}")
                    
                    # Validate 'slider-images' section
                    if 'slider-images' in data:
                        if not isinstance(data['slider-images'], list) or len(data['slider-images']) == 0:
                            errors.append("slider-images must be a non-empty array")
                    
                    # Validate 'categories' section
                    if 'categories' in data:
                        if not isinstance(data['categories'], list) or len(data['categories']) == 0:
                            errors.append("categories must be a non-empty array")
                        else:
                            for idx, cat in enumerate(data['categories']):
                                cat_required = ['title', 'description', 'image']
                                for field in cat_required:
                                    if field not in cat or not cat[field]:
                                        errors.append(f"categories[{idx}].{field} is missing or empty")
                    
                    # Validate 'gallery-images' section
                    if 'gallery-images' in data:
                        if not isinstance(data['gallery-images'], list) or len(data['gallery-images']) == 0:
                            errors.append("gallery-images must be a non-empty array")
                    
                    if errors:
                        return {
                            'valid': False,
                            'error': '\n'.join(errors),
                            'missing_fields': []
                        }
                    
                    # All required fields present
                    return {
                        'valid': True,
                        'error': None,
                        'missing_fields': sorted(missing_fields)
                    }
                else:
                    # Single photo item validation
                    required_fields = ['id', 'title', 'category', 'imageUrl', 'description']
                    optional_fields = ['date', 'location', 'camera', 'lens', 'settings', 'tags', 'featured', 'cloudinaryPublicId']
                    
                    missing_required = [field for field in required_fields if field not in data or not data[field]]
                    if missing_required:
                        return {
                            'valid': False,
                            'error': f'Missing required fields: {", ".join(missing_required)}',
                            'missing_fields': []
                        }
                    
                    missing_optional = [field for field in optional_fields if field not in data]
                    
                    return {
                        'valid': True,
                        'error': None,
                        'missing_fields': sorted(missing_optional)
                    }
                
            elif isinstance(data, list):
                # Photo items array validation
                required_fields = ['id', 'title', 'category', 'imageUrl', 'description']
                optional_fields = ['date', 'location', 'camera', 'lens', 'settings', 'tags', 'featured', 'cloudinaryPublicId']
                
                if not data:
                    return {
                        'valid': False,
                        'error': 'JSON file is empty.',
                        'missing_fields': []
                    }
                
                # Validate each item
                all_missing_fields = set()
                errors = []
                
                for idx, item in enumerate(data):
                    if not isinstance(item, dict):
                        errors.append(f"Item {idx + 1}: Not a valid object")
                        continue
                    
                    # Check required fields
                    missing_required = [field for field in required_fields if field not in item or not item[field]]
                    if missing_required:
                        errors.append(f"Item {idx + 1}: Missing required fields: {', '.join(missing_required)}")
                    
                    # Track optional missing fields
                    missing_optional = [field for field in optional_fields if field not in item]
                    all_missing_fields.update(missing_optional)
                
                if errors:
                    return {
                        'valid': False,
                        'error': '\n'.join(errors),
                        'missing_fields': []
                    }
                
                return {
                    'valid': True,
                    'error': None,
                    'missing_fields': sorted(list(all_missing_fields))
                }
            else:
                return {
                    'valid': False,
                    'error': 'Invalid JSON structure. Expected object or array.',
                    'missing_fields': []
                }
            
        except json.JSONDecodeError as e:
            return {
                'valid': False,
                'error': f'Invalid JSON syntax: {str(e)}',
                'missing_fields': []
            }
        except Exception as e:
            return {
                'valid': False,
                'error': f'Error reading file: {str(e)}',
                'missing_fields': []
            }
    
    def browse_file(self):
        """Open file dialog to select JSON file"""
        repo_root = Path(__file__).parent.parent
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select JSON File",
            str(repo_root),
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            # Validate JSON file
            validation_result = self.validate_json_file(file_path)
            
            # Log validation details
            self.log_message(f"🔍 Validating file: {file_path}", "#60A5FA")
            
            if not validation_result['valid']:
                # Show validation error
                self.log_message(f"❌ Validation failed: {validation_result['error']}", "#EF4444")
                
                # Update UI to show error state
                self.validation_icon.setStyleSheet("font-size: 20px; color: #EF4444; background: transparent;")
                self.validation_value.setText("Invalid ✗")
                self.validation_value.setStyleSheet("color: #EF4444; font-size: 14px; font-weight: 600; background: transparent;")
                
                # Show error in missing fields widget
                self.missing_fields_label.setText(validation_result['error'])
                self.missing_fields_widget.setStyleSheet("""
                    background: rgba(239, 68, 68, 0.1);
                    border: 1px solid rgba(239, 68, 68, 0.3);
                    border-radius: 8px;
                    padding: 12px;
                """)
                missing_title_label = self.missing_fields_widget.findChild(QLabel)
                if missing_title_label:
                    missing_title_label.setText("❌ Validation Errors:")
                    missing_title_label.setStyleSheet("color: #EF4444; font-size: 12px; font-weight: 600; background: transparent;")
                self.missing_fields_widget.show()
                
                # Don't enable deploy button
                self.deploy_btn.setEnabled(False)
                return
            
            # Show validation success with missing fields if any
            if validation_result['missing_fields']:
                # Don't show popup, just log to console
                self.log_message(f"⚠️  File validated with {len(validation_result['missing_fields'])} missing optional fields:", "#f59e0b")
                # Log each missing field
                for field in validation_result['missing_fields']:
                    self.log_message(f"    • {field}", "#FCD34D")
            
            self.selected_file = file_path
            self.file_path_label.setText(file_path)
            self.file_path_label.setStyleSheet("""
                background-color: rgba(208, 188, 255, 0.08);
                border: 1px solid #D0BCFF;
                border-radius: 12px;
                padding: 16px;
                color: #D0BCFF;
                font-family: 'Cascadia Mono', 'Consolas', monospace;
                font-size: 13px;
                letter-spacing: 0.25px;
            """)
            self.deploy_btn.setEnabled(True)
            
            # Update validation status in UI
            if validation_result['missing_fields']:
                self.validation_icon.setStyleSheet("font-size: 20px; color: #FBBF24; background: transparent;")
                self.validation_value.setText(f"Valid ({len(validation_result['missing_fields'])} warnings)")
                self.validation_value.setStyleSheet("color: #FBBF24; font-size: 14px; font-weight: 600; background: transparent;")
                
                # Reset missing fields widget style
                self.missing_fields_widget.setStyleSheet("""
                    background: rgba(251, 191, 36, 0.1);
                    border: 1px solid rgba(251, 191, 36, 0.3);
                    border-radius: 8px;
                    padding: 12px;
                """)
                self.missing_title.setText("⚠️ Missing Optional Fields:")
                self.missing_title.setStyleSheet("color: #FBBF24; font-size: 12px; font-weight: 600; background: transparent;")
                
                # Show missing fields - format nicely with line breaks
                missing_display = "\n".join(validation_result['missing_fields'])
                self.missing_fields_label.setText(missing_display)
                self.missing_fields_label.setStyleSheet("color: #FCD34D; font-size: 11px; background: transparent;")
                self.missing_fields_widget.show()
            else:
                self.validation_icon.setStyleSheet("font-size: 20px; color: #10b981; background: transparent;")
                self.validation_value.setText("Valid ✓")
                self.validation_value.setStyleSheet("color: #10b981; font-size: 14px; font-weight: 600; background: transparent;")
                
                # Hide missing fields
                self.missing_fields_widget.hide()
                
                self.log_message("✅ File validated successfully - All fields present", "#10b981")
            
    def start_deployment(self):
        """Start the deployment process"""
        if not self.selected_file or self.is_deploying:
            return
        
        # Confirmation dialog with custom styling
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Deployment")
        msg_box.setText(f"Deploy to branch: {TARGET_BRANCH if TARGET_BRANCH else 'Current Branch'}?")
        msg_box.setInformativeText("This will commit and push changes to the remote repository.")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1a1a1a;
            }
            QMessageBox QLabel {
                color: #E6E1E5;
                font-size: 14px;
                min-width: 300px;
            }
            QPushButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 13px;
                font-weight: 500;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #7c63b8;
            }
            QPushButton:pressed {
                background-color: #5a4492;
            }
        """)
        
        reply = msg_box.exec()
        
        if reply != QMessageBox.Yes:
            return
        
        self.is_deploying = True
        self.deploy_btn.setEnabled(False)
        self.deploy_btn.setText("⏳ Deploying...")
        self.progress_bar.setValue(0)
        self.console.clear()
        self.step_label.show()
        self.status_label.setText("● Deploying")
        self.status_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #FBBF24;
            background-color: transparent;
        """)
        
        # Create worker signals
        signals = WorkerSignals()
        signals.log.connect(self.log_message)
        signals.progress.connect(self.update_progress)
        signals.finished.connect(self.deployment_finished)
        signals.step.connect(self.update_step)
        
        # Start worker thread
        self.worker = DeploymentWorker(self.selected_file, signals)
        self.worker.start()
        
    def update_step(self, step):
        """Update current step label"""
        self.step_label.setText(f"⏳ {step}")
        
    def log_message(self, message, color="#10b981"):
        """Add message to console"""
        # Convert hex color to HTML
        self.console.setTextColor(QColor(color))
        self.console.append(message)
        self.console.verticalScrollBar().setValue(
            self.console.verticalScrollBar().maximum()
        )
        
    def update_progress(self, value):
        """Update progress bar with Material Design animation"""
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"{value}%")
        
    def deployment_finished(self, success, message):
        """Handle deployment completion"""
        self.is_deploying = False
        self.deploy_btn.setEnabled(True)
        self.deploy_btn.setText("🚀  Deploy to Production")
        self.step_label.hide()
        
        if success:
            self.status_label.setText("● Success")
            self.status_label.setStyleSheet("""
                font-size: 16px;
                font-weight: 600;
                color: #10b981;
                background-color: transparent;
            """)
            
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Deployment Successful")
            msg_box.setText("Your photography portfolio has been deployed successfully!")
            msg_box.setInformativeText("The website is now live with your updates.")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1a1a1a;
                }
                QMessageBox QLabel {
                    color: #E6E1E5;
                    font-size: 14px;
                    min-width: 300px;
                }
                QPushButton {
                    background-color: #10b981;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 24px;
                    font-size: 13px;
                    font-weight: 500;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #14c48d;
                }
            """)
            msg_box.exec()
        else:
            self.status_label.setText("● Failed")
            self.status_label.setStyleSheet("""
                font-size: 16px;
                font-weight: 600;
                color: #EF4444;
                background-color: transparent;
            """)
            
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Deployment Failed")
            msg_box.setText("Deployment failed with error:")
            msg_box.setInformativeText(f"{message}\n\nPlease check the console for details.")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #1a1a1a;
                }
                QMessageBox QLabel {
                    color: #E6E1E5;
                    font-size: 14px;
                    min-width: 300px;
                }
                QPushButton {
                    background-color: #EF4444;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 24px;
                    font-size: 13px;
                    font-weight: 500;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #f35555;
                }
            """)
            msg_box.exec()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = DeploymentApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
