import mySerCommLibrary

lib = mySerCommLibrary.SerialComm(9600, "/dev/ttyUSB0", 1)

lib.initSerComm()

parked = False

# TODO: check touch sensor to start the program

while not parked:

    # move forward

    # TODO: check space color thread

    # stop and begin turn sequence

    # TODO: check gyro thread

    # stop and begin forward sequence

    # TODO: check parking distance thread

    # stop and end program

    break

