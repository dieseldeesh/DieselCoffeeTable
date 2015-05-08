import socket
import sys
import json

from Tkinter import *

# Send data
message = {}
message["H_MIN"] = 0
message["S_MIN"] = 112
message["V_MIN"] = 90
message["H_MAX"] = 200
message["S_MAX"] = 200
message["V_MAX"] = 270
message["A_MIN"] = 0
message["A_MAX"] = 500
message["trace"] = 0
message["audio"] = 0

trace = 0
audio = 0
updateMode = 1

def update():
  global message
  # Create a UDS socket
  sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
  # Connect the socket to the port where the server is listening
  server_address = './uds_socket'
  # print >>sys.stderr, 'connecting to %s' % server_address
  try:
      sock.connect(server_address)
  except socket.error, msg:
      print >>sys.stderr, msg
      sys.exit(1)

  try:

      # print >>sys.stderr, 'sending "%s"' % message

      mjson = json.dumps(message)
      # print "mjson: ",mjson
      sock.sendall(mjson)

  finally:
      # print >>sys.stderr, 'closing socket'
      sock.close()


def show_values(arg):
    message["H_MIN"] = w1.get()
    message["S_MIN"] = w2.get()
    message["V_MIN"] = w3.get()
    message["H_MAX"] = w4.get()
    message["S_MAX"] = w5.get()
    message["V_MAX"] = w6.get()
    message["A_MIN"] = w7.get()
    message["A_MAX"] = w8.get()
    if(updateMode):
      update()

def set():
  global trace
  trace = not(trace)
  print "trace: ", trace
  message["trace"]=trace

def set2():
  global audio
  audio = not(audio)
  print "audio: ", audio
  message["audio"] = audio

def set3():
  global updateMode
  updateMode = not(updateMode)
  print "Update Mode: ", updateMode

master = Tk()
w1 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values, label ="H_MIN")
w1.pack()
w2 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values, label = "S_MIN")
w2.pack()
w3 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values, label = "V_MIN")
w3.pack()
w4 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values, label = "H_MAX")
w4.pack()
w5 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values, label = "S_MAX")
w5.pack()
w6 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values, label = "V_MAX")
w6.pack()
w7 = Scale(master, from_=0, to=1000, orient=HORIZONTAL, command=show_values, label = "A_MIN")
w7.pack()
w8 = Scale(master, from_=0, to=1000, orient=HORIZONTAL, command=show_values, label = "A_MAX")
w8.pack()
b = Button(master, text='Update', command = update)
b.pack()
c2 = Button(master, text="updateMode", command=set3)
c2.pack()
c = Button(master, text="Trace", command=set)
c.pack()
c2 = Button(master, text="Audio", command=set2)
c2.pack()
mainloop()



