from machine import Pin, I2C
from umqtt.simple import MQTTClient
import network, time
import sht4x, scd4x

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("YOUR_WIFI_SSID", "YOUR_WIFI_PASS")
while not wlan.isconnected(): time.sleep(1)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
sht = sht4x.SHT4X(i2c)
scd = scd4x.SCD4X(i2c)
scd.start_periodic_measurement()

c = MQTTClient("esp32-sht-scd", "YOUR_PI_IP")
c.connect()

while True:
    t, rh = sht.measure()
    co2 = scd.CO2
    c.publish("hydro/zone1/temp", str(t))
    c.publish("hydro/zone1/humidity", str(rh))
    c.publish("hydro/zone1/co2", str(co2))
    time.sleep(30)
