# Launchad Controller

:warning: This is a work in progress :warning:

Don't expect stuff here to be easy to use and to work as expected.

This project allows me to launch sounds (samples), run terminal commands, control OBS and send key combinations from my Novation Launchpad Mk1, while I'm streaming on my Linux computer.

## Requirements

- [launchpad.py by FMMT666](https://github.com/FMMT666/launchpad.py), without this piece of software none of this would be possible
- [pygame](https://github.com/pygame/pygame) (needed by launchpad.py)
- [python bindings for libvlc](https://github.com/oaubert/python-vlc), to play sounds
- [pystray](https://github.com/moses-palmer/pystray), to create the system tray icon (cause we need a way to quit the program)
- [xdotool](https://github.com/jordansissel/xdotool), to launch key combinations (I'm not using libxdo-python for now, and I don't remember why not)

And I think that's all, but this list may be updated.

## TODO

- install script (to remove my home folder from the .desktop file)
- clean everything, remove unused stuff
- JSON config file : build a GTK App to configure it !