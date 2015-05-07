#!/usr/bin/env python
"""Play a fixed frequency sound."""
from __future__ import division
import math
import Tkinter as tk
import threading
from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio
import time

pfrequency1 = 261.26
pfrequency2 = 350.665
pfrequency3 = 420.628
pfrequency4 = 520.225
frequency1 = 261.26
frequency2 = 350.665
frequency3 = 420.628
frequency4 = 520.225
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


def sine_tone(frequency, duration, sample_rate, stream):
    global volume
    # print "volume ", volume
    # print "frequency", frequency

    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

 
    s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
    samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))

    for buf in izip(*[samples]*sample_rate):
        bytebuf = bytes(bytearray(buf))
        #print "     bytes written", bytebuf # write several samples at a time
        stream.write(bytebuf)

#    # fill remainder of frameset with silence
#    stream.write(b'\x80' * restframes)

def onKeyPress(event):
    global frequency1, frequency2, frequency3, frequency4, cup1, cup2, cup3, cup4, volume
    text.insert('end', 'You pressed %s\n' % (event.char, ))
    if (event.char == 'a'):
        volume = 0.5
    if (event.char == 'b'):
        volume = 1
    if (event.char == 'c'):
        frequency1 = 440
    if (event.char == 'l'):
        frequency1 = 230.66
    if (event.char == '1'):
        cup1 = 1
    if (event.char == '2'):
        cup2 = 1
    if (event.char == '3'):
        cup3 = 1
    if (event.char == '4'):
        cup4 = 1
    if (event.char == '5'):
        cup1 = 0
    if (event.char == '6'):
        cup2 = 0
    if (event.char == '7'):
        cup3 = 0
    if (event.char == '8'):
        cup4 = 0

    if (event.char == 's'):
        for x in xrange(7):
            frequency1 = genFreq(x+50)
        for x in xrange(7):
            frequency1 = genFreq(56-x)

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


def genFreq(n):
    return 2**((n-49)/12)*440

def getFrequency(num):
    global frequency1, frequency2, frequency3, frequency4
    if num == 1:
        return frequency1
    elif num == 2: 
        return frequency2
    elif num == 3:
        return frequency3
    else:
        return frequency4

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

def play(num, stream):
    while(True):
        if (getCup(num)):
            f = getFrequency(num)
            sine_tone(
                f,
                # see http://www.phy.mtu.edu/~suits/notefreqs.html
                #frequency, # Hz, waves per second A4
                duration=3, # seconds to play sound
                #volume=vol, # 0..1 how loud it is
                # see http://en.wikipedia.org/wiki/Bit_rate#Audio
                sample_rate=22050, # number of samples per second
                stream=stream
            )

def start(num,stream):
  thr = threading.Thread(target=play, args=([num, stream]), kwargs={})
  thr.start()
  return thr 

start(1, stream1)
start(2, stream2)
start(3, stream3)
start(4, stream4)

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
stream2.stop_stream()
stream2.close()
p.terminate()
