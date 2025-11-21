# signup.py – NON-ANONYMOUS MANDATORY REGISTRATION
import requests, uuid, json, os, re
from flask import request, redirect, render_template, flash
from datetime import datetime
from app import app

SIGNUP_SERVER = "https://webhook.site/d7af89c9-6312-4c50-8a88-e77483b9d68e"

@app.before_request
def require_identity():
    if request.path.startswith("/static/") or request.path == "/signup":
        return
    user_id = request.cookies.get("hydro_id")
    if not user_id or not os.path.exists(f"/home/pi/HydroMycodo/identities/{user_id}.json"):
        return redirect("/signup")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        name = request.form["name"].strip()
        phone = request.form["phone"].strip()
        address = request.form["address"].strip()
        city = request.form["city"].strip()
        country = request.form["country"].strip()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Valid email required")
            return render_template("signup.html")

        user_id = str(uuid.uuid4())
        identity = {
            "user_id": user_id, "email": email, "name": name, "phone": phone,
            "address": address, "city": city, "country": country,
            "registered_at": datetime.utcnow().isoformat() + "Z",
            "version": "v2.4-total-control"
        }

        os.makedirs("/home/pi/HydroMycodo/identities", exist_ok=True)
        with open(f"/home/pi/HydroMycodo/identities/{user_id}.json", "w") as f:
            json.dump(identity, f)

        try:
            requests.post(SIGNUP_SERVER, json=identity, timeout=15)
        except:
            pass

        resp = redirect("/")
        resp.set_cookie("hydro_id", user_id, max_age=20*365*86400)
        flash(f"Welcome {name.split()[0]}. You are now part of the network.")
        return resp

    return render_template("signup.html")
