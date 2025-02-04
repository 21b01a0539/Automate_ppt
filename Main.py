import streamlit as st
from PIL import Image

# Set the page title and layout
st.set_page_config(page_title="Home", layout="centered")

# Load the background image
background_image = Image.open("background.jpg")  # Replace with your image path

# Custom CSS to set the background image
def set_background_image(image):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Convert the image to base64
import base64
from io import BytesIO

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Set the background image
set_background_image(image_to_base64(background_image))

# Title of the main page with custom styling
st.markdown(
    """
    <style>
    .title {
        font-size: 50px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">Welcome to My Project</div>', unsafe_allow_html=True)

# Custom CSS for buttons
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Button to redirect to Research Paper to PDF
if st.button("Research Paper to PDF"):
    st.session_state.page = "research_paper_to_pdf"
    st.experimental_rerun()

# Button to redirect to Speech to PPT
if st.button("Speech to PPT"):
    st.session_state.page = "speech_to_ppt"
    st.experimental_rerun()

# Redirect logic
if "page" in st.session_state:
    if st.session_state.page == "research_paper_to_pdf":
        st.switch_page("pages/researchpaper_to_ppt.py")
    elif st.session_state.page == "speech_to_ppt":
        st.switch_page("pages/speech_to_ppt.py")