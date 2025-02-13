paper to ppt

import streamlit as st
from components import extract_pdf_text, get_openai_client, generate_slide_content, parse_slides
from ppt import create_ppt
import fitz  # PyMuPDF library
from PIL import Image
import io
import hashlib


def extract_and_display_images(uploaded_file, max_width=400):
    uploaded_file.seek(0)  # Reset file pointer
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    image_hashes = set()
    columns = st.columns(4)  # 3 images per row
    column_idx = 0

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        images = page.get_images(full=True)

        # st.write(f"Number of images on page {page_num + 1}: {len(images)}")  # Debug info

        for img in images:
            try:
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                img_hash = hashlib.md5(image_bytes).hexdigest()

                if img_hash in image_hashes:
                    continue  # Skip duplicates
                image_hashes.add(img_hash)

                # Resize image
                image = Image.open(io.BytesIO(image_bytes))
                width, height = image.size
                if width > max_width:
                    aspect_ratio = height / width
                    image = image.resize((max_width, int(max_width * aspect_ratio)))

                # Display image in columns
                with columns[column_idx % len(columns)]:
                    st.image(image, use_column_width=True)
                column_idx += 1

            except Exception as e:
                st.error(f"Failed to process image on page {page_num + 1}: {e}")
                continue

    pdf_document.close()


# Custom CSS for better styling and animations
st.markdown("""
    <style>
    /* Base reset */
    .main {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #EEF2FF 0%, #E6E9F5 100%);
    }

    /* Reset all default spacings */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        margin: 0 !important;
    }

    /* Header container */
    .header-container {
        padding: 2rem 0 1rem 0 !important;
        margin: 0 !important;
        background: transparent !important;
    }

    /* Main title styling */
    h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        background: linear-gradient(120deg, #2B3A67, #4E6E81);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-align: center;
        padding: 1rem 0 !important;
        margin: 0 !important;
    }

    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #4A5568;
        margin: 0.5rem 0 1.5rem 0 !important;
        padding: 0 !important;
    }

    /* Content sections */
    .section-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 6px rgba(43, 58, 103, 0.1);
    }

    /* File uploader */
    .stFileUploader {
        padding: 0 !important;
        margin: 0 !important;
    }

    .stFileUploader > div {
        padding: 1rem !important;
        margin: 0 !important;
        background: white !important;
        border-radius: 12px;
        border: 2px dashed #4E6E81;
    }

    /* Text inputs */
    .stTextInput > div,
    .stTextArea > div {
        padding: 0 !important;
        margin: 0.5rem 0 !important;
    }

    /* Remove all extra padding */
    .css-1544g2n {
        padding: 0 !important;
    }

    .css-1y4p8pa {
        padding: 0 !important;
    }

    .row-widget {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Style section headers */
    h2, h3 {
        margin: 0 0 1rem 0 !important;
        padding: 0 !important;
        color: #2B3A67;
        font-family: 'Montserrat', sans-serif;
    }

    /* Sidebar adjustments */
    .css-1d391kg {
        padding: 1rem !important;
    }

    /* Remove white spaces between elements */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Style buttons */
    .stButton > button {
        width: auto;
        padding: 0.5rem 1rem !important;
        margin: 0.5rem 0 !important;
        background: linear-gradient(135deg, #2B3A67 0%, #4E6E81 100%);
        color: white;
        border: none;
        border-radius: 8px;
    }

    /* Ensure proper spacing for markdown */
    .stMarkdown {
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing data between reruns
if 'combined_text' not in st.session_state:
    st.session_state['combined_text'] = ""

# Update the page structure
st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.markdown('<h1>Research Paper to Presentation</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your research paper into professional presentation slides easily! Follow the steps below to generate your customized presentation.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.header("How to Use")
    st.markdown("""
    1. *Upload your PDF* - Start by uploading your research paper in PDF format
    2. *Select Slide Sections* - Choose which sections to include in your presentation
    3. *Customize Design* - Pick colors and fonts for your slides
    4. *Generate* - Click submit to create your presentation
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# File upload section with unique key
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.header("Upload Research Paper")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf_uploader")

pdf_text = ""
if uploaded_file is not None:
    pdf_text = extract_pdf_text(uploaded_file)
    # extract_and_display_images(uploaded_file)
    with st.expander("View Extracted PDF Text"):
        st.text_area("Extracted Content:", pdf_text, height=200, key="extracted_text")
    st.markdown('</div>', unsafe_allow_html=True)

# Slide structure selection with unique key
st.markdown('<div class="section-container">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

# Design customization with unique keys
st.markdown('<div class="section-container">', unsafe_allow_html=True)
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
        st.title("Extracted Images")
        extract_and_display_images(uploaded_file)
        with st.spinner('Processing your presentation...'):
            slide_contents = generate_slide_content(client, pdf_text, "3", slide_titles)
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