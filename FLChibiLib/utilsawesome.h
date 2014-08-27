struct Reading{
	String name;
	double value;
	String timestamp;
};

uint8_t chibiGetUnusedAddress(uint8_t scan_length);
void addToTXbuf(uint8_t *TXbuf, struct Reading *reading);

#define HUMHUM 2