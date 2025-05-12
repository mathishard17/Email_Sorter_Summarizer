from openai import OpenAI

import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

email_array = [
    [
        "Quarterly Sales Review & Strategic Shifts",
        "Dear Team,\n\nAs we close out Q1, I want to thank everyone for their hard work. Our sales have grown 12% over last quarter, largely thanks to new outreach efforts in the Pacific Northwest. However, customer churn in our software-as-a-service sector remains a concern. To address this, we’ll be piloting a new retention-focused initiative starting next month, including customer success check-ins, revised onboarding, and more proactive support. Please review the attached slide deck before Friday’s strategy meeting.\n\nBest,\nSandra"
    ],
    [
        "Upcoming Maintenance Downtime for Internal Systems",
        "Hello all,\n\nPlease note that on Sunday between 1am and 6am EST, the internal ticketing and file-sharing systems will be offline for scheduled maintenance. The IT team will be upgrading our backend infrastructure to improve performance and reliability. If you have critical tasks or files needed during that window, please download them in advance. Any questions can be sent to helpdesk@company.com.\n\nThanks,\nDan"
    ],
    [
        "Invitation to Speak at the FutureMed Innovation Summit",
        "Dear Dr. Kim,\n\nWe’re thrilled to invite you as a featured speaker at this year’s FutureMed Innovation Summit in San Diego. Your work on bio-integrated sensors has inspired our programming committee, and we believe it will spark valuable discussion on the future of wearable diagnostics. The conference takes place October 17–19, with your keynote proposed for the morning of Day 2. We would cover all travel and accommodation expenses.\n\nWarm regards,\nAllison Freeman\nSummit Organizer"
    ],
    [
        "Updated Remote Work Guidelines and Expectations",
        "Team,\n\nWe’ve finalized updates to our remote work policies. Going forward, all team members are expected to be available between 10am–3pm EST, regardless of time zone, for synchronous collaboration. We’re also implementing a monthly virtual town hall to ensure alignment and foster culture. While we support flexibility, it’s essential that core hours are respected and camera use is encouraged during meetings unless previously discussed.\n\nPlease review the full document in your HR portal.\n\n– HR Team"
    ],
    [
        "New Product Launch: EchoTrack v2.0 Rollout Plan",
        "Hi everyone,\n\nAfter months of development, we're excited to launch EchoTrack v2.0. This update includes major improvements in data visualization, real-time geolocation accuracy, and user onboarding flows. Marketing campaigns will begin next week, followed by a staggered user release starting Monday. All client-facing teams will receive updated training materials by Friday. Please familiarize yourselves with the changelog and FAQs.\n\nBest,\nProduct Team"
    ],
    [
        "Reminder: Diversity & Inclusion Training Completion",
        "Dear Colleagues,\n\nAs part of our company-wide initiative on building an inclusive culture, all staff are required to complete the D&I training module by April 15th. The course takes approximately 90 minutes and can be accessed through your learning dashboard. Completion will be tracked, and managers will be notified of outstanding employees. Let’s take this opportunity seriously and grow together.\n\nThank you,\nDEI Office"
    ],
    [
        "Monthly Finance Update & Budget Reallocations",
        "Finance Team,\n\nWe saw modest gains in Q1 driven by strong licensing renewals, but several departments have exceeded discretionary budgets. Effective immediately, we are reallocating funds to prioritize product development and marketing expansion. Travel budgets will be capped through Q2, and procurement will require VP approval. Please review the revised budget spreadsheet and submit any questions by Thursday’s check-in.\n\nRegards,\nLaura R."
    ],
    [
        "New Security Protocols for External Communications",
        "Hi All,\n\nDue to an increase in phishing attempts, we’re tightening rules around external email communication. Starting this week, emails to external domains must exclude any sensitive files unless encrypted with our company’s approved PGP tool. In addition, we’ve activated a warning banner for unknown senders and enabled automatic quarantining of flagged attachments. IT will be holding drop-in Q&A sessions every morning this week.\n\nStay safe,\nCIO Office"
    ],
    [
        "Invitation to Join Pilot Group for AI-Driven Scheduling Tool",
        "Hello,\n\nWe’re looking for volunteers to test our new AI-powered scheduling assistant. The tool automatically finds optimal meeting times, resolves conflicts, and syncs across calendars. As an early tester, you’ll provide feedback that shapes the product roadmap and receive priority access to future beta features. Participation requires a 15-minute onboarding and weekly surveys.\n\nLet us know if you’re interested!\n– Product Ops"
    ],
    [
        "Client Escalation: Urgent Resolution Needed for Acme Corp",
        "Team,\n\nWe received an urgent escalation from Acme Corp regarding a service outage that began yesterday. Their account team has flagged this as a potential contract risk unless resolved within 24 hours. Please prioritize triage and involve Tier 2 support immediately. A root cause analysis must be delivered to the client by close of business. PMs, coordinate a response timeline ASAP and keep leadership updated.\n\n– Customer Success Lead"
    ]
]

for idx, (subject, body) in enumerate(email_array):
    try:
        prompt = (
            f"Summarize the following email in **one short sentence or phrase**. "
            f"Only include the **main topic** and any **important dates or actions** if mentioned. "
            f"Be concise.\n\n"
            f"Subject: {subject}\nBody: {body}"
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
        print(f"\n--- Summary for Email #{idx + 1} ---")
        print(summary)

    except Exception as e:
        print(f"Error summarizing Email #{idx + 1}: {e}")
