#!/usr/bin/env python
"""Play a fixed frequency sound."""
from __future__ import division
import math
import Tkinter as tk
import threading
from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio
import time

pfrequency1 = 130.82
pfrequency2 = 329.63
pfrequency3 = 659.26
pfrequency4 = 783.99
frequency1 = 130.82
frequency2 = 329.63
frequency3 = 659.26
frequency4 = 783.99
volume = 1
cup1 = 0
cup2 = 0
cup3 = 0
cup4 = 0

try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range

sample_rate=22050

p = PyAudio()

stream1 = p.open(format=p.get_format_from_width(1), # 8bit
                channels=1, # mono
                rate=sample_rate,
                output=True)
stream2 = p.open(format=p.get_format_from_width(1), # 8bit
                channels=1, # mono
                rate=sample_rate,
                output=True)
stream3 = p.open(format=p.get_format_from_width(1), # 8bit
                channels=1, # mono
                rate=sample_rate,
                output=True)
stream4 = p.open(format=p.get_format_from_width(1), # 8bit
                channels=1, # mono
                rate=sample_rate,
                output=True)

bytebufs1 = ''
bytebufs2 = ''
bytebufs3 = ''
bytebufs4 = ''

def gen_Sine_Tone(num, frequency, duration, sample_rate):
    global bytebufs1, bytebufs2, bytebufs3, bytebufs4, volume

    duration = 3
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

 
    s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
    samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))

    bytebufsTemp = ""
    for buf in izip(*[samples]*sample_rate):
        bytebuf = bytes(bytearray(buf))
        bytebufsTemp+= bytebuf

    if num == 1:
        bytebufs1 = bytebufsTemp
    elif num == 2:
        bytebufs2 = bytebufsTemp
    elif num == 3:
        bytebufs3 = bytebufsTemp
    else:
        bytebufs4 = bytebufsTemp



def sine_tone(num, frequency, duration, sample_rate, stream):
    global volume, bytebufs1, bytebufs2, bytebufs3, bytebufs4
    # # print "volume ", volume
    # # print "frequency", frequency

    # n_samples = int(sample_rate * duration)
    # restframes = n_samples % sample_rate

 
    # s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
    # samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))

    # for buf in izip(*[samples]*sample_rate):
    #     bytebuf = bytes(bytearray(buf))
    #     #print "     bytes written", bytebuf # write several samples at a time
    #     #stream.write(bytebuf)
    if (num == 1):
        while True:
            stream1.write(bytebufs1)
    elif (num == 2):
        while True:
            stream2.write(bytebufs2)
    elif (num == 3):
        while True:
            stream3.write(bytebufs3)
    else:
        while True:
            stream4.write(bytebufs4)
#    # fill remainder of frameset with silence
#    stream.write(b'\x80' * restframes)

def onKeyPress(event):
    global frequency1, frequency2, frequency3, frequency4, cup1, cup2, cup3, cup4, volume
    text.insert('end', 'You pressed %s\n' % (event.char, ))
    num = 0
    if (event.char == 'b'):
        volume = 1
    if (event.char == 'c'):
        frequency1 = 440
    if (event.char == 'l'):
        frequency1 = 230.66
    if (event.char == '1'):
        cup1 = 1
        num = 1
    if (event.char == '2'):
        cup2 = 1
        num = 2
    if (event.char == '3'):
        cup3 = 1
        num = 3
    if (event.char == '4'):
        cup4 = 1
        num = 4
    if (event.char == '5'):
        cup1 = 0
        num = 1
    if (event.char == '6'):
        cup2 = 0
        num = 2
    if (event.char == '7'):
        cup3 = 0
        num = 3
    if (event.char == '8'):
        cup4 = 0
        num = 4

    if (event.char == 's'):
        for x in xrange(7):
            frequency1 = genFreq(x+50)
        for x in xrange(7):
            frequency1 = genFreq(56-x)
            
    f = getFrequency(num)
    gen_Sine_Tone(num, f, 3, 22050)

def onClick(event):
    text.insert('end', 'x= %d y = %d\n' %(event.x, event.y))
    cx = event.x
    cy = event.y
    num = 1
    if cx > 200 and cx < 700 and cy < 350:
        num = 2
    elif cx > 200 and cx < 700 and cy >= 350:
      num = 4
    elif cx <= 200:
      num = 1
    elif cx >= 700:
        num = 3
    genFrequency(cx, cy, num)
    f = getFrequency(num)
    gen_Sine_Tone(num, f, 3, 22050)


def genFreq(n):
    return 2**((n-49)/12)*440

def getFrequency(num):
    global frequency1, frequency2, frequency3, frequency4, cup1, cup2, cup3, cup4
    if num == 1:
        if getCup(num):
            return frequency1
        else:
            return 0
    elif num == 2:
        if getCup(num):
            return frequency2
        else:
            return 0
    elif num == 3:
        if getCup(num):
            return frequency3
        else:
            return 0
    else:
        if getCup(num):
            return frequency4
        else:
            return 0


def setFrequency(num, delta):
    global frequency1, frequency2, frequency3, frequency4, pfrequency1, pfrequency2, pfrequency3, pfrequency4
    print "number = ", num
    if num == 1:
        frequency1 = pfrequency1 + delta
        print "Frequency = ", frequency1
    elif num == 2: 
        frequency2 = pfrequency2 + delta
        print "Frequency = ", frequency2
    elif num == 3:
        frequency3 = pfrequency3 + delta
        print "Frequency = ", frequency3
    else:
        frequency4 = pfrequency4 + delta
        print "Frequency = ", frequency4

def getPFrequency(num):
    global pfrequency1, pfrequency2, pfrequency3, pfrequency4
    if num == 1:
        return pfrequency1
    elif num == 2: 
        return pfrequency2
    elif num == 3:
        return pfrequency3
    else:
        return pfrequency4

def genFrequency(cx, cy, num):
    if (num == 1 or num == 3):
        ratio = cy/10.0
        setFrequency(num, ratio)
    else:
        ratio = (abs(cx - 150.0))/10.0
        setFrequency(num, ratio)

def getCup(num):
    global cup1, cup2, cup3, cup4
    if num == 1:
        return cup1
    elif num == 2:
        return cup2
    elif num == 3:
        return cup3
    else:
        return cup4

def play(stream, num):
    while(True):
        if (getCup(num)):
            f = getFrequency(num)
            sine_tone(
                num,
                f,
                # see http://www.phy.mtu.edu/~suits/notefreqs.html
                #frequency, # Hz, waves per second A4
                duration=3, # seconds to play sound
                #volume=vol, # 0..1 how loud it is
                # see http://en.wikipedia.org/wiki/Bit_rate#Audio
                sample_rate=22050, # number of samples per second
                stream=stream
            )


def start(stream, num):
  thr = threading.Thread(target=play, args=([stream, num]), kwargs={})
  thr.start()
  return thr 

start(stream1, 1)
start(stream2, 2)
start(stream3, 3)
start(stream4, 4)
root = tk.Tk()
root.configure(background='black')
root.geometry('900x700')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
root.bind('<KeyPress>', onKeyPress)
root.bind('<Button-1>', onClick)
root.mainloop()

stream1.stop_stream()
stream1.close()
p.terminate()
