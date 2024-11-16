import threading
import time

import mySerCommLibrary
import brickpi3 # import the BrickPi3 drivers

# Setup Comms and Sensors:
serial_comm = mySerCommLibrary.SerialComm(9600, "/dev/ttyUSB0", 1)
serial_comm.initSerComm()

brickpi_sensors = mySerCommLibrary.Sensors()
time.sleep(1)

# Start Color Checking Thread:
color_thread = threading.Thread(target=brickpi_sensors.check_color)
color_thread.start()

# Check touch sensor to start the program:
print("Press touch sensor on port 1 to start program")
brickpi_sensors.check_touch()


# Main Parking Program:
parked = False

try:
    while not parked:

        # Move Forward:
        serial_comm.moveForward(15)

        # Check space color thread
        print("Color Thread Start")
        while True:
            print(brickpi_sensors.color_detected)
            if brickpi_sensors.color_detected == "Blue":
                serial_comm.stop_robot()
                break

        print("begin turn")

        # begin turn sequence
        serial_comm.turnLeft(20)
        time.sleep(1.8) # TODO: calibrate turning
        serial_comm.stop_robot()

        # TODO: check gyro thread

        # check if space available. if true, park; if not, turn back and continue searching for a space

        # TODO: check parking distance thread, an error where the thread and library call the arduino at same time coausing an erro that the arduino is busy,
        #ie a critical section problem
        #could solving this by using a semaphore or mutex
        # print(type(serial_comm.readSonicCM(3)))
        initial_distance = serial_comm.readSonicCM(3)
        print("Parking Distance ", initial_distance)
        # print ("Type ", type(initial_distance))
        if  initial_distance >= 30:
            print("Space Available")
            serial_comm.moveForward(15)
            while serial_comm.readSonicCM(3) > 15:
                time.sleep(0.1)

            serial_comm.stop_robot()
            parked = True
        else:
            serial_comm.moveBack(15)
            time.sleep(1.6)
            serial_comm.stop_robot()
            time.sleep(0.5)
            serial_comm.turnRight(20)
            time.sleep(1.8)  # TODO: calibrate turning
            serial_comm.stop_robot()


        # stop and end program

except KeyboardInterrupt:
    print("Exit")
    color_thread.join()
    exit(1)

