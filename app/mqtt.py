import paho.mqtt.client as mqtt
from datetime import datetime
from collections import defaultdict

sensors = defaultdict(lambda: {"value": None, "updated": None})

def on_message(client, userdata, msg):
    topic = msg.topic
    value = msg.payload.decode()
    sensors[topic]["value"] = value
    sensors[topic]["updated"] = datetime.now().strftime("%H:%M:%S")

def start_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.subscribe("hydro/#")
    client.loop_start()

def get_sensors():
    return dict(sensors)