import streamlit as st
import PyPDF2
import io
import os
import re
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

def generate_slide_content(client, text,No_of_Slides,sections):
    """
    Use OpenAI to generate slide content with improved parsing strategy.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in creating concise and professional presentation slides."},
                {"role": "user", "content": f"""Convert the research paper text into a structured presentation. 
                Convert the research paper text into a structured presentation.
                Generate the content for the presentation slides.{sections}
            Follow these formatting rules:
-Title each slide with square brackets: [Slide Title]
- Use {No_of_Slides} bullet points per slide
- Do not include irrelevant information or long paragraphs.
Research Paper:{text[:4000]}"""}
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

    sections = text.split("\n\n")
    for section in sections:
        lines = section.splitlines()
        if lines and lines[0].startswith("[") and lines[0].endswith("]"):
            slide_title = lines[0][1:-1]
            slide_key = f"Slide {len(content) + 1}: {slide_title}"
            content[slide_key] = []
            items = [line[2:] for line in lines[1:] if line.startswith("-")]
            content[slide_key].extend(items)

    return (content)