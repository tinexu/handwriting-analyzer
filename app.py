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

# OCR Function
def extract_text_from_image(image_source):
    """Extract text from image using Google Cloud Vision API"""
    try:
        # Initialize Vision API client
        client = vision.ImageAnnotatorClient()
        
        # Convert image to bytes
        if hasattr(image_source, 'getvalue'):
            content = image_source.getvalue()
        else:
            img_byte_arr = io.BytesIO()
            image = Image.open(image_source)
            image.save(img_byte_arr, format='PNG')
            content = img_byte_arr.getvalue()
        
        # Create Vision API image object
        image = vision.Image(content=content)
        
        # Perform text detection
        response = client.text_detection(image=image)
        
        if response.error.message:
            raise Exception(f"Vision API error: {response.error.message}")
            
        # Extract text
        texts = response.text_annotations
        if texts:
            return texts[0].description.strip()
        else:
            return None
            
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return None

# AI Analysis Function
def analyze_text_with_gemini(text):
    """Analyze text using Google Gemini API"""
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create analysis prompt
        prompt = f"""
        Analyze this handwritten text and provide helpful suggestions:
        
        Text: "{text}"
        
        Please provide:
        1. Grammar and spelling corrections (if any)
        2. Sentence structure improvements
        3. Content organization suggestions
        4. Overall writing flow assessment
        5. Any ideas for expanding or restructuring the content
        
        Be constructive and encouraging in your feedback.
        """
        
        # Generate analysis
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        st.error(f"Error analyzing text: {str(e)}")
        return "Sorry, I couldn't analyze the text right now. Please try again."

if image_source is not None:
    # Display the image
    image = Image.open(image_source)
    st.image(image, caption="Your handwritten text", use_column_width=True)
    
    # Add analysis button
    if st.button("🔍 Analyze Handwriting", type="primary"):
        with st.spinner("Extracting text from your handwriting..."):
            # Extract text using Google Vision API
            extracted_text = extract_text_from_image(image_source)
            
            if extracted_text:
                st.success("Text extracted successfully!")
                st.write("**Extracted Text:**")
                st.write(f"_{extracted_text}_")
                
                # Analyze with Gemini
                with st.spinner("Analyzing your writing with AI..."):
                    analysis = analyze_text_with_gemini(extracted_text)
                    
                    st.write("**AI Analysis & Suggestions:**")
                    st.write(analysis)
            else:
                st.error("Could not extract text from the image. Please try a clearer photo.")

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