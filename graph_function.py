from datetime import datetime, timedelta
import pandas as pd
import seaborn as sns
import sqlite3
import matplotlib.pyplot as plt
#from dateutil.relativedelta import relativedelta  # Import for handling months

def df_search(): 
    """Get from the SQL the information needed and return a sorted DataFrame."""
    
    with sqlite3.connect('tracker.db') as conn:
        filter_type = input("You want a graph of: today/yesterday/last_week/last_month: ").strip().lower()
        
        today = datetime.today().strftime('%d-%m-%Y')  # Store as string
        
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
        
        


def graph_maker(data_frame, vers, total_time):
    """Using the version (pie OR bar) this function will create a pie chart or cumulative bar chart"""
    colors = sns.color_palette("pastel", n_colors=10)

    # Replace empty program names with 'Unknown'
    data_frame.loc[data_frame['program'] == "", 'program'] = 'Unknown'
    
    # Ensure we are modifying a copy and not overwriting
    data_frame = data_frame.copy()

    # Create a combined column for program and project
    data_frame["pro_pro"] = data_frame['program'] + " " + data_frame['project']
    # pie chart Creation   
    if vers == "pie":
        plt.figure(figsize=(10,10))
        plt.pie(data_frame['total_time_min'], 
                colors=colors, 
                labels=data_frame['pro_pro'], 
                autopct='%1.1f%%', 
                startangle=90, 
                pctdistance=0.7, 
                labeldistance=1.05, 
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
        
        plt.suptitle("Distribution of Time Spent Using the Computer", y=0.95, fontsize=18)
        plt.title(f'Total Time on Computer: {total_time} min')
        plt.axis('equal')
        plt.show()
    else:
        
        grouped_df = data_frame.groupby(['date', 'pro_pro'])['total_time_min'].sum().reset_index()
        pivot_df = grouped_df.pivot(index="date", columns="pro_pro", values="total_time_min").fillna(0)

        #Plot stacked bar chart
        pivot_df.plot(kind="bar", stacked=True, figsize=(12,6), colormap="Pastel1")
        
        plt.title("Top 5 Most Used Programs Per Day (Stacked Bar Chart)")
        plt.xlabel("Date")
        plt.xticks(rotation=45)
        plt.ylabel("Total Time (Minutes)")
        plt.legend(title="Programs", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.show()

    



