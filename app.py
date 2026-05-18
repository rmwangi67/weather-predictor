"""
Weather Predictor API
A Flask application that provides real-time weather for Kenyan counties.
"""

import os
import json
import logging
import urllib.request
import urllib.error
from urllib.parse import urlencode

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

from kenyan_counties import KENYAN_COUNTIES, get_county_by_name

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Change this via env var in Docker/CI: APP_VERSION=1.0.3 etc.
APP_VERSION = os.environ.get("APP_VERSION", "1.0")
TIMEZONE = os.environ.get("TIMEZONE", "Africa/Nairobi")

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


def fetch_current_weather(latitude: float, longitude: float) -> dict:
    """Fetch real-time weather from Open-Meteo API."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "timezone": TIMEZONE,
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urlencode(params)

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        current = data.get("current_weather")
        if not current:
            raise ValueError("No current weather returned by API")

        code = current.get("weathercode")
        return {
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "winddirection": current.get("winddirection"),
            "weathercode": code,
            "condition": WEATHER_CODE_MAP.get(code, "unknown"),
            "time": current.get("time"),
        }

    except urllib.error.HTTPError as e:
        # API responded but with error status code (e.g., 4xx/5xx)
        logger.error("Open-Meteo HTTPError: %s", e)
        raise
    except urllib.error.URLError as e:
        # Network/DNS/timeout errors
        logger.error("Open-Meteo URLError: %s", e)
        raise


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Weather Predictor API is running",
        "version": APP_VERSION,
        "endpoints": {
            "health": "/health",
            "version": "/version",
            "predict": "/predict (POST)",
        }
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "OK"}), 200


@app.route("/version", methods=["GET"])
def version():
    return jsonify({"version": APP_VERSION}), 200


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    Get real-time weather for a Kenyan county.

    POST Request JSON:
      - county (str): Name of the Kenyan county
      - all_counties (bool): If true, return weather for all counties

    Response JSON:
      - county/counties with current weather data
    """

    # Helpful message so browser/GET doesn't show 405
    if request.method == "GET":
        return jsonify({
            "message": "Use POST with JSON.",
            "examples": [
                {"county": "Nairobi"},
                {"all_counties": True}
            ]
        }), 200

    try:
        data = request.get_json(silent=False)
        if data is None or not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON body"}), 400

        # Get weather for all counties (warning: can be slow)
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
        county_name = str(data.get("county", "")).strip()
        if not county_name:
            return jsonify({"error": "Provide 'county' or set 'all_counties': true"}), 400

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

    except urllib.error.URLError:
        return jsonify({"error": "Unable to fetch current weather (network/API error)"}), 502
    except BadRequest:
        return jsonify({"error": "Invalid JSON"}), 400
    except Exception as e:
        logger.exception("Unhandled error in /predict: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("FLASK_RUN_PORT", 5000)))
    app.run(host="0.0.0.0", port=port, debug=False)
