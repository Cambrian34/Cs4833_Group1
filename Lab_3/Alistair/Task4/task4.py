#!/usr/bin/env python

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

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

#thread 2
def move_robot():
    port = "/dev/ttyUSB0"
    ser = serial.Serial(port, baudrate=9600, timeout=1)
    #while True:
       # try:
            


#start the threads
import threading
threading.Thread(target=check_color).start()

import serial
#threading.Thread(target=move_robot).start()
