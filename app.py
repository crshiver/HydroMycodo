from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1 style='text-align:center;margin-top:100px'>🌱 HydroMycodo<br>by Crshiver & Grok<br>Real repo – launching now!</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)