#include <config.h>
#include <utilsawesome.h>



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

//struct Reading{
//	String name;
//	double value;
//	String timestamp;
//};
//int length = 200;
//
//void addToTXbuf(byte *TXbuf, struct Reading *reading){
//  
//  byte buf[10];
//  String value = String(dtostrf(reading->value, 2, 2, (char *)buf));
//  
//  String msg = (char *)TXbuf;
//  msg += reading->name + ':' + value + ':' + reading->timestamp + ';';
//  msg.getBytes(TXbuf, length);
//  
//}

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
  Serial.println(HUMHUM);
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
//  Serial.print(DHT.humidity, 1);
//  Serial.print(",\t");
//  Serial.println(DHT.temperature, 1);
  byte TXbuf[TX_LENGTH];
  memset(TXbuf, 0, TX_LENGTH);
  
  
  String time = "now";
  Reading temp = {"temperature", DHT.temperature, time};
  addToTXbuf(TXbuf, &temp);
  Reading hum = {"humidity", DHT.humidity, time};
  addToTXbuf(TXbuf, &hum);
  chibiTx(42, TXbuf, TX_LENGTH);
  Serial.println((char*) TXbuf);
    
  
//  byte temperature_buffer[10];
//  byte humidity_buffer[10];
//  String temperature = String(dtostrf(DHT.temperature,2,2, (char *)temperature_buffer));
//  String humidity = String(dtostrf(DHT.humidity,2,2, (char *)humidity_buffer));
//
//  String msg;
//  msg = temperature + ";" + humidity;
//  
//  msg.getBytes(TXbuf, length);
//  chibiTx(42, TXbuf, length);
//  Serial.println(msg);



//  // Transfer the temperature to a buffer
//  byte temperature_buffer[10]; 

  //AVR libc function to convert from double to char* , sprintf doesn't work
//  dtostrf(DHT.temperature,2,2, (char *)temperature_buffer); 
  
//  byte humidity_buffer[10];
  
  
//  dtostrf(DHT.temperature,2,2, (char *)temperature_buffer); 
  // Send the data to other Chibis
//  chibiTx(42, temperature_buffer, sizeof(temperature_buffer));
  
  //Wait one second until we read and send more temperature data
  delay(1000);
}
