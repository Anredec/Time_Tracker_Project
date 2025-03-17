from datetime import datetime
from pathlib import Path
import pandas as pd
import os
import sqlite3

def check_old_data(version):
    

    today = datetime.today().strftime('%d-%m-%Y')
    
    if version == "CSV":
        folder_name= "data"
        
        my_file = Path(os.path.join(folder_name, f"tracker_log_{today}.csv"))

        if my_file.exists():
            df = pd.read_csv(my_file)
            data = {}

            for _, row in df.iterrows():
                name = f"{row['program']}-{row['project']}"
                data[name] = {
                    'total_time': row['total_time'],
                    'start': row['start_time'],
                    'end': row['end_time'],
                    'date': row['date'],
                    'pro_name': row['program'],
                    'pro_seg': row['project']
                }
            return data
        else:
            print("Data not found")
            return {}

    elif version == "SQL":
        try:
            with sqlite3.connect('tracker.db') as conn:  
                database_sql = conn.cursor()

                # Checking if the information is already in the database
                database_sql.execute('''
                    SELECT program, project, total_time, start_time, end_time, date
                    FROM usage_tracking
                    WHERE date = ?;
                ''', (today,))

                results = database_sql.fetchall()

                if not results:
                    print("Data not found in SQL database")
                    return {}

                data = {}
                for row in results:
                    name = f"{row[0]}-{row[1]}"  # program-project
                    data[name] = {
                        'total_time': row[2],
                        'start': row[3],
                        'end': row[4],
                        'date': row[5],
                        'pro_name': row[0],
                        'pro_seg': row[1]
                    }

                return data

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {}



                       
                       

