from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import paho.mqtt.client as mqtt
from collections import defaultdict
from datetime import datetime
import threading, time
import board, busio, adafruit_dht, adafruit_shtc3, adafruit_bme680, adafruit_scd4x, adafruit_ccs811

app = Flask(__name__)
app.secret_key = "hydro2025-change-me-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hydro.db"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id): return User.query.get(int(user_id))

# MQTT + unified sensor dict
sensors = defaultdict(lambda: {"value":"—","time":"never"})

def on_mqtt(client, userdata, msg):
    try:
        v = msg.payload.decode().strip()
        sensors[msg.topic]["value"] = v
        sensors[msg.topic]["time"] = datetime.now().strftime("%H:%M:%S")
    except: pass

client = mqtt.Client()
client.on_message = on_mqtt
client.connect("localhost", 1883, 60)
client.subscribe("hydro/#")
client.loop_start()

# Local sensor reading
i2c = busio.I2C(board.SCL, board.SDA)
def read_local():
    try: dht = adafruit_dht.DHT22(board.D4)
    except: dht = None
    while True:
        # DHT22
        if dht:
            try:
                sensors["local/dht_temp"]["value"] = round(dht.temperature,1)
                sensors["local/dht_hum"]["value"] = round(dht.humidity,1)
                sensors["local/dht_temp"]["time"] = datetime.now().strftime("%H:%M:%S")
            except: pass
        # SHT4x
        try:
            sht = adafruit_shtc3.SHTC3(i2c)
            sensors["local/sht_temp"]["value"] = round(sht.temperature,1)
            sensors["local/sht_hum"]["value"] = round(sht.relative_humidity,1)
        except: pass
        # BME680
        try:
            bme = adafruit_bme680.Adafruit_BME680_I2C(i2c)
            sensors["local/bme_temp"]["value"] = round(bme.temperature,1)
            sensors["local/bme_hum"]["value"] = round(bme.relative_humidity,1)
            sensors["local/bme_pressure"]["value"] = round(bme.pressure)
        except: pass
        # SCD41 CO₂
        try:
            scd = adafruit_scd4x.SCD4X(i2c)
            if scd.data_ready:
                sensors["local/co2"]["value"] = scd.CO2
        except: pass
        # CCS811 VOC
        try:
            ccs = adafruit_ccs811.CCS811(i2c)
            if ccs.data_ready():
                sensors["local/eco2"]["value"] = ccs.eco2
                sensors["local/tvoc"]["value"] = ccs.tvoc
        except: pass
        time.sleep(15)

threading.Thread(target=read_local, daemon=True).start()

# Routes
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html", sensors=sensors)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", password="hydro2025")
            db.session.add(admin)
            db.session.commit()
    app.run(host="0.0.0.0", port=5000)
import app.pid_control, app.camera_ai  # auto-starts on import
import app.calibration, app.push_alerts, app.recipes
