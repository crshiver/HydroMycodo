from flask import Flask, render_template, jsonify
from mqtt import start_mqtt, get_sensors

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html', sensors=get_sensors())

@app.route('/data')
def data():
    return jsonify(get_sensors())

if __name__ == '__main__':
    start_mqtt()
    app.run(host='0.0.0.0', port=5000, debug=False)