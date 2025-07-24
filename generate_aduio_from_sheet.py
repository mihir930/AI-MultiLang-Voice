import os
import wave
import pandas as pd
import numpy as np
import gspread
from sarvamai import SarvamAI
from sarvamai.play import save
from google_auth_oauthlib.flow import InstalledAppFlow

# 1. Google Sheets Setup
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]
CREDS_FILE = "credentials.json"
SHEET_NAME = "TTS_Sheet"  # Replace with your actual Google Sheet name
WORKSHEET_INDEX = 0  # Use 0 for first sheet

flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
creds = flow.run_local_server(port=0)
client_gsheets = gspread.authorize(creds)

sheet = client_gsheets.open(SHEET_NAME).get_worksheet(WORKSHEET_INDEX)
data = sheet.get_all_records()
df = pd.DataFrame(data)

# 2. Sarvam API Setup
SARVAM_API_KEY = "sk_li69ptgl_pZ0qdiBl1G7OYSTsskigWibF"  # Replace with your Sarvam API Key
client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

# 3. Output Folder Setup
output_folder = "translated_audio"
os.makedirs(output_folder, exist_ok=True)

# 4. Silence Prepend Function
def prepend_silence(wav_path, output_path, silence_duration_ms=200):
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

# 5. Audio Generation Loop
if "Final Hindi" not in df.columns:
    raise ValueError("❌ 'Final Hindi' column not found in Google Sheet. Please ensure it's present.")

for idx, row in df.iterrows():
    text = str(row["Final Hindi"]).strip()
    if not text or text.lower() == "nan":
        continue

    print(f"\n🔊 Generating audio for Row {idx + 1}: {text}")
    try:
        response = client.text_to_speech.convert(
            text=text,
            target_language_code="od-IN",
            speaker="anushka",
            enable_preprocessing=True,
        )

        temp_path = os.path.join(output_folder, f"row_{idx + 1}_raw.wav")
        final_path = os.path.join(output_folder, f"row_{idx + 1}.wav")

        save(response, temp_path)
        prepend_silence(temp_path, final_path)
        os.remove(temp_path)

    except Exception as e:
        print(f"❌ Error generating audio for Row {idx + 1}: {e}")

print("\n✅ All done! Check your 'translated_audio' folder.")
