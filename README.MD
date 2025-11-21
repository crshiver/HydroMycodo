# HydroMycodo v2.1 – An open-source grow controller that learns from real grows

A simple project started by one grower (Crshiver) and an AI (Grok) because commercial systems were too expensive and too closed.

It just works and already does more than most $1000+ controllers.

### What you get today (real hardware tested)

- One-line install on any Raspberry Pi
- Unlimited ESP32 wireless sensors (no hubs, no limits)
- Auto-detected local sensors (DHT22, SHT4x, BME680, SCD41, CCS811, Atlas pH/EC)
- Secure login + dark-mode dashboard + historical graphs
- PID control with real dosing pumps
- Live camera + AI plant-health detection (disease & deficiency)
- Auto pH/EC calibration
- Pushover phone alerts
- Web-based nutrient recipe editor (DWC, NFT, aeroponics, soil, cannabis, herbs)
- One-click OTA updates
- Full data logging
- 100 % local by default – runs forever offline
- GPL-3.0 – you own it completely

### Optional community data sharing (you control it)

HydroMycodo can anonymously send daily summaries (strain, week, pH/EC targets, yield, AI health reports) to a public open-grow database.
No personal info, no IP addresses, no photos – just pure grow data.

Goal: build the largest open-source dataset of real grows ever created so everyone gets better recipes, faster.

Toggle in Settings → “Contribute to open-grow science” (off by default).

### Compared to commercial controllers

| Feature                       | HydroMycodo v2.1 | Typical $800-$2000 system |
|-------------------------------|------------------|---------------------------|
| Unlimited wireless sensors    | Yes              | No (4-16 max)             |
| AI plant disease detection    | Yes              | No                        |
| One-click OTA updates         | Yes              | Rare                      |
| Web recipe editor             | Yes              | No                        |
| Community-driven strain data  | Yes (opt-in)     | Never                     |
| Full source + GPL-3.0         | Yes              | No                        |
| Price                         | Free             | $800-$2000+               |

### Install (one command)

```bash
curl -sSL https://raw.githubusercontent.com/crshiver/HydroMycodo/main/install.sh | bash
