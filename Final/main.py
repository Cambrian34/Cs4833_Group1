import threading
import mySerCommLibrary
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.

lib = mySerCommLibrary.SerialComm(9600, "/dev/ttyUSB0", 1)

lib.initSerComm()


#thread for color detectioncolor_thread = threading.Thread(target=check_color)

threading.Thread(target=lib.check_color).start()



# Check touch sensor to start the program
print("Press touch sensor on port 1 to check color")
touch = 0
while not touch:
    try:
        touch = BP.get_sensor(BP.PORT_1)
    except brickpi3.SensorError:
        pass

# Main Parking Program:
parked = False

while not parked:

    # move forward

    # TODO: check space color thread
    if lib.color_detected == "Blue":
        lib.stop_robot()
        break

    # stop and begin turn sequence

    # TODO: check gyro thread

    # stop and begin forward sequence

    # TODO: check parking distance thread, an error where the thread and library call the arduino at same time coausing an erro that the arduino is busy,
    #ie a critical section problem
    #could solving this by using a semaphore or mutex
    

    # stop and end program

    break

