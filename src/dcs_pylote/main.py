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

from .core.bridge import DCSVJoyBridge
from .core.config import Config
from .utils.logger import setup_logging


# Initialize colorama for Windows
init(autoreset=True)


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
    # Setup logging
    log_level = logging.DEBUG if debug else (logging.INFO if verbose else logging.WARNING)
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    # Print banner
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔══════════════════════════════════════╗")
    print("║              DCS Pylote              ║")
    print("║   DCS-BIOS to vJoy Bridge v0.1.0    ║")
    print("╚══════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")
    
    try:
        # Load configuration
        logger.info("Loading configuration...")
        app_config = Config.load(config)
        
        # Initialize the bridge
        logger.info("Initializing DCS-BIOS to vJoy bridge...")
        bridge = DCSVJoyBridge(app_config)
        
        # Start the bridge
        logger.info(f"{Fore.GREEN}Starting bridge... Press Ctrl+C to stop{Style.RESET_ALL}")
        bridge.start()
        
        # Main application loop
        try:
            while bridge.is_running():
                time.sleep(0.1)  # Small sleep to prevent excessive CPU usage
                
        except KeyboardInterrupt:
            logger.info(f"{Fore.YELLOW}Shutdown requested by user{Style.RESET_ALL}")
            
    except Exception as e:
        logger.error(f"{Fore.RED}Application error: {e}{Style.RESET_ALL}")
        if debug:
            logger.exception("Full traceback:")
        sys.exit(1)
        
    finally:
        logger.info("Shutting down bridge...")
        if 'bridge' in locals():
            bridge.stop()
        logger.info(f"{Fore.GREEN}DCS Pylote stopped successfully{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
