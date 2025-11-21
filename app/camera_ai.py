import cv2, time, os
from threading import Thread
from picamera2 import Picamera2
from ultralytics import YOLO

model = YOLO("yolov8n-plant-disease.pt")  # will auto-download on first run

def camera_loop():
    picam = Picamera2()
    picam.start()
    while True:
        img = picam.capture_array()
        results = model(img, imgsz=640, conf=0.4)
        health = "Healthy"
        for r in results:
            for label in r.boxes.cls:
                name = model.names[int(label)]
                if "deficiency" in name or "disease" in name:
                    health = name.replace("_", " ").title()
        sensors["ai/plant_health"]["value"] = health
        sensors["ai/plant_health"]["time"] = time.strftime("%H:%M:%S")
        cv2.imwrite("/home/pi/HydroMycodo/app/static/latest.jpg", img)
        time.sleep(300)  # every 5 min

Thread(target=camera_loop, daemon=True).start()
