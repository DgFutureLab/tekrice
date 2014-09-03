#include <config.h>
#include <utilsawesome.h>

/*
Freakduino Chibi-9000

Collects data from different sensors and sends it to 
the aggregator as defined in "config.h"
*/

#include <chibi.h>
#include "DHT.h"

#define DHTTYPE DHT11   // Type of DHT sensor, in our case we are using DHT11
#define DHT11_PIN A0    // Pin where the DHT11 is connected

dht DHT;

/**************************************************************************/
// Initialize
/**************************************************************************/
void setup()
{
  // Initialize the chibi command line and set the speed to 57600 bps
  chibiCmdInit(57600);
  
  // Initialize the chibi wireless stack
  chibiInit();

  Serial.println("Type,\tstatus,\tHumidity (%),\tTemperature (C)");
}

/**************************************************************************/
// Loop
/**************************************************************************/
void loop()
{
  // Read latest temperature data from DHT11
  int chk = DHT.read11(DHT11_PIN);
  switch (chk)
  {
    case DHTLIB_OK:  
		Serial.print("OK,\t"); 
		break;
    case DHTLIB_ERROR_CHECKSUM: 
		Serial.print("Checksum error,\t"); 
		break;
    case DHTLIB_ERROR_TIMEOUT: 
		Serial.print("Time out error,\t"); 
		break;
    default: 
		Serial.print("Unknown error,\t"); 
		break;
  }

  byte tx_buf[TX_LENGTH];
  memset(tx_buf, 0, TX_LENGTH);
  long duration, inches, cm;
  
  // Read sonar distance
  float distance = sonar_measure_distance();
  if (distance > 0) {
    Reading dist = {"distance", distance, millis()};
    add_to_tx_buf((char*)tx_buf, &dist);
  }

  // Read temperature
  Reading temp = {"temperature", DHT.temperature, millis()};
  add_to_tx_buf((char*)tx_buf, &temp);
  
  // Read humidity
  Reading hum = {"humidity", DHT.humidity, millis()};
  add_to_tx_buf((char*)tx_buf, &hum);
  
  //Send data stored on "tx_buf" to collector
  chibiTx(42, tx_buf, TX_LENGTH);

  // Debug print
  Serial.println((char*) tx_buf);

  free(tx_buf);
  //Wait
  delay(10000);
}

float sonar_measure_distance(){
  int checkTimes = 10;
  long duration, cm;

  // read sensor data and send average data
  int sum = 0;
  for (int i=0; i<checkTimes; i++){
    delay(100);
    // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
    // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
    pinMode(SONAR_PIN, OUTPUT);
    digitalWrite(SONAR_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(SONAR_PIN, HIGH);
    delayMicroseconds(5);
    digitalWrite(SONAR_PIN, LOW);
  
    // The same pin is used to read the signal from the PING))): a HIGH
    // pulse whose duration is the time (in microseconds) from the sending
    // of the ping to the reception of its echo off of an object.
    pinMode(SONAR_PIN, INPUT);
    duration = pulseIn(SONAR_PIN, HIGH);
  
    // convert the time into a distance
    cm = microsecondsToCentimeters(duration);
    if(VERBOSE == 1){ 
      Serial.print(i);
      Serial.print(cm, 1);
      Serial.print("cm");
      Serial.println();
    }
    
    sum += cm;
  }
  float average = sum/(float)checkTimes;
  if(VERBOSE == 1){
    Serial.print("Average: ");
    Serial.println(average, 1);
    Serial.println();
  }
  return average;
}

long microsecondsToCentimeters(long microseconds)
{
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}


