@echo off
:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed.
) else (
    echo Python is not installed. Downloading and installing Python...
    :: Download Python installer
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe' -OutFile 'python_installer.exe'"
    :: Install Python silently
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo Python installed successfully.
)

:: Install Python dependencies
pip install -r requirements.txt

:: Run the Python script
python ghost_watcher.py