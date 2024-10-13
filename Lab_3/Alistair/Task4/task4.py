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
wrong_color = ["none", "Black", "Green", "White", "Brown"]

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



#start the threads
import threading
#threading.Thread(target=check_color).start()


#threading.Thread(target=move_robot).start()
#move_robot()



#version2 of the code
def follow_the_line():
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

                #move forward slowly
                ack = cmdSend(ser,7 )
                print(ack)
                print("t1")

                #time.sleep(0.5)

                #ack = cmdSend(ser, 6)
                #print(ack)
                #print("t2")



                
            elif color[value] == "Yellow":
                #call the follow the line sub function
                print("Move forward")
                #if the color is yellow move forward if the color is black turn left slightly and check the color again and if yellow move forward else turn right slightly and check the color again
                ack = cmdSend(ser, 7)
                print(ack)
                time.sleep(0.1)
        
            elif color[value] == "Black":
                #turn left slightly cmd 14
                ack = cmdSend(ser, 14)
                print(ack)
                time.sleep(0.1)#to make sure the robot has turned
                #check the color again
                value = BP.get_sensor(BP.PORT_3)
                print("Color: ", color[value])
                if color[value] == "Yellow":
                    #move forward
                    ack = cmdSend(ser, 7)
                    print(ack)
                    time.sleep(0.1)
                else:
                    #turn right slightly
                    ack = cmdSend(ser, 15)
                    print(ack)
                    time.sleep(0.1)
                




                
            elif color[value] == "Blue":
                print("Stop")
                #should i add something to make sure this only runs once
                
                ack = cmdSend(ser, 6)
                print(ack)
                time.sleep(0.5)
                #turn around 180 degrees which is 13
                ack = cmdSend(ser, 13)
                print(ack)
                time.sleep(0.5)
                #move forward
                ack = cmdSend(ser, 7)
                print(ack)
                time.sleep(0.1)



            
        
        except brickpi3.SensorError as error:
            print(error)


"""import time
import brickpi3
import serial
import threading

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_COLOR_COLOR)
color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

color_detected = "none"
port = "/dev/ttyUSB0"
ser = serial.Serial(port, baudrate=9600, timeout=1)

def cmdSend(ser, cmd):
    msg = str(cmd) + "\n"
    ser.write(msg.encode())
    ack_origin = ser.readline()
    ack = ack_origin[:-2].decode("utf-8")
    return ack

def move_forward():
    print("Move forward")
    ack = cmdSend(ser, 7)
    print(ack)

def turn_left():
    print("Turn left")
    ack = cmdSend(ser, 14)
    print(ack)

def turn_right():
    print("Turn right")
    ack = cmdSend(ser, 15)
    print(ack)

def stop_robot():
    print("Stop")
    ack = cmdSend(ser, 5)
    print(ack)

def turn_around():
    print("Turn around")
    ack = cmdSend(ser, 13)
    print(ack)

def check_color():
    global color_detected
    while True:
        try:
            value = BP.get_sensor(BP.PORT_3)
            color_detected = color[value]
            time.sleep(0.1)
        except brickpi3.SensorError as error:
            print(error)
Counter = 0 #if counter is 0, the robot will turn left 
counter2 = 0 
def follow_the_line():
    print("*** Press the GREEN button to start the robot ***")
    time.sleep(2)
    
    while True:
        print("--- Sending out handshaking signal ---")
        ack = cmdSend(ser, 1)
        if not ack:
            print("*** Try again ***")
            print("*** Press the GREEN button to start the robot ***")

        else:
            print("!!! Connected to the robot !!!")
            ser.readall()
            break    
    count = 0;           
    while True:
            if color_detected == "Blue":
                if count == 1:
                    stop_robot()
                    break
                move_forward()
                
            
            elif color_detected == "Red":
                stop_robot()
                time.sleep(0.5)
                turn_around()
                count = 1
                time.sleep(0.5)
                move_forward()
                time.sleep(0.1)


#thread for checking the color
color_thread = threading.Thread(target=check_color)
color_thread.daemon = True
color_thread.start()

follow_the_line()"""