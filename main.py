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
    LX1 = True

# Selects if the head and/or the body are connected
class SystemConnection:
    """Declares which modules are connected"""
    head = False
    body = True

class TeensyConnection(IntEnum):
    """Number of teensy microcontrollers connected to the system"""
    numTeensy = 1

# main function
def main():
    """Main function"""
    # initializes receive array and flushes serial ports
    time.sleep(0.1)

    storm.receive_serials()
    storm.flush_buffer()

    # identify the Teensys that are connected
    if SystemConnection.head == True and SystemConnection.body == True and TeensyConnection.numTeensy == 2:
        storm.StormBreaker.identify()

    # Initializes data with received artnet
    while True:
        old_data = artnet.receive_artnet_packets()
        if old_data != None:
            break

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


if __name__== '__main__':
    """Sets main as the top level function"""
    main()
