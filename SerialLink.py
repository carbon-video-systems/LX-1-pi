#!/usr/bin/python3

import serial
import time

ser = serial.Serial('/dev/ttyACM0', 921600, timeout=5)

#read from Arduino
input = ser.read()
print("Read input " + input.decode("utf-8") + " from Arduino")

while 1:
    # write back
    ser.write(b'A5z')
    
    #read response back from Arduino
    for i in range (0,1):
        input = ser.read()
        print(input)
        #input_number = ord(input)
        #print (str(input_number))
        
    time.sleep(0.5)