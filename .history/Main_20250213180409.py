import streamlit as st

# Set page config
st.set_page_config(page_title="PPT Generator", page_icon="📊", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Set background image */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?ixlib=rb-1.2.1&auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Style for the main heading with animation */
    .main-heading {
        font-family: 'Playfair Display', serif;
        font-size: 52px;
        font-weight: 800;
        color: #5D4E6D;
        text-align: center;
        margin-top: -25px;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.6);
        animation: fadeIn 1.5s ease-in;
    }
    /* Style for buttons with hover animation */
    .stButton button {
        background-color: #B8A9C6;
        color: #4A4A4A;
        font-family: 'Quicksand', sans-serif;
        font-size: 18px;
        padding: 12px 20px;
        border-radius: 15px;
        border: none;
        width: 80%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(93, 78, 109, 0.15);
    }
    .stButton button:hover {
        background-color: #9B8AA8;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(93, 78, 109, 0.25);
    }
    /* Style for transparent boxes with hover effect */
    .description-box {
        background-color: rgba(255, 248, 250, 0.85);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        color: #5D4E6D;
        font-family: 'Lato', sans-serif;
        font-size: 16px;
        font-weight: 400;
        width: 80%;
        transition: all 0.3s ease;
        animation: slideIn 1s ease-out;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 15px rgba(184, 169, 198, 0.2);
        border: 1px solid rgba(184, 169, 198, 0.2);
    }
    .description-box:hover {
        transform: translateY(-5px);
        background-color: rgba(255, 248, 250, 0.95);
        box-shadow: 0 8px 20px rgba(184, 169, 198, 0.3);
    }
    .description-box h3 {
        font-family: 'Cormorant Garamond', serif;
        color: #816894;
        font-size: 26px;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;800&family=Cormorant+Garamond:wght@600&family=Lato:wght@400;500&family=Quicksand:wght@400;500&display=swap');
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    /* Responsive design */
    @media (max-width: 768px) {
        .main-heading {
            font-size: 36px;
            margin-top: -15px;
        }
        .description-box {
            width: 95%;
            padding: 15px;
        }
        .stButton button {
            width: 95%;
            font-size: 16px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main heading
st.markdown('<div class="main-heading">PPT Generator</div>', unsafe_allow_html=True)

# Add some spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# Create three columns with different widths for better layout
col1, col2, col3 = st.columns([0.2, 1, 0.2])

with col2:
    # First card - Research Paper PPT
    st.markdown(
        '<div class="description-box">'
        '<h3>PPT from Research Paper</h3>'
        '<p>Upload a research paper and generate a professional PowerPoint presentation. Customize the content, layout, and design to suit your needs.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate PPT using Research Paper"):
        st.switch_page("pages/researchpaper_to_ppt.py")

    # Add spacing between cards
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Second card - Voice PPT
    st.markdown(
        '<div class="description-box">'
        '<h3>PPT from Voice</h3>'
        '<p>Record your voice or provide text to create a PowerPoint presentation. Our tool will transcribe and organize your content into slides.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate PPT using Voice"):
        st.switch_page("pages/speech_to_ppt.py")

# Add some CSS to make the layout more dynamic
st.markdown("""
    <style>
    /* Additional layout styles */
    .description-box {
        margin: 0 auto;  /* Center the boxes */
        transform-origin: center;
        opacity: 0;
        animation: fadeSlideIn 0.8s ease-out forwards;
    }
    
    .description-box:nth-child(2) {
        animation-delay: 0.3s;
    }
    
    @keyframes fadeSlideIn {
        0% {
            opacity: 0;
            transform: translateY(30px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Make cards appear side by side on wider screens */
    @media (min-width: 1200px) {
        .description-box {
            width: 90%;
        }
    }
    
    /* Add some depth to the layout */
    .stApp > div:first-child {
        perspective: 1000px;
    }
    
    .description-box:hover {
        transform: translateY(-5px) rotateX(2deg);
    }
    </style>
    """, unsafe_allow_html=True)