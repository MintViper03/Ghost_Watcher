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
git clone https://github.com/your-username/keylogger.git
cd keylogger
