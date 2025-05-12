# Email Sorter and Summarizer

This project is an email sorting and summarizing tool that integrates with the Gmail API to fetch recent emails and uses OpenAI to summarize them. It enables users to quickly get a brief summary of their email content and sends the user an email of all their recent emails. In particular, this project focuses on the college advertisement emails, since high schoolers like us receive so many of these (annoying) emails!

## Features

- **Gmail Authentication**: Uses OAuth2 to authenticate and interact with the Gmail API.
- **Fetch Recent Emails**: Retrieves recent emails from the user's Gmail account.
- **Text Cleanup**: Cleans up the email content by removing URLs, signatures, and unnecessary text.
- **Summarize Emails**: Summarizes the content of emails using OpenAI's GPT model.
- **Sends Email**: Sends the user an email containing all the summaries and labels.

## Prerequisites

Before you start, you'll need to have the following installed:

- Python 3.6 or higher
- Google API Client Library: make credentials.json file
- OpenAI API key
- A Google Cloud project with Gmail API enabled

## Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/email-sorter-summarizer.git
   cd email-sorter-summarizer

2. **Add API keys**:
    Add a credential.json file containing Gmail API and .env file with OPENAI_API_KEY = your_token

3. **Run main.py**:
    
    The file that has everything put together is main.py
    During the first run, you will login to your Gmail API account and token.json will be created; in the future, you'll be automatically signed in. Everytime you run, it will send an email of the summary and links to your most recent emails. Feel free to change the number of emails it reads and make other adjustments.