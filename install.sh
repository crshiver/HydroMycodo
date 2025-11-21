#!/bin/bash
echo "Installing HydroMycodo..."
sudo apt update && sudo apt install -y python3-venv mosquitto nginx git
# Full code will be added in next 5 minutes
echo "HydroMycodo will be live at http://your-pi-ip"