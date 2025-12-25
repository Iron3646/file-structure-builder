@echo off
echo 🚀 Building File Structure Builder v3.0...
echo.

echo 📦 Installing PyInstaller...
pip install pyinstaller

echo.
echo 🔨 Building executable...
pyinstaller --onefile --windowed --name "FileStructureBuilder" --icon=icon.ico optimized_main.py

echo.
echo 📁 Creating distribution folder...
if not exist "dist\FileStructureBuilder" mkdir "dist\FileStructureBuilder"

echo.
echo 📋 Copying files...
copy "dist\FileStructureBuilder.exe" "dist\FileStructureBuilder\"
copy "README.md" "dist\FileStructureBuilder\"
copy "LICENSE" "dist\FileStructureBuilder\" 2>nul

echo.
echo 📦 Creating installer with NSIS (if available)...
if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
    echo ✅ Installer created!
) else (
    echo ⚠️  NSIS not found. Installer not created.
    echo    Download NSIS from: https://nsis.sourceforge.io/
)

echo.
echo ✅ Build complete!
echo 📁 Files location: dist\FileStructureBuilder\
echo 🎯 Executable: FileStructureBuilder.exe
echo.
pause