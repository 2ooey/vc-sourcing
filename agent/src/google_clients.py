import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
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
        # Decode and write credentials
        creds_json = base64.b64decode(os.environ['CREDENTIALS_JSON']).decode('utf-8')
        with open(self.credentials_file, 'w') as f:
            f.write(creds_json)

        # Decode and write token
        token_json = base64.b64decode(os.environ['TOKEN_JSON']).decode('utf-8')
        with open(self.token_file, 'w') as f:
            f.write(token_json)

    def append_to_sheet(self, spreadsheet_id, range_name, values):
        """Appends a row of values to the specified spreadsheet."""
        try:
            service = build("sheets", "v4", credentials=self.creds)
            body = {"values": values}
            result = (
                service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption="USER_ENTERED",
                    body=body,
                )
                .execute()
            )
            print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
            return result
        except HttpError as error:
            print(f"An error occurred appending to sheet: {error}")
            return None

    def send_email(self, to_email, subject, body_text):
        """Sends an email via Gmail API."""
        try:
            service = build("gmail", "v1", credentials=self.creds)
            message = EmailMessage()

            message.set_content(body_text)
            message["To"] = to_email
            message["From"] = "me"  # 'me' denotes the authenticated user
            message["Subject"] = subject

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            send_message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(f"An error occurred sending email: {error}")

if __name__ == "__main__":
    # Test authentication
    clients = GoogleClients()
    print("Authentication successful if token.json was generated/updated.")
