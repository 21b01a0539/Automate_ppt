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

# Main title with description
st.title("Research Paper to Presentation Generator")
st.markdown("""
    Transform your research paper into professional presentation slides easily!
    Follow the steps below to generate your customized presentation.
""")

# Sidebar with instructions
with st.sidebar:
    st.header("How to Use")
    st.markdown("""
    1. *Upload your PDF* - Start by uploading your research paper in PDF format
    2. *Select Slide Sections* - Choose which sections to include in your presentation
    3. *Customize Design* - Pick colors and fonts for your slides
    4. *Generate* - Click submit to create your presentation
    """)

# File upload section with unique key
st.header("Upload Research Paper")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf_uploader")

pdf_text = ""
if uploaded_file is not None:
    pdf_text = extract_pdf_text(uploaded_file)
    # extract_and_display_images(uploaded_file)
    with st.expander("View Extracted PDF Text"):
        st.text_area("Extracted Content:", pdf_text, height=200, key="extracted_text")

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