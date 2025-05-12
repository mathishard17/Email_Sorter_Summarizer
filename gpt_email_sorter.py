from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Sample input list (replace or expand this manually for testing)
email_summaries = ['Emails for 05/08/2025 include discussions on class choices for next semester, late probation, an AP Physics review session, and an opportunity for a Digital Development Camp at Drexel University from July 7-24.', 'Class registration reminder for "STD\'s and Human Sexuality" meeting next Friday.', 'Probation warning for consistent lateness in classes.', 'AP Physics review session on Tuesday.', "Drexel University's Digital Development Camp, VirtuaQuest, running from July 7 to July 24, offers hands-on learning in various tech fields for high school students with no prior experience required, at a $750 program fee.", 'Email summary: Testimonial from Lilli-Ann Greene ’26 about the supportive community at York College of Pennsylvania.', 'Virtual event invitation for LAUNCH program with Cornell, Emory, Pomona, Rice, and WashU; register for academic insights and Q&A.', 'Submit application to Widener University for scholarships by midnight.', 'Upcoming virtual sessions on college admissions and programs, including Simons STEM Scholars Program Information Sessions, with various dates in May, June, July, and August 2025, featuring Stony Brook students, staff, and faculty panels.', 'Invitation to UConn Admissions & Financial Aid Early Planning webinar on May 20.', 'Invitation to virtual information session with Caltech, CC, UChicago, Vanderbilt, and Yale to learn about QuestBridge program for high-achieving, low-income students.', 'Gabby shares her positive experience at Alfred University, highlighting community support, involvement opportunities, and affordability, encouraging Justin to apply.', "Email introducing Alfred University's College of Liberal Arts and Sciences from Dean Stein, encouraging application and exploring educational pathways, with contact information provided.", 'Email highlights the vibrant student life at Hillsdale College with various clubs, organizations, and events.', "Email promoting the benefits of joining the University of Alabama's Honors College and highlighting the Adapted Athletics program, with resources for prospective students and families.", 'Florida Tech offers affordable education with merit-based scholarships covering up to 50% of tuition, and invites you to apply for free to receive an admission decision and scholarship offer within 10 days.', 'Emails for 05/08/2025 include various topics such as greetings, money, work, and school.', 'Email confusion, seeking clarification.', 'Emails for 05/06/2025 include topics on money, work, and a social hangout invitation.', 'Email about liking money.', 'Email about expanding the expression (a+b)^n.', 'UDoU offers customizable degrees and diplomas for $49.99, with a limited time offer including a free honorary doctorate in Time Management. Apply now or pretend you did.', 'Invitation for drinks at Thai Village in Princeton after work today.', 'Email congratulating recipient for being recognized during Appreciation Week at Princeton International School of Mathematics & Science.', 'Invitation to PRISMS, highlighting best cafeteria food, AI classes, and graduates.', 'Encouragement to work today for financial benefit.', 'OpenAI API account funded with $10.00 charge to credit card ending in 0221.']

# Categories to sort into
categories = {
    "College Advertisements": [],
    "School": [],
    "Work": [],
    "Money": [],
    "Other": []
}

def categorize_summary(summary):
    category_list = "', '".join(categories.keys())
    prompt = (
        f"Classify the following email summaries into one of the following categories (Note, college advertisements are summaries trying to entice us to apply to that university by showing good things about it. School is emails related to what I'm doing or will do at the school I'm at. Other is anything else.'): "
        f"'{category_list}'.\n\n"
        f"Summary: \"{summary}\"\n\n"
        "Respond only with the one category name."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an email categorization assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=10
        )
        raw_category = response.choices[0].message.content.strip()
        # Normalize and match against original keys
        for cat in categories.keys():
            if raw_category.lower() == cat.lower():
                return cat
        return "Other"
    except Exception as e:
        print(f"Error: {e}")
        return "Other"


def categorize_summaries(summaries):
    for idx, summary in enumerate(summaries):
        category = categorize_summary(summary)
        categories[category].append((idx, summary))

def print_categorized_summaries():
    for cat, summaries in categories.items():
        print(f"\n=== {cat.upper()} ===")
        for index, summary in summaries:
            print(f"[{index}] {summary}")

 # Run the categorization
if __name__ == "__main__":
    categorize_summaries(email_summaries)
    print_categorized_summaries()