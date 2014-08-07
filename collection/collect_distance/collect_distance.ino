/*
Freakduino Chibi-9000 using a DHT11 temperature sensor 
and broadcasting the latest temperature reading. 
It sends only the temperature.
*/

#include <chibi.h> 

// this constant won't change.  It's the pin number
// of the sensor's output:
const int pingPin = 7;

int sum = 0;
int checkTimes = 10;

/**************************************************************************/
// Initialize
/**************************************************************************/
void setup()
{  
  // Initialize the chibi command line and set the speed to 57600 bps
  chibiCmdInit(57600);
  
  // Initialize the chibi wireless stack
  chibiInit();
}

/**************************************************************************/
// Loop
/**************************************************************************/
void loop()
{
  // establish variables for duration of the ping, 
  // and the distance result in inches and centimeters:
  long duration, inches, cm;

  // read sensor data and send average data
  sum = 0;
  for (int i=0; i<checkTimes; i++){
    delay(100);
    // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
    // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
    pinMode(pingPin, OUTPUT);
    digitalWrite(pingPin, LOW);
    delayMicroseconds(2);
    digitalWrite(pingPin, HIGH);
    delayMicroseconds(5);
    digitalWrite(pingPin, LOW);
  
    // The same pin is used to read the signal from the PING))): a HIGH
    // pulse whose duration is the time (in microseconds) from the sending
    // of the ping to the reception of its echo off of an object.
    pinMode(pingPin, INPUT);
    duration = pulseIn(pingPin, HIGH);
  
    // convert the time into a distance
    inches = microsecondsToInches(duration);
    cm = microsecondsToCentimeters(duration);
    
    Serial.print(i);
    Serial.print(": ");
    Serial.print(inches, 1);
    Serial.print("in, ");
    Serial.print(cm, 1);
    Serial.print("cm");
    Serial.println();
    
    sum += cm;
  }
  float average = sum/(float)checkTimes;
  Serial.print("Average: ");
  Serial.println(average, 1);
  Serial.println();
  
//Send Data
//  uint8_t *p = (uint8_t*)&average;
//  chibiTx(42, p, sizeof(p));
}

long microsecondsToInches(long microseconds)
{
  // According to Parallax's datasheet for the PING))), there are
  // 73.746 microseconds per inch (i.e. sound travels at 1130 feet per
  // second).  This gives the distance travelled by the ping, outbound
  // and return, so we divide by 2 to get the distance of the obstacle.
  // See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds)
{
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}
