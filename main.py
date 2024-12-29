import os
import json
import helper_functions as HF
from dotenv import load_dotenv

JSON_FILE = "./events.json"
def main():
    load_dotenv()
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("APP_PASSWORD")
    recipient_emails = os.getenv("RECIPIENT_EMAIL").split(',')
    events = HF.load_events(JSON_FILE)
    day_of_tomorrow = HF.get_tomorrow_day()
    date_of_tomorrow = HF.get_tomorrow_date()
    current_time = HF.get_time()
    for event in events:
        if event["reminder_sent"] == False:
            if event["recurring"] == True:
                email_contents = HF.email_alerts_recurring(event,day_of_tomorrow,current_time)
                if len(email_contents)==2:
                    HF.send_email(event,sender_email,recipient_emails,app_password,email_contents)
                continue # skip to next iteration if email_contents size is incorrect, indicating not to send email
            elif event["recurring"] == False:
                email_contents = HF.email_alerts_non_recurring(event,date_of_tomorrow,current_time)
                if len(email_contents)==2:
                    HF.send_email(event,sender_email,recipient_emails,app_password,email_contents)
                continue
        elif event["reminder_sent"] == True:
            if event["recurring"] == True:
                pass
    
if __name__ == "__main__":
    main()