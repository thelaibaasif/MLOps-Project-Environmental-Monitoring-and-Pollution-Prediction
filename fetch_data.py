import os
import requests
import json
from datetime import datetime

# Define constants
API_KEY = "2fbc453063630496c3ab531f5de7535f"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
DATA_DIR = "data"

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_air_pollution_data(lat, lon):
    print("Fetching data...")  # Debug log
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        print(f"Response status code: {response.status_code}")  # Debug log
        if response.status_code == 200:
            data = response.json()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(DATA_DIR, f"environmental_data_{timestamp}.json")
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Data saved to {filename}")
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Script started...")  # Debug log
    fetch_air_pollution_data(lat=40.7128, lon=-74.0060)  # Example: New York City
    print("Script finished.")  # Debug log
