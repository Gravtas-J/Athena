import streamlit as st
from PIL import Image

icon = Image.open('logo.png')
# Set the initial sidebar state to collapsed
st.session_state.sidebar_state = 'expanded'
st.set_page_config(
    page_title=("General-AI"),
    page_icon=(icon),
    initial_sidebar_state=st.session_state.sidebar_state
)

col1, col2, col3 = st.columns([1, 2, 1])  # creates 3 columns

with col2:  # use the center column
    st.image("logo.png", width=300)  # adjust width to your preference

# Main Title
st.markdown("<h1 style='text-align: center;'>Welcome To General-AI</h1>", unsafe_allow_html=True)


# Main content
st.write("Welcome to Our Project Hub, Home of Mimir and Norna.")
st.write("Embark on an innovative journey through the future of healthcare and discover the vast potential of AI in medical practice with Mimir and Norna.")
st.write("Meet Mimir, an AI Intake chatbot that functions as a sophisticated assistant to medical receptionists. Designed to intelligently assess and prioritize patient cases in real-time, Mimir ensures the right care at the right time.")
st.write("Meanwhile, Norna revolutionizes clinical analysis, meticulously extracting valuable insights from patient chatlogs. This extraordinary tool enables healthcare professionals to deliver personalized care backed by informed decisions.")
st.write("Discover more about Mimir and Norna on our project pages for a detailed understanding of these groundbreaking AI tools.")
st.write("Join us in redefining healthcare, one AI tool at a time.")
