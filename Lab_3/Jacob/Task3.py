#!/usr/bin/python3
import serial
import time


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
            


# Follow hand:
while True:
    # cmd 4 is to read sonic sensor:
    read_sonic = str(4)+'\n'
    ser.write(read_sonic.encode())
    ack = ser.readline().decode("utf-8").strip()
    print("Sonic Distance: ")
    print(ack)

    distance = int(ack)

    if distance > 20:
        # move forward, cmd 7
        command = str(7)+'\n'
        ser.write(command.encode())
        ack = ser.readline().decode("utf-8").strip()
        print("Move forward cmd ", ack)

    elif distance < 20 and distance > 10:
        # brake, cmd 5
        command = str(5)+'\n'
        ser.write(command.encode())
        ack = ser.readline().decode("utf-8").strip()
        print("Brake cmd ", ack)
    else:
        # move backward, cmd 8
        command = str(8)+'\n'
        ser.write(command.encode())
        ack = ser.readline().decode("utf-8").strip()
        print("Move backward cmd ", ack)