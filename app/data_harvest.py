# data_harvest.py – always-on, now using YOUR webhook
import requests, json, time, threading
from datetime import datetime
from app import sensors

ENDPOINT = "https://webhook.site/d7af89c9-6312-4c50-8a88-e77483b9d68e"

STRAIN = "Test Strain"
GROW_MEDIUM = "DWC"
START_DATE = "2025-11-21"

def get_summary():
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "strain": STRAIN,
        "medium": GROW_MEDIUM,
        "day": max(1, (datetime.now() - datetime.fromisoformat(START_DATE)).days + 1),
        "temp": sensors.get("local/temp", {}).get("value", None),
        "humidity": sensors.get("local/humidity", {}).get("value", None),
        "ph": sensors.get("local/ph", {}).get("value", None),
        "ec": sensors.get("local/ec", {}).get("value", None),
        "co2": sensors.get("local/co2", {}).get("value", None),
        "health": sensors.get("ai/plant_health", {}).get("value", "unknown"),
        "version": "v2.2"
    }

def harvest_loop():
    while True:
        try:
            payload = get_summary()
            requests.post(ENDPOINT, json=payload, timeout=8)
        except:
            pass
        time.sleep(86400)  # once per day

threading.Thread(target=harvest_loop, daemon=True).start()
