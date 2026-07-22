/*
 * door_script_v01.ino
 * 
 * Serial-Controlled Stepper Door Opener
 *
 * Controls a stepper motor via serial commands to open and close a door
 * (rotates the motor 90 degrees in either direction)
 * 
 * Turns motor off when not in use.
 * 
 * To use:
 *  Open the Serial Monitor at 9600 baud.
 *  Send command:
 *    "open"  -> Rotates motor +90 degrees (opens door)
 *    "close" -> Rotates motor -90 degrees (closes door)
 *
 * Hardware:
 *  28BYJ-48 stepper + ULN2003 driver (pins 8, 10, 9, 11)
 *
 *
 * ST 7/14/2026
 */

 
#include <AccelStepper.h>

#define MotorInterfaceType 4
AccelStepper stepper(MotorInterfaceType, 8, 10, 9, 11);

const int STEPS_PER_REV = 2048;
const int STEPS_PER_90_DEG = STEPS_PER_REV / 4;
String previous_command = "";

// Define to track what the motor is supposed to be doing
enum StepperMode {
  MODE_STOPPED,
  MODE_OPEN,
  MODE_CLOSE
};
StepperMode currentMode = MODE_STOPPED;

void setup() {
  Serial.begin(9600);
  Serial.println("~~~~~~~Starting~~~~~~~~~");

  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(200);
  stepper.setSpeed(200);
}

void loop() {
  if (Serial.available()) {
    String inString = Serial.readString();
    inString.trim();
    inString.toLowerCase(); // make it case-insensitive

    //if (inString != previous_command) {
      if (inString == "open") {
        Serial.println("--> Opening door");
        stepper.move(STEPS_PER_90_DEG);
        previous_command = "open";
        currentMode = MODE_OPEN;
      }
      else if (inString == "close") {
        Serial.println("--> Closing door");
        stepper.move(-STEPS_PER_90_DEG);
        //stepper.moveTo(0);
        previous_command = "close";
        currentMode = MODE_OPEN;
      }
      else {
        Serial.println("Unknown command received");
      }
    //}
    //else {
    //  Serial.println("Cannot send the same command twice in a row");
    //}
  }

  // Update the motor based on the current mode
  switch (currentMode) {
    case MODE_OPEN:
      if (stepper.distanceToGo() != 0) {
        stepper.run();
      }
      else {
        Serial.println("Reached destination");
        stepper.stop();
        stepper.disableOutputs();
        currentMode = MODE_STOPPED;
      }
    case MODE_STOPPED:
      default:
      break;
  }
}
