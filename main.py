import launchpad_py as LP
import json

from page import *
from key import *

from pystray import MenuItem as item
import pystray
from PIL import Image
import threading
import os
import time
import subprocess

# TODO: MOVE TO ANOTHER FILE
def byebye():
    # clear LP
    lp.Reset()

    # text matrix
    text = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    displayTextMatrix(text, 0.2)

def displayTextMatrix(textMatrix, delay):
    # loop through textMatrix column length
    for i in range(0, len(textMatrix[0])):
        lp.Reset()

        for line in range(0, 8):
            for col in range(0, 8):
                try:
                    if(textMatrix[line][col+i] == 1):
                        lp.LedCtrlXY(col, line+1, 0, 3)
                except IndexError:
                    pass

        time.sleep(delay)


# TODO: move in another file
def close():
    # clear active keys before animation
    for key in pages[current_page].keys:
        # OBS Active Scene
        if key.active == True:
            key.active = False
    # display Bye !
    byebye()
    # clear screen before exit
    lp.Reset()
    os._exit(1)

def about():
    # display about notification
    subprocess.run('notify-send -t 10000 -i /home/baptiste/Projects/launchpad_controller/icon_small.png "Launchpad Controller v0.1" "By github.com/bdelphin - GNU GPL v3.\nBased on launchpad.py by FMMT666."', shell=True)



def keyDown(pressed_key):
    global current_page, count

    if(len(str(pressed_key)) > 2 and str(pressed_key).startswith('20')):
        # PAGES Buttons
        switchToPage(int(str(pressed_key)[2]))
        return

    #TODO: create as many objects as keys to avoid for loop

    for key in pages[current_page].keys:
        # OBS Active Scene
        if key.active == True:
            key.active = False
            lp.LedCtrlRaw(int(key.index), 3, 0)
        
        if key.index == pressed_key:
            lp.LedCtrlRaw(pressed_key, 3, 3)
            key.processKeypress()

def keyUp(pressed_key):
    # restore led color
    for key in pages[current_page].keys:
        if key.index == pressed_key and key.playing == False:
            lp.LedCtrlRaw(key.index, 3, 0)

    if(len(str(pressed_key)) > 2 and str(pressed_key).startswith('20')):
        lp.LedCtrlRaw(pressed_key, 3, 3)
    #if (page == 0):
    #    updateLedColorSoundAnimation()

def switchToPage(newPage):
    global current_page, pages, lp

    if(int(newPage) < current_page):
        # right to left animation
        pages[newPage].display(lp, 'left')
    elif(int(newPage) > current_page):
        #left to right animation
        pages[newPage].display(lp, 'right')
        
    current_page = int(newPage)


## TODO : fix (delete) stuff below
#? doesn't seems to be needed anymore.
# def updateLedColorSoundAnimation():
#     global playing
#     for key, value in playing.items():
#         if (value == True):
#             print("found playing tune, led to green")
#             lp.LedCtrlRaw(int(key), 0, 3)
#             #playing_led_on[key] = True
#         elif (value == False):
#             lp.LedCtrlRaw(int(key), 3, 0)
#             print("tune ended, led to red")
#             #playing_led_on[key] = False



# Main

print("Launchpad Controller started.")

# Systray icon (cause we need a way to close this app !)
image = Image.open("icon_small.png")
menu = ( item('about', about), item('exit', close))
icon = pystray.Icon("Launchpad Controller", image, "Launchpad Controller", menu)
# launch systray icon in a thread, cause icon.run is a blocking function
systrayThread = threading.Thread(target=icon.run)
systrayThread.start()

# TODO: custom config with -c / --config XXXX.json
# JSON config file parsing
config_file = open('config.json',)
config = json.load(config_file)

# this array will store all keys.
pages = []

# Launchpad init
lp = LP.Launchpad()
lp.Open()
lp.Reset()

# load config
for page_index in range(len(config['pages'])):
    pages.append(Page(page_index))
    for key in config['pages'][page_index]:
        current_key = config['pages'][page_index][key]
        if(current_key['type'] == 'sound'):
            pages[page_index].addKey(Key(lp, int(key), current_key['type'], duration=current_key['duration'], file=current_key['file']))
        elif(current_key['type'] == 'command'):
            pages[page_index].addKey(Key(lp, int(key), current_key['type'], command=current_key['command']))
        elif(current_key['type'] == 'keyboard'):
            pages[page_index].addKey(Key(lp, int(key), current_key['type'], keys=current_key['keys']))
        elif(current_key['type'] == 'keyboard_obs'):
            pages[page_index].addKey(Key(lp, int(key), current_key['type'], keys=current_key['keys'], windowPattern=current_key['windowPattern']))
        else:
            print("error, key type unrecognized")

# default page
current_page = 0

pages[0].display(lp, 'none')

# OBS : switch to first scene by default
pages[0].keys[0].active = True
subprocess.run(pages[0].keys[0].command, shell=True)

# main loop
while(1):
    # key poll
    buttonState = lp.ButtonStateRaw()
    if(len(buttonState) > 0):
        if(buttonState[1] == True):
            keyDown(buttonState[0])
        elif(buttonState[1] == False):
            keyUp(buttonState[0])

    #TODO : fix playing animation (overriden by keyUp restore color)
    #? already fixed ?

    for key in pages[current_page].keys:
        # OBS Active Scene
        if key.active == True:
            key.setGreen()
        
        if key.playing == True:
            key.animate()

    time.sleep(0.1)

lp.Close()

