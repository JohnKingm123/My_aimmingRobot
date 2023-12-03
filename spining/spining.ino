#include <Servo.h>


Servo Servo_X;//port sv 5
Servo Servo_Y;//port sv 9

void setup(){

  Serial.begin(9600);
  Servo_X.attach(5);
  Servo_Y.attach(9);
  //舵机初始化

  Servo_X.write(103);
  Servo_Y.write(103);
  //舵机角度矫正
  // print("done!")

}


void loop(){

  while (!Serial.available());
  int dx = Serial.readStringUntil(',').toInt();
  while (!Serial.available());
  int dy = Serial.readStringUntil('\n').toInt();
  
  if (dx<180&&dx>0){Servo_X.write(dx);}
  if (dx<180&&dx>0){Servo_Y.write(dy);}

}


