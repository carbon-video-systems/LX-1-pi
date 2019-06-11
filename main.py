from __future__ import print_function

import time
import math
from enum import Enum

import ArtNet as artnet
import StormBreakerSerial as stormbreaker

class SystemConnection:
    head = True
    body = True

def isNaN(num):
    return num != num

# Finding drive
def main():
    
    time.sleep(0.2)
    old_data = artnet.receive_artnet_packets()
    
    stormbreaker.receive_serials()
    time.sleep(0.2)
    stormbreaker.flush_buffer()
    time.sleep(0.2)

    while True:
        data = artnet.receive_artnet_packets()

        if data == None:
            data = old_data
        else:
            old_data = data
            print(data[24], data[25])
            stormbreaker.send_stormbreaker(data, SystemConnection.body, SystemConnection.head)
            # send new data to arduino

        stormbreaker.receive_stormbreaker(SystemConnection.body, SystemConnection.head)
        # Check for serial available
        time.sleep(0.1)
        

if __name__== '__main__':
    main()
