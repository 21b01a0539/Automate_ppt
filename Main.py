import streamlit as st

# Set page config
st.set_page_config(page_title="PPT Generator", page_icon="📊", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Set background image */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1952&q=80');
        background-size: cover;
        background-position: center;
    }
    /* Style for the main heading */
    .main-heading {
        font-size: 48px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-top: -25px;
        text-shadow: 2px 2px 4px #000000;
    }
    /* Style for buttons */
    .stButton button {
        background-color: orange;
        color: white;
        font-size: 18px;
        padding: 12px 20px;
        border-radius: 8px;
        border: none;
        width: 80%;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    /* Style for transparent boxes */
    .description-box {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: #333333;
        font-size: 16px;
        font-weight: bold;
        width: 80%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main heading
st.markdown('<div class="main-heading">PPT Generator</div>', unsafe_allow_html=True)

# Top-left section for Research Paper PPT
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(
        '<div class="description-box">'
        '<h3>PPT from Research Paper</h3>'
        '<p>Upload a research paper and generate a professional PowerPoint presentation. Customize the content, layout, and design to suit your needs.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)  # Adding space before the button
    if st.button("Generate PPT using Research Paper"):
        st.switch_page("pages/researchpaper_to_ppt.py")  # Ensure correct lowercase filename

# Empty space to push the next section to the bottom
st.write("\n\n\n\n\n\n\n\n\n")

# Bottom-right section for Voice PPT
col3, col4 = st.columns([1, 1])

with col4:
    st.markdown(
        '<div class="description-box">'
        '<h3>PPT from Voice</h3>'
        '<p>Record your voice or provide text to create a PowerPoint presentation. Our tool will transcribe and organize your content into slides.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)  # Adding space before the button
    if st.button("Generate PPT using Voice"):
        st.switch_page("pages/speech_to_ppt.py")