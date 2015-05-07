import numpy as np
import cv2
import cv2.cv as cv
import threading
import sys
import os
import socket
import json


H_MIN = 0
S_MIN = 0
done = 0

def start_srv():
  global H_MIN, S_MIN, V_MIN, H_MAX, S_MAX, V_MAX, done
  server_address = './uds_socket'

  # Make sure the socket does not already exist
  try:
      os.unlink(server_address)
  except OSError:
      if os.path.exists(server_address):
          raise

  # Create a UDS socket
  sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
  # Bind the socket to the port
  print >>sys.stderr, 'starting up on %s' % server_address
  sock.bind(server_address)

  # Listen for incoming connections
  sock.listen(1)

  while (done == 0):
      # Wait for a connection
      # print >>sys.stderr, 'waiting for a connection'
      connection, client_address = sock.accept()
      try:
          # print >>sys.stderr, 'connection from', client_address
          djson = connection.recv(1024)
          data = json.loads(djson)
          # print 'received "%s"' % data
          H_MIN = data["H_MIN"]
          S_MIN = data["S_MIN"]
      finally:
          # Clean up the connection
          connection.close()

thr = threading.Thread(target=start_srv, args=(), kwargs={})
thr.start()

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # the area of the image with the largest intensity value
    ret,thresh1 = cv2.threshold(gray,H_MIN,S_MIN,cv2.THRESH_BINARY)


    # Display the resulting frame
    cv2.imshow('gray',gray)
    cv2.imshow('frame',thresh1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

done = 1
thr.join()