"""
Photography Portfolio Deployment Tool
Modern Material Design 3 Dashboard UI
Single-screen user-friendly interface
"""

import sys
import json
import subprocess
import threading
import time
import os
from pathlib import Path
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QTextEdit, QFileDialog,
    QGroupBox, QFrame, QGridLayout, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt, QTimer, Signal, QObject, QSize, QPropertyAnimation
from PySide6.QtGui import QFont, QColor, QPalette

# ================================
# CONFIGURATION
# ================================
TARGET_BRANCH = ""  # Will use current branch
INCLUDE_FILES = ["data/*.json"]


class WorkerSignals(QObject):
    """Signals for worker thread"""
    log = Signal(str, str)  # message, color
    progress = Signal(int)
    finished = Signal(bool, str)
    step = Signal(str)


class DeploymentWorker(threading.Thread):
    """Worker thread for deployment"""
    
    def __init__(self, selected_file, signals):
        super().__init__(daemon=True)
        self.selected_file = selected_file
        self.signals = signals
        
        # Find git repository root
        if getattr(sys, 'frozen', False):
            exe_dir = Path(sys.executable).parent
        else:
            exe_dir = Path(__file__).parent
        
        self.repo_root = self.find_git_root(exe_dir)
        if not self.repo_root:
            self.repo_root = self.find_git_root(Path.cwd())
        if not self.repo_root:
            self.repo_root = exe_dir
    
    def find_git_root(self, start_path):
        """Find git repository root"""
        current = Path(start_path).resolve()
        for _ in range(5):
            if (current / ".git").exists():
                return current
            if current.parent == current:
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
        """Execute git command"""
        try:
            self.log(f"  → {command}", "#60a5fa")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(self.repo_root),
                timeout=60
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    self.log(f"  ✓ {result.stdout.strip()}", "#10b981")
                return True
            else:
                if result.stderr.strip():
                    self.log(f"  ⚠ {result.stderr.strip()}", "#f59e0b")
                return False
                
        except Exception as e:
            self.log(f"  ✗ Error: {str(e)}", "#ef4444")
            return False
    
    def run(self):
        """Main deployment process"""
        try:
            # Step 1: Validate file
            self.set_step("1/6: Validating JSON file")
            self.log("=" * 60, "#60a5fa")
            self.log("🚀 DEPLOYMENT STARTED", "#10b981")
            self.log("=" * 60, "#60a5fa")
            self.log("\n📋 Step 1/6: Validating JSON file...", "#fbbf24")
            
            if not Path(self.selected_file).exists():
                raise Exception(f"File not found: {self.selected_file}")
            
            try:
                with open(self.selected_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.log(f"  ✓ Valid JSON file ({len(json.dumps(data))} bytes)", "#10b981")
            except json.JSONDecodeError as e:
                raise Exception(f"Invalid JSON: {str(e)}")
            
            # Check .git folder
            if not (self.repo_root / ".git").exists():
                self.log(f"\n⚠️ No .git folder found in: {self.repo_root}", "#f59e0b")
                self.log("\n💡 Solution:", "#60a5fa")
                self.log("  1. Copy this executable to your git repository root", "#60a5fa")
                self.log("  2. Make sure the repository has .git folder", "#60a5fa")
                raise Exception("Not a git repository")
            
            # Create data folder
            data_folder = self.repo_root / "data"
            if not data_folder.exists():
                data_folder.mkdir(parents=True)
                self.log(f"  ✓ Created data/ folder", "#10b981")
            
            # Copy file
            target_file = data_folder / Path(self.selected_file).name
            with open(self.selected_file, 'r', encoding='utf-8') as src:
                content = src.read()
            with open(target_file, 'w', encoding='utf-8') as dst:
                dst.write(content)
            
            self.log(f"  ✓ File copied to: data/{Path(self.selected_file).name}", "#10b981")
            self.set_progress(10)
            
            # Step 2: Check branch
            self.set_step("2/6: Checking Git branch")
            self.log("\n🌿 Step 2/6: Checking Git branch...", "#fbbf24")
            
            branch_result = subprocess.run(
                "git branch --show-current",
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(self.repo_root),
                timeout=10
            )
            
            if branch_result.returncode == 0:
                branch = branch_result.stdout.strip()
                self.log(f"  ✓ Current branch: {branch}", "#10b981")
            else:
                branch = "main"
            
            self.set_progress(20)
            
            # Step 3: Git add
            self.set_step("3/6: Staging changes")
            self.log("\n➕ Step 3/6: Staging changes...", "#fbbf24")
            
            self.run_git_command("git add data/*.json", "Add JSON files")
            self.set_progress(40)
            
            # Step 4: Git commit
            self.set_step("4/6: Committing changes")
            self.log("\n💾 Step 4/6: Committing changes...", "#fbbf24")
            
            commit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.run_git_command(f'git commit -m "Update portfolio data - {commit_time}"', "Commit")
            self.set_progress(60)
            
            # Step 5: Git push
            self.set_step(f"5/6: Pushing to {branch}")
            self.log(f"\n📤 Step 5/6: Pushing to {branch}...", "#fbbf24")
            
            self.run_git_command(f"git push origin {branch}", "Push")
            self.set_progress(80)
            
            # Step 6: Complete
            self.set_step("6/6: Complete!")
            self.log("\n✅ Step 6/6: Deployment complete!", "#10b981")
            self.log("=" * 60, "#60a5fa")
            self.set_progress(100)
            
            self.signals.finished.emit(True, "Deployment successful!")
            
        except Exception as e:
            self.log(f"\n❌ DEPLOYMENT FAILED: {str(e)}", "#ef4444")
            self.log("=" * 60, "#60a5fa")
            self.signals.finished.emit(False, str(e))


class MaterialCard(QFrame):
    """Material Design 3 Card Component"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 16px;
            }
        """)


