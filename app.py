"""
Weather Predictor API
A simple Flask application that provides weather predictions.
"""

from flask import Flask, request, jsonify
import random
import logging
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEATHER_CONDITIONS = ["sunny", "cloudy", "rainy", "stormy", "snowy"]


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict weather for a given city.
    
    Request JSON:
        - city (str): Name of the city
    
    Response JSON:
        - city (str): The city name
        - prediction (str): Weather prediction
    """
    try:
        data = request.get_json()
        if data is None or not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON"}), 400
        
        if "city" not in data:
            return jsonify({"error": "City name is required"}), 400
            
        city = data.get("city", "").strip()
        if not city:
            return jsonify({"error": "City name is required"}), 400
        
        prediction = random.choice(WEATHER_CONDITIONS)
        logger.info(f"Prediction for {city}: {prediction}")
        
        return jsonify({
            "city": city,
            "prediction": prediction
        }), 200
    
    except BadRequest as e:
        logger.error(f"Bad request in predict endpoint: {str(e)}")
        return jsonify({"error": "Invalid JSON"}), 400
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
