#!/usr/bin/env bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary folders if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file for testing
echo "Hello, world!" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link and update ownership
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"

sudo sed -i '/^\s*location \/hbnb_static/i \\\talias \/data\/web_static\/current\/;' "$config_file"

# Restart Nginx
sudo service nginx restart
