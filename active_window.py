import psutil
import pygetwindow as gw
import win32process
import win32gui
import re

def active_win_open():
    """This function aims to get the PID of the active window and return the name of the program and its specific detail."""
    pattern = r'([^\-—]+)\s*(?:-|—)\s*([^\-—]+)$'
    hwnd_activo = gw.getActiveWindow()
    if hwnd_activo is None:
        return None, None  # No active window
    
    hwnd_activo = hwnd_activo._hWnd
    active_pid = win32process.GetWindowThreadProcessId(hwnd_activo)[1]
    
    window_title = win32gui.GetWindowText(hwnd_activo)
    print(window_title)  # Debugging: Check what title is retrieved
    
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['pid'] == active_pid:
            #center_prog = re.search(pattern_middle, window_title)  # Extract middle part
            match = re.search(pattern, window_title)
            if match:
                middle_part = match.group(1).strip()  # Extracts the middle part
                final_part = match.group(2).strip()  # Extracts the last part
            else:
                middle_part = ""
                final_part = window_title.strip()  # If no match, assume it's a standalone program
            if "overflow" in final_part:
                final_part= proc.info['name']
            
            return middle_part, final_part
    
    return None, None  # Return None if nothing found
