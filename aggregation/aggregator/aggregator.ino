


/* 
  Code for the arduino aggregator note wwhich acts as the central data collection device
  and then forwards the received data to the serial port for later upload to the Internet
  
  Written by Halfdan Rump for Future Lab. Based on code written by Christopher Wang aka Akiba.
*/

#include <chibi.h>
#include <config.h>





byte msg[] = "exec";

void setup()
{
  Serial.begin(57600);
  chibiInit();
  chibiSetShortAddr(AGGREGATOR_SHORT_ADDRESS);
}

void loop()
{ 
   // This function checks the command line to see if anything new was typed.
//  chibiCmdPoll();
  if (chibiDataRcvd() == true){ 
//    int len, rssi, src_addr;
    int rssi = chibiGetRSSI();
    int src_addr = chibiGetSrcAddr();
    
    byte buf[100];  // this is where we store the received data
    int len = chibiGetData(buf);
//    Serial.print("Received message: ");
    printBufferToSerial(src_addr, buf);
    
//    Serial.print(", from node: 0x");
//    Serial.println(src_addr);
    if (len == 0) return;
  }
}

void printBufferAsAscii(byte *buf){
  for(int i=0; i<=3; i++){
    Serial.print(buf[i]);
    Serial.print(" ");
  }
  Serial.println("");
}

void printBufferToSerial(int src_addr, byte *buf){
  Serial.print(src_addr);
  Serial.print(",");
  Serial.println((char*)buf);
}
