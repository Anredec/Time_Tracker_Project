from datetime import datetime
import json
import threading
from active_window import active_win_open
import time
import sqlite3
from old_data_check import check_old_data

def save_data_to_file():
    """Saves the current tracking data to a text file every 1 minute."""
    with open(f"tracker_log_{datetime.today().strftime('%d-%m-%Y')}.txt", "w", encoding="utf-8") as file:
        file.write("program,project,date,total_time,start_time,end_time\n")
        for y in data_to_store:
            file.write(f"{data_to_store[y]['pro_name']},"
                       f"{data_to_store[y]['pro_seg']},"
                       f"{data_to_store[y]['date']},"
                       f"{data_to_store[y]['total_time']},"
                       f"{data_to_store[y]['start']},"
                       f"{data_to_store[y]['end']}\n")
        #json.dump(data_to_store, file, indent=4)  # Save in JSON format for readability
    print("Data saved to tracker_log.txt")  # Debugging message


def save_data_sqlite():
    '''Saves the current tracking data to a sqlite file every 1 minute.'''
    #opening sqlite
    with sqlite3.connect('tracker.db') as conn:  
        database_sql = conn.cursor()
        #checking if the information is already in the db
        for i in data_to_store:
            database_sql.execute('''
                SELECT total_time FROM usage_tracking
                WHERE program= ? AND project= ? AND date= ?;
            ''', (data_to_store[i]['pro_name'], data_to_store[i]['pro_seg'], data_to_store[i]['date']))
    
            result = database_sql.fetchone()
            
            if result:
                # Update existing entry
                database_sql.execute('''
                    UPDATE usage_tracking
                    SET total_time= ?, end_time= ?
                    WHERE program= ? AND project= ? AND date= ?;
                ''', (data_to_store[i]['total_time'], data_to_store[i]['end'], 
                      data_to_store[i]['pro_name'], data_to_store[i]['pro_seg'], data_to_store[i]['date']))
            else:
                # Insert new entry
                database_sql.execute('''
                    INSERT INTO usage_tracking(program, project, date, total_time, start_time, end_time)
                    VALUES (?,?,?,?,?,?);
                ''', (data_to_store[i]['pro_name'], data_to_store[i]['pro_seg'], data_to_store[i]['date'],
                      data_to_store[i]['total_time'], data_to_store[i]['start'], data_to_store[i]['end']))

        conn.commit()  # Ensure changes are saved
        print("SQLite Saved")

    


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


#checking if data is stored already today
data_to_store= check_old_data()
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