from datetime import datetime, timedelta
import pandas as pd
import seaborn as sns
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path
import os
import plotly.express as px
#from dateutil.relativedelta import relativedelta  # Import for handling months

def df_search_sql(filter_type): 
    """Get from the SQL the information needed and return a sorted DataFrame."""
    
    with sqlite3.connect('tracker.db') as conn:
        #filter_type = input("You want a graph of: today/yesterday/last_week/last_month: ").strip().lower()
        
        today = datetime.today().strftime('%d-%m-%Y')  
        
        if filter_type == "today":
            sql = "SELECT * FROM usage_tracking WHERE date = ?;"
            params = (today,)
            version= "pie"
        
        elif filter_type == "yesterday":
            date = (datetime.today() - timedelta(days=1)).strftime('%d-%m-%Y')
            sql = "SELECT * FROM usage_tracking WHERE date = ?;"
            params = (date,)
            version= "pie"
        
        elif filter_type == "last_week":
            date = (datetime.today() - timedelta(days=7)).strftime('%d-%m-%Y')
            sql = "SELECT * FROM usage_tracking WHERE date BETWEEN ? AND ?;"
            params = (date, today)
            version= "bar"
        
        elif filter_type == "last_month":
            date = (datetime.today() - timedelta(days=30)).strftime('%d-%m-%Y')  
            sql = "SELECT * FROM usage_tracking WHERE date BETWEEN ? AND ?;"
            params = (date, today)
            version= "bar"
        
        else:
            raise ValueError("Invalid filter type. Choose: today/yesterday/last_week/last_month")
        
        # Read SQL query into DataFrame
        df = pd.read_sql_query(sql, conn, params=params)

        # Sorting and Formatting
        if not df.empty:
            if version == "pie":
                df_sorted = df.sort_values(by='total_time', ascending=False).head(10)
                df_sorted['total_time_min'] = (df_sorted['total_time'] / 60).astype(int)
                total_time=0
                for i in df_sorted['total_time_min']:
                    total_time +=i
                return df_sorted, version, total_time
            else:
                df_sorted= df.sort_values(by=['date','total_time'], ascending=[True, False])
                df_sorted["total_time_min"]= (df_sorted['total_time'] / 60).astype(int)
                df_sorted["rank"]= df_sorted.groupby('date')['total_time'].rank(method='dense', ascending=False)
                ranked_df= df_sorted[df_sorted['rank'] <=5]
                total_time=0
                for i in df_sorted['total_time_min']:
                    total_time +=i
                return ranked_df, version, total_time
        else:
            print("No data found for the selected period.")
            return None
        
def df_search_csv(filter_type):
    """Get from the csv files the information needed and return a sorted DataFrame."""
    today = datetime.today().strftime('%d-%m-%Y')
    folder_name = "data"
    df = pd.DataFrame()  # Initialize df to avoid UnboundLocalError

    if filter_type == "today":
        try:
            my_file = Path(os.path.join(folder_name, f"tracker_log_{today}.csv"))
            version = "pie"
            df = pd.read_csv(my_file)
        except FileNotFoundError:
            print("Log not found")
    
    elif filter_type == "yesterday":
        try:
            yesterday = (datetime.today() - timedelta(days=1)).strftime('%d-%m-%Y')
            version = "pie"
            my_file = Path(os.path.join(folder_name, f"tracker_log_{yesterday}.csv"))
            df = pd.read_csv(my_file)
        except FileNotFoundError:
            print("Log not found")
    
    elif filter_type in ["last_week", "last_month"]:
        version = "bar"
        days = 7 if filter_type == "last_week" else 30

        for i in range(days):
            date = (datetime.today() - timedelta(days=i)).strftime('%d-%m-%Y')
            my_file = Path(os.path.join(folder_name, f"tracker_log_{date}.csv"))
            try:
                read = pd.read_csv(my_file).sort_values('total_time', ascending=False)
                df = pd.concat([df, read], ignore_index=True)
            except FileNotFoundError:
                print(f'{date} not found')
    
    else:
        print("Mode not found")
        return None

    # Check if df has data before accessing it
    if df.empty:
        print("No data found for the selected period.")
        return None

    # Sorting and Formatting
    if version == "pie":
        df_sorted = df.sort_values(by='total_time', ascending=False).head(10)
        df_sorted['total_time_min'] = (df_sorted['total_time'] / 60).astype(int)
        total_time = df_sorted['total_time_min'].sum()
        return df_sorted, version, total_time
    else:
        df_sorted = df.sort_values(by=['date', 'total_time'], ascending=[True, False])
        df_sorted["total_time_min"] = (df_sorted['total_time'] / 60).astype(int)
        df_sorted["rank"] = df_sorted.groupby('date')['total_time'].rank(method='dense', ascending=False)
        ranked_df = df_sorted[df_sorted['rank'] <= 5]
        total_time = df_sorted['total_time_min'].sum()
        return ranked_df, version, total_time
        
        
            



def graph_maker(data_frame, vers, total_time):
    """Create an interactive pie chart or cumulative bar chart with consistent colors."""
    
    # Replace empty program names with 'Unknown'
    data_frame.loc[data_frame['program'] == "", 'program'] = 'Unknown'
    
    # Ensure we are modifying a copy
    data_frame = data_frame.copy()

    # Create a combined column for program and project
    data_frame["pro_pro"] = data_frame['program'] + " " + data_frame['project']

    # 🔵 **Assign consistent colors to each program-project combination**
    unique_programs = data_frame["pro_pro"].unique()
    color_map = {program: px.colors.qualitative.Safe[i % len(px.colors.qualitative.Safe)] 
                 for i, program in enumerate(unique_programs)}

    if vers == "pie":
        fig = px.pie(data_frame, 
                     names="pro_pro", 
                     values="total_time_min", 
                     title=f"Total Time on Computer: {total_time} min",
                     color="pro_pro", 
                     color_discrete_map=color_map,  # Apply consistent colors
                     hover_data=["program", "project"])  # Show extra info on hover
        fig.update_traces(textinfo="percent+label")
        fig.show()

    else:  # Stacked Bar Chart
        grouped_df = data_frame.groupby(['date', 'pro_pro'], as_index=False).first()
        fig = px.bar(grouped_df, 
                     x="date", 
                     y="total_time_min", 
                     color="pro_pro",
                     title="Top 5 Most Used Programs Per Day (Stacked Bar Chart)",
                     labels={"pro_pro": "Programs", "total_time_min": "Total Time (Minutes)"},
                     color_discrete_map=color_map,  # Apply consistent colors
                     hover_data=["pro_pro", "total_time_min"])  # Show extra info on hover
        fig.update_layout(barmode="stack", xaxis_tickangle=-45)
        fig.show()
   


