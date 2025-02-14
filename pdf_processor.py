# Import required libraries
import fitz  # PyMuPDF library for PDF processing
from PIL import Image  # Python Imaging Library for image manipulation
import io  # For handling input/output operations
import streamlit as st  # For web interface components
import hashlib  # For generating unique hashes of images

def extract_and_display_images(uploaded_file, max_width=400):
    """
    Extract and display images from a PDF file in a grid layout.
    
    Args:
        uploaded_file: The uploaded PDF file object
        max_width: Maximum width for displayed images (default: 400px)
    """
    # Open the PDF file using PyMuPDF
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    # Create a set to store unique image hashes (avoid duplicates)
    image_hashes = set()
    
    # Create a grid layout with 3 columns for displaying images
    columns = st.columns(3)
    
    # Track current column position
    column_idx = 0

    # Iterate through each page in the PDF
    for page_num in range(len(pdf_document)):
        # Get current page
        page = pdf_document[page_num]
        
        # Extract all images from the current page
        images = page.get_images(full=True)

        # Process each image found on the page
        for img in images:
            # Get the image reference number
            xref = img[0]
            
            # Extract the raw image data
            base_image = pdf_document.extract_image(xref)
            
            # Get the binary image data
            image_bytes = base_image["image"]
            
            # Generate a unique hash for the image
            img_hash = hashlib.md5(image_bytes).hexdigest()

            # Skip if this image has already been processed
            if img_hash in image_hashes:
                continue
                
            # Add hash to set of processed images
            image_hashes.add(img_hash)

            # Convert binary data to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Get original image dimensions
            width, height = image.size

            # Resize image if it's too wide
            if width > max_width:
                # Calculate new height maintaining aspect ratio
                aspect_ratio = height / width
                new_width = max_width
                new_height = int(new_width * aspect_ratio)
                
                # Resize the image
                image = image.resize((new_width, new_height))

            # Display image in the current column
            with columns[column_idx]:
                st.image(image, use_column_width=True)

            # Move to next column
            column_idx += 1

            # Reset to first column if row is full
            if column_idx >= len(columns):
                column_idx = 0

    # Clean up: close the PDF document
    pdf_document.close()

# Note: The following code is commented out as it's now integrated elsewhere
# # Create sidebar header
# st.sidebar.header("PDF Image Extractor")
# 
# # Add file uploader to sidebar
# uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
# 
# # Process file if uploaded
# if uploaded_file is not None:
#     extract_and_display_images(uploaded_file)
# else:
#     st.text("Please upload a PDF file to extract images.")
