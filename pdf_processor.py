import fitz  # PyMuPDF library
from PIL import Image
import io
import streamlit as st
import hashlib

def extract_and_display_images(uploaded_file, max_width=400):
    """
    Extract images from an uploaded PDF file, resize them, and display them side by side.
    
    Parameters:
    - uploaded_file: Uploaded PDF file object.
    - max_width: Maximum width for resized images (default: 400 pixels).
    """
    # Read the file-like object into PyMuPDF
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    image_hashes = set()  # To store unique image hashes
    columns = st.columns(3)  # Change number based on how many images you want per row
    column_idx = 0  # To keep track of the column index

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        images = page.get_images(full=True)

        for img in images:
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            img_hash = hashlib.md5(image_bytes).hexdigest()

            # Skip duplicates
            if img_hash in image_hashes:
                continue
            image_hashes.add(img_hash)

            # Resize and display image
            image = Image.open(io.BytesIO(image_bytes))
            width, height = image.size

            # Resize the image while maintaining the aspect ratio
            if width > max_width:
                aspect_ratio = height / width
                new_width = max_width
                new_height = int(new_width * aspect_ratio)
                image = image.resize((new_width, new_height))

            # Display image in columns
            with columns[column_idx]:
                st.image(image, use_column_width=True)  # Corrected argument

            # Move to the next column
            column_idx += 1

            # If the current row is full, move to the next row
            if column_idx >= len(columns):
                column_idx = 0

    pdf_document.close()

# Streamlit interface
# st.sidebar.header("PDF Image Extractor")
# uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

# if uploaded_file is not None:
#     extract_and_display_images(uploaded_file)
# else:
#     st.text("Please upload a PDF file to extract images.")
