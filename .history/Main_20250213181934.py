import streamlit as st

# Set page config
st.set_page_config(page_title="PPT Generator", page_icon="📊", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Set background and global styles */
    .stApp {
        background: linear-gradient(45deg, #f6f9fc 0%, #eef2f7 100%);
        min-height: 100vh;
    }

    /* Main heading with animated gradient */
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

    /* Card container with perspective */
    .card-container {
        perspective: 1000px;
        padding: 2rem;
        max-width: 1000px;
        margin: 0 auto;
    }

    /* Enhanced description box */
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

    .description-box:nth-child(2) {
        animation-delay: 0.3s;
    }

    /* Animated border effect */
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

    /* Heading styles with animation */
    .description-box h3 {
        font-size: 32px;
        color: #2c3e50;
        margin-bottom: 1rem;
        position: relative;
        display: inline-block;
    }

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

    .description-box:hover h3::after {
        width: 100%;
    }

    /* Button styles with pulse effect */
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

    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(52, 152, 219, 0.3);
        animation: none;
    }

    /* Animations */
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

    /* Hover effects */
    .description-box:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 30px rgba(0,0,0,0.1);
    }

    /* Card content animation */
    .description-box p {
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        line-height: 1.6;
        color: #546e7a;
        opacity: 0;
        animation: textFadeIn 0.8s ease-out 0.3s forwards;
    }

    @keyframes textFadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-heading { font-size: 40px; }
        .description-box { padding: 1.5rem; }
        .description-box h3 { font-size: 24px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main content
st.markdown('<div class="main-heading">Presentation Generator</div>', unsafe_allow_html=True)

# Container for cards
st.markdown('<div class="card-container">', unsafe_allow_html=True)

# First card
st.markdown(
    '<div class="description-box">'
    '<h3>Research Paper to Presentation</h3>'
    '<p>Transform your academic papers into engaging presentations automatically. Our AI-powered tool analyzes your research and creates professional slides with key insights.</p>'
    '</div>',
    unsafe_allow_html=True,
)
if st.button("Create from Research Paper"):
    st.switch_page("pages/researchpaper_to_ppt.py")

# Second card
st.markdown(
    '<div class="description-box">'
    '<h3>Voice to Presentation</h3>'
    '<p>Convert your spoken ideas into polished presentations. Simply record or upload your voice, and watch as it transforms into organized, visually appealing slides.</p>'
    '</div>',
    unsafe_allow_html=True,
)
if st.button("Create from Voice"):
    st.switch_page("pages/speech_to_ppt.py")

st.markdown('</div>', unsafe_allow_html=True)