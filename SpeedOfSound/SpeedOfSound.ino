#define trigPin 10 //definitions for ultrasonic sensor's pins - trigPin sends out a ping
#define echoPin 13 //echoPin receives it

float predefdist = 50; //distance predefined as 50cm in experiment - change
float expnumber = 10; //number of iterations used to find average - can change as needed

float time_us = 0; // time tracked by ultrasonic sensor in micro-seconds
float sumsos = 0; //sum of speed of sound - used to find the average speed
float avgspeed = 0; //initializes the average speed as 0

float pcerr = 0; //initialzies the percent error as 0

void setup() {
  //setup arduino bits - sets trigpin as output and echopin as input and 9600 is speed of data exchange (9600 bits/s)
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  //defaults sumsos as 0 on each iteration - this loop runs forever technically
  sumsos = 0;
  for (int i = 0; i < expnumber; i++)
  {
    //for each iteration of the experiment it adds up all the speeds returned by the function
    sumsos = sumsos + read_ultrasonic();
  }
  //calculates the average speed
  avgspeed = sumsos / expnumber;
  //calculates the percent error
  pcerr = ((avgspeed - 343.21) / 343.21) * 100;
  //prints to the serial monitor (console equivalent) the values
  Serial.println((String)"Average speed of sound is " + avgspeed + " m/s");
  Serial.println((String)"Percent error is " + pcerr + "%");
  //pauses for 3 seconds
  delay(3000);
}

float read_ultrasonic()
{
  //turns the trigpin (output one) to high intensity sending a "pulse" for 10 microseconds and then turns it to low
  digitalWrite (trigPin, HIGH);
  delayMicroseconds (10);
  digitalWrite (trigPin, LOW);
  //calculates the time for the pulse to bounce and come back
  time_us = pulseIn (echoPin, HIGH);
  //uses a predefined distance - you can calculate the distance but you'd need to use the speed of sound and in turn you use that speed of sound value to calculate the speed of sound.......
  return (2 * (predefdist / 100)) / (time_us / 1000000); // v = d/t
}
