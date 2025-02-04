from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.dml.fill import FillFormat
import streamlit as st
import io

def create_ppt(content, heading_color, heading_size, bg_color, content_color, content_size, heading_font, content_font):
    """
    Create a PowerPoint presentation based on the given content and style parameters.
    """
    prs = Presentation()

    # Create the title slide
    title_slide_content = content.pop("Title Slide")  # Extract title content
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])  # Use the Title Slide layout
    title = title_slide.shapes.title
    subtitle = title_slide.placeholders[1]  # Subtitle placeholder

    # Set title and subtitle text
    title.text = title_slide_content[0]  # First item as the title
    subtitle.text = "\n".join(title_slide_content[1:])  # Remaining items as subtitle

    # Customize title font
    title.text_frame.paragraphs[0].font.size = Pt(heading_size)
    title.text_frame.paragraphs[0].font.color.rgb = RGBColor(*heading_color)
    title.text_frame.paragraphs[0].font.name = heading_font

    # Customize subtitle font
    for p in subtitle.text_frame.paragraphs:
        p.font.size = Pt(content_size)
        p.font.color.rgb = RGBColor(*content_color)
        p.font.name = content_font

    # Set background color for the title slide
    background = title_slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # Create content slides
    for slide_title, slide_content in content.items():
        slide = prs.slides.add_slide(prs.slide_layouts[1])  # Use the content slide layout

        # Set the title ("Click to add title")
        title_placeholder = slide.shapes.title
        title_placeholder.text = slide_title
        title_placeholder.text_frame.paragraphs[0].font.size = Pt(heading_size)
        title_placeholder.text_frame.paragraphs[0].font.color.rgb = RGBColor(*heading_color)
        title_placeholder.text_frame.paragraphs[0].font.name = heading_font

        # Set the content ("Click to add text")
        content_placeholder = slide.placeholders[1]
        content_placeholder.text = "\n".join(slide_content)
        for p in content_placeholder.text_frame.paragraphs:
            p.font.size = Pt(content_size)
            p.font.color.rgb = RGBColor(*content_color)
            p.font.name = content_font

        # Set background color for the content slide
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*bg_color)

    # Save presentation to BytesIO
    pptx_buffer = io.BytesIO()
    prs.save(pptx_buffer)
    pptx_buffer.seek(0)
    return pptx_buffer

def main():
    st.title("Automated PowerPoint Presentation Generator")

    # Sidebar for customization options
    st.sidebar.header("Customize Your Presentation")
    heading_color = st.sidebar.color_picker("Choose Heading Color", "#000000")
    heading_size = st.sidebar.slider("Heading Font Size", 20, 60, 30)
    heading_font = st.sidebar.selectbox("Select Heading Font", 
                                        ["Arial", "Helvetica", "Times New Roman", "Courier New", "Georgia", "Verdana", 
                                         "Trebuchet MS", "Calibri", "Cambria", "Garamond", "Comic Sans MS", 
                                         "Palatino Linotype", "Tahoma", "Lucida Sans Unicode", "Impact", 
                                         "Franklin Gothic Medium", "Segoe UI", "Optima", "Baskerville", "Bookman","Algerian"])
    content_color = st.sidebar.color_picker("Choose Content Color", "#000000")
    content_size = st.sidebar.slider("Content Font Size", 10, 40, 20)
    content_font = st.sidebar.selectbox("Select Content Font", 
                                        ["Arial", "Helvetica", "Times New Roman", "Courier New", "Georgia", "Verdana", 
                                         "Trebuchet MS", "Calibri", "Cambria", "Garamond", "Comic Sans MS", 
                                         "Palatino Linotype", "Tahoma", "Lucida Sans Unicode", "Impact", 
                                         "Franklin Gothic Medium", "Segoe UI", "Optima", "Baskerville", "Bookman","Algerian"])
    bg_color = st.sidebar.color_picker("Choose Background Color", "#FFFFFF")

    # Convert hex to RGB
    heading_rgb = tuple(int(heading_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    content_rgb = tuple(int(content_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    bg_rgb = tuple(int(bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    # Define the content
    content = {
        "Title": [
            "Automated Presentation Slide Generation from Research Papers using NLP and Deep Learning",
            "Atul Shreewastav, Bidhan Acharya, Nischal Paudel, Yugratna Humagain",
            "Department of Electronics and Computer Engineering, IOE, Thapathali Campus",
            "May 13, 2024"
        ],
        "Abstract": [
            "Novel approach for automating generation of presentation slides from academic research papers",
            "Leveraging NLP techniques, specifically a fine-tuned T5 transformer model",
            "Custom dataset of research articles used for training the model",
            "Enables automatic conversion into concise and informative slides",
            "Potential impact on summarizing and communicating technical information within research community"
        ],
        "Introduction": [
            "Communication of complex information in professional and educational settings relies on clear presentations",
            "Manual creation of presentations time-consuming and resource-intensive",
            "NLP advancements offer opportunities for automating content extraction and organization",
            "Proposal of automated slide generation methodology using fine-tuned T5 transformer model",
            "Aim to empower users to focus on content creation and knowledge dissemination"
        ],
        "Methodology": [
            "Challenges associated with manual slide creation addressed using NLP techniques",
            "Fine-tuned T5 transformer model utilized for extracting key information and summarizing content",
            "Model trained on custom dataset of research articles for proficiency in text-to-text transfer tasks",
            "Approach enables automatic conversion of research articles into well-structured presentation slides"
        ],
        "Related Work": [
            "Active research area in automating generation of presentation slides from research papers",
            "Examples of existing approaches like PPSGen, Learning Based Slide Generator, and DOC2PPT",
            "Emphasis on factual accuracy, machine learning techniques, and analyzing paper structure for slide generation",
            "Various methods explored for automatic slide generation from scientific documents"
        ],
        "Results": [
            "Successful implementation of automated slide generation methodology",
            "Extraction of key information and creation of concise slides demonstrated",
            "Comparison of manually created slides with those generated automatically",
            "Improved efficiency and clarity in presentation creation process observed"
        ],
        "Conclusions": [
            "Novel approach using NLP and deep learning techniques for automating slide generation from research papers",
            "Potential to revolutionize how technical information is summarized and communicated",
            "Future directions include enhancing the model's capabilities and expanding to other domains",
            "Contributions to efficient and effective presentation creation process for professional and educational contexts"
        ]
    }

    # Generate button
    if st.button("Generate Presentation"):
        pptx_file = create_ppt(content, heading_rgb, heading_size, bg_rgb, content_rgb, content_size, heading_font, content_font)
        st.download_button(label="Download Presentation", data=pptx_file, file_name="generated_presentation.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
        st.success("Presentation generated successfully!")

if __name__ == "_main_":
    main()