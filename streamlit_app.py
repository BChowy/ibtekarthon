# streamlit_app.py
# import streamlit as st
# import joblib
# import numpy as np

# @st.cache_resource
# def load_model():
#     return joblib.load("landslide_model.pkl")

# model = load_model()

# st.title("🌋 Landslide Risk Predictor")
# st.markdown("Predict risk using terrain/weather factors")

# col1, col2 = st.columns(2)
# with col1:
#     slope = st.slider("Slope Angle (°)", 0, 45, 25)
#     rainfall = st.slider("7-Day Rainfall (mm)", 0, 300, 150)
# with col2:
#     soil = st.slider("Soil Moisture", 0.0, 1.0, 0.6)
#     human_activity = st.selectbox("Human Activity Nearby", ["No", "Yes"])

# human_activity_bin = 1 if human_activity == "Yes" else 0

# # Inside your Streamlit prediction button logic:
# if st.button("Predict Risk"):
#     input_data = np.array([[slope, rainfall, soil, human_activity_bin]])
    
#     try:
#         # Get prediction and confidence
#         prediction = model.predict(input_data)[0]  # 0 or 1
#         proba = model.predict_proba(input_data)[0][prediction]  # Confidence for the predicted class
#         confidence = proba * 100
        
#         # Determine message
#         if prediction == 1:
#             risk_message = f"🚨 Landslide Predicted! (Confidence: {confidence:.1f}%)"
#             color = "#000000"
#         else:
#             risk_message = f"✅ Safe Zone (Confidence: {confidence:.1f}%)"
#             color = "#000000"
        
#         # Display
#         st.markdown(f"""
#         <div style='background-color:{color}; padding:20px; border-radius:10px;'>
#             <h3 style='text-align:center;'>{risk_message}</h3>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Progress bar for visual emphasis
#         st.progress(int(confidence))
        
#     except Exception as e:
#         st.error(f"Error: {str(e)}")

import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("landslide_model.pkl")

# Streamlit app
st.title("Landslide Risk Prediction")

# User input
slope = st.slider("Slope (degrees)", 0, 90, 30)
rainfall = st.slider("Rainfall (mm)", 0, 500, 100)
soil_moisture = st.slider("Soil Moisture (%)", 10, 100, 50)
human_activity = st.radio("Human Activity Level", [0, 1, 2], format_func=lambda x: ["Low", "Medium", "High"][x])

# Create feature array
features = np.array([[slope, rainfall, soil_moisture, human_activity, slope * rainfall]])

# Predict
prediction = model.predict(features)[0]
confidence = model.predict_proba(features)[0]

# Output
risk_levels = ["Low", "Medium", "High"]
st.subheader(f"Landslide Risk: {risk_levels[int(prediction)]}")
st.write(f"Confidence: {max(confidence) * 100:.2f}%")
