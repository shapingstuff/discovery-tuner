#!/usr/bin/python

import struct
import binhex
import math
import time
import random

#radio stations
radiourl = [
    'http://ice6.somafm.com/groovesalad-16-aac',
    'http://ice2.somafm.com/dronezone-32-aac',
    'http://ice2.somafm.com/indiepop-32-aac',
    'http://ice2.somafm.com/spacestation-32-aac',
    'http://ice2.somafm.com/secretagent-32-aac',
    'http://ice2.somafm.com/lush-32-aac',
    'http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-eieuk',
    ]

def read_mouse():
    f = open( "/dev/input/mice", "rb" )
    while 1:
        data = f.read(3)  # Reads the 3 bytes
        identity,x,y = struct.unpack('3b',data)  #Unpacks the bytes to integers
        return x,y
                
# creates circular zones
class Zone:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

zone_size=50
canvas_dimensions=(800,600)
zones=[]

while True:
    x,y = read_mouse()
    print(str(x)+" , "+str(y))
