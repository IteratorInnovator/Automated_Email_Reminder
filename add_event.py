import json
from datetime import datetime
import custom_error_class as er
import helper_functions as HF
import re
import os
from dotenv import load_dotenv 


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
            if re.match(date_pattern,event_date) == None:
                raise ValueError("Invalid date entered!")
            event_date_as_datetime = datetime.strptime(event_date,"%Y-%m-%d").date()
            current_date = datetime.today().date()
            if event_date_as_datetime < current_date:
                raise er.InvalidTimeInputError("Date entered cannot be in the past!")
            return event_date
        except er.InvalidTimeInputError as e:
            print(f"Error: {e} Please try again.")
        except Exception as e:
            print(f"Error: {e} Please try again.")

def get_event_days():
    event_days = set()
    valid_days = {"monday","tuesday","wednesday","thursday","friday","saturday","sunday"}
    while True:
        try:
            day = input("Enter the events days one per line (e.g monday, tuesday) . Type 'done' when finished. ").lower()
            if day == 'done':
                break
            if day in valid_days:
                event_days.add(day)
            else:
                raise ValueError("Invalid day entered!")
        except Exception as e:
            print(f"Error: {e} Please try again.")
    event_days = list(event_days)
    event_days = [day.capitalize() for day in event_days]
    return event_days 

def get_event_time(event):
    while True:
        try:
            event_time = input("Enter time of event in HH:MM AM/PM format (e.g 02:30 PM): ")
            # Retrieve event_time as a datetime.time object
            event_time_as_datetime = datetime.strptime(event_time,"%I:%M %p").time()
            if event["recurring"] == False:
                today_datetime = datetime.today()
                # Retrieve event_date as datetime.date object
                event_date_as_datetime = datetime.strptime(event["date"],"%Y-%m-%d").date()
                # Combine event_date and event_time to get event as datetime object
                event_datetime = datetime.combine(event_date_as_datetime,event_time_as_datetime)
                if event_datetime < today_datetime:
                    raise er.InvalidTimeInputError("Event cannot be in the past!")
            # Reformat event_time into standardized format 
            return datetime.strftime(datetime.strptime(event_time,"%I:%M %p"),"%I:%M %p")
        except er.InvalidTimeInputError as e:
            print(f"Error: {e} Please try again.")
        except Exception as e:
            print("Error: Invalid Input! Please try again.")

def sort_event_by_keys(event):
    if event["recurring"] == True:
        custom_order = ["name","time","location","recurring","day","reminder_sent"]
    else:
        custom_order = ["name","date","time","location","recurring","reminder_sent"]
    sorted_event = {k:event[k] for k in custom_order}
    return sorted_event

def main():
    load_dotenv()
    JSON_FILE = os.getenv("EVENT_FILE","./sample_events.json")
    event = {}
    event["name"] = get_event_name()
    event["location"] = get_event_location()
    event["recurring"] = is_event_recurring()
    if event["recurring"] == True:
        event["day"] = get_event_days()
    else:
        event["date"] = get_event_date()
    event["time"] = get_event_time(event)
    event["reminder_sent"] = False
    event = sort_event_by_keys(event)
    with open(JSON_FILE,'r') as f:
        events = json.load(f)
    events.append(event)
    with open(JSON_FILE,'w') as f:
        json.dump(events,f,indent=4)
    print("Event has been succesfully added.")
        
if __name__ == "__main__":
    main()