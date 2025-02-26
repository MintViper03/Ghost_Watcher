#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
	echo "Python is not installed. Installing Python and dependencies..."
	if[["$OSTYPE" == "linux-gnu"* ]]; then
		sudo apt update && sudo apt install python3 python3-pip -y
	elif [["$OSTYPE" == "darwin"* ]]; then
		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
		brew install python3
	fi
	pip3 install pynput pyperclip requests pyautogui cryptography winshell
fi

# Run the Python script
python3 ghost_watcher.py