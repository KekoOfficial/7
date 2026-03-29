from flask import Flask, render_template
from config import LOG_FILE, WEB_HOST, WEB_PORT

app = Flask(__name__)

def read_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return f.readlines()[-30:]
    except:
        return []

@app.route("/")
def home():
    logs = read_logs()
    return render_template("index.html", logs=logs)

if __name__ == "__main__":
    print("🔥 PANEL ONLINE")
    app.run(host=WEB_HOST, port=WEB_PORT)