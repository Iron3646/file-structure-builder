import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import platform
import re
from pathlib import Path

class FileStructureBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("File Structure Builder Tool")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        self.style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        self.style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="📁 File Structure Builder", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Path Selection Section
        path_frame = ttk.LabelFrame(main_frame, text="📍 Select Location", padding="15")
        path_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Drive selection (Windows only)
        if platform.system() == "Windows":
            ttk.Label(path_frame, text="Drive:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
            self.drive_var = tk.StringVar()
            self.drive_combo = ttk.Combobox(path_frame, textvariable=self.drive_var, width=5, state="readonly")
            self.drive_combo['values'] = self.get_available_drives()
            self.drive_combo.current(0) if self.drive_combo['values'] else None
            self.drive_combo.grid(row=0, column=1, padx=(0, 10))
        
        # Path selection
        ttk.Label(path_frame, text="Path:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=40)
        self.path_entry.grid(row=0, column=3, padx=(0, 10), sticky=(tk.W, tk.E))
        
        browse_btn = ttk.Button(path_frame, text="📂 Browse", command=self.browse_folder, style='Custom.TButton')
        browse_btn.grid(row=0, column=4)
        
        # Configure column weights
        path_frame.columnconfigure(3, weight=1)
        
        # File Structure Input Section
        structure_frame = ttk.LabelFrame(main_frame, text="📝 File Structure", padding="15")
        structure_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Instructions
        instructions = """Instructions:
• Use indentation (spaces/tabs) to show folder hierarchy
• Add '/' at end for folders: folder_name/
• Files don't need '/' at end: file.txt
• Example:
    project/
        src/
            main.py
            utils.py
        docs/
            readme.md
        tests/"""
        
        ttk.Label(structure_frame, text=instructions, justify=tk.LEFT, font=('Arial', 9)).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Text area for file structure
        self.structure_text = scrolledtext.ScrolledText(structure_frame, height=15, width=70, font=('Consolas', 10))
        self.structure_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Sample button
        sample_btn = ttk.Button(structure_frame, text="📋 Load Sample", command=self.load_sample, style='Custom.TButton')
        sample_btn.grid(row=2, column=0, pady=(10, 0), sticky=tk.W)
        
        # Configure weights
        structure_frame.columnconfigure(0, weight=1)
        structure_frame.rowconfigure(1, weight=1)
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 15))
        
        create_btn = ttk.Button(button_frame, text="🚀 Create Structure", command=self.create_structure, style='Custom.TButton')
        create_btn.configure(width=20)
        create_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="🗑️ Clear", command=self.clear_all, style='Custom.TButton')
        clear_btn.pack(side=tk.LEFT)
        
        # Output Section
        output_frame = ttk.LabelFrame(main_frame, text="📄 Output", padding="15")
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, width=70, font=('Consolas', 9))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
    def get_available_drives(self):
        """Get available drives on Windows"""
        if platform.system() != "Windows":
            return []
        
        drives = []
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(f"{letter}:")
        return drives
    
    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(title="Select Folder Location")
        if folder:
            self.path_var.set(folder)
    
    def load_sample(self):
        """Load a sample file structure"""
        sample = """my_project/
    src/
        main.py
        utils/
            helper.py
            config.py
        models/
            user.py
            product.py
    docs/
        README.md
        API.md
        setup_guide.txt
    tests/
        test_main.py
        test_utils.py
    requirements.txt
    .gitignore
    setup.py"""
        
        self.structure_text.delete(1.0, tk.END)
        self.structure_text.insert(1.0, sample)
    
    def clear_all(self):
        """Clear all fields"""
        self.structure_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.path_var.set("")
    
    def parse_structure(self, text):
        """Parse the text structure into a list of (path, is_folder) tuples"""
        lines = text.strip().split('\n')
        structure = []
        path_stack = []
        
        for line in lines:
            if not line.strip():
                continue
                
            # Calculate indentation level
            stripped_line = line.lstrip()
            indent_level = len(line) - len(stripped_line)
            
            # Determine current depth based on indentation
            current_depth = indent_level // 4  # Assuming 4 spaces per level
            
            # Adjust path stack based on current depth
            while len(path_stack) > current_depth:
                path_stack.pop()
            
            # Check if it's a folder (ends with /)
            is_folder = stripped_line.endswith('/')
            item_name = stripped_line.rstrip('/')
            
            # Build full path
            if path_stack:
                full_path = '/'.join(path_stack + [item_name])
            else:
                full_path = item_name
            
            structure.append((full_path, is_folder))
            
            # Add to path stack if it's a folder
            if is_folder:
                if len(path_stack) == current_depth:
                    path_stack.append(item_name)
                else:
                    path_stack = path_stack[:current_depth] + [item_name]
        
        return structure
    
    def create_structure(self):
        """Create the file structure"""
        # Get base path
        base_path = self.path_var.get().strip()
        if not base_path:
            messagebox.showerror("Error", "Please select a base path!")
            return
        
        # Add drive prefix for Windows
        if platform.system() == "Windows" and hasattr(self, 'drive_var'):
            drive = self.drive_var.get()
            if drive and not base_path.startswith(drive):
                base_path = os.path.join(drive + "\\", base_path.lstrip('\\'))
        
        # Get structure text
        structure_text = self.structure_text.get(1.0, tk.END).strip()
        if not structure_text:
            messagebox.showerror("Error", "Please enter a file structure!")
            return
        
        try:
            # Parse structure
            structure = self.parse_structure(structure_text)
            
            # Clear output
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Creating structure at: {base_path}\n")
            self.output_text.insert(tk.END, "=" * 50 + "\n\n")
            
            created_folders = 0
            created_files = 0
            
            # Create structure
            for item_path, is_folder in structure:
                full_path = os.path.join(base_path, item_path.replace('/', os.sep))
                
                try:
                    if is_folder:
                        os.makedirs(full_path, exist_ok=True)
                        self.output_text.insert(tk.END, f"✅ Created folder: {item_path}\n")
                        created_folders += 1
                    else:
                        # Create parent directories if needed
                        parent_dir = os.path.dirname(full_path)
                        if parent_dir:
                            os.makedirs(parent_dir, exist_ok=True)
                        
                        # Create empty file
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write("")
                        self.output_text.insert(tk.END, f"📄 Created file: {item_path}\n")
                        created_files += 1
                        
                except Exception as e:
                    self.output_text.insert(tk.END, f"❌ Error creating {item_path}: {str(e)}\n")
            
            # Summary
            self.output_text.insert(tk.END, f"\n" + "=" * 50 + "\n")
            self.output_text.insert(tk.END, f"🎉 COMPLETED!\n")
            self.output_text.insert(tk.END, f"📁 Folders created: {created_folders}\n")
            self.output_text.insert(tk.END, f"📄 Files created: {created_files}\n")
            
            # Scroll to bottom
            self.output_text.see(tk.END)
            
            messagebox.showinfo("Success", f"File structure created successfully!\n\nFolders: {created_folders}\nFiles: {created_files}")
            
        except Exception as e:
            error_msg = f"Error creating structure: {str(e)}"
            self.output_text.insert(tk.END, f"❌ {error_msg}\n")
            messagebox.showerror("Error", error_msg)

def main():
    root = tk.Tk()
    app = FileStructureBuilder(root)
    root.mainloop()

if __name__ == "__main__":
    main()