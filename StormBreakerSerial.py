"""StormBreaker Serial Communications Protocol and Framework

This script packages received and parsed ArtNet data into data packages that
are ready to be sent to connected microcontrollers.

This script requires at least one active Serial port connected to a USB port.

This file should be imported as a module and contains the following classes:

    * StormBreaker

and the following functions outside of classes:

    * receive_ident
    * receive_serials
    * flush_buffer
"""
import sys
import serial
import time
from struct import pack, unpack
from enum import IntEnum
import array as arr
import main as top


# initializes USB serial ports for communication with the Teensy
# serBody = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)

if top.TeensyConnection.numTeensy == 1:
    try:
        if top.options.testing == True:
            print("serBody initialization")
        serBody = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    except:
        try:
            serBody = serial.Serial('/dev/ttyUSB1', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
            print("serial exception, trying USB1")
        except:
            if top.options.testing == True:
                print("DOUBLE serial exception")

    try:
        serHead = serBody
    except:
        if top.options.testing == True:
            print("both serial ports disconnected")
        while True:
            if top.options.testing == True:
                print("SYS ERROR")
            time.sleep(2)

elif top.TeensyConnection.numTeensy == 2:
    try:
        if top.options.testing == True:
            print("serBody initialization")
        serBody = serial.Serial('/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    except:
        if top.options.testing == True:
            print("ONE TEENSY NOT CONNECTED - check numTeensys")
    try:
        if top.options.testing == True:
            print("serHead initialization")
        serHead = serial.Serial('/dev/ttyUSB1', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    except:
        if top.options.testing == True:
            print("SECOND TEENSY NOT CONNECTED - check numTeensys")

else:
    if top.options.testing == True:
        print("NO TEENSYS CONNECTED - CHECK NUMTEENSYS")

class StormBreaker:
    """StormBreaker Protocol"""
    class MsgType(IntEnum):
        """Header enumeration for different messages"""
        StormError = -2
        StormWarning = -1
        StormOK = 0
        StormBody = 1
        StormHead = 2
        StormIdent = 99

    class MsgLength(IntEnum):
        """Length of the StormBreaker payload"""
        ident = 0
        body = 5
        head = 11

    class Ident(IntEnum):
        """System identification message"""
        body = 0xAF
        head = 0x50
        both_for_testing = 0xB7

    # def unpack_storm()
    class Headers():
        """Packs the StormBreaker header with relevent information"""
        def body():
            return pack('>BB', StormBreaker.MsgType.StormBody, StormBreaker.MsgLength.body)

        def head():
            return pack('>BB', StormBreaker.MsgType.StormHead, StormBreaker.MsgLength.head)

        def ident():
            return pack('>BB', StormBreaker.MsgType.StormIdent, StormBreaker.MsgLength.ident)

        def pack_header(message_type):
            """Packages two bytes in the format of a StormBreaker Header

            Parameters
            ----------
            message_type : int
                Create a StormBreaker header of this msg type

            Returns
            -------
            bytes object
                2 byte packaged header, ready to send
            """
            header = {
                StormBreaker.MsgType.StormBody: StormBreaker.Headers.body,
                StormBreaker.MsgType.StormHead: StormBreaker.Headers.head,
                StormBreaker.MsgType.StormIdent: StormBreaker.Headers.ident
            }
            retrieve_header = header.get(message_type, lambda: "INVALID MESSAGE")
            return retrieve_header()

    def identify():
        """Identifies connected Teensys as body or head units"""
        global serBody, serHead

        ident_message = StormBreaker.Headers.pack_header(StormBreaker.MsgType.StormIdent)
        serBody.write(ident_message)
        time.sleep(0.1)
        check1 = receive_ident(True)

        # Send ident to head
        serHead.write(ident_message)
        time.sleep(0.1)
        check2 = receive_ident(False)

        if top.options.testing == True:
            print("check1 = ")
            print(check1)
            print("check2 = ")
            print(check2)

        if check1 == False and check2 == False:
            serBuff = serBody
            serBody = serHead
            serHead = serBuff

        if check1 == None or check2 == None:
            if top.options.testing == True:
                print("Identity check failed")

    def send(data, body, head):
        """Sends the StormBreaker package to destination microcontrollers"""
        if head == True:
            if top.options.debugging == True:
                print("Sending head frame")

            # change these variables to change packet data
            strobe_shutter = 0
            iris = data[26]
            zoom = 0
            focus = 0
            tilt = (data[24] << 8) | data[25]
            tilt_control = 1
            pan_tilt_speed = 0
            power_special_functions = 0

            # according to LX1 DMX spec:
            # strobe_shutter = data[0]
            # iris = data[20]
            # zoom = (data[21] << 8) | data[22]
            # focus = (data[23] << 8) | data[24]
            # tilt = (data[27] << 8) | data[28]
            # tilt_control = data[30]
            # pan_tilt_speed = data[31]
            # power_special_functions = data[32]

            serHead.write(StormBreaker.Headers.pack_header(StormBreaker.MsgType.StormHead))
            serHead.write(pack('>B', strobe_shutter))
            serHead.write(pack('>B', iris))
            serHead.write(pack('>B', zoom >> 8))
            serHead.write(pack('>B', zoom & 0xFF))
            serHead.write(pack('>B', focus >> 8))
            serHead.write(pack('>B', focus & 0xFF))
            serHead.write(pack('>B', tilt >> 8))
            serHead.write(pack('>B', tilt & 0xFF))
            serHead.write(pack('>B', tilt_control))
            serHead.write(pack('>B', pan_tilt_speed))
            serHead.write(pack('>B', power_special_functions))

            if top.options.debugging == True:
                print("Head Data: ")
                print(strobe_shutter)
                print(iris)
                print(zoom)
                print(focus)
                print(tilt)
                print(tilt_control)
                print(pan_tilt_speed)
                print(power_special_functions)

        if body == True:
            if top.options.debugging == True:
                print("Sending body frame")

            # change these variables to change packet data
            pan = (data[19] << 8) | data[20]    # 0 - 65535
            pan_control = 0                     # 0 - 255
            pan_tilt_speed = data[26]                  # 0 - 255
            power_special_functions = 0         # 0 - 255

            # according to LX1 DMX spec:
            # pan = (data[25] << 8) | data[26]
            # pan_control = data[29]
            # pan_tilt_speed = data[31]
            # power_special_functions = data[32]

            serBody.write(StormBreaker.Headers.pack_header(StormBreaker.MsgType.StormBody))
            serBody.write(pack('>B', pan >> 8))
            serBody.write(pack('>B', pan & 0xFF))
            serBody.write(pack('>B', pan_control))
            serBody.write(pack('>B', pan_tilt_speed))
            serBody.write(pack('>B', power_special_functions))

            if top.options.debugging == True:
                print("Body Data: ")
                print(pan)
                print(pan_control)
                print(pan_tilt_speed)
                print(power_special_functions)


    def receive(body, head):
        """Receives StormBreaker messages from connected microcontrollers"""
        if head == True:
            while serHead.in_waiting > 0:
                while serHead.in_waiting > 0:
                    line = serHead.readline().strip()
                    if top.options.testing == True:
                        print(line)
                time.sleep(0.01)

        if body == True:
            while serBody.in_waiting > 0:
                while serBody.in_waiting > 0:
                    line = serBody.readline().strip
                    if top.options.testing == True:
                        print(line)
                time.sleep(0.01)

def receive_ident(body):
    if body == True:
        while serBody.in_waiting == 0:
            time.sleep(0.01)
        line = serBody.readline().strip()
        if top.options.testing == True:
            print(line)
        if line == pack('>B', StormBreaker.Ident.body):
            return True
        elif line == pack('>B', StormBreaker.Ident.head):
            return False
        else:
            return None

    else:
        while serHead.in_waiting == 0:
            time.sleep(0.01)
        line = serHead.readline().strip()
        if top.options.testing == True:
            print(line)
        if line == pack('>B', StormBreaker.Ident.head):
            return True
        elif line == pack('>B', StormBreaker.Ident.body):
            return False
        else:
            return None

def receive_serials():
    while serBody.in_waiting > 0:
        while serBody.in_waiting > 0:
            line = serBody.readline()
            if top.options.testing == True:
                print(line)
        time.sleep(0.01)

    while serHead.in_waiting > 0:
        while serHead.in_waiting > 0:
            line = serHead.readline()
            if top.options.testing == True:
                print(line)
        time.sleep(0.01)

def flush_buffer():
    serBody.reset_input_buffer()
    serHead.reset_input_buffer()
    serBody.reset_output_buffer()
    serHead.reset_output_buffer()
    time.sleep(0.1)
