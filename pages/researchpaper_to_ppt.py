# ============= Import Section =============
# Import Streamlit for creating the web application interface
import streamlit as st

# Import custom functions from our components module
from components import (
    extract_pdf_text,      # Function to extract text from PDFs
    get_openai_client,     # Function to initialize OpenAI API
    generate_slide_content,# Function to generate slide content using AI
    parse_slides          # Function to parse generated content into slides
)

# Import PowerPoint creation functions from our ppt module
from ppt import (
    create_ppt,              # Function for creating basic PPT
    create_ppt_with_pdf_images # Function for creating PPT with PDF images
)

# Import PDF processing library
import fitz  # PyMuPDF library for handling PDF files

# Import image processing library
from PIL import Image  # Python Imaging Library for image manipulation

# Import utilities
import io  # For handling input/output operations
import hashlib  # For generating unique identifiers
from openai import OpenAI  # OpenAI API client
from io import BytesIO  # For handling binary data in memory

# ============= OpenAI Client Setup =============
def get_openai_client():
    """
    Initialize and configure OpenAI API client
    Returns: Configured OpenAI client or None if no valid API key
    """
    # Set default API key (replace with your actual key)
    openai_api_key = "your-api-key-here"
    
    # If no API key is set, prompt user to input one
    if not openai_api_key:
        openai_api_key = st.text_input(
            "Enter your OpenAI API Key",  # Input label
            type="password",              # Hide the API key
            help="Get your API key from OpenAI dashboard"  # Help text
        )
    
    # Validate the API key
    if not openai_api_key:
        st.warning("Please enter a valid OpenAI API Key")
        return None
    
    # Return configured OpenAI client
    return OpenAI(api_key=openai_api_key)

# ============= Main Application UI =============
# Set the application title
st.title("Research Paper to Presentation Converter")

# Add description text
st.markdown("""
    Transform your research papers into professional presentations automatically!
    Upload your PDF and customize the output.
""")

# Create file uploader widget that accepts PDF files
uploaded_file = st.file_uploader("Upload your research paper (PDF)", type="pdf")

# ============= PDF Processing Section =============
# Process the uploaded file if one exists
if uploaded_file is not None:
    try:
        # Step 1: Extract text content from the PDF
        text = extract_pdf_text(uploaded_file)
        
        # Reset file pointer to beginning for image extraction
        uploaded_file.seek(0)
        
        # Initialize PDF document for image extraction
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        extracted_images = []  # List to store extracted images

        # Loop through each page in the PDF
        for page_num in range(len(pdf_document)):
            # Get current page
            page = pdf_document[page_num]
            # Get list of images on the page
            images = page.get_images(full=True)
            
            # Process each image found on the page
            for img in images:
                try:
                    # Get image reference number
                    xref = img[0]
                    # Extract raw image data
                    base_image = pdf_document.extract_image(xref)
                    # Get binary image data
                    image_bytes = base_image["image"]
                    
                    # Create PIL Image object to validate image
                    image = Image.open(BytesIO(image_bytes))
                    
                    # Create new BytesIO buffer for the image
                    image_data = BytesIO()
                    # Save image with original format or PNG as fallback
                    image.save(image_data, format=image.format if image.format else 'PNG')
                    # Reset buffer pointer to start
                    image_data.seek(0)
                    # Add processed image to list
                    extracted_images.append(image_data)
                    
                    # Log successful extraction
                    print(f"Successfully extracted image {len(extracted_images)} from page {page_num + 1}")
                except Exception as img_error:
                    print(f"Error processing image: {str(img_error)}")
        
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

    except Exception as e:
        st.error(f"Failed to process PDF: {e}")

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
            slide_contents = generate_slide_content(client, text, "3", slide_titles)
            parsed_slides = parse_slides(slide_contents)
            
            # Show slide contents with PDF images
            st.subheader("Slide Contents and Images:")
            for idx, (title, content_list) in enumerate(parsed_slides.items()):
                with st.expander(f"📑 {title}"):
                    # Show content
                    st.markdown("**Content:**")
                    for point in content_list:
                        st.write(f"• {point}")
                    
                    # Show image preview from PDF if available
                    st.markdown("**Image:**")
                    if 'pdf_images' in st.session_state and st.session_state['pdf_images']:
                        # Use modulo to cycle through available images
                        image_idx = idx % len(st.session_state['pdf_images'])
                        image_data = st.session_state['pdf_images'][image_idx]
                        st.image(
                            image_data, 
                            caption=f"Image from PDF for: {title}", 
                            width=300
                        )
                    else:
                        st.info("No images found in the PDF")
            
            # Generate PPT with PDF images
            pptx_file = create_ppt_with_pdf_images(
                parsed_slides, 
                heading_rgb, 
                heading_size, 
                bg_rgb, 
                content_rgb, 
                content_size, 
                heading_font, 
                content_font,
                st.session_state.get('pdf_images', [])
            )
            
            # Download button and success message
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