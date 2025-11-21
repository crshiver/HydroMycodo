#!/bin/bash
set -e
echo "Installing HydroMycodo v1.0 – Complete Edition"
sudo apt update && sudo apt install -y python3-venv python3-pip mosquitto mosquitto-clients nginx git i2c-tools
python3 -m venv ~/hydro-venv
source ~/hydro-venv/bin/activate
pip install Flask Flask-SQLAlchemy paho-mqtt RPi.GPIO gunicorn plotly adafruit-circuitpython-*
mkdir -p ~/HydroMycodo/app/templates
cd ~/HydroMycodo
git clone https://github.com/Crshiver/HydroMycodo.git . --depth 1
sudo cp hydromycodo.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now hydromycodo
echo "Done! Open http://$(hostname -I | awk '{print $1}')"
echo "Login: admin / hydro2025"
