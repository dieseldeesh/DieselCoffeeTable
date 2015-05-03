import wave
import pyaudio
import threading
import time
import pyaudio  
import wave 
import audioPyGame

print "hello1?"
audioPyGame.initAll()
print "hello2?"
cups = [0,0,0,1]
vols = [0.0, 0.0, 0.0, 0.10]
audioPyGame.setAllCups(cups, vols)
time.sleep(5)
cups = [0,0,0,1]
vols = [0.0, 0.0, 0.0, 0.75]
audioPyGame.setAllCups(cups, vols)
time.sleep(5)
cups = [1,0,0,0]
vols = [0.75, 0.0, 0.0, 0.0]
audioPyGame.setAllCups(cups, vols)
time.sleep(5)
cups = [1,0,0,1]
vols = [0.75, 0.0, 0.0, 0.75]
audioPyGame.setAllCups(cups, vols)
time.sleep(5)
cups = [1,0,1,1]
vols = [0.75, 0.0, 1.0, 0.75]
audioPyGame.setAllCups(cups, vols)
time.sleep(5)
cups = [1,0,1,1]
vols = [0.75, 0.0, 0.33, 0.75]
audioPyGame.setAllCups(cups, vols)
time.sleep(5)
cups = [1,0,1,1]
vols = [1.0, 0.0, 0.0, 1.0]
audioPyGame.setAllCups(cups, vols)