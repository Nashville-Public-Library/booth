#!/bin/bash

# URL of the Chrome zip file
CHROME_URL="https://storage.googleapis.com/chrome-for-testing-public/125.0.6375.0/linux64/chrome-linux64.zip"

# Directory to download Chrome zip file
DOWNLOAD_DIR="/tmp"

# Directory to install Chrome
INSTALL_DIR="/opt/google/chrome"

# Download Chrome zip file
echo "Downloading Chrome..."
wget "$CHROME_URL" -P "$DOWNLOAD_DIR"

# Unzip Chrome
echo "Installing Chrome..."
sudo mkdir -p "$INSTALL_DIR"
sudo unzip -o "$DOWNLOAD_DIR/chromedriver-linux64.zip" -d "$INSTALL_DIR"

# Create a symbolic link to Chrome binary (optional)
sudo ln -sf "$INSTALL_DIR/chrome" /usr/local/bin/chrome

echo "Chrome installation complete."


# Directory containing Chromedriver
chromedriver_dir="/var/app/current/chromedriver"

# Check if the directory exists
if [ -d "$chromedriver_dir" ]; then
    # Add directory to PATH if it's not already there
    if [[ ":$PATH:" != *":$chromedriver_dir:"* ]]; then
        export PATH="$chromedriver_dir:$PATH"
        echo "Chromedriver directory added to PATH."
    else
        echo "Chromedriver directory is already in PATH."
    sudo chmod 777 /var/app/current/chromedriver/chromedriver
    fi
else
    echo "Chromedriver directory not found: $chromedriver_dir"
fi

sudo chmod 777 /var/app/current/chromedriver/chromedriver
