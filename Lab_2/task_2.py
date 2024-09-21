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
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.EV3_COLOR_COLOR)
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.


color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

touch_counter = 0

try:
    print("Press touch sensor on port 1 to check color")
    touch = 0
    while not touch:
        try:
            touch = BP.get_sensor(BP.PORT_1)
        except brickpi3.SensorError:
            pass

    while True:
        touch = BP.get_sensor(BP.PORT_1)

        time.sleep(2)  

        if touch:
            touch_counter += 1
        
        if touch_counter == 2:
            raise KeyboardInterrupt

        try:
            value = BP.get_sensor(BP.PORT_2)

            speed = value * 10 # calculate speed by value of color

            # Set the motor speed for all four motors
            BP.set_motor_power(BP.PORT_D, speed)

            print("Color: ", color[value], " Speed: ", speed) # print the color and speed

        except brickpi3.SensorError as error:
            print(error)
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
