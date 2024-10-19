from mySerCommLibrary import *

initSerComm(9600)

#Implement DrunkRobot program
# Move forward until 5cm before an obstacle;
# Move backward 5cm; turn left/right for a random degree;
# Repeat the above actions for 2 minutes!!!


#run a thread to read the sensor data
import threading
import time
import random

getSonic = readSonicCM(3)
sonicthread = threading.Thread(target=getSonic)
sonicthread.daemon = True
sonicthread.start()

#set timer for 2 minutes
start_time = time.time()
while time.time() - start_time < 120:
    if getSonic < 5:
        moveForward(25)
    else:
        stop_robot()
        time.sleep(1)
        turnRight(random.randint(1, 50))
        time.sleep(50)
        turnLeft(random.randint(1, 50))
        time.sleep(1)
    
    
