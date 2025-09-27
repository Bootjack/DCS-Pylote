"""
Simple test runner for DCS Pylote examples.

This script allows you to easily test individual components.
"""

import sys
import argparse
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from examples.test_vjoy import main as test_vjoy_main
from examples.test_dcsbios import main as test_dcsbios_main


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(
        description="Test runner for DCS Pylote components",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py vjoy       # Test vJoy functionality
  python test_runner.py dcsbios    # Test DCS-BIOS functionality  
  python test_runner.py both       # Test both components
        """
    )
    
    parser.add_argument(
        'component',
        choices=['vjoy', 'dcsbios', 'both'],
        help='Which component to test'
    )
    
    args = parser.parse_args()
    
    print("DCS Pylote Component Tester")
    print("===========================")
    
    if args.component in ['vjoy', 'both']:
        try:
            test_vjoy_main()
        except Exception as e:
            print(f"\n✗ vJoy test failed with error: {e}")
        
        if args.component == 'both':
            print("\n" + "="*50 + "\n")
    
    if args.component in ['dcsbios', 'both']:
        try:
            test_dcsbios_main()
        except Exception as e:
            print(f"\n✗ DCS-BIOS test failed with error: {e}")
    
    print("\nTesting completed!")


if __name__ == "__main__":
    main()
