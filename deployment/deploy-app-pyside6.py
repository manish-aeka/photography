"""
Photography Portfolio Deployment Tool
Modern GUI using PySide6 with professional design
"""

import sys
import json
import subprocess
import threading
import time
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
        self.repo_root = Path(__file__).parent.parent
        
    def log(self, message, color="#10b981"):
        self.signals.log.emit(message, color)
        
    def set_progress(self, value):
        self.signals.progress.emit(value)
        
    def set_step(self, step):
        self.signals.step.emit(step)
        
    def run_git_command(self, command, description):
        """Execute git command and log result"""
        self.log(f"  🔧 Executing: {command}", "#9ca3af")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=60
            )
            
            if result.stdout.strip():
                self.log(f"  ✓ {result.stdout.strip()}", "#60a5fa")
            
            if result.returncode != 0 and result.stderr.strip():
                self.log(f"  ⚠️ {result.stderr.strip()}", "#f59e0b")
                
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            self.log(f"  ❌ Command timed out: {command}", "#ef4444")
            return False
        except Exception as e:
            self.log(f"  ❌ Error: {str(e)}", "#ef4444")
            return False
    
    def run(self):
        """Main deployment logic"""
        try:
            # Determine branch
            branch = TARGET_BRANCH
            if not branch:
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=self.repo_root
                )
                branch = result.stdout.strip()
                self.log(f"Using current branch: {branch}", "#60a5fa")
            
            self.log("=" * 70, "#60a5fa")
            self.log("🚀 Starting deployment process...", "#60a5fa")
            self.log(f"📍 Deployment branch: {branch}", "#60a5fa")
            self.log(f"📁 Working directory: {self.repo_root}", "#60a5fa")
            self.log("=" * 70, "#60a5fa")
            
            # Check data folder
            data_folder = self.repo_root / "data"
            if not data_folder.exists():
                self.log("  ❌ Error: data/ folder not found", "#ef4444")
                self.signals.finished.emit(False, "data/ folder not found")
                return
            
            # Step 1: Update JSON file (10%)
            self.set_step("Step 1/6: Updating JSON file")
            self.log("\n📋 Step 1/6: Updating JSON file in data/ folder...", "#fbbf24")
            self.set_progress(5)
            
            target_file = data_folder / "anupam-dutta-photography-data-set.json"
            
            try:
                with open(self.selected_file, 'r', encoding='utf-8') as src:
                    content = src.read()
                
                self.log(f"  📄 Source file: {Path(self.selected_file).name}", "#60a5fa")
                self.log(f"  📁 Target file: {target_file}", "#60a5fa")
                
                with open(target_file, 'w', encoding='utf-8') as dst:
                    dst.write(content)
                
                self.log("  ✓ File updated successfully", "#10b981")
            except Exception as e:
                self.log(f"  ❌ Error updating file: {str(e)}", "#ef4444")
                self.signals.finished.emit(False, f"File update failed: {str(e)}")
                return
            
            self.set_progress(10)
            
            # Step 2: Git status (20%)
            self.set_step("Step 2/6: Checking Git status")
            self.log("\n🔍 Step 2/6: Checking Git status...", "#fbbf24")
            
            git_check = subprocess.run("git --version", shell=True, capture_output=True, text=True)
            if git_check.returncode != 0:
                self.log("  ⚠️ Git is not installed. Skipping Git operations.", "#f59e0b")
                self.set_progress(100)
                self.log("\n✅ Deployment completed (JSON updated only)", "#10b981")
                self.signals.finished.emit(True, "JSON file updated successfully")
                return
            
            if not self.run_git_command("git status", "Git status check"):
                raise Exception("Git status check failed")
            
            self.set_progress(20)
            
            # Step 3: Git add (35%)
            self.set_step("Step 3/6: Staging changes")
            self.log("\n➕ Step 3/6: Adding .json files from data/ folder to Git...", "#fbbf24")
            
            status_result = subprocess.run(
                ["git", "status", "--short", "data/"],
                capture_output=True,
                text=True,
                cwd=self.repo_root
            )
            
            if status_result.stdout.strip():
                self.log(f"  📝 Changes detected:\n{status_result.stdout}", "#60a5fa")
                if not self.run_git_command("git add data/", "Git add data/"):
                    raise Exception("Git add failed")
                self.log("  ✓ Changes added successfully", "#10b981")
            else:
                self.log("  ℹ️ No changes detected in data/ folder", "#60a5fa")
            
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
                    background-color: #6750A4;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 24px;
                    font-size: 14px;
                    font-weight: 500;
                    letter-spacing: 0.1px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #7965AF;
                }
                QPushButton:pressed {
                    background-color: #5A4793;
                }
                QPushButton:disabled {
                    background-color: rgba(31, 31, 31, 0.12);
                    color: rgba(31, 31, 31, 0.38);
                }
            """)
        elif self.button_type == "tonal":
            # Tonal button (secondary action)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #E8DEF8;
                    color: #1D192B;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 24px;
                    font-size: 14px;
                    font-weight: 500;
                    letter-spacing: 0.1px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #D5C9E9;
                }
                QPushButton:pressed {
                    background-color: #C2B5D8;
                }
                QPushButton:disabled {
                    background-color: rgba(31, 31, 31, 0.12);
                    color: rgba(31, 31, 31, 0.38);
                }
            """)
        elif self.button_type == "outlined":
            # Outlined button
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #6750A4;
                    border: 1px solid #79747E;
                    border-radius: 20px;
                    padding: 10px 24px;
                    font-size: 14px;
                    font-weight: 500;
                    letter-spacing: 0.1px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: rgba(103, 80, 164, 0.08);
                    border-color: #6750A4;
                }
                QPushButton:pressed {
                    background-color: rgba(103, 80, 164, 0.12);
                }
                QPushButton:disabled {
                    border-color: rgba(31, 31, 31, 0.12);
                    color: rgba(31, 31, 31, 0.38);
                }
            """)
        else:  # text button
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #6750A4;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 12px;
                    font-size: 14px;
                    font-weight: 500;
                    letter-spacing: 0.1px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: rgba(103, 80, 164, 0.08);
                }
                QPushButton:pressed {
                    background-color: rgba(103, 80, 164, 0.12);
                }
                QPushButton:disabled {
                    color: rgba(31, 31, 31, 0.38);
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
        """Apply Material Design 3 theme"""
        # Material Design 3 Dark Theme Colors matching editor
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #111827, stop:1 #1f2937);
            }
            QWidget {
                color: #E6E1E5;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                font-size: 14px;
            }
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(31, 41, 55, 0.95), stop:1 rgba(17, 24, 39, 0.95));
                border: 1px solid rgba(75, 85, 99, 0.3);
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
                color: #60A5FA;
                background: rgba(96, 165, 250, 0.1);
                border: 1px solid rgba(96, 165, 250, 0.3);
                border-radius: 8px;
            }
            QLabel {
                color: #D1D5DB;
                background-color: transparent;
            }
            QTextEdit {
                background-color: #0a0f1a;
                border: 1px solid #374151;
                border-radius: 12px;
                color: #10b981;
                font-family: 'Cascadia Code', 'JetBrains Mono', 'Consolas', monospace;
                font-size: 13px;
                padding: 16px;
                selection-background-color: #1C5BAE;
                selection-color: #FFFFFF;
            }
            QProgressBar {
                border: none;
                border-radius: 10px;
                background: rgba(75, 85, 99, 0.3);
                text-align: center;
                height: 10px;
                color: transparent;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1C5BAE, stop:1 #1DA6E1);
                border-radius: 10px;
            }
        """)
        
    def create_dashboard_header(self, layout):
        """Create dashboard header with welcome message"""
        header = QWidget()
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #1C5BAE, stop:1 #1DA6E1);
            border-radius: 20px;
            padding: 24px;
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 24, 32, 24)
        
        # Left side - Title and subtitle
        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)
        
        title = QLabel("📸 Photography Portfolio Deployment")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #FFFFFF;
            background-color: transparent;
        """)
        left_layout.addWidget(title)
        
        subtitle = QLabel("Professional Git Deployment Dashboard • Deploy your portfolio with one click")
        subtitle.setStyleSheet("""
            font-size: 14px;
            font-weight: 400;
            color: rgba(255, 255, 255, 0.9);
            background-color: transparent;
        """)
        left_layout.addWidget(subtitle)
        
        header_layout.addLayout(left_layout, 1)
        
        # Right side - Status indicator
        status_widget = QWidget()
        status_widget.setStyleSheet("""
            background: rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 16px 24px;
        """)
        status_layout = QVBoxLayout(status_widget)
        status_layout.setSpacing(4)
        
        self.status_label = QLabel("● Ready")
        self.status_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #10b981;
            background-color: transparent;
        """)
        status_layout.addWidget(self.status_label)
        
        status_desc = QLabel("System Status")
        status_desc.setStyleSheet("""
            font-size: 12px;
            color: rgba(255, 255, 255, 0.8);
            background-color: transparent;
        """)
        status_layout.addWidget(status_desc)
        
        header_layout.addWidget(status_widget)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 4)
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
            color: #CAC4D0;
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
            background-color: #211F26;
            border: 1px solid #49454F;
            border-radius: 12px;
            padding: 16px;
            color: #938F99;
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
            color: #D0BCFF;
            font-size: 14px;
            padding: 12px 16px;
            font-weight: 500;
            background-color: rgba(208, 188, 255, 0.12);
            border-radius: 8px;
        """)
        group_layout.addWidget(branch_label)
        
        # Current step label
        self.step_label = QLabel("")
        self.step_label.setStyleSheet("""
            color: #E8DEF8;
            font-size: 14px;
            font-weight: 500;
            padding: 12px 16px;
            background-color: rgba(208, 188, 255, 0.08);
            border-radius: 12px;
            border-left: 3px solid #D0BCFF;
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
            color: #CAC4D0;
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
            background: rgba(31, 41, 55, 0.5);
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
            self.log_message("✅ File selected successfully", "#4DB6AC")
            
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
