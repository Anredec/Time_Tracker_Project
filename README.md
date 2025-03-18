# Time Tracker

## Project Overview

Time Tracker is a Python-based application that monitors the time spent on different programs and projects. It automatically logs active windows, saves the data, and provides visual reports.

## Project Structure

- **main.py**: Entry point that initializes and runs the GUI.
- **gui.py**: Manages the graphical interface using Tkinter.
- **active\_window\.py**: Detects the currently active window.
- **save\_module.py**: Handles saving data to CSV and SQLite.
- **graph\_function.py**: Generates graphical reports of tracked time.
- **old\_data\_check.py**: Checks for previously stored session data.
- **tracker.db**: SQLite database for storing usage data (if SQL mode is selected).

## How It Works

1. The user starts tracking, and the application records the active window every 10 seconds.
2. The recorded data includes the program name, project name, start time, end time, and total time spent.
3. The user can choose to save data as CSV or in an SQLite database.
4. The user can generate graphs to visualize usage for different time periods.

## Installation Guide

### Prerequisites

- Python 3.8 or later
- Required dependencies (Tkinter, Pandas, Matplotlib, SQLite3)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Anredec/Time_Tracker_Project.git
   cd time-tracker
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Select a save format (CSV/SQL).
2. Click **Start** to begin tracking.
3. Click **Stop** to save and stop tracking.
4. Choose a time period and click **Show Graph** to view data.

## Future Improvements

- Custom time intervals for tracking
- Export options (PDF, Excel)
- Advanced filtering and report generation


