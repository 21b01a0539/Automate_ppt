import streamlit as st
from components import get_openai_client, parse_slides
from ppt import create_ppt
import speech_recognition as sr
from components import generate_slide_content_general
import requests  # For making API requests

# Custom CSS for better styling and animations
st.markdown("""
    <style>
    /* General Styling */
    .main {
        padding: 2rem;
        background: linear-gradient(to bottom, #f0f4fc, #ffffff);
        animation: fadeIn 1s;
    }
    
    .stTitle {
        color: #2E4057;
        text-align: center;
        padding-bottom: 2rem;
        font-size: 2.5rem;
        font-weight: bold;
        animation: slideDown 1s;
    }
    
    .section-header {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        animation: fadeIn 1s ease-in-out;
    }
    
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }

    .stColorPicker > label {
        font-weight: bold;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
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

# Function to fetch images from Unsplash
def fetch_unsplash_images(query, api_key, per_page=5):
    """Fetch images from Unsplash based on a query."""
    url = f"https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {api_key}"
    }
    params = {
        "query": query,
        "per_page": per_page,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        st.error(f"Failed to fetch images: {response.status_code}")
        return []

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

# Fetch and display related images
if topic:
    st.header("Related Images")
    unsplash_api_key = "your_unsplash_api_key"  # Replace with your Unsplash API key
    images = fetch_unsplash_images(topic, unsplash_api_key, per_page=5)
    
    if images:
        st.write(f"Displaying {len(images)} related images for '{topic}':")
        for image in images:
            st.image(image["urls"]["regular"], caption=image["description"] if image["description"] else "No description", use_column_width=True)
    else:
        st.warning("No images found for the given topic.")

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