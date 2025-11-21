import time, board, busio
from adafruit_ads1x15.ads1115 import ADS1115, Mode
from simple_pid import PID

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)

def calibrate_ph():
    print("pH 7.0 in buffer → press Enter")
    input(); v7 = ads.read_adc(0)
    print("pH 4.0 in buffer → press Enter")
    input(); v4 = ads.read_adc(0)
    slope = (7.0 - 4.0) / (v7 - v4)
    offset = 7.0 - slope * v7
    with open("/home/pi/HydroMycodo/calibration.txt", "w") as f:
        f.write(f"ph_slope={slope}\nph_offset={offset}\n")
    return slope, offset

def read_ph():
    with open("/home/pi/HydroMycodo/calibration.txt") as f:
        d = dict(line.strip().split("=") for line in f)
    v = ads.read_adc(0)
    ph = float(d["ph_slope"]) * v + float(d["ph_offset"])
    sensors["local/ph"]["value"] = round(ph, 2)

# Run calibration on first boot if no file
if not os.path.exists("/home/pi/HydroMycodo/calibration.txt"):
    calibrate_ph()
