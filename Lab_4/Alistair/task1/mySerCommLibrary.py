import time
#import brickpi3
import serial
import threading

#BP = brickpi3.BrickPi3()

#BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_COLOR_COLOR)
#color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

#color_detected = "none"
#port = "/dev/ttyUSB0"
#ser = serial.Serial(port, baudrate=9600, timeout=1)

def  initSerComm(baudrate):
    global ser
    global port 
    port = "/dev/ttyUSB0"
    ser = serial.Serial(port, baudrate=baudrate, timeout=1)
    #starts handshaking
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



def cmdSend(ser, cmd):
    msg = str(cmd) + "\n"
    ser.write(msg.encode())
    ack_origin = ser.readline()
    ack = ack_origin[:-2].decode("utf-8")
    return ack

def moveForward(power):
    print("Move forward")
    
    ack = cmdSend(ser, 12)
    
    # check the output we get from the controller
    print("Arduino is now waiting for motor power input...")
    print(ack)
    
    #timer for 1 seconds
    time.sleep(1)
    # Send the motor power as plain data, not as a command
    motor_power = power+"\n"  # Send motor power value
    
    ser.write(motor_power.encode())  # Send motor power directly to Arduino
    
    # Wait for Arduino response
    ack = ser.readline().decode("utf-8").strip()
    #print(f"Motor power set: {ack}")
    print(ack)

def moveBack(power):
    print("Move backward")
    ack = cmdSend(ser, 12)
    
    # check the output we get from the controller
    print("Arduino is now waiting for motor power input...")
    print(ack)
    
    #timer for 1 seconds
    time.sleep(1)
    # Send the motor power as plain data, not as a command
    motor_power = (-power)+"\n"  # Send motor power value
    
    ser.write(motor_power.encode())  # Send motor power directly to Arduino
    
    # Wait for Arduino response
    ack = ser.readline().decode("utf-8").strip()
    #print(f"Motor power set: {ack}")
    print(ack)

def turnLeft(power):
    print("Turn left")
    ack = cmdSend(ser, 16)
    # check the output we get from the controller
    print("Arduino is now waiting for motor power input...")
    print(ack)
    
    #timer for 1 seconds
    time.sleep(1)
    # Send the motor power as plain data, not as a command
    motor_power = power+"\n"  # Send motor power value
    
    ser.write(motor_power.encode())  # Send motor power directly to Arduino
    
    # Wait for Arduino response
    ack = ser.readline().decode("utf-8").strip()
    #print(f"Motor power set: {ack}")
    print(ack)

def turnRight(power):
    print("Turn right")
    ack = cmdSend(ser, 17)
    # check the output we get from the controller
    print("Arduino is now waiting for motor power input...")
    print(ack)
    
    #timer for 1 seconds
    time.sleep(1)
    # Send the motor power as plain data, not as a command
    motor_power = power+"\n"  # Send motor power value
    
    ser.write(motor_power.encode())  # Send motor power directly to Arduino
    
    # Wait for Arduino response
    ack = ser.readline().decode("utf-8").strip()
    #print(f"Motor power set: {ack}")

    print(ack)

def stop_robot():
    print("Stop")
    ack = cmdSend(ser, 5)
    print(ack)

def turn_around():
    print("Turn around")
    ack = cmdSend(ser, 13)
    print(ack)

def readSonicIN(port):
    print("Read Sonic INCHES")
    ack = cmdSend(ser, 11)
    # check the output we get from the controller
    print("Arduino is now waiting for port input...")
    print(ack)
    
    #timer for 0.5 seconds
    time.sleep(0.5)
    # Send the motor power as plain data, not as a command
    motor_power = port+"\n"  # Send motor power value
    
    ser.write(motor_power.encode())  # Send motor power directly to Arduino
    
    # Wait for Arduino response
    ack = ser.readline().decode("utf-8").strip()
    #print(f"Motor power set: {ack}")
    print(ack)

def readSonicCM(port):
    print("Read Sonic CM")
    ack = cmdSend(ser, 4)
    # check the output we get from the controller
    print("Arduino is now waiting for port input...")
    print(ack)
    
    #timer for 0.5 seconds
    time.sleep(0.5)
    # Send the motor power as plain data, not as a command
    motor_power = port+"\n"  # Send motor power value
    
    ser.write(motor_power.encode())  # Send motor power directly to Arduino
    
    # Wait for Arduino response
    ack = ser.readline().decode("utf-8").strip()
    #print(f"Motor power set: {ack}")
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