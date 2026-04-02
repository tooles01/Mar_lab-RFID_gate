"""
list_RFID_readers.py


Detects and displays all Sycreader RFID devices connected to a Linux system.

Gets info for all devices from /proc/bus/input/devices.
Checks if any are a keyboard, then if any are a Sycreader RFID.
Prints list of all Sycreader RFIDs.

It parses the /proc/bus/input/devices file to extract keyboard hardware information
including device names, handler paths, and physical connection ports.
The script requires root privileges to access system device information and
displays a formatted list of all detected keyboards with their connection details.


(based on list_keyboard_devices.py)

"""

import re


def get_keyboard_devices():
    """Find all keyboard devices and their connection ports."""

    devices = []

    # Check /proc/bus/input/devices for keyboard info
    try:
        # Get info for all input devices
        with open("/proc/bus/input/devices", "r") as f:
            content = f.read()

        device_blocks = content.split("\n\n")  # Split that into "device blocks"

        # For each input device, check if it's a keyboard
        for block in device_blocks:
            if "keyboard" in block.lower() or "kbd" in block.lower():

                # Extract device name
                name_match = re.search(r'N: Name="([^"]+)"', block)
                name = name_match.group(1) if name_match else "Unknown"

                # If it's a Sycreader RFID, add it to our device list
                if "Sycreader RFID" in name:

                    # Extract physical port
                    phys_match = re.search(r"P: Phys=(.+)", block)
                    phys = phys_match.group(1) if phys_match else "Unknown"

                    devices.append({"name": name, "physical_port": phys})

    except PermissionError:
        print("Error: This script requires root privileges.")
        return []
    except FileNotFoundError:
        print("Error: /proc/bus/input/devices not found.")
        return []

    return devices


def main():

    print("Keyboard Devices on Linux")
    print("=" * 60)

    keyboards = get_keyboard_devices()

    if not keyboards:
        print("No keyboard devices found.")
        return

    for i, kbd in enumerate(keyboards, 1):
        print(f"\nKeyboard {i}:")
        print(f" Name: {kbd['name']}")
        print(f" Port: {kbd['physical_port']}")


if __name__ == "__main__":
    main()
