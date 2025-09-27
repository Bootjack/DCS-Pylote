"""
Simple vJoy Z-axis test for throttle input.

This script establishes and tests a Z-axis on vJoy device 1 for throttle control.
"""

import time
import sys

try:
    import pyvjoy
    print("✓ pyvjoy imported successfully")
except ImportError as e:
    print(f"✗ Failed to import pyvjoy: {e}")
    sys.exit(1)


def test_throttle_axis():
    """Test Z-axis for throttle control."""
    print("DCS Pylote - Throttle Z-axis Test")
    print("=================================")
    
    device_id = 1
    
    try:
        # Initialize device (this will check if vJoy is enabled)
        device = pyvjoy.VJoyDevice(device_id)
        print(f"✓ vJoy device {device_id} initialized")
        print("✓ vJoy driver is enabled and working")
        
        # Reset device
        device.reset()
        print("✓ Device reset")
        
        # Test Z-axis (throttle) with simple movement
        print("\n--- Testing Z-axis for Throttle ---")
        print("Go to DCS Input Settings to see the vJoy device!")
        print()
        
        z_axis = pyvjoy.HID_USAGE_Z
        
        # Test sequence: 0% -> 50% -> 100% -> 0%
        print("✓ Setting throttle to 0% (idle)")
        device.set_axis(z_axis, 0)
        time.sleep(1)
        
        print("✓ Setting throttle to 50%")
        device.set_axis(z_axis, 16383)  # 50% of 32767
        time.sleep(1)
        
        print("✓ Setting throttle to 100% (full)")
        device.set_axis(z_axis, 32767)  # Full throttle
        time.sleep(1)
        
        print("✓ Returning throttle to 0% (idle)")
        device.set_axis(z_axis, 0)
        
        print("\n✓ Z-axis throttle test completed!")
        print("Check DCS Input Settings -> Axis Commands for 'vJoy Device' Z-axis")
        
        return True
        
    except pyvjoy.vJoyNotEnabledException:
        print("✗ vJoy driver is not enabled!")
        print("\nTo fix this:")
        print("1. Download vJoy from: http://vjoystick.sourceforge.net/")
        print("2. Install vJoy with default settings")
        print("3. Run 'Configure vJoy' from Start Menu")
        print("4. Enable Device 1 with at least Z-axis")
        print("5. Click 'Apply' and restart this test")
        return False
    except Exception as e:
        print(f"✗ Error testing vJoy: {e}")
        print(f"Error type: {type(e).__name__}")
        
        if "vJoy" in str(e):
            print("\nThis looks like a vJoy configuration issue.")
            print("Make sure vJoy is properly installed and configured.")
        
        return False


def main():
    """Run the throttle axis test."""
    success = test_throttle_axis()
    
    if not success:
        print("\n✗ Throttle test failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
