import streamlit as st
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb


# Load model
model = joblib.load("landslide_model.pkl")

# Streamlit app
st.title("🌋 Landslide Risk Prediction")
    
# User input
slope = st.slider("Slope (degrees)", 0, 90, 30)
rainfall = st.slider("Rainfall (mm)", 0, 500, 100)
soil_moisture = st.slider("Soil Moisture (%)", 10, 100, 50)
human_activity = st.selectbox("Human Activity Level", [0, 1, 2], format_func=lambda x: ["Low", "Medium", "High"][x])

# Create feature array
features = np.array([[slope, rainfall, soil_moisture, human_activity, slope * rainfall]])

# Predict
prediction = model.predict(features)[0]
confidence = model.predict_proba(features)[0]

# Output with emoji based on risk level
risk_levels = ["Low", "Medium", "High"]
risk_emojis = ["✅", "⚠️", "🚨"]
st.subheader(f"Landslide Risk: {risk_levels[int(prediction)]} {risk_emojis[int(prediction)]}")
st.write(f"Confidence: {max(confidence) * 100:.2f}%")