import streamlit as st
import pandas as pd
import plotly.express as px

# Custom red theme configuration
RED_PALETTE = px.colors.sequential.Reds
DARK_RED = "#8B0000"
ACCENT_RED = "#FF4C4C"
BG_COLOR = "#0e1118"  # Dark background from map view

st.set_page_config(page_title="Landslide Dashboard", layout="wide", initial_sidebar_state="collapsed")
st.title("🌍 Landslide Events Dashboard")

# Apply dark theme from map view
st.markdown(f"""
<style>
    .main {{
        background-color: {BG_COLOR};
        color: white;
    }}
    [data-testid="stMetric"] {{
        background-color: #1a1a1a;
        border-radius: 5px;
        padding: 10px;
    }}
    [data-testid="stMetricLabel"] {{
        color: {ACCENT_RED} !important;
    }}
    [data-testid="stMetricValue"] {{
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)

# Load and prepare data (keep your existing code)
df = pd.read_csv("data/cleaned_landslide_data.csv")
df['event_date'] = pd.to_datetime(df['event_date'])
df['year'] = df['event_date'].dt.year
df = df.assign(
    latitude=pd.to_numeric(df['latitude'], errors='coerce'),
    longitude=pd.to_numeric(df['longitude'], errors='coerce'),
    fatality_count=df['fatality_count'].fillna(0).astype(int),
    injury_count=df['injury_count'].fillna(0).astype(int)
).dropna(subset=['latitude', 'longitude'])

filtered_df = df[
    (df["landslide_category"]).isin(["landslide", "mudslide", "rock_fall"]) &
    (df["landslide_size"]).isin(["small", "medium", "large"]) &
    (df["landslide_trigger"] != "unknown")
]

# Metrics - Simplified and color-matched
col1, col2, col3 = st.columns([2, 2, 1])
with col3:
    st.markdown("### Impact Summary")
    st.metric("Injuries", f"{filtered_df['injury_count'].sum():,}")
    st.metric("Fatalities", f"{filtered_df['fatality_count'].sum():,}")
    
    if st.button("Predictive Analysis", type="primary"):
        st.session_state.go_to_prediction = True

# Charts with map view's red theme
chart_config = {
    "color_discrete_sequence": RED_PALETTE,
    "template": "plotly_dark",
    "labels": {
        "landslide_trigger": "Trigger",
        "landslide_category": "Category",
        "landslide_size": "Size"
    }
}

with col1:
    fig_trigger = px.histogram(
        filtered_df, 
        x="landslide_trigger", 
        title="<b>Trigger Distribution</b>",
        **chart_config
    ).update_layout(
        plot_bgcolor=BG_COLOR,
        paper_bgcolor=BG_COLOR,
        font_color="white"
    )
    st.plotly_chart(fig_trigger, use_container_width=True)

with col2:
    fig_category = px.histogram(
        filtered_df,
        x="landslide_category",
        title="<b>Category Breakdown</b>",
        **chart_config
    ).update_layout(
        plot_bgcolor=BG_COLOR,
        paper_bgcolor=BG_COLOR,
        font_color="white"
    )
    st.plotly_chart(fig_category, use_container_width=True)

# Size vs Trigger chart matching map style
st.markdown("### Event Scale by Trigger")
fig_size_trigger = px.histogram(
    filtered_df,
    x="landslide_size",
    color="landslide_trigger",
    barmode="group",
    color_discrete_sequence=RED_PALETTE,
    template="plotly_dark"
).update_layout(
    plot_bgcolor=BG_COLOR,
    paper_bgcolor=BG_COLOR,
    font_color="white",
    legend=dict(
        bgcolor="#1a1a1a",
        font=dict(color="white")
))
st.plotly_chart(fig_size_trigger, use_container_width=True)

# Navigation handling
if st.session_state.get("go_to_prediction", False):
    st.switch_page("pages/1_Prediction.py")