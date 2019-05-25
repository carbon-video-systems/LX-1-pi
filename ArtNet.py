import sys

from socket import (socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR,
                    SO_BROADCAST)
from struct import pack, unpack


UDP_IP = ""
UDP_PORT = 6454

BROADCAST_PORT = 7788


class ArtnetPacket:

    ARTNET_HEADER = b'Art-Net\x00'

    def __init__(self):
        self.op_code = None
        self.ver = None
        self.sequence = None
        self.physical = None
        self.universe = None
        self.length = None
        self.data = None

    def __str__(self):
        return ("ArtNet package:\n - op_code: {0}\n - version: {1}\n - "
                "sequence: {2}\n - physical: {3}\n - universe: {4}\n - "
                "length: {5}\n - data : {6}").format(
            self.op_code, self.ver, self.sequence, self.physical,
            self.universe, self.length, self.data)

    def unpack_raw_artnet_packet(raw_data):

     

        if unpack('!8s', raw_data[:8])[0] != ArtnetPacket.ARTNET_HEADER:
            print("Received a non Art-Net packet")
            return None
        ##print("-----------")
        op=unpack('!B',raw_data[9:10])
        ##print(op)
        ##print("-----------")

        if op[0]==32 or op[0] == 33:
            #print("Recieved Artnet Poll")
            return None

        
        packet = ArtnetPacket()
        (packet.op_code, packet.ver, packet.sequence, packet.physical,
            packet.universe, packet.length) = unpack('!HHBBHH', raw_data[8:18])

        packet.data = unpack(
            '{0}s'.format(int(packet.length)),
            raw_data[18:18+int(packet.length)])[0]

        return packet


def receive_artnet_packets():
    sock = socket(AF_INET, SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    data, addr = sock.recvfrom(1024)
    packet = ArtnetPacket.unpack_raw_artnet_packet(data)
    if packet == None:
        pass
    else:
        return packet.data