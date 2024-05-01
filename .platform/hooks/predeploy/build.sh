#!/bin/bash

# Install dependencies required for Chrome
sudo yum install -y \
    libX11 \
    GConf2 \
    alsa-lib \
    atk \
    gtk3 \
    ipa-gothic-fonts \
    xorg-x11-fonts-100dpi \
    xorg-x11-fonts-75dpi \
    xorg-x11-utils \
    xorg-x11-fonts-cyrillic \
    xorg-x11-fonts-Type1 \
    xorg-x11-fonts-misc

# Download and install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum localinstall -y google-chrome-stable_current_x86_64.rpm



# Directory containing Chromedriver
chromedriver_dir="/var/app/current/chromedriverdir"

# Check if the directory exists
if [ -d "$chromedriver_dir" ]; then
    # Add directory to PATH if it's not already there
    if [[ ":$PATH:" != *":$chromedriver_dir:"* ]]; then
        export PATH="$chromedriver_dir:$PATH"
        echo "Chromedriver directory added to PATH."
    else
        echo "Chromedriver directory is already in PATH."
    sudo chmod 777 /var/app/current/chromedriverdir/chromedriver
    fi
else
    echo "Chromedriver directory not found: $chromedriver_dir"
fi

sudo chmod 777 /var/app/current/chromedriverdir/chromedriver
