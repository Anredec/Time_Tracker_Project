from datetime import datetime
import json
import threading
from active_window import active_win_open
import time
import sqlite3


def save_data_to_file():
    """Saves the current tracking data to a text file every 1 minute."""
    with open("tracker_log.txt", "w", encoding="utf-8") as file:
        json.dump(data_to_store, file, indent=4)  # Save in JSON format for readability
    print("Data saved to tracker_log.txt")  # Debugging message


def save_data_sqlite():
    '''Saves the current tracking data to a sqlite file every 1 minute.'''
    
    database_sql= conn.cursor()
    #checking existing entries
    for i in data_to_store:
        
        database_sql.execute('''
                     SELECT total_time from usage_tracking
                     WHERE program= ? AND project= ? AND date= ?;
                     ''',(data_to_store[i]['pro_name'], data_to_store[i]['pro_seg'], data_to_store[i]['date']))
    
        #if the record exist
        result= database_sql.fetchone()
        if result:
            #if there is previous record -update
            database_sql.execute('''
                    UPDATE usage_tracking
                    SET total_time= ?, end_time= ?
                    WHERE program= ? AND project= ? AND date= ?;
                    ''',(data_to_store[i]['total_time'], data_to_store[i]['end'], data_to_store[i]['pro_name'],data_to_store[i]['pro_seg'], data_to_store[i]['date']))
        else:
            #if there is not previous record -save new row
            database_sql.execute('''
                         INSERT  INTO usage_tracking(program, project, date, total_time, start_time, end_time)
                         VALUES (?,?,?,?,?,?);''',(data_to_store[i]['pro_name'],data_to_store[i]['pro_seg'],data_to_store[i]['date'],data_to_store[i]['total_time'],data_to_store[i]['start'], data_to_store[i]['end']))
    conn.commit()
    


def auto_save():
    save_data_to_file()
    save_data_sqlite()
    threading.Timer(60, auto_save).start()  # Schedule the function to run every 60 seconds


# Dictionary to store tracking data
data_to_store = {}

# Tracking loop
run = True
sleeping_time = 10  # Time interval in seconds

#connecting to sqlite database
conn= sqlite3.connect('tracker.db')
database_sql= conn.cursor()
database_sql.executescript('''
            CREATE TABLE IF NOT EXISTS usage_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program TEXT NOT NULL,
                project TEXT NOT NULL,
                date TEXT NOT NULL,
                total_time INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL
            );
                ''')

conn.commit()


# Start auto-saving when the program starts
auto_save()
try:
    while run:
        today_date = datetime.today().strftime('%d-%m-%Y')
        now = datetime.today().strftime('%H:%M')

        time.sleep(sleeping_time)

        project, program = active_win_open()
        if project is None or program is None:
            continue  

        name = f"{program} - {project}"  

        if name in data_to_store:
            data_to_store[name]['total_time'] += sleeping_time
            data_to_store[name]['end'] = now  
        else:
            data_to_store[name] = {
                'total_time': sleeping_time,
                'start': now,
                'end': now,
                'date': today_date,
                'pro_name': program,
                'pro_seg': project
            }
except KeyboardInterrupt:
    print("\nClosing database connection...")
    conn.commit()
    conn.close()
    print("Database connection closed.")