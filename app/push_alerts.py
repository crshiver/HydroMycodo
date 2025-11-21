import requests, time, threading
from app import sensors

PUSHOVER_USER = "YOUR_PUSHOVER_USER_KEY"
PUSHOVER_TOKEN = "YOUR_PUSHOVER_API_TOKEN"

def push(title, msg, priority=0):
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_TOKEN, "user": PUSHOVER_USER,
        "title": title, "message": msg, "priority": priority, "sound": "siren" if priority==2 else "magic"
    })

def alert_loop():
    last_ph = last_co2 = None
    while True:
        ph = sensors.get("local/ph", {}).get("value")
        co2 = sensors.get("local/co2", {}).get("value")
        if ph and (last_ph is None or abs(ph - last_ph) > 0.3):
            push("pH Alert", f"pH is now {ph}", 2 if not 5.5 <= ph <= 6.5 else 1)
        if co2 and co2 > 1500:
            push("CO₂ CRITICAL", f"CO₂ at {co2} ppm – VENT NOW!", 2)
        last_ph = ph
        time.sleep(300)

threading.Thread(target=alert_loop, daemon=True).start()
