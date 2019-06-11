#!/usr/bin/python3

import serial
import time
from struct import pack, unpack
from enum import IntEnum
import array as arr

serBody = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
serHead = serBody
#serial.Serial('/dev/ttyACM1', 921600, timeout=5)

def flush_buffer():
    serBody.reset_input_buffer()
    serHead.reset_input_buffer()
    time.sleep(0.25)
    serBody.reset_output_buffer()
    serHead.reset_output_buffer()
    time.sleep(0.25)

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
        serHead.write(pack('>BBBBBBBBBBBBB', StormBreakerType.StormBreakerHead, StormBreakerLength.head, data[0], data[24], data[25], data[26], data[27], data[34], data[58], data[59], data[60], data[61], data[126]))
        print("Head Data: ")
        print(data[0])
        print(data[24])
        print(data[25])
        print(data[26])
        print(data[27])
        print(data[34])
        print(data[58])
        print(data[59])
        print(data[60])
        print(data[61])
        print(data[126])
        time.sleep(0.2)
        
    if body == True:
        print("Sending body frame")
        serBody.write(pack('>BB', StormBreakerType.StormBreakerBody,StormBreakerLength.body))
        serBody.write(pack('>B', data[24]))
        serBody.write(pack('>B', data[25]))
        serBody.write(pack('>B', data[26]))
        serBody.write(pack('>B', data[27]))
        serBody.write(pack('>B', data[34]))
        print(data[24])
        print(data[25])
        print(data[26])
        print(data[27])
        print(data[34])
        time.sleep(0.3)
        

def receive_stormbreaker(body, head):
    if head == True:
        while serHead.in_waiting > 0:
            while serHead.in_waiting > 0:
                line = serHead.readline()
                print(line)
                # print(line.decode("utf-8"))
            time.sleep(0.2)
    
    if body == True:
        while serBody.in_waiting > 0:
            while serBody.in_waiting > 0:
                line = serBody.readline()
                print(line)
                # print(line.decode("utf-8"))
            time.sleep(0.2)

def receive_serials():
    while serBody.in_waiting > 0:
        while serBody.in_waiting > 0:
            line = serBody.readline()
            print(line)
        time.sleep(0.5)

    while serHead.in_waiting > 0:
        while serHead.in_waiting > 0:
            line = serHead.readline()
            print(line)
        time.sleep(0.5)
