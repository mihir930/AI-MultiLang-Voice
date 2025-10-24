#!/usr/bin/env python3
"""
Simple test script to verify the translation app works correctly
"""

import os
import pandas as pd
import tempfile
from app import process_file

def create_test_excel():
    """Create a test Excel file with sample English text"""
    test_data = {
        'English_Text': [
            'Hello, how are you?',
            'Good morning',
            'Thank you very much',
            'Have a nice day',
            'See you later'
        ]
    }
    
    df = pd.DataFrame(test_data)
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    df.to_excel(temp_file.name, index=False)
    temp_file.close()
    
    return temp_file.name

def test_translation():
    """Test the translation functionality"""
    print("🧪 Testing Translation App...")
    
    try:
        # Create test file
        test_file = create_test_excel()
        print(f"✅ Created test file: {test_file}")
        
        # Test file processing
        result = process_file(test_file)
        print(f"✅ Translation completed!")
        print(f"   - Translated: {result['translated_count']} rows")
        print(f"   - Total rows: {result['total_rows']}")
        print(f"   - Output file: {result['output_filename']}")
        
        # Clean up
        os.unlink(test_file)
        print("✅ Test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_translation()
    exit(0 if success else 1)
