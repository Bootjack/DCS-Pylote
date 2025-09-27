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
    
    # Check if vJoy driver is enabled
    if not pyvjoy.vJoyEnabled():
        print("✗ vJoy driver is not enabled")
        return False
    print("✓ vJoy driver is enabled")
    
    device_id = 1
    
    # Check device status
    status = pyvjoy.VjdStat(device_id)
    if status != pyvjoy.VJD_STAT_FREE:
        print(f"✗ vJoy device {device_id} is not available (status: {status})")
        return False
    print(f"✓ vJoy device {device_id} is available")
    
    try:
        # Initialize device
        device = pyvjoy.VJoyDevice(device_id)
        print(f"✓ vJoy device {device_id} initialized")
        
        # Reset device
        device.reset()
        print("✓ Device reset")
        
        # Test Z-axis (throttle)
        print("\n--- Testing Z-axis for Throttle ---")
        z_axis = pyvjoy.HID_USAGE.HID_USAGE_Z
        
        # Test throttle at 0% (idle)
        device.set_axis(z_axis, 0)
        print("✓ Throttle set to 0% (idle)")
        time.sleep(1)
        
        # Test throttle at 50% (mid-power)
        device.set_axis(z_axis, 16383)
        print("✓ Throttle set to 50% (mid-power)")
        time.sleep(1)
        
        # Test throttle at 100% (full power)
        device.set_axis(z_axis, 32767)
        print("✓ Throttle set to 100% (full power)")
        time.sleep(1)
        
        # Return to idle
        device.set_axis(z_axis, 0)
        print("✓ Throttle returned to 0% (idle)")
        
        print("\n✓ Z-axis throttle test completed successfully!")
        print("The throttle axis is ready for DCS integration.")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing Z-axis: {e}")
        return False


def main():
    """Run the throttle axis test."""
    success = test_throttle_axis()
    
    if not success:
        print("\n✗ Throttle test failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
