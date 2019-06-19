from __future__ import print_function

import time
import math
from enum import Enum, IntEnum

import StormBreakerSerial as storm
import ArtNet as artnet

# Selects if the head and/or the body are connected
class SystemConnection:
    head = True
    body = True

class TeensyConnection(IntEnum):
    numTeensy = 1

# main function
def main():
    
    # initializes receive array and flushes serial ports
    time.sleep(0.5)

    old_data = artnet.receive_artnet_packets()

    if old_data == None:
        while old_data == None:
            old_data = artnet.receive_artnet_packets()
    
    storm.receive_serials()
    time.sleep(0.5)
    storm.flush_buffer()
    time.sleep(0.5)

    # identify the Teensys that are connected
    if SystemConnection.head == True and SystemConnection.body == True:
        time.sleep(5)
        #storm.StormBreaker.identify()  #this currently throws an error when commented in
    
    # main program loop
    while True:
        # Receive new artnet data
        data = artnet.receive_artnet_packets()
        
        # Updates StormBreaker protocol with new data
        if data == None:
            data = old_data
        else:
            old_data = data
            print(data[24], data[25])
            # function sends data to the stormbreaker structure
            storm.StormBreaker.send(data, SystemConnection.body, SystemConnection.head)

        # Checks for incoming serial messages from Teensy
        storm.StormBreaker.receive(SystemConnection.body, SystemConnection.head)
        time.sleep(0.1)
        

if __name__== '__main__':
    main()


# def isNaN(num):
#     return num != num