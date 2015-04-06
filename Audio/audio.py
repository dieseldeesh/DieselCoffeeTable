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
cup1 = 1
cup2 = 1
cup3 = 1
cup4 = 1

def getCup(fname):
  if(fname == "test.wav"):
    return cup1
  if(fname == "test1.wav"):
    return cup2
  if(fname == "test2.wav"):
    return cup3
  if(fname == "test3.wav"):
    return cup4

def play(fname):
  #read data 
  while(1): 
    if(getCup(fname)):
      f = wave.open(r"/Users/anuj/Code/18549/DieselCoffeeTable/Audio/"+fname,"rb")  

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

def start(fname):
  thr = threading.Thread(target=play, args=([fname]), kwargs={})
  thr.start()
  return thr 


#start all sounds
t1 = start("test.wav")
t2 = start("test1.wav")
t3 = start("test2.wav")
t4 = start("test3.wav")

#testing code
time.sleep(5)
cup1 = 0
time.sleep(5)
cup2 = 0
time.sleep(5)
cup3 = 0
time.sleep(5)
cup4 = 0

