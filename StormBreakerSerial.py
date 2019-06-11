#!/usr/bin/python3

import serial
import time
from struct import pack, unpack
from enum import IntEnum
import array as arr

serBody = serial.Serial('/dev/ttyACM0', 115200, timeout=5)
serHead = serBody
#serial.Serial('/dev/ttyACM1', 921600, timeout=5)

# #read from Arduino
# input = ser.read()
# print("Read input " + input.decode("utf-8") + " from Arduino")

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
        serHead.write(pack('>BBBBBBBBBBBBB', StormBreakerType.StormBreakerHead, StormBreakerLength.head, data[0], data[3], data[5], data[35], data[38], data[39],data[27], data[28], data[30], data[31], data[32]))
        # serHead.write(pack('>BB', StormBreakerType.StormBreakerHead, StormBreakerLength.head))
        print("Head Data: ")
        print(data[24])
        # serHead.write(pack('B', StormBreakerLength.head))
        # serHead.write(pack('B', data[0]))
        # serHead.write(pack('>B', data[3]))
        # serHead.write(pack('>B', data[5]))
        # serHead.write(pack('>B', data[35]))
        # serHead.write(pack('>B', data[38]))
        # serHead.write(pack('>B', data[39]))
        # serHead.write(data[0])
        # serHead.write(data[3])
        # serHead.write(data[5])
        # serHead.write(data[35])
        # serHead.write(data[38:39])
        # serHead.write(data[20:24])
        # serHead.write(pack('>B', data[27]))
        # serHead.write(pack('>B', data[28]))
        # serHead.write(data[27:28])
        # serHead.write(pack('>B', data[30]))
        # serHead.write(pack('>B', data[31]))
        # serHead.write(pack('>B', data[32]))
        # serHead.write(data[30:32])
        time.sleep(0.2)
        
    if body == True:
        print("Sending body frame")
        # serBody.write(pack('>BBBBBBB', StormBreakerType.StormBreakerBody,StormBreakerLength.body, data[24], data[25], data[29], data[31], data[32]))
        serBody.write(pack('>BB', StormBreakerType.StormBreakerBody,StormBreakerLength.body))
        send_data = arr.array('B', [data[24], data[25], data[29], data[31], data[32]])
        send_data[0] = data[24]
        send_data[1] = data[25]
        send_data[2] = data[29]
        send_data[3] = data[31]
        send_data[4] = data[32]
        serBody.write(send_data[0:4])
        print("header")
        # serBody.write(pack('>B', StormBreakerLength.body))
        print("body")
        # serBody.write(data[25:26])
        # serBody.write(pack('>B', data[24]))
        # serBody.write(pack('>B', data[25]))
        # serBody.write(pack('>B', data[24]))
        # serBody.write(pack('>B', data[25]))
        # serBody.write(data[24:25])
        # serBody.write(data[29])
        # serBody.write(data[31])
        # serBody.write(data[32])
        # serBody.write(pack('>B', data[29]))
        # serBody.write(pack('>B', data[31]))
        # serBody.write(pack('>B', data[32]))
        time.sleep(0.5)
        

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
