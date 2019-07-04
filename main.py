"""LX-1 Main

This script controls the flow of receiving ArtNet packets and the application
of the StormBreaker communication protocol.

This script requires at least one active Serial port connected to a USB port.
This script requires a connected Artnet broadcast to the ethernet socket.

This file could be imported as a module and contains the following classes:

    * SystemConnection
    * TeensyConnection

and the following functions outside of classes:

    * main
"""
from __future__ import print_function

import time
import math
from enum import Enum, IntEnum

import StormBreakerSerial as storm
import ArtNet as artnet

# Selects if debugging print statements are output
class options:
    """Sets debugging print statements"""
    testing = True
    debugging = False

# Selects if the head and/or the body are connected
class SystemConnection:
    """Declares which modules are connected"""
    head = True
    body = True

class TeensyConnection(IntEnum):
    """Number of teensy microcontrollers connected to the system"""
    numTeensy = 1

# main function
def main():
    """Main function"""
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
    if SystemConnection.head == True and SystemConnection.body == True and TeensyConnection.numTeensy == 2:
        time.sleep(5)
        # TODO CHECK THIS ERROR??
        # storm.StormBreaker.identify()  #this currently throws an error when commented in

    # main program loop
    while True:
        # Receive new artnet data
        data = artnet.receive_artnet_packets()

        # Updates StormBreaker protocol with new data
        if data == None:
            data = old_data
        else:
            old_data = data
            # function sends data to the stormbreaker structure
            storm.StormBreaker.send(data, SystemConnection.body, SystemConnection.head)

        # Checks for incoming serial messages from Teensy
        storm.StormBreaker.receive(SystemConnection.body, SystemConnection.head)
        # time.sleep(0.05)


if __name__== '__main__':
    """Sets main as the top level function"""
    main()


# def isNaN(num):
#     return num != num
