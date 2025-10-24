# English to Hindi Translation Web App

A web application that translates English text from Excel/CSV files to Hindi using Sarvam AI API.

## Features

- 🌐 **Web Interface**: User-friendly drag-and-drop file upload
- 📊 **Excel/CSV Support**: Handles .xlsx, .xls, and .csv files
- 🔄 **Multi-Language Translation**: Supports 10+ Indian languages
- 🔊 **Audio Generation**: Create audio files from translated text
- 🎤 **Voice Selection**: Choose from different speaker voices
- 📥 **Instant Download**: Get translated files and audio files immediately
- 🐳 **Docker Ready**: Easy deployment with Docker
- 🚀 **Production Ready**: Configured for deployment

## Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Open in Browser**
   ```
   http://localhost:8080
   ```

### Docker Deployment

1. **Build and Run with Docker**
   ```bash
   docker-compose up --build
   ```

2. **Access the Application**
   ```
   http://localhost:8080
   ```

## Usage

1. **Upload File**: Drag and drop or click to select an Excel/CSV file
2. **Automatic Processing**: The app will translate the first column from English to Hindi
3. **Download Results**: Get your translated file with a new "Translated_Hindi" column

## File Format

Your Excel/CSV file should have English text in the first column. The app will:
- Read the first column
- Translate each row from English to Hindi
- Add a new "Translated_Hindi" column with the results
- Preserve all other columns and data

## API Endpoints

- `GET /` - Main web interface
- `POST /upload` - File upload and translation
- `GET /download/<filename>` - Download translated file
- `GET /health` - Health check

## Configuration

### Environment Variables

Create a `.env` file (optional):
```env
SARVAM_API_KEY=your_sarvam_api_key
FLASK_ENV=production
MAX_CONTENT_LENGTH=16777216
```

### Translation Settings

The app translates from English (en-IN) to Hindi (od-IN) using:
- Model: sarvam-translate:v1
- Mode: formal
- Preprocessing: enabled

## Deployment Options

### 1. Local Development
```bash
python app.py
```

### 2. Docker
```bash
docker-compose up -d
```

### 3. Cloud Deployment
- **Heroku**: Add Procfile and deploy
- **AWS**: Use ECS with the Dockerfile
- **Google Cloud**: Use Cloud Run with the Dockerfile
- **Azure**: Use Container Instances

## File Structure

```
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── config.py           # Configuration settings
└── README.md           # This file
```

## Requirements

- Python 3.9+
- Sarvam AI API Key
- Modern web browser

## Troubleshooting

### Common Issues

1. **File Upload Fails**
   - Check file size (max 16MB)
   - Ensure file is .xlsx, .xls, or .csv
   - Check file is not corrupted

2. **Translation Errors**
   - Verify Sarvam API key is correct
   - Check internet connection
   - Ensure first column contains text data

3. **Docker Issues**
   - Ensure Docker is running
   - Check port 5000 is available
   - Verify Dockerfile syntax

### Support

For issues or questions:
1. Check the console logs
2. Verify API key configuration
3. Test with a simple Excel file first

## License

This project is for educational and personal use.
