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
wget https://storage.googleapis.com/chrome-for-testing-public/114.0.5696.0/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
echo "make dir"
sudo mkdir -p /opt/google-chrome
sudo mv -f chrome-linux64 /opt/google-chrome/chrome-linux64
sudo ln -s -f /opt/google-chrome/chrome-linux64/chrome /usr/local/bin/chrome