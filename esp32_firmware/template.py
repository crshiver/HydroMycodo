# Copy this file, add your sensor libraries and publish away!
from umqtt.simple import MQTTClient
import network, time

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# CHANGE THESE TWO LINES ONLY
wifi_ssid = "YOUR_WIFI_SSID"
wifi_pass = "YOUR_WIFI_PASS"
pi_ip     = "YOUR_PI_IP"
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_pass)
while not wlan.isconnected(): time.sleep(1)

c = MQTTClient("my-esp32", pi_ip)
c.connect()

while True:
    # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
    # ADD YOUR SENSOR READINGS HERE
    c.publish("hydro/test/value", "42.0")
    # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
    time.sleep(30)
