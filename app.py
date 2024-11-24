import streamlit as st
import pyttsx3
import threading
from PIL import Image
import pytesseract
import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Google Generative AI with API Key
genai.configure(api_key="AIzaSyAICv8vBurXD_44UKLFgTJlZcwl4pWG1aA")

# Set page configuration
st.set_page_config(page_title="Guardian Vision")

# Page title and description
st.title("Project: Guardian Vision")
st.markdown(
    """
    <h3 style='font-size:18px; font-weight:normal;'>
    An AI Powered by Gemini for Scene Interpretation, Text Extraction & Speech Assistance for the Visually Impaired
    </h3>
    """, 
    unsafe_allow_html=True
)

# LangChain prompt template for scene understanding
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

# Functions for functionality
def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    """Convert text to speech and speak it."""
    def speak():
        local_engine = pyttsx3.init()  # Initialize a new TTS engine instance
        local_engine.setProperty("rate", 150)  # Set speech rate
        local_engine.say(text)  # Queue the text for speaking
        local_engine.runAndWait()  # Process the queue
        local_engine.stop()  # Stop the engine to release resources

    # Use threading to avoid blocking the app
    threading.Thread(target=speak, daemon=True).start()

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

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

# Upload Image Section
st.markdown("### 🌟 Upload an Image")
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Buttons Section
st.markdown("### 🛠️ Features")
col1, col2, col3 = st.columns(3)

scene_button = col1.button("🖼️ Scene Analysis")
ocr_button = col2.button("📜 Text Extraction")
tts_button = col3.button("🔈 Voice Narration")

# Input Prompt for Scene Understanding
user_context = "Provide detailed information about the image for a visually impaired user."
input_prompt = langchain_prompt_template.format(user_context=user_context)

# Initialize session state variables for scene description and OCR text
if "scene_description" not in st.session_state:
    st.session_state.scene_description = None

if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = None

if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    # Process user interactions
    if scene_button:
        with st.spinner("🖼️ Generating scene description..."):
            scene_description = generate_scene_description(input_prompt, image_data)
            st.session_state.scene_description = scene_description  # Store in session state
            st.markdown("### 🖼️ Scene Description")
            st.success(scene_description)
            text_to_speech(scene_description)  # Play speech for scene description

    if ocr_button:
        with st.spinner("📜 Extracting text from the image..."):
            ocr_text = extract_text_from_image(image)
            st.session_state.ocr_text = ocr_text  # Store in session state
            st.markdown("### 📜 Extracted Text")
            st.text_area("Extracted Text", ocr_text, height=150)
            text_to_speech(ocr_text)  # Play speech for OCR text

    # Text-to-Speech Button: Play audio in Streamlit
    if tts_button:
        if st.session_state.scene_description:  # If scene description is available
            st.info("🔈 Speaking Scene Description...")
            text_to_speech(st.session_state.scene_description)
        elif st.session_state.ocr_text:  # If OCR text is available
            st.info("🔈 Speaking Extracted Text...")
            text_to_speech(st.session_state.ocr_text)
        else:
            st.warning("⚠️ Please generate a scene description or extract text first.")
