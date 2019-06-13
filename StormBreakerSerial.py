
import sys
import serial
import time
from struct import pack, unpack
from enum import IntEnum
import array as arr
import main as top

# initializes USB serial ports for communication with the Teensy
if top.TeensyConnection.numTeensy == 1:
    try:
        print("serBody initialization")
        serBody = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    except:
        try:
            serBody = serial.Serial('/dev/ttyUSB1', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
            print("serial exception, trying USB1")
        except:
            print("DOUBLE serial exception")

    try:
        serHead = serBody
    except:
        print("both serial ports disconnected")
        while True:
            print("SYS ERROR")
            time.sleep(2)

elif top.TeensyConnection.numTeensy == 2:
    try:
        print("serBody initialization")
        serBody = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    except:
        print("ONE TEENSY NOT CONNECTED - check numTeensys")
    try:
        print("serHead initialization")
        serHead = serial.Serial('/dev/ttyUSB1', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    except:
        print("SECOND TEENSY NOT CONNECTED - check numTeensys")

else:
    print("NO TEENSYS CONNECTED - CHECK NUMTEENSYS")


class StormBreaker:
    
    # def __init__(self):
    #     self.message_type = None
    #     self.length = None
    #     # self.data = None
        
    # def __str__(self):
    #     return ("StormBreaker package:\n - message_type: {0}\n - length: {1}\n - "
    #             "data: {2}").format(self.message_type, self.length, self.data)

    class MsgType(IntEnum):
        StormError = -2
        StormWarning = -1
        StormOK = 0
        StormBody = 1
        StormHead = 2
        StormIdent = 99

    class MsgLength(IntEnum):
        ident = 0
        body = 5
        head = 11

    class Ident(IntEnum):
        body = 0xAF
        head = 0x50

    def identify():
        # Send ident to body
        serBody.write(pack('>BB', StormBreaker.MsgType.StormIdent, StormBreaker.MsgLength.ident))
        time.sleep(0.1)
        check1 = receive_ident(True)
        # Receive from body

        # Send ident to head
        serHead.write(pack('>BB', StormBreaker.MsgType.StormIdent, StormBreaker.MsgLength.ident))
        time.sleep(0.1)
        check2 = receive_ident(False)
        
        print("check1 = ")
        print(check1)
        print("check2 = ")
        print(check2)

        if check1 == False and check2 == False:
            serBuff = serBody
            serBody = serHead
            serHead = serBuff
        
        if check1 == None or check2 == None:
            print("Identity check failed")

    def send(data, body, head):
        if head == True:
            print("Sending head frame")
            serHead.write(pack('>BBBBBBBBBBBBB', StormBreaker.MsgType.StormHead, StormBreaker.MsgLength.head, data[24], data[24], data[25], data[26], data[27], data[34], data[58], data[59], data[60], data[61], data[126]))
            print("Head Data: ")
            print(data[24])
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
            serBody.write(pack('>BB', StormBreaker.MsgType.StormBody,StormBreaker.MsgLength.body))
            serBody.write(pack('>B', 0))
            serBody.write(pack('>B', 0))
            serBody.write(pack('>B', 255))
            serBody.write(pack('>B', data[10]))
            serBody.write(pack('>B', data[9]))
            print("0")
            print("0")
            print("127")
            print(data[10])
            print(data[9])
            time.sleep(0.25)
            

    def receive(body, head):
        if head == True:
            while serHead.in_waiting > 0:
                while serHead.in_waiting > 0:
                    line = serHead.readline()
                    print(line)
                    # print(line.decode("utf-8"))
                time.sleep(0.05)
        
        if body == True:
            while serBody.in_waiting > 0:
                while serBody.in_waiting > 0:
                    line = serBody.readline()
                    print(line)
                    # print(line.decode("utf-8"))
                time.sleep(0.05)

def receive_ident(body):
    if body == True:
        while serBody.in_waiting == 0:
            time.sleep(0.1)
        check = int(serBody.readline().strip())
        print(check)
        if check == StormBreaker.Ident.body:
            return True
        elif check == StormBreaker.Ident.head:
            return False
        else:
            return None
    
    else:
        while serHead.in_waiting == 0:
            time.sleep(0.1)
        check = int(serBody.readline().strip())
        print(check)
        if check == StormBreaker.Ident.head:
            return True
        elif check == StormBreaker.Ident.body:
            return False
        else:
            return None

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

def flush_buffer():
    serBody.reset_input_buffer()
    serHead.reset_input_buffer()
    time.sleep(0.25)
    serBody.reset_output_buffer()
    serHead.reset_output_buffer()
    time.sleep(0.25)