from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def create_event(title, start_time, end_time):
    print("GOOGLE START:", start_time.isoformat())
    print("GOOGLE END:", end_time.isoformat())
    service = get_calendar_service()

    event = {
        "summary": title,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Karachi",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Karachi",
        },
    }

    service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return "Meeting created successfully."

def create_simple_event(title, hour=15, minute=0, days_from_now=1):

    print("=" * 40)
    print("RECEIVED HOUR:", hour)

    start = datetime.now() + timedelta(days=days_from_now)

    start = start.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )

    end = start + timedelta(hours=1)

    print("START:", start)
    print("END:", end)
    print("START ISO:", start.isoformat())
    print("END ISO:", end.isoformat())
    print("=" * 40)

    return create_event(title, start, end)