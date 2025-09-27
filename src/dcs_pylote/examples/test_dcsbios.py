"""
DCS-BIOS test for MiG-21 PRMG channel using correct multicast configuration.

This script connects to DCS-BIOS multicast stream and looks for PRMG_CHAN control.
"""

import socket
import struct
import time
import sys

try:
    from dcs_bios_connector.control_parser import ControlParser
    from pyee import EventEmitter
    print("✓ DCS-BIOS components imported successfully")
except ImportError as e:
    print(f"✗ Failed to import DCS-BIOS components: {e}")
    sys.exit(1)


def test_mig21_prmg_chan():
    """Test MiG-21 PRMG channel control via DCS-BIOS multicast."""
    print("DCS Pylote - MiG-21 PRMG Channel Test")
    print("====================================")
    print("Monitoring MiG-21 PRMG_CHAN via DCS-BIOS multicast")
    print("Change the PRMG channel in your MiG-21 to see updates")
    print()
    
    prmg_chan_value = None
    data_received = False
    total_controls = 0
    
    def on_control_update(value, control=None, output=None):
        """Handle PRMG_CHAN updates from DCS-BIOS.
        
        DCS-BIOS emits: emitter.emit(identifier, value, control, output)
        """
        nonlocal prmg_chan_value, data_received, total_controls
        total_controls += 1
        
        # Store the PRMG channel value
        prmg_chan_value = value
        data_received = True
        print(f"[{time.strftime('%H:%M:%S')}] PRMG Channel: {value}")
        
    
    try:
        # Create event emitter and control parser
        emitter = EventEmitter()
        parser = ControlParser(emitter)
        

        # DCS-BIOS emits events with control identifier as event name
        # Listen specifically for PRMG_CHAN events
        emitter.on('PRMG_CHAN', on_control_update)
        print("✓ Registered listener for 'PRMG_CHAN' events")
        
        print("✓ DCS-BIOS control parser initialized")
        
        # Create multicast UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)
        
        # Enable address reuse (required for multicast)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to port 5010
        sock.bind(('', 5010))
        print("✓ Socket bound to port 5010")
        
        # Join multicast group using the multicast address itself as interface
        multicast_group = socket.inet_aton('239.255.50.10')
        local_interface = socket.inet_aton('239.255.50.10')  # Use multicast addr as interface
        mreq = struct.pack('4s4s', multicast_group, local_interface)
        
        try:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            print("✓ Joined multicast group successfully")
        except OSError as e:
            print(f"✗ Failed to join multicast group: {e}")
            raise
        
        print("\n--- Monitoring MiG-21 PRMG Channel ---")
        print("Parsing DCS-BIOS data for PRMG_CHAN control...")
        print("Monitoring for 15 seconds...")
        print("-" * 50)
        
        packet_count = 0
        start_time = time.time()
        last_status_time = start_time
        
        while (time.time() - start_time) < 15:
            try:
                # Receive multicast data
                data, addr = sock.recvfrom(4096)
                packet_count += 1
                
                # Parse DCS-BIOS message
                try:
                    parser.handle_incoming_dcs_bios_message(data)
                except Exception as parse_error:
                    if packet_count <= 3:  # Only show first few parse errors
                        print(f"Parse error: {parse_error}")
                
                # Status update every 5 seconds
                current_time = time.time()
                if current_time - last_status_time >= 5:
                    elapsed = int(current_time - start_time)
                    print(f"[{time.strftime('%H:%M:%S')}] Status: {packet_count} packets, {total_controls} control events received")
                    last_status_time = current_time
                
            except socket.timeout:
                # No data received in timeout period
                pass
            except KeyboardInterrupt:
                print("\n⚠ Test interrupted by user")
                break
            except Exception as e:
                print(f"Error receiving data: {e}")
                break
        
        print("-" * 50)
        print(f"Results: {packet_count} packets, {total_controls} control events received")
        
        if data_received:
            print(f"✓ SUCCESS: PRMG Channel value = {prmg_chan_value}")
            print("DCS-BIOS is working correctly with MiG-21 PRMG channel!")
        elif packet_count > 0:
            print("⚠ DCS-BIOS packets received but no PRMG_CHAN events")
            print("This might mean:")
            print("  - MiG-21 is not the active aircraft")
            print("  - MiG-21 PRMG system is not active")
            print("  - Aircraft state hasn't changed (controls only emit on change)")
            print("  - Try changing the PRMG channel knob in the cockpit")
        else:
            print("⚠ No DCS-BIOS data received (unexpected)")
        
        sock.close()
        return data_received
        
    except Exception as e:
        print(f"✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run the MiG-21 PRMG channel test."""
    success = test_mig21_prmg_chan()
    
    if success:
        print("\n✓ DCS-BIOS PRMG channel detected successfully!")
    else:
        print("\n⚠ No PRMG channel data detected - see troubleshooting above")


if __name__ == "__main__":
    main()
