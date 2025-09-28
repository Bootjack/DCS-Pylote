"""
Main entry point for DCS Pylote application.

This module provides the main application loop and command-line interface
for bridging DCS-BIOS data with vJoy virtual joystick inputs.
"""

import sys
import time
import logging
from typing import Optional
import click
from colorama import init, Fore, Style
import pygetwindow as gw

from .utils.logger import setup_logging

from .vendor.dcs_client import DCSClient, DCSLaunchMode
from .vendor.autogui import ButtonLocations, DCSAutoGUI, MenuItems

# Initialize colorama for Windows
init(autoreset=True)

# Setup logging
log_level = logging.DEBUG
setup_logging(log_level)
logger = logging.getLogger(__name__)

def start_dcs_client():
    loading_time = 5  # seconds to wait for DCS to load
    polling_interval = 0.5  # seconds
    polling_timeout = 60  # seconds
    polling_time = 0

    # Initialize DCS Client
    logger.info("Starting DCS Client...")
    dcs_client = DCSClient(mode=DCSLaunchMode.NORMAL)
    dcs_client.launch()

    window = None
    logger.debug("Waiting for DCS window to appear...")
    while window is None and polling_time < polling_timeout:
        windows = gw.getWindowsWithTitle(dcs_client.instance_id)
        if windows:
            window = windows[0]
            logger.info(f"DCS window found: {window.title}")
        else:
            time.sleep(polling_interval)
            polling_time += polling_interval

    time.sleep(loading_time)  # Wait for DCS to fully initialize

    # Initialize DCSAutoGUI to handle popups
    gui = DCSAutoGUI(window)
    gui.close_data_collection_popup()
    gui.main_menu_click(MenuItems.MULTIPLAYER)

    return dcs_client, gui

def join_multiplayer_session(gui: DCSAutoGUI, server_ip = '127.0.0.1', server_port = '10308', coalition: str = 'blue', slot_index: int = 0):
    """
    Automates joining a multiplayer session in DCS World.

    :param gui: Instance of DCSAutoGUI for interaction.
    :param server_ip: IP address of the multiplayer server.
    :param slot_index: Index of the slot to join (0-based).
    """
    server_address = f"{server_ip}:{server_port}"
    logger.info(f"Joining multiplayer server at {server_address}...")
    gui.button_click(ButtonLocations.JOIN_BY_IP)
    time.sleep(1)

    # Enter server IP
    gui.button_click(ButtonLocations.IP_TEXT_FIELD)
    gui.typewrite(server_address, interval=0.05)
    gui.button_click(ButtonLocations.IP_TEXT_SUBMIT)

    logger.info("Submitted server IP, waiting for server response...")
    time.sleep(90)

    logger.info("Selecting coalition and slot...")

    # Handle first-time multiplayer popup if it appears
    gui.button_click(ButtonLocations.FIRST_TIME_MULTIPLAYER_OKAY)
    time.sleep(10)

    # Select coalition
    if coalition.upper() == 'BLUE':
        gui.button_click(ButtonLocations.JOIN_BLUE_COALITION)
    elif coalition.upper() == 'RED':
        gui.button_click(ButtonLocations.JOIN_RED_COALITION)
    gui.button_click(ButtonLocations.JOIN_SERVER)
    time.sleep(20)

    # Select slot and confirm
    gui.multiplayer_slot_click(slot_index)
    time.sleep(20)

    gui.button_click(ButtonLocations.BRIEFING_BUTTON)
    time.sleep(20)

    gui.button_click(ButtonLocations.FLY_BUTTON)
    logger.info("Successfully joined the multiplayer session.")

@click.command()
@click.option(
    '--config', '-c',
    type=click.Path(exists=True),
    help='Path to configuration file'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose logging'
)
@click.option(
    '--debug', '-d',
    is_flag=True,
    help='Enable debug logging'
)
@click.version_option(version='0.1.0', prog_name='DCS Pylote')
def main(config: Optional[str], verbose: bool, debug: bool) -> None:
    """
    DCS Pylote - Bridge DCS World simulation data with virtual joystick controller.
    
    This application reads DCS-BIOS data and translates it into vJoy inputs,
    enabling custom flight simulation control setups.
    """
        
    # Print banner
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔══════════════════════════════════════╗")
    print("║              DCS Pylote              ║")
    print("║   DCS-BIOS to vJoy Bridge v0.1.0    ║")
    print("╚══════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

    dcs_client, gui = start_dcs_client()
    join_multiplayer_session(gui)

    # Main application loop
    try:
        while True:
            time.sleep(0.5)  # Placeholder for actual processing interval
    except KeyboardInterrupt:
        logger.info("Shutting down DCS Pylote...")
        gui.quit_dcs()
        time.sleep(15)  # Give DCS some time to close gracefully
        dcs_client.terminate()
        sys.exit(0) 

if __name__ == "__main__":
    main()
