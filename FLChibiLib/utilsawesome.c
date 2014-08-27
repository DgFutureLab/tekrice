#include "utilsawesome.h"

uint8_t chibiGetUnusedAddress(uint8_t scan_length){
	/*
	Select an address at random and listen if any messages are being sent to this address. If not return that address.
	*/
	return 0;

}

void addToTXbuf(uint8_t *TXbuf, struct Reading *reading){
  uint8_t buf[10];
  String value = String(dtostrf(reading->value, 2, 2, (char *)buf));
  
  String msg = (char *)TXbuf;
  msg += reading->name + ':' + value + ':' + reading->timestamp + ';';
  msg.getBytes(TXbuf, length);
}