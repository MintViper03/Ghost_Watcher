
#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Installing Python..."
    # Install Python
    sudo apt-get update
    sudo apt-get install -y python3
    echo "Python installed successfully."
else
    echo "Python is already installed."
fi

# Install Python dependencies
pip3 install -r requirements.txt

# Set the environment variable for PyAutoGUI to use scrot
export PYAUTOGUI_SCREENSHOT=scrot

# Run the Python script
python3 ghost_watcher.py