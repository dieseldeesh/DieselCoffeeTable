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

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    cups = [0,0,0,0]
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
      if(area > 200):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print "center: ",cx,cy
        if cx > 200 and cx < 700 and cy < 350:
          cups[0] = 1
        elif cx > 200 and cx < 700 and cy >= 350:
          cups[1] = 1
        elif cx < 200:
          cups[2] = 1
        elif cx > 700:
          cups[3] = 1

    print "cups : ", cups
    # Display the resulting frame
    audio.setAllCups(cups)
    time.sleep(5)
    cv2.imshow('frame',dilation)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# When everything done, release the capture
audio.closeAll()
cap.release()
cv2.destroyAllWindows()

