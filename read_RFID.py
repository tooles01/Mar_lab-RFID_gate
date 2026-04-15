#!/usr/bin/env python3
"""
read_RFID.py

RFID Reader Monitor - Detects keyboard events from Sycreader RFID devices
and prints timestamped messages with USB hub location.



based on read_RFID_test_01.py

4/14/2026
"""

import threading, struct
from datetime import datetime
from list_RFID_readers import get_RFID_devices

# Linux input event format: (time_sec, time_usec, type, code, value)
EVENT_FORMAT = "llHHI"
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

# Key code to character mapping (subset - common keys for RFID readers)
KEY_MAP = {
    2: '1', 3: '2', 4: '3', 5: '4', 6: '5',
    7: '6', 8: '7', 9: '8', 10: '9', 11: '0',
    16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't',
    21: 'y', 22: 'u', 23: 'i', 24: 'o', 25: 'p',
    30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g',
    35: 'h', 36: 'j', 37: 'k', 38: 'l',
    44: 'z', 45: 'x', 46: 'c', 47: 'v', 48: 'b',
    49: 'n', 50: 'm',
    28: 'ENTER', 57: 'SPACE', 14: 'BACKSPACE',
}

# Event type constants
EV_KEY = 1
KEY_PRESS = 1  # value=1 means key pressed, value=0 means released

# Common stop threading event
stop_event = threading.Event()


def monitor_device(device):
    """
    Monitor a single input device for key events.
    Runs in its own thread, one thread per RFID reader.
    """
    handler_path = device['dev_path']       # Ex: /dev/input/event16
    port_name = device['port_name']         # Ex: front USB port, Hub position #5
    buffer = []  # Accumulate keypresses into a full scan/string

    try:
        with open(handler_path, 'rb') as dev_file:
            while not stop_event.is_set():  # Add graceful shutdown
                # Read one input event
                raw_event = dev_file.read(EVENT_SIZE)
                if not raw_event:
                    break

                # Unpack the binary event data
                (tv_sec, tv_usec, ev_type, ev_code, ev_value) = struct.unpack(EVENT_FORMAT, raw_event)

                # Only process key-press events (not releases or repeats)
                if ev_type == EV_KEY and ev_value == KEY_PRESS:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    key_char = KEY_MAP.get(ev_code, f"[code:{ev_code}]")

                    if key_char == 'ENTER':
                        # ENTER signals end of RFID scan - print the full message
                        full_message = ''.join(buffer)
                        buffer.clear()
                        print(
                            f"\n{timestamp} | "
                            f"Location: {port_name} | "
                            f"Animal: {full_message}"
                        )
                    elif key_char not in ('BACKSPACE', 'SPACE'):
                        buffer.append(key_char) # Accumulate characters into the buffer

    except PermissionError:
        print(f"Error: No permission to read {handler_path}. Run as root.")
    except FileNotFoundError:
        print(f"Error: Device {handler_path} not found. Was it unplugged?")
    except OSError as e:
        if e.strerror == 'No such device':
            print(F"Error: did you unplug it\n")
        else:
            print(f"Error reading {handler_path}: {e}")


def main():
    
    '''Find all Sycreader RFID devices'''
    print("=" * 60)
    print("Scanning for connected RFID readers...\n")
    RFID_readers = get_RFID_devices()

    if RFID_readers:
        '''Print info about each reader'''
        print(f"Identified {len(RFID_readers)} RFID reader(s), Connected to ports:")
        for device in RFID_readers:
            print(f"  -->  {device.get('port_name')}")
        print("=" * 60)
        print("\nMonitoring for keyboard events... (Ctrl+C to stop)")
        print("\n")

        '''Start reader thread for each device'''
        threads = []
        for device in RFID_readers:
            t_rfid_read = threading.Thread(target=monitor_device,args=(device,),name=f"monitor_thread-{device['dev_path']}")
            t_rfid_read.daemon = True
            threads.append(t_rfid_read)
            t_rfid_read.start()

        '''Keep the main thread alive until Ctrl+C'''
        try:
            for t in threads:
                t.join()    # Blocks until each thread finishes (e.g, device unplugged)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user.")
    
    if not RFID_readers:
        print("No Sycreader RFID devices found. Exiting.")
        return


if __name__ == "__main__":
    main()