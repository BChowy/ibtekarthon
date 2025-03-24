import streamlit as st
import joblib
import numpy as np

# Load your model
@st.cache_resource
def load_model():
    return joblib.load('best_model.pkl')  # Replace with your model

model = load_model()

# Title
st.title("🌋 Real-Time Landslide Risk Prediction")
st.markdown("Predict landslide probability using terrain and weather factors")

# Input widgets
slope = st.slider("Slope Angle (degrees)", 0, 45, 25)
rainfall = st.slider("7-Day Rainfall (mm)", 0, 300, 150)
soil_moisture = st.slider("Soil Moisture Index", 0.0, 1.0, 0.6)
human_activity = st.selectbox("Human Activity Nearby", ["No", "Yes"])
human_activity_bin = 1 if human_activity == "Yes" else 0

# Prediction logic
if st.button("Predict Risk"):
    # Format input as a 2D numpy array
    input_array = np.array([[slope, rainfall, soil_moisture, human_activity_bin]])
    
    # Predict
    try:
        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0][1]
        
        # Display results
        st.success(f"Predicted Risk: {probability*100:.1f}%")
        st.progress(probability)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
