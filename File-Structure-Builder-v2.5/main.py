import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import threading
try:
    import winsound
except ImportError:
    winsound = None
from builder import build_structure, count_structure_items, clean_structure_text
from ai_assistant import ProjectStructureAI

# Clean theme
THEME = {
    "bg": "#f8f9fa",
    "fg": "#212529", 
    "accent": "#007bff",
    "text_bg": "#ffffff",
    "border": "#dee2e6",
    "font": "Segoe UI"
}


class FileStructureBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 File Structure Builder v2.5 - AI Powered")
        
        # Dynamic window sizing
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate optimal size (80% of screen)
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Set minimum and maximum sizes
        min_width, min_height = 900, 650
        max_width, max_height = int(screen_width * 0.95), int(screen_height * 0.95)
        
        # Apply constraints
        window_width = max(min_width, min(window_width, max_width))
        window_height = max(min_height, min(window_height, max_height))
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(min_width, min_height)
        self.root.maxsize(max_width, max_height)
        self.root.configure(bg=THEME["bg"])
        
        self.output_dir = None
        self.ai_assistant = ProjectStructureAI()
        
        # Center window on screen
        self.center_window()
        
        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Main container with grid
        main_frame = tk.Frame(root, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header with title and subtitle
        header_frame = tk.Frame(main_frame, bg=THEME["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame, text="🚀 File Structure Builder v2.5",
            font=(THEME["font"], 18, "bold"),
            fg=THEME["accent"], bg=THEME["bg"]
        ).pack()
        
        tk.Label(
            header_frame, text="AI-Powered Project Structure Generator",
            font=(THEME["font"], 10),
            fg="#6c757d", bg=THEME["bg"]
        ).pack(pady=(2, 0))
        
        # Target directory display - improved
        self.target_frame = tk.Frame(main_frame, bg="#e8f4fd", relief="solid", bd=1)
        self.target_frame.pack(fill=tk.X, pady=(0, 20))
        
        target_inner = tk.Frame(self.target_frame, bg="#e8f4fd")
        target_inner.pack(fill=tk.X, padx=15, pady=12)
        
        tk.Label(
            target_inner, text="📁 Target Directory:",
            font=(THEME["font"], 9, "bold"), fg="#1565c0", bg="#e8f4fd"
        ).pack(side=tk.LEFT)
        
        self.target_label = tk.Label(
            target_inner, text="No folder selected",
            font=(THEME["font"], 9), fg="#1976d2", bg="#e8f4fd",
            anchor="w"
        )
        self.target_label.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Content area with adaptive grid
        content_frame = tk.Frame(main_frame, bg=THEME["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Dynamic column weights based on window size
        self.content_frame = content_frame
        self.adjust_layout()
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left: Text area - using grid
        left_frame = tk.Frame(content_frame, bg=THEME["bg"])
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left_frame.grid_rowconfigure(2, weight=1)
        
        # AI Assistant section - improved layout
        ai_frame = tk.Frame(left_frame, bg="#f0f8f0", relief="solid", bd=1)
        ai_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ai_frame.grid_columnconfigure(1, weight=1)
        
        # AI Header with better styling
        ai_header = tk.Frame(ai_frame, bg="#e8f5e8")
        ai_header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=1, pady=1)
        
        header_content = tk.Frame(ai_header, bg="#e8f5e8")
        header_content.pack(fill=tk.X, padx=12, pady=8)
        
        tk.Label(
            header_content, text="🤖 AI Assistant",
            font=(THEME["font"], 11, "bold"), fg="#2e7d32", bg="#e8f5e8"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            header_content, text="Smart project structure generation",
            font=(THEME["font"], 8), fg="#4caf50", bg="#e8f5e8"
        ).pack(side=tk.RIGHT)
        
        # AI Input area with better layout
        ai_input_frame = tk.Frame(ai_frame, bg="#f0f8f0")
        ai_input_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=12, pady=(8, 12))
        ai_input_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(
            ai_input_frame, text="Describe your project (e.g., 'React ecommerce app', 'Python ML project'):",
            font=(THEME["font"], 9), fg="#2e7d32", bg="#f0f8f0"
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        
        # Input with placeholder effect
        self.ai_input = tk.Entry(
            ai_input_frame, font=(THEME["font"], 10), bg="white", fg=THEME["fg"],
            relief="solid", bd=1, highlightthickness=0
        )
        self.ai_input.grid(row=1, column=0, sticky="ew", padx=(0, 8), ipady=4)
        self.ai_input.bind('<Return>', self.generate_ai_structure)
        self.ai_input.bind('<FocusIn>', self.on_ai_input_focus)
        
        # Add placeholder text
        self.ai_input.insert(0, "e.g., React ecommerce website with payment integration")
        self.ai_input.config(fg="#999")
        
        ai_btn = tk.Button(
            ai_input_frame, text="🤖 Generate", command=self.generate_ai_structure,
            bg="#4caf50", fg="white", relief="flat",
            font=(THEME["font"], 9, "bold"), padx=20, pady=8,
            cursor="hand2"
        )
        ai_btn.grid(row=1, column=1)
        
        tk.Label(
            left_frame, text="📝 Manual Structure Input:",
            font=(THEME["font"], 10, "bold"), fg=THEME["fg"], bg=THEME["bg"]
        ).grid(row=1, column=0, sticky="w", pady=(0, 8))
        
        text_frame = tk.Frame(left_frame, bg=THEME["border"], relief="solid", bd=1)
        text_frame.grid(row=2, column=0, sticky="nsew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame, wrap=tk.WORD, relief="flat", bd=0,
            bg=THEME["text_bg"], fg=THEME["fg"],
            font=("Consolas", 10), padx=12, pady=12,
            selectbackground="#b3d9ff"
        )
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
        
        # Bind events for live preview
        self.text_area.bind('<KeyRelease>', self.on_text_change)
        self.text_area.bind('<Button-1>', lambda e: self.root.after(50, self.on_text_change))
        self.text_area.bind('<Control-v>', lambda e: self.root.after(100, self.on_text_change))
        
        # Initial call to setup preview
        self.root.after(100, self.on_text_change)
        
        # Right: Preview - using grid
        right_frame = tk.Frame(content_frame, bg=THEME["bg"])
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(
            right_frame, text="📊 Live Preview:",
            font=(THEME["font"], 10, "bold"), fg=THEME["fg"], bg=THEME["bg"]
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        # Stats frame - improved with better visual feedback
        stats_frame = tk.Frame(right_frame, bg="#f1f8ff", relief="solid", bd=1)
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        
        # Folder stats
        folder_frame = tk.Frame(stats_frame, bg="#f1f8ff")
        folder_frame.grid(row=0, column=0, padx=8, pady=8)
        
        self.folder_count = tk.Label(
            folder_frame, text="📁 0", font=(THEME["font"], 14, "bold"),
            fg="#1976d2", bg="#f1f8ff"
        )
        self.folder_count.pack()
        
        tk.Label(
            folder_frame, text="Folders", font=(THEME["font"], 8),
            fg="#666", bg="#f1f8ff"
        ).pack()
        
        # File stats
        file_frame = tk.Frame(stats_frame, bg="#f1f8ff")
        file_frame.grid(row=0, column=1, padx=8, pady=8)
        
        self.file_count = tk.Label(
            file_frame, text="📄 0", font=(THEME["font"], 14, "bold"),
            fg="#1976d2", bg="#f1f8ff"
        )
        self.file_count.pack()
        
        tk.Label(
            file_frame, text="Files", font=(THEME["font"], 8),
            fg="#666", bg="#f1f8ff"
        ).pack()
        
        # Preview area with better styling
        preview_frame = tk.Frame(right_frame, bg=THEME["border"], relief="solid", bd=1)
        preview_frame.grid(row=2, column=0, sticky="nsew")
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        self.preview_area = scrolledtext.ScrolledText(
            preview_frame, wrap=tk.WORD, relief="flat", bd=0,
            bg="#fafbfc", fg=THEME["fg"], state="disabled",
            font=("Consolas", 9), padx=12, pady=12,
            selectbackground="#b3d9ff", cursor="arrow"
        )
        self.preview_area.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
        
        # Add initial preview content
        self.preview_area.config(state="normal")
        self.preview_area.insert("1.0", "💡 Live Preview\n\nYour file structure will appear here as you type or generate with AI.\n\n🎯 Features:\n• Real-time structure validation\n• File/folder counting\n• Syntax highlighting\n• Error detection")
        self.preview_area.config(state="disabled")
        
        # Buttons - improved layout
        btn_frame = tk.Frame(main_frame, bg=THEME["bg"])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        btn_frame.grid_columnconfigure(1, weight=1)
        
        self.folder_btn = tk.Button(
            btn_frame, text="📁 Select Folder", command=self.select_folder,
            bg="#6c757d", fg="white", relief="flat",
            font=(THEME["font"], 10), padx=25, pady=10,
            cursor="hand2"
        )
        self.folder_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        self.build_btn = tk.Button(
            btn_frame, text="🚀 Build Structure", command=self.build,
            bg=THEME["accent"], fg="white", relief="flat",
            font=(THEME["font"], 11, "bold"), padx=35, pady=10,
            cursor="hand2"
        )
        self.build_btn.pack(side=tk.RIGHT)
        
        # Status - improved
        status_frame = tk.Frame(main_frame, bg="#f8f9fa", relief="solid", bd=1)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.status_label = tk.Label(
            status_frame, text="💡 Select a folder and describe your project or paste structure manually",
            font=(THEME["font"], 9), fg="#495057", bg="#f8f9fa",
            padx=15, pady=10
        )
        self.status_label.pack(fill=tk.X)

    def on_text_change(self, event=None):
        """FIXED Live Preview Function"""
        try:
            # Get current text
            structure_text = self.text_area.get("1.0", tk.END).strip()
            
            # Enable preview area for editing
            self.preview_area.config(state="normal")
            self.preview_area.delete("1.0", tk.END)
            
            if structure_text:
                try:
                    # Use builder functions to process
                    cleaned_text = clean_structure_text(structure_text)
                    folders, files = count_structure_items(cleaned_text)
                    
                    # Update counters
                    self.folder_count.config(text=f"📁 {folders}", fg="#1976d2")
                    self.file_count.config(text=f"📄 {files}", fg="#1976d2")
                    
                    # Build preview content
                    preview_lines = []
                    preview_lines.append(f"📊 Live Preview: {folders} folders, {files} files")
                    preview_lines.append("─" * 40)
                    preview_lines.append("")
                    
                    # Add structure with emojis
                    lines = cleaned_text.splitlines()
                    for line in lines[:25]:
                        if line.strip():
                            # Clean the line to check content
                            clean_part = line.replace("├──", "").replace("└──", "").replace("│", "").replace("─", "").strip()
                            
                            if clean_part.endswith('/'):
                                # Folder
                                if "📁" not in line:
                                    line = line.replace(clean_part, f"📁 {clean_part}")
                            elif '.' in clean_part:
                                # File
                                emoji = self.get_file_emoji(clean_part)
                                if not any(e in line for e in ['📄', '🐍', '☕', '🌐', '🎨']):
                                    line = line.replace(clean_part, f"{emoji} {clean_part}")
                            
                            preview_lines.append(line)
                    
                    if len(lines) > 25:
                        preview_lines.append(f"\n... {len(lines) - 25} more items")
                    
                    # Insert all content
                    self.preview_area.insert("1.0", "\n".join(preview_lines))
                    
                    # Update status
                    self.status_label.config(
                        text=f"✅ Ready: {folders} folders, {files} files",
                        fg="#28a745"
                    )
                    
                except Exception as e:
                    # Error in processing
                    self.folder_count.config(text="📁 0", fg="#dc3545")
                    self.file_count.config(text="📄 0", fg="#dc3545")
                    
                    self.preview_area.insert("1.0", f"❌ Error: {str(e)}\n\nCheck your structure format")
                    
                    self.status_label.config(
                        text="⚠️ Invalid format",
                        fg="#dc3545"
                    )
            else:
                # Empty input
                self.folder_count.config(text="📁 0", fg="#6c757d")
                self.file_count.config(text="📄 0", fg="#6c757d")
                
                welcome = "💡 Live Preview\n\n"
                welcome += "Structure will appear here as you type!\n\n"
                welcome += "Try:\n• Use AI Assistant\n• Paste structure manually\n\n"
                welcome += "Example:\nsrc/\n├── components/\n└── utils/\nREADME.md"
                
                self.preview_area.insert("1.0", welcome)
                
                self.status_label.config(
                    text="💡 Ready - describe project or paste structure",
                    fg="#6c757d"
                )
            
            # Disable preview area
            self.preview_area.config(state="disabled")
            
        except Exception as e:
            print(f"Preview error: {e}")
    
    def get_file_emoji(self, filename: str) -> str:
        """Get appropriate emoji for file type"""
        ext = filename.split('.')[-1].lower() if '.' in filename else ''
        
        emoji_map = {
            'js': '🟨', 'jsx': '⚛️', 'ts': '🔷', 'tsx': '⚛️',
            'py': '🐍', 'java': '☕', 'cpp': '⚙️', 'c': '⚙️',
            'html': '🌐', 'css': '🎨', 'scss': '🎨', 'sass': '🎨',
            'json': '📋', 'xml': '📋', 'yml': '⚙️', 'yaml': '⚙️',
            'md': '📝', 'txt': '📄', 'pdf': '📕',
            'png': '🖼️', 'jpg': '🖼️', 'jpeg': '🖼️', 'gif': '🖼️',
            'mp4': '🎬', 'mp3': '🎵', 'wav': '🎵',
            'zip': '📦', 'tar': '📦', 'gz': '📦'
        }
        
        return emoji_map.get(ext, '📄')
    
    def apply_preview_highlighting(self):
        """Apply syntax highlighting to preview"""
        try:
            # Configure text tags
            self.preview_area.tag_configure("folder", foreground="#1976d2", font=("Consolas", 9, "bold"))
            self.preview_area.tag_configure("file", foreground="#424242")
            self.preview_area.tag_configure("summary", foreground="#2e7d32", font=("Consolas", 9, "bold"))
            self.preview_area.tag_configure("tree", foreground="#9e9e9e")
            
            # Get all content
            content = self.preview_area.get("1.0", tk.END)
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                line_start = f"{i+1}.0"
                line_end = f"{i+1}.end"
                
                if "Structure Summary" in line or "─" in line:
                    self.preview_area.tag_add("summary", line_start, line_end)
                elif any(char in line for char in ['├', '└', '│']):
                    # Tree structure lines
                    if line.strip().endswith('/') or '📁' in line:
                        self.preview_area.tag_add("folder", line_start, line_end)
                    elif '.' in line:
                        self.preview_area.tag_add("file", line_start, line_end)
                    else:
                        self.preview_area.tag_add("tree", line_start, line_end)
                elif line.strip().endswith('/') or '📁' in line:
                    self.preview_area.tag_add("folder", line_start, line_end)
                elif '.' in line and line.strip():
                    self.preview_area.tag_add("file", line_start, line_end)
        except Exception as e:
            print(f"Highlighting error: {e}")
    
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir = folder
            folder_name = os.path.basename(folder) or folder
            self.folder_btn.config(text=f"📁 {folder_name}", bg="#28a745")
            self.target_label.config(text=folder)
            self.status_label.config(text=f"✅ Ready to build in: {folder_name}", fg="#28a745")
    
    def play_success_sound(self):
        """Play success sound"""
        try:
            if winsound:
                winsound.MessageBeep(winsound.MB_OK)
        except:
            pass
    
    def build_in_thread(self):
        """Build structure in separate thread"""
        structure_text = self.text_area.get("1.0", tk.END).strip()
        
        try:
            self.root.after(0, lambda: self.status_label.config(text="🔄 Building structure...", fg="#ffc107"))
            
            created_items = build_structure(self.output_dir, structure_text)
            
            # Success
            success_msg = f"✅ Created {len(created_items)} items successfully!"
            self.root.after(0, lambda: self.status_label.config(text=success_msg, fg="#28a745"))
            self.root.after(0, self.play_success_sound)
            
        except Exception as e:
            error_msg = f"❌ Error: {e}"
            self.root.after(0, lambda: self.status_label.config(text=error_msg, fg="#dc3545"))
    
    def build(self):
        if not self.output_dir:
            messagebox.showwarning("No Folder", "Please select a folder first!")
            return
        
        structure_text = self.text_area.get("1.0", tk.END).strip()
        if not structure_text:
            messagebox.showwarning("Empty", "Please paste your file structure!")
            return
        
        # Build in separate thread to avoid UI freezing
        threading.Thread(target=self.build_in_thread, daemon=True).start()
    
    def center_window(self):
        """Center window on screen with better positioning"""
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position (slightly above center for better visual balance)
        x = (screen_width - width) // 2
        y = max(50, (screen_height - height) // 2 - 50)
        
        self.root.geometry(f"+{x}+{y}")
    
    def generate_ai_structure(self, event=None):
        """Generate structure using AI assistant"""
        description = self.ai_input.get().strip()
        if not description:
            messagebox.showwarning("Empty Description", "Please describe your project!")
            return
        
        try:
            result = self.ai_assistant.get_suggestions(description)
            
            # Clear and set new structure
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", result['structure'])
            
            # Force preview update
            self.root.after(50, self.on_text_change)
            
            # Update status with detailed info
            project_type = result['detected_type'].replace('_', ' ').title()
            keywords = ', '.join(result['matched_keywords'][:3]) if result['matched_keywords'] else 'general'
            
            self.status_label.config(
                text=f"🤖 Generated {project_type} structure • Keywords: {keywords} • Confidence: {result['confidence']}",
                fg="#28a745"
            )
            
            # Clear AI input
            self.ai_input.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("AI Error", f"Failed to generate structure: {e}")
    
    def on_ai_input_focus(self, event):
        """Handle placeholder text"""
        if self.ai_input.get() == "e.g., React ecommerce website with payment integration":
            self.ai_input.delete(0, tk.END)
            self.ai_input.config(fg=THEME["fg"])
    
    def on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.root:
            self.adjust_layout()
    
    def adjust_layout(self):
        """Adjust layout based on window size"""
        try:
            window_width = self.root.winfo_width()
            
            if window_width > 1200:
                # Large screen - more space for preview
                self.content_frame.grid_columnconfigure(0, weight=2)
                self.content_frame.grid_columnconfigure(1, weight=1)
            elif window_width > 900:
                # Medium screen - balanced
                self.content_frame.grid_columnconfigure(0, weight=3)
                self.content_frame.grid_columnconfigure(1, weight=2)
            else:
                # Small screen - focus on main area
                self.content_frame.grid_columnconfigure(0, weight=4)
                self.content_frame.grid_columnconfigure(1, weight=1)
        except:
            # Fallback
            self.content_frame.grid_columnconfigure(0, weight=2)
            self.content_frame.grid_columnconfigure(1, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileStructureBuilderApp(root)
    root.mainloop()
