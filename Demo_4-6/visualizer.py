# events-example0.py
# Barebones timer, mouse, and keyboard events
import pyin
import time
import threading

from Tkinter import *

tt = pyin.TapTester()
amp = 0
def mousePressed(event):
    redrawAll()

def keyPressed(event):
    redrawAll()

def timerFired():
    global amp
    print "amp: ", amp
    delay = 200 # milliseconds
    redrawAll()
    canvas.after(delay, timerFired) # pause, then call timerFired again

def redrawAll():
    canvas.delete(ALL)
    canvas.create_line(0, 0, 200, amp*1000)

def listen():
    global amp
    while(True):
        amp = tt.listen()
        # time.sleep(10)


def init():
    print "initing..."
    thr = threading.Thread(target=listen, args=(), kwargs={})
    thr.start()

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    canvas = Canvas(root, width=300, height=200)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    init()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()