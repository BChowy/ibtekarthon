import streamlit as st
import joblib
import numpy as np


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

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize

booster = model.get_booster()
importance = booster.get_score(importance_type="weight")
features = list(importance.keys())
scores = list(importance.values())

n = len(features)
theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
width = 2 * np.pi / n

# Create different red shades using Reds colormap
reds = cm.get_cmap('Reds')
colors = reds(np.linspace(0.3, 0.9, n))

# Set dark background and white foreground
plt.style.use('dark_background')
fig = plt.figure(facecolor="#0e1118")
ax = fig.add_subplot(111, projection='polar', facecolor="#0e1118")

# Create bars with different red shades
bars = ax.bar(theta, scores, width=width, color=colors, 
             align='edge', edgecolor='white', linewidth=0.8)

# Adjust polar plot settings
ax.set_theta_offset(np.pi/2)
ax.set_theta_direction(-1)
ax.set_ylim(0, max(scores)*1.1)

# Customize labels and ticks (white color)
ax.set_xticks(theta + width/2)
ax.set_xticklabels(features, fontsize=8, color="white")
ax.tick_params(axis='y', colors='white')
ax.yaxis.grid(True, color="white", linestyle='--', alpha=0.4)

# Set title with white color
ax.set_title("Feature Importance in Landslide Prediction", 
            pad=20, color="white", fontweight='bold')

# Rotate labels and set white color
for label, angle in zip(ax.get_xticklabels(), np.degrees(theta + width/2)):
    if angle > 90:
        angle -= 180
    elif angle < -90:
        angle += 180
    label.set_rotation(angle)
    label.set_color("white")
    label.set_horizontalalignment('center' if -90 <= angle <= 90 else 'right')

# Create colorbar with white text
sm = plt.cm.ScalarMappable(cmap=reds, norm=Normalize(vmin=0, vmax=max(scores)))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, pad=0.1)
cbar.set_label('Importance Score', rotation=270, labelpad=15, color="white")
cbar.ax.yaxis.set_tick_params(color="white")
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color="white")

# Set spine color (for radial grid)
ax.spines['polar'].set_color('white')

st.pyplot(fig)