#!/bin/bash

# No fancy stuff here, just a simple script to deploy the application

# Fail on any error
set -e

echo -n "Granting execute on start and stop scripts... "
sudo chmod +x start.sh
sudo chmod +x stop.sh
echo "Granted."
echo -n "Updating system & installing python3-pip... "
sudo apt update
sudo apt install -y python3-pip
echo "Done."
echo -n "Installing python3-pip requirements... "
sudo pip install -r requirements.txt
echo "Done."
echo -n "Creating service... "
sudo cp ocean.service /etc/systemd/system/
sudo systemctl daemon-reload
echo "Done."
echo -n "Starting service & enable on startup... "
sudo systemctl start ocean
sudo systemctl enable ocean
echo "Done."
echo "Check status with:"
echo "sudo systemctl status ocean"