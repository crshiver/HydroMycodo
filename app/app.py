from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import mqtt_handler, local_sensors, threading, time
from simple_pid import PID

app = Flask(__name__)
app.secret_key = "hydro2025-change-me"
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

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "hydro2025":
            user = User.query.filter_by(username="admin").first()
            if not user:
                user = User(username="admin", password="hydro2025")
                db.session.add(user)
                db.session.commit()
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Bad credentials")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html", sensors=mqtt_handler.sensors)

@app.route("/pid")
@login_required
def pid():
    return render_template("pid.html")

# Background local sensor reader
def sensor_loop():
    while True:
        for k,v in local_sensors.read_local_sensors().items():
            mqtt_handler.sensors[k]["value"] = v
            mqtt_handler.sensors[k]["time"] = time.strftime("%H:%M:%S")
        time.sleep(15)

threading.Thread(target=sensor_loop, daemon=True).start()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    mqtt_handler.start()
    app.run(host="0.0.0.0", port=5000)
