#!/bin/bash
set -e
echo "🌱 Installing HydroMycodo v0.2 (MQTT + ESP32 Edition)"

# Basics
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-venv python3-pip mosquitto mosquitto-clients nginx git libcamera-apps

# Project setup
python3 -m venv ~/hydro-venv
source ~/hydro-venv/bin/activate
pip install Flask Flask-SQLAlchemy paho-mqtt RPi.GPIO gunicorn adafruit-circuitpython-dht plotly

# Systemd service
sudo tee /etc/systemd/system/hydromycodo.service > /dev/null <<EOF
[Unit]
Description=HydroMycodo
After=network.target

[Service]
WorkingDirectory=/home/pi/HydroMycodo
ExecStart=/home/pi/hydro-venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now hydromycodo
echo "✅ Done! Open http://\$(hostname -I | awk '{print \$1}') – login: admin / hydro2025"