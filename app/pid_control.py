from simple_pid import PID
import threading, time
from flask import jsonify, request
from app import app, db, sensors

# Relay pins (change to your actual GPIO pins)
PUMP_PH_UP   = 17
PUMP_PH_DOWN = 27
PUMP_NUTE_A  = 22
PUMP_NUTE_B  = 23
FAN          = 24
HEATER       = 25

for pin in [PUMP_PH_UP, PUMP_PH_DOWN, PUMP_NUTE_A, PUMP_NUTE_B, FAN, HEATER]:
    from RPi import GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # off = HIGH if using common relays

class Controller:
    def __init__(self, name, sensor_topic, setpoint, kp, ki, kd, output_pin, reverse=False):
        self.pid = PID(kp, ki, kd, setpoint=setpoint, output_limits=(0, 30))  # max 30s on per minute
        self.sensor_topic = sensor_topic
        self.output_pin = output_pin
        self.reverse = reverse
        self.name = name

controllers = [
    Controller("pH Up",   "local/ph",        5.8, 2.0, 0.1, 0.05, PUMP_PH_UP),
    Controller("pH Down", "local/ph",        5.8, 2.0, 0.1, 0.05, PUMP_PH_DOWN, reverse=True),
    Controller("Nutrient A", "local/ec",    1.4, 3.0, 0.2, 0.1, PUMP_NUTE_A),
    Controller("Nutrient B", "local/ec",    1.4, 3.0, 0.2, 0.1, PUMP_NUTE_B),
    Controller("Temperature", "local/temp", 24.0, 2.0, 0.5, 0.1, HEATER),
    Controller("Fan",        "local/humidity", 60, 1.5, 0.3, 0.05, FAN, reverse=True),
]

def control_loop():
    while True:
        for c in controllers:
            val = float(sensors.get(c.sensor_topic, {}).get("value", 0) or 0)
            output = c.pid(val)
            state = int(output > 0) if not c.reverse else int(output == 0)
            GPIO.output(c.output_pin, GPIO.HIGH if state == 0 else GPIO.LOW)
        time.sleep(60)  # run every minute

threading.Thread(target=control_loop, daemon=True).start()
