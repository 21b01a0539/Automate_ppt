# 📊 PPT Generator – Streamlit Web App

Create stunning PowerPoint presentations effortlessly using **AI-powered tools**. Choose between:
- 🧠 **Research Paper to PPT**
- 🎤 **Voice to PPT**

This app uses **OpenAI's LLM** and **Pixel API** to intelligently summarize and generate slides.

---

## 🚀 Features

- 📄 Upload a research paper (PDF) and convert it into a professional PowerPoint presentation.
- 🎙️ Record voice or provide transcribed content to auto-generate slides.
- 🧠 Uses **OpenAI** for natural language processing and summarization.
- 🖼️ Uses **Pixel API** to generate contextual visuals for your slides.
- 🌐 Stylish UI built with **Streamlit** and animated CSS for a smooth UX.

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ppt-generator.git
   cd ppt-generator
   ```

2. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API keys**

   Create a `.streamlit/secrets.toml` file:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key"
   PIXEL_API_KEY = "your-pixel-api-key"
   ```

   Or set them as environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export PIXEL_API_KEY="your-pixel-api-key"
   ```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
ppt-generator/
│
├── app.py                        # Main Streamlit homepage
├── pages/
│   ├── researchpaper_to_ppt.py   # Research paper to PPT logic
│   └── speech_to_ppt.py          # Voice to PPT logic
│
├── utils/
│   ├── openai_helper.py          # OpenAI interaction logic
│   └── pixel_helper.py           # Pixel API logic
│
├── assets/                       # CSS, logos, images
├── requirements.txt
└── README.md
---

## ✨ Future Improvements

- Support `.docx` and `.txt` file inputs
- Option for theme customization in slides
- Export to PDF or Google Slides
- Save and retrieve user history

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
