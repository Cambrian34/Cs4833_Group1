
#include <Wire.h>  // include the PRIZM library in the sketch
#include <PRIZM.h>               // include the PRIZM library in the sketch
PRIZM prizm;                     // instantiate a PRIZM object “prizm” so we can use its functions

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
String outputString = "";        // a string to hold outgoing data

int cmd = 0;         // an integer to store the cmd
String cmdStr = "";  // a string to store the cmd

void setup() {
  prizm.PrizmBegin();            // start prizm
  prizm.setMotorInvert(1,1);     // invert the direction of DC Motor 1 to harmonize the direction of opposite facing drive motors

  Serial.begin(9600);  // initialize serial:

  // reserve 20/10 bytes for the string:
  inputString.reserve(20);
  outputString.reserve(20);
  cmdStr.reserve(10);
}

void loop() {
  // when stringComplete is true, we take actions, otherwise we skip
  if (stringComplete) {
    //our error lies here, we wanted to read more than just the first character and the example code only reads the first character
    cmdStr = inputString.substring(0, 2);  // here we only read the first char, and ignore the remainings. In the future, you can design your own msg format to transfer more information
    cmd = cmdStr.toInt();                  // convert string cmd to integer cmd

    switch (cmd) {
      // echo
      case 1:
        {
          outputString += "1";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          
          break;
        }
      // turn left
      case 2:
        {
          outputString += "2";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          prizm.setMotorPowers(125,20);      // please note that here we hardcode the speed of the motor, you can adjust my code and transfer the speed value you want through the serial communication
          break;
        }
      // turn right
      case 3:
        {
          outputString += "3";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          prizm.setMotorPowers(20,125);      // please note that here we hardcode the speed of the motor, you can adjust my code and transfer the speed value you want through the serial communication
          break;
        }
      // read sonic sensor connected to D3 on the controller
      case 4:
        {
          outputString += "4";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          outputString += prizm.readSonicSensorCM(3); // please note that here we hardcode the port number of the sonic sensor, you can adjust the value to make it fits your robot
          // also, here we append the distance to the outputString so that we can send back to Pi
          break;
        }
      // break the motor
      case 5:
        {
          outputString += "5";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          prizm.setMotorPowers(125,125);
          break;
        }
      // stop the motor
      case 6:
        {
          outputString += "6";  
          prizm.setMotorPowers(0,0);
          break;
        }
      //move forward with motor power 5
      case 7:
        {
          outputString += "7";    
          prizm.setMotorPowers(10,10);
          break;
        }
      //move backward with motor power 50
      case 8:
        {
          outputString += "8";  
          prizm.setMotorPowers(-50,-50);
          break;
        }
      //move forward with motor power 100
      case 9:
        {
          outputString += "9"; 
          prizm.setMotorPowers(100,100);
          break;
        }
      //move backward with motor power 100
      case 10:
        {
          outputString += "10";  
          prizm.setMotorPowers(-100,-100);
          break;
        }
      //return distance with the ultrasonic sensor in cm
      case 11:
        {
          outputString += "11\n";  
          outputString += prizm.readSonicSensorCM(3); 
          outputString += " cm";
          break;
        }
      //set motor power with user input
      case 12:
        {
          // Wait for the motor power input
          while (Serial.available() == 0) {
            // Wait until something is available on the serial line
          }

          String motorPowerStr = Serial.readStringUntil('\n');  // Read until newline
          int motorPower = motorPowerStr.toInt();               // Convert the input to an integer
//can modify to have back and forward motor power
          if (motorPower >= (-100) && motorPower <= 100) {
            outputString += "13 Motor power set to: ";
            outputString += motorPower;
            prizm.setMotorPowers(motorPower, motorPower); 
          } else {
            outputString += "13 Invalid motor power. Enter a value between 0 and 100.";
          }

          Serial.println(outputString);  // Send back the result
          outputString = "";             // Clear the output string for the next command
          break;
        }
        // case13 is for the code to turn the robot 180 degree
      case 13:
        {
          outputString += "13";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          prizm.setMotorPowers(50,-50);  // please note that here we hardcode the speed of the motor, you can adjust my code and transfer the speed value you want through the serial communication
          delay(1200);  // delay 1s to make sure the robot turns 180 degree
          prizm.setMotorPowers(125,125);  // stop the robot
          break;
        }
        //turn left slowly with 5
      case 14:
        {
          outputString += "14";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          prizm.setMotorPowers(5,-5);  // please note that here we hardcode the speed of the motor, you can adjust my code and transfer the speed value you want through the serial communication
          break;
        }
        //turn right slowly with 5
      case 15:
        {
          outputString += "15";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          prizm.setMotorPowers(-5,5);  // please note that here we hardcode the speed of the motor, you can adjust my code and transfer the speed value you want through the serial communication
          break;
        }
        //turn left with given power
      case 16:
        {
          // Wait for the motor power input
          while (Serial.available() == 0) {
            // Wait until something is available on the serial line
          }

          String motorPowerStr = Serial.readStringUntil('\n');  // Read until newline
          int motorPower = motorPowerStr.toInt();               // Convert the input to an integer

          if (motorPower >= 0 && motorPower <= 100) {
            outputString += "16 Motor power set to: ";
            outputString += motorPower;
            prizm.setMotorPowers(motorPower, 0); 
          } else {
            outputString += "16 Invalid motor power. Enter a value between 0 and 100.";
          }

          Serial.println(outputString);  // Send back the result
          outputString = "";             // Clear the output string for the next command
          break;
        }
        //turn right with given power
      case 17:
        {
          // Wait for the motor power input
          while (Serial.available() == 0) {
            // Wait until something is available on the serial line
          }

          String motorPowerStr = Serial.readStringUntil('\n');  // Read until newline
          int motorPower = motorPowerStr.toInt();               // Convert the input to an integer

          if (motorPower >= 0 && motorPower <= 100) {
            outputString += "17 Motor power set to: ";
            outputString += motorPower;
            prizm.setMotorPowers(0, motorPower); 
          } else {
            outputString += "17 Invalid motor power. Enter a value between 0 and 100.";
          }

          Serial.println(outputString);  // Send back the result
          outputString = "";             // Clear the output string for the next command
          break;
        }
      //default case
      default:
        {
          outputString += "Invalid command";
          break;
        }
    }

    Serial.println(outputString);  // println helps us to send back msg with a '\n' at the end

    // clear the variables to wait for another cmd sending
    inputString = "";
    outputString = "";
    cmdStr = "";
    cmd = 0;
    stringComplete = false;  // reset the flag to make sure we only enter this if condition when the next line of data is received
  }
}


// ************* You do not need to modify the following ***************
// ************* Read the following code will help you understand how it deal with incoming data from serial port **************
/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
