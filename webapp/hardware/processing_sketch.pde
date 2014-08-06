import processing.serial.*;
Serial myPort;
int val = 0;
int NEWLINE = 10;
String buff = "";
int counter = 0;  
int radius = 512;
String completeVal = "";

void setup() {  
  String portName = Serial.list()[11];
  println(portName);
  myPort = new Serial(this, portName, 9600);
  size(1900, 1200);
  background(0,0,0);
}

//void draw() {
//  ellipseMode(CENTER);    
////  for(int i=0; i<100; i++){
////    ellipse(512, 512, i,i);
////  }
//  ellipse(mouseX, mouseY, 42,42);
//  
//
//  if (myPort.available() > 0) {
//    val = myPort.readStringUntil('\n');
////    println("Available", myPort.available());
//    if (myPort.available() == 0) {
//      completeVal = val;
////      println("Finished reading");
////      delay(100);
//
//    }
//  }
//  if (val != null){ 
//    println(val.getClass().getName());
//    radius = Integer.parseInt(val);
//    println("Radius,val: ", radius, val);
//    ellipse(radius-500, 500, 42, 42);
//  }
//}

void draw()
{
  while (myPort.available() > 0) {
    serialEvent(myPort.read());
  }
  background(val,255,100);
}

void serialEvent(int serial) 
{ 
  // If the variable "serial" is not equal to the value for 
  // a new line, add the value to the variable "buff". If the 
  // value "serial" is equal to the value for a new line,
  //  save the value of the buffer into the variable "val".
  if(serial != NEWLINE) { 
    buff += char(serial);
  } else {
    // The end of each line is marked by two characters, a carriage
    // return and a newline.  We're here because we've gotten a newline,
    // but we still need to strip off the carriage return.
    buff = buff.substring(0, buff.length()-1);
    // Parse the String into an integer
    val = Integer.parseInt(buff)/4;
    println(0,255,255);
    // Clear the value of "buff"
    buff = "";
  }
}
