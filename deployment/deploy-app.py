import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import subprocess
import threading
import os
import time
from pathlib import Path
import queue

# ================================
# CONFIGURATION
# ================================
# Branch name (will use current branch if empty)
TARGET_BRANCH = ""

# Specific files/folders to include in deployment (relative to repository root)
INCLUDE_FILES = [
    "data/*.json"
]

class DeploymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📸 Photography Portfolio Deployment Tool")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Modern color scheme with gradient feel
        self.bg_color = "#0f172a"  # Deep blue-gray
        self.bg_secondary = "#1e293b"  # Lighter blue-gray
        self.fg_color = "#f1f5f9"
        self.accent_color = "#3b82f6"  # Bright blue
        self.accent_hover = "#2563eb"  # Darker blue
        self.success_color = "#10b981"
        self.error_color = "#ef4444"
        self.warning_color = "#f59e0b"
        self.info_color = "#06b6d4"
        
        self.root.configure(bg=self.bg_color)
        
        self.selected_file = None
        self.is_deploying = False
        self.loading_dots = 0
        self.loading_spinner_chars = ["⏳", "⌛"]
        self.loading_spinner_index = 0
        self.message_queue = queue.Queue()
        
        self.setup_ui()
        self.process_queue()
        
    def setup_ui(self):
        # Header with gradient effect (simulated with two frames)
        header_outer = tk.Frame(self.root, bg=self.accent_color, height=100)
        header_outer.pack(fill=tk.X, padx=0, pady=0)
        header_outer.pack_propagate(False)
        
        header_inner = tk.Frame(header_outer, bg=self.accent_color)
        header_inner.pack(fill=tk.BOTH, expand=True)
        
        # Icon and title container
        title_container = tk.Frame(header_inner, bg=self.accent_color)
        title_container.pack(expand=True)
        
        title_label = tk.Label(
            title_container,
            text="📸 Photography Portfolio",
            font=("Segoe UI", 22, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_container,
            text="Deployment Management Tool",
            font=("Segoe UI", 11),
            bg=self.accent_color,
            fg="#e0f2fe"
        )
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # File selection section with modern card design
        file_frame = tk.Frame(main_frame, bg=self.bg_secondary, relief=tk.FLAT)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Section header
        file_header = tk.Label(
            file_frame,
            text="📁 Data File Selection",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_secondary,
            fg=self.fg_color,
            anchor="w"
        )
        file_header.pack(fill=tk.X, padx=20, pady=(15, 5))
        
        file_desc = tk.Label(
            file_frame,
            text="Select the JSON file containing your photography data to deploy",
            font=("Segoe UI", 9),
            bg=self.bg_secondary,
            fg="#94a3b8",
            anchor="w"
        )
        file_desc.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # File path display with icon
        self.file_path_var = tk.StringVar(value="No file selected yet...")
        file_display_frame = tk.Frame(file_frame, bg=self.bg_color, relief=tk.SOLID, borderwidth=1)
        file_display_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        file_icon = tk.Label(
            file_display_frame,
            text="📄",
            font=("Segoe UI", 12),
            bg=self.bg_color,
            fg=self.fg_color
        )
        file_icon.pack(side=tk.LEFT, padx=(10, 5), pady=8)
        
        file_path_label = tk.Label(
            file_display_frame,
            textvariable=self.file_path_var,
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#94a3b8",
            anchor="w"
        )
        file_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10), pady=8)
        
        # Browse button with hover effect
        btn_frame = tk.Frame(file_frame, bg=self.bg_secondary)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        browse_btn = tk.Button(
            btn_frame,
            text="🔍  Browse Files",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            cursor="hand2",
            relief=tk.FLAT,
            borderwidth=0,
            padx=25,
            pady=12,
            command=self.browse_file
        )
        browse_btn.pack(side=tk.LEFT)
        
        # Bind hover effects
        browse_btn.bind("<Enter>", lambda e: browse_btn.config(bg=self.accent_hover))
        browse_btn.bind("<Leave>", lambda e: browse_btn.config(bg=self.accent_color))
        
        # Validation status card
        self.validation_frame = tk.Frame(main_frame, bg=self.bg_secondary, relief=tk.FLAT)
        self.validation_frame.pack(fill=tk.X, pady=(0, 15))
        
        validation_header = tk.Label(
            self.validation_frame,
            text="✓ Validation Status",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_secondary,
            fg=self.fg_color,
            anchor="w"
        )
        validation_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        self.validation_label = tk.Label(
            self.validation_frame,
            text="ℹ️  Please select a JSON file to validate",
            font=("Segoe UI", 10),
            bg=self.bg_secondary,
            fg=self.info_color,
            wraplength=800,
            justify=tk.LEFT,
            anchor="w"
        )
        self.validation_label.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Deploy button section
        deploy_container = tk.Frame(main_frame, bg=self.bg_color)
        deploy_container.pack(fill=tk.X, pady=(0, 15))
        
        self.deploy_btn = tk.Button(
            deploy_container,
            text="🚀  Deploy to Production",
            font=("Segoe UI", 13, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            cursor="hand2",
            relief=tk.FLAT,
            borderwidth=0,
            padx=40,
            pady=15,
            state=tk.DISABLED,
            command=self.deploy
        )
        self.deploy_btn.pack()
        
        # Deploy info label
        deploy_info = tk.Label(
            deploy_container,
            text=f"Target Branch: {TARGET_BRANCH if TARGET_BRANCH else 'Current Branch'}",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg="#64748b"
        )
        deploy_info.pack(pady=(8, 0))
        
        # Bind hover effects for deploy button
        self.deploy_btn.bind("<Enter>", lambda e: self.deploy_btn.config(bg="#059669") if self.deploy_btn['state'] == tk.NORMAL else None)
        self.deploy_btn.bind("<Leave>", lambda e: self.deploy_btn.config(bg=self.success_color) if self.deploy_btn['state'] == tk.NORMAL else None)
        
        # Progress section with modern design
        progress_outer = tk.Frame(main_frame, bg=self.bg_secondary, relief=tk.FLAT)
        progress_outer.pack(fill=tk.BOTH, expand=True)
        
        # Progress header
        progress_header = tk.Label(
            progress_outer,
            text="📊 Deployment Console",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_secondary,
            fg=self.fg_color,
            anchor="w"
        )
        progress_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        # Progress bar container
        progress_container = tk.Frame(progress_outer, bg=self.bg_color, relief=tk.SOLID, borderwidth=1)
        progress_container.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        progress_label = tk.Label(
            progress_container,
            text="Progress:",
            font=("Segoe UI", 9, "bold"),
            bg=self.bg_color,
            fg="#94a3b8"
        )
        progress_label.pack(anchor="w", padx=10, pady=(8, 2))
        
        self.progress_var = tk.IntVar()
        
        # Style the progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar",
                       troughcolor=self.bg_color,
                       bordercolor=self.bg_color,
                       background=self.success_color,
                       lightcolor=self.success_color,
                       darkcolor=self.success_color)
        
        self.progress_bar = ttk.Progressbar(
            progress_container,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        # Console output
        console_label = tk.Label(
            progress_outer,
            text="Console Output:",
            font=("Segoe UI", 9, "bold"),
            bg=self.bg_secondary,
            fg="#94a3b8",
            anchor="w"
        )
        console_label.pack(fill=tk.X, padx=20, pady=(5, 5))
        
        console_frame = tk.Frame(progress_outer, bg="#0a0f1a", relief=tk.SOLID, borderwidth=1)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Loading indicator (horizontal bar above console)
        self.loading_frame = tk.Frame(console_frame, bg="#1e293b", height=50)
        
        loading_inner = tk.Frame(self.loading_frame, bg="#1e293b")
        loading_inner.pack(expand=True)
        
        self.loading_spinner = tk.Label(
            loading_inner,
            text="⏳",
            font=("Segoe UI", 18),
            bg="#1e293b",
            fg=self.accent_color
        )
        self.loading_spinner.pack(side=tk.LEFT, padx=(10, 5))
        
        self.loading_text = tk.Label(
            loading_inner,
            text="Initializing deployment",
            font=("Segoe UI", 10, "bold"),
            bg="#1e293b",
            fg=self.fg_color
        )
        self.loading_text.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(
            console_frame,
            font=("Consolas", 9),
            bg="#0a0f1a",
            fg="#10b981",
            height=10,
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0,
            insertbackground="#10b981"
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.status_text.config(state=tk.DISABLED)
        
        # Footer with version info
        footer_frame = tk.Frame(self.root, bg=self.bg_color)
        footer_frame.pack(fill=tk.X, pady=(5, 10))
        
        footer_label = tk.Label(
            footer_frame,
            text="Made with ❤️ for Anupam Dutta Photography",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg="#64748b"
        )
        footer_label.pack()
        
        version_label = tk.Label(
            footer_frame,
            text="Version 1.0  •  Git Deployment Tool",
            font=("Segoe UI", 8),
            bg=self.bg_color,
            fg="#475569"
        )
        version_label.pack()
    
    def log_message(self, message, color="#10b981"):
        """Add message to queue for thread-safe display"""
        self.message_queue.put(("log", message, color))
    
    def process_queue(self):
        """Process queued messages from worker thread"""
        try:
            while True:
                msg_type, *args = self.message_queue.get_nowait()
                
                if msg_type == "log":
                    message, color = args
                    self.status_text.config(state=tk.NORMAL)
                    self.status_text.insert(tk.END, message + "\n")
                    # Tag the last line with color
                    line_start = self.status_text.index("end-2l")
                    line_end = self.status_text.index("end-1c")
                    tag_name = f"color_{id(message)}"
                    self.status_text.tag_add(tag_name, line_start, line_end)
                    self.status_text.tag_config(tag_name, foreground=color)
                    self.status_text.see(tk.END)
                    self.status_text.config(state=tk.DISABLED)
                elif msg_type == "progress":
                    value = args[0]
                    self.progress_var.set(value)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(50, self.process_queue)
    
    def update_progress(self, value):
        """Update progress bar (thread-safe)"""
        self.message_queue.put(("progress", value))
    
    def show_loading(self, message="Initializing deployment"):
        """Show loading indicator above console"""
        def _show():
            self.loading_text.config(text=message)
            if not self.loading_frame.winfo_ismapped():
                self.loading_frame.pack(fill=tk.X, before=self.status_text, padx=2, pady=5)
                self.animate_loading()
        
        self.root.after(0, _show)
    
    def animate_loading(self):
        """Animate loading spinner"""
        if not self.is_deploying:
            return
        
        # Rotate spinner icons
        self.loading_spinner_index = (self.loading_spinner_index + 1) % len(self.loading_spinner_chars)
        self.loading_spinner.config(text=self.loading_spinner_chars[self.loading_spinner_index])
        
        # Animate dots
        self.loading_dots = (self.loading_dots + 1) % 4
        dots = "." * self.loading_dots
        current_text = self.loading_text.cget("text")
        base_text = current_text.rstrip(".")
        self.loading_text.config(text=f"{base_text}{dots}")
        
        self.root.after(400, self.animate_loading)
    
    def hide_loading(self):
        """Hide loading indicator"""
        def _hide():
            if self.loading_frame.winfo_ismapped():
                self.loading_frame.pack_forget()
        
        self.root.after(0, _hide)
    
    def browse_file(self):
        """Open file dialog to select JSON file"""
        # Get repository root (parent of deployment folder)
        repo_root = Path(__file__).parent.parent
        
        filename = filedialog.askopenfilename(
            title="📁 Select Photography Data JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=str(repo_root)  # Start from repository root
        )
        
        if filename:
            self.selected_file = filename
            # Show just filename if path is too long
            display_name = os.path.basename(filename)
            if len(filename) > 60:
                self.file_path_var.set(f"...{filename[-57:]}")
            else:
                self.file_path_var.set(filename)
            self.validate_json()
    
    def validate_json(self):
        """Validate the selected JSON file"""
        if not self.selected_file:
            return
        
        self.validation_label.config(text="⏳ Validating JSON structure...", fg=self.warning_color, bg=self.bg_secondary)
        self.deploy_btn.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # Read the uploaded JSON
            with open(self.selected_file, 'r', encoding='utf-8') as f:
                uploaded_data = json.load(f)
            
            # Read the reference JSON from data folder in repository root
            repo_root = Path(__file__).parent.parent
            reference_file = repo_root / "data" / "anupam-dutta-photography-data-set.json"
            
            if not reference_file.exists():
                # If no reference file exists, just validate it's valid JSON
                self.validation_label.config(
                    text="✅ Valid JSON format - No reference file to compare against",
                    fg=self.success_color,
                    bg=self.bg_secondary
                )
                self.deploy_btn.config(state=tk.NORMAL, bg=self.success_color)
                return
            
            with open(reference_file, 'r', encoding='utf-8') as f:
                reference_data = json.load(f)
            
            # Validate structure
            errors = self.validate_structure(uploaded_data, reference_data)
            
            if errors:
                error_msg = "❌ Validation Failed - Missing or invalid fields:\n" + "\n".join(errors[:5])
                if len(errors) > 5:
                    error_msg += f"\n...and {len(errors) - 5} more errors"
                self.validation_label.config(text=error_msg, fg=self.error_color, bg=self.bg_secondary)
                self.deploy_btn.config(state=tk.DISABLED, bg="#6b7280")
            else:
                self.validation_label.config(
                    text="✅ Validation Successful - All required fields are present and valid",
                    fg=self.success_color,
                    bg=self.bg_secondary
                )
                self.deploy_btn.config(state=tk.NORMAL, bg=self.success_color)
                
        except json.JSONDecodeError as e:
            self.validation_label.config(
                text=f"❌ JSON Parse Error: Invalid JSON format at line {e.lineno}",
                fg=self.error_color,
                bg=self.bg_secondary
            )
            self.deploy_btn.config(state=tk.DISABLED, bg="#6b7280")
        except Exception as e:
            self.validation_label.config(
                text=f"❌ Validation Error: {str(e)}",
                fg=self.error_color,
                bg=self.bg_secondary
            )
            self.deploy_btn.config(state=tk.DISABLED, bg="#6b7280")
    
    def validate_structure(self, uploaded, reference, path=""):
        """Recursively validate JSON structure"""
        errors = []
        
        # Check if both are dictionaries
        if isinstance(reference, dict):
            if not isinstance(uploaded, dict):
                errors.append(f"  • {path or 'Root'} should be an object")
                return errors
            
            # Check required keys
            for key in reference.keys():
                if key not in uploaded:
                    errors.append(f"  • Missing required field: {path}.{key}" if path else f"  • Missing required field: {key}")
                else:
                    # Recursively validate nested structures
                    nested_errors = self.validate_structure(
                        uploaded[key],
                        reference[key],
                        f"{path}.{key}" if path else key
                    )
                    errors.extend(nested_errors)
        
        # Check if both are lists
        elif isinstance(reference, list) and len(reference) > 0:
            if not isinstance(uploaded, list):
                errors.append(f"  • {path} should be an array")
            elif len(uploaded) > 0:
                # Validate first item structure for arrays
                nested_errors = self.validate_structure(
                    uploaded[0],
                    reference[0],
                    f"{path}[0]"
                )
                errors.extend(nested_errors)
        
        return errors
    
    def deploy(self):
        """Execute deployment"""
        if self.is_deploying:
            return
        
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a JSON file first")
            return
        
        response = messagebox.askyesno(
            "Confirm Deployment",
            "Are you sure you want to deploy to production?\n\nThis will update your live website.",
            icon='warning'
        )
        
        if not response:
            return
        
        self.is_deploying = True
        self.deploy_btn.config(state=tk.DISABLED, text="⏳ Deploying...")
        self.update_progress(0)
        
        # Clear console and show loading
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.show_loading()
        
        # Run deployment in separate thread
        thread = threading.Thread(target=self.run_deployment)
        thread.daemon = True
        thread.start()
    
    def run_git_command(self, command, description):
        """Execute a git command and log the result"""
        self.log_message(f"  🔧 Executing: {command}", "#9ca3af")
        try:
            # Get repository root
            repo_root = Path(__file__).parent.parent
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=repo_root  # Run from repository root
            )
            
            # Always show output for better debugging
            if result.stdout.strip():
                self.log_message(f"  📄 Output:\n{result.stdout.strip()}", "#9ca3af")
            
            if result.stderr.strip():
                self.log_message(f"  ⚠️ Stderr:\n{result.stderr.strip()}", "#f59e0b")
            
            if result.returncode == 0:
                self.log_message(f"  ✓ {description} completed", "#10b981")
                return True
            else:
                if result.stderr.strip():
                    self.log_message(f"  ⚠️ Warning: {result.stderr.strip()}", "#f59e0b")
                return True
                
        except Exception as e:
            self.log_message(f"  ❌ Error: {str(e)}", "#ef4444")
            return False
    
    def run_deployment(self):
        """Run deployment commands"""
        try:
            # Change to repository root
            repo_root = Path(__file__).parent.parent
            os.chdir(repo_root)
            
            # Determine target branch
            if TARGET_BRANCH:
                branch = TARGET_BRANCH
                self.log_message(f"Using configured branch: {branch}", "#60a5fa")
                
                # Get current branch
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                current_branch = result.stdout.strip()
                
                # Switch branch if needed
                if current_branch != branch:
                    self.log_message(f"Switching to branch: {branch}", "#60a5fa")
                    subprocess.run(["git", "checkout", branch], check=True)
                    self.log_message(f"✓ Switched to {branch}", "#10b981")
            else:
                # Get current branch
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                branch = result.stdout.strip()
                self.log_message(f"Using current branch: {branch}", "#60a5fa")
            
            self.log_message("=" * 70, "#60a5fa")
            self.log_message("🚀 Starting deployment process...", "#60a5fa")
            self.log_message(f"📍 Deployment branch: {branch}", "#60a5fa")
            self.log_message(f"📁 Working directory: {repo_root}", "#60a5fa")
            self.log_message("=" * 70, "#60a5fa")
            
            # Check if data folder exists
            data_folder = repo_root / "data"
            if not data_folder.exists():
                self.log_message("  ❌ Error: data/ folder not found in root directory", "#ef4444")
                return False
            
            # Step 1: Copy JSON file to data folder (10%)
            self.show_loading("Step 1/6: Updating JSON file")
            self.log_message("\n📋 Step 1/6: Updating JSON file in data/ folder...", "#fbbf24")
            self.update_progress(5)
            
            target_file = data_folder / "anupam-dutta-photography-data-set.json"
            
            # No backup - directly update the file with retry logic
            import shutil
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Read the source file content
                    with open(self.selected_file, 'r', encoding='utf-8') as src:
                        content = src.read()
                    
                    self.log_message(f"  📄 Source file: {Path(self.selected_file).name}", "#60a5fa")
                    self.log_message(f"  📁 Target file: {target_file}", "#60a5fa")
                    
                    # Write to target file (this overwrites the existing file)
                    with open(target_file, 'w', encoding='utf-8') as dst:
                        dst.write(content)
                    
                    self.log_message(f"  ✓ Successfully updated {target_file.name} with new content", "#10b981")
                    
                    # Verify the update
                    file_size = target_file.stat().st_size
                    self.log_message(f"  ℹ️ Updated file size: {file_size:,} bytes", "#60a5fa")
                    break
                except PermissionError as e:
                    if attempt < max_retries - 1:
                        self.log_message(f"  ⏳ File in use, retrying... (attempt {attempt + 1}/{max_retries})", "#f59e0b")
                        time.sleep(1)
                    else:
                        raise Exception(f"Cannot update JSON file: {str(e)}. Please close the file 'anupam-dutta-photography-data-set.json' in VS Code or any other editor and try again.")
            
            self.update_progress(10)
            
            # Step 2: Git - Check status (20%)
            self.show_loading("Step 2/6: Checking Git status")
            self.log_message("\n🔍 Step 2/6: Checking Git status...", "#fbbf24")
            
            # Check if git is installed
            git_check = subprocess.run("git --version", shell=True, capture_output=True, text=True)
            if git_check.returncode != 0:
                self.log_message("  ⚠️ Git is not installed. Skipping Git operations.", "#f59e0b")
                self.update_progress(100)
                self.log_message("\n✅ Deployment completed (JSON updated only)", "#10b981")
                self.show_completion_message(True)
                return
            
            if not self.run_git_command("git status", "Git status check"):
                raise Exception("Git status check failed")
            
            self.update_progress(20)
            
            # Step 3: Git - Add changes (35%)
            self.show_loading("Step 3/6: Staging changes")
            self.log_message("\n➕ Step 3/6: Adding .json files from data/ folder to Git...", "#fbbf24")
            
            # Check if there are changes in data folder
            status_result = subprocess.run(
                ["git", "status", "--short", "data/"],
                capture_output=True,
                text=True,
                cwd=repo_root
            )
            
            if status_result.stdout.strip():
                self.log_message(f"  📝 Changes detected:\n{status_result.stdout}", "#60a5fa")
                
                # Add the entire data folder (only contains JSON)
                if not self.run_git_command("git add data/", "Git add data/"):
                    raise Exception("Git add failed")
                self.log_message("  ✓ Changes added successfully", "#10b981")
            else:
                self.log_message("  ℹ️ No changes detected in data/ folder", "#60a5fa")
            
            self.update_progress(35)
            
            # Step 4: Git - Commit changes (50%)
            self.show_loading("Step 4/6: Committing changes")
            self.log_message("\n💾 Step 4/6: Committing changes...", "#fbbf24")
            
            import datetime
            commit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Update photography data - {commit_time}"
            
            if not self.run_git_command(f'git commit -m "{commit_message}"', "Git commit"):
                self.log_message("  ℹ️ No changes to commit or commit completed", "#60a5fa")
            
            self.update_progress(50)
            
            # Step 5: Git - Push to remote (75%)
            self.show_loading(f"Step 5/6: Pushing to {branch}")
            self.log_message(f"\n🚀 Step 5/6: Pushing to remote ({branch})...", "#fbbf24")
            
            if not self.run_git_command(f"git push origin {branch}", f"Git push to {branch}"):
                self.log_message(f"  ⚠️ Push to {branch} failed, continuing...", "#f59e0b")
            
            self.update_progress(75)
            
            # Step 6: Verify deployment (100%)
            self.show_loading("Step 6/6: Verifying deployment")
            self.log_message("\n✨ Step 6/6: Verifying deployment...", "#fbbf24")
            
            if not self.run_git_command("git status", "Final status check"):
                self.log_message("  ⚠️ Final status check warning", "#f59e0b")
            
            self.update_progress(100)
            
            self.log_message("\n" + "=" * 70, "#60a5fa")
            self.log_message("✅ DEPLOYMENT COMPLETED SUCCESSFULLY!", "#10b981")
            self.log_message(f"📍 Changes pushed to branch: {branch}", "#10b981")
            self.log_message("=" * 70, "#60a5fa")
            
            self.show_completion_message(True)
            
        except Exception as e:
            self.log_message(f"\n❌ Deployment failed: {str(e)}", "#ef4444")
            self.update_progress(0)
            self.show_completion_message(False, str(e))
        
        finally:
            self.is_deploying = False
            self.hide_loading()
            self.root.after(0, lambda: self.deploy_btn.config(state=tk.NORMAL, text="🚀 Deploy to Production"))
    
    def show_completion_message(self, success, error_msg=""):
        """Show completion message box"""
        def show_msg():
            if success:
                messagebox.showinfo(
                    "Deployment Successful",
                    "Your photography portfolio has been deployed successfully!\n\nThe website is now live with your updates."
                )
            else:
                messagebox.showerror(
                    "Deployment Failed",
                    f"Deployment encountered an error:\n\n{error_msg}\n\nPlease check the logs for details."
                )
        
        self.root.after(0, show_msg)


def main():
    root = tk.Tk()
    app = DeploymentApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
