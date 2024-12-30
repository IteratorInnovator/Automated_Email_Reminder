import json
from datetime import datetime
import custom_error_class as er
import helper_functions as HF
import re

JSON_FILE = "./events.json"

def get_event_name():
    return input("Enter event name: ")

def get_event_location():
    return input("Enter location of event: ")

def is_event_recurring():
    while True:
        try:
            is_recurring = input("Is the event recurring? [Yes/No]: ").capitalize()
            if is_recurring == "Yes" or is_recurring == "Y":
                return True
            elif is_recurring == "No" or is_recurring == "N":
                return False
            else:
                raise ValueError("Invalid input! Please try again.")
        except ValueError as error:
            print(f"Error: {error}")

def get_event_date():
    date_pattern = r"^[0-9]{1,4}-(0[1-9]|1[0-2])-([0][1-9]|[1-2][0-9]|[3][0-1])$" # Check input date format is valid using regex
    while True:
        try:
            event_date = input("Enter event date in YYYY-MM-DD format (e.g 2025-01-20): ")
            if re.match(date_pattern,event_date) == False:
                raise ValueError
            event_datetime_obj = datetime.strptime(event_date,"%Y-%m-%d").date()
            current_date = datetime.today().date()
            if event_date < current_date:
                raise er.InvalidTimeInputError("Date entered cannot be in the past!")
            return event_date
        except er.InvalidTimeInputError as e:
            print(f"Error: {e} Please try again.")
        except:
            print("Error: Invalid input! Please try again.")

def get_event_days():
    pass

def get_event_time(event):
    while True:
        try:
            event_time = input("Enter time of event in HH:MM AM/PM format (e.g 02:30 PM): ")
            event_time_as_datetime = datetime.strptime(event_time,"%I:%m %P").time()
            if event["recurring"] == False:
                today_datetime = datetime.today()
                event_date_as_datetime = datetime.strptime(event["date"],"%Y-%m-%d").date()
                event_datetime = datetime.combine(event_date_as_datetime,event_time_as_datetime)
            if event_datetime < today_datetime:
                raise er.InvalidTimeInputError("Event cannot be in the past!")
            return event_time
        except er.InvalidTimeInputError as e:
            print(f"Error: {e} Please try again.")
        except Exception as e:
            print("Error: Invalid Input! Please try again.")
    

def main():
    event = {}
    event["name"] = get_event_name()
    event["location"] = get_event_location()
    event["recurring"] = is_event_recurring()
    if event["recurring"] == True:
        event["day"] = get_event_days()
    else:
        event["date"] = get_event_date()
    event["time"] = get_event_time(event)
    with open(JSON_FILE,'r') as f:
        events = json.load(f)
    events.append(event)
    with open(JSON_FILE,'w') as f:
        json.dump(events,f,indent=4)
        
if __name__ == "__main__":
    main()