import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    print("Available Gemini Models:", models)
except Exception as e:
    print("Gemini API Error:", e)

import sys
sys.path.append('src')
from google_clients import GoogleClients
from googleapiclient.discovery import build

try:
    clients = GoogleClients()
    service = build("sheets", "v4", credentials=clients.creds)
    sheet_metadata = service.spreadsheets().get(spreadsheetId=os.environ.get("SPREADSHEET_ID")).execute()
    sheets = sheet_metadata.get('sheets', '')
    print("Available Sheets:")
    for sheet in sheets:
        print(" -", sheet.get("properties", {}).get("title", ""))
except Exception as e:
    print("Sheets API Error:", e)
