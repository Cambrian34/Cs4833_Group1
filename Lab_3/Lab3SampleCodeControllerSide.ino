/*
  Serial Event example
 
 When new serial data arrives, this sketch adds it to a String.
 When a newline is received, the loop prints the string and 
 clears it.
 
 A good test for this is to try it with a GPS receiver 
 that sends out NMEA 0183 sentences. 
 
 Created 9 May 2011
 by Tom Igoe
 
 This example code is in the public domain.
 
 http://www.arduino.cc/en/Tutorial/SerialEvent
 
 */

#include <Wire.h>  // include the PRIZM library in the sketch
//#include <PRIZM.h>               // include the PRIZM library in the sketch
//PRIZM prizm;                     // instantiate a PRIZM object “prizm” so we can use its functions

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
String outputString = "";        // a string to hold outgoing data

int cmd = 0;         // an integer to store the cmd
String cmdStr = "";  // a string to store the cmd

void setup() {
  //prizm.PrizmBegin();            // start prizm
  //prizm.setMotorInvert(1,1);     // invert the direction of DC Motor 1 to harmonize the direction of opposite facing drive motors

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
          //prizm.setMotorPowers(125,20);      // please note that here we hardcode the speed of the motor, you can adjust my code and transfer the speed value you want through the serial communication
          break;
        }
      // turn right
      case 3:
        {
          outputString += "3";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          //prizm.setMotorPowers(20,125);      // please note that here we hardcode the speed of the motor, you can adjust my code and transfer the speed value you want through the serial communication
          break;
        }
      // read sonic sensor connected to D3 on the controller
      case 4:
        {
          outputString += "4";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          //outputString += prizm.readSonicSensorCM(3); // please note that here we hardcode the port number of the sonic sensor, you can adjust the value to make it fits your robot
          // also, here we append the distance to the outputString so that we can send back to Pi
          break;
        }
      // break the motor
      case 5:
        {
          outputString += "5";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          //prizm.setMotorPowers(125,125);
          break;
        }
      // stop the motor
      case 6:
        {
          outputString += "6";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          //prizm.setMotorPowers(0,0);
          break;
        }
      //move forward with motor power 50
      case 7:
        {
          outputString += "7";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
                                // prizm.setMotorPowers(50,50);
          break;
        }
      //move backward with motor power 50
      case 8:
        {
          outputString += "8";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          //prizm.setMotorPowers(-50,-50);
          break;
        }
      //move forward with motor power 100
      case 9:
        {
          outputString += "9";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          //prizm.setMotorPowers(100,100);
          break;
        }
      //move backward with motor power 100
      case 10:
        {
          outputString += "10";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          //prizm.setMotorPowers(-100,-100);
          break;
        }
      //return distance with the ultrasonic sensor in cm
      case 11:
        {
          outputString += "11";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          //outputString += prizm.readSonicSensorCM(3); // please note that here we hardcode the port number of the sonic sensor, you can adjust the value to make it fits your robot
          outputString += " cm";
          break;
        }
      //ask user to for motor power
      case 12:
        {
          outputString += "12";  // everytime we put the original cmd to our outputString, to tell Pi know we get the cmd
          outputString += "Please enter the motor power you want to set (0-100): ";
          break;
        }
        //got a little carried away with the test cases
      //set motor power based on user input in 12
      case 13:
        {
          // Wait for the motor power input
          while (Serial.available() == 0) {
            // Wait until something is available on the serial line
          }

          String motorPowerStr = Serial.readStringUntil('\n');  // Read until newline
          int motorPower = motorPowerStr.toInt();               // Convert the input to an integer

          if (motorPower >= 0 && motorPower <= 100) {
            outputString += "13 Motor power set to: ";
            outputString += motorPower;
            //prizm.setMotorPowers(motorPower, motorPower);  // Uncomment this to set motor power
          } else {
            outputString += "13 Invalid motor power. Enter a value between 0 and 100.";
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
