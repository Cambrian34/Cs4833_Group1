#!/usr/bin/env python

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import serial

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# Configure for an EV3 color sensor.
# BP.set_sensor_type configures the BrickPi3 for a specific sensor.
# BP.PORT_1 specifies that the sensor will be on sensor port 1.
# BP.Sensor_TYPE.EV3_COLOR_COLOR specifies that the sensor will be an ev3 color sensor.
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

#follow the line

#create two threads to follow the line, one for brickpi and one for serial
#thread 1:create a method to check the color of the line
#thread 2: move the robot according to the color of the line by sending commands to the arduino

#thread 1
def check_color():
    while True:
        try:
            value = BP.get_sensor(BP.PORT_3)
            print("Color: ", color[value]) # print the color
        except brickpi3.SensorError as error:
            print(error)
def cmdSend(ser, cmd):
    # our msg must append a newline symbol, because that symbol is used for controller to check whether the cmd is fully received
    msg = str(cmd) + "\n"
    
    #print(f"Sending: {msg.strip()}")  # Debugging: See what’s being sent

    # encode the msg before sending
    ser.write(msg.encode())
    
    # originally received msg will end with '\r\n'
    ack_origin = ser.readline()
    
    # we can skip the last two chars
    # and then decode the msg using utf-8
    ack = ack_origin[:-2].decode("utf-8")
    
    # return the msg we get
    return ack    
#thread 2
def move_robot():
    port = "/dev/ttyUSB0"
    ser = serial.Serial(port, baudrate=9600, timeout=1)
    #*Control robot to follow color tape track
    #(WHITE or other color) on the ground
    #(ground normally recognized as BLACK)*#

    #The start/end points of the tape track is
    #different color (RED or YELLOW)
    
    #The robot should turnaround and return to the start point to complete the task

    #at the start of the track the robot should move forward when it detects red
    # and while it detects yellow it should move forward
    #and when it detects blue it should stop and turn around
    #and then move forward while detecting yellow
    #and stop when it detects red

    # let user know what is the next step
    print("*** Press the GREEN button to start the robot ***")

    time.sleep(2)

    while True:

        print("--- Sending out handshaking signal ---")
        try:
            value = BP.get_sensor(BP.PORT_3)
            print("Color: ", color[value]) # print the color
            if color[value] == "Red":
                print("Move forward")
                ack = cmdSend(ser,7 )
                print(ack)
                print("t1")

                #time.sleep(0.5)

                #ack = cmdSend(ser, 6)
                #print(ack)
                #print("t2")



                
            elif color[value] == "Yellow":
                print("Move forward")


                
            elif color[value] == "Blue":
                print("Stop")
                ack = cmdSend(ser, 6)
                print(ack)
                time.sleep(1)
                #turn around 180 degrees


        
        except brickpi3.SensorError as error:
            print(error)

       


#start the threads
import threading
#threading.Thread(target=check_color).start()


#threading.Thread(target=move_robot).start()
move_robot()
