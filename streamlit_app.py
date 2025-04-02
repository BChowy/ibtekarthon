import streamlit as st
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns  # Add this import


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

booster = model.get_booster()
importance = booster.get_score(importance_type="weight")

# Sort features by importance
sorted_importance = dict(sorted(importance.items(), key=lambda item: item[1]))

# Set style
plt.style.use('ggplot')  # Modern seaborn style name
plt.rcParams['font.family'] = 'DejaVu Sans'

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))
colors = plt.cm.viridis_r(np.linspace(0.2, 0.8, len(sorted_importance)))

# Plot horizontal bars
bars = ax.barh(list(sorted_importance.keys()), 
               list(sorted_importance.values()), 
               color=colors,
               edgecolor='black',
               linewidth=0.5,
               alpha=0.8)

# Add value labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.005*max(sorted_importance.values()),
            bar.get_y() + bar.get_height()/2,
            f'{width:.2f}',
            va='center',
            ha='left',
            fontsize=9)

# Styling
ax.set_xlabel("Feature Importance Score", fontsize=12, labelpad=10)
ax.set_title("Landslide Prediction Feature Importance\n", 
             fontsize=16, fontweight='bold', pad=20)
ax.xaxis.set_tick_params(labelsize=10)
ax.yaxis.set_tick_params(labelsize=10)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='x', linestyle='--', alpha=0.7)

# Add color bar for visual scale
sm = plt.cm.ScalarMappable(cmap='viridis_r', 
                         norm=plt.Normalize(vmin=0, vmax=max(sorted_importance.values())))
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.5)
cbar.set_label('Importance Magnitude', rotation=270, labelpad=15)

plt.tight_layout()
st.pyplot(fig)
