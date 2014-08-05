

/* 
  Basic transmitting node sending a message out to an aggregator node
  
  Written by Halfdan Rump for Future Lab. Based on code written by Christopher Wang aka Akiba.
*/

#include <chibi.h>
#include <config.h>

// Define send interval in milliseconds
#define SEND_INTERVAL 1000

// Define short address of this node. In future updates an address will be asigned to the device 
// automatically based on availability.
#define DEVICE_SHORT_ADDRESS 1


byte msg[] = "exec";

void setup()
{
  Serial.begin(57600);
  chibiInit();
  chibiSetShortAddr(DEVICE_SHORT_ADDRESS);
}

void loop()
{ 
  // We're going to add 1 to the message length to handle the terminating null 
  // character for a string '/0'.
  chibiTx(AGGREGATOR_SHORT_ADDRESS, msg, 5);

  // delay between transmission
  delay(SEND_INTERVAL);
//  Serial.print("Sent message ");
//  Serial.println((char *)msg);
}
