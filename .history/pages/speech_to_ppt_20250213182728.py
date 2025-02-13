import streamlit as st
from components import get_openai_client, parse_slides
from ppt import create_ppt
import speech_recognition as sr
from components import generate_slide_content_general

# Custom CSS for better styling and animations
st.markdown("""
    <style>
    /* Modern clean background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
    }

    /* Custom container for content */
    .content-wrapper {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    /* Elegant title styling */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        color: #1a237e;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        opacity: 0;
        animation: fadeInDown 1s forwards;
    }

    /* Modern card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.05),
            0 10px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        opacity: 0;
        animation: slideUp 0.6s forwards;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 8px 12px rgba(0, 0, 0, 0.05),
            0 15px 25px rgba(0, 0, 0, 0.1);
    }

    /* Section headers */
    .section-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.5rem;
        color: #1a237e;
        margin-bottom: 1.5rem;
        font-weight: 600;
        position: relative;
        padding-left: 1rem;
    }

    .section-title::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        height: 70%;
        width: 4px;
        background: linear-gradient(to bottom, #1a237e, #7986cb);
        border-radius: 2px;
    }

    /* Modern button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(26, 35, 126, 0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(26, 35, 126, 0.3);
    }

    /* Recording button */
    .recording-active {
        background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%) !important;
        animation: pulseRecord 2s infinite;
    }

    /* Input field styling */
    .stTextInput > div > div {
        background: white;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div:focus-within {
        border-color: #1a237e;
        box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1);
    }

    /* Textarea styling */
    .stTextArea > div > div {
        background: white;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }

    .stTextArea > div > div:focus-within {
        border-color: #1a237e;
        box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1);
    }

    /* Color picker styling */
    .stColorPicker > div > div {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulseRecord {
        0% { box-shadow: 0 0 0 0 rgba(211, 47, 47, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(211, 47, 47, 0); }
        100% { box-shadow: 0 0 0 0 rgba(211, 47, 47, 0); }
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .glass-card {
            padding: 1.5rem;
        }
        .section-title {
            font-size: 1.25rem;
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
st.markdown('<h1 class="main-title">Speech to Presentation</h1>', unsafe_allow_html=True)

# Voice Input Section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Voice Input</h2>', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])

with col1:
    topic = st.text_input(
        "What's your presentation about?",
        placeholder="e.g., The Future of Artificial Intelligence",
        key="topic_input"
    )

with col2:
    if st.session_state.get('is_recording', False):
        if st.button("🔴 Stop", key="stop_mic", help="Stop recording"):
            st.session_state['is_recording'] = False
    else:
        if st.button("🎤 Start", key="start_mic", help="Start recording", on_click=start_listening):
            pass
st.markdown('</div>', unsafe_allow_html=True)

# Slide Structure Section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Slide Structure</h2>', unsafe_allow_html=True)
slide_titles_input = st.text_area(
    "Enter your slide titles",
    placeholder="Introduction\nKey Points\nMethodology\nConclusion",
    key="slide_titles",
    height=150
)
st.markdown('</div>', unsafe_allow_html=True)

# Design Section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Design Customization</h2>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("##### Colors")
    heading_color = st.color_picker("Heading", "#1a237e", key="heading_color")
    content_color = st.color_picker("Content", "#333333", key="content_color")

with col4:
    st.markdown("##### Heading Style")
    heading_font = st.selectbox(
        "Font Family",
        ["Playfair Display", "Montserrat", "Roboto", "Open Sans"],
        key="heading_font"
    )
    heading_size = st.slider("Size", 24, 48, 36, key="heading_size")

with col5:
    st.markdown("##### Content Style")
    content_font = st.selectbox(
        "Font Family",
        ["Open Sans", "Roboto", "Lato", "Montserrat"],
        key="content_font"
    )
    content_size = st.slider("Size", 14, 28, 18, key="content_size")
st.markdown('</div>', unsafe_allow_html=True)

# Generate Button Section
st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
if st.button("Generate Presentation ✨", key="generate_btn"):
    client = get_openai_client()
    if not client:
        st.warning("Please enter a valid OpenAI API Key")
    else:
        with st.spinner('Processing your presentation...'):
            slide_contents = generate_slide_content_general(client, topic, "3", slide_titles_input.split("\n"))
            text = parse_slides(slide_contents)
            st.text_area("Slide Contents:", slide_contents, height=200, key="slide_contents")
            pptx_file = create_ppt(text, tuple(int(heading_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)), heading_size, tuple(int(content_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)), content_size, heading_font, content_font)
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
    <div style='text-align: center; color: #666; padding: 2rem; font-family: "Montserrat", sans-serif;'>
        Made with 💫 for effortless presentations
    </div>
""", unsafe_allow_html=True)