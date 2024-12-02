from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

ORS_API_KEY = "5b3ce3597851110001cf6248b3782f56a250458aad0e370fa48340d1"  # Replace with your OpenRouteService API Key


def geocode_location(location_name):
    """Fetch coordinates for a given location using ORS Geocoding API."""
    url = f"https://api.openrouteservice.org/geocode/search"
    params = {"api_key": ORS_API_KEY, "text": location_name, "size": 1}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("features"):
        return data["features"][0]["geometry"]["coordinates"]
    return None


@app.route('/api/routing', methods=['POST'])
def routing():
    """Fetch route geometry and details between two locations."""
    data = request.json
    start = data.get("start")
    end = data.get("end")

    start_coords = geocode_location(start)
    end_coords = geocode_location(end)

    if not start_coords or not end_coords:
        return jsonify({"error": "Unable to geocode locations"}), 400

    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_API_KEY}
    body = {"coordinates": [start_coords, end_coords]}

    response = requests.post(url, json=body, headers=headers)
    route_data = response.json()

    distance = route_data['routes'][0]['summary']['distance'] / 1000  # Convert meters to km
    duration = route_data['routes'][0]['summary']['duration'] / 60    # Convert seconds to minutes

    return jsonify({
        "start": start,
        "end": end,
        "distance": round(distance, 2),
        "duration": round(duration, 2),
        "geometry": route_data['routes'][0]['geometry']
    })


@app.route('/api/traffic', methods=['POST'])
def traffic():
    """Predict traffic volume based on time of day."""
    data = request.json
    time_of_day = data.get("time_of_day")

    if 7 <= time_of_day <= 9 or 16 <= time_of_day <= 18:
        traffic_volume = "High"
    elif 10 <= time_of_day <= 15:
        traffic_volume = "Moderate"
    else:
        traffic_volume = "Low"

    return jsonify({"predicted_traffic": traffic_volume})


if __name__ == '__main__':
    app.run(debug=True)
