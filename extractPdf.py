import streamlit as st
import PyPDF2
import io
import os
import re

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