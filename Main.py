# Import Streamlit library for creating web applications
import streamlit as st

# Configure the webpage settings
st.set_page_config(
    page_title="PPT Generator",  # Set browser tab title
    page_icon="📊",             # Set browser tab icon
    layout="wide"               # Use wide layout for better space utilization
)

# Define custom CSS styling for the application
st.markdown(
    """
    <style>
    /* Set the main background with a gradient effect */
    .stApp {
        background: linear-gradient(45deg, #f6f9fc 0%, #eef2f7 100%);
        min-height: 100vh;  /* Ensure full viewport height */
    }

    /* Style for main title with animated gradient effect */
    .main-heading {
        font-family: 'Cormorant Garamond', serif;
        font-size: 65px;
        background: linear-gradient(120deg, #2c3e50, #3498db, #2c3e50);
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        animation: gradientText 8s linear infinite;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* Container for card elements with 3D effect */
    .card-container {
        perspective: 1000px;
        padding: 2rem;
        max-width: 1000px;
        margin: 0 auto;
    }

    /* Styling for description boxes */
    .description-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
        animation: cardFloat 1s ease-out forwards;
    }

    /* Add delay to second description box animation */
    .description-box:nth-child(2) {
        animation-delay: 0.3s;
    }

    /* Create animated border effect */
    .description-box::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(120deg, #3498db, #2ecc71, #3498db);
        -webkit-mask: 
            linear-gradient(#fff 0 0) content-box, 
            linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        animation: borderRotate 4s linear infinite;
        background-size: 200% auto;
    }

    /* Style headings within description boxes */
    .description-box h3 {
        font-size: 32px;
        color: #2c3e50;
        margin-bottom: 1rem;
        position: relative;
        display: inline-block;
    }

    /* Add underline animation to headings */
    .description-box h3::after {
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        bottom: -4px;
        left: 0;
        background: linear-gradient(90deg, #3498db, #2ecc71);
        transition: width 0.6s ease;
    }

    /* Animate heading underline on hover */
    .description-box:hover h3::after {
        width: 100%;
    }

    /* Style buttons with gradient and pulse effect */
    .stButton button {
        background: linear-gradient(120deg, #3498db, #2ecc71);
        color: white;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        padding: 12px 30px;
        border-radius: 12px;
        border: none;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        animation: buttonPulse 2s infinite;
    }

    /* Button hover effect */
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(52, 152, 219, 0.3);
        animation: none;
    }

    /* Define animations */
    @keyframes gradientText {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    @keyframes cardFloat {
        0% {
            opacity: 0;
            transform: translateY(40px) rotateX(-10deg);
        }
        100% {
            opacity: 1;
            transform: translateY(0) rotateX(0);
        }
    }

    @keyframes borderRotate {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    @keyframes buttonPulse {
        0% { box-shadow: 0 0 0 0 rgba(52, 152, 219, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(52, 152, 219, 0); }
        100% { box-shadow: 0 0 0 0 rgba(52, 152, 219, 0); }
    }

    /* Add hover effect to description boxes */
    .description-box:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 30px rgba(0,0,0,0.1);
    }

    /* Style and animate description text */
    .description-box p {
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        line-height: 1.6;
        color: #546e7a;
        opacity: 0;
        animation: textFadeIn 0.8s ease-out 0.3s forwards;
    }

    /* Text fade-in animation */
    @keyframes textFadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Responsive design adjustments */
    @media (max-width: 768px) {
        .main-heading { font-size: 40px; }
        .description-box { padding: 1.5rem; }
        .description-box h3 { font-size: 24px; }
    }
    </style>
    """,
    unsafe_allow_html=True,  # Allow HTML/CSS to be rendered
)

# Create main heading
st.markdown('<div class="main-heading">PPT Generator</div>', unsafe_allow_html=True)

# Create two-column layout
col1, col2 = st.columns([1, 1])

# Left column: Research Paper PPT section
with col1:
    # Create description box for research paper option
    st.markdown(
        '<div class="description-box">'
        '<h3>PPT from Research Paper</h3>'
        '<p>Upload a research paper and generate a professional PowerPoint presentation. '
        'Customize the content, layout, and design to suit your needs.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)
    # Add button to navigate to research paper page
    if st.button("Generate PPT using Research Paper"):
        st.switch_page("pages/researchpaper_to_ppt.py")

# Add vertical spacing
st.write("\n\n\n\n\n\n\n\n\n")

# Create two more columns for voice section
col3, col4 = st.columns([1, 1])

# Right column: Voice PPT section
with col4:
    # Create description box for voice option
    st.markdown(
        '<div class="description-box">'
        '<h3>PPT from Voice</h3>'
        '<p>Record your voice or provide text to create a PowerPoint presentation. '
        'Our tool will transcribe and organize your content into slides.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)
    # Add button to navigate to speech page
    if st.button("Generate PPT using Voice"):
        st.switch_page("pages/speech_to_ppt.py")