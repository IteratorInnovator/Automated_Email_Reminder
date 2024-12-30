import json 
import smtplib
import ssl
from datetime import datetime, timedelta
from email.message import EmailMessage

# Convert events in json file into a list of dictionaries
def load_events(JSON_FILE):
    with open(JSON_FILE,'r') as f:
        return json.load(f)
   
def update_events(JSON_FILE,events):
    with open(JSON_FILE,'w') as f:
        json.dump(events,f,indent=4)

# Get tomorrow's date in YYYY-MM-DD format
def get_tomorrow_date():
    tomorrow_date = datetime.today() + timedelta(days=1)
    return tomorrow_date.date()

# Get the day in abbreaviated name for tomorrow 
def get_tomorrow_day():
    # Get tomorrows date by adding timedelta(days=1) to today
    day_tmr = datetime.today() + timedelta(days=1)
    return day_tmr.strftime('%A')

# Get current time in HH:MM:SS 
def get_time():
    return datetime.today().time()
        
      
# For recurring events, retrieve day of tomorrow and time
# Process event and craft email body
# Return email content for plain text and html
def email_alerts_recurring(event,day_of_tomorrow,current_time):
    # Check if day of tomorrow in the list of event days
    if day_of_tomorrow in event["day"]:
        event_time = datetime.strptime(event["time"],"%I:%M %p").time()
        # Check if current time in within 24 hr mark
        if current_time >= event_time:
            event_name = event["name"]
            location = event["location"]
            time = event["time"]
            email_content = f"""
Hi Harry,
    
This is a reminder that you have the following class tomorrow:
    
Class: {event_name}
Location: {location}
Time: {time}

Please ensure you are prepared for the lesson.

Best regards,
Automated Reminder System
            """
            email_content_in_html = f"""
    <html>
        <body>
            <h1 style="color: #0056b3;"><b>REMINDER</b></h1>
            <p>Hi Harry,</p>
            <p>This is a reminder that you have the following class <b>tomorrow</b>:</p>
            <p>
                <b>Class:</b> {event_name}<br>
                <b>Location:</b> {location}<br>
                <b>Time:</b> {time}<br><br>
            </p>
            <p>Please ensure you are prepared for the lesson.</p>
            <p>Best regards,<br>Automated Reminder System</p>
        </body>
    </html>
            """
            return (email_content,email_content_in_html)
    return ()

# For recurring events, retrieve date of tomorrow and time
# Process event and craft email body
# Return email content for plain text and html
def email_alerts_non_recurring(event,date_of_tomorrow,current_time):
    # Convert event date to datetime.date object for comparison
    event_date = datetime.strptime(event["date"],"%Y-%m-%d").date()
    if date_of_tomorrow == event_date:
        event_time = datetime.strptime(event["time"],"%I:%M %p").time()
        if current_time >= event_time:
            event_name = event["name"]
            location = event["location"]
            time = event["time"]
            email_content = f"""
Hi Harry,
    
This is a reminder that you have the following activity tomorrow:
    
Activity: {event_name}
Location: {location}
Time: {time}

Best regards,
Automated Reminder System
            """
            email_content_in_html = f"""
    <html>
        <body>
            <h1 style="color: #0056b3;"><b>REMINDER</b></h1>
            <p>Hi Harry,</p>
            <p>This is a reminder that you have the following activity <b>tomorrow</b>:</p>
            <p>
                <b>Activity:</b> {event_name}<br>
                <b>Location:</b> {location}<br>
                <b>Time:</b> {time}<br><br>
            </p>
            <p>Best regards,<br>Automated Reminder System</p>
        </body>
    </html>
            """
            return (email_content,email_content_in_html)
    return ()


def send_email(event,sender_email,recipient_emails,app_password,email_contents):
    msg = EmailMessage()
    msg["Subject"] = f"REMINDER - {event['name']}"
    msg["From"] = sender_email
    msg["To"] = ','.join(recipient_emails)
    msg.set_content(email_contents[0])
    msg.add_alternative(email_contents[1],subtype="html")
    
    context = ssl.create_default_context()
    # SSL connections: port 465
    # If using starttls(), use port 587
    # Close using server.close() if no 'with' statement used
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
            server.login(sender_email,app_password)
            server.sendmail(sender_email,recipient_emails,msg.as_string())
            # Convert EmailMessage object into a properly formatted string that follows the MIME standard
    except Exception as e:
        print(f"Error: {e}")