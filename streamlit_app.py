# landslide_app.py (simplified)
import streamlit as st
import joblib
import numpy as np

# Simple model (replace with your trained model)
class HackathonModel:
    def predict(self, X):
        return np.where(
            (X[:,0] > 25) &  # Slope
            (X[:,1] > 150) &  # Rainfall
            (X[:,2] > 0.6),  # Soil moisture
            1, 0
        )

# Load model
model = HackathonModel()

# Streamlit UI
st.title("🌋 Landslide Risk Predictor")
slope = st.slider("Slope", 0, 45, 25)
rainfall = st.slider("Rainfall", 0, 300, 150)
soil_moisture = st.slider("Soil Moisture", 0.0, 1.0, 0.6)

if st.button("Predict"):
    input_data = [[slope, rainfall, soil_moisture]]
    prediction = model.predict(input_data)
    st.write("Landslide Risk: ", "High 🔴" if prediction[0] else "Low 🟢")
