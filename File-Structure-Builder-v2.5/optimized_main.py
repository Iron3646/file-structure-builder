import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import threading
from datetime import datetime
try:
    import winsound
except ImportError:
    winsound = None
from builder import build_structure, count_structure_items, clean_structure_text
from enhanced_ai import EnhancedAI

THEME = {
    "bg": "#f8f9fa",
    "fg": "#212529", 
    "accent": "#007bff",
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545",
    "text_bg": "#ffffff",
    "border": "#dee2e6",
    "font": "Segoe UI"
}

class OptimizedFileBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 File Structure Builder v3.0 - Enhanced AI")
        
        # Dynamic sizing
        screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
        w, h = int(screen_w * 0.85), int(screen_h * 0.85)
        self.root.geometry(f"{w}x{h}")
        self.root.minsize(1000, 700)
        self.root.configure(bg=THEME["bg"])
        
        self.output_dir = None
        self.ai = EnhancedAI()
        self.is_building = False
        
        self.setup_ui()
        self.center_window()
        
        # Auto-update preview
        self.root.after(200, self.update_preview)

    def setup_ui(self):
        # Main container
        main = tk.Frame(self.root, bg=THEME["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(main, bg=THEME["bg"])
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(header, text="🚀 File Structure Builder v3.0", 
                 font=(THEME["font"], 20, "bold"), fg=THEME["accent"], bg=THEME["bg"]).pack()
        tk.Label(header, text="Enhanced AI-Powered Project Generator", 
                 font=(THEME["font"], 10), fg="#6c757d", bg=THEME["bg"]).pack()
        
        # Target folder
        target_frame = tk.Frame(main, bg="#e8f4fd", relief="solid", bd=1)
        target_frame.pack(fill=tk.X, pady=(0, 15))
        
        target_inner = tk.Frame(target_frame, bg="#e8f4fd")
        target_inner.pack(fill=tk.X, padx=12, pady=10)
        
        tk.Label(target_inner, text="📁 Target:", font=(THEME["font"], 9, "bold"),
                 fg="#1565c0", bg="#e8f4fd").pack(side=tk.LEFT)
        
        self.target_label = tk.Label(target_inner, text="No folder selected",
                                      font=(THEME["font"], 9), fg="#1976d2", bg="#e8f4fd")
        self.target_label.pack(side=tk.LEFT, padx=(8, 0), fill=tk.X, expand=True)
        
        # Main content with notebook
        notebook = ttk.Notebook(main)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # AI Chat Tab
        chat_frame = tk.Frame(notebook, bg=THEME["bg"])
        notebook.add(chat_frame, text="🤖 AI Assistant")
        self.setup_chat_tab(chat_frame)
        
        # Manual Tab
        manual_frame = tk.Frame(notebook, bg=THEME["bg"])
        notebook.add(manual_frame, text="📝 Manual Input")
        self.setup_manual_tab(manual_frame)
        
        # Preview Tab
        preview_frame = tk.Frame(notebook, bg=THEME["bg"])
        notebook.add(preview_frame, text="📊 Live Preview")
        self.setup_preview_tab(preview_frame)
        
        # Control buttons
        self.setup_controls(main)
        
        # Status bar
        self.setup_status(main)

    def setup_chat_tab(self, parent):
        # Chat history
        chat_container = tk.Frame(parent, bg=THEME["bg"])
        chat_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(chat_container, text="💬 AI Chat Assistant", 
                 font=(THEME["font"], 12, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(anchor="w", pady=(0, 8))
        
        # Chat display
        chat_frame = tk.Frame(chat_container, bg=THEME["border"], relief="solid", bd=1)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, relief="flat", bd=0,
            bg="#f8f9fa", fg=THEME["fg"], state="disabled",
            font=(THEME["font"], 9), padx=12, pady=12
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Configure chat tags
        self.chat_display.tag_configure("user", foreground="#007bff", font=(THEME["font"], 9, "bold"))
        self.chat_display.tag_configure("ai", foreground="#28a745", font=(THEME["font"], 9, "bold"))
        self.chat_display.tag_configure("timestamp", foreground="#6c757d", font=(THEME["font"], 8))
        
        # Input area
        input_frame = tk.Frame(chat_container, bg=THEME["bg"])
        input_frame.pack(fill=tk.X)
        
        self.chat_input = tk.Entry(input_frame, font=(THEME["font"], 10), 
                                   relief="solid", bd=1, bg="white")
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=6)
        self.chat_input.bind('<Return>', self.send_chat_message)
        self.chat_input.bind('<FocusIn>', self.clear_placeholder)
        
        # Placeholder
        self.chat_input.insert(0, "Describe your project (e.g., 'React ecommerce with payment')")
        self.chat_input.config(fg="#999")
        
        tk.Button(input_frame, text="💬 Send", command=self.send_chat_message,
                  bg=THEME["success"], fg="white", relief="flat",
                  font=(THEME["font"], 9, "bold"), padx=20, pady=6).pack(side=tk.RIGHT)
        
        # Quick actions
        quick_frame = tk.Frame(chat_container, bg=THEME["bg"])
        quick_frame.pack(fill=tk.X, pady=(8, 0))
        
        tk.Button(quick_frame, text="🗑️ Clear Chat", command=self.clear_chat,
                  bg="#6c757d", fg="white", relief="flat", font=(THEME["font"], 8), padx=12, pady=4).pack(side=tk.LEFT)
        
        # Add welcome message
        self.add_chat_message("ai", "👋 Hi! I'm your AI assistant. Describe your project and I'll help you create the perfect structure!", "")

    def setup_manual_tab(self, parent):
        container = tk.Frame(parent, bg=THEME["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(container, text="📝 Manual Structure Input", 
                 font=(THEME["font"], 12, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(anchor="w", pady=(0, 8))
        
        text_frame = tk.Frame(container, bg=THEME["border"], relief="solid", bd=1)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame, wrap=tk.WORD, relief="flat", bd=0,
            bg=THEME["text_bg"], fg=THEME["fg"],
            font=("Consolas", 10), padx=12, pady=12
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        self.text_area.bind('<KeyRelease>', lambda e: self.root.after(100, self.update_preview))
        self.text_area.bind('<Control-v>', lambda e: self.root.after(200, self.update_preview))

    def setup_preview_tab(self, parent):
        container = tk.Frame(parent, bg=THEME["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Stats
        stats_frame = tk.Frame(container, bg="#f1f8ff", relief="solid", bd=1)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        stats_inner = tk.Frame(stats_frame, bg="#f1f8ff")
        stats_inner.pack(fill=tk.X, padx=15, pady=12)
        
        self.folder_count = tk.Label(stats_inner, text="📁 0 Folders", 
                                      font=(THEME["font"], 11, "bold"), fg="#1976d2", bg="#f1f8ff")
        self.folder_count.pack(side=tk.LEFT)
        
        self.file_count = tk.Label(stats_inner, text="📄 0 Files", 
                                    font=(THEME["font"], 11, "bold"), fg="#1976d2", bg="#f1f8ff")
        self.file_count.pack(side=tk.RIGHT)
        
        # Preview
        tk.Label(container, text="📊 Live Preview", 
                 font=(THEME["font"], 12, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(anchor="w", pady=(0, 8))
        
        preview_frame = tk.Frame(container, bg=THEME["border"], relief="solid", bd=1)
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        self.preview_area = scrolledtext.ScrolledText(
            preview_frame, wrap=tk.WORD, relief="flat", bd=0,
            bg="#fafbfc", fg=THEME["fg"], state="disabled",
            font=("Consolas", 9), padx=12, pady=12
        )
        self.preview_area.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

    def setup_controls(self, parent):
        btn_frame = tk.Frame(parent, bg=THEME["bg"])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.folder_btn = tk.Button(btn_frame, text="📁 Select Folder", command=self.select_folder,
                                     bg="#6c757d", fg="white", relief="flat",
                                     font=(THEME["font"], 10), padx=25, pady=10)
        self.folder_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        self.build_btn = tk.Button(btn_frame, text="🚀 Build Structure", command=self.build_structure,
                                    bg=THEME["accent"], fg="white", relief="flat",
                                    font=(THEME["font"], 11, "bold"), padx=35, pady=10)
        self.build_btn.pack(side=tk.RIGHT)

    def setup_status(self, parent):
        status_frame = tk.Frame(parent, bg="#f8f9fa", relief="solid", bd=1)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.status_label = tk.Label(status_frame, text="💡 Ready - Select folder and describe your project",
                                      font=(THEME["font"], 9), fg="#495057", bg="#f8f9fa", padx=15, pady=8)
        self.status_label.pack(fill=tk.X)

    def clear_placeholder(self, event):
        if self.chat_input.get() == "Describe your project (e.g., 'React ecommerce with payment')":
            self.chat_input.delete(0, tk.END)
            self.chat_input.config(fg=THEME["fg"])

    def add_chat_message(self, sender, message, timestamp):
        self.chat_display.config(state="normal")
        
        if sender == "user":
            self.chat_display.insert(tk.END, f"👤 You", "user")
        else:
            self.chat_display.insert(tk.END, f"🤖 AI", "ai")
        
        if timestamp:
            self.chat_display.insert(tk.END, f" ({timestamp})", "timestamp")
        
        self.chat_display.insert(tk.END, f"\n{message}\n\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def send_chat_message(self, event=None):
        message = self.chat_input.get().strip()
        if not message or message == "Describe your project (e.g., 'React ecommerce with payment')":
            return
        
        # Add user message
        timestamp = datetime.now().strftime("%H:%M")
        self.add_chat_message("user", message, timestamp)
        
        # Get AI response
        try:
            response_data = self.ai.chat_response(message)
            self.add_chat_message("ai", response_data['response'], timestamp)
            
            # Update text area with generated structure
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", response_data['structure'])
            
            # Update preview
            self.root.after(100, self.update_preview)
            
        except Exception as e:
            self.add_chat_message("ai", f"❌ Error: {e}", timestamp)
        
        # Clear input
        self.chat_input.delete(0, tk.END)

    def clear_chat(self):
        self.ai.clear_chat()
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state="disabled")
        self.add_chat_message("ai", "Chat cleared! How can I help you?", "")

    def update_preview(self):
        try:
            text = self.text_area.get("1.0", tk.END).strip()
            
            self.preview_area.config(state="normal")
            self.preview_area.delete("1.0", tk.END)
            
            if text:
                cleaned = clean_structure_text(text)
                folders, files = count_structure_items(cleaned)
                
                self.folder_count.config(text=f"📁 {folders} Folders")
                self.file_count.config(text=f"📄 {files} Files")
                
                preview = f"📊 Structure Overview\n{'─' * 40}\n\n"
                
                for line in cleaned.splitlines()[:25]:
                    if line.strip():
                        clean_line = line.replace("├──", "").replace("└──", "").replace("│", "").strip()
                        if clean_line.endswith('/'):
                            preview += f"📁 {line}\n"
                        elif '.' in clean_line:
                            preview += f"📄 {line}\n"
                        else:
                            preview += f"{line}\n"
                
                if len(cleaned.splitlines()) > 25:
                    preview += f"\n... and {len(cleaned.splitlines()) - 25} more items"
                
                self.preview_area.insert("1.0", preview)
                self.status_label.config(text=f"✅ Structure ready: {folders} folders, {files} files", fg=THEME["success"])
            else:
                self.folder_count.config(text="📁 0 Folders")
                self.file_count.config(text="📄 0 Files")
                self.preview_area.insert("1.0", "💡 Preview will appear here\n\nUse AI Assistant or Manual Input to create your structure")
                self.status_label.config(text="💡 Ready - describe your project", fg="#6c757d")
            
            self.preview_area.config(state="disabled")
        except Exception as e:
            print(f"Preview error: {e}")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir = folder
            folder_name = os.path.basename(folder) or folder
            self.folder_btn.config(text=f"📁 {folder_name}", bg=THEME["success"])
            self.target_label.config(text=folder)
            self.status_label.config(text=f"✅ Target set: {folder_name}", fg=THEME["success"])

    def build_structure(self):
        if self.is_building:
            return
            
        if not self.output_dir:
            messagebox.showwarning("No Folder", "Please select a target folder first!")
            return
        
        structure_text = self.text_area.get("1.0", tk.END).strip()
        if not structure_text:
            messagebox.showwarning("Empty Structure", "Please create a structure first!")
            return
        
        self.is_building = True
        self.build_btn.config(text="🔄 Building...", bg=THEME["warning"])
        threading.Thread(target=self.build_thread, daemon=True).start()

    def build_thread(self):
        try:
            structure_text = self.text_area.get("1.0", tk.END).strip()
            self.root.after(0, lambda: self.status_label.config(text="🔄 Creating structure...", fg=THEME["warning"]))
            
            created_items = build_structure(self.output_dir, structure_text)
            
            self.root.after(0, lambda: self.status_label.config(
                text=f"✅ Successfully created {len(created_items)} items!", fg=THEME["success"]))
            self.root.after(0, lambda: self.build_btn.config(text="🚀 Build Structure", bg=THEME["accent"]))
            
            if winsound:
                winsound.MessageBeep(winsound.MB_OK)
                
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"❌ Error: {e}", fg=THEME["danger"]))
            self.root.after(0, lambda: self.build_btn.config(text="🚀 Build Structure", bg=THEME["accent"]))
        finally:
            self.is_building = False

    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_reqwidth(), self.root.winfo_reqheight()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = max(50, (self.root.winfo_screenheight() - h) // 2 - 50)
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizedFileBuilder(root)
    root.mainloop()