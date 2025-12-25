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
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        min_width, min_height = 900, 650
        
        window_width = max(min_width, min(window_width, int(screen_width * 0.95)))
        window_height = max(min_height, min(window_height, int(screen_height * 0.95)))
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(min_width, min_height)
        self.root.configure(bg=THEME["bg"])
        
        self.output_dir = None
        self.ai_assistant = ProjectStructureAI()
        
        self.center_window()
        
        main_frame = tk.Frame(root, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        header_frame = tk.Frame(main_frame, bg=THEME["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="🚀 File Structure Builder v2.5",
                 font=(THEME["font"], 18, "bold"), fg=THEME["accent"], bg=THEME["bg"]).pack()
        tk.Label(header_frame, text="AI-Powered Project Structure Generator",
                 font=(THEME["font"], 10), fg="#6c757d", bg=THEME["bg"]).pack(pady=(2, 0))
        
        target_frame = tk.Frame(main_frame, bg="#e8f4fd", relief="solid", bd=1)
        target_frame.pack(fill=tk.X, pady=(0, 20))
        
        target_inner = tk.Frame(target_frame, bg="#e8f4fd")
        target_inner.pack(fill=tk.X, padx=15, pady=12)
        
        tk.Label(target_inner, text="📁 Target Directory:", font=(THEME["font"], 9, "bold"),
                 fg="#1565c0", bg="#e8f4fd").pack(side=tk.LEFT)
        
        self.target_label = tk.Label(target_inner, text="No folder selected",
                                      font=(THEME["font"], 9), fg="#1976d2", bg="#e8f4fd", anchor="w")
        self.target_label.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        content_frame = tk.Frame(main_frame, bg=THEME["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        left_frame = tk.Frame(content_frame, bg=THEME["bg"])
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left_frame.grid_rowconfigure(2, weight=1)
        
        ai_frame = tk.Frame(left_frame, bg="#f0f8f0", relief="solid", bd=1)
        ai_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        ai_header = tk.Frame(ai_frame, bg="#e8f5e8")
        ai_header.pack(fill=tk.X, padx=12, pady=8)
        
        tk.Label(ai_header, text="🤖 AI Assistant", font=(THEME["font"], 11, "bold"),
                 fg="#2e7d32", bg="#e8f5e8").pack(side=tk.LEFT)
        
        ai_input_frame = tk.Frame(ai_frame, bg="#f0f8f0")
        ai_input_frame.pack(fill=tk.X, padx=12, pady=(0, 12))
        
        self.ai_input = tk.Entry(ai_input_frame, font=(THEME["font"], 10), bg="white",
                                 fg=THEME["fg"], relief="solid", bd=1)
        self.ai_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=4)
        self.ai_input.bind('<Return>', self.generate_ai_structure)
        
        tk.Button(ai_input_frame, text="🤖 Generate", command=self.generate_ai_structure,
                  bg="#4caf50", fg="white", relief="flat", font=(THEME["font"], 9, "bold"),
                  padx=20, pady=8, cursor="hand2").pack(side=tk.RIGHT)
        
        tk.Label(left_frame, text="📝 Manual Structure Input:",
                 font=(THEME["font"], 10, "bold"), fg=THEME["fg"], bg=THEME["bg"]).grid(row=1, column=0, sticky="w", pady=(0, 8))
        
        text_frame = tk.Frame(left_frame, bg=THEME["border"], relief="solid", bd=1)
        text_frame.grid(row=2, column=0, sticky="nsew")
        
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, relief="flat", bd=0,
                                                    bg=THEME["text_bg"], fg=THEME["fg"],
                                                    font=("Consolas", 10), padx=12, pady=12)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        self.text_area.bind('<KeyRelease>', self.on_text_change)
        self.text_area.bind('<Control-v>', lambda e: self.root.after(100, self.on_text_change))
        
        right_frame = tk.Frame(content_frame, bg=THEME["bg"])
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(2, weight=1)
        
        tk.Label(right_frame, text="📊 Live Preview:", font=(THEME["font"], 10, "bold"),
                 fg=THEME["fg"], bg=THEME["bg"]).grid(row=0, column=0, sticky="w", pady=(0, 8))
        
        stats_frame = tk.Frame(right_frame, bg="#f1f8ff", relief="solid", bd=1)
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        
        folder_frame = tk.Frame(stats_frame, bg="#f1f8ff")
        folder_frame.grid(row=0, column=0, padx=8, pady=8)
        
        self.folder_count = tk.Label(folder_frame, text="📁 0", font=(THEME["font"], 14, "bold"),
                                      fg="#1976d2", bg="#f1f8ff")
        self.folder_count.pack()
        tk.Label(folder_frame, text="Folders", font=(THEME["font"], 8), fg="#666", bg="#f1f8ff").pack()
        
        file_frame = tk.Frame(stats_frame, bg="#f1f8ff")
        file_frame.grid(row=0, column=1, padx=8, pady=8)
        
        self.file_count = tk.Label(file_frame, text="📄 0", font=(THEME["font"], 14, "bold"),
                                    fg="#1976d2", bg="#f1f8ff")
        self.file_count.pack()
        tk.Label(file_frame, text="Files", font=(THEME["font"], 8), fg="#666", bg="#f1f8ff").pack()
        
        preview_frame = tk.Frame(right_frame, bg=THEME["border"], relief="solid", bd=1)
        preview_frame.grid(row=2, column=0, sticky="nsew")
        
        self.preview_area = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, relief="flat", bd=0,
                                                       bg="#fafbfc", fg=THEME["fg"], state="disabled",
                                                       font=("Consolas", 9), padx=12, pady=12)
        self.preview_area.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        btn_frame = tk.Frame(main_frame, bg=THEME["bg"])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.folder_btn = tk.Button(btn_frame, text="📁 Select Folder", command=self.select_folder,
                                     bg="#6c757d", fg="white", relief="flat",
                                     font=(THEME["font"], 10), padx=25, pady=10, cursor="hand2")
        self.folder_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        self.build_btn = tk.Button(btn_frame, text="🚀 Build Structure", command=self.build,
                                    bg=THEME["accent"], fg="white", relief="flat",
                                    font=(THEME["font"], 11, "bold"), padx=35, pady=10, cursor="hand2")
        self.build_btn.pack(side=tk.RIGHT)
        
        status_frame = tk.Frame(main_frame, bg="#f8f9fa", relief="solid", bd=1)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.status_label = tk.Label(status_frame, text="💡 Ready - describe your project or paste structure",
                                      font=(THEME["font"], 9), fg="#495057", bg="#f8f9fa", padx=15, pady=10)
        self.status_label.pack(fill=tk.X)
        
        self.root.after(100, self.on_text_change)

    def on_text_change(self, event=None):
        try:
            text = self.text_area.get("1.0", tk.END).strip()
            
            self.preview_area.config(state="normal")
            self.preview_area.delete("1.0", tk.END)
            
            if text:
                cleaned = clean_structure_text(text)
                folders, files = count_structure_items(cleaned)
                
                self.folder_count.config(text=f"📁 {folders}", fg="#1976d2")
                self.file_count.config(text=f"📄 {files}", fg="#1976d2")
                
                preview = f"📊 Preview: {folders} folders, {files} files\n" + "─" * 40 + "\n\n"
                
                for line in cleaned.splitlines()[:20]:
                    if line.strip():
                        clean_line = line.replace("├──", "").replace("└──", "").replace("│", "").strip()
                        if clean_line.endswith('/'):
                            preview += f"📁 {line}\n"
                        elif '.' in clean_line:
                            preview += f"📄 {line}\n"
                        else:
                            preview += f"{line}\n"
                
                if len(cleaned.splitlines()) > 20:
                    preview += f"\n... {len(cleaned.splitlines()) - 20} more"
                
                self.preview_area.insert("1.0", preview)
                self.status_label.config(text=f"✅ Ready: {folders} folders, {files} files", fg="#28a745")
            else:
                self.folder_count.config(text="📁 0", fg="#6c757d")
                self.file_count.config(text="📄 0", fg="#6c757d")
                self.preview_area.insert("1.0", "💡 Live Preview\n\nPaste structure or use AI\n\nExample:\nsrc/\n├── components/\n└── pages/\nREADME.md")
                self.status_label.config(text="💡 Ready - add your structure", fg="#6c757d")
            
            self.preview_area.config(state="disabled")
        except Exception as e:
            print(f"Error: {e}")

    def get_file_emoji(self, filename):
        ext = filename.split('.')[-1].lower() if '.' in filename else ''
        emoji_map = {'py': '🐍', 'js': '🟨', 'html': '🌐', 'css': '🎨', 'json': '📋', 'md': '📝'}
        return emoji_map.get(ext, '📄')

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir = folder
            folder_name = os.path.basename(folder) or folder
            self.folder_btn.config(text=f"📁 {folder_name}", bg="#28a745")
            self.target_label.config(text=folder)
            self.status_label.config(text=f"✅ Ready: {folder_name}", fg="#28a745")

    def build(self):
        if not self.output_dir:
            messagebox.showwarning("No Folder", "Please select a folder first!")
            return
        
        structure_text = self.text_area.get("1.0", tk.END).strip()
        if not structure_text:
            messagebox.showwarning("Empty", "Please paste your file structure!")
            return
        
        threading.Thread(target=self.build_in_thread, daemon=True).start()

    def build_in_thread(self):
        structure_text = self.text_area.get("1.0", tk.END).strip()
        try:
            self.root.after(0, lambda: self.status_label.config(text="🔄 Building...", fg="#ffc107"))
            created_items = build_structure(self.output_dir, structure_text)
            self.root.after(0, lambda: self.status_label.config(text=f"✅ Created {len(created_items)} items!", fg="#28a745"))
            if winsound:
                winsound.MessageBeep(winsound.MB_OK)
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"❌ Error: {e}", fg="#dc3545"))

    def generate_ai_structure(self, event=None):
        description = self.ai_input.get().strip()
        if not description:
            messagebox.showwarning("Empty", "Please describe your project!")
            return
        
        try:
            result = self.ai_assistant.get_suggestions(description)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", result['structure'])
            self.ai_input.delete(0, tk.END)
            self.root.after(100, self.on_text_change)
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = max(50, (self.root.winfo_screenheight() - height) // 2 - 50)
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileStructureBuilderApp(root)
    root.mainloop()
