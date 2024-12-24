import streamlit as st
from components import extract_pdf_text,get_openai_client,generate_slide_content,parse_slides
from ppt import create_ppt

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2E4057;
        text-align: center;
        padding-bottom: 2rem;
    }
    .section-header {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

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
    1. **Upload your PDF** - Start by uploading your research paper in PDF format
    2. **Enter Additional Content** - Add any extra information you want to include
    3. **Select Slide Sections** - Choose which sections to include in your presentation
    4. **Customize Design** - Pick colors and fonts for your slides
    5. **Generate** - Click submit to create your presentation
    """)

# Initialize session state
if 'combined_text' not in st.session_state:
    st.session_state['combined_text'] = ""

# File upload section
st.header("Step 1: Upload Research Paper")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

pdf_text = ""
if uploaded_file is not None:
    pdf_text = extract_pdf_text(uploaded_file)
    with st.expander("View Extracted PDF Text"):
        st.text_area("Extracted Content:", pdf_text, height=200)

# Additional text input
st.header("Step 2: Additional Information")
st.session_state['combined_text'] = st.text_area(
    "Enter any additional information or notes:",
    value=st.session_state['combined_text'],
    height=150
)

# Slide structure selection
st.header("Step 3: Select Presentation Structure")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic Sections")
    title_slide = st.checkbox("Title Slide", value=True)
    intro_slide = st.checkbox("Introduction", value=True)
    contents = st.checkbox("Table of Contents", value=True)
    methodology = st.checkbox("Methodology")
    results = st.checkbox("Results")

with col2:
    st.subheader("Additional Sections")
    discussion = st.checkbox("Discussion")
    conclusion = st.checkbox("Conclusion")
    references = st.checkbox("References")
    custom_section = st.text_input("Add Custom Section")

# Design customization
st.header("Step 4: Customize Design")
col3, col4, col5 = st.columns(3)

with col3:
    st.subheader("Color Scheme")
    heading_color = st.color_picker("Heading Color", "#2E4057")
    content_color = st.color_picker("Content Color", "#333333")
    background_color = st.color_picker("Background Color", "#FFFFFF")

with col4:
    st.subheader("Heading Font")
    heading_font = st.selectbox(
        "Select Heading Font",
        ["Arial", "Helvetica", "Times New Roman", "Courier New", "Georgia", "Verdana", 
                                         "Trebuchet MS", "Calibri", "Cambria", "Garamond", "Comic Sans MS", 
                                         "Palatino Linotype", "Tahoma", "Lucida Sans Unicode", "Impact", 
                                         "Franklin Gothic Medium", "Segoe UI", "Optima", "Baskerville", "Bookman","Algerian"]
    )
    heading_size = st.slider("Heading Size (px)", 24, 48, 36)

with col5:
    st.subheader("Content Font")
    content_font = st.selectbox(
        "Select Content Font",
        ["Arial", "Helvetica", "Times New Roman", "Courier New", "Georgia", "Verdana", 
                                         "Trebuchet MS", "Calibri", "Cambria", "Garamond", "Comic Sans MS", 
                                         "Palatino Linotype", "Tahoma", "Lucida Sans Unicode", "Impact", 
                                         "Franklin Gothic Medium", "Segoe UI", "Optima", "Baskerville", "Bookman","Algerian"]
    )
    content_size = st.slider("Content Size (px)", 14, 28, 18)
heading_rgb = tuple(int(heading_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
content_rgb = tuple(int(content_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
bg_rgb = tuple(int(background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

# Preview section
st.header("Step 5: Preview Settings")
preview = f"""
Selected Settings:
- Heading Style: {heading_font}, {heading_size}px, {heading_color}
- Content Style: {content_font}, {content_size}px, {content_color}
- Background Color: {background_color}
"""
st.code(preview)

# Generate button
if st.button("Generate Presentation", type="primary"):
    # st.success("Processing your presentation...")
    
    # Display structure
    # st.subheader("Presentation Structure")
    sections = []
    if title_slide: sections.append("Title Slide")
    if intro_slide: sections.append("Introduction")
    if contents: sections.append("Table of Contents")
    if methodology: sections.append("Methodology")
    if results: sections.append("Results")
    if discussion: sections.append("Discussion")
    if conclusion: sections.append("Conclusion")
    if references: sections.append("References")
    if custom_section: sections.append(custom_section)
    
    # for i, section in enumerate(sections, 1):
    #     st.write(f"{i}. {section}")

    # # Display design settings
    # # st.subheader("Design Settings")
    # # st.write("**Extracted PDF Text:**")
    # # st.write(pdf_text)
    # # st.write("**Additional Information:**")
    # # st.write(st.session_state['combined_text'])

    client = get_openai_client()
    if not client:
        st.warning("Please enter a valid OpenAI API Key")
    else:
       with st.spinner('Processing your presentation...'):
            slide_contents = generate_slide_content(client, pdf_text,"3",sections)
            # st.subheader("Generated Slide Contents")
            text = parse_slides(slide_contents)
            # st.text_area("Slide Contents:", slide_contents, height=200)
            # st.text_area("Parsed Slide Contents:", parse_slides(slide_contents), height=200)
            pptx_file = create_ppt(text, heading_rgb, heading_size, bg_rgb, content_rgb, content_size, heading_font, content_font)
            st.download_button(label="Download Presentation", data=pptx_file, file_name="generated_presentation.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
            st.success("Presentation generated successfully!")
# Footer
st.markdown("---")
st.markdown("Created with ❤️ for researchers")