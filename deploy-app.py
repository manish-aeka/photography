import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import subprocess
import threading
import os
import sys
import time
from pathlib import Path

# Configuration
DEPLOYMENT_BRANCH = "feat"  # Change this to your deployment branch name (e.g., "main", "master", "feat")


class Tooltip:
    """Simple tooltip for tkinter widgets"""
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.id = None
        self.tw = None
        try:
            widget.bind("<Enter>", self.schedule)
            widget.bind("<Leave>", self.hide)
        except Exception:
            pass

    def schedule(self, _event=None):
        try:
            self.id = self.widget.after(self.delay, self.show)
        except Exception:
            self.id = None

    def show(self):
        if self.tw:
            return
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 1
            self.tw = tk.Toplevel(self.widget)
            self.tw.wm_overrideredirect(True)
            self.tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self.tw, text=self.text, justify=tk.LEFT,
                             background="#333333", foreground="#ffffff",
                             relief=tk.SOLID, borderwidth=1, padx=6, pady=3,
                             font=("Segoe UI", 9))
            label.pack()
        except Exception:
            pass

    def hide(self, _event=None):
        if self.id:
            try:
                self.widget.after_cancel(self.id)
            except Exception:
                pass
            self.id = None
        if self.tw:
            try:
                self.tw.destroy()
            except Exception:
                pass
            self.tw = None


def find_data_files():
    """Return list of candidate JSON data files from common locations"""
    search_paths = [
        Path.cwd(),
        Path.home(),
        Path.home() / "Photography",
        Path.home() / "Documents",
        Path.home() / "Desktop",
        Path("/Users/saugata/Photography"),
    ]
    found_files = []
    for search_path in search_paths:
        try:
            if search_path.exists():
                for f in search_path.glob("*.json"):
                    name = f.name.lower()
                    if any(k in name for k in ("photography", "data", "anupam")):
                        found_files.append(f)
        except Exception:
            continue
    # also include cwd JSONs if nothing matched
    if not found_files:
        for f in Path.cwd().glob("*.json"):
            found_files.append(f)
    return found_files

class DeploymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photography Portfolio Deployment")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set color scheme
        self.bg_color = "#1f2937"
        self.fg_color = "#f3f4f6"
        self.accent_color = "#1C5BAE"
        self.success_color = "#10b981"
        self.error_color = "#ef4444"
        
        self.root.configure(bg=self.bg_color)
        
        self.selected_file = None
        self.is_deploying = False
        
        self.setup_ui()
        self.auto_detect_json_files()
        
    def auto_detect_json_files(self):
        """Auto-detect and load JSON files from multiple locations"""
        search_paths = [
            Path.cwd(),  # Current working directory
            Path.home(),  # Home directory
            Path.home() / "Photography",  # Photography folder
            Path.home() / "Documents",  # Documents folder
            Path.home() / "Desktop",  # Desktop folder
            Path("/Users/saugata/Photography"),  # Specific project directory
        ]
        
        found_files = []
        
        # Search in all paths for JSON files
        for search_path in search_paths:
            if search_path.exists():
                json_files = list(search_path.glob("*.json"))
                # Look for common data file names
                data_files = [f for f in json_files if "photography" in f.name.lower() or "data" in f.name.lower() or "anupam" in f.name.lower()]
                found_files.extend(data_files)
        
        if found_files:
            # Use the first matching data file
            selected = found_files[0]
            self.selected_file = str(selected)
            self.file_path_var.set(f"Auto-loaded: {selected.name}")
            self.validate_json()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="📸 Photography Portfolio Deployment",
            font=("Segoe UI", 18, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=18)

        subtitle = tk.Label(
            header_frame,
            text="Validate and deploy your photography dataset — fast and safe",
            font=("Segoe UI", 10),
            bg=self.accent_color,
            fg="#e6eef8"
        )
        subtitle.pack(side=tk.LEFT, padx=(10, 0), pady=22)

        # Main container (two columns)
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)
        main_frame.columnconfigure(1, weight=1)

        # Left: File selection & controls
        left_frame = tk.Frame(main_frame, bg=self.bg_color, width=360)
        left_frame.grid(row=0, column=0, sticky="nsw", padx=(0, 12), pady=4)

        file_frame = tk.LabelFrame(
            left_frame,
            text="📁 File & Controls",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=10
        )
        file_frame.pack(fill=tk.X)

        # Combobox for discovered JSON files
        self.file_path_var = tk.StringVar(value="No file selected")
        self.file_combo = ttk.Combobox(file_frame, values=[], state="readonly")
        self.file_combo.pack(fill=tk.X, pady=(4, 8))
        self.file_combo.bind("<<ComboboxSelected>>", lambda e: self.on_file_selected())

        # Small path display
        file_path_label = tk.Label(
            file_frame,
            textvariable=self.file_path_var,
            font=("Segoe UI", 9),
            bg="#374151",
            fg=self.fg_color,
            anchor="w",
            relief=tk.SUNKEN,
            padx=8,
            pady=6
        )
        file_path_label.pack(fill=tk.X, pady=(0, 8))

        # Control buttons
        btn_row = tk.Frame(file_frame, bg=self.bg_color)
        btn_row.pack(fill=tk.X, pady=(0, 6))

        refresh_btn = tk.Button(btn_row, text="🔄 Refresh", command=self.refresh_file_list, bg="#2563eb", fg="white", relief=tk.FLAT, padx=8)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 6))
        Tooltip(refresh_btn, "Refresh file list (Ctrl+R)")

        browse_btn = tk.Button(btn_row, text="🔍 Browse", command=self.browse_file, bg=self.accent_color, fg="white", relief=tk.FLAT, padx=8)
        browse_btn.pack(side=tk.LEFT, padx=(0, 6))
        Tooltip(browse_btn, "Select a JSON file (Ctrl+O)")

        open_btn = tk.Button(btn_row, text="📂 Open Folder", command=self.open_selected_folder, bg="#374151", fg="white", relief=tk.FLAT, padx=8)
        open_btn.pack(side=tk.LEFT)
        Tooltip(open_btn, "Open folder containing selected file")

        scan_btn = tk.Button(file_frame, text="🔎 Scan Locations", command=self.refresh_file_list, bg="#065f46", fg="white", relief=tk.FLAT)
        scan_btn.pack(fill=tk.X, pady=(6, 0))
        Tooltip(scan_btn, "Scan common locations for dataset files")

        # Validation status area (under controls)
        self.validation_frame = tk.Frame(left_frame, bg=self.bg_color)
        self.validation_frame.pack(fill=tk.X, pady=(12, 6))

        self.validation_label = tk.Label(
            self.validation_frame,
            text="",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            wraplength=320,
            justify=tk.LEFT
        )
        self.validation_label.pack()

        # Right: Progress and deploy
        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Deploy button (prominent)
        self.deploy_btn = tk.Button(
            right_frame,
            text="🚀 Deploy",
            font=("Segoe UI", 14, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=0,
            padx=24,
            pady=12,
            state=tk.DISABLED,
            command=self.deploy
        )
        self.deploy_btn.pack(anchor="ne", pady=(0, 10))

        # Progress section
        progress_frame = tk.LabelFrame(
            right_frame,
            text="📊 Deployment Progress",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            relief=tk.GROOVE,
            borderwidth=2
        )
        progress_frame.pack(fill=tk.BOTH, expand=True)

        # Progress bar
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, padx=12, pady=(12, 8))

        # Status text
        self.status_text = scrolledtext.ScrolledText(
            progress_frame,
            font=("Consolas", 10),
            bg="#0b1220",
            fg="#a7f3d0",
            height=14,
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        self.status_text.config(state=tk.DISABLED)

        # Footer
        footer_label = tk.Label(
            self.root,
            text="Made with ❤️ for Anupam Dutta Photography",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg="#9ca3af"
        )
        footer_label.pack(pady=(6, 10))

        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.browse_file())
        self.root.bind('<Control-r>', lambda e: self.refresh_file_list())
        self.root.bind('<Control-d>', lambda e: self.deploy())

        # Initial population of file list
        self.refresh_file_list()
    
    def log_message(self, message, color="#10b981"):
        """Add message to status text"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.tag_add("color", "end-2c linestart", "end-1c")
        self.status_text.tag_config("color", foreground=color)
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
    
    def browse_file(self):
        """Open file dialog to select JSON file"""
        filename = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )
        
        if filename:
            self.selected_file = filename
            # update combobox if present
            try:
                if hasattr(self, 'file_combo'):
                    self.file_combo.set(Path(filename).name)
            except Exception:
                pass
            self.file_path_var.set(filename)
            self.validate_json()

    def on_file_selected(self):
        """Handle selection from combobox"""
        name = self.file_combo.get()
        if not name:
            return
        # find full path from discovered files
        candidates = find_data_files()
        for f in candidates:
            if f.name == name:
                self.selected_file = str(f)
                self.file_path_var.set(str(f))
                self.validate_json()
                return

    def refresh_file_list(self):
        """Populate combobox with discovered files"""
        files = find_data_files()
        names = [f.name for f in files]
        try:
            self.file_combo['values'] = names
        except Exception:
            pass

        if files:
            # select first by default
            first = files[0]
            try:
                self.file_combo.set(first.name)
            except Exception:
                pass
            self.selected_file = str(first)
            self.file_path_var.set(str(first))
            self.validate_json()
        else:
            self.file_path_var.set("No data files found")

    def open_selected_folder(self):
        """Open the folder that contains the selected file"""
        if not self.selected_file:
            messagebox.showinfo("No file", "No file selected to open folder for.")
            return
        folder = Path(self.selected_file).parent
        try:
            if os.name == 'nt':
                subprocess.run(['explorer', str(folder)])
            elif sys.platform == 'darwin':
                subprocess.run(['open', str(folder)])
            else:
                subprocess.run(['xdg-open', str(folder)])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")
    
    def validate_json(self):
        """Validate the selected JSON file"""
        if not self.selected_file:
            return
        
        self.validation_label.config(text="⏳ Validating JSON file...", fg="#f59e0b")
        self.deploy_btn.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # Read the uploaded JSON
            with open(self.selected_file, 'r', encoding='utf-8') as f:
                uploaded_data = json.load(f)
            
            # Search for reference file in multiple locations
            search_paths = [
                Path.cwd(),
                Path.home(),
                Path.home() / "Photography",
                Path.home() / "Documents",
                Path.home() / "Desktop",
                Path("/Users/saugata/Photography"),
                Path(self.selected_file).parent,  # Same directory as selected file
            ]
            
            reference_file = None
            for search_path in search_paths:
                candidate = search_path / "anupam-dutta-photography-data-set.json"
                if candidate.exists():
                    reference_file = candidate
                    break
            
            if not reference_file:
                self.validation_label.config(
                    text="❌ Reference file 'anupam-dutta-photography-data-set.json' not found in common locations",
                    fg=self.error_color
                )
                return
            
            with open(reference_file, 'r', encoding='utf-8') as f:
                reference_data = json.load(f)
            
            # Validate structure
            errors = self.validate_structure(uploaded_data, reference_data)
            
            if errors:
                error_msg = "❌ Validation failed:\n" + "\n".join(errors)
                self.validation_label.config(text=error_msg, fg=self.error_color)
                self.deploy_btn.config(state=tk.DISABLED)
            else:
                self.validation_label.config(
                    text="✅ JSON validation successful! All required fields are present.",
                    fg=self.success_color
                )
                self.deploy_btn.config(state=tk.NORMAL)
                
        except json.JSONDecodeError as e:
            self.validation_label.config(
                text=f"❌ Invalid JSON format: {str(e)}",
                fg=self.error_color
            )
            self.deploy_btn.config(state=tk.DISABLED)
        except Exception as e:
            self.validation_label.config(
                text=f"❌ Error: {str(e)}",
                fg=self.error_color
            )
            self.deploy_btn.config(state=tk.DISABLED)
    
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
        self.progress_var.set(0)
        
        # Run deployment in separate thread
        thread = threading.Thread(target=self.run_deployment)
        thread.daemon = True
        thread.start()
    
    def run_git_command(self, command, description):
        """Execute a git command and log the result"""
        self.log_message(f"  Executing: {command}", "#9ca3af")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            
            if result.stdout.strip():
                self.log_message(f"  Output: {result.stdout.strip()}", "#9ca3af")
            
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
            self.log_message("=" * 70, "#60a5fa")
            self.log_message("🚀 Starting deployment process...", "#60a5fa")
            self.log_message(f"📍 Deployment branch: {DEPLOYMENT_BRANCH}", "#60a5fa")
            self.log_message("=" * 70, "#60a5fa")
            
            # Step 1: Copy JSON file (10%)
            self.log_message("\n📋 Step 1/6: Updating JSON file...", "#fbbf24")
            self.progress_var.set(5)
            
            target_file = Path(__file__).parent / "anupam-dutta-photography-data-set.json"
            
            # Backup existing file with retry logic
            if target_file.exists():
                backup_file = Path(__file__).parent / "anupam-dutta-photography-data-set.json.backup"
                import shutil
                
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        shutil.copy2(target_file, backup_file)
                        self.log_message(f"  ✓ Backup created: {backup_file.name}", "#10b981")
                        break
                    except PermissionError as e:
                        if attempt < max_retries - 1:
                            self.log_message(f"  ⏳ File in use, retrying... (attempt {attempt + 1}/{max_retries})", "#f59e0b")
                            time.sleep(1)
                        else:
                            raise Exception(f"Cannot create backup: {str(e)}. Please close the JSON file in any editors and try again.")
            
            # Copy new file with retry logic
            import shutil
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Read the source file content
                    with open(self.selected_file, 'r', encoding='utf-8') as src:
                        content = src.read()
                    
                    # Write to target file
                    with open(target_file, 'w', encoding='utf-8') as dst:
                        dst.write(content)
                    
                    self.log_message(f"  ✓ JSON file updated successfully", "#10b981")
                    break
                except PermissionError as e:
                    if attempt < max_retries - 1:
                        self.log_message(f"  ⏳ File in use, retrying... (attempt {attempt + 1}/{max_retries})", "#f59e0b")
                        time.sleep(1)
                    else:
                        raise Exception(f"Cannot update JSON file: {str(e)}. Please close the file 'anupam-dutta-photography-data-set.json' in VS Code or any other editor and try again.")
            
            self.progress_var.set(10)
            
            # Step 2: Git - Check status (20%)
            self.log_message("\n🔍 Step 2/6: Checking Git repository status...", "#fbbf24")
            
            # Check if git is installed
            git_check = subprocess.run("git --version", shell=True, capture_output=True, text=True)
            if git_check.returncode != 0:
                self.log_message("  ⚠️ Git is not installed. Skipping Git operations.", "#f59e0b")
                self.progress_var.set(100)
                self.log_message("\n✅ Deployment completed (JSON updated only)", "#10b981")
                self.show_completion_message(True)
                return
            
            if not self.run_git_command("git status", "Git status check"):
                raise Exception("Git status check failed")
            
            self.progress_var.set(20)
            
            # Step 3: Git - Add changes (35%)
            self.log_message("\n➕ Step 3/6: Adding changes to Git...", "#fbbf24")
            
            if not self.run_git_command("git add .", "Git add"):
                raise Exception("Git add failed")
            
            self.progress_var.set(35)
            
            # Step 4: Git - Commit changes (50%)
            self.log_message("\n💾 Step 4/6: Committing changes...", "#fbbf24")
            
            import datetime
            commit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Update photography data - {commit_time}"
            
            if not self.run_git_command(f'git commit -m "{commit_message}"', "Git commit"):
                self.log_message("  ℹ️ No changes to commit or commit completed", "#60a5fa")
            
            self.progress_var.set(50)
            
            # Step 5: Git - Push to remote (75%)
            self.log_message(f"\n🚀 Step 5/6: Pushing to remote ({DEPLOYMENT_BRANCH})...", "#fbbf24")
            
            if not self.run_git_command(f"git push origin {DEPLOYMENT_BRANCH}", f"Git push to {DEPLOYMENT_BRANCH}"):
                self.log_message(f"  ⚠️ Push to {DEPLOYMENT_BRANCH} failed, continuing...", "#f59e0b")
            
            self.progress_var.set(75)
            
            # Step 6: Verify deployment (100%)
            self.log_message("\n✨ Step 6/6: Verifying deployment...", "#fbbf24")
            
            if not self.run_git_command("git status", "Final status check"):
                self.log_message("  ⚠️ Final status check warning", "#f59e0b")
            
            self.progress_var.set(100)
            
            self.log_message("\n" + "=" * 70, "#60a5fa")
            self.log_message("✅ DEPLOYMENT COMPLETED SUCCESSFULLY!", "#10b981")
            self.log_message(f"📍 Changes pushed to branch: {DEPLOYMENT_BRANCH}", "#10b981")
            self.log_message("=" * 70, "#60a5fa")
            
            self.show_completion_message(True)
            
        except Exception as e:
            self.log_message(f"\n❌ Deployment failed: {str(e)}", "#ef4444")
            self.progress_var.set(0)
            self.show_completion_message(False, str(e))
        
        finally:
            self.is_deploying = False
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
