import os
import base64
import schedule
import time
import requests
from transformers import pipeline
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from readAndSummarize import summarize_email, gmail_authenticate, read_recent_emails
from email_sorter import categorize_summary
from send_email import send_email
from datetime import datetime, timedelta


def get_labels(service):
    results = service.users().labels().list(userId='me').execute()
    return {label['name']: label['id'] for label in results['labels']}

def apply_label(service, msg_id, label_name, label_map):
    label_id = label_map.get(label_name)
    if label_id:
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'addLabelIds': [label_id]}
        ).execute()

def get_first_30_words(input_string):
    # Split the string into words
    words = input_string.split()
    
    # Get the first 30 words
    first_30_words = words[:30]
    
    # Join the first 30 words back into a string
    result = ' '.join(first_30_words)
    
    return result

from collections import defaultdict
from datetime import datetime

from collections import defaultdict
from datetime import datetime

from collections import defaultdict
from datetime import datetime

def archive_email(service, msg_id):
    """Remove 'INBOX' label to archive the message"""
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['INBOX']}
    ).execute()

def classify_all(email_array, service):
    label_map = get_labels(service) if service else {}
    print("Reading emails...")
    current_date = datetime.now().strftime("%m/%d/%Y")
    daily = f"Emails for {current_date}"

    # Group emails by label
    labeled_emails = defaultdict(list)
    college_ads = []

    for i, (id, subject, body) in enumerate(email_array):
        print(f"Current email {i}: {subject}")
        summarized = summarize_email(subject, body)
        print(f"Summarized: {summarized}")
        label = categorize_summary(summarized)
        print(f"Labelled: {label}")
        gmail_link = f"https://mail.google.com/mail/u/0/#all/{id}"

        # Check if the email has the 'College Advertisements' label
        if label == 'College Advertisements':
            archive_email(service, id) #archives the email
            college_ads.append(
                f"\n📩 College Advertisement Email #{i + 1}"
                f", 📌 Subject: {subject}"
                f", 🏷️ Label: {label}\n"
                f"📝 Preview: {summarized}"
                f"\n🔗 View here: {gmail_link}\n"
            )
        else:
            # Add formatted email to the corresponding label section
            email_entry = (
                f"\n📌 Subject: {subject}"
                f", 🏷️ Label: {label}\n"
                f"📝 Preview: {summarized}"
                f"\n🔗 View here: {gmail_link}\n"
            )
            labeled_emails[label].append(email_entry)

        apply_label(service, id, label, label_map)
        print(f"Added!")

    # Build final string with college advertisements first, then other emails grouped by label
    All_emails = ""
    if college_ads:
        All_emails += "\n\n=== 📢 COLLEGE ADVERTISEMENTS ===\n" + "".join(college_ads)

    # Add emails grouped by label
    for label, entries in labeled_emails.items():
        if label != 'College Advertisements':  # Skip college ads in this section
            All_emails += f"\n\n=== 📂 {label.upper()} ===\n" + "".join(entries)

    send_email(All_emails, daily)
    


service = gmail_authenticate()
email_array = read_recent_emails(service, 10) # currently reading 6 newest emails
classify_all(email_array, service)

while True:
    schedule.run_pending()
    time.sleep(1)
