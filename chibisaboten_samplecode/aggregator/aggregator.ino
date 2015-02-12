/* 
  Test code for the arduino aggregator note wwhich acts as the central data collection device
  and then forwards the received data to the serial port for later upload to the Internet
  
  Written by Halfdan Rump for Future Lab. Based on code written by Christopher Wang aka Akiba.
*/

#include <chibi.h>
#include <config.h>

void setup()
{
  Serial.begin(57600);
  chibiInit();
  chibiSetShortAddr(AGGREGATOR_SHORT_ADDRESS);
}

void loop()
{ 
  if (chibiDataRcvd() == true){ 
    int rssi = chibiGetRSSI();
    int src_addr = chibiGetSrcAddr();
    
    byte buf[TX_LENGTH];  // this is where we store the received data
    int len = chibiGetData(buf);

    
    if (len == 0) {
      return;
    } else{
      printBufferToSerial(src_addr, buf);
    }
  }
}

void printBufferAsAscii(byte *buf){
  for(int i=0; i<=3; i++){
    Serial.println(buf[i]);
    Serial.print(" ");
  }
  Serial.println("");
}

void printBufferToSerial(int src_addr, byte *buf){
  Serial.print("^");
  Serial.print(src_addr);
  Serial.print("@");
  Serial.println((char*)buf);
}
