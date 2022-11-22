# class key
from vlc import *
import subprocess
import time

class Key:
       
    def __init__(self, lp, index, type, duration=None, file=None, command=None, keys=None, windowPattern=None):
        self.lp = lp

        self.index = index
        self.type = type
        self.duration = duration
        self.file = file
        self.command = command
        self.keys = keys
        self.windowPattern = windowPattern
        self.playing = False
        self.active = False
        self.vlc = ''
        self.start_time = 0
        self.green_level = 1
        if(self.type == 'sound'):
            self.vlc = MediaPlayer()
            self.media = Media(self.file)
            self.vlc.set_media(self.media)

    def processKeypress(self):
        if(self.type == 'sound'):
            if(self.duration == 'long'):
                if(not self.playing):
                    # self.vlc = MediaPlayer(self.file)
                    #TODO : replace things below with the same logic as short sounds
                    self.vlc.set_time(0)
                    self.vlc.play()
                    self.playing = True

                    # for animation
                    self.start_time = time.time_ns()
                    self.green_level = 1
                    
                    # events
                    self.events = self.vlc.event_manager()
                    self.events.event_attach(EventType.MediaPlayerEndReached, self.soundEnded)
                else:
                    self.vlc.stop()
                    self.playing = False
            else:
                # short sounds can be played multiple times
                # nope, doesn't work (it does actually, but just a few times until PulseAudio considers this DoS and start dropping connections)
                #self.vlc = MediaPlayer(self.file)
                
                # This is needed, fuck vlc
                self.vlc.set_media(self.media)
                #self.vlc.set_time(0)
                #print('just before vlc.play')
                self.vlc.play()
                #print('just after vlc.play')
                # events
                self.events = self.vlc.event_manager()
                self.events.event_attach(EventType.MediaPlayerEndReached, self.shortSoundEnded)

        elif(self.type == "command"):
            #command type, run command
            if('obs-cli' in self.command):
                self.active = True;
            subprocess.run(self.command, shell=True)
        elif(self.type == "keyboard"):
            #key type, run xdotool
            subprocess.run("xdotool key "+self.keys, shell=True)
        elif(self.type == "keyboard_obs"):
            subprocess.run("actwin=$(xdotool getactivewindow); xdotool search --name '" + self.windowPattern + "' windowactivate --sync key " + self.keys + " && xdotool windowactivate $actwin", shell=True)

    def soundEnded(self, event):
        self.playing = False
        # restore led color
        self.lp.LedCtrlRaw(self.index, 3, 0)
        #print("Sound ended !")

    #TODO : delete all this, not needed anymore
    def shortSoundEnded(self, event):
        #self.vlc.stop()

        # mediaplayer already has is_playing
        #TODO : delete
        self.playing = False
        
        # garbage :
        #self.vlc.release()
        
        # print(self.vlc.get_media())
        #media = Media(self.file)
        
        #self.vlc.set_media(self.media)
        
        #self.vlc.set_time(0)
        #self.vlc.stop()

    def setGreen(self):
        self.lp.LedCtrlRaw(self.index, 0, 3)
    
    def animate(self):
        cur_time = time.time_ns()
        if((cur_time-self.start_time) > 200000000):
            self.start_time = cur_time
            if(self.green_level < 3):
                self.green_level +=1
            else:
                self.green_level = 1
            self.lp.LedCtrlRaw(self.index, 0, self.green_level)
            

