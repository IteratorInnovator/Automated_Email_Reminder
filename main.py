from datetime import datetime
import os
import json
import helper_functions as HF
from dotenv import load_dotenv

def main():
    load_dotenv()
    sender_email = os.environ("SENDER_EMAIL")
    app_password = os.environ("APP_PASSWORD")
    recipient_emails = os.environ("RECIPIENT_EMAIL").split(',')
    JSON_FILE = os.environ("EVENT_FILE","./sample_events.json")
    events = HF.load_events(JSON_FILE)
    day_of_tomorrow = HF.get_tomorrow_day()
    date_of_tomorrow = HF.get_tomorrow_date()
    current_time = HF.get_time()
    updated_events = []
    for event in events:
        if event["reminder_sent"] == False:
            email_contents = []
            if event["recurring"] == True:
                email_contents = HF.email_alerts_recurring(event,day_of_tomorrow,current_time)
            elif event["recurring"] == False:
                email_contents = HF.email_alerts_non_recurring(event,date_of_tomorrow,current_time)
            if len(email_contents)==2:
                HF.send_email(event,sender_email,recipient_emails,app_password,email_contents)
                event["reminder_sent"] = True
        elif event["reminder_sent"] == True:
            if event["recurring"] == True:
            # Check if current day matches recurring event days
            # Reset reminder_sent back to false if event has occured by comparing current time and event time
                current_day = datetime.today().strftime('%A')
                if current_day in event["day"]:
                    event_time = datetime.strptime(event["time"],"%I:%M %p").time()
                    if current_time > event_time:
                        event["reminder_sent"] = False
            elif event["recurring"] == False:
                event_date = datetime.strptime(event["date"],"%Y-%m-%d").date()
                current_date = datetime.today().date()
                # Check if event has already passed
                if current_date > event_date:
                    continue # Skip appending to updated_events since event has already occured
                elif current_date == event_date:
                    event_time = datetime.strptime(event["time"],"%I:%M %p").time()
                    if current_time > event_time:
                        continue
        updated_events.append(event)
    HF.update_events(JSON_FILE,updated_events)
    
if __name__ == "__main__":
    main()