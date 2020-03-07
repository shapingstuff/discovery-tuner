#!/usr/bin/python

radiourl = [
    'http://ice6.somafm.com/groovesalad-16-aac',
    'http://ice2.somafm.com/dronezone-32-aac',
    'http://ice2.somafm.com/indiepop-32-aac',
    'http://ice2.somafm.com/spacestation-32-aac',
    'http://ice2.somafm.com/secretagent-32-aac',
    'http://ice2.somafm.com/lush-32-aac',
    'http://ice6.somafm.com/groovesalad-16-aac',
    'http://ice2.somafm.com/dronezone-32-aac',
    'http://ice2.somafm.com/indiepop-32-aac',
    'http://ice2.somafm.com/spacestation-32-aac',
    'http://ice2.somafm.com/secretagent-32-aac',
    'http://ice2.somafm.com/lush-32-aac',
    ]

#vlc states
NothingSpecial=0
Opening=1
Buffering=2
Playing=3
Paused=4
Stopped=5
Ended=6

import struct
import binhex
import sys
import math
import vlc
import time
import random
from gpiozero import LED

width=800
height=600
mouse_speed=1 #was 0.5
t_size=50#tuned zone size
f_size=100 #fade in overlap size
mouse_speed=0.5 #mouse speed factor
circle_num=len(radiourl)
max_vol=100
mid_vol=20
min_vol=5

#starting coodrinates
position_y=height/2 
position_x=width/2

#test the light at startup
light =LED(21)
light.off()
time.sleep(1)
light.on()

class circle():
    def __init__(self, size, fade):
        self.x = random.randint(0+(t_size),width-(t_size))
        self.y = random.randint(0+(t_size),height-(t_size))
        self.r = size
        self.f = fade

#what to play as a tuple of play/stop and volume
playlist=[]
for url in radiourl:
    playlist.append((0,0))

#vlc
instances=[]
for url in radiourl:
    instances.append(vlc.Instance('--input-repeat=-1'))
players=[]
media=[]
index=0
for instance in instances:
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
        
#create non-intersecting zones that represent tuned to 100%
t_zones=[]
while len(t_zones) < circle_num:
    new = circle(t_size, f_size)
    if any(pow(c.r - new.r, 2) <=
           pow(c.x - new.x, 2) + pow(c.y - new.y, 2) <=
           pow(c.r + new.r, 2)
       for c in t_zones):
        continue
    t_zones.append(new)

for zone in t_zones:
    print(str(zone.x)+" , "+str(zone.y)+" , "+str(zone.r))

while True:
    x,y = read_mouse()
    #print(str(x)+" , "+str(y))
    position_x = position_x+(int(0.5*x))
    position_y = position_y+(int(0.5*y))
    if position_x < 0:
        position_x = width
    if position_x > width:
        position_x = 0
    if position_y < 0:
        position_y = height
    if position_y > height:
        position_y = 0
    print(str(position_x)+" , "+str(position_y)) 
    
    i=0
    for zone in t_zones:
        c=math.sqrt((zone.x-position_x)*(zone.x-position_x)+(zone.y-position_y)*(zone.y-position_y))
        if c<t_size:
            playlist[i]=(1,max_vol)
            light.off() # ON
            break
        else:
            playlist[i]=(0,0)
            light.on() # OFF
        i=i+1              
    
    s=0
    i=0
    #plays and sets the volume based on playlist
    for u in playlist:
        if u[0] is 1: #is it meant to be playing
            if players[i].get_state() != Playing:
                print("-- playing "+str(i)+" --")
                players[i].audio_set_volume(u[1])
                players[i].play()
                pState=0
                cState=players[i].get_state()
                #wait until playing
                while cState != Playing:
                    cState=players[i].get_state()
                    if cState != pState:
                        print(cState)
                    pState=cState
            else: #just set volume if already playing
                players[i].audio_set_volume(u[1])
        else: #stop if not meant to be playing
            players[i].stop()
        i=i+1
