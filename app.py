import os
import pandas as pd
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from sarvamai import SarvamAI
from sarvamai.play import save
import tempfile
import zipfile
import wave
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['AUDIO_FOLDER'] = 'audio_outputs'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# Sarvam API configuration
SARVAM_API_KEY = "sk_li69ptgl_pZ0qdiBl1G7OYSTsskigWibF"
sarvam_client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepend_silence(wav_path, output_path, silence_duration_ms=200):
    """Add silence to the beginning of audio file"""
    with wave.open(wav_path, 'rb') as wf:
        params = wf.getparams()
        audio_data = wf.readframes(wf.getnframes())

    sample_rate = params.framerate
    n_channels = params.nchannels
    sampwidth = params.sampwidth
    silence_frames = int(sample_rate * silence_duration_ms / 1000) * n_channels
    silence = (b'\x00' * sampwidth) * silence_frames

    with wave.open(output_path, 'wb') as wf_out:
        wf_out.setparams(params)
        wf_out.writeframes(silence + audio_data)

def generate_audio_from_text(text, row_number, session_folder, language_code="od-IN", speaker="anushka"):
    """Generate audio from text using Sarvam TTS"""
    try:
        print(f"🔊 Generating audio for Row {row_number}: {text}")
        
        response = sarvam_client.text_to_speech.convert(
            text=text,
            target_language_code=language_code,
            speaker=speaker,
            enable_preprocessing=True,
        )

        # Use the provided session folder
        os.makedirs(session_folder, exist_ok=True)
        
        temp_path = os.path.join(session_folder, f"row_{row_number}_raw.wav")
        final_path = os.path.join(session_folder, f"row_{row_number}.wav")

        save(response, temp_path)
        prepend_silence(temp_path, final_path)
        os.remove(temp_path)
        
        return final_path
        
    except Exception as e:
        print(f"❌ Error generating audio for Row {row_number}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload Excel (.xlsx, .xls) or CSV files.'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get processing options
        generate_audio = request.form.get('generate_audio', 'false').lower() == 'true'
        target_language = request.form.get('target_language', 'od-IN')
        speaker = request.form.get('speaker', 'anushka')
        
        # Process the file
        result = process_file(filepath, generate_audio, target_language, speaker)
        
        return jsonify({
            'success': True,
            'message': 'File processed successfully',
            'download_url': f'/download/{result["output_filename"]}',
            'translated_count': result['translated_count'],
            'total_rows': result['total_rows'],
            'audio_generated': result.get('audio_generated', False),
            'audio_session': result.get('audio_session', None)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_file(filepath, generate_audio=False, target_language="od-IN", speaker="anushka"):
    """Process the uploaded Excel/CSV file and translate the first column"""
    try:
        # Read the file
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        # Get the first column (assuming it contains English text)
        first_column = df.iloc[:, 0]
        english_texts = first_column.dropna().tolist()
        
        # Create output dataframe
        output_df = df.copy()
        output_df['Translated_Hindi'] = ''
        
        translated_count = 0
        audio_session = None
        audio_files = []
        
        # Create session folder for audio if needed
        if generate_audio:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_session = os.path.join(app.config['AUDIO_FOLDER'], f"session_{timestamp}")
            os.makedirs(audio_session, exist_ok=True)
        
        # Translate each text
        for i, text in enumerate(english_texts):
            try:
                print(f"🔄 Translating Row {i + 1}: {text}")
                
                response = sarvam_client.text.translate(
                    input=str(text),
                    source_language_code="en-IN",
                    target_language_code=target_language,
                    model="sarvam-translate:v1",
                    mode="formal",
                    enable_preprocessing=True
                )
                
                hindi_text = response.translated_text
                output_df.iloc[i, -1] = hindi_text  # Update the last column
                translated_count += 1
                print(f"✅ Row {i + 1} Hindi: {hindi_text}")
                
                # Generate audio if requested
                if generate_audio and hindi_text and audio_session:
                    audio_path = generate_audio_from_text(
                        hindi_text, i + 1, audio_session, target_language, speaker
                    )
                    if audio_path:
                        audio_files.append(audio_path)
                
            except Exception as e:
                print(f"❌ Failed for Row {i + 1}: {e}")
                output_df.iloc[i, -1] = f"Translation failed: {str(e)}"
        
        # Save the translated file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"translated_{timestamp}.xlsx"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        output_df.to_excel(output_path, index=False)
        
        result = {
            'output_filename': output_filename,
            'translated_count': translated_count,
            'total_rows': len(english_texts)
        }
        
        if generate_audio and audio_session:
            result['audio_generated'] = True
            # Extract just the session folder name for the URL
            session_name = os.path.basename(audio_session)
            result['audio_session'] = session_name
            result['audio_count'] = len(audio_files)
        
        return result
        
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

@app.route('/download/<filename>')
def download_file(filename):
    """Download the translated file"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_audio/<session_id>/<row_number>')
def download_audio(session_id, row_number):
    """Download individual audio file by row number"""
    try:
        # Handle session path - session_id should already be the folder name
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], session_id, f"row_{row_number}.wav")
        
        if os.path.exists(audio_path):
            return send_file(
                audio_path, 
                as_attachment=True, 
                download_name=f"audio_row_{row_number}.wav",
                mimetype='audio/wav'
            )
        else:
            return jsonify({'error': f'Audio file not found: {audio_path}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_all_audio/<session_id>')
def download_all_audio(session_id):
    """Download all audio files as a zip"""
    try:
        # Handle session path - session_id should already be the folder name
        session_folder = os.path.join(app.config['AUDIO_FOLDER'], session_id)
        
        if not os.path.exists(session_folder):
            return jsonify({'error': f'Audio session not found: {session_folder}'}), 404
        
        # Create zip file in a temporary location
        import tempfile
        temp_dir = tempfile.gettempdir()
        zip_filename = f"audio_files_{session_id}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)
        
        # Create the zip file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            audio_files_found = 0
            for root, dirs, files in os.walk(session_folder):
                for file in files:
                    if file.endswith('.wav'):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, session_folder)
                        zipf.write(file_path, arcname)
                        audio_files_found += 1
            
            if audio_files_found == 0:
                return jsonify({'error': 'No audio files found in session'}), 404
        
        # Send the zip file
        return send_file(
            zip_path, 
            as_attachment=True, 
            download_name=zip_filename,
            mimetype='application/zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_audio/<session_id>')
def list_audio_files(session_id):
    """List all audio files in a session"""
    try:
        # Handle session path - session_id should already be the folder name
        session_folder = os.path.join(app.config['AUDIO_FOLDER'], session_id)
        
        if not os.path.exists(session_folder):
            return jsonify({'error': f'Audio session not found: {session_folder}'}), 404
        
        audio_files = []
        for file in os.listdir(session_folder):
            if file.endswith('.wav'):
                row_number = file.replace('row_', '').replace('.wav', '')
                audio_files.append({
                    'filename': file,
                    'row_number': row_number,
                    'download_url': f'/download_audio/{session_id}/{row_number}'
                })
        
        return jsonify({'audio_files': audio_files})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/debug_audio/<session_id>')
def debug_audio(session_id):
    """Debug endpoint to check audio files"""
    try:
        session_folder = os.path.join(app.config['AUDIO_FOLDER'], session_id)
        
        if not os.path.exists(session_folder):
            return jsonify({'error': f'Session folder not found: {session_folder}'}), 404
        
        files = []
        for file in os.listdir(session_folder):
            file_path = os.path.join(session_folder, file)
            files.append({
                'name': file,
                'exists': os.path.exists(file_path),
                'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
            })
        
        return jsonify({
            'session_folder': session_folder,
            'files': files
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
