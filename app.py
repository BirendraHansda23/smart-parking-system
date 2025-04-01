from flask import Flask, render_template, jsonify, make_response
import time
import threading
import sqlite3
import os
import random  # For simulation

app = Flask(__name__)

# Initialize database
DB_FILE = 'parking_logs.db'

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_id TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp DATETIME NOT NULL
        )
        ''')
        conn.commit()
        conn.close()

init_db()

# Initial sensor data
sensor_data = {
    "slot_1": False,
    "slot_2": False,
    "slot_3": False,
}

# Simulation function (since you might not have real sensors)
def simulate_sensor_data():
    global sensor_data
    while True:
        for slot in sensor_data:
            # Randomly change status (10% chance)
            if random.random() < 0.1:
                sensor_data[slot] = not sensor_data[slot]
                log_state_change(slot, sensor_data[slot])
        time.sleep(2)

def log_state_change(slot_id, new_status):
    """Log changes to the database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    status_text = "Occupied" if new_status else "Available"
    
    cursor.execute(
        "INSERT INTO logs (slot_id, status, timestamp) VALUES (?, ?, ?)",
        (slot_id, status_text, timestamp)
    )
    
    conn.commit()
    conn.close()

# API Endpoints
@app.route("/api/sensor-data")
def get_sensor_data():
    response = make_response(jsonify(sensor_data))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

@app.route("/api/logs")
def get_logs():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 100")
    logs = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    response = make_response(jsonify(logs))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    # Start sensor simulation thread
    sensor_thread = threading.Thread(target=simulate_sensor_data, daemon=True)
    sensor_thread.start()
    
    # Run Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)