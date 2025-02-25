# Time Tracker Project

## Overview
This project is a Python-based time tracker that monitors which program you are actively using. If you are using Firefox, it will also track which webpage you are on. The program will log data every 5 minutes and generate visual graphs showing time spent on different applications/webpages.

## Features
- Detect which program is currently active.
- If using Firefox, extract the current webpage URL.
- Track the time spent in each program or webpage.
- Log data into a CSV file or MySQL database every 5 minutes.
- Generate graphs summarizing daily and weekly usage.
- Optional UI (to be determined later).

## Technologies Used
- **Active Window Detection**: `psutil`, `pygetwindow`, `pywinctl`
- **Firefox Page Tracking**: `win32gui`, `xdotool` (Linux), or `browser API`
- **Time Tracking**: `datetime`, `schedule`
- **Data Storage**: `csv`, `MySQL (mysql-connector-python)`
- **Graph Generation**: `matplotlib`, `pandas`
- **Optional UI**: `tkinter`, `PyQt`, or `streamlit`

## Project Structure
```
/time-tracker
│-- tracker.py          # Main script for tracking and logging data
│-- data_handler.py     # Handles saving data to CSV/MySQL
│-- graph_generator.py  # Generates daily/weekly graphs
│-- README.txt          # To-do list and documentation
│-- requirements.txt    # List of dependencies
│-- config.py           # Configuration file (database settings, interval settings, etc.)
│-- logs/               # Folder to store CSV logs (if not using MySQL)
```

## To-Do List
### Phase 1: Basic Tracking
- [ ] Detect which program is currently active
- [ ] Track time spent per program
- [ ] If using Firefox, extract the active webpage
- [ ] Store recorded data in memory

### Phase 2: Data Logging
- [ ] Save the data to a CSV file
- [ ] Add support for MySQL storage
- [ ] Automate data logging every 5 minutes

### Phase 3: Data Visualization
- [ ] Generate a daily usage graph
- [ ] Implement a weekly usage graph
- [ ] Display graphs before closing the program

### Phase 4: Optional Enhancements
- [ ] Decide whether a UI is needed
- [ ] Add real-time tracking visualization
- [ ] Implement additional features (e.g., productivity analysis)

## Next Steps
1. Set up a Python environment and install necessary libraries.
2. Start with detecting active applications.
3. Implement Firefox webpage tracking.
4. Develop a basic CSV logging system.
5. Expand to MySQL if needed.
6. Work on graph generation.

---
This document will be updated as the project progresses. Happy coding!

