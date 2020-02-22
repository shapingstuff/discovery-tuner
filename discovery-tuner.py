#!/usr/bin/python

import struct
import binhex
import math
import time
import random
import vlc

zone_size=50
canvas_dimensions=(800,600)
zones=[]
position_y = canvas_dimensions[0]/2 
position_x = canvas_dimensions[1]/2

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

#vlc
instance=vlc.Instance('--input-repeat=-1')
players = []
for x in radiourl:
    players.append(instance.media_player_new())

#set all players to off
play =[]
for x in radiourl:
    play.append(0)

f = open("/dev/input/mice", "rb" )

def read_mouse():
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

#create zones for each url added
for x in radiourl:
    rndCor = (random.randint(zone_size/2, canvas_dimensions[0]), random.randint(zone_size/2, canvas_dimensions[1]))
    zones.append(Zone(rndCor[0],rndCor[1],zone_size))

while True:
    x,y = read_mouse()
    #print(str(x)+" , "+str(y))
    position_x = position_x+x
    position_y = position_y+y
    if position_x < 0:
        position_x = canvas_dimensions[0]
    if position_x > canvas_dimensions[0]:
        position_x = 0
    if position_y < 0:
        position_y = canvas_dimensions[1]
    if position_y > canvas_dimensions[1]:
        position_y = 0
    #print(str(position_x)+" , "+str(position_y)) 

    index=0
    for x in zones:
        c = math.sqrt((x.x-position_x)*(x.x-position_x) + (x.y-position_y)*(x.y-position_y))
        if c <= zone_size:
            p = c/zone_size*100
            p = int(100-p)
            print("--Zone-- "+str(index)+" active at "+str(p)+" %")
            #players[index].audio_set_volume(p)
            if play[index]==0:
                print("--playing-- " + str(index))
                #print(radiourl[index])
                #media=instance.media_new(radiourl[index])
                #Set player media
                #players[index].set_media(media)
                #Play the media
                #print("Playing")
                #players[index].play()
                play[index]=1
        else:
            print("--stopping--" + str(index))
            play[index]=0
            #players[index].stop()
        print(str(index))
        index = index+1
