# Adjust the script to include a window activation check and increase delays for stability

adjusted_script_content = ""
import subprocess
import pygetwindow as gw
import pyautogui
import time
import pygame
import win32gui

# Written by Idlan bin Hafiz

# Path to your Ascension WoW client executable
client_path = r"D:\\Ascension WoW\\Ascension Launcher\\resources\\client\\Ascension.exe"
fanfare_sound = r"D:\\WinTradeBot\\ff_fanfare.mp3"  # Path to the Fanfare sound file

# Number of clients to open
num_clients = 4

# Credentials for each account
credentials = [
    {"username": "Your_Username_1", "password": "password1"},
    {"username": "Your_Username_2", "password": "password2"},
    {"username": "Your_Username_3", "password": "password3"},
    {"username": "Your_Username_4", "password": "password4"},
]

# New positions based on the updated layout
positions = [
    (-1920, 0),    # Ascension 1 - Top left of left monitor
    (0, 0),        # Ascension 2 - Top left of right monitor
    (-960, 0),     # Ascension 3 - Top right of left monitor
    (960, 0)       # Ascension 4 - Top right of right monitor
]

# Enter World button offset remains the same
relative_enter_world_button = (340, 550)

# Function to open the game clients
def open_clients():
    processes = []
    for _ in range(num_clients):
        process = subprocess.Popen(client_path)
        processes.append(process)
        time.sleep(5)  # Wait for each client to open fully
    return processes

# Function to rename windows to "Ascension 1", "Ascension 2", etc.
def rename_windows():
    # Get all windows with "Ascension" in the title
    windows = [win for win in gw.getAllWindows() if 'Ascension' in win.title]
    
    for i, window in enumerate(windows, start=1):
        new_title = f"Ascension {i}"
        hwnd = window._hWnd  # Get the handle to the window
        win32gui.SetWindowText(hwnd, new_title)
        print(f"Renamed window {window.title} to {new_title}")

# Function to log into each game window, clearing the old username first
def login_to_game(account, window):
    window.activate()
    time.sleep(1)
    pyautogui.doubleClick(window.left + 50, window.top + 50)  # Ensure the window is active
    time.sleep(1)
    pyautogui.write(account["password"])
    time.sleep(0.5)
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    pyautogui.write(account["username"])
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(5)

# Function to double-click "Enter World" for each window
def click_enter_world(window):
    enter_world_button = (window.left + relative_enter_world_button[0], window.top + relative_enter_world_button[1])
    pyautogui.doubleClick(enter_world_button)
    time.sleep(2)

# Function to activate, position, and log in to each game window
def activate_and_position_windows():
    time.sleep(10)
    windows = [win for win in gw.getAllWindows() if 'Ascension' in win.title]

    if not windows:
        print("No game windows found with 'Ascension' in the title. Ensure the game clients are open.")
        return

    for i, (window, account, position) in enumerate(zip(windows, credentials, positions), start=1):
        try:
            print(f"Activating and positioning window {i} - Title: {window.title}")
            window.activate()
            time.sleep(2)
            if not window.isActive:
                print(f"Failed to activate window {i}. Retrying...")
                window.activate()
                time.sleep(2)
            window.moveTo(position[0], position[1])
            time.sleep(1)
            login_to_game(account, window)
            click_enter_world(window)
        except Exception as e:
            print(f"Failed to login and position window {i}: {e}")

# Function to play the fanfare sound
def play_fanfare():
    pygame.mixer.init()
    pygame.mixer.music.load(fanfare_sound)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Main code execution
if __name__ == "__main__":
    open_clients()
    print("Opened clients, waiting for them to load...")
    time.sleep(20)
    
    # Rename windows after all clients are open
    rename_windows()
    
    # Activate and log into each game client
    activate_and_position_windows()
    
    # Play fanfare upon completion
    play_fanfare()
""
