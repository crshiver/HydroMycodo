import board, busio, time
import adafruit_dht
import adafruit_shtc3
import adafruit_bme680
import adafruit_scd4x
import adafruit_ccs811

i2c = busio.I2C(board.SCL, board.SDA)

def read_local_sensors():
    data = {}
    # DHT22 on GPIO4
    try:
        dht = adafruit_dht.DHT22(board.D4)
        data["local/dht_temp"] = round(dht.temperature, 1)
        data["local/dht_hum"] = round(dht.humidity, 1)
    except: pass

    # SHT4x
    try:
        sht = adafruit_shtc3.SHTC3(i2c)
        data["local/sht_temp"] = round(sht.temperature, 1)
        data["local/sht_hum"] = round(sht.relative_humidity, 1)
    except: pass

    # BME680
    try:
        bme = adafruit_bme680.Adafruit_BME680_I2C(i2c)
        data["local/bme_temp"] = round(bme.temperature, 1)
        data["local/bme_hum"] = round(bme.relative_humidity, 1)
        data["local/bme_pressure"] = round(bme.pressure)
        data["local/bme_gas"] = bme.gas
    except: pass

    # SCD4x CO₂
    try:
        scd = adafruit_scd4x.SCD4X(i2c)
        scd.start_periodic_measurement()
        time.sleep(1)
        if scd.data_ready:
            data["local/co2"] = scd.CO2
    except: pass

    # CCS811 VOC
    try:
        ccs = adafruit_ccs811.CCS811(i2c)
        if ccs.data_ready():
            data["local/eco2"] = ccs.eco2
            data["local/tvoc"] = ccs.tvoc
    except: pass

    return data
