from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
from adsb_data import get_adsb_data
from weather_data import get_weather_data
from prediction_model import predict_landing_site

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) to allow frontend to communicate with backend

# API Endpoint to fetch flight telemetry data
@app.route('/flight_data', methods=['GET'])
def flight_data():
    # Simulate fetching live ADS-B flight data
    data = get_adsb_data()
    return jsonify(data)

# API Endpoint to fetch weather data
@app.route('/weather_data', methods=['GET'])
def weather_data():
    # Simulate fetching weather data (e.g., from NOAA)
    data = get_weather_data()
    return jsonify(data)

# API Endpoint to get the predicted emergency landing site
@app.route('/landing_site', methods=['GET'])
def landing_site():
    # Predict the best emergency landing site based on flight data, terrain, and weather
    landing_site = predict_landing_site()
    return jsonify(landing_site)

def run_backend():
    # Running the Flask server
    app.run(host="0.0.0.0", port=5000)

# Run Flask app in a separate thread to avoid blocking
if __name__ == '__main__':
    threading.Thread(target=run_backend).start()

