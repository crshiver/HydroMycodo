from flask import Flask, render_template
import paho.mqtt.client as mqtt
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)
sensors = defaultdict(lambda: {"value":"—","time":"never"})

def on_message(c,u,m):
    try:
        v = m.payload.decode().strip()
        sensors[m.topic]["value"] = v
        sensors[m.topic]["time"] = datetime.now().strftime("%H:%M:%S")
    except: pass

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost",1883,60)
client.subscribe("hydro/#")
client.loop_start()

@app.route('/')
def dashboard():
    return render_template('dashboard.html', sensors=sensors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
