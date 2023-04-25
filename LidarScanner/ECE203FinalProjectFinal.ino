#include <SoftwareSerial.h>
#include "TFMini.h"
#include <Servo.h>

Servo panservo;  // create servo object to control the tilt servo
Servo tiltservo; // create servo object to control the pan servo


int pos = 0;    // variable to store the tilt servo position
int pos2 = 0;   // variable to store the pan servo position

TFMini tfmini;  // creates a tfmini object to control the lidar sensor
 
SoftwareSerial SerialTFMini(10, 11);          
 
void getTFminiData(int* distance, int* strength)
{
  static char i = 0;
  char j = 0;
  int checksum = 0;
  static int rx[9];

  if (SerialTFMini.available())
  {
    rx[i] = SerialTFMini.read();
    if (rx[0] != 0x59)
    {
      i = 0;
    }
    else if (i == 1 && rx[1] != 0x59)
    {
      i = 0;
    }
    else if (i == 8)
    {
      for (j = 0; j < 8; j++)
      {
        checksum += rx[j];
      }
      if (rx[8] == (checksum % 256))
      {
        *distance = rx[2] + rx[3] * 256;
        *strength = rx[4] + rx[5] * 256;
      }
      i = 0;
    }
    else
    {
      i++;
    }
  }
}
 

void setup()
{
  Serial.begin(115200);  //Initialize hardware serial port (serial debug port)
  panservo.attach(9);   // attaches the pan servo on pin 9 to the pan servo object
  tiltservo.attach(8); // attaches the tilt servo on pin 8 to the tilt servo object
  while (!Serial);            // wait for serial port to connect. Needed for native USB port only
  Serial.println ("Initializing...");
  SerialTFMini.begin(TFMINI_BAUDRATE);    //Initialize the data rate for the SoftwareSerial port
  tfmini.begin(&SerialTFMini);            //Initialize the TF Mini sensor
}
 
void loop()
{
  int distance = 0;
  int strength = 0;
  
    for (pos = 90; pos >= 0; pos -= 10) {
      tiltservo.write(pos); 
      delay(100);

      for (pos2 = 0; pos2 <= 180; pos2 += 10) {
          distance = 0;
          strength = 0;

          getTFminiData(&distance, &strength);
          while (!distance)
          {
            getTFminiData(&distance, &strength);
            if (distance)
            {
              Serial.print(distance);
              Serial.print("cm\t");
              Serial.print("strength: ");
              Serial.println(strength);
            }

          }

          panservo.write(pos2);
          delay(100);
    }
   
  }
  delay(100);
}