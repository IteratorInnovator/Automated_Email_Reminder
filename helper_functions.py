import json 
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

# Convert events in json file into a list of dictionaries
def load_events(JSON_FILE):
    with open(JSON_FILE,'r') as f:
        return json.load(f)

# Get tomorrow's date in YYYY-MM-DD format
def get_tomorrow_date():
    tomorrow_date = datetime.today() + timedelta(days=1)
    return tomorrow_date.date()

# Get the day in abbreaviated name for tomorrow 
def get_tomorrow_day():
    # Get tomorrows date by adding timedelta(days=1) to today
    day_tmr = datetime.today() + timedelta(days=1)
    return day_tmr.strftime('%a')

# Get current time in HH:MM:SS 
def get_time():
    return datetime.today().time()
    
def send_email(event,sender_email,recipient_email):
    event_name = event["name"]
    location = event["location"]
    time = event["time"]
    email_content = f"""
    Hi Harry,
    
    This is a reminder that you have the following class tomorrow:
    
    Class: {event_name}
    Location: {location}
    Time: {time}

    Please ensure you're prepared for the session.

    Best regards,
    Automated Reminder System
    """
    msg = EmailMessage()
    msg["Subject"] = f"REMINDER - {event_name}"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(email_content)

# For recurring events, retrieve day of tomorrow and date
# Process event and craft subject and body
# If more or equal than, send email
def email_alerts_recurring(event,day_of_tomorrow,current_time):
    # Check if day of tomorrow in the list of event days
    if day_of_tomorrow in event["day"]:
        event_time = datetime.strptime(event["time"],"%I:%M %p").time()
        # Check if current time in within 24 hr mark
        if event_time < current_time:
            pass
    
def email_alerts_non_recurring(event,date_of_tomorrow,current_time):
    pass