import streamlit as st
from components import get_openai_client, parse_slides
from ppt import create_ppt
import speech_recognition as sr
from components import generate_slide_content_general

# Custom CSS with matching aesthetic
st.markdown("""
    <style>
    /* Global styles */
    .stApp {
        background: linear-gradient(45deg, #f6f9fc 0%, #eef2f7 100%);
        min-height: 100vh;
    }

    /* Main title styling */
    .page-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 48px;
        background: linear-gradient(120deg, #2c3e50, #3498db, #2c3e50);
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        animation: gradientText 8s linear infinite;
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
    }

    /* Section styling */
    .section-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        animation: slideIn 0.8s ease-out forwards;
        position: relative;
        overflow: hidden;
    }

    .section-container::after {
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

    /* Button styling */
    .stButton > button {
        background: linear-gradient(120deg, #3498db, #2ecc71);
        color: white;
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        padding: 12px 30px;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(52, 152, 219, 0.3);
    }

    /* Recording button special styling */
    .recording-button {
        background: linear-gradient(120deg, #e74c3c, #c0392b) !important;
        animation: pulse 2s infinite;
    }

    /* Input field styling */
    .stTextInput > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 1px solid rgba(52, 152, 219, 0.2);
        transition: all 0.3s ease;
    }

    .stTextInput > div > div:focus-within {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1rem;
    }

    /* Color picker styling */
    .stColorPicker > label {
        font-family: 'Poppins', sans-serif;
        color: #2c3e50;
    }

    /* Animations */
    @keyframes gradientText {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    @keyframes slideIn {
        0% { 
            opacity: 0;
            transform: translateY(20px);
        }
        100% { 
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes borderRotate {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(231, 76, 60, 0); }
        100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .page-title {
            font-size: 36px;
        }
        .section-container {
            padding: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing data between reruns
if 'combined_text' not in st.session_state:
    st.session_state['combined_text'] = ""
if 'transcribed_text' not in st.session_state:
    st.session_state['transcribed_text'] = ""
if 'final_text' not in st.session_state:
    st.session_state['final_text'] = ""
if 'is_recording' not in st.session_state:
    st.session_state['is_recording'] = False
if 'audio_recorder' not in st.session_state:
    st.session_state['audio_recorder'] = sr.Recognizer()

def start_listening():
    """Listen continuously until user stops speaking"""
    st.session_state['is_recording'] = True
    st.session_state['transcribed_text'] = ""

    with sr.Microphone() as source:
        st.session_state['audio_recorder'].adjust_for_ambient_noise(source)
        st.info("🎙 Listening... Speak now.")

        try:
            audio = st.session_state['audio_recorder'].listen(source, timeout=10, phrase_time_limit=15)
            recognized_text = st.session_state['audio_recorder'].recognize_google(audio)
            st.session_state['transcribed_text'] = recognized_text
            st.session_state['topic_input'] = recognized_text
        except sr.UnknownValueError:
            st.warning("Couldn't understand the speech. Please try again.")
        except sr.RequestError as e:
            st.error(f"Speech recognition request failed: {e}")
        except Exception as e:
            st.error(f"Error accessing microphone: {e}")
        finally:
            st.session_state['is_recording'] = False

# Main title
st.markdown('<h1 class="page-title">Speech to Presentation Generator</h1>', unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.header("How to Use")
    st.markdown("""
    1. *Record Live Speech* - Click the microphone button and speak
    2. *Review Text* - Check and edit the transcribed text
    3. *Customize Design* - Select colors and fonts
    4. *Generate* - Create your presentation
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Main content sections
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.subheader("Voice Input")
col1, col2 = st.columns([5, 1])

with col1:
    topic = st.text_input(
        "Presentation Topic:",
        placeholder="e.g., Artificial Intelligence in Healthcare",
        key="topic_input"
    )

with col2:
    if st.session_state.get('is_recording', False):
        button_class = "recording-button"
        if st.button("🔴 Stop", key="stop_mic", help="Stop recording"):
            st.session_state['is_recording'] = False
    else:
        button_class = ""
        if st.button("🎤 Record", key="start_mic", help="Start recording", on_click=start_listening):
            pass
st.markdown('</div>', unsafe_allow_html=True)

# Slide structure section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.subheader("Slide Structure")
slide_titles_input = st.text_area(
    "Enter slide titles (one per line):",
    placeholder="Title Slide\nIntroduction\nKey Points\nConclusion",
    key="slide_titles"
)
st.markdown('</div>', unsafe_allow_html=True)

# Design customization section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.subheader("Design Customization")
col3, col4, col5 = st.columns(3)

with col3:
    heading_color = st.color_picker("Heading Color", "#2c3e50", key="heading_color")
    content_color = st.color_picker("Content Color", "#34495e", key="content_color")

with col4:
    heading_font = st.selectbox(
        "Heading Font",
        ["Cormorant Garamond", "Playfair Display", "Montserrat", "Poppins"],
        key="heading_font"
    )
    heading_size = st.slider("Heading Size", 24, 48, 36, key="heading_size")

with col5:
    content_font = st.selectbox(
        "Content Font",
        ["Poppins", "Lato", "Open Sans", "Roboto"],
        key="content_font"
    )
    content_size = st.slider("Content Size", 14, 28, 18, key="content_size")
st.markdown('</div>', unsafe_allow_html=True)

# Generate button section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
if st.button("✨ Generate Presentation", key="generate_btn"):
    client = get_openai_client()
    if not client:
        st.warning("Please enter a valid OpenAI API Key")
    else:
        with st.spinner('Processing your presentation...'):
            slide_contents = generate_slide_content_general(client, topic, "3", slide_titles_input.split("\n"))
            text = parse_slides(slide_contents)
            st.text_area("Slide Contents:", slide_contents, height=200, key="slide_contents")
            pptx_file = create_ppt(text, heading_color, heading_size, content_color, content_size, heading_font, content_font)
            st.download_button(
                label="Download Presentation",
                data=pptx_file,
                file_name="generated_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key="download_btn"
            )
            st.success("Presentation generated successfully!")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; font-family: "Poppins", sans-serif; 
    margin-top: 2rem; animation: fadeIn 1s ease-in;'>
        Created with ❤️ for seamless presentations
    </div>
""", unsafe_allow_html=True)