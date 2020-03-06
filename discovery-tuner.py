#!/usr/bin/python

import struct
import binhex
import math
import time
import random
import vlc
from gpiozero import LED

#vlc states
NothingSpecial=0
Opening=1
Buffering=2
Playing=3
Paused=4
Stopped=5
Ended=6

mouse_speed = 0.5

zone_size=50
canvas_dimensions=(800,600)
zones=[]
position_y = canvas_dimensions[0]/2 
position_x = canvas_dimensions[1]/2

light = LED(21)

#test relay
light.on()
time.sleep(10)
light.off()
time.sleep(10)

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
instances=[]
for url in radiourl:
    instances.append(vlc.Instance('--input-repeat=-1'))

players=[]
media=[]
index=0
fo
    players.append(instance.media_player_new())
    media.append(instance.media_new(radiourl[index]))
    index=index+1

index=0
for player in players:
    player.set_media(media[index])
    index=index+1

#mouse
def read_mouse():
    f=open("/dev/input/mice", "rb" )
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
    position_x = position_x+(int(0.5*x))
    position_y = position_y+(int(0.5*y))
    if position_x < 0:
        position_x = canvas_dimensions[0]
    if position_x > canvas_dimensions[0]:
        position_x = 0
    if position_y < 0:
        position_y = canvas_dimensions[1]
    if position_y > canvas_dimensions[1]:
        position_y = 0
    print(str(position_x)+" , "+str(position_y)) 

    index=0
    for x in zones:
        c = math.sqrt((x.x-position_x)*(x.x-position_x) + (x.y-position_y)*(x.y-position_y))
        if c <= zone_size:
            p = c/zone_size*100
            p = int(100-p)
            players[index].audio_set_volume(p)
            print("--zone-- "+str(index)+" active at "+str(p)+" %")
            if players[index].get_state() != Playing:
                #print("playing...")
                players[index].play()
                pState = 0
                cState = players[index].get_state()
                while cState != Playing:
                    cState = players[index].get_state()
                    if cState != pState:
                        print(cState)
                    pState = cState
                    #add timeout
        else:
            players[index].stop()
        index=index+1
