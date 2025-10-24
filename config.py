import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Sarvam AI Configuration
    SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', 'sk_li69ptgl_pZ0qdiBl1G7OYSTsskigWibF')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # File Upload Settings
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'outputs'
    
    # Translation Settings
    SOURCE_LANGUAGE = 'en-IN'
    TARGET_LANGUAGE = 'od-IN'
    TRANSLATION_MODEL = 'sarvam-translate:v1'
    TRANSLATION_MODE = 'formal'
