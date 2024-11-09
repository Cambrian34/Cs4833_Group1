import threading
import mySerCommLibrary
import brickpi3 # import the BrickPi3 drivers

# Setup Comms and Sensors:
serial_comm = mySerCommLibrary.SerialComm(9600, "/dev/ttyUSB0", 1)
serial_comm.initSerComm()

brickpi_sensors = mySerCommLibrary.Sensors()

#thread for color detectioncolor_thread = threading.Thread(target=check_color)

threading.Thread(target=lib.check_color).start()
threading.Thread(target=lib.check_gyro).start()


# Check touch sensor to start the program
print("Press touch sensor on port 1 to start program")
brickpi_sensors.check_touch()


# Main Parking Program:
parked = False

while not parked:

    # move forward

    # TODO: check space color thread
    if serial_comm.color_detected == "Blue":
        serial_comm.stop_robot()
        break

    # stop and begin turn sequence

    # TODO: check gyro thread

    # stop and begin forward sequence

    # TODO: check parking distance thread, an error where the thread and library call the arduino at same time coausing an erro that the arduino is busy,
    #ie a critical section problem
    #could solving this by using a semaphore or mutex


    # stop and end program

    break

