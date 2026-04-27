from flask import Flask, request, jsonify
import random

app = Flask(__name__)

WEATHER = ["sunny", "cloudy", "rainy", "stormy", "snowy"]

@app.route("/predict", methods=["POST"])
def predict():
    city = request.json.get("city", "")
    prediction = random.choice(WEATHER)
    return jsonify({"city": city, "prediction": prediction})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
