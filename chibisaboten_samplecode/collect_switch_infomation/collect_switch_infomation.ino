/*
Freakduino Chibi-9000 using a DHT11 temperature sensor 
and broadcasting the latest temperature reading. 
It sends only the temperature.
*/

#include <chibi.h> 

int button1Pin = 2;//D2
int button2Pin = 3;//D3
int sliderPin = A0;//A0
int length = 50;

/**************************************************************************/
// Initialize
/**************************************************************************/
void setup()
{  
  // Initialize the chibi command line and set the speed to 57600 bps
  chibiCmdInit(57600);
  
  // Initialize the chibi wireless stack
  chibiInit();
  
  //set up sensor pin mode
  pinMode(button1Pin, INPUT);
  pinMode(button2Pin, INPUT);
  pinMode(sliderPin, INPUT);
}

/**************************************************************************/
// Loop
/**************************************************************************/
void loop()
{
  // read and save sensor date
  boolean button1State = digitalRead(button1Pin);
  boolean button2State = digitalRead(button2Pin);
  float sliderState = analogRead(sliderPin);
   
  //print sensor date to serial monitor 
  Serial.print(button1State, 1);
  Serial.print(",\t");
  Serial.print(button2State, 1);
  Serial.print(",\t");
  Serial.println(sliderState, 2);
  
   // if the button pushed, send message
  byte message[length];
  String msg;
  if(button1State){
    if(sliderState > 900){
      msg = "I love you so much!";
      msg.getBytes(message, length);
    }else if(sliderState > 600){
      msg = "I love you!";
      msg.getBytes(message, length);
    }
    else if(sliderState > 300){
      msg = "I like you.";
      msg.getBytes(message, length);
    }else{
      msg = "I miss you.";
      msg.getBytes(message, length);
    }
    Serial.print(msg);
    chibiTx(42, message, length);
  }
  if(button2State){
    if(sliderState > 900){
      msg = "Fuck off!";
      msg.getBytes(message, length);
    }else if(sliderState > 600){
      msg = "I hate you!"; 
      msg.getBytes(message, length);
    }
    else if(sliderState > 300){
      msg = "I don't like you!";
      msg.getBytes(message, length);
    }else{
      msg = "Don't be mean to me.";
      msg.getBytes(message, length);
    }
    Serial.println(msg);
    chibiTx(42, message, length);
  }
  
  //Wait half a second
  delay(500);
}
