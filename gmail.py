from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_gmail_service():

    creds = None

    if os.path.exists("token_gmail.json"):
        creds = Credentials.from_authorized_user_file(
            "token_gmail.json",
            SCOPES,
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES,
            )

            creds = flow.run_local_server(port=0)

        with open("token_gmail.json", "w") as token:
            token.write(creds.to_json())

    return build(
        "gmail",
        "v1",
        credentials=creds,
    )
import base64

def read_latest_emails(limit=5):

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=limit
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return "No emails found."

    output = ""

    for msg in messages:

        message = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        headers = message["payload"]["headers"]

        subject = "No Subject"
        sender = "Unknown"

        for h in headers:

            if h["name"] == "Subject":
                subject = h["value"]

            if h["name"] == "From":
                sender = h["value"]

        output += f"\nFrom: {sender}\nSubject: {subject}\n"

    return output

from email.mime.text import MIMEText
import base64


def send_email(to_email, subject, body):

    service = get_gmail_service()

    message = MIMEText(body)

    message["to"] = to_email
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={
            "raw": raw
        }
    ).execute()

    return f"Email sent to {to_email}"