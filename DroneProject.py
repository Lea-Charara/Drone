"""
tellopy sample using keyboard and video player

Requires mplayer to record/save video.


Controls:
- tab to lift off
- WASD to move the drone
- space/shift to ascend/descent slowly
- Q/E to yaw slowly
- arrow keys to ascend, descend, or yaw quickly
- backspace to land, or P to palm-land
- enter to take a picture
- R to start recording video, R again to stop recording
(video and photos will be saved to a timestamped file in ~/Pictures/)
- Z to toggle camera zoom state
(zoomed-in widescreen or high FOV 4:3)
"""

import time
import imagerecognition as ir
from pathlib import Path
from pathlib import Path
import sys
import tellopy
import pygame
import pygame.display
import pygame.key
import pygame.locals
import pygame.font
import os
import datetime
from subprocess import Popen, PIPE
import Spots


prev_flight_data = None
video_player = None
video_recorder = None
font = None
wid = None
date_fmt = '%Y-%m-%d_%H%M%S'
picpath = None
picnb = None



def toggle_recording(drone, speed):
    global video_recorder
    global date_fmt
    if speed == 0:
        return

    if video_recorder:
        # already recording, so stop
        video_recorder.stdin.close()
        status_print('Video saved to %s' % video_recorder.video_filename)
        video_recorder = None
        return

    # start a new recording
    filename = '%s/Pictures/tello-%s.mp4' % (os.getenv('HOME'),
                                                datetime.datetime.now().strftime(date_fmt))
    video_recorder = Popen([
                        'mencoder', '-', '-vc', 'x264', '-fps', '30', '-ovc', 'copy',
                        '-of', 'lavf', '-lavfopts', 'format=mp4',
                        # '-ffourcc', 'avc1',
                        # '-really-quiet',
                        '-o', filename,
                        ], stdin=PIPE)
    video_recorder.video_filename = filename
    status_print('Recording video to %s' % filename)

def take_picture(drone, speed):
    if speed == 0:
        return
    print('took picture')
    drone.take_picture()

def palm_land(drone, speed):
    if speed == 0:
        return
    drone.palm_land()

def toggle_zoom(drone, speed):
# In "video" mode the drone sends 1280x720 frames.
# In "photo" mode it sends 2592x1936 (952x720) frames.
# The video will always be centered in the window.
# In photo mode, if we keep the window at 1280x720 that gives us ~160px on
# each side for status information, which is ample.
# Video mode is harder because then we need to abandon the 16:9 display size
# if we want to put the HUD next to the video.
    if speed == 0:
        return
    drone.set_video_mode(not drone.zoom)
    pygame.display.get_surface().fill((0,0,0))
    pygame.display.flip()

controls = {
'w': 'forward',
's': 'backward',
'a': 'left',
'd': 'right',
'space': 'up',
'left shift': 'down',
'right shift': 'down',
'q': 'counter_clockwise',
'e': 'clockwise',
# arrow keys for fast turns and altitude adjustments
'left': lambda drone, speed: drone.counter_clockwise(speed*2),
'right': lambda drone, speed: drone.clockwise(speed*2),
'up': lambda drone, speed: drone.up(speed*2),
'down': lambda drone, speed: drone.down(speed*2),
'tab': lambda drone, speed: drone.takeoff(),
'backspace': lambda drone, speed: drone.land(),
'takeoff': lambda drone, speed: drone.takeoff(),
'land': lambda drone, speed: drone.land(),
'p': palm_land,
'r': toggle_recording,
'z': toggle_zoom,
'enter': take_picture,
'takepicture': take_picture,
'return': take_picture,
}

class FlightDataDisplay(object):
    # previous flight data value and surface to overlay
    _value = None
    _surface = None
    # function (drone, data) => new value
    # default is lambda drone,data: getattr(data, self._key)
    _update = None
    def __init__(self, key, format, colour=(255,255,255), update=None):
        self._key = key
        self._format = format
        self._colour = colour
        
        if update:
            self._update = update
        else:
            self._update = lambda drone,data: getattr(data, self._key)

    def update(self, drone, data):
        new_value = self._update(drone, data)
        if self._value != new_value:
            self._value = new_value
            self._surface = font.render(self._format % (new_value,), True, self._colour)
            return self._surface

