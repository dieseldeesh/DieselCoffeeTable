import wave
import pyaudio
import threading
import time
import pygame
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

v1 = 0
v2 = 0
v3 = 0
v4 = 0

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

def setAllCups(a, v):
  global cup1, cup2, cup3, cup4, v1, v2, v3, v4
  print "In SET ALL CUPS"
  cup1 = a[0]
  cup2 = a[1]
  cup3 = a[2]
  cup4 = a[3]
  v1 = v[0]
  v2 = v[1]
  v3 = v[2]
  v4 = v[3]



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

def getVolume (fname):
  global v1, v2, v3, v4
  if(fname == "../Audio/test.wav"):
    return v1
  if(fname == "../Audio/test1.wav"):
    return v2
  if(fname == "../Audio/test2.wav"):
    return v3
  if(fname == "../Audio/test3.wav"):
    return v4

def play():
  #read data 
  global killAll, cup1, cup2, cup3, cup4, v1, v2, v3, v4

  print "hello inside play?"

  tog1 = 1
  tog2 = 1
  tog3 = 1
  tog4 = 1

  sound1 = pygame.mixer.Sound('../Audio/test.wav')
  sound2 = pygame.mixer.Sound('../Audio/test1.wav')
  sound3 = pygame.mixer.Sound('../Audio/test2.wav')
  sound4 = pygame.mixer.Sound('../Audio/test3.wav')

  while(not(killAll)):
    #print "hello inside while and" 
    length = 0
    channel1 = None
    channel2 = None
    channel3 = None
    channel4 = None
    if(cup1):
      #print "cup1 = ", cup1
      sound = pygame.mixer.Sound('../Audio/test.wav')
      sound.set_volume(v1)
      channel1 = sound.play()
      #tog1 = 0
      length = max(length, sound.get_length())
    if(cup2):
      #print "cup2 = ", cup2
      sound = pygame.mixer.Sound('../Audio/test1.wav')
      sound.set_volume(v2)
      channel2 = sound.play()
      #tog2 = 0
      length = max(length, sound.get_length())
    if(cup3):
      #print "cup3 = ", cup3
      sound = pygame.mixer.Sound('../Audio/test2.wav')
      sound.set_volume(v3)
      channel3 = sound.play()
      #tog3 = 0
      length = max(length, sound.get_length())
    if(cup4):
      #print "cup4 = ", cup4
      sound = pygame.mixer.Sound('../Audio/test3.wav')
      sound.set_volume(v4)
      channel4 = sound.play()
      #tog4 = 0
      length = max(length, sound.get_length())

      if (channel1 != None):
        while channel1.get_busy():
          count = 0

      if (channel2 != None):
        while channel2.get_busy():
          count = 0

      if (channel3 != None):
        while channel3.get_busy():
          count = 0

      if (channel4 != None):
        while channel4.get_busy():
          count = 0

def start():
  thr = threading.Thread(target=play, args=(), kwargs={})
  thr.start()
  return thr 


#start all sounds
def initAll():
  global t1,t2,t3,t4
  pygame.mixer.init()
  print "hello inside initall 1"
  pygame.mixer.pre_init(44100, -16, 2, 2048)
  pygame.init()
  print "hello inside install 2?"
  t1 = start()
  #t2 = start("../Audio/test1.wav")
  #t3 = start("../Audio/test2.wav")
  #t4 = start("../Audio/test3.wav")

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

