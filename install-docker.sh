#!/usr/bin/env bash
set -e

echo "Installing HydroMycodo (Docker edition)..."

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found, installing..."
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker "$USER"
  echo "Logout and login to use docker without sudo."
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin missing. Cannot continue."
  exit 1
fi

sudo mkdir -p /opt
sudo chown "$USER":"$USER" /opt
cd /opt

if [ -d HydroMycodo ]; then
  cd HydroMycodo && git pull
else
  git clone https://github.com/crshiver/HydroMycodo.git
  cd HydroMycodo
fi

docker compose up -d

IP=$(hostname -I | awk '{print $1}')
echo "HydroMycodo running at: http://$IP:8000"
