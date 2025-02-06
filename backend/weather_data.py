import requests
from flask import Flask, jsonify
from opensky_api import OpenSkyApi

# Initialize Flask app
app = Flask(__name__)

# OpenSky API setup
api = OpenSkyApi()

# OpenWeatherMap API details
WEATHER_API_KEY = 'fda0da1cb56d840df2bfd84074038d8b'  # Replace with your OpenWeatherMap API key

# Function to fetch weather data from OpenWeatherMap
def get_weather_data(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/flight_and_weather_data', methods=['GET'])
def get_flight_and_weather_data():
    # Fetch current flight data (positions of aircraft)
    states = api.get_states()

    if states.states:
        flight_data = states.states[0]  # Get data for the first aircraft (you can loop for more)
        
        # Get weather data based on aircraft's position
        weather_data = get_weather_data(flight_data.latitude, flight_data.longitude)
        
        # If weather data is available, return both flight data and weather data
        if weather_data:
            data = {
                "icao24": flight_data.icao24,
                "latitude": flight_data.latitude,
                "longitude": flight_data.longitude,
                "altitude": flight_data.altitude,
                "velocity": flight_data.velocity,
                "heading": flight_data.heading,
                "on_ground": flight_data.on_ground,
                "weather": {
                    "temperature": weather_data['main']['temp'],
                    "humidity": weather_data['main']['humidity'],
                    "windspeed": weather_data['wind']['speed'],
                    "weather_description": weather_data['weather'][0]['description']
                }
            }
            return jsonify(data)
        
        return jsonify({"error": "Weather data not available"}), 500
    
    return jsonify({"error": "No flight data available"}), 500

if __name__ == '__main__':
    app.run(debug=True)
