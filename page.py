# class page

import launchpad_py as LP

class Page:

    def __init__(self, index):
        self.index = index
        self.keys = []

    def addKey(self, key):
        self.keys.append(key)

    def display(self, lp, animationDirection):
        # reset to clear Automap LEDs
        lp.Reset()
        # show current automap position
        lp.LedCtrlRaw(int('20'+str(self.index)), 3, 3)
        # TODO : replace with LetCtrlAutomap()
        #lp.LedCtrlAutomap()

        # TODO : move animation elsewhere ?
        if(animationDirection == 'left'):
            #right to left animation
            for i in range(8):
                for j in range(1,9):
                    lp.LedCtrlXY(7-i-1, 9-j, 0, 3)
                    lp.LedCtrlXY(7-i, 9-j, 3, 3)
            for i in range(8):
                for j in range(1,9):
                    lp.LedCtrlXY(7-i, 9-j, 0, 0)
        elif(animationDirection == 'right'):
            #left to right animation
            for i in range(8):
                for j in range(1,9):
                    lp.LedCtrlXY(i, j, 0, 3)
                    lp.LedCtrlXY(i-1, j, 3, 3)
            for i in range(8):
                for j in range(1,9):
                    lp.LedCtrlXY(i, j, 0, 0)
        elif(animationDirection == 'none'):
            pass
        else:
            print("wrong animation direction sent to page.display() !")

        for key in self.keys:
            lp.LedCtrlRaw(int(key.index), 3, 0)
