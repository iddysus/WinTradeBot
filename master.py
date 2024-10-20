
import pygetwindow as gw
import mss
import cv2
import numpy as np
import pytesseract
import os
import pyautogui
import time
import glob
import keyboard  # Import the keyboard module
from datetime import datetime

# Written by Idlan bin Hafiz

# Configure Tesseract executable path (adjust this path to your local setup)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Folders and offsets
testing_screenshot_folder = 'testing_screenshots'
os.makedirs(testing_screenshot_folder, exist_ok=True)

# MMR offsets
mmr_x_offset = 340
mmr_y_offset = 230
mmr_width = 40
mmr_height = 30

# Window coordinates for the game
relative_pvp_tab = (250, 380)
relative_2v2_arena = (250, 270)
relative_join_as_group = (250, 350)
relative_enter_battle = (350, 160)

# Client names
ascension_windows = ["Ascension 1", "Ascension 2", "Ascension 3", "Ascension 4"]

# Minimap offsets
minimap_x_offset = -95
minimap_y_offset = 65
minimap_width = 60
minimap_height = 60

reference_map_folder = 'reference_maps'

# Function to capture MMR from the window
def get_mmr(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        x = window.left + mmr_x_offset
        y = window.top + mmr_y_offset

        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": mmr_width, "height": mmr_height}
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = os.path.join(testing_screenshot_folder, f"{window_title}_mmr_{timestamp}.png")
            cv2.imwrite(screenshot_filename, img_gray)

            mmr_text = pytesseract.image_to_string(img_gray, config='--psm 7 digits')
            # Remove any non-numeric characters
            mmr_cleaned = ''.join(filter(str.isdigit, mmr_text))
            if mmr_cleaned:
                return int(mmr_cleaned)
            else:
                raise ValueError("No numeric MMR detected.")
    except Exception as e:
        print(f"Error retrieving MMR for {window_title}: {e}")
        return None

# Key pressing helper function
def press_key(window, key):
    window.activate()
    time.sleep(0.5)
    pyautogui.press(key)
    time.sleep(0.5)

# Function to open and navigate to PvP
def open_pvp_tab(window):
    window.activate()
    time.sleep(1)
    pyautogui.press('i')
    time.sleep(2)
    pvp_tab_position = (window.left + relative_pvp_tab[0], window.top + relative_pvp_tab[1])
    for _ in range(3):
        pyautogui.click(pvp_tab_position)
        time.sleep(0.1)

# Selecting 2v2 Arena
def select_2v2_arena(window):
    arena_position = (window.left + relative_2v2_arena[0], window.top + relative_2v2_arena[1])
    pyautogui.moveTo(arena_position)
    time.sleep(0.5)
    for _ in range(3):
        pyautogui.click(arena_position)
        time.sleep(0.1)

# Joining as a group
def join_as_group(window):
    join_group_position = (window.left + relative_join_as_group[0], window.top + relative_join_as_group[1])
    pyautogui.moveTo(join_group_position)
    time.sleep(0.5)
    for _ in range(3):
        pyautogui.click(join_group_position)
        time.sleep(0.1)

# Entering the battle
def enter_battle(window):
    enter_battle_position = (window.left + relative_enter_battle[0], window.top + relative_enter_battle[1])
    pyautogui.moveTo(enter_battle_position)
    time.sleep(0.5)
    for _ in range(3):
        pyautogui.click(enter_battle_position)
        time.sleep(0.1)

# Mount up on leader bots
def mount_up():
    for title in ["Ascension 1", "Ascension 3"]:
        try:
            window = gw.getWindowsWithTitle(title)[0]
            press_key(window, 'r')
        except IndexError:
            print(f"Error: {title} window not found.")

# Follow Ascension 1 with Ascension 3
def follow_ascension1():
    try:
        ascension3 = gw.getWindowsWithTitle("Ascension 3")[0]
        press_key(ascension3, 'f')
    except IndexError:
        print("Error: Ascension 3 window not found.")

# Wait for arena start
def wait_for_arena_start():
    time.sleep(45)

# Taking minimap screenshot
def take_minimap_screenshot():
    ascension1 = gw.getWindowsWithTitle("Ascension 1")[0]
    x = ascension1.left + ascension1.width + minimap_x_offset
    y = ascension1.top + minimap_y_offset

    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": minimap_width, "height": minimap_height}
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(f"{testing_screenshot_folder}/minimap_{timestamp}.png", img_bgr)

        return img_bgr

# Recognizing map based on screenshot
def recognize_arena_map(minimap_screenshot):
    print("Recognize arena map function called.")
    map_names = ["NagrandArena", "BlackRookHold", "AshamaneFall", 'TigersPeak', 'RuinsOfLordaeron', 'BladesEdgeArena']
    threshold = 200000  # Lowered threshold to reduce false positives

    for map_name in map_names:
        reference_images = glob.glob(f"{reference_map_folder}/{map_name}_1.png")
        print(f"Reference images for {map_name}: {reference_images}")
        
        for ref_image_path in reference_images:
            ref_image = cv2.imread(ref_image_path, cv2.IMREAD_COLOR)
            if ref_image is None or ref_image.shape[:2] != (60, 60):
                continue

            difference = cv2.absdiff(minimap_screenshot, ref_image)
            difference_score = np.sum(difference)
            print(f"Map: {map_name}, Image: {ref_image_path}, Difference: {difference_score}")

            if difference_score < threshold:
                print(f"Map recognized: {map_name}")
                return map_name

    print("No map recognized.")
    return None

# Moving based on map recognition
def path_ascension1_based_on_map(map_name):
    try:
        ascension1 = gw.getWindowsWithTitle("Ascension 1")[0]
    except IndexError:
        print("Ascension 1 window not found. Ensure the window is open and named correctly.")
        return

    if ascension1.isMinimized:
        ascension1.restore()

    try:
        ascension1.activate()
    except Exception as e:
        print(f"Failed to activate Ascension 1 window: {e}")
        return
    
    if map_name in ["RuinsOfLordaeron"]:
        pyautogui.press("w", presses=1, interval=0.5)
        pyautogui.keyDown("w")
        time.sleep(4)
        pyautogui.keyUp("w")
        pyautogui.keyDown("d")
        time.sleep(2.75)
        pyautogui.keyUp("d")
        pyautogui.keyDown("w")
        time.sleep(2)
        pyautogui.keyUp("w")
        pyautogui.keyDown("a")
        time.sleep(3)
        pyautogui.keyUp("a")
        pyautogui.keyDown("w")
        time.sleep(4.6)
        pyautogui.keyUp("w")

    elif map_name in ["TigersPeak"]:
        pyautogui.press("w", presses=1, interval=0.5)
        pyautogui.keyDown("w")
        time.sleep(2)
        pyautogui.keyUp("w")
        pyautogui.keyDown("d")
        time.sleep(1)
        pyautogui.keyUp("d")
        pyautogui.keyDown("w")
        time.sleep(6)
        pyautogui.keyUp("w")
        pyautogui.keyDown("a")
        time.sleep(1)
        pyautogui.keyUp("a")
        pyautogui.keyDown("w")
        time.sleep(2.2)
        pyautogui.keyUp("w")
        
    elif map_name in ["NagrandArena"]:
        pyautogui.press("w", presses=2, interval=0.5)
        pyautogui.keyDown("w")
        time.sleep(8.2)
        pyautogui.keyUp("w")

    elif map_name in ["AshamaneFall"]:
        pyautogui.press("w", presses=2, interval=0.5)
        pyautogui.keyDown("w")
        time.sleep(9.1)
        pyautogui.keyUp("w")
        
    elif map_name == "BlackRookHold":
        pyautogui.press("a", presses=1, interval=0.5)
        pyautogui.keyDown("a")
        time.sleep(0.8)
        pyautogui.keyUp("a")
        pyautogui.keyDown("w")
        time.sleep(6.6)
        pyautogui.keyUp("w")
        pyautogui.keyDown("d")
        time.sleep(3)
        pyautogui.keyUp("d")
        
    else:  # Default path for Blade's Edge Arena
        pyautogui.press("w", presses=1, interval=0.5)
        pyautogui.keyDown("w")
        time.sleep(6)
        pyautogui.keyUp("w")
        pyautogui.keyDown("d")
        time.sleep(3.3)
        pyautogui.keyUp("d")
        pyautogui.keyDown("w")
        time.sleep(1.6)
        pyautogui.keyUp("w")

def move_ascension3_after_pathing():
    try:
        ascension3 = gw.getWindowsWithTitle("Ascension 3")[0]
        ascension3.activate()
        time.sleep(0.4)
        pyautogui.press("w", presses=1, interval=0.5)
        pyautogui.keyDown("w")
        time.sleep(0.4)
        pyautogui.keyUp("w")
    except IndexError:
        print("Error: Ascension 3 window not found.")

#Execute Combat after Pathing
def execute_combat_sequence(winner):
    odd_team = ["Ascension 1", "Ascension 3"]
    even_team = ["Ascension 2", "Ascension 4"]
    
    winning_team = odd_team if winner == "Ascension 1" else even_team
    losing_team = even_team if winner == "Ascension 1" else odd_team
    
    combat_duration = 38  # Duration in seconds for each cycle before switching target
    
    for cycle in range(1):  # one cycle, with a tab target in between
        end_time = time.time() + combat_duration
        
        while time.time() < end_time:
            # Winning team presses '1'
            for player in winning_team:
                window = gw.getWindowsWithTitle(player)[0]
                window.activate()
                pyautogui.press("1")
                time.sleep(0.2)
                pyautogui.press("2")
                time.sleep(0.2)
            
            # Losing team presses 'g'
            for player in losing_team:
                window = gw.getWindowsWithTitle(player)[0]
                window.activate()
                pyautogui.press("g")
                time.sleep(0.4)
        
        # After the cycle duration, tab target
        for player in winning_team + losing_team:
            window = gw.getWindowsWithTitle(player)[0]
            window.activate()
            pyautogui.press("tab")
            time.sleep(0.3)
    
    time.sleep(5)  # Wait for the fight to fully conclude
    
    # Leave arena
def leave_arena():
    # Coordinates for the "Leave Arena" button near the bottom center
    leave_arena_x_offset = 0  # Adjust if necessary to match the button's horizontal position
    leave_arena_y_offset = -185  # Adjust based on the vertical distance from the bottom of the window

    for player in ascension_windows:
        try:
            window = gw.getWindowsWithTitle(player)[0]
            window.activate()
            time.sleep(1)
            
            # Calculate the exact position for the "Leave Arena" button click
            leave_arena_x = window.left + window.width // 2 + leave_arena_x_offset
            leave_arena_y = window.top + window.height + leave_arena_y_offset
            
            pyautogui.click(leave_arena_x, leave_arena_y)
            time.sleep(0.5)
        except IndexError:
            print(f"Error: {player} window not found.")




# Main sequence
def perform_full_sequence():
    print("Starting sequence with MMR check...")
    windows = [gw.getWindowsWithTitle(title)[0] for title in ascension_windows if gw.getWindowsWithTitle(title)]
    for window in windows[:2]:
        open_pvp_tab(window)
        select_2v2_arena(window)
        join_as_group(window)

    time.sleep(5)
    ascension_1_mmr = get_mmr("Ascension 1")
    ascension_2_mmr = get_mmr("Ascension 2")

    if ascension_1_mmr is None or ascension_2_mmr is None:
        print("MMR detection failed. Aborting.")
        return

    winner = "Ascension 1" if ascension_1_mmr < ascension_2_mmr else "Ascension 2"
    print(f"Winner: {winner} with lower MMR.")

    for window in windows:
        enter_battle(window)

    time.sleep(10)
    mount_up()
    follow_ascension1()

    minimap_screenshot = take_minimap_screenshot()
    map_name = recognize_arena_map(minimap_screenshot)
    print(f"Recognized map: {map_name}" if map_name else "Map recognition failed.")

    wait_for_arena_start()
    path_ascension1_based_on_map(map_name)
    move_ascension3_after_pathing()
    execute_combat_sequence(winner)
    leave_arena()
    print(f"Sequence complete. Winner: {winner}.")

if __name__ == "__main__":
    for i in range(10):
        print(f"Starting iteration {i + 1}...")

        # Check if Q is pressed to break the loop
        if keyboard.is_pressed('q'):
            print("Q key pressed. Stopping iterations.")
            break

        perform_full_sequence()
        print(f"Iteration {i + 1} complete.")
        
        # Optional delay between iterations; adjust as needed
        time.sleep(5)
