import mySerCommLibrary
from mySerCommLibrary import *

#baudrate=9600, port="/dev/ttyUSB0", timeout=1

lib = mySerCommLibrary.SerialComm(9600, "/dev/ttyUSB0", 1)

lib.initSerComm()

#Implement DrunkRobot program
# Move forward until 5cm before an obstacle;
# Move backward 5cm; turn left/right for a random degree;
# Repeat the above actions for 2 minutes!!!


#run a thread to read the sensor data
import threading
import time
import random


#had to increase the distance to 15cm, the robot's ultrasonic sensor was less than 5cm from the front of the robot
#also had to increase backup distance to 10cm

#set timer for 2 minutes
start_time = time.time()

while time.time() - start_time < 120:
    #check if sonic data is valid
#    print("work " +sonicdata)
    getSonic = int(lib.readSonicCM(3))
    #time.sleep(0.2)
    if getSonic > 15:
        lib.moveForward(10)
        #time.sleep(0.1)
    else:
        print("stop")
        lib.stop_robot()
        time.sleep(1)
        lib.moveBack(15)
        if(int( lib.readSonicCM(3))== 15):
            lib.stop_robot()
        time.sleep(0.5) 
        if(random.choice([1,0])):
            lib.turnRight(random.randint(10,50))
            time.sleep (0.5)
            lib.stop_robot()
            
        else:
            lib.turnLeft(random.randint(10,50))
            time.sleep (0.5)
            lib.stop_robot()
            
print("End")  
lib.stop_robot()
