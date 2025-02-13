import streamlit as st
from components import get_openai_client, parse_slides
from ppt import create_ppt
import speech_recognition as sr
from components import generate_slide_content_general

# Custom CSS for better styling and animations
st.markdown("""
    <style>
    /* Modern clean styling */
    .stApp {
        background: linear-gradient(135deg, #EEF2FF 0%, #E6E9F5 100%);
    }

    /* Title styling */
    h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        background: linear-gradient(120deg, #2B3A67, #4E6E81);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-align: center;
        margin: 2rem 0;
        animation: fadeIn 1s ease-out;
    }

    /* Subheader styling */
    h2, h3, .subheader {
        font-family: 'Montserrat', sans-serif;
        color: #2B3A67;
        margin: 1rem 0;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
    }

    /* Input container styling */
    .stTextInput > div, .stTextArea > div {
        background: white;
        border-radius: 12px;
        padding: 0.5rem;
        border: 2px solid #E6E9F5;
        box-shadow: 0 4px 6px rgba(43, 58, 103, 0.1);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }

    .stTextInput > div:focus-within, .stTextArea > div:focus-within {
        border-color: #2B3A67;
        box-shadow: 0 8px 12px rgba(43, 58, 103, 0.15);
        transform: translateY(-2px);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2B3A67 0%, #4E6E81 100%);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 10px;
        border: none;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(43, 58, 103, 0.2);
        animation: fadeIn 0.5s ease-out;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(43, 58, 103, 0.25);
        background: linear-gradient(135deg, #4E6E81 0%, #2B3A67 100%);
    }

    /* Recording button special styling */
    button[data-testid="baseButton-secondary"] {
        background: linear-gradient(135deg, #FF6B6B 0%, #EE5253 100%);
        animation: pulse 2s infinite;
    }

    /* Select box styling */
    .stSelectbox > div > div {
        background: white;
        border-radius: 10px;
        border: 2px solid #E6E9F5;
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:hover {
        border-color: #2B3A67;
    }

    /* Slider styling */
    .stSlider > div > div {
        background-color: #E6E9F5;
    }

    .stSlider > div > div > div {
        background-color: #2B3A67;
    }

    /* Color picker styling */
    .stColorPicker > div > div {
        border-radius: 10px;
        overflow: hidden;
        border: 2px solid #E6E9F5;
    }

    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(238, 82, 83, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(238, 82, 83, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(238, 82, 83, 0);
        }
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.5rem;
        }
        .stButton > button {
            width: 100%;
            padding: 0.8rem;
        }
    }

    /* Remove empty spaces */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1000px;
        margin: 0 auto;
    }

    .stMarkdown {
        margin-bottom: 0.5rem;
    }

    /* Add subtle dividers between sections */
    .element-container {
        border-bottom: 1px solid rgba(43, 58, 103, 0.1);
        padding: 1rem 0;
    }

    .element-container:last-child {
        border-bottom: none;
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

# Main title with description
st.title("Live Speech to Presentation Generator")
st.markdown("""
    Transform your live speech into professional presentation slides easily!
    Follow the steps below to generate your customized presentation.
""")

# Sidebar with instructions
with st.sidebar:
    st.header("How to Use")
    st.markdown("""
    1. *Record Live Speech* - Click the "Start Recording" button and speak into your microphone.
    2. *Select Slide Sections* - Choose which sections to include in your presentation.
    3. *Customize Design* - Pick colors and fonts for your slides.
    4. *Generate* - Click submit to create your presentation.
    """)

# UI for Voice Input
st.header("Enter Presentation Topic")
col1, col2 = st.columns([5, 1])

with col1:
    topic = st.text_input(
        "Enter the topic of your presentation:",
        placeholder="e.g., Artificial Intelligence in Healthcare",
        key="topic_input"
    )

with col2:
    if st.session_state.get('is_recording', False):
        if st.button("🔴 Stop Recording", key="stop_mic"):
            st.session_state['is_recording'] = False
    else:
        if st.button("🎤 Start Voice Input", key="start_mic", on_click=start_listening):
            pass

if st.session_state.get('transcribed_text', ""):
    st.markdown(f"*Recognized Text:* {st.session_state['transcribed_text']}")

# Slide structure selection with unique key
st.header("Enter Slide Titles")
st.write("You can specify the slides you need for your presentation by listing their titles below.")

slide_titles_input = st.text_area(
    "Enter the titles of your slides, one per line:",
    placeholder="e.g., Title Slide\nIntroduction\nMethodology\nResults\nConclusion",
    key="slide_titles"
)

if slide_titles_input.strip():
    slide_titles = [title.strip() for title in slide_titles_input.split("\n") if title.strip()]
    st.write("### Selected Slide Titles:")
    for i, title in enumerate(slide_titles, 1):
        st.write(f"{i}. {title}")
else:
    st.write("No slide titles entered yet.")

# Design customization with unique keys
st.header("Customize Design")
col3, col4, col5 = st.columns(3)

with col3:
    st.subheader("Color Scheme")
    heading_color = st.color_picker("Heading Color", "#2E4057", key="heading_color")
    content_color = st.color_picker("Content Color", "#333333", key="content_color")
    background_color = st.color_picker("Background Color", "#FFFFFF", key="bg_color")

with col4:
    st.subheader("Heading Font")
    heading_font = st.selectbox(
        "Select Heading Font",
        ["Arial", "Helvetica", "Times New Roman", "Courier New", "Georgia", "Verdana", "Trebuchet MS", "Calibri", "Cambria"],
        key="heading_font"
    )
    heading_size = st.slider("Heading Size (px)", 24, 48, 36, key="heading_size")

with col5:
    st.subheader("Content Font")
    content_font = st.selectbox(
        "Select Content Font",
        ["Arial", "Helvetica", "Times New Roman", "Courier New", "Georgia", "Verdana", "Trebuchet MS", "Calibri", "Cambria"],
        key="content_font"
    )
    content_size = st.slider("Content Size (px)", 14, 28, 18, key="content_size")

# Convert colors to RGB
heading_rgb = tuple(int(heading_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
content_rgb = tuple(int(content_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
bg_rgb = tuple(int(background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

# Preview section
st.header("Preview Settings")
preview = f"""
Selected Settings:
- Heading Style: {heading_font}, {heading_size}px, {heading_color}
- Content Style: {content_font}, {content_size}px, {content_color}
- Background Color: {background_color}
"""
st.code(preview)

# Generate button
if st.button("Generate Presentation", key="generate_btn"):
    client = get_openai_client()
    if not client:
        st.warning("Please enter a valid OpenAI API Key")
    else:
        with st.spinner('Processing your presentation...'):
            slide_contents = generate_slide_content_general(client, topic, "3", slide_titles)
            text = parse_slides(slide_contents)
            st.text_area("Slide Contents:", slide_contents, height=200, key="slide_contents")
            pptx_file = create_ppt(text, heading_rgb, heading_size, bg_rgb, content_rgb, content_size, heading_font, content_font)
            st.download_button(
                label="Download Presentation",
                data=pptx_file,
                file_name="generated_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key="download_btn"
            )
            st.success("Presentation generated successfully!")

# Footer
st.markdown("---")
st.markdown("Created with ❤ for researchers")