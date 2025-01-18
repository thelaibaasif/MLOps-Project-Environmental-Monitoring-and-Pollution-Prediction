import requests

# API endpoint
url = "http://127.0.0.1:5000/predict"

# Sample input data (with cloud cover included)
input_data = {
    "list": [
        {"main": {"temp": 298.15, "humidity": 65, "pressure": 1013}, "wind": {"speed": 3.1}, "clouds": {"all": 10}},
        {"main": {"temp": 297.85, "humidity": 70, "pressure": 1012}, "wind": {"speed": 3.6}, "clouds": {"all": 20}},
        {"main": {"temp": 296.55, "humidity": 75, "pressure": 1011}, "wind": {"speed": 2.9}, "clouds": {"all": 15}},
        {"main": {"temp": 295.15, "humidity": 80, "pressure": 1010}, "wind": {"speed": 3.0}, "clouds": {"all": 25}},
        {"main": {"temp": 294.85, "humidity": 78, "pressure": 1009}, "wind": {"speed": 2.5}, "clouds": {"all": 30}},
    ]
}

try:
    # Send POST request to the API
    response = requests.post(url, json=input_data)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    print("Prediction response:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
