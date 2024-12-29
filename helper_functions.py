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
    return tomorrow_date.strftime('%Y-%m-%d')

# Get the day in abbreaviated name for tomorrow 
def get_tomorrow_day():
    # Get tomorrows date by adding timedelta(days=1) to today
    day_tmr = datetime.today() + timedelta(days=1)
    return day_tmr.strftime('%a')

# Get current time in HH:MM:SS 
def get_time():
    return datetime.today().time()
    
def send_email():
    pass

def email_alerts_recurring():
    pass

def email_alerts_non_recurring():
    pass