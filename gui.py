import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
from active_window import active_win_open
from save_module import save_data_sqlite, save_data_to_file
from graph_function import graph_maker, df_search_csv
from old_data_check import check_old_data
import sqlite3

class TimeTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        self.root.geometry("350x150")

        # vars for checking state
        self.running = False
        self.sleeping_time = 10
        self.data_to_store = {}

        # Check if SQLite is available
        self.sqlite_available = self.check_sqlite()

        # GUI Elements
        self.start_button = tk.Button(root, text="Start", command=self.start_tracking)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_tracking, state=tk.DISABLED)
        self.graph_label = tk.Label(root, text="Select a period to graph:")
        self.graph_type = ttk.Combobox(root, values=["Today", "Yesterday", "Last Week", "Last Month"])
        self.graph_button = tk.Button(root, text="Show Graph", command=self.show_graph)
        self.save_mode = tk.Label(root, text="Save data as:")

        # Set default options for save format
        save_options = ["CSV"]
        if self.sqlite_available:
            save_options.append("SQL")

        self.save_type = ttk.Combobox(root, values=save_options, state="readonly")
        self.save_type.set("CSV")  # Default to CSV
        
        #on closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # positioning
        self.start_button.grid(row=0, column=0, padx=10, pady=5)
        self.stop_button.grid(row=0, column=1, padx=30, pady=5)
        self.save_mode.grid(row=1, column=0, padx=10, pady=5)
        self.save_type.grid(row=1, column=1, padx=30, pady=5)
        self.graph_label.grid(row=2, column=0, padx=10, pady=5)
        self.graph_type.grid(row=2, column=1, padx=30, pady=5)
        self.graph_button.place(x=140, y=110)

    def check_sqlite(self):
        """Check if SQLite is available on the system."""
        try:
            conn = sqlite3.connect(":memory:")
            conn.close()
            return True
        except Exception as e:
            messagebox.showerror("SQLite Error", f"SQLite is not available.\n{e}")
            return False

    def track_usage(self):
        """Function to track active window usage"""
        while self.running:
            today_date = datetime.today().strftime('%d-%m-%Y')
            now = datetime.today().strftime('%H:%M')

            time.sleep(self.sleeping_time)
            project, program = active_win_open()
            if project is None or program is None:
                continue

            name = f"{program} - {project}"
            if name in self.data_to_store:
                self.data_to_store[name]['total_time'] += self.sleeping_time
                self.data_to_store[name]['end'] = now
            else:
                self.data_to_store[name] = {
                    'total_time': self.sleeping_time,
                    'start': now,
                    'end': now,
                    'date': today_date,
                    'pro_name': program,
                    'pro_seg': project
                }

    def sql_table_check(self):
        """Check if the SQLite database exists and create the table if necessary."""
        conn = sqlite3.connect('tracker.db')
        database_sql = conn.cursor()
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
        conn.close()

    def save_data(self):
        """Saves the tracking data based on the selected format"""
        format_choice = self.save_type.get()

        if format_choice == "CSV":
            save_data_to_file(self.data_to_store)

        elif format_choice == "SQL":
            if not self.sqlite_available:
                messagebox.showerror("Error", "SQLite is not available on your system.")
                return
            save_data_sqlite(self.data_to_store)

        else:
            messagebox.showerror("Error", "Please select a save format.")

        if self.running:
            threading.Timer(60, self.save_data).start()  # Save every 60 seconds

    def start_tracking(self):
        """Starts tracking active window usage"""
        if self.save_type.get() == "SQL" and not self.sqlite_available:
            messagebox.showerror("Error", "SQLite is not available. Cannot save to SQL.")
            return

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        if self.save_type.get() == "SQL":
            self.sql_table_check()

        self.data_to_store = check_old_data(self.save_type.get())

        tracking_thread = threading.Thread(target=self.track_usage, daemon=True)
        tracking_thread.start()

        self.save_data()  # Start saving data loop

    def stop_tracking(self):
        """Stops the tracking process"""
        self.running = False
        self.save_data()
        messagebox.showinfo(title="Process stopped", message="Time tracking has been stopped.\nSaving data...")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def show_graph(self):
        """Displays a graph based on selected type"""
        graph_choice = self.graph_type.get()
        if graph_choice:
            df, vers, total_time = df_search_csv(graph_choice.lower().replace(" ", "_"))
            if df is not None:
                graph_maker(df, vers, total_time)
            else:
                messagebox.showerror("Error", "No data available for this period.")
        else:
            messagebox.showerror("Error", "Please select a graph type.")
            
            
    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you wish to quit?"):
            self.running= False
            self.save_data()        
            self.root.destroy()    
    

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerGUI(root)
    root.mainloop()
