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
    
    logger.info(f"{Fore.GREEN}DCS Pylote stopped successfully{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
