import os
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.send"
]

class GoogleClients:
    def __init__(self, credentials_file="credentials.json", token_file="token.json"):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        self._authenticate()

    def _authenticate(self):
        # SecretsからBase64を読み込んでファイルに書き出す
        try:
            creds_raw = os.environ.get('CREDENTIALS_JSON')
            token_raw = os.environ.get('TOKEN_JSON')
            
            if not creds_raw or not token_raw:
                raise ValueError("Credentials or Token not found in Environment Variables")

            with open(self.credentials_file, 'w') as f:
                f.write(base64.b64decode(creds_raw).decode('utf-8'))
            with open(self.token_file, 'w') as f:
                f.write(base64.b64decode(token_raw).decode('utf-8'))

            self.creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        except Exception as e:
            print(f"Auth Error: {e}")
            raise

    def append_to_sheet(self, spreadsheet_id, range_name, values):
        try:
            service = build("sheets", "v4", credentials=self.creds)
            body = {"values": values}
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            ).execute()
        except Exception as e:
            print(f"Sheets Error: {e}")
