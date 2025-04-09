import streamlit as st 
from components import extract_pdf_text, get_openai_client, generate_slide_content, parse_slides, extract_slide_titles_from_paper
  # Import custom functions
from ppt import create_ppt_researchpaper
from PIL import Image 
import io  
import os
import hashlib
import fitz
from openai import OpenAI  
from io import BytesIO  
from Exceptions.exceptions import OpenAIError, SlideGenerationError, PDFProcessingError

def get_openai_client():
    """
    Initialize OpenAI client with API key from multiple sources:
    1. Streamlit secrets
    2. Environment variables (.env)
    3. User input
    
    Returns:
        OpenAI: Configured OpenAI client
    """
    # 2. Check environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    # 3. Prompt user input if no API key found
    if not openai_api_key:
        openai_api_key = st.text_input(
            "Enter your OpenAI API Key", 
            type="password", 
            help="You can find your API key at https://platform.openai.com/account/api-keys"
        )
    
    # Validate API key
    if not openai_api_key:
        st.warning("Please enter a valid OpenAI API Key")
        return None
    
    return OpenAI(api_key=openai_api_key)


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

import openai



# Custom CSS matching speech_to_ppt.py
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

    /* File uploader styling */
    .stFileUploader > div {
        background: white !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: 2px dashed #4E6E81 !important;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }

    .stFileUploader > div:hover {
        border-color: #2B3A67 !important;
        background: rgba(255, 255, 255, 0.9) !important;
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

    /* Select box and other input styling */
    .stSelectbox > div > div,
    .stColorPicker > div > div {
        background: white;
        border-radius: 10px;
        border: 2px solid #E6E9F5;
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:hover {
        border-color: #2B3A67;
    }

    /* Remove empty spaces */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 1000px !important;
        margin: 0 auto !important;
    }

    .element-container {
        margin: 0 !important;
        padding: 1rem 0 !important;
        border-bottom: 1px solid rgba(43, 58, 103, 0.1);
    }

    .element-container:last-child {
        border-bottom: none;
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

    /* Expander styling */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 10px;
        border: 2px solid #E6E9F5;
        transition: all 0.3s ease;
    }

    /* Remove default streamlit margins */
    .css-1544g2n {
        padding: 0 !important;
    }

    .css-1y4p8pa {
        padding: 0 !important;
    }

    /* Sidebar styling */
    .css-1d391kg {  /* Sidebar background */
        background: linear-gradient(180deg, #f5f7ff 0%, #e8ecfd 100%);
        border-right: 1px solid #e0e5f5;
    }

    /* Sidebar header */
    .css-1d391kg h1, .css-1d391kg h2 {
        color: #2B3A67;
        font-size: 1.5rem;
        padding: 1rem 0;
        border-bottom: 2px solid #4E6E81;
        margin-bottom: 1.5rem;
    }

    /* Sidebar content */
    .css-1d391kg .stMarkdown {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }

    /* Sidebar list items */
    .css-1d391kg ul {
        list-style-type: none;
        padding-left: 0;
    }

    .css-1d391kg li {
        margin: 0.8rem 0;
        padding-left: 1.5rem;
        position: relative;
    }

    .css-1d391kg li:before {
        content: '→';
        position: absolute;
        left: 0;
        color: #4E6E81;
    }

    /* Sidebar emphasis */
    .css-1d391kg em {
        color: #2B3A67;
        font-style: normal;
        font-weight: 600;
        background: linear-gradient(120deg, #4E6E81 0%, #4E6E81 100%);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
    }
    </style>
""", unsafe_allow_html=True)


# Main title
st.title("Research Paper to Presentation")
st.markdown("""
    Transform your research paper into professional presentation slides easily!
    Follow the steps below to generate your customized presentation.
""")

# Sidebar with instructions
with st.sidebar:
    st.header("📚 How to Use")
    st.markdown("""
    ### Step-by-Step Guide
    
    1. *Upload your PDF* 📄
       - Supported format: PDF
       - Max size: 200MB
       - Clear text required
    
    2. *Select Slide Sections* 📑
       - Choose key sections
       - Arrange in order
       - Add custom sections
    
    3. *Customize Design* 🎨
       - Pick color scheme
       - Choose fonts
       - Set sizes
    
    4. *Generate* ✨
       - Review content
       - Download PPTX
    
    ### Tips
    - Use clear, legible PDFs
    - Structure content logically
    - Preview before finalizing
    
    ### Need Help?
    Contact support at:
    support@example.com
    """)

# File upload section
client = get_openai_client()
st.header("Upload Research Paper")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        # Step 1: Extract text content from the PDF
        try:
            text = extract_pdf_text(uploaded_file)
        except Exception as e:
            raise PDFProcessingError(f"Failed to extract text from PDF: {e}")
        
        # Step 2: Reset file pointer to start of file for image extraction
        uploaded_file.seek(0)
        
        # Step 3: Initialize PDF document for image extraction
        try:
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        except Exception as e:
            raise PDFProcessingError(f"Failed to open PDF document: {e}")
        
        extracted_images = []  # List to store extracted images
        
        # Step 4: Extract images from each page of the PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            images = page.get_images(full=True)
            
            # Process each image found in the page
            for img in images:
                try:
                    # Extract image data
                    xref = img[0]  # Get image reference
                    base_image = pdf_document.extract_image(xref)  # Extract raw image data
                    image_bytes = base_image["image"]  # Get binary image data
                    
                    # Step 5: Validate and convert image
                    # Create PIL Image object to verify image is valid and get format
                    image = Image.open(BytesIO(image_bytes))
                    
                    # Step 6: Save image to BytesIO buffer
                    image_data = BytesIO()
                    # Save with original format or fallback to PNG
                    image.save(image_data, format=image.format if image.format else 'PNG')
                    image_data.seek(0)  # Reset buffer pointer
                    extracted_images.append(image_data)
                    
                    # Log successful extraction
                    print(f"Successfully extracted image {len(extracted_images)} from page {page_num + 1}")
                except Exception as img_error:
                    raise ImageExtractionError(f"Error processing image on page {page_num + 1}: {img_error}")
        
        # Step 7: Store extracted images in session state for later use
        st.session_state['pdf_images'] = extracted_images
        
        # Step 8: Display extraction results
        if extracted_images:
            # Show number of images found
            st.info(f"Found {len(extracted_images)} images in the PDF")
            
            # Step 9: Display image preview grid
            st.subheader("Extracted Images from PDF")
            cols = st.columns(3)  # Create 3 columns for grid layout
            for idx, img_data in enumerate(extracted_images):
                try:
                    with cols[idx % 3]:  # Cycle through columns
                        img_data.seek(0)  # Reset image data pointer
                        # Display image with caption
                        st.image(img_data, caption=f"Image {idx + 1}", width=200)
                except Exception as e:
                    st.error(f"Error displaying image {idx + 1}: {str(e)}")
        else:
            st.warning("No images found in the PDF")
        
        # Step 10: Show extracted text in expandable section
        with st.expander("View Extracted PDF Text"):
            st.text_area("Extracted Content:", text, height=200)

    except PDFProcessingError as e:
        st.error(f"PDF Processing Error: {e}")
    except ImageExtractionError as e:
        st.error(f"Image Extraction Error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
# Slide structure selection with unique key
# st.header("Enter Slide Titles")
# st.write("You can specify the slides you need for your presentation by listing their titles below.")

# slide_titles_input = st.text_area(
#     "Enter the titles of your slides, one per line:",
#     placeholder="e.g., Title\nIntroduction\nMethodology\nResults\nConclusion",
#     key="slide_titles"
# )

# if slide_titles_input.strip():
#     slide_titles = [title.strip() for title in slide_titles_input.split("\n") if title.strip()]
#     st.write("### Selected Slide Titles:")
#     for i, title in enumerate(slide_titles, 1):
#         st.write(f"{i}. {title}")
# else:
#     st.write("No slide titles entered yet.")

        
st.header("Step 2: Choose Slide Title Generation Method")
slide_option = st.radio(
            "How would you like to generate slide titles?",
            ("Specify slide titles manually","Auto-generate from the research paper")
        )

slide_titles = []

if slide_option == "Specify slide titles manually":
            st.info("✍️ Enter the titles for each slide, one per line.")
            slide_titles_input = st.text_area(
                "Slide Titles:",
                placeholder="e.g., Title Slide\nIntroduction\nMethodology\nResults\nConclusion"
            )

            if slide_titles_input.strip():
                slide_titles = [title.strip() for title in slide_titles_input.split("\n") if title.strip()]
                st.subheader("Your Slide Titles:")
                for i, title in enumerate(slide_titles, 1):
                    st.markdown(f"**{i}. {title}**")
            else:
                st.warning("⚠️ No slide titles entered yet.")
else:
            if client:
                st.info("🤖 Extracting slide titles using AI...")
                with st.spinner("Generating slide titles..."):
                    slide_titles = extract_slide_titles_from_paper(text, client)

                if slide_titles:
                    st.subheader("Generated Slide Titles:")
                    for i, title in enumerate(slide_titles, 1):
                        st.markdown(f"**{i}. {title}**")
                else:
                    st.error("❌ Could not generate slide titles.")
            else:
                st.warning("⚠️ Please provide your OpenAI API key to auto-generate titles.")
 # Implement this function


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

# Add this after the slide titles input section

# Edit Preview Section
st.header("Edit Slide Content and Select Images")

if 'parsed_slides' not in st.session_state:
    st.session_state['parsed_slides'] = {}

if 'selected_images' not in st.session_state:
    st.session_state['selected_images'] = {}

if uploaded_file is not None:
    # Generate initial slide content if not already generated
    if not st.session_state['parsed_slides']:
        client = get_openai_client()
        if client:
            with st.spinner('Generating initial slide content...'):
                slide_contents = generate_slide_content(client, text, "3", slide_titles)
                st.session_state['parsed_slides'] = parse_slides(slide_contents)
        else:
            st.warning("Please enter a valid OpenAI API Key to generate slide content.")

    # Display editable slide content and image selection
    if st.session_state['parsed_slides']:
        for idx, (title, content_list) in enumerate(st.session_state['parsed_slides'].items()):
            st.subheader(f"Slide: {title}")
            
            # Editable content
            edited_content = st.text_area(
                f"Edit content for '{title}'",
                value="\n".join(content_list),
                key=f"edited_content_{idx}"
            )
            st.session_state['parsed_slides'][title] = edited_content.split("\n")
            
            # Image selection for this slide
            if 'pdf_images' in st.session_state and st.session_state['pdf_images']:
                st.write("**Select an image for this slide:**")
                image_options = [f"Image {i+1}" for i in range(len(st.session_state['pdf_images']))]
                selected_image = st.selectbox(
                    f"Choose an image for '{title}'",
                    options=image_options,
                    index=idx % len(image_options),  # Default to cycling through images
                    key=f"selected_image_{idx}"
                )
                st.session_state['selected_images'][title] = selected_image
                
                # Show preview of the selected image
                selected_image_idx = int(selected_image.split(" ")[1]) - 1
                st.image(
                    st.session_state['pdf_images'][selected_image_idx],
                    caption=f"Selected Image for {title}",
                    width=300
                )
            else:
                st.info("No images available for selection.")

# Finalize and Download PPT
if st.button("Finalize and Download Presentation", key="finalize_btn"):
    if not st.session_state['parsed_slides']:
        st.warning("Please generate slide content first.")
    else:
        with st.spinner('Creating your presentation...'):
            # Prepare selected images for each slide
            slide_images = []
            for title in st.session_state['parsed_slides']:
                slide_images.append(st.session_state['selected_images'][title])
            
            # Generate PPT with edited content and selected images
            pptx_file = create_ppt_researchpaper(
                st.session_state['parsed_slides'],
                heading_rgb,
                heading_size,
                bg_rgb,
                content_rgb,
                content_size,
                heading_font,
                content_font,
                slide_images
            )
            
            # Download button
            st.download_button(
                label="Download Presentation",
                data=pptx_file,
                file_name="generated_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                key="download_btn_final"
            )
            st.success("Presentation finalized and ready for download!")
# Footer
st.markdown("---")
st.markdown("Created with ❤ for researchers")
