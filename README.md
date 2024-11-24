Project: Guardian Vision Documentation
Introduction
Guardian Vision is an AI-powered web application designed to assist visually impaired individuals. 
It leverages advanced technologies to analyze images, extract text, and provide voice-based assistance. 
This application is built using Streamlit, integrates Google Generative AI (Gemini model), and includes the LangChain library to enhance scene understanding.
 
Features
1.	Scene Analysis: Generates a detailed description of the uploaded image.
2.	Text Extraction: Uses Optical Character Recognition (OCR) to extract text from images.
3.	Voice Narration: Converts text and scene descriptions into speech.

Technologies Used
1.	Streamlit: For creating a user-friendly web interface.
2.	PyTesseract: For OCR to extract text from images.
3.	Google Generative AI (Gemini): For generating detailed scene descriptions.
4.	LangChain: For managing prompts and improving the AI's context understanding.
5.	pyttsx3: For text-to-speech conversion.

Code Explanation
Below is a detailed breakdown of the code with explanations.
1.	Setting Up Dependencies
import streamlit as st
import pyttsx3
import threading
from PIL import Image
import pytesseract
import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate
•	Streamlit (st): Builds the app's interface.
•	pyttsx3: A Python library for speech synthesis.
•	threading: Ensures the text-to-speech process does not block the app.
•	Pillow (Image): Processes image files.
•	pytesseract: Performs OCR for text extraction.
•	google.generativeai: Connects to Google Gemini for content generation.
•	LangChain: Creates structured prompts for AI tasks.

2.	Configuring External Tools
Tesseract OCR Path:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
•	Specifies the location of the Tesseract OCR executable. Update this path based on your system setup.
Google Generative AI API Key:
genai.configure(api_key="YOUR_API_KEY")
•	Replace "YOUR_API_KEY" with your valid Google API key.

3.	Streamlit App Configuration
st.set_page_config(page_title="Guardian Vision")





•	Sets the title of the web app.

st.title("Project: Guardian Vision")
st.markdown(
    """
    <h3 style='font-size:18px; font-weight:normal;'>
    An AI Powered by Gemini for Scene Interpretation, Text Extraction & Speech Assistance for the Visually Impaired
    </h3>
    """, 
    unsafe_allow_html=True
)
•	Displays the app title and a description.

4.	LangChain Prompt for Scene Analysis

langchain_prompt_template = PromptTemplate(
    input_variables=["user_context"],
    template="""
    As an AI assistant, you assist visually impaired users by interpreting the content of images. 
    User Context: {user_context}
    
    Please provide:
    1. A list of identified items in the image along with their purposes/functions.
    2. Overall description of the image.
    3. Recommendations/Suggestions for actions or safety measures/precautions for the visually impaired.
    """
)
•	LangChain PromptTemplate: Structures prompts for Google Generative AI to produce clear, user-focused scene descriptions.

5. Functionality
Extract Text from Image
def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)
•	Uses PyTesseract to extract text from the uploaded image.

Convert Text to Speech
def text_to_speech(text):
    """Convert text to speech and speak it."""
    def speak():
        local_engine = pyttsx3.init()
        local_engine.setProperty("rate", 150)
        local_engine.say(text)
        local_engine.runAndWait()
        local_engine.stop()

    threading.Thread(target=speak, daemon=True).start()
•	Converts text into spoken words using pyttsx3.
•	Threading ensures this process doesn't block the app.

Generate Scene Description
def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text
•	Sends a LangChain-generated prompt and image data to the Gemini model.
•	Returns the AI-generated description.

Prepare Uploaded Image
def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")
•	Processes the uploaded file into a format compatible with the AI model.




5.	User Interface
Image Upload Section
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
•	Allows users to upload an image. Displays the uploaded image.
Interactive Buttons
scene_button = col1.button("🖼️ Scene Analysis")
ocr_button = col2.button("📜 Text Extraction")
tts_button = col3.button("🔈 Voice Narration")
•	Provides buttons for: 
o	Scene Analysis: Generates a description.
o	Text Extraction: Extracts text using OCR.
o	Voice Narration: Reads text aloud.
7. Handling User Interactions
Scene Analysis
if scene_button:
    with st.spinner("🖼️ Generating scene description..."):
        scene_description = generate_scene_description(input_prompt, image_data)
        st.session_state.scene_description = scene_description
        st.markdown("### 🖼️ Scene Description")
        st.success(scene_description)
        text_to_speech(scene_description)
•	Displays a loading spinner while generating a scene description.
•	Saves the description to session state and reads it aloud.
Text Extraction
if ocr_button:
    with st.spinner("📜 Extracting text from the image..."):
        ocr_text = extract_text_from_image(image)
        st.session_state.ocr_text = ocr_text
        st.markdown("### 📜 Extracted Text")
        st.text_area("Extracted Text", ocr_text, height=150)
        text_to_speech(ocr_text)
•	Extracts text, saves it, and reads it aloud.
Voice Narration
if tts_button:
    if st.session_state.scene_description:
        text_to_speech(st.session_state.scene_description)
    elif st.session_state.ocr_text:
        text_to_speech(st.session_state.ocr_text)
    else:
        st.warning("⚠️ Please generate a scene description or extract text first.")
•	Speaks the available scene description or OCR text.

How to Use
1.	Upload an Image: Upload a JPG, JPEG, or PNG file.
2.	Select Features: 
o	Scene Analysis: Get a description of the image.
o	Text Extraction: Extract text from the image.
o	Voice Narration: Hear the results read aloud.
3.	Listen to Outputs: Use headphones for better clarity.

Conclusion
This project demonstrates how AI can assist visually impaired individuals by combining image analysis, text extraction, and speech synthesis into one seamless application.

