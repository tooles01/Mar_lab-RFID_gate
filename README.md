# README

## RFID Reader Detection Utilities

Tools for detecting and identifying Sycreader RFID readers connected to a Linux system, including their physical USB port locations.

---

## Files

| File | Description |
|------|-------------|
| `list_RFID_readers.py` | Scans connected input devices and returns info on all detected Sycreader RFID readers |
| `config.py` | Maps raw USB port identifiers to human-readable labels |

---

## Requirements

- Linux (reads from `/proc/bus/input/devices`)
- Python 3
- [`evdev`](https://python-evdev.readthedocs.io/en/latest/)

```bash
pip install evdev
```

> **Note:** Root privileges are required to read input device information.

---

## Usage

### Run directly
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

### Import as a module
```python
from list_RFID_readers import get_RFID_devices

devices = get_RFID_devices()
for d in devices:
    print(d['physical_port'], d['dev_path'])
```

Each device is returned as a dict with four keys:

| Key | Example Value |
|-----------|--------------------------------------|
| `dev_path` | `/dev/input/event3` |
| `dev_name` | `Sycreader RFID Technology` |
| `physical_port` | `usb-0000:05:00.4-1.1.3/input0` |
| `port_name` | `front USB port, Hub position #5` |

---

## Configuration

Edit `config.py` to add or update USB port labels for your specific machine. Each entry maps a raw USB port string to a descriptive name:

```python
known_ports.append({"usb-0000:05:00.4-1.1.3/input0": "front USB port, Hub position #5"})
```

To find the raw USB port string for a connected device, run `list_RFID_readers.py` and check the `physical_port` field. If a port is not found in `config.py`, `port_name` will be reported as `"unknown"`.