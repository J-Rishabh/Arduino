// code based on https://forum.arduino.cc/t/serial-input-basics-updated/382007/3


const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

      // variables to hold the parsed data
char messageFromPC[numChars] = {0};
float alt = 0.0;
float az = 0.0;
boolean running = true;
boolean newData = false;

// Include the AccelStepper library:
#include <AccelStepper.h>

// Define the AccelStepper interface type:
#define MotorInterfaceType 4

// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(MotorInterfaceType, 4, 5, 6, 7);
AccelStepper stepper2 = AccelStepper(MotorInterfaceType, 8, 9, 10, 11);

//============

void setup() {
    Serial.begin(9600);
    Serial.println("Expects 3 pieces of data - letter, alt, az");
    Serial.println("Enter data in this style <R, 12, 24.7>  ");
    // two versions
    // <R, 12, 24.7> will run the motors
    // <E> will unwind + stop
    // Set the maximum steps per second:
    stepper.setCurrentPosition(0);
    stepper.setMaxSpeed(200);
    
    // Set the maximum acceleration in steps per second^2:
    stepper.setAcceleration(25);
  
    // 2
    stepper2.setCurrentPosition(0);
    stepper2.setMaxSpeed(200);
    
    // Set the maximum acceleration in steps per second^2:
    stepper2.setAcceleration(25);
}

//============

void loop() {
    if (running) {
      recvWithStartEndMarkers();
      if (newData == true) {
          strcpy(tempChars, receivedChars);
              // this temporary copy is necessary to protect the original data
              //   because strtok() used in parseData() replaces the commas with \0
          parseData();
          showParsedData();
          newData = false;
      }
    } else {
      Serial.print("FINISH!");
    }
}

//============

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    strcpy(messageFromPC, strtokIndx); // copy it to messageFromPC
    
    if (strcmp(messageFromPC, "E") == 0) {
      unwindMotors();
    } else if (strcmp(messageFromPC, "R") == 0){
      strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
      alt = atoi(strtokIndx);     // convert this part to an integer
  
      strtokIndx = strtok(NULL, ",");
      az = atof(strtokIndx);     // convert this part to a float
      runMotors(alt, az);
    }
 
    

}

//============
void runMotors(int altitude, int azimuth) {
  //Serial.print("RNNNNNNNN");
  //Serial.println(altitude);
  //Serial.println(azimuth);
  if (stepper.distanceToGo() == 0)
        stepper.moveTo(altitude);
  if (stepper2.distanceToGo() == 0)
        stepper2.moveTo(azimuth);
  while (stepper.distanceToGo() != 0 || stepper2.distanceToGo() != 0) {
      stepper.run();
      stepper2.run();
  }
  //Serial.println(stepper.distanceToGo());
  //Serial.println(stepper2.distanceToGo());
  stepper.run();
  stepper2.run();

}

void unwindMotors() {
  // moveTo 0
  stepper.moveTo(0);
  // Run to position with set speed and acceleration:
  stepper.runToPosition();
  delay(1000);

  stepper2.moveTo(0);
  // Run to position with set speed and acceleration:
  stepper2.runToPosition();
  
  //Serial.print("OVR");
  running = false;
}
void showParsedData() {
    /*Serial.print("Message ");
    Serial.println(messageFromPC);
    Serial.print("Alt ");
    Serial.println(alt);
    Serial.print("Az ");
    Serial.println(az);*/
}
