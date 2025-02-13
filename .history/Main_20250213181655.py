import streamlit as st

# Set page config
st.set_page_config(page_title="PPT Generator", page_icon="📊", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Set background and global styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf3 100%);
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Main heading styles */
    .main-heading {
        font-family: 'Cormorant Garamond', serif;
        font-size: 60px;
        font-weight: 600;
        color: #2c3e50;
        text-align: center;
        margin: 2rem 0;
        letter-spacing: 2px;
        animation: fadeIn 1.5s ease-in;
    }

    /* Card container styles */
    .card-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
    }

    /* Description box styles */
    .description-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 2.5rem;
        border-radius: 25px;
        text-align: left;
        width: 100%;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 20px rgba(0, 0, 0, 0.1);
    }

    .description-box h3 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 32px;
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .description-box p {
        font-family: 'Lato', sans-serif;
        font-size: 18px;
        line-height: 1.6;
        color: #596575;
        margin-bottom: 1.5rem;
    }

    /* Button styles */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-family: 'Lato', sans-serif;
        font-size: 16px;
        font-weight: 500;
        padding: 12px 30px;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        width: auto;
        margin-top: 1rem;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    /* Card hover effects */
    .description-box:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 8px 12px rgba(0, 0, 0, 0.05),
            0 15px 25px rgba(0, 0, 0, 0.1);
    }

    /* Decorative elements */
    .description-box::before {
        content: '';
        position: absolute;
        top: -1px;
        left: -1px;
        right: -1px;
        bottom: -1px;
        border-radius: 25px;
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        z-index: -1;
        transition: opacity 0.3s ease;
        opacity: 0;
    }

    .description-box:hover::before {
        opacity: 1;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-heading {
            font-size: 40px;
            margin: 1rem 0;
        }

        .description-box {
            padding: 1.5rem;
        }

        .description-box h3 {
            font-size: 24px;
        }

        .description-box p {
            font-size: 16px;
        }
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
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