#include <PRIZM.h>
#include <Wire.h>
PRIZM prizm;


void setup() {
  // put your setup code here, to run once:
  PRIZM prizm;
  prizm.PrizmBegin();

  prizm.setMotorInvert(1,1);     // invert the direction of DC Motor 1   

}

void loop() {
  // put your main code here, to run repeatedly:
  if(prizm.readSonicSensorCM(3) > 20) 
  {
    prizm.setMotorPowers(25, 25);    // if distance greater than 20cm, do this
  }
  else if(prizm.readSonicSensorCM(3) < 20 && prizm.readSonicSensorCM(3) > 10)
  {
    prizm.setMotorPowers(125,125);   // if distance less than 25cm, do this
  }
  else
  {
   prizm.setMotorPowers(-25,-25);   // if distance less than 10cm, do this
  }   

}
