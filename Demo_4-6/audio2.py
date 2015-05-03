import wave
import pyaudio
import sys
import threading

p = pyaudio.PyAudio()  
chunk = 131072  

fname = "../Audio/test3.wav"
f = wave.open(fname,"rb")
format = p.get_format_from_width(f.getsampwidth())
channels = f.getnchannels() 
rate = f.getframerate() 
output = True
data = f.readframes(chunk)  
# cc = data

# stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
#                 channels = f.getnchannels(),  
#                 rate = f.getframerate(),  
#               output = True) 

# #play stream  
# while data != '':  
#     stream.write(data)  
#     data = f.readframes(chunk)  



# stream.stop_stream()  
# stream.close()

def play_sound2():
  stream = p.open(format = format,  
                channels = channels,  
                rate = rate,  
              output = output) 
  stream.write(data)  
  stream.stop_stream()  
  stream.close()

def play_sound():
  thr = threading.Thread(target=play_sound2, args=(), kwargs={})
  thr.start()

