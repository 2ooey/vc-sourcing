import os
from googleapiclient.discovery import build
import sys
sys.path.append('src')
from google_clients import GoogleClients
from dotenv import load_dotenv

load_dotenv()

try:
    clients = GoogleClients()
    service = build("sheets", "v4", credentials=clients.creds)
    sheet_metadata = service.spreadsheets().get(spreadsheetId=os.environ.get("SPREADSHEET_ID")).execute()
    sheets = sheet_metadata.get('sheets', '')
    
    print("Available Sheets:")
    for sheet in sheets:
        title = sheet.get("properties", {}).get("title", "")
        print(" -", title)

        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=os.environ.get("SPREADSHEET_ID"),
                range=f"'{title}'!A1:Z1"
            ).execute()
            headers = result.get('values', [])
            if headers:
                print(f"   Headers: {headers[0]}")
            else:
                print("   Headers: (None)")
        except Exception as inner_e:
            print(f"   Could not fetch headers: {inner_e}")
            
except Exception as e:
    print("Sheets API Error:", e)