class MaterialButton(QPushButton):
    """Material Design 3 Button"""
    def __init__(self, text, style="filled", parent=None):
        super().__init__(text, parent)
        
        if style == "filled":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6366f1, stop:1 #8b5cf6);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 14px 28px;
                    font-size: 14px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4f46e5, stop:1 #7c3aed);
                }
                QPushButton:disabled {
                    background: #334155;
                    color: #64748b;
                }
            """)
        elif style == "outlined":
            self.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #818cf8;
                    border: 2px solid #6366f1;
                    border-radius: 12px;
                    padding: 12px 28px;
                    font-size: 14px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: rgba(99, 102, 241, 0.1);
                    border-color: #818cf8;
                    color: #a5b4fc;
                }
            """)


class DashboardApp(QMainWindow):
    """Main Dashboard Application"""
    
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Photography Portfolio Deployment Dashboard")
        self.setMinimumSize(1200, 700)
        self.resize(1400, 900)
        
        # Set theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
            QLabel {
                color: #e4e4e7;
                background: transparent;
            }
            QTextEdit {
                background: #0f172a;
                border: 1px solid #334155;
                border-radius: 12px;
                color: #a5f3fc;
                font-family: 'Cascadia Mono', Consolas, monospace;
                font-size: 13px;
                padding: 16px;
            }
        """)
        
        # Central widget with scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
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
        self.setCentralWidget(scroll)
        
        central = QWidget()
        scroll.setWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header
        self.create_header(layout)
        
        # Main dashboard grid
        grid = QGridLayout()
        grid.setSpacing(20)
        
        # Row 1: File selection (span full width)
        self.create_file_card(grid, 0, 0, 1, 3)
        
        # Row 2: Three cards - Status, Actions, Stats
        self.create_status_card(grid, 1, 0)
        self.create_actions_card(grid, 1, 1)
        self.create_stats_card(grid, 1, 2)
        
        layout.addLayout(grid)
        
        # Console (full width)
        self.create_console(layout)
        
    def create_header(self, layout):
        """Create dashboard header"""
        header = QFrame()
        header.setFixedHeight(110)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                border: none;
                border-radius: 16px;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 20, 24, 20)
        header_layout.setSpacing(20)
        
        # Left side
        left = QVBoxLayout()
        left.setSpacing(8)
        
        icon_title = QHBoxLayout()
        icon = QLabel("📸")
        icon.setStyleSheet("font-size: 48px;")
        icon_title.addWidget(icon)
        
        title_layout = QVBoxLayout()
        title = QLabel("Photography Portfolio Deployment")
        title.setStyleSheet("font-size: 28px; font-weight: 700; color: white;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Professional Git Deployment Dashboard • Material Design 3")
        subtitle.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.9);")
        title_layout.addWidget(subtitle)
        
        icon_title.addLayout(title_layout)
        left.addLayout(icon_title)
        
        header_layout.addLayout(left, 1)
        
        # Right side - Status
        self.status_indicator = QLabel("● READY")
        self.status_indicator.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #10b981;
            background: #064e3b;
            border: 2px solid #10b981;
            border-radius: 10px;
            padding: 12px 28px;
        """)
        self.status_indicator.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.status_indicator)
        
        layout.addWidget(header)
    
    def create_file_card(self, grid, row, col, row_span, col_span):
        """File selection card"""
        card = MaterialCard()
        card.setMinimumHeight(140)
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("📁 FILE SELECTION")
        title.setStyleSheet("font-size: 15px; font-weight: 700; color: #818cf8;")
        layout.addWidget(title)
        
        desc = QLabel("Select your JSON portfolio file to deploy")
        desc.setStyleSheet("font-size: 13px; color: #94a3b8;")
        layout.addWidget(desc)
        
        # File path + button
        file_row = QHBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("""
            background: #0f172a;
            border: 2px dashed #475569;
            border-radius: 10px;
            padding: 14px;
            font-family: 'Cascadia Mono', Consolas, monospace;
            font-size: 13px;
            color: #94a3b8;
        """)
        file_row.addWidget(self.file_label, 1)
        
        browse_btn = MaterialButton("Browse Files", "filled")
        browse_btn.setFixedWidth(180)
        browse_btn.clicked.connect(self.browse_file)
        file_row.addWidget(browse_btn)
        
        layout.addLayout(file_row)
        
        grid.addWidget(card, row, col, row_span, col_span)
    
    def create_status_card(self, grid, row, col):
        """Status card"""
        card = MaterialCard()
        card.setMinimumHeight(200)
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("📊 DEPLOYMENT STATUS")
        title.setStyleSheet("font-size: 14px; font-weight: 700; color: #818cf8;")
        layout.addWidget(title)
        
        self.step_label = QLabel("Ready to deploy")
        self.step_label.setStyleSheet("""
            font-size: 14px;
            color: #e4e4e7;
            padding: 12px;
            background: #0f172a;
            border-left: 4px solid #6366f1;
            border-radius: 6px;
        """)
        self.step_label.setWordWrap(True)
        layout.addWidget(self.step_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: #0f172a;
                border: 1px solid #334155;
                border-radius: 5px;
                text-align: center;
                color: #e4e4e7;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        
        grid.addWidget(card, row, col)
    
    def create_actions_card(self, grid, row, col):
        """Actions card"""
        card = MaterialCard()
        card.setMinimumHeight(200)
        layout = QVBoxLayout(card)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("🚀 ACTIONS")
        title.setStyleSheet("font-size: 14px; font-weight: 700; color: #818cf8;")
        layout.addWidget(title)
        
        # Deploy button
        self.deploy_btn = MaterialButton("Deploy Now", "filled")
        self.deploy_btn.clicked.connect(self.start_deployment)
        self.deploy_btn.setEnabled(False)
        layout.addWidget(self.deploy_btn)
        
        # Clear button
        clear_btn = MaterialButton("Clear Console", "outlined")
        clear_btn.clicked.connect(lambda: self.console.clear())
        layout.addWidget(clear_btn)
        
        layout.addStretch()
        
        grid.addWidget(card, row, col)
    
    def create_stats_card(self, grid, row, col):
        """Stats card"""
        card = MaterialCard()
        card.setMinimumHeight(200)
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("📈 QUICK STATS")
        title.setStyleSheet("font-size: 14px; font-weight: 700; color: #818cf8;")
        layout.addWidget(title)
        
        # Stats
        self.stats_label = QLabel("No file selected")
        self.stats_label.setStyleSheet("""
            font-size: 13px;
            color: #94a3b8;
            line-height: 1.6;
        """)
        self.stats_label.setWordWrap(True)
        layout.addWidget(self.stats_label)
        
        layout.addStretch()
        
        grid.addWidget(card, row, col)
    
    def create_console(self, layout):
        """Console output"""
        console_card = MaterialCard()
        console_layout = QVBoxLayout(console_card)
        console_layout.setSpacing(12)
        console_layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("💻 DEPLOYMENT CONSOLE")
        title.setStyleSheet("font-size: 15px; font-weight: 700; color: #818cf8;")
        console_layout.addWidget(title)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(280)
        console_layout.addWidget(self.console)
        
        layout.addWidget(console_card)
    
    def browse_file(self):
        """Browse for JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select JSON File", "", "JSON Files (*.json)"
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path)
            self.file_label.setStyleSheet("""
                background: #064e3b;
                border: 2px solid #10b981;
                border-radius: 10px;
                padding: 14px;
                font-family: 'Cascadia Mono', Consolas, monospace;
                font-size: 13px;
                color: #6ee7b7;
            """)
            self.deploy_btn.setEnabled(True)
            
            # Update stats
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                size = os.path.getsize(file_path)
                self.stats_label.setText(
                    f"File: {Path(file_path).name}\n"
                    f"Size: {size:,} bytes\n"
                    f"Ready to deploy"
                )
                self.stats_label.setStyleSheet("font-size: 13px; color: #6ee7b7; font-weight: 500;")
            except:
                pass
    
    def start_deployment(self):
        """Start deployment process"""
        if not self.selected_file:
            return
        
        self.deploy_btn.setEnabled(False)
        self.status_indicator.setText("● DEPLOYING")
        self.status_indicator.setStyleSheet("""
            font-size: 16px; font-weight: 700; color: #fbbf24;
            background: #78350f; border: 2px solid #fbbf24;
            border-radius: 10px; padding: 12px 28px;
        """)
        self.console.clear()
        self.progress_bar.setValue(0)
        
        signals = WorkerSignals()
        signals.log.connect(self.add_log)
        signals.progress.connect(self.update_progress)
        signals.step.connect(self.update_step)
        signals.finished.connect(self.deployment_finished)
        
        self.worker = DeploymentWorker(self.selected_file, signals)
        self.worker.start()
    
    def add_log(self, message, color):
        """Add log to console"""
        self.console.append(f'<span style="color:{color}">{message}</span>')
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def update_step(self, step):
        """Update step label"""
        self.step_label.setText(step)
    
    def deployment_finished(self, success, message):
        """Handle deployment completion"""
        self.deploy_btn.setEnabled(True)
        
        if success:
            self.status_indicator.setText("● SUCCESS")
            self.status_indicator.setStyleSheet("""
                font-size: 16px; font-weight: 700; color: #10b981;
                background: #064e3b; border: 2px solid #10b981;
                border-radius: 10px; padding: 12px 28px;
            """)
            QMessageBox.information(self, "Success", message)
        else:
            self.status_indicator.setText("● FAILED")
            self.status_indicator.setStyleSheet("""
                font-size: 16px; font-weight: 700; color: #ef4444;
                background: #7f1d1d; border: 2px solid #ef4444;
                border-radius: 10px; padding: 12px 28px;
            """)
            QMessageBox.critical(self, "Error", message)
        
        # Reset to READY after 3 seconds
        QTimer.singleShot(3000, lambda: self.status_indicator.setText("● READY") or
                          self.status_indicator.setStyleSheet("""
                              font-size: 16px; font-weight: 700; color: #10b981;
                              background: #064e3b; border: 2px solid #10b981;
                              border-radius: 10px; padding: 12px 28px;
                          """))


def main():
    app = QApplication(sys.argv)
    
    # Set app-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = DashboardApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
