from machine import Pin
from umqtt.simple import MQTTClient
import network, time, dht

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("YOUR_WIFI_SSID", "YOUR_WIFI_PASS")
while not wlan.isconnected(): time.sleep(1)

d = dht.DHT22(Pin(4))
c = MQTTClient("esp32-dht", "YOUR_PI_IP")
c.connect()

while True:
    d.measure()
    c.publish("hydro/zone1/temp", str(d.temperature()))
    c.publish("hydro/zone1/humidity", str(d.humidity()))
    time.sleep(30)
