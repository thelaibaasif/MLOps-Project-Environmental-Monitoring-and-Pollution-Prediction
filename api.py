from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from prometheus_flask_exporter import PrometheusMetrics
import numpy as np
import requests
import pickle

# Initialize Flask app
app = Flask(__name__)

# Integrate Prometheus metrics
metrics = PrometheusMetrics(app)

# Expose default Prometheus metrics at `/metrics`
metrics.info('app_info', 'Application Info', version='1.0.0')

# Load the trained model
model = load_model("best_model.h5")
print(f"Model loaded successfully with input shape: {model.input_shape}")

# Load the updated scaler
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
    print(f"Scaler loaded successfully with expected features: {scaler.n_features_in_}")

# Define the `/predict` route for batch predictions
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate input structure
        if "list" not in data:
            return jsonify({"error": "Missing 'list' field in input data"}), 400

        # Extract features (temperature, humidity, pressure, wind speed, and cloud cover)
        features = []
        for item in data["list"]:
            try:
                temp = item["main"]["temp"]
                humidity = item["main"]["humidity"]
                pressure = item["main"]["pressure"]
                wind_speed = item["wind"]["speed"]
                cloud_cover = item.get("clouds", {}).get("all", 0)  # Default to 0 if missing
                features.append([temp, humidity, pressure, wind_speed, cloud_cover])
            except KeyError as e:
                return jsonify({"error": f"Missing key in input data: {e}"}), 400

        # Convert to NumPy array and preprocess
        features = np.array(features)
        print(f"Extracted features: {features}")
        print(f"Feature array shape: {features.shape}")

        # Validate scaler input dimensions
        if features.shape[1] != scaler.n_features_in_:
            return jsonify({"error": f"Input features do not match scaler dimensions. "
                                     f"Expected {scaler.n_features_in_} features, got {features.shape[1]}"}), 400

        # Scale the features
        scaled_features = scaler.transform(features)
        print(f"Scaled features shape: {scaled_features.shape}")

        # Reshape for LSTM input
        look_back = model.input_shape[1]
        if len(scaled_features) < look_back:
            return jsonify({"error": f"Not enough data points for prediction. Requires at least {look_back} data points."}), 400
        reshaped_input = scaled_features[-look_back:].reshape(1, look_back, -1)
        print(f"Reshaped input shape: {reshaped_input.shape}")

        # Make prediction
        prediction = model.predict(reshaped_input)
        print(f"Raw prediction: {prediction}")

        # Return prediction
        return jsonify({"prediction": float(prediction[0, 0])})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 400

# Define the `/live_predict` route for fetching live data and making predictions
@app.route("/live_predict", methods=["GET"])
def live_predict():
    try:
        # Fetch live weather data from OpenWeatherMap API
        api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
        city = "London"  # Replace with desired city
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch live data"}), 500

        # Parse response
        data = response.json()
        main = data["main"]
        wind = data["wind"]
        clouds = data.get("clouds", {"all": 0})  # Use 0 if "clouds" key is missing
        features = [[main["temp"], main["humidity"], main["pressure"], wind["speed"], clouds["all"]]]

        # Validate scaler input dimensions
        features = np.array(features)
        if features.shape[1] != scaler.n_features_in_:
            return jsonify({"error": "Live data format does not match the expected dimensions"}), 400

        # Preprocess features and make prediction
        scaled_features = scaler.transform(features)
        look_back = model.input_shape[1]
        if len(scaled_features) < look_back:
            return jsonify({"error": f"Not enough live data points for prediction. Requires at least {look_back} data points."}), 400
        reshaped_input = scaled_features[-look_back:].reshape(1, look_back, -1)
        prediction = model.predict(reshaped_input)

        # Return prediction
        return jsonify({"prediction": float(prediction[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
