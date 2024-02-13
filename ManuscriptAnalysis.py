from dotenv import load_dotenv
load_dotenv()  # load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from googletrans import Translator

# Initialize Google API key for translation
translator = Translator()

# Configure Google API for OpenAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, image[0]])
    return response.text

# Function to set up image data
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set page title and header
st.set_page_config(page_title="Mike App", page_icon=":apple:")
st.header("Manuscript analyzer")

# Define input prompt
input_prompt = """Assist me in identitying an image and providing a detailed explanation of its content. Additionally, I need the text within the image translated into 300 words After the translation explain the output in Simple term."""

# File upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Language selection
selected_language = st.selectbox("Select Language:", ["English", "Telugu", "Hindi"])

# Submit button
submit = st.button("Translate")

# Custom CSS
custom_css = """
<style>
.stButton>button {
    background-color: white;
    color: orange;
    padding: 10px 20px;
    border: 2px solid orange; /* Set border color */
    border-radius: 5px;
    cursor: pointer;
    text-decoration: none;
    transition: transform 0.3s, background-color 0.3s;
}

.stButton>button:hover {
    transform: translateY(-2px); /* Uplift effect */
    background-color: orange; /* Change background color on hover */
    colour:black;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# If submit button is clicked
if submit:
    if image:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(image_data, input_prompt)

        # Translation based on selected language
        if selected_language != "English":
            translated_response = translator.translate(response, dest=selected_language.lower())
            st.subheader("Translated Response:")
            st.write(translated_response.text)
        else:
            st.subheader("The Response is:")
            st.write(response)