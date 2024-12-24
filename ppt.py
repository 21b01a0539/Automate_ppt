from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
import streamlit as st
import io

def create_ppt(content, heading_color, heading_size, background_color, content_color, content_size, heading_font, content_font):
    """
    Create a PowerPoint presentation based on the given content and style parameters.
    """
    prs = Presentation()

    for slide_title, slide_content in content.items():
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank slide layout
        slide_bg = slide.background
        fill = slide_bg.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*background_color)

        # Add heading (title)
        title = slide.shapes.title or slide.shapes.add_textbox(0, 0, prs.slide_width, Pt(50))
        title.text = slide_title
        title_frame = title.text_frame
        title_frame.paragraphs[0].font.size = Pt(heading_size)
        title_frame.paragraphs[0].font.color.rgb = RGBColor(*heading_color)
        title_frame.paragraphs[0].font.name = heading_font

        # Add content
        left = Pt(50)
        top = Pt(100)
        width = prs.slide_width - Pt(100)
        height = prs.slide_height - Pt(150)

        content_box = slide.shapes.add_textbox(left, top, width, height)
        content_frame = content_box.text_frame
        content_frame.word_wrap = True

        for paragraph in slide_content:
            p = content_frame.add_paragraph()
            p.text = paragraph
            p.font.size = Pt(content_size)
            p.font.color.rgb = RGBColor(*content_color)
            p.font.name = content_font

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
        "Slide 1: Title": [
            "Automated Presentation Slide Generation from Research Papers using NLP and Deep Learning",
            "Atul Shreewastav, Bidhan Acharya, Nischal Paudel, Yugratna Humagain",
            "Department of Electronics and Computer Engineering, IOE, Thapathali Campus",
            "May 13, 2024"
        ],
        "Slide 2: Abstract": [
            "Novel approach for automating generation of presentation slides from academic research papers",
            "Leveraging NLP techniques, specifically a fine-tuned T5 transformer model",
            "Custom dataset of research articles used for training the model",
            "Enables automatic conversion into concise and informative slides",
            "Potential impact on summarizing and communicating technical information within research community"
        ],
        "Slide 3: Introduction": [
            "Communication of complex information in professional and educational settings relies on clear presentations",
            "Manual creation of presentations time-consuming and resource-intensive",
            "NLP advancements offer opportunities for automating content extraction and organization",
            "Proposal of automated slide generation methodology using fine-tuned T5 transformer model",
            "Aim to empower users to focus on content creation and knowledge dissemination"
        ],
        "Slide 4: Methodology": [
            "Challenges associated with manual slide creation addressed using NLP techniques",
            "Fine-tuned T5 transformer model utilized for extracting key information and summarizing content",
            "Model trained on custom dataset of research articles for proficiency in text-to-text transfer tasks",
            "Approach enables automatic conversion of research articles into well-structured presentation slides"
        ],
        "Slide 5: Related Work": [
            "Active research area in automating generation of presentation slides from research papers",
            "Examples of existing approaches like PPSGen, Learning Based Slide Generator, and DOC2PPT",
            "Emphasis on factual accuracy, machine learning techniques, and analyzing paper structure for slide generation",
            "Various methods explored for automatic slide generation from scientific documents"
        ],
        "Slide 6: Results": [
            "Successful implementation of automated slide generation methodology",
            "Extraction of key information and creation of concise slides demonstrated",
            "Comparison of manually created slides with those generated automatically",
            "Improved efficiency and clarity in presentation creation process observed"
        ],
        "Slide 7: Conclusions": [
            "Novel approach using NLP and deep learning techniques for automating slide generation from research papers",
            "Potential to revolutionize how technical information is summarized and communicated",
            "Future directions include enhancing the model's capabilities and expanding to other domains",
            "Contributions to efficient and effective presentation creation process for professional and educational contexts"
        ]
    }
    text = {'Slide 1: Title Slide': ['Presentify: Automated Presentation Slide Generation from Research Papers using NLP and Deep Learning', 'Authors: Atul Shreewastav, Bidhan Acharya, Nischal Paudel, and Yugratna Humagain', 'Department of Electronics and Computer Engineering, IOE, Thapathali Campus'], 'Slide 2: Introduction': ['The study presents a novel approach for automating the generation of presentation slides from academic research papers.', 'The approach leverages Natural Language Processing (NLP) techniques, particularly a fine-tuned T5 transformer model.', 'The research aims to impact how technical information is summarized and communicated within the research community.'], 'Slide 3: Table of Contents': ['Introduction', 'Related Work', 'Methodology', 'Results', 'Discussion', 'Conclusion'], 'Slide 4: Methodology': ['The research addresses the challenges associated with manual slide creation.', 'A fine-tuned T5 transformer model is used to extract key information, summarize content, and generate well-structured presentation slides.', 'This approach aims to empower users to focus on content creation and knowledge dissemination by automating the tasks of information extraction and formatting.'], 'Slide 5: Results': ['The model, trained on a custom dataset of research articles, extracts key information and transforms it into well-structured presentation slides.', 'The T5 model’s proficiency in text-to-text transfer tasks is enhanced through fine-tuning with domain-specific metrics.', 'The approach enables the automatic conversion of research articles into concise and informative presentation slides.'], 'Slide 6: Discussion': ['The study contributes to a more efficient and effective presentation creation process, benefiting diverse professional and educational contexts.', 'The research has the potential to significantly impact how technical information is summarized and communicated within the research community.', 'The approach fosters greater efficiency and clarity in knowledge dissemination.'], 'Slide 7: Conclusion': ['The research presents a novel approach for automating the generation of presentation slides from academic research papers using NLP and Deep Learning.', 'The approach has the potential to significantly impact how technical information is summarized and communicated within the research community.', 'The study contributes to a more efficient and effective presentation creation process, benefiting diverse professional and educational contexts.'], 'Slide 8: References': ['PPSGen, Learning-Based Presentation Slides Generation for Academic Papers', 'Learning Based Slide Generator', 'Technique for Generating Automatic Slides on the basis of Paper Structure Analysis', 'DOC2PPT: Automatic Presentation Slides Generation from Scientific Documents']}

    # Generate button
    if st.button("Generate Presentation"):
        pptx_file = create_ppt(text, heading_rgb, heading_size, bg_rgb, content_rgb, content_size, heading_font, content_font)
        st.download_button(label="Download Presentation", data=pptx_file, file_name="generated_presentation.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
        st.success("Presentation generated successfully!")

if __name__ == "__main__":
    main()