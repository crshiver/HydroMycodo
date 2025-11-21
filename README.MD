

🚀 HydroMycodo

Modular Raspberry Pi + ESP32 Automation Platform (Early Alpha)

HydroMycodo is an open-source greenhouse automation framework designed to be modular, flexible, and easy to extend. The project is in early alpha and currently focuses on the core foundations:
	•	Raspberry Pi backend
	•	MQTT communication
	•	ESP32 sensor/actuator nodes
	•	Simple on/off control of pumps (via SSR or relay)
	•	Basic install scripts

This README explains the current state, what works, and where we’re headed.

⸻

✅ Current Capabilities (Early Alpha)

🧠 Raspberry Pi Backend
	•	Python backend (app.py)
	•	Connects to Mosquitto (MQTT)
	•	Receives sensor data from ESP32 nodes
	•	Sends actuator commands back to nodes
	•	Can run as:
	•	Systemd service (hydromycodo.service)
	•	Docker container (Dockerfile + docker-compose)

📡 MQTT Communication

Clear topic structure:
	•	Sensor publish:
hydromycodo/sensors/<node>/<type>
	•	Actuator control:
hydromycodo/actuators/<zone>/<device>/set

🔌 ESP32 Nodes

Included example firmware supports:
	•	WiFi + MQTT
	•	Reading sensors (e.g. temp/humidity)
	•	Controlling pumps via SSR or relay
	•	Simple ON/OFF commands via MQTT

🔧 Installers
	•	install.sh (native Pi install)
	•	install-docker.sh (Docker install)

🗂 Repository Layout

app/               # Python backend modules
app.py             # Backend entry point
esp32_firmware/    # ESP32 example code
Dockerfile         # Backend container build
docker-compose.yml # Backend + MQTT stack
docker/            # Mosquitto config
install.sh         # Native Pi install
install-docker.sh  # Docker install
hydromycodo.service# Systemd service

HydroMycodo is fully operational for basic MQTT-based environmental monitoring and pump control.

⸻

⚠️ Not Yet Implemented (Planned)

The following features are not implemented yet:
	•	Full web dashboard
	•	User accounts / authentication
	•	Historical charts / data visualization
	•	Automation rules engine
	•	PID nutrient/pH dosing
	•	pH/EC calibration tools
	•	Camera integration
	•	AI plant-health analysis
	•	OTA firmware updates
	•	Nutrient recipe editor
	•	Multi-zone management UI
	•	Community data sharing

These features are part of the long-term vision but are not available yet.

⸻

🧭 Roadmap (Help Wanted)

HydroMycodo’s vision is a full modular automation system.
We are actively looking for contributors in the following areas:

🔹 Phase 1 — Core System (In Progress)
	•	Modular backend (FastAPI/Flask)
	•	Stable MQTT handling
	•	Node registry (online/offline)
	•	Local sensor support (DHT22/BME/BME680)
	•	SQLite data logging
	•	Minimal dashboard

🔹 Phase 2 — Automation
	•	Rules engine (threshold-based)
	•	PID dosing control
	•	pH/EC calibration workflows
	•	Alert system (Pushover/Telegram)

🔹 Phase 3 — UI/UX
	•	Full dashboard (dark mode)
	•	Live sensor tiles
	•	Historical graphs
	•	Configuration pages
	•	Recipe builder

🔹 Phase 4 — Advanced Features
	•	Camera snapshots
	•	AI plant-health detection
	•	Long-term analytics
	•	Optional cloud sync

🔹 Phase 5 — OTA & Cloud
	•	Pi and ESP32 OTA updates
	•	Encrypted backups
	•	Multi-site deployments

Contributors for Python, MQTT, FastAPI, frontend, ESP32, and ML/AI are especially welcome.

⸻

👋 Contributing

Ways to help:
	•	Add code to backend or ESP32 firmware
	•	Improve Docker or systemd deployments
	•	Build UI pages or graphs
	•	Add support for new sensors/actuators
	•	Write documentation
	•	Open issues with suggestions or bugs

Any contribution—small or large—is appreciated.

⸻

📥 Installation

Raspberry Pi (native)

curl -sSL https://raw.githubusercontent.com/crshiver/HydroMycodo/main/install.sh | bash

Docker (Pi or Linux)

curl -sSL https://raw.githubusercontent.com/crshiver/HydroMycodo/main/install-docker.sh | bash

After installation, open:

http://<pi-ip>:8000


⸻

📜 License

MIT License — free for personal and commercial use.

⸻

❤️ Acknowledgements

Inspired by systems like Mycodo and Home Assistant, but aiming to remain lightweight, modular, and fully open-source.

⸻

If you’d like, I can also generate:
	•	ROADMAP.md
	•	CONTRIBUTING.md
	•	Architecture diagrams (PNG/SVG)
	•	ESP32 example nodes (sensor_node_v1, pump_node_v1)

Just tell me what you want next.