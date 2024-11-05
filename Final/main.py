import threading
import mySerCommLibrary

lib = mySerCommLibrary.SerialComm(9600, "/dev/ttyUSB0", 1)

lib.initSerComm()

parked = False

#thread for color detectioncolor_thread = threading.Thread(target=check_color)

threading.Thread(target=lib.check_color).start()



# TODO: check touch sensor to start the program

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

