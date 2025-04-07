import streamlit as st

st.set_page_config(page_title="Landslide Risk Intelligence", layout="wide", initial_sidebar_state="collapsed")

# Initialize session state variables
if 'navigation' not in st.session_state:
    st.session_state.navigation = None

# ---------- Hero Section ----------
st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem;">
        <h1 style="font-size: 3em; color: white;">Monitor Landslide Risks Earth's
Health Starts Here</h1>
        <p style="font-size: 1.5em; color: white; max-width: 600px; margin: auto;">
            "Get to Know the Earth's Condition Today"</p>
        <p style="font-size: 1.2em; color: #cccccc; max-width: 70dvw; margin: auto;">
            "This project aims to analyze weather factors related to landslides, such as rainfall, temperature, and erosion, to provide accurate risk predictions. The system utilizes an Al model that processes historical data to predict the likelihood of landslides, helping individuals and authorities make effective preventive decisions
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------- Button Section ----------
button_css = """
<style>
.stButton > button {
    width: 100% !important;
    min-height: 80px !important;
    height: 100% !important;
    font-size: 1.1rem !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    align-items: center;
    justify-content: center;
    white-space: normal !important;
    padding: 1rem !important;
    color: white !important;
    margin: 0 !important;
}

.stButton > button:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 4px 20px rgba(255, 76, 76, 0.3) !important;
    opacity: 0.9 !important;
}
</style>
"""

st.markdown(button_css, unsafe_allow_html=True)

# Create buttons in a container
with st.container():
    cols = st.columns(5)
    button_config = [
        ("Dashboard", "dashboard"),
        ("Landslide Risk Prediction", "prediction"),
        ("Is My path Safe?", "map"),
        ("Weather Data trends", "data"),
        ("Today's Weather Impact", "impact")
    ]

    # Create buttons and handle clicks
    for idx, (label, page) in enumerate(button_config):
        with cols[idx % 5]:
            if st.button(label, key=f"btn_{page}"):
                st.session_state.navigation = page

# Handle navigation
nav_mapping = {
    "dashboard": "/Dashboard",
    "prediction": "/Prediction",
    "map": "/Map",
    "data": "/Data",
    "impact": "/Impact"
}

if st.session_state.navigation:
    target_page = nav_mapping.get(st.session_state.navigation)
    if target_page:
        # Reset navigation state before redirecting
        st.session_state.navigation = None
        st.markdown(f'<meta http-equiv="refresh" content="0; url={target_page}">', 
                    unsafe_allow_html=True)