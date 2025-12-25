import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

# ------------------------------
# THEME LOADER
# ------------------------------
def load_theme():
    """Load UI theme from assets/ui_theme.json"""
    theme_path = os.path.join("assets", "ui_theme.json")
    try:
        with open(theme_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "background": "#1e1e1e",
            "foreground": "#ffffff",
            "accent": "#00ffcc",
            "font": "Segoe UI"
        }
    except Exception as e:
        messagebox.showerror("Theme Error", str(e))
        return {
            "background": "#1e1e1e",
            "foreground": "#ffffff",
            "accent": "#00ffcc",
            "font": "Segoe UI"
        }

# ------------------------------
# FOLDER CREATION POPUP
# ------------------------------
def create_folder_popup(base_path):
    """Show popup to create new folder in selected directory"""
    if not base_path:
        messagebox.showwarning("⚠ No Path", "Please select a base folder first.")
        return

    popup = tk.Toplevel()
    popup.title(f"📂 Create Folder in {base_path}")
    popup.configure(bg="#2e2e2e")
    popup.geometry("380x160")
    popup.grab_set()  # Lock focus on popup

    label_info = tk.Label(
        popup,
        text=f"Creating inside: {base_path}",
        bg="#2e2e2e",
        fg="#cccccc",
        font=("Segoe UI", 9, "italic"),
        wraplength=350,
        justify="center"
    )
    label_info.pack(pady=(10, 5))

    label = tk.Label(popup, text="Enter new folder name:", bg="#2e2e2e", fg="#ffffff")
    label.pack()

    entry = tk.Entry(popup, width=35)
    entry.pack(pady=5)

    button_frame = tk.Frame(popup, bg="#2e2e2e")
    button_frame.pack(pady=10)

    def on_ok():
        folder_name = entry.get().strip()
        if folder_name:
            new_path = os.path.join(base_path, folder_name)
            try:
                os.makedirs(new_path, exist_ok=True)
                messagebox.showinfo("✅ Success", f"Folder created at:\n{new_path}")
                popup.destroy()
            except Exception as e:
                messagebox.showerror("❌ Error", str(e))
        else:
            messagebox.showwarning("⚠ Invalid Input", "Folder name cannot be empty.")

    tk.Button(button_frame, text="OK", width=10, command=on_ok).pack(side="left", padx=10)
    tk.Button(button_frame, text="Cancel", width=10, command=popup.destroy).pack(side="right", padx=10)
