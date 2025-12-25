import os
from tkinter import messagebox
from templates import FILE_TEMPLATES

def create_structure_with_templates(base_path, structure_text):
    """
    Parse file structure text and create files/folders with templates.
    """
    lines = structure_text.strip().splitlines()
    path_stack = []

    for line in lines:
        if not line.strip():
            continue

        # detect ├── or └──
        symbol_pos = line.find("├──")
        if symbol_pos == -1:
            symbol_pos = line.find("└──")
        if symbol_pos == -1:
            continue

        depth = symbol_pos // 4
        name = line[symbol_pos + 3:].strip()

        # adjust stack
        path_stack = path_stack[:depth]
        path_stack.append(name)

        full_path = os.path.join(base_path, *path_stack)

        if "." in name and not name.startswith("."):
            # it's a file
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            ext = os.path.splitext(name)[1].lower()
            template = FILE_TEMPLATES.get(ext, "")

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(template)
        else:
            # it's a folder
            os.makedirs(full_path, exist_ok=True)

    messagebox.showinfo("✅ Success", "📂 File Structure created with functioning files!")
