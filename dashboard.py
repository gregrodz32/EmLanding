import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import json
import requests

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = html.Div([
    # Title and description
    html.H1('Emergency Landing System Dashboard', style={'text-align': 'center'}),
    
    # Real-time monitoring graphs
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(id='flight-data-graph', style={'height': '400px'})),
            dbc.Col(dcc.Graph(id='weather-graph', style={'height': '400px'})),
        ])
    ], className='mb-4'),
    
    # CesiumJS Map
    html.Div([
        html.Iframe(id='map', srcDoc='', width='100%', height='600px', style={'border': 'none'}),
    ], className='mb-4'),
    
    # Control panel for user interactions
    html.Div([
        dbc.Row([
            dbc.Col(dbc.Button('Start Flight', id='start-flight-btn', color='primary', block=True)),
            dbc.Col(dbc.Button('Pause Flight', id='pause-flight-btn', color='secondary', block=True)),
        ])
    ], className='mb-4')
])

# Callback for updating graphs and map
@app.callback(
    [Output('flight-data-graph', 'figure'),
     Output('weather-graph', 'figure'),
     Output('map', 'srcDoc')],
    [Input('start-flight-btn', 'n_clicks'),
     Input('pause-flight-btn', 'n_clicks')]
)
def update_data(start_clicks, pause_clicks):
    # Example of fetching live data for updates
    flight_data = requests.get('http://localhost:5000/flight_data')  # Fetch from backend
    weather_data = requests.get('http://localhost:5000/weather_data')  # Fetch weather data
    flight_json = flight_data.json()
    weather_json = weather_data.json()

    # Flight data graph
    flight_figure = {
        'data': [{
            'x': [flight['timestamp'] for flight in flight_json],
            'y': [flight['altitude'] for flight in flight_json],
            'type': 'line',
            'name': 'Altitude'
        }],
        'layout': {
            'title': 'Flight Altitude Over Time',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Altitude (ft)'},
        }
    }

    # Weather data graph
    weather_figure = {
        'data': [{
            'x': [weather['timestamp'] for weather in weather_json],
            'y': [weather['temperature'] for weather in weather_json],
            'type': 'line',
            'name': 'Temperature'
        }],
        'layout': {
            'title': 'Weather Conditions Over Time',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Temperature (°C)'},
        }
    }

    # Map with CesiumJS
    cesium_html = '''
        <html>
            <head>
                <script src="https://cesium.com/downloads/cesiumjs/releases/1.85/Build/Cesium/Widgets/widgets.js"></script>
                <script src="https://cesium.com/downloads/cesiumjs/releases/1.85/Build/Cesium/Cesium.js"></script>
                <link href="https://cesium.com/downloads/cesiumjs/releases/1.85/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
            </head>
            <body>
                <div id="cesiumContainer" style="width: 100%; height: 100%;"></div>
                <script>
                    const viewer = new Cesium.Viewer('cesiumContainer');
                    // Example: Add a marker for the landing site
                    viewer.entities.add({
                        name: 'Landing Site',
                        position: Cesium.Cartesian3.fromDegrees(-75.59777, 40.03883),
                        point: { pixelSize: 10, color: Cesium.Color.RED }
                    });
                </script>
            </body>
        </html>
    '''

    return flight_figure, weather_figure, cesium_html

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
