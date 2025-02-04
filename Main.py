import streamlit as st

# Set the page title and layout
st.set_page_config(page_title="Home", layout="centered")

# Title of the main page
st.title("Welcome to My Project")

# Button to redirect to Research Paper to PDF
if st.button("Research Paper to PDF"):
    st.session_state.page = "research_paper_to_pdf"
    st.experimental_rerun()

# Button to redirect to Speech to PPT
if st.button("Speech to PPT"):
    st.session_state.page = "speech_to_ppt"
    st.experimental_rerun()

# Redirect logic
if "page" in st.session_state:
    if st.session_state.page == "research_paper_to_pdf":
        st.switch_page("pages/researchpaper_to_ppt.py")
    elif st.session_state.page == "speech_to_ppt":
        st.switch_page("pages/text_to_ppt.py")