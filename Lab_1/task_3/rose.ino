#include <PRIZM.h>
#include <Wire.h>
PRIZM prizm;

void setup() {
  prizm.PrizmBegin();
  Serial.begin(9600);
  prizm.setMotorInvert(1,1);
}
void loop() {
  int distance = prizm.readSonicSensorCM(3);
  while (distance > 80) {
    prizm.setMotorPowers(50, 50);
    Serial.println("Moving Forward until Target distance");
    //delay(100);
    distance = prizm.readSonicSensorCM(3);
  }
  prizm.setMotorPowers(125,125);
  if (distance < 80) {
    while (distance < 100) {
      prizm.setMotorPowers(-50,-50);
      Serial.println("Moving backward until target distance");
      distance = prizm.readSonicSensorCM(3);
      delay(10);
    }
  }
  prizm.setMotorPowers(125,125);
  delay(3000);
  
  
  prizm.setMotorPowers(50,-50);
  delay(600);
  prizm.setMotorPowers(125,125);
  delay(3000);
  
  distance = prizm.readSonicSensorCM(3);
  while (distance > 80) {
      prizm.setMotorPowers(50,50);
      Serial.println("Moving Forward until target distance");
      //delay(10);
      distance = prizm.readSonicSensorCM(3);
  }
  prizm.setMotorPowers(125,125);
  if (distance < 80) {
    while (distance < 80) {
      prizm.setMotorPowers(-50,-50);
      Serial.println("Moving backward until target distance");
      distance = prizm.readSonicSensorCM(3);
      delay(10);
    }
  }
  prizm.setMotorPowers(125,125);
  prizm.PrizmEnd();
}

