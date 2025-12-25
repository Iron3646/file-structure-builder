import os

# 🔹 Root project folder (isske andar structure banega)
ROOT = os.path.join(os.getcwd(), "MySoftware")

# 🔹 Folder → Files mapping
structure = {
    "assets": ["README.md"],
    "build": [],
    "config": ["default.json", "user.json"],
    "dist": [],
    "docs": ["README.md", "CHANGELOG.md"],
    "logs": ["app.log"],
    "scripts": ["build_installer.bat", "clean_build.sh"],
    "src": ["main.py"],
    "tests": ["test_core.py", "test_ui.py"],
}

# 🔹 Root-level files
root_files = ["LICENSE", "requirements.txt", "setup.py", "README.md"]

# ✅ Create root folder
os.makedirs(ROOT, exist_ok=True)

# ✅ Create folders + files
for folder, files in structure.items():
    folder_path = os.path.join(ROOT, folder)
    os.makedirs(folder_path, exist_ok=True)

    for file in files:
        file_path = os.path.join(folder_path, file)
        if not os.path.exists(file_path):
            open(file_path, "w", encoding="utf-8").close()  # empty file

# ✅ Create root-level files
for file in root_files:
    file_path = os.path.join(ROOT, file)
    if not os.path.exists(file_path):
        open(file_path, "w", encoding="utf-8").close()  # empty file

print(f"✅ File structure created at: {ROOT}")
