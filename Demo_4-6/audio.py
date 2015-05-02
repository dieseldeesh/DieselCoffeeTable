import wave
import pyaudio
import threading
import time
#!usr/bin/env python  
#coding=utf-8  

import pyaudio  
import wave  

#read audio in 1kb chunks
chunk = 1024  
p = pyaudio.PyAudio()  
#control values for cups
cup1 = 0
cup2 = 0
cup3 = 0
cup4 = 0

t1 = 0
t2 = 0
t3 = 0
t4 = 0
killAll = 0

def setCup(cupName, val):
  global cup1, cup2, cup3, cup4
  if(cupName == "1"):
    print "hi"
    cup1 = val
  if(cupName == "2"):
    cup2 = val
  if(cupName == "3"):
    cup3 = val
  if(cupName == "4"):
    cup4 = val

def setAllCups(a):
  global cup1, cup2, cup3, cup4
  cup1 = a[0]
  cup2 = a[1]
  cup3 = a[2]
  cup4 = a[3]



def getCup(fname):
  global cup1, cup2, cup3, cup4
  if(fname == "../Audio/test.wav"):
    return cup1
  if(fname == "../Audio/test1.wav"):
    return cup2
  if(fname == "../Audio/test2.wav"):
    return cup3
  if(fname == "../Audio/test3.wav"):
    return cup4

def play(fname):
  #read data 
  global killAll
  while(not(killAll)): 
    if(getCup(fname)):
      f = wave.open(r"../Audio/"+fname,"rb")  

      stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                      channels = f.getnchannels(),  
                      rate = f.getframerate(),  
                    output = True) 
      data = f.readframes(chunk)  

      #paly stream  
      while data != '':  
          stream.write(data)  
          data = f.readframes(chunk)  
      
      stream.stop_stream()  
      stream.close()
    else:
      time.sleep(4)

def start(fname):
  thr = threading.Thread(target=play, args=([fname]), kwargs={})
  thr.start()
  return thr 


#start all sounds
def initAll():
  global t1,t2,t3,t4
  t1 = start("../Audio/test.wav")
  t2 = start("../Audio/test1.wav")
  t3 = start("../Audio/test2.wav")
  t4 = start("../Audio/test3.wav")

def closeAll():
  print "attempting close audio loops..."
  global killAll, t1, t2, t3, t4
  killAll = 1
  t1.join()
  t2.join()
  t3.join()
  t4.join()
  print "closed all audio loops"


# initAll()
# setAllCups([1,1,1,1])


# #testing code
# time.sleep(5)
# cup1 = 0
# time.sleep(5)
# cup2 = 0
# time.sleep(5)
# cup3 = 0
# time.sleep(5)
# cup4 = 0
# closeAll()
# print "killed all audio loops"

