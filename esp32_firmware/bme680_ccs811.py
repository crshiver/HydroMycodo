from machine import Pin, I2C
from umqtt.simple import MQTTClient
import network, time, bme680, ccs811

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("YOUR_WIFI_SSID", "YOUR_WIFI_PASS")
while not wlan.isconnected(): time.sleep(1)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
bme = bme680.BME680_I2C(i2c)
ccs = ccs811.CCS811(i2c)

c = MQTTClient("esp32-bme-ccs", "YOUR_PI_IP")
c.connect()

while True:
    if bme.data.heat_stable:
        c.publish("hydro/zone1/temp", str(round(bme.data.temperature,1)))
        c.publish("hydro/zone1/humidity", str(round(bme.data.humidity,1)))
        c.publish("hydro/zone1/pressure", str(round(bme.data.pressure)))
        c.publish("hydro/zone1/gas_resistance", str(bme.data.gas_resistance))
    if ccs.data_ready():
        c.publish("hydro/zone1/eco2", str(ccs.eco2))
        c.publish("hydro/zone1/tvoc", str(ccs.tvoc))
    time.sleep(20)
