"""
Simple PyAutoGUI wrapper for DCS Pylote
Provides basic automation functionality including key presses
"""

from enum import Enum
import pyautogui
import time

MENU_GAP = 35
SLOT_MENU_GAP = 20

# Predefined button locations for DCS World UI
# Coordinates are relative to the DCS window's top-left corner  
# These may need adjustment based on screen resolution and UI scaling
# These coordinates are based on a 1920x1080 resolution with 100% UI scale
class ButtonLocations(Enum):
    BRIEFING_BUTTON = (1050, 650)
    FIRST_TIME_MULTIPLAYER_CHECKBOX = (300, 660)
    FIRST_TIME_MULTIPLAYER_OKAY = (660, 700)
    FLY_BUTTON = (1200, 770)
    IP_TEXT_FIELD = (660, 400)
    IP_TEXT_SUBMIT = (960, 430)
    JOIN_BY_IP = (940, 100)
    JOIN_BLUE_COALITION = (900, 690)
    JOIN_RED_COALITION = (390, 690)
    JOIN_SERVER = (650, 740)
    MENU_START = (1100, 220)
    SLOT_MENU_START = (630, 315)
    QUIT_BUTTON = (660, 500)

class MenuItems(Enum):
    INSTANT_ACTION = 0
    QUICK_ACTION = 1
    MISSION = 2
    CAMPAIGN = 3
    MULTIPLAYER = 4
    # Gap
    LOGBOOK = 6
    ENCYCLOPEDIA = 7
    TRAINING = 8
    REPLAY = 9
    # Gap
    MISSION_EDITOR = 11
    CAMPAIGN_BUILDER = 12
    # Big Gap
    EXIT = 15


class DCSAutoGUI():
    """Wrapper class for PyAutoGUI to provide basic automation functionality"""
    
    def __init__(self, dcs_window):
        self.dcs_window = dcs_window
        # Initialize any settings if needed
        pyautogui.FAILSAFE = True  # Move mouse to top-left to abort
        print("DCSAutoGUI initialized with failsafe enabled.")
    
    def button_click(self, button_location: ButtonLocations):
        """Clicks on a button based on the ButtonLocations enum"""
        x, y = button_location.value
        self.window_relative_click(x, y)
        time.sleep(0.2)  # Brief pause after click
    
    def close_data_collection_popup(self):
        """Closes the DCS data collection popup if it appears"""
        # Ensure the DCS window is focused before pressing 'esc'
        self.dcs_window.activate()
        time.sleep(0.2)  # Give time for window to focus
        pyautogui.press('esc')

    def main_menu_click(self, menu_item: MenuItems):
        """Clicks on a main menu item based on the MenuItems enum"""
        x, y = ButtonLocations.MENU_START.value
        y = y + (menu_item.value * MENU_GAP)
        self.window_relative_click(x, y)
        time.sleep(0.2)  # Brief pause after click
    
    def multiplayer_slot_click(self, slot_index: int):
        """Clicks on a multiplayer slot based on the slot index (0-based)"""
        x, y = ButtonLocations.SLOT_MENU_START.value
        y = y + (slot_index * SLOT_MENU_GAP)
        self.window_relative_click(x, y)
        time.sleep(0.2)  # Brief pause after click
    
    def print_mouse_position(self):
        """Prints the current mouse position relative to the DCS window"""
        x, y = pyautogui.position()
        rel_x = x - self.dcs_window.left
        rel_y = y - self.dcs_window.top
        print(f"Mouse position relative to DCS window: ({rel_x}, {rel_y})")
    
    def quit_dcs(self):
        """Quits DCS by clicking the Quit button in the main menu"""
        pyautogui.press('esc')  # Ensure we are in the main menu
        time.sleep(1)  # Wait for the exit confirmation dialog to appear
        self.button_click(ButtonLocations.QUIT_BUTTON)
        time.sleep(1)  # Wait for the quit process to complete
        pyautogui.press('space')  # Confirm quit if needed
        print("Quit command issued to DCS World.")
    
    def typewrite(self, text, interval=0.05):
        """Types out the given text with a specified interval between keystrokes"""
        pyautogui.typewrite(text, interval=interval)
        time.sleep(0.2)  # Brief pause after typing

    def window_relative_click(self, x, y):
        """Clicks at a position relative to the DCS window"""
        abs_x = self.dcs_window.left + x
        abs_y = self.dcs_window.top + y
        pyautogui.moveTo(abs_x, abs_y)
        time.sleep(0.5)  # Brief pause
        pyautogui.leftClick()
