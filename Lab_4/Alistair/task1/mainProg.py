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

sonicdata = 100

def upsonic():
    global sonicdata
    while True:
        if(readSonicCM(3) is not None):
            getSonic = int(readSonicCM(3))
            time.sleep(0.5)
            #print(getSonic)
            
#sonicthread = threading.Thread(target=upsonic)
#sonicthread.daemon = True
#sonicthread.start()

#set timer for 2 minutes
start_time = time.time()

while time.time() - start_time < 120:
    getSonic = int(readSonicCM(3))
    time.sleep(0.1)
    if getSonic < 5:
        moveForward(50)
        time.sleep(1)
    elif(sonicdata > 5 ):
        stop_robot()
        time.sleep(1)
        if(random.choice([1,0])):
            turnRight(random.randint(10,50))
            time.sleep (0.5)
            stop_robot()
        else:
            turnLeft(random.randint(10,50))
            time.sleep (0.5)
            stop_robot()
        time.sleep(0.5)
    
