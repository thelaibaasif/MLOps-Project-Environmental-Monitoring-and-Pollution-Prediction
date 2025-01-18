import requests

try:
    response = requests.get("http://localhost:5000/metrics")
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
except Exception as e:
    print("Error:", e)
