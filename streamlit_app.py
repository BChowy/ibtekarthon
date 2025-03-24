# streamlit_app.py
import streamlit as st
import joblib
import numpy as np

@st.cache_resource
def load_model():
    return joblib.load("landslide_model.pkl")

model = load_model()

st.title("🌋 Landslide Risk Predictor")
st.markdown("Predict risk using terrain/weather factors")

col1, col2 = st.columns(2)
with col1:
    slope = st.slider("Slope Angle (°)", 0, 45, 25)
    rainfall = st.slider("7-Day Rainfall (mm)", 0, 300, 150)
with col2:
    soil = st.slider("Soil Moisture", 0.0, 1.0, 0.6)
    human_activity = st.selectbox("Human Activity Nearby", ["No", "Yes"])

human_activity_bin = 1 if human_activity == "Yes" else 0

if st.button("Predict Risk"):
    input_data = np.array([[slope, rainfall, soil, human_activity_bin]])
    
    try:
        proba = model.predict_proba(input_data)[0][1]
        risk_percent = proba * 100
        
        if risk_percent > 70:
            color = "#ff0000"
            emoji = "🚨 HIGH RISK!"
        elif risk_percent > 50:
            color = "#ffd700"
            emoji = "⚠️ Moderate Risk"
        else:
            color = "#00ff00"
            emoji = "✅ Low Risk"
        
        st.markdown(f"""
        <div style='background-color:{color}; padding:20px; border-radius:10px;'>
            <h3 style='text-align:center;'>{emoji}</h3>
            <p style='text-align:center; font-size:24px;'>{risk_percent:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")
