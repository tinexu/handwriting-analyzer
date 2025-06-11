import streamlit as st
import os
from PIL import Image
import io
import google.generativeai as genai
from google.cloud import vision
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Set page config
st.set_page_config(
    page_title="Handwriting Analyzer",
    page_icon="✍️",
    layout="wide"
)

# Title and description
st.title("✍️ AI Handwriting Analyzer")
st.write("Upload a photo of your handwritten text for intelligent analysis and suggestions!")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image of handwritten text", 
    type=['png', 'jpg', 'jpeg'],
    help="Take a clear photo of your handwritten notes, essay, or brainstorm"
)

# Camera input (works on mobile browsers)
camera_photo = st.camera_input("Or take a photo now")

# Use camera photo if available, otherwise use uploaded file
image_source = camera_photo if camera_photo else uploaded_file

if image_source is not None:
    # Display the image
    image = Image.open(image_source)
    st.image(image, caption="Your handwritten text", use_column_width=True)
    
    # Add analysis button
    if st.button("🔍 Analyze Handwriting", type="primary"):
        with st.spinner("Analyzing your handwriting..."):
            # TODO: Add OCR and AI analysis here
            st.success("Analysis complete!")
            st.write("**Extracted Text:** (Coming soon...)")
            st.write("**AI Analysis:** (Coming soon...)")

# Sidebar with instructions
with st.sidebar:
    st.header("📝 How to use")
    st.write("1. Take a clear photo of your handwritten text")
    st.write("2. Upload it or use the camera")
    st.write("3. Click 'Analyze' to get AI suggestions")
    
    st.header("✨ Features")
    st.write("• Grammar and spelling analysis")
    st.write("• Sentence structure suggestions")
    st.write("• Content organization tips")
    st.write("• Writing flow improvements")