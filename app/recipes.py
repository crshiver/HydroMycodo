import json, time, threading
from datetime import datetime

RECIPES = {
    "DWC Lettuce":   {"ph": 5.8, "ec": 1.2, "duration_weeks": 6},
    "NFT Basil":     {"ph": 6.0, "ec": 1.4, "duration_weeks": 8},
    "Aeroponics":    {"ph": 5.7, "ec": 1.6, "duration_weeks": 10},
    "Soil Cannabis Veg":  {"ph": 6.2, "ec": 1.3, "duration_weeks": 4},
    "Soil Cannabis Flower": {"ph": 6.5, "ec": 2.0, "duration_weeks": 9},
}

current_recipe = "DWC Lettuce"

def scheduler():
    while True:
        sensors["system/recipe"]["value"] = current_recipe
        sensors["system/week"]["value"] = int((time.time() - start_time) // (7*86400)) + 1
        time.sleep(3600)

threading.Thread(target=scheduler, daemon=True).start()
