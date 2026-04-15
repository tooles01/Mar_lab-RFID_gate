## RFID Reader Detection Utilities

Monitors one or more Sycreader RFID readers simultaneously and prints each scan to the terminal as it occurs.  
Each reader runs in its own thread.

---

## Requirements

- Linux (reads from `/proc/bus/input/devices`)
- Python 3
- [`evdev`](https://python-evdev.readthedocs.io/en/latest/)

***Note:*** Root privileges are required to read from `/dev/input/eventX` devices.

---

## Usage

```bash
sudo python3 read_RFID.py
```

On launch, the script will:
1. Scan for connected Sycreader RFID readers
2. Print a summary of detected readers
3. Begin monitoring all readers simultaneously
4. Print a timestamped line to the console each time an RFID tag is scanned

Press **Ctrl+C** to stop monitoring.

---

## Example Output

```
============================================================
Scanning for connected RFID readers...

Found 2 RFID reader(s):
============================================================
  dev_path:      /dev/input/event17
  dev_name:      Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader
  physical_port: usb-0000:05:00.4-1.3/input0
  port_name:     front USB port, Hub position #2
============================================================
============================================================
  dev_path:      /dev/input/event16
  dev_name:      Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader
  physical_port: usb-0000:05:00.4-1.4/input0
  port_name:     front USB port, Hub position #1
============================================================

Monitoring for keyboard events... (Ctrl+C to stop)


0621221024
[2026-04-15 16:36:35.306] | Port: front USB port, Hub position #2     | RFID Scan: 0621221024

0621221024
[2026-04-15 16:36:38.466] | Port: front USB port, Hub position #1     | RFID Scan: 0621221024
```

---

## Files

| File | Description |
|---|---|
| `read_RFID.py` | Main script — monitors devices and prints scans |
| `list_RFID_readers.py` | Module: Detects connected Sycreader RFID devices |
| `config.py` | Maps raw USB port identifiers to human-readable labels |


---

## Notes

- Each reader runs in its own thread, so multiple readers can be monitored
  simultaneously without blocking each other.
- If a reader is unplugged, its thread exits cleanly and monitoring continues
  on any remaining readers.
- USB port labels come from `config.py`. If a port is not listed there,
  `port_name` will display as `"unknown"`.

<!--
### Detect connected RFID devices
```bash
sudo python3 list_RFID_readers.py
```
Prints a list of all connected Sycreader RFID readers and their USB port locations.

**Example output:**
```
List of connected RFID readers:
============================================================
  dev_path:       /dev/input/event3
  dev_name:       Sycreader RFID Technology
  physical_port:  usb-0000:05:00.4-1.1.3/input0
  port_name:      front USB port, Hub position #5
============================================================
```

---

## Configuration

Edit `config.py` to add or update USB port labels for your specific machine. Each entry maps a raw USB port string to a descriptive name:

```python
known_ports.append({"usb-0000:05:00.4-1.1.3/input0": "front USB port, Hub position #5"})
```

To find the raw USB port string for a connected device, run `list_RFID_readers.py` and check the `physical_port` field. If a port is not found in `config.py`, `port_name` will be reported as `"unknown"`.
-->