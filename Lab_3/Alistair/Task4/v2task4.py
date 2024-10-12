import time
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

follow_the_line()
