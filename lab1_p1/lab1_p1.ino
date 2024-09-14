#include <Wire.h>
#include <PRIZM.h>
PRIZM prizm;

void setup() {
  // put your setup code here, to run once:
  prizm.PrizmBegin();
  serial.Begin();
  prizm.setMotorInvert(1,1);

}

void loop() {
  // put your main code here, to run repeatedly:
  turnLeft();
  turnRight();
  prizm.PRIZMEnd();

}

void turnLeft(){
  prizm.setMotorPowers(50,-50);
  delay(600);
  prizm.setMotorPowers(125,125);
  delay(3000);
}
void turnRight(){
  prizm.setMotorPowers(-50,50);
  delay(600);
  prizm.setMotorPowers(125,125);
  delay(3000);
}

