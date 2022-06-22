
//Copy all and paste to file Control MatrixLed

#include <Servo.h>



int servo1 = 6;
int servo2 = 5;
int c;
int angle;

Servo myServo1;
Servo myServo2;


void setup()
 {
  Serial.begin(115200);
  myServo1.attach(servo1);
  myServo2.attach(servo2);
}

void loop() {
  c = analogRead(A0);
  angle = map(c,0,1023,0,180);
  myServo1.write(angle);
  myServo2.write(angle);

  


}
