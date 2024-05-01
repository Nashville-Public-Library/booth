#!/bin/bash
sudo amazon-linux-extras install epel
# this version is reallyyyyy important.
# don't change unless you've a great reason to do so
sudo yum install -y chromium

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
    chmod 777 /var/app/current/chromedriver/chromedriver
    fi
else
    echo "Chromedriver directory not found: $chromedriver_dir"
fi
