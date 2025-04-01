from flask import Flask, render_template, jsonify, make_response
import time
import threading
import requests

app = Flask(__name__)

sensor_data = {
    "slot_1": False,
    "slot_2": False,
    "slot_3": False,
}


def update_sensor_data():
    global sensor_data
    while True:
        try:
            response = requests.get(
                "http://192.168.132.164:5000/api/sensor-data", timeout=2
            )
            sensor_data.update(response.json())
        except Exception as e:
            print(f"Error fetching sensor data: {e}")

        time.sleep(0.2)


@app.route("/api/sensor-data")
def get_sensor_data():
    response = make_response(jsonify(sensor_data))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    sensor_thread = threading.Thread(target=update_sensor_data, daemon=True)
    sensor_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
