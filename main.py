from __future__ import print_function

import time
import math
from enum import Enum

import ArtNet as artnet
import StormBreakerSerial as stormbreaker

# Selects if the head and/or the body are connected
class SystemConnection:
    head = True
    body = True

def isNaN(num):
    return num != num

# main function
def main():
    
    # initializes receive array and flushes serial ports
    time.sleep(0.2)

    old_data = artnet.receive_artnet_packets()

    if old_data == None:
        while old_data == None:
            old_data = artnet.receive_artnet_packets()
    
    stormbreaker.receive_serials()
    time.sleep(0.25)
    stormbreaker.flush_buffer()
    time.sleep(0.25)

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
            stormbreaker.send_stormbreaker(data, SystemConnection.body, SystemConnection.head)

        # Checks for incoming serial messages from Teensy
        stormbreaker.receive_stormbreaker(SystemConnection.body, SystemConnection.head)
        time.sleep(0.1)
        

if __name__== '__main__':
    main()
