from __future__ import print_function

import time
import math

import ArtNet as artnet
import SerialLink as serial

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

if __name__== '__main__':
    main()
