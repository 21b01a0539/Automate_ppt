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
from urllib.request import urlopen
import requests
from io import BytesIO
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

def get_relevant_image_topics(client, slide_content):
    """
    Extract relevant image topics based on slide content.
    Uses OpenAI GPT-4 to generate appropriate image keywords for each slide.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in selecting relevant image topics for presentation slides."},
                {"role": "user", "content": f"""Extract relevant image topics for each slide title and its content.
                
                - For each slide, suggest 1-2 keywords or phrases that best describe the visual representation needed.
                - Keywords should be concise and useful for image searches.
                - The image topics should be broad enough to find suitable images online but specific to the slide content.

                Slide Content:
                {slide_content}

                Format output as:
                [Slide Title] - Image Topics: keyword1, keyword2
                """}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        # Extracting generated content
        image_topics = response.choices[0].message.content
        return image_topics

    except Exception as e:
        print(f"Error generating image topics: {e}")
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

def get_relevant_image(topic, api_key=None):
    """Get a relevant image from Pexels based on slide title and context"""
    try:
        pexels_api_key = "pYdOIXG0gmI8pymPsfhRh8V5OeGjOfPB1eHUNGprIE0Qz4fazw2aS5yx"
        
        # Clean and process the topic/title
        search_topic = topic.replace("[", "").replace("]", "").split(":")[0].strip().lower()
        
        # Comprehensive mapping of slide titles to relevant search terms
        title_mapping = {
            # Title and Introduction slides
            "title": "professional business presentation podium",
            "introduction": "business introduction meeting professional",
            
            # Research-related slides
            "research": "scientific research laboratory",
            "methodology": "scientific research method laboratory",
            "methods": "research methodology science",
            "experiment": "scientific experiment laboratory",
            "hypothesis": "scientific hypothesis research",
            
            # Results and Analysis
            "results": "data analysis business chart",
            "analysis": "data analytics dashboard",
            "findings": "research findings presentation",
            "data": "data visualization analytics",
            
            # Discussion and Conclusion
            "discussion": "team business discussion meeting",
            "conclusion": "business conclusion handshake",
            "summary": "business summary presentation",
            
            # Future and Recommendations
            "future work": "future technology innovation",
            "recommendations": "business recommendation strategy",
            "future": "futuristic technology innovation",
            
            # Common sections
            "background": "relevant background context",
            "objectives": "target goals business",
            "literature review": "research library books",
            "implementation": "project implementation process",
            "evaluation": "evaluation assessment metrics",
            
            # Specific topics
            "technology": "modern technology innovation",
            "education": "modern education classroom",
            "healthcare": "modern healthcare medical",
            "environment": "environmental sustainability nature",
            "business": "professional business corporate",
            "science": "scientific research laboratory",
            "engineering": "engineering technology design",
            "artificial intelligence": "AI technology digital",
            "machine learning": "machine learning AI technology",
            "data science": "data science analytics",
            
            # Closing slides
            "thank you": "thank you presentation professional",
            "questions": "questions and answers discussion",
            "references": "research library references",
            "appendix": "additional information appendix"
        }
        
        # Extract keywords from the title for better context
        words = search_topic.split()
        search_terms = []
        
        # Check for exact matches first
        if search_topic in title_mapping:
            search_terms.append(title_mapping[search_topic])
        else:
            # Check for partial matches and combine relevant terms
            for word in words:
                if word in title_mapping:
                    search_terms.append(title_mapping[word])
            
            # If no matches found, use the cleaned title with professional context
            if not search_terms:
                search_terms.append(f"{search_topic} professional business")
        
        # Try each search term until we find an image
        for search_term in search_terms:
            print(f"Trying search term: {search_term}")
            
            url = "https://api.pexels.com/v1/search"
            headers = {"Authorization": pexels_api_key}
            params = {
                "query": search_term,
                "per_page": 1,
                "orientation": "landscape",
                "size": "large"
            }
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("photos"):
                    image_url = data["photos"][0]["src"]["large"]
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        print(f"Found image for term: {search_term}")
                        return BytesIO(image_response.content)
        
        # Fallback to a generic professional image if no matches found
        print("No specific images found, using fallback...")
        params["query"] = "professional business presentation"
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if data.get("photos"):
            image_url = data["photos"][0]["src"]["large"]
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                return BytesIO(image_response.content)
        
        return None
            
    except Exception as e:
        print(f"Error in get_relevant_image: {str(e)}")
        return None
