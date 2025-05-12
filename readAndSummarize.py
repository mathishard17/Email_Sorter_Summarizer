import os.path
import base64
import re
from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email import message_from_bytes
from email.header import decode_header
from bs4 import BeautifulSoup
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
client = OpenAI(api_key=api_key)


def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def decode_subject(subject):
    if subject:
        parts = decode_header(subject)
        return ''.join(
            part.decode(enc or 'utf-8') if isinstance(part, bytes) else part
            for part, enc in parts
        )
    return "(No Subject)"

def clean_email_text(raw_text):
    text = re.sub(r'<https?://[^>]+>', '', raw_text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\[image:.*?\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Sent from my .+?\n', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Get Outlook for.*?\n', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return text.strip()

def extract_body_from_mime(mime_msg):
    for part in mime_msg.walk():
        content_type = part.get_content_type()
        content_disposition = part.get("Content-Disposition", "")
        if content_type == "text/plain" and "attachment" not in content_disposition:
            raw_body = part.get_payload(decode=True).decode(errors='replace')
            return clean_email_text(raw_body)
    for part in mime_msg.walk():
        if part.get_content_type() == "text/html":
            html = part.get_payload(decode=True).decode(errors='replace')
            soup = BeautifulSoup(html, "html.parser")
            return clean_email_text(soup.get_text())
    return ""

def read_recent_emails(service, max_results=50):
    days_ago = (datetime.now(timezone.utc) - timedelta(days=7)).timestamp()
    query = f"after:{int(days_ago)}"
    results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    messages = results.get('messages', [])
    email_array = []

    for msg in messages:
        msg_id = msg['id']
        message = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        mime_msg = message_from_bytes(msg_raw)

        subject = decode_subject(mime_msg['Subject'])
        body_text = extract_body_from_mime(mime_msg)

        if body_text.strip():
            email_array.append([msg_id, subject.strip(), body_text.strip()])

    return email_array

def summarize_email(subject, body):
    try:
        prompt = (
            f"Summarize the following email in one short sentence or phrase. "
            f"Only include the main topic and any important dates or actions if mentioned. "
            f"Be concise and don't need to specify it's an email.\n\nSubject: {subject}\nBody: {body}"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )

        summary = response.choices[0].message.content.strip()
    except Exception as e:
        summary = f"Error summarizing Email: {e}"
    return summary
    

def summarize_emails(email_array):
    summaries = []
    for idx, (subject, body) in enumerate(email_array):
        try:
            prompt = (
                f"Summarize the following email in one short sentence or phrase. "
                f"Only include the main topic and any important dates or actions if mentioned. "
                f"Be concise.\n\nSubject: {subject}\nBody: {body}"
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=150
            )

            summary = response.choices[0].message.content.strip()
        except Exception as e:
            summary = f"Error summarizing Email #{idx + 1}: {e}"
        summaries.append(summary)
    return summaries

def print_emails(email_array):
    for i, (subject, body) in enumerate(email_array, 1):
        print("\n===========================")
        print(f"Email #{i}")
        print(f"Subject: {subject}")
        print("Body:")
        print(body)

def print_email_summaries(summaries):
    for i, summary in enumerate(summaries, 1):
        print(f"\n--- Summary for Email #{i} ---")
        print(summary)

# Run
if __name__ == "__main__":
     service = gmail_authenticate()
     emails = read_recent_emails(service)
#     #print_emails(emails)
     email_summaries = summarize_emails(emails)
     print(email_summaries)
#     #print_email_summaries(email_summaries)