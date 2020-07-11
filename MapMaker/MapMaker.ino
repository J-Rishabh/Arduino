#include <Servo.h> //Servo library used to control motor

#define trigPin 10 //pin definitions for ultrasonic
#define echoPin 11

Servo myServo; //initializing the servo as myservo

float time_us = 0; // time tracked by ultrasonic sensor in micro-seconds
float distance; //distance variable
int degreeofrot = 180; //range of motion of the servo (180 is max)
float average = 0; //setting average as 0 - used with iterations to calculate a more accurate distance based on # of iterations
int iterations = 10;

void setup() {
  pinMode(trigPin, OUTPUT); //output pin for ultrasonic
  pinMode(echoPin, INPUT); //input pin for ultrasonic
  Serial.begin(9600); //open and begin writing to this channel
  myServo.attach(12, 880, 2120); //digital pin 12 defined for the servo
}
void loop() {
  //generating and writing data in a csv format into the serial monitor (basically cmd)
  //adding headers defining the data - this data represents polar coordinates (angle (theta) and distance (r))
  Serial.println("Angle,Distance");
  //for each rotation of the servo, record the distance it measures
  for (int i = 1; i < degreeofrot; i++) {
    myServo.write(i); //writes to the servo the angle that it should turn to
    delay(100); // waits 100ms for the servo to reach the position
    //averaging distance for better readings (10 times based on # of iterations defined)
    average = 0;
    for (int i = 0; i < iterations; i++) {
      average = average + read_ultrasonic();
      delay(30);
    }
    delay(200);
    distance = average / iterations;
    //writing data
    Serial.println((String) i + "," + distance);
    delay(300);
  }
  delay(1000);
  //basically unwinding the servo so the wires don't get super tangled (reverse)
  for (int i = 1; i < degreeofrot; i++) {
    myServo.write(degreeofrot - i);
    delay(100);
  }
  //since there's no way to "kill" the process as soon as it ends we just have a long wait - more than enough for me to unplug the arduino
  delay(1000000);
}
//just calculating the distance
float read_ultrasonic()
{
  digitalWrite (trigPin, HIGH);
  delayMicroseconds (10);
  digitalWrite (trigPin, LOW);
  time_us = pulseIn (echoPin, HIGH);
  return (time_us * 0.0344) / 2; // distance = (time in us * 0.034 cm/us)/2  (0.0344 to get a more accurate distance given the conditions (temps))
}
