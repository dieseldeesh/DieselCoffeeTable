import numpy as np
import cv2
import cv2.cv as cv
import threading
import sys
import os
import socket
import json

#0 112 125 84 226 270
H_MIN = 44
S_MIN = 103
V_MIN = 176
H_MAX = 140
S_MAX = 184
V_MAX = 250

trace = 0
audio = 0
A_MIN = 0
A_MAX = 0

done = 0

def start_srv():
  global H_MIN, S_MIN, V_MIN, H_MAX, S_MAX, V_MAX, done, trace, audio, A_MIN, A_MAX
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
          V_MIN = data["V_MIN"]
          H_MAX = data["H_MAX"]
          S_MAX = data["S_MAX"]
          V_MAX = data["V_MAX"]
          A_MIN = data["A_MIN"]
          A_MAX = data["A_MAX"]
          trace = data["trace"]
          audio = data["audio"]
          print "trace:", trace
      finally:
          # Clean up the connection
          connection.close()

# thr = threading.Thread(target=start_srv, args=(), kwargs={})
# thr.start()

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
    erosion = cv2.erode(frame_threshed,kernel,iterations = 5)
    dilation = cv2.dilate(erosion,kernel,iterations = 5)
    tmp = dilation.copy()

    # Display the resulting frame
    contours, heirarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
      M = cv2.moments(cnt)
      area = M['m00']
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00'])

      # if(area >= A_MIN and area <= A_MAX):
        #audio code here

        # if(trace):
      img = frame
      x,y,w,h = cv2.boundingRect(cnt)
      img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

      # (1) create a copy of the original:
      img = frame
      overlay = img.copy()
      # # (2) draw shapes:
      cv2.circle(overlay, (cx, cy), 12, (0, 255, 0), -1)
      # # (3) blend with the original:
      opacity = 0.4
      cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)


    cv2.imshow('frame',frame)
    cv2.imshow('dilation',tmp)

    # cv2.imshow('frame',dilation)

    # cv2.imshow('hsv',hsv)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        done = 1
        break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

done = 1
# thr.join()

