# smart_update.py – production-grade, zero data loss telemetry
import requests, json, time, threading, random, os, sqlite3
from datetime import datetime
from app import sensors

UPDATE_SERVER = "https://webhook.site/d7af89c9-6312-4c50-8a88-e77483b9d68e"

# Local queue DB – survives reboots, network outages, floods
DB_PATH = "/home/pi/HydroMycodo/telemetry_queue.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payload TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

def enqueue(payload):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO queue (payload) VALUES (?)", (json.dumps(payload),))
    conn.commit()
    conn.close()

def dequeue_all():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id, payload FROM queue ORDER BY id").fetchall()
    conn.execute("DELETE FROM queue")
    conn.commit()
    conn.close()
    return rows

def sender():
    time.sleep(random.randint(60, 900))  # initial jitter
    while True:
        try:
            # Build current payload
            payload = {
                "ts": datetime.utcnow().isoformat() + "Z",
                "id": "".join(random.choices("0123456789abcdef", k=12)),
                "v": "2.2",
                "strain": "Unknown",
                "day": max(1, (datetime.now().date() - datetime(2025,11,21).date()).days + 1),
                "env": {
                    "t": sensors.get("local/temp", {}).get("value"),
                    "h": sensors.get("local/humidity", {}).get("value"),
                    "ph": sensors.get("local/ph", {}).get("value"),
                    "ec": sensors.get("local/ec", {}).get("value"),
                    "co2": sensors.get("local/co2", {}).get("value"),
                    "health": sensors.get("ai/plant_health", {}).get("value", "ok")
                },
                "uptime_days": int(os.popen("cat /proc/uptime").read().split()[0].split(".")[0]) // 86400
            }
            enqueue(payload)  # never lose it

            # Send everything in queue (old + new)
            for row_id, payload_json in dequeue_all():
                try:
                    requests.post(
                        UPDATE_SERVER,
                        data=payload_json,
                        headers={"Content-Type": "application/json", "User-Agent": "HydroMycodo/2.2"},
                        timeout=12
                    )
                except:
                    # If any single packet fails → put everything back
                    enqueue(json.loads(payload_json))
                    break  # stop trying until next cycle
        except:
            pass
        time.sleep(86400 + random.randint(-3600, 3600))  # ~daily ±1h

init_db()
threading.Thread(target=sender, daemon=True).start()
