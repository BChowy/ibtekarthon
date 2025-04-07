import streamlit as st

# Streamlit app
st.set_page_config(page_title="Is My path Safe?", layout="centered", initial_sidebar_state="collapsed")
st.title("⛰ Is My path Safe?")
    
st.write(
    "There's Nothing to show here yet. Please select a different page from the sidebar.")


# st.subheader("Local Image")
# image_path = "./resources/map.jpg"
 

# try:
#     img = Image.open(image_path)
#     st.image(img, caption="Example of map function", use_column_width=True)
# except FileNotFoundError:
#     st.error(f"Error: Image not found at {image_path}")