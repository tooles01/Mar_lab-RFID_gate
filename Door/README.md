# Door mechanism

# Quick use
### Hardware
Connect the motor pins to the Arduino
| Motor | Arduino |
| - | - |
| -, + | GND, 5V |
| IN1, IN2, IN3, IN4 | 8, 9, 10, 11 |

### Software
- Open the Arduino Serial Monitor (9600 baud)
- Send command:
    - "open" --> Opens door
    - "close" --> Closes door

<br>

# Setup
## To upload Arduino script
**Motor 5V/GND should NOT be connected to Arduino pins while uploading the sketch!!!!!**

- Install the Arduino IDE (version 1.8.9)
- Connect the Arduino to the computer
- In the IDE, select:
    - Tools --> Board --> Board type you are using
    - Port --> Port the board is connected to
    - Sketch --> Upload

<br>

## Troubleshooting/Possible error messages:

### When uploading sketch:
### AccelStepper.h: No such file or directory:
**--> AccelStepper library is not installed**
- Sketch --> Include Library --> Manage Libraries
- Type "accelstepper" into th search bar
- Click on the "AccelStepper" library (should be the first one)
- Click "Install"

### avrdude: ser_open(): can't open device "/dev/ttyACM0: Permission denied
**--> Arduino is bugging out**
- on the mega, double press the reset button

**--> Linux user account does not have read/write access to the serial port --> Add user to the `dialout` group**
- Open a terminal
- `sudo usermod -aG dialout acmeneuro`
- Restart computer

<br>

### When opening the serial monitor
### Error opening serial port 'dev/tty/ACM0'
**--> Linux user account does not have read/write access to the serial port --> Add user to the `dialout` group**
- Open a terminal
- `sudo usermod -aG dialout acmeneuro`
- Restart computer

<br>

---
# CAD

CAD files can be found [here](../CAD/Door)

![image](../images/door.png)