# events-example0.py
# Barebones timer, mouse, and keyboard events
import pyin
import time
import threading
import numpy as np
from Tkinter import *

tt = pyin.TapTester()
amp = 0
fft_block = []
mag = 0

def mousePressed(event):
    redrawAll()

def keyPressed(event):
    redrawAll()

def timerFired():
    global amp, fft_block, mag
    # print "amp: ", amp
    
    # if(len(fft_block) > 0):
    #     x = np.absolute(fft_block)
    #     y = sum(x)/len(x)
    #     mag = y
    #     # print "y: ",y

    delay = 5 # milliseconds
    redrawAll()
    canvas.after(delay, timerFired) # pause, then call timerFired again

def redrawAll():
    global mag,amp
    canvas.delete(ALL)
    cx = canvas.data.cx
    cy = canvas.data.cy
    r = amp*1000*4
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="cyan")

def listen():
    global amp, fft_block
    while(True):
        amp, fft_block = tt.listen()

        # time.sleep(10)


def init():
    print "initing..."
    thr = threading.Thread(target=listen, args=(), kwargs={})
    thr.start()

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    canvas = Canvas(root, width=1000, height=1000)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.cx = 500
    canvas.data.cy = 500
    init()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()