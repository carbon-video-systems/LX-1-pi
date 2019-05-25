from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

import calibration as calib
import ArtNet as artnet

def find_drive():
    # Find a connected ODrive (this will block until you connect one)
    print("finding an odrive...")
    found_drive = odrive.find_any()
    # Find an ODrive that is connected on the serial port /dev/ttyUSB0
    #my_drive = odrive.find_any("serial:/dev/ttyUSB0")
    return found_drive

def isNaN(num):
    return num != num

# Finding drive
def main():
    my_drive = find_drive()
    calib.startup_sequence(my_drive)

    print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")
    old_data = artnet.receive_artnet_packets()

    while True:
        data = artnet.receive_artnet_packets()
        if data == None:
            data = old_data
        else:
            old_data = data
        print(data[24], data[72])
        my_drive.axis0.controller.pos_setpoint = 256 * data[24]
        my_drive.axis1.controller.pos_setpoint = 256 * data[72]

if __name__== '__main__':
    main()


# Or to change a value, just assign to the property
# my_drive.axis1.controller.pos_setpoint = 10000
# print("Position setpoint is " + str(my_drive.axis1.controller.pos_setpoint))

# And this is how function calls are done:
# for i in [1,2,3,4]:
#     print('voltage on GPIO{} is {} Volt'.format(i, my_drive.get_adc_voltage(i)))
    