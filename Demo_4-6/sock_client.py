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

def update():
  global message
  # Create a UDS socket
  sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
  # Connect the socket to the port where the server is listening
  server_address = './uds_socket'
  print >>sys.stderr, 'connecting to %s' % server_address
  try:
      sock.connect(server_address)
  except socket.error, msg:
      print >>sys.stderr, msg
      sys.exit(1)

  try:

      print >>sys.stderr, 'sending "%s"' % message

      mjson = json.dumps(message)
      print "mjson: ",mjson
      sock.sendall(mjson)

  finally:
      print >>sys.stderr, 'closing socket'
      sock.close()


def show_values(arg):
    message["H_MIN"] = w1.get()
    message["S_MIN"] = w2.get()
    message["V_MIN"] = w3.get()
    message["H_MAX"] = w4.get()
    message["S_MAX"] = w5.get()
    message["V_MAX"] = w6.get()
    update()

master = Tk()
w1 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values)
w1.pack()
w2 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values)
w2.pack()
w3 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values)
w3.pack()
w4 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values)
w4.pack()
w5 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values)
w5.pack()
w6 = Scale(master, from_=0, to=500, orient=HORIZONTAL, command=show_values)
w6.pack()
mainloop()