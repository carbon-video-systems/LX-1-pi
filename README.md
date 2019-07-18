# LX-1-pi
This project aims to take ArtNet and parse it into useable data.  The data is then packaged into Carbon Video System's StormBreaker protocol.

## StormBreaker
Relevant data is taken from the ArtNet stream and passed along to their intended destinations.

## Connections
ArtNet in -> over Ethernet \
USB-FTDI based UART connection to Teensy 3.6 microcontrollers.

# Changelog
6/20/19:  Added support for 1 or 2 microcontrollers.\
6/27/19:  Added the LX1 data structure to StormBreaker. \
7/04/19:  Removed delays, added classes for debugging options. \
7/15/19:  Added support for receiving data from Teensy. \
7/17/19:  Fixed head and body system identification.

# TODO
Initialize data to 0. \
ArtNet poll callback.
