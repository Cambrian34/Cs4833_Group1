import threading
import time
import sys

import mySerCommLibrary
import brickpi3 # import the BrickPi3 drivers

# Get Command Line Arguments:
args = sys.argv
if len(args) < 2:
    print("Error: Must specify Student, Faculty, or Reserved")
    print("Example usage: python main.py Student")
    exit(1)

target_color = ""
if args[1] == "Student":
    target_color = "Blue"
elif args[1] == "Faculty":
    target_color = "Green"
elif args[1] == "Reserved":
    target_color = "Red"
else:
    print("Error: Invalid input, must specify Student, Faculty, or Reserved")
    exit(1)

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
        serial_comm.moveForward(17)

        # Check space color thread
        print("Color Thread Start")
        while True:
            print(brickpi_sensors.color_detected)
            if brickpi_sensors.color_detected == target_color:
                print("Target color ", target_color, " detected")
                serial_comm.stop_robot()
                break
            elif brickpi_sensors.color_detected == "Yellow":
                serial_comm.stop_robot()
                print("No available spaces!")
                raise KeyboardInterrupt  # stop program from continuing

        print("begin turn")

        # begin turn sequence
        serial_comm.turnLeft(20)
        time.sleep(1.8)
        serial_comm.stop_robot()


        # check if space available. if true, park; if not, turn back and continue searching for a space

        # Check Parking Distance:
        # print(type(serial_comm.readSonicCM(3)))
        initial_distance = serial_comm.readSonicCM(3)
        print("Parking Distance ", initial_distance)
        # print ("Type ", type(initial_distance))
        if  initial_distance >= 30:
            print("Space Available")
            serial_comm.moveForward(15)
            while serial_comm.readSonicCM(3) > 22:
                time.sleep(0.05)

            serial_comm.stop_robot()
            parked = True
        else:
            serial_comm.flashRed()
            time.sleep(2)
            serial_comm.moveBack(15)
            time.sleep(1.1)
            serial_comm.stop_robot()
            time.sleep(0.5)
            serial_comm.turnRight(20)
            time.sleep(1.7)  # TODO: calibrate turning
            serial_comm.stop_robot()


        # stop and end program
    serial_comm.flashGreen()

except KeyboardInterrupt:
    print("Exit")
    color_thread.join()
    brickpi_sensors.reset_sensors()
    exit(1)

