# Deployment Guide for Render

## Quick Deploy to Render

1. **Fork/Clone this repository**
2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Create a new Web Service

3. **Configure the service:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`
   - **Environment**: Python 3.9

4. **Environment Variables:**
   - `SARVAM_API_KEY`: Your Sarvam API key
   - `PORT`: (Auto-set by Render)

## Alternative Deployment Methods

### Using Docker
```bash
docker build -t translation-app .
docker run -p 8000:8000 -e SARVAM_API_KEY=your_key translation-app
```

### Using Docker Compose
```bash
docker-compose up --build
```

### Local Development
```bash
pip install -r requirements.txt
python run.py
```

## Troubleshooting

### Common Issues:

1. **ImportError: cannot import name 'SarvamAI'**
   - The app now handles this gracefully with fallback mode
   - Check if sarvamai package is properly installed

2. **Worker failed to boot**
   - Check the logs for specific error messages
   - Ensure all dependencies are in requirements.txt

3. **Audio generation not working**
   - Verify SarvamAI API key is set correctly
   - Check if the API key has sufficient credits

### Health Check Endpoints:
- `/health` - Basic health check
- `/status` - Detailed status including SarvamAI availability

## Features:
- ✅ Multi-language translation (10+ Indian languages)
- ✅ Audio generation with TTS
- ✅ Excel/CSV file processing
- ✅ Individual and bulk audio downloads
- ✅ Graceful fallback when SarvamAI is unavailable
- ✅ Production-ready with proper error handling
