/*
Chibi Arduino using a DHT11 temperature sensor 
and broadcasting the latest temperature reading
*/

#include <chibi.h>
#include "DHT.h"

#define DHT11_PIN A0    // Pin where the DHT11 is connected
#define DHTTYPE DHT11

dht DHT;

void setup()
{  
  // Initialize the chibi command line and set the speed to 57600 bps
  chibiCmdInit(57600);
  
  // Initialize the chibi wireless stack
  chibiInit();

  Serial.println("Type,\tstatus,\tHumidity (%),\tTemperature (C)");
}

void loop()
{
  // DHT Data
  Serial.print(DHT.humidity, 1);
  Serial.print(",\t");
  Serial.println(DHT.temperature, 1);

  // Read data and transfer it to a buffer
  byte temperature_buffer[10]; 
  dtostrf(DHT.temperature,2,2,(char *)temperature_buffer);
  
  // Send the data to other Chibis
  chibiTx(42, temperature_buffer, sizeof(temperature_buffer));
  delay(1000);
}