def flight_data_mode(drone, *args):
    return (drone.zoom and "VID" or "PIC")

def flight_data_recording(*args):
    return (video_recorder and "REC 00:00" or "")

def update_hud(hud, drone, flight_data):
    (w,h) = (158,0) # width available on side of screen in 4:3 mode
    blits = []
    for element in hud:
        surface = element.update(drone, flight_data)
        if surface is None:
            continue
        blits += [(surface, (0, h))]
        # w = max(w, surface.get_width())
        h += surface.get_height()
    h += 64  # add some padding
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0,0,0)) # remove for mplayer overlay mode
    for blit in blits:
        overlay.blit(*blit)
    pygame.display.get_surface().blit(overlay, (0,0))
    pygame.display.update(overlay.get_rect())

def status_print(text):
    pygame.display.set_caption(text)

hud = [
    FlightDataDisplay('height', 'ALT %3d'),
    FlightDataDisplay('ground_speed', 'SPD %3d'),
    FlightDataDisplay('battery_percentage', 'BAT %3d%%'),
    FlightDataDisplay('wifi_strength', 'NET %3d%%'),
    FlightDataDisplay(None, 'CAM %s', update=flight_data_mode),
    FlightDataDisplay(None, '%s', colour=(255, 0, 0), update=flight_data_recording),
    ]

def flightDataHandler(event, sender, data):
    global prev_flight_data
    text = str(data)
    if prev_flight_data != text:
        update_hud(hud, sender, data)
        prev_flight_data = text

def videoFrameHandler(event, sender, data):
    global video_player
    global video_recorder
    if video_player is None:
        cmd = [ 'mplayer', '-fps', '35', '-really-quiet' ]
        if wid is not None:
            cmd = cmd + [ '-wid', str(wid) ]
        video_player = Popen(cmd + ['-'], stdin=PIPE)

    try:
        video_player.stdin.write(data)
    except IOError as err:
        status_print(str(err))
        video_player = None

    try:
        if video_recorder:
            video_recorder.stdin.write(data)
    except IOError as err:
        status_print(str(err))
        video_recorder = None

def handleFileReceived(event, sender, data):
    global date_fmt
    global picnb 
    picnb = 0 
    print('Handling file')
    
    dir = picpath+"/pic"+str(picnb)+".png"
    picnb+=1

    print(picnb)
    with open(dir, 'wb') as fd:
        fd.write(data)
        status_print('Saved photo to %s' % dir)

