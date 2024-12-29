import os
import json
import email_alerts
from dotenv import load_dotenv

JSON_FILE = "./events.json"
def main():
    load_dotenv()
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("APP_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    events = email_alerts.load_events(JSON_FILE)
    for event in events:
        if event["reminder_sent"] == False:
            if event["recurring"] == True:
                email_alerts.email_alerts_recurring(event)
            elif event["recurring"] == False:
                email_alerts.email_alerts_non_recurring(event)
            
    
if __name__ == "__main__":
    main()