import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from sarvamai import SarvamAI

# --- Step 1: Google Sheets Authentication ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)
client_gsheets = gspread.authorize(creds)

# --- Step 2: Connect to your Google Sheet ---
SHEET_NAME = "TTS_Sheet"  # Replace with your sheet name
WORKSHEET_INDEX = 0
sheet = client_gsheets.open(SHEET_NAME).get_worksheet(WORKSHEET_INDEX)

# --- this is a change ---
# --- Step 3: Read English dialogues ---
english_texts = sheet.col_values(1)[1:]  # Skip header

# --- Step 4: Authenticate Sarvam API ---
sarvam = SarvamAI(api_subscription_key="sk_li69ptgl_pZ0qdiBl1G7OYSTsskigWibF")

# --- Step 5: Translate and update the sheet ---
for i, text in enumerate(english_texts):
    print(f"🔄 Translating Row {i + 1}: {text}")
    try:
        response = sarvam.text.translate(
            input=text,
            source_language_code="en-IN",
            target_language_code="od-IN",
            model="sarvam-translate:v1",
            mode="formal",
            enable_preprocessing=True
        )
        hindi_text = response.translated_text
        print(f"✅ Row {i + 1} Hindi: {hindi_text}")
        sheet.update_cell(i + 2, 2, hindi_text)  # Row offset +1, Column 2 = "Final Hindi"
    except Exception as e:
        print(f"❌ Failed for Row {i + 1}: {e}")
