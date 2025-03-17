from datetime import datetime
from pathlib import Path
import sqlite3
import os

def save_data_to_file(data_to_store):
    """Saves the current tracking data to a text file"""
    folder_name= "data"
    today_file = Path(os.path.join(folder_name, f"tracker_log_{datetime.today().strftime('%d-%m-%Y')}.csv"))
    
    with open(today_file, "w", encoding="utf-8") as file:
        file.write("program,project,date,total_time,start_time,end_time\n")
        for y in data_to_store:
            file.write(f"{data_to_store[y]['pro_name']},"
                       f"{data_to_store[y]['pro_seg']},"
                       f"{data_to_store[y]['date']},"
                       f"{data_to_store[y]['total_time']},"
                       f"{data_to_store[y]['start']},"
                       f"{data_to_store[y]['end']}\n")
        
    print("Data saved to tracker_log.txt")  # Debugging message


def save_data_sqlite(data_to_store):
    '''Saves the current tracking data to a sqlite file'''
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