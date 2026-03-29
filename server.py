import json
import os
from flask import Flask, request, jsonify, render_template
from config import LOG_FILE, QUEUE_FILE, WEB_HOST, WEB_PORT, ADMIN_ID

app = Flask(__name__, template_folder="templates")

# =========================
# UTIL
# =========================

def load_queue():
    if os.path.exists(QUEUE_FILE):
        try:
            return json.load(open(QUEUE_FILE))
        except:
            return []
    return []

def save_queue(q):
    with open(QUEUE_FILE, "w") as f:
        json.dump(q, f)

def load_logs():
    if os.path.exists(LOG_FILE):
        return open(LOG_FILE).readlines()[-50:]
    return []

# =========================
# API SEND
# =========================

@app.route("/send", methods=["POST"])
def send():
    data = request.json

    if int(data.get("admin_id", 0)) != ADMIN_ID:
        return jsonify({"status": "denied"}), 403

    queue = load_queue()
    queue.append({
        "id": data["id"],
        "msg": data["msg"]
    })

    save_queue(queue)

    return jsonify({"status": "ok"})

# =========================
# LOGS
# =========================

@app.route("/logs")
def logs():
    return jsonify({"logs": load_logs()})

# =========================
# PANEL
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# RUN
# =========================

if __name__ == "__main__":
    print("🌐 PANEL ONLINE")
    app.run(host=WEB_HOST, port=WEB_PORT)