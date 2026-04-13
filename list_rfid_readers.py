"""
list_RFID_readers.py

Scans all connected input devices and identifies Sycreader RFID readers.
Each detected device is stored as a dict containing:
    dev_path  - the /dev/input/eventX path        (e.g. /dev/input/event3)
    dev_name  - the device name                   (e.g. Sycreader RFID Technology)
    usb_port  - the physical USB port identifier  (e.g. usb-0000:05:00.4-1.1.3/input0)
    port_name - the human-readable port label     (e.g. "front USB port, Hub position #1")

USB port names are loaded from config.py (known_ports).

Functions:
    get_usb_port(event_path)  - looks up USB port from /proc/bus/input/devices
    get_port_name(usb_port)   - matches USB port to a human-readable name
    get_RFID_devices()        - returns a list of dicts for all found RFID readers

Dependencies:
    evdev, re, config.py

Usage:
    python3 get_RFID_devices.py       (run directly to print detected devices)
    from get_RFID_devices import get_RFID_devices   (import into other scripts)


4/13/2026
"""

import re 
from evdev import InputDevice, list_devices
from config import known_ports


def get_usb_port(event_path):
    """Look up the USB physical port for a given /dev/input/eventX path."""
    
    event_name = event_path.split('/')[-1]  # Ex: "event3"
    usb_port = []

    # Check /proc/bus/input/devices for keyboard info
    try:
        # Get info for all input devices
        with open('/proc/bus/input/devices', 'r') as f:
            content = f.read()
        
        device_blocks = content.split('\n\n')   # Split that into "device blocks"
        for block in device_blocks:
            # Check if this block contains our event device
            if event_name in block:
                # Extract physical port
                phys_match = re.search(r'P: Phys=(.+)', block)
                if phys_match:
                    usb_port = phys_match.group(1).strip()  # 'usb-0000:05:00.4-1.1.2/input0'
    
    except PermissionError as err:
        print(f"Error: This script requires root privileges: {err}")
        usb_port = "Unknown"
    except FileNotFoundError as err:
        print(f"Error: /proc/bus/input/devices not found: {err}")
        usb_port = "Unknown"
    
    return usb_port     # Ex: 'usb-0000:05:00.4-1.1.2/input0'

def get_port_name(usb_port):
    """Get the name of this usb port from the dictionary in config.py"""
    
    for port_dict in known_ports:
        if usb_port in port_dict:
            port_name = port_dict[usb_port]
            #print('yay found it')
            break
        else:
            port_name = "unknown"
    
    return port_name    # Ex: 'back USB port, Hub position #7'

def get_RFID_devices():
    """Get Sycreaders as InputDevice"""
    
    rfid_devices = []
    for path in list_devices():
        dev = InputDevice(path)
        if "Sycreader" in dev.name or "Keyboard" in dev.name:
            usb_port = get_usb_port(dev.path)
            port_name = get_port_name(usb_port)
            rfid_devices.append({
                'dev_path': dev.path,
                'dev_name': dev.name,
                'usb_port': usb_port,
                'port_name': port_name
            })
            dev.close() # close each device after inspecting it

    return rfid_devices     # List of dicts


if __name__ == "__main__":
    rfid_devices = []
    rfid_devices = get_RFID_devices()        
    
    if rfid_devices:
        # For safety: print out the info for each rfid device we just got
        print("\nList of connected RFID readers:")
        print("=" * 60)
        for device in rfid_devices:
            print(f"  dev_path: {device.get('dev_path')}")
            print(f"  dev_name: {device.get('dev_name')}")
            print(f"  usb_port: {device.get('usb_port')}")
            print(f"  port_name: {device.get('port_name')}")
            print("=" * 60)
    else:
        print("No Sycreader RFID devices found.")