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


sudo chmod 777 /var/app/current/chromedriver
sudo chmod +x /var/app/current/chromedriver