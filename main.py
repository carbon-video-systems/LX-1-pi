from __future__ import print_function

import time
import math
from enum import Enum

import ArtNet as artnet
import StormBreakerSerial as stormbreaker

class SystemConnection:
    Head = True
    Body = False

def isNaN(num):
    return num != num

# Finding drive
def main():

    old_data = artnet.receive_artnet_packets()

    while True:
        data = artnet.receive_artnet_packets()

        if data == None:
            data = old_data
        else:
            old_data = data
            print(data[24], data[72])
            stormbreaker.send_stormbreaker(data, SystemConnection.Body, SystemConnection.Head)
            # send new data to arduino

        stormbreaker.receive_stormbreaker(SystemConnection.Body, SystemConnection.Head)
        # Check for serial available
        

if __name__== '__main__':
    main()
