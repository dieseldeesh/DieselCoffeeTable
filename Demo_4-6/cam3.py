import numpy as np
import cv2
import cv2.cv as cv
import threading
import sys
import audio
import time

from Tkinter import *

#0 112 125 84 226 270
H_MIN = 103
S_MIN = 125
V_MIN = 7
H_MAX = 368
S_MAX = 279
V_MAX = 103

done = 0
audio.initAll()
cap = cv2.VideoCapture(0)
counter = 0
global cups
cups = [0,0,0,0]
threhold = 2


def averagePlay():
  global cups
  print "cups in play : ", cups
  cupVals = [0,0,0,0]

  cupVals[0] = 1 if  cups[0] >= threhold else 0
  cupVals[1] = 1 if  cups[1] >= threhold else 0
  cupVals[2] = 1 if  cups[2] >= threhold else 0
  cupVals[3] = 1 if  cups[3] >= threhold else 0
 
  print "cupValues : ", cupVals
  audio.setAllCups(cupVals)

  cups = [0,0,0,0]

while(True):
    # Capture frame-by-frame
    global cups
    ret, frame = cap.read()
    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    ORANGE_MIN = np.array([H_MIN, S_MIN, V_MIN],np.uint16)
    ORANGE_MAX = np.array([H_MAX, S_MAX, V_MAX],np.uint16)
    frame_threshed = cv2.inRange(hsv, ORANGE_MIN, ORANGE_MAX)

    kernel = np.ones((10,10),np.uint8)
    erosion = cv2.erode(frame_threshed,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)

    contours, heirarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if(len(contours) > 0):
      cnt = contours[0]
      M = cv2.moments(cnt)
      area = M['m00']
      counter += 1
      if(area > 200):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print "center: ",cx,cy
        if cx > 200 and cx < 700 and cy < 350:
          cups[0] += 1
        elif cx > 200 and cx < 700 and cy >= 350:
          cups[1] += 1
        elif cx < 200:
          cups[2] += 1
        elif cx > 700:
          cups[3] += 1

    # Display the resulting frame
    #time.sleep(1)
    if counter == 5:
      print "cups : ", cups
      averagePlay()
      counter = 0

    cv2.imshow('frame1',dilation)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
audio.closeAll()
cap.release()
cv2.destroyAllWindows()

