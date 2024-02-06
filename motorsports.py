import csv
import os
from datetime import datetime, timedelta

# The dates and times in your CSV files should be in the format ‘YYYY-MM-DD HH:MM’.

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
event_lists_path = os.path.join(dir_path, "Data", "Events")

def get_events_this_week(folder_path):
    # Get today's date
    today = datetime.utcnow()
    
    # Calculate the start and end of the week (Monday to Sunday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Initialize an empty list to store events
    events_this_week = []
    
    # Loop over all CSV files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            # Open the CSV file
            with open(os.path.join(folder_path, filename), 'r') as f:
                reader = csv.DictReader(f)
                
                # Loop over all rows in the CSV file
                for row in reader:
                    # Convert the 'date' column to datetime
                    date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M')
                    
                    # Check if the date is in this week
                    if start_of_week <= date <= end_of_week:
                        # Append the event to the list
                        events_this_week.append(row)
    
    # Convert the list of events to a single string
    events_string = '\n'.join([f"{event['name']} on {event['date'].strftime('%Y-%m-%d %H:%M')}" for event in events_this_week])
    
    return events_string
