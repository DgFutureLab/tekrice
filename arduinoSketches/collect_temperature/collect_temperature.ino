/*
Freakduino Chibi-9000 using a DHT11 temperature sensor 
and broadcasting the latest temperature reading. 
It sends only the temperature.
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

  // Print the DHT Data
  Serial.print(DHT.humidity, 1);
  Serial.print(",\t");
  Serial.println(DHT.temperature, 1);

  // Transfer the temperature to a buffer
  byte temperature_buffer[10]; 

  //AVR libc function to convert from double to char* , sprintf doesn't work
  dtostrf(DHT.temperature,2,2, (char *)temperature_buffer); 
  
  // Send the data to other Chibis
  chibiTx(42, temperature_buffer, sizeof(temperature_buffer));
  
  //Wait one second until we read and send more temperature data
  delay(1000);
}
