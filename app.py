"""
Weather Predictor API
A Flask application that provides real-time weather for Kenyan counties.
"""

import os

from flask import Flask, request, jsonify
import json
import logging
import urllib.request
import urllib.error
from werkzeug.exceptions import BadRequest

from kenyan_counties import KENYAN_COUNTIES, get_county_by_name

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEATHER_CODE_MAP = {
    0: "clear", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "depositing rime fog", 51: "light drizzle", 53: "moderate drizzle",
    55: "dense drizzle", 56: "light freezing drizzle", 57: "dense freezing drizzle",
    61: "light rain", 63: "moderate rain", 65: "heavy rain",
    66: "light freezing rain", 67: "heavy freezing rain",
    71: "light snow", 73: "moderate snow", 75: "heavy snow", 77: "snow grains",
    80: "rain showers", 81: "moderate rain showers", 82: "violent rain showers",
    85: "light snow showers", 86: "heavy snow showers",
    95: "thunderstorm", 96: "thunderstorm with hail", 99: "thunderstorm with heavy hail",
}


def fetch_current_weather(latitude, longitude):
    """Fetch real-time weather from Open-Meteo API."""
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current_weather=true&timezone=Africa%2FNairobi"
    )
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode())
    current = data.get("current_weather")
    if not current:
        raise ValueError("No current weather returned by API")

    return {
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "winddirection": current.get("winddirection"),
        "weathercode": current.get("weathercode"),
        "condition": WEATHER_CODE_MAP.get(current.get("weathercode"), "unknown"),
        "time": current.get("time"),
    }


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Get real-time weather for a Kenyan county.
    
    Request JSON:
        - county (str): Name of the Kenyan county
        - all_counties (bool): If true, return weather for all counties
    
    Response JSON:
        - county/counties with current weather data
    """
    try:
        data = request.get_json()
        if data is None or not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON"}), 400

        # Get weather for all counties
        if data.get("all_counties", False):
            counties_data = []
            for county in KENYAN_COUNTIES:
                weather = fetch_current_weather(county["latitude"], county["longitude"])
                counties_data.append({
                    "name": county["name"],
                    "latitude": county["latitude"],
                    "longitude": county["longitude"],
                    "current_weather": weather,
                })
            return jsonify({"counties": counties_data}), 200

        # Get weather for a specific county
        county_name = data.get("county", "").strip()
        if county_name:
            county = get_county_by_name(county_name)
            if county is None:
                return jsonify({"error": f"County '{county_name}' not found"}), 404

            weather = fetch_current_weather(county["latitude"], county["longitude"])
            return jsonify({
                "county": county["name"],
                "latitude": county["latitude"],
                "longitude": county["longitude"],
                "current_weather": weather,
            }), 200

        return jsonify({"error": "County name or all_counties flag is required"}), 400

    except urllib.error.URLError as e:
        logger.error(f"Weather API request failed: {e}")
        return jsonify({"error": "Unable to fetch current weather"}), 502
    except BadRequest as e:
        logger.error(f"Bad request in predict endpoint: {str(e)}")
        return jsonify({"error": "Invalid JSON"}), 400
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5000)))
    app.run(host="0.0.0.0", port=port, debug=False)
