#!/usr/bin/python3

import serial
import time
from struct import pack, unpack
from enum import IntEnum

serHead = serial.Serial('/dev/ttyACM0', 921600, timeout=5)
serBody = serial.Serial('/dev/ttyACM1', 921600, timeout=5)

# #read from Arduino
# input = ser.read()
# print("Read input " + input.decode("utf-8") + " from Arduino")

class StormBreakerType(IntEnum):
    StormBreakerError = -2
    StormBreakerWarning = -1
    StormBreakerOK = 0
    StormBreakerBody = 1
    StormBreakerHead = 2

class StormBreakerLength(IntEnum):
    body = 5
    head = 11

class StormBreaker:
    
    def __init__(self):
        self.message_type = None
        self.length = None
        self.data = None
        
    def __str__(self):
        return ("StormBreaker package:\n - message_type: {0}\n - length: {1}\n - "
                "data: {2}").format(self.message_type, self.length, self.data)


def send_stormbreaker(data, body, head):
    if head == True:
        print("Sending head frame")
        serHead.write(StormBreakerType.StormBreakerHead)
        serHead.write(StormBreakerLength.head)
        serHead.write(data[0])
        serHead.write(data[20:24])
        serHead.write(data[27:28])
        serHead.write(data[30:32])

    if body == True:
        print("Sending body frame")
        serBody.write(StormBreakerType.StormBreakerBody)
        serBody.write(StormBreakerLength.body)
        serBody.write(data[25:26])
        serBody.write(data[29])
        serBody.write(data[31:32])
    

def receive_stormbreaker(body, head):
    if head == True:
        if serHead.in_waiting > 0:
            line = serHead.readline()
            print(line)
            # print(line.decode("utf-8"))
    
    if body == True:
        if serBody.in_waiting > 0:
            line = serBody.readline()
            print(line)
            # print(line.decode("utf-8"))
