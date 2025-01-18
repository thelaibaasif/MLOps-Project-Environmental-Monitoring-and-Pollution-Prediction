from sklearn.preprocessing import MinMaxScaler
import pickle
import numpy as np

# Example training data with 5 features (temperature, humidity, pressure, wind speed, cloud cover)
data = np.array([
    [298.15, 65, 1013, 3.1, 10],
    [297.85, 70, 1012, 3.6, 20],
    [296.55, 75, 1011, 2.9, 15],
    [295.15, 80, 1010, 3.0, 25],
    [294.85, 78, 1009, 2.5, 30],
])

# Fit scaler on all features
scaler = MinMaxScaler()
scaler.fit(data)

# Save the updated scaler
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Scaler retrained and saved successfully.")
