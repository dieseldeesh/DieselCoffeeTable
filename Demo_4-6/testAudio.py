import wave
import pyaudio
import threading
import time
import pyaudio  
import wave 
import audio


audio.initAll()
cups = [0,0,0,1]
audio.setAllCups(cups)
time.sleep(5)
cups = [1,0,0,0]
audio.setAllCups(cups)
time.sleep(5)
cups = [1,0,0,1]
audio.setAllCups(cups)
time.sleep(5)
cups = [1,0,1,1]
audio.setAllCups(cups)