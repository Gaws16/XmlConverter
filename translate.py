import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Google Translate client
def initialize_translate_client():
    # For API Key Authentication or Service Account Key
    translate_client = translate.Client()
    return translate_client

def translate_name_with_google(name, target_language="bg"):
    # Initialize the translation client
    translate_client = initialize_translate_client()
    
    # Translate the text (only the product name)
    result = translate_client.translate(name, target_language=target_language)
    
    return result['translatedText']
