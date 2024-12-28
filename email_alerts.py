import json 
# Convert events in json file into a list of dictionaries
def load_events(JSON_FILE):
    with open(JSON_FILE,'r') as f:
        return json.load(f)

def get_current_date():
    pass 

def send_email():
    pass

def email_alerts_recurring():
    

def email_alerts_non_recurring():
    pass