def WritePath(path):
    pygame.init()
    pygame.display.set_caption('Parking Detector')
    pygame.display.init()
    pygame.display.set_mode((250, 250))
    pygame.font.init()

    global font
    font = pygame.font.SysFont("dejavusansmono", 32)

    global wid
    if 'window' in pygame.display.get_wm_info():
        wid = pygame.display.get_wm_info()['window']
    print("Tello video WID:", wid)

    drone = tellopy.Tello()
    drone.connect()
    drone.start_video()
    drone.subscribe(drone.EVENT_FLIGHT_DATA, flightDataHandler)
    drone.subscribe(drone.EVENT_VIDEO_FRAME, videoFrameHandler)
    drone.subscribe(drone.EVENT_FILE_RECEIVED, handleFileReceived)
    speed = 30

    file = open(path,"w+")
    start = 0
    end = 0
    keyused = 'none';

    try:
        while 1:
            time.sleep(0.01)  # loop with pygame.event.get() is too mush tight w/o some sleep
            for e in pygame.event.get():
                # WASD for movement
                if e.type == pygame.locals.KEYDOWN:
                    start = time.time()
                    print('+' + pygame.key.name(e.key))
                    keyname = pygame.key.name(e.key)
                    
                    if keyname == 'escape':
                        #YOU CAN ADD THE ASKING PART HERE
                        file.write("end")
                        file.close()
                        print('Shutting down connection to drone...')
                        if video_recorder:
                            toggle_recording(drone, 1)
                        drone.quit()
                        exit(1)
                    
                    
                    
                    if keyname in controls:
                        key_handler = controls[keyname]
                        keyused = key_handler
                        if type(key_handler) == str:
                            getattr(drone, key_handler)(speed)
                        else:
                            key_handler(drone, speed)
        
        
                elif e.type == pygame.locals.KEYUP:
                    end = time.time()
                    
                    print('-' + pygame.key.name(e.key))
                    keyname = pygame.key.name(e.key)
                    if keyname in controls:
                            
                        key_handler = controls[keyname]
                            
                        if type(key_handler) == str:
                            file.write(keyused+ " " + str((end - start))+"\r\n")
                            getattr(drone, key_handler)(0)
                        

                        else:
                            if(keyname == 'backspace'):
                                file.write('land \r\n')
                            
                            elif(keyname == 'tab'):
                                file.write('takeoff \r\n')
                                
                            elif(keyname == 'return'):
                                    file.write('takepicture \r\n')
                            key_handler(drone, 0)

                                

                
    except e:
        print(str(e))
    finally:
        file.close()
        print('Shutting down connection to drone...')
        if video_recorder:
            toggle_recording(drone, 1)
        drone.quit()
        exit(1)

def ReadPath(path):
    

    # ASK THE MAX PARKING SPOTS
    Spots.show()
 ###################################################################

    global picnb
    
    pygame.init()
    surface = pygame.image.load("Icon.png")
    pygame.display.set_icon(surface)
    pygame.display.set_caption('Parking Detector')
    pygame.display.init()
    pygame.display.set_mode((250, 250))
    pygame.font.init()
    
    global font
    font = pygame.font.SysFont("dejavusansmono", 32)
    
    global wid
    if 'window' in pygame.display.get_wm_info():
        wid = pygame.display.get_wm_info()['window']
    print("Tello video WID:", wid)


    drone = tellopy.Tello()
    drone.connect()
    drone.start_video()
    drone.subscribe(drone.EVENT_FLIGHT_DATA, flightDataHandler)
    drone.subscribe(drone.EVENT_VIDEO_FRAME, videoFrameHandler)
    drone.subscribe(drone.EVENT_FILE_RECEIVED, handleFileReceived)
    speed = 30
    global picpath
    
    #CREATE THE PICTURES FILE
    parent = Path(path).parent
    if not os.path.exists(str(parent)+"/pictures"):
        os.makedirs(str(parent)+"/pictures")
    picpath = str(parent)+"/pictures"
    print(picpath)
    
    file = open(path,"r+")
    commands = file.readlines()
    file.close()
    
    time.sleep(3)
    
    
    for command in commands:
        command = command.split()
        if len(command) == 1:
            print(command[0])
            if command[0] == 'end':
                time.sleep(2)
                cars = 0;

                print('Shutting down connection to drone...')
                if video_recorder:
                    toggle_recording(drone, 1)
                drone.quit()
                for i in range(picnb):
                    print(i)
                    cars+= ir.imagerec(picpath+"/pic"+str(i)+".png")
                    print (str(cars))
                
                
                #MESSAGE OF NB IF PARKING AVAILABLE
                Spots.resDialog(cars)
                             
                
                exit(1)
            else:
                key = controls[command[0]]
                print(str(key))
                key(drone,speed)
                time.sleep(3)
    
    
        else :
            print (command[0])
            if(command[0] == 'delay'):
                time.sleep(int(command[1]))
            else:
                timeout = float(command[1])
                start = time.time()
                print(start + timeout)
                while time.time() < start + timeout:
                    getattr(drone, command[0])(speed)
                getattr(drone, command[0])(0)
                time.sleep(2)
    



# def main():
#     ReadPath("/Users/shake9334/Desktop/DroneTest/test.txt")
# if __name__ == "__main__":
#     main()