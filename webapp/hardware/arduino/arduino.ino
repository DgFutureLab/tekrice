const int buttonPin = 2;

int buttonState = 0;
int counter = 0;
boolean pressed = false;
void setup(){
   Serial.begin(9600);
}

void loop(){
    Serial.println(analogRead(buttonPin));
    delay(100);
}
