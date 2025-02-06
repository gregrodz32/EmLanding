import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import dash_bootstrap_components as dbc

# Your OpenWeatherMap API key
API_KEY = 'fda0da1cb56d840df2bfd84074038d8b'
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the layout of the dashboard
app.layout = html.Div([
    html.H1("Emergency Landing System Dashboard"),
    
    # Flight Data
    html.Div([
        html.H3("Flight Data"),
        html.Pre(id='flight-data', children="Loading..."),
    ]),
    
    # Weather Data
    html.Div([
        html.H3("Weather Data"),
        html.Label("Latitude:"),
        dcc.Input(id='latitude-input', type='number', value=37.7749, debounce=True),  # Default: San Francisco latitude
        html.Label("Longitude:"),
        dcc.Input(id='longitude-input', type='number', value=-122.4194, debounce=True),  # Default: San Francisco longitude
        html.Button('Get Weather', id='weather-button', n_clicks=0),
        html.Pre(id='weather-data', children="Loading..."),
    ]),
    
    # Predicted Landing Site
    html.Div([
        html.H3("Predicted Landing Site"),
        html.Pre(id='landing-site', children="Loading..."),
    ])
])

# Define the callbacks to update components with data from the backend

# Callback for fetching flight data (using your existing backend)
@app.callback(
    Output('flight-data', 'children'),
    Input('flight-data', 'id')
)
def update_flight_data(n):
    response = requests.get(f"{BASE_URL}/flight_data")
    if response.status_code == 200:
        flight_data = response.json()[0]
        return f"Altitude: {flight_data['altitude']} ft\nLatitude: {flight_data['latitude']}\nLongitude: {flight_data['longitude']}"
    return "Error fetching flight data"

# Callback for fetching weather data from OpenWeatherMap
@app.callback(
    Output('weather-data', 'children'),
    Input('weather-button', 'n_clicks'),
    Input('latitude-input', 'value'),
    Input('longitude-input', 'value')
)
def update_weather_data(n_clicks, latitude, longitude):
    if n_clicks > 0:
        # Construct the OpenWeatherMap API URL with the provided latitude, longitude, and API key
        url = f"{BASE_URL}?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        
        # If the response is successful, process the data
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            weather_description = weather_data['weather'][0]['description']
            
            # Return the weather data to display in the UI
            return f"Temperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s\nDescription: {weather_description}"
        else:
            return "Error: Unable to fetch weather data"
    return "Enter latitude and longitude, then click 'Get Weather'"

# Callback for fetching landing site prediction (using your existing backend)
@app.callback(
    Output('landing-site', 'children'),
    Input('landing-site', 'id')
)
def update_landing_site(n):
    response = requests.get(f"{BASE_URL}/landing_site")
    if response.status_code == 200:
        landing_site = response.json()
        return f"Latitude: {landing_site['latitude']}\nLongitude: {landing_site['longitude']}\nAltitude: {landing_site['altitude']} ft"
    return "Error fetching landing site prediction"

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
