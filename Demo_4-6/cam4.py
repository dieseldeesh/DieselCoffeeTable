import numpy as np
import cv2
import cv2.cv as cv
import threading
import sys
import os
import socket
import json

#0 112 125 84 226 270
H_MIN = 0
S_MIN = 112
V_MIN = 90
H_MAX = 200
S_MAX = 200
V_MAX = 270
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
      print >>sys.stderr, 'waiting for a connection'
      connection, client_address = sock.accept()
      try:
          print >>sys.stderr, 'connection from', client_address
          djson = connection.recv(1024)
          data = json.loads(djson)
          print 'received "%s"' % data
          H_MIN = data["H_MIN"]
          S_MIN = data["S_MIN"]
          V_MIN = data["V_MIN"]
          H_MAX = data["H_MAX"]
          S_MAX = data["S_MAX"]
          V_MAX = data["V_MAX"]
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
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ORANGE_MIN = np.array([H_MIN, S_MIN, V_MIN],np.uint16)
    ORANGE_MAX = np.array([H_MAX, S_MAX, V_MAX],np.uint16)
    frame_threshed = cv2.inRange(hsv, ORANGE_MIN, ORANGE_MAX)

    kernel = np.ones((10,10),np.uint8)
    erosion = cv2.erode(frame_threshed,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)

    # Display the resulting frame
    cv2.imshow('frame',dilation)
    # cv2.imshow('hsv',hsv)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        done = 1
        break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

done = 1
thr.join()

