import streamlit as st
import PyPDF2
import io
import os
import re
import fitz  # PyMuPDF library
from PIL import Image
import hashlib
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def extract_pdf_text(uploaded_file):
    """
    Extract text from an uploaded PDF file.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text() + "\n\n"
        
        return full_text
    except Exception as e:
        st.error(f"Error extracting PDF text: {e}")
        return ""

def get_openai_client():
    """
    Initialize OpenAI client with API key from multiple sources.
    """
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai_api_key:
        openai_api_key = st.text_input(
            "Enter your OpenAI API Key", 
            type="password", 
            help="You can find your API key at https://platform.openai.com/account/api-keys"
        )
    
    if not openai_api_key:
        st.warning("Please enter a valid OpenAI API Key")
        return None
    
    return OpenAI(api_key=openai_api_key)

def generate_slide_content(client, text):
    """
    Use OpenAI to generate slide content
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert presentation designer..."},
                {"role": "user", "content": f"Convert the research paper text...{text[:4000]}"}
            ],
            max_tokens=1500
        )
        
        # Get the raw content
        raw_content = response.choices[0].message.content
        
        return raw_content
    except Exception as e:
        st.error(f"Error generating slide content: {e}")
        return ""

def generate_slide_content_general(client, input_text, no_of_slides, sections):
    """
    Use OpenAI to generate slide content for general topics with improved parsing strategy.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in creating concise and professional presentation slides."},
                {"role": "user", "content": f"""Convert the provided content into a structured presentation. 
                The content can be from a general topic, research paper, or any other source. 
                Generate the content for the presentation slides based on the following sections: {sections}.
                Follow these formatting rules:
- Title each slide with square brackets: [Slide Title]
- Use {no_of_slides} bullet points per slide
- Ensure the content is concise and relevant to the topic
- Do not include long paragraphs or irrelevant information

Content to be converted into slides:
{input_text[:4000]}"""}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        # Get the raw content
        raw_content = response.choices[0].message.content
        
        return raw_content
    except Exception as e:
        st.error(f"Error generating slide content: {e}")
        return ""

def parse_slides(text):
    content = {}

    content = {}
    section_map = {
        "Slide 1: Title": "Title",
        "Slide 2: Abstract": "Abstract",
        "Slide 3: Introduction": "Introduction",
        "Slide 4: Related Work": "Related Work",
        "Slide 5: Methodology": "Methodology",
        "Slide 6: Results": "Results",
        "Slide 7: Conclusions": "Conclusions",
    }

    sections = text.split("\n\n")
    for section in sections:
        lines = section.splitlines()
        if lines and lines[0].startswith("[") and lines[0].endswith("]"):
            slide_title = lines[0][1:-1]  # Remove square brackets
            mapped_title = section_map.get(slide_title, slide_title)
            content[mapped_title] = [
                line[2:] for line in lines[1:] if line.startswith("-")
            ]

    return content

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

    st.title("Extracted Images from PDF")

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
                st.image(image, use_container_width=True)  # use_container_width instead of use_column_width

            # Move to the next column
            column_idx += 1

            # If the current row is full, move to the next row
            if column_idx >= len(columns):
                column_idx = 0

    pdf_document.close()
