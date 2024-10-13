#!/usr/bin/python3
import serial
import time
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# Configure for an EV3 color sensor.
# BP.set_sensor_type configures the BrickPi3 for a specific sensor.
# BP.PORT_1 specifies that the sensor will be on sensor port 1.
# BP.Sensor_TYPE.EV3_COLOR_COLOR specifies that the sensor will be an ev3 color sensor.
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]


# Define port
port = "/dev/ttyUSB0"

# Setup serial port
ser = serial.Serial(port, baudrate=9600, timeout=1)


# since we need to send cmd to the controller multiple times
# we can write a function for convenient use
def cmdSend(ser, cmd):
    # our msg must append a newline symbol, because that symbol is used for controller to check whether the cmd is fully received
    msg = str(cmd) + "\n"
    
    # encode the msg before sending
    ser.write(msg.encode())
    
    # originally received msg will end with '\r\n'
    ack_origin = ser.readline()
    
    # we can skip the last two chars
    # and then decode the msg using utf-8
    ack = ack_origin[:-2].decode("utf-8")
    
    # return the msg we get
    return ack


# let user know what is the next step
print("*** Press the GREEN button to start the robot ***")

# wait 2 seconds to give time to press the button        
time.sleep(2)

# Setup communication with controller
while True:
    print("--- Sending out handshaking signal ---")
    # ser is the variable name we initialed as a serial.Serial instance, see line 10 in this file
    # cmd is 1, used for checking whether the controller have responded
    ack = cmdSend(ser, 1)

    # not received any msg
    if not ack:
        print("*** Try again ***")
        print("*** Press the GREEN button to start the robot ***")
    
    # received msg
    else:
        print("!!! Connected to the robot !!!")
        
        # clear the serial receive buffer
        ser.readall()

        # we can break this while loop now
        break

# -------------------
# Follow Yellow Line:
# -------------------
def move_forward():
    # move forward, cmd 7
    command = str(7)+'\n'
    ser.write(command.encode())
    ack = ser.readline().decode("utf-8").strip()
    # print("Move forward cmd ", ack)

def brake():
    # brake, cmd 5
    command = str(5)+'\n'
    ser.write(command.encode())
    ack = ser.readline().decode("utf-8").strip()
    # print("Brake cmd ", ack)


def find_yellow_line():
    # want to turn left 90 degrees, then right 180 degrees until yellow is found
    # turn left, cmd 2
    command = str(2)+'\n'
    ser.write(command.encode())
    ack = ser.readline().decode("utf-8").strip()
    print("Turn left cmd ", ack)


yellowLost = False # tracks if yellow line lost
started = False # tracks if started already

lostCounter = 0

# Follow Line:
while True:
    # Read the color:
    try:
        value = BP.get_sensor(BP.PORT_3)
        print("Color: ", color[value]) # print the color
    except brickpi3.SensorError as error:
        print(error)
        continue

    if not started and color[value] == "Blue" :
        print("Start")
        move_forward()
        started = True
        time.sleep(1)

    elif yellowLost and color[value] == "Yellow":
        print("Found track")
        move_forward()
        yellowLost = False

    elif yellowLost:
        # TODO: FIND YELLOW!!!
        print("Yellow Lost")
        brake()
        break

    elif color[value] != "Yellow": # color black, find yellow:
        lostCounter += 1

        if lostCounter >= 10 and not yellowLost:
            print("Off track")

            # Set yellowLost to true:
            yellowLost = True
            lostCounter = 0

        