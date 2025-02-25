from datetime import datetime
import json
import threading
from active_window import active_win_open
import time

def save_data_to_file():
    """Saves the current tracking data to a text file every 1 minute."""
    with open("tracker_log.txt", "w", encoding="utf-8") as file:
        json.dump(data_to_store, file, indent=4)  # Save in JSON format for readability
    print("Data saved to tracker_log.txt")  # Debugging message





def auto_save():
    save_data_to_file()
    threading.Timer(60, auto_save).start()  # Schedule the function to run every 60 seconds


# Dictionary to store tracking data
data_to_store = {}
# Start auto-saving when the program starts
auto_save()
# Tracking loop
run = True
sleeping_time = 10  # Time interval in seconds

while run:
    today_date = datetime.today().strftime('%d-%m-%Y')
    now = datetime.today().strftime('%H:%M')

    time.sleep(sleeping_time)

    project, program = active_win_open()
    if project is None or program is None:
        continue  # Skip if no valid window is found

    name = f"{program} - {project}"  # Correctly format the dictionary key

    if name in data_to_store:
        # If the program is already being tracked, update total time
        data_to_store[name]['total_time'] += sleeping_time
        data_to_store[name]['sessions'][-1]['end'] = now  # Update end time of last session
    else:
        # New program entry
        data_to_store.update({
            name: {
                'total_time': sleeping_time,
                'sessions': [{'start': now, 'end': now}],
                'date': today_date
            }
        })


