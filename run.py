#!/usr/bin/env python3
"""
Simple startup script for the translation app
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    print("🚀 Starting English to Hindi Translation App...")
    print("📁 Created upload and output directories")
    print("🌐 Access the app at: http://localhost:8000")
    print("📖 Upload Excel/CSV files to translate English to Hindi")
    print("=" * 50)
    
    # Run the app
    app.run(
        debug=True,
        host='127.0.0.1',
        port=8000,
        threaded=True
    )
