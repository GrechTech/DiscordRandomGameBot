import csv
import os
from datetime import datetime, timedelta

# The dates and times in your CSV files should be in the format ‘YYYY-MM-DD HH:MM’.

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
event_lists_path = os.path.join(dir_path, "Data", "Events")

def get_events_this_week():
    # Get today's date
    print("Start")
    today = datetime.utcnow()
    print(today)
    
    # Calculate the start and end of the week (Monday to Sunday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Initialize an empty list to store events
    events_this_week = []
    print(event_lists_path)
    # Loop over all CSV files in the folder
    for filename in os.listdir(event_lists_path):
        print(filename)
        if filename.endswith('.csv'):
            # Open the CSV file
            with open(os.path.join(event_lists_path, filename), 'r') as f:
                print(os.path.join(event_lists_path, filename))
                reader = csv.DictReader(f)
                
                # Loop over all rows in the CSV file
                for row in reader:
                    print(row)
                    # Convert the 'date' column to datetime
                    date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M')
                    if not isinstance(date, datetime):
                        print("DateError")
                    # Check if the date is in this week
                    if start_of_week <= date <= end_of_week:
                        print("Found")
                        # Append the event to the list
                        events_this_week.append([row['name'],date])
    if not events_this_week:
        events_string = "Nothing this week"
    # Convert the list of events to a single string
    else:
        events_string = '\n'.join([f"-{filename.replace('.csv', '')}: {event[0]} on {event[1].strftime('%A, %H:%M')}"  \
            if isinstance(event[1], datetime)  else f"-{filename.replace('.csv', '')}: {event[0]} on {event[1]}" for event in events_this_week])
    print("Done")
    return events_string
