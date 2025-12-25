import os
import subprocess
import sys

def build_exe():
    print("Building File Structure Builder v3.0...")
    
    # Install PyInstaller
    print("Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build executable
    print("Building executable...")
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "FileStructureBuilder",
        "optimized_main.py"
    ]
    
    subprocess.run(cmd)
    
    # Create distribution folder
    print("Creating distribution...")
    os.makedirs("dist/FileStructureBuilder", exist_ok=True)
    
    # Copy files
    import shutil
    shutil.copy("dist/FileStructureBuilder.exe", "dist/FileStructureBuilder/")
    shutil.copy("README.md", "dist/FileStructureBuilder/")
    if os.path.exists("LICENSE"):
        shutil.copy("LICENSE", "dist/FileStructureBuilder/")
    
    print("Build complete!")
    print("Files location: dist/FileStructureBuilder/")
    print("Executable: FileStructureBuilder.exe")

if __name__ == "__main__":
    build_exe()