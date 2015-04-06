import numpy as np
import cv2
import time
import audio


print "starting cam.py..."
audio.initAll()

cap = cv2.VideoCapture(0)

while(True):
  ret,frame = cap.read()

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  #http://stackoverflow.com/questions/11424002/how-to-detect-simple-geometric-shapes-using-opencv
  img = frame

  ret,thresh = cv2.threshold(gray,127,255,1)

  contours,h = cv2.findContours(thresh,1,2)

  for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print len(approx)
    if len(approx)==5:
      print "pentagon"
      audio.setAllCups([1,0,0,0])
      # cv2.drawContours(img,[cnt],0,255,-1)
    elif len(approx)==3:
      print "triangle"
      audio.setAllCups([0,1,0,0])
      # cv2.drawContours(img,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
      print "square"
      audio.setAllCups([0,0,1,0])
      # cv2.drawContours(img,[cnt],0,(0,0,255),-1)
    elif len(approx) == 9:
      print "half-circle"
      audio.setAllCups([0,0,0,1])
      # cv2.drawContours(img,[cnt],0,(255,255,0),-1)
    elif len(approx) > 15:
      print "circle"
      audio.setAllCups([0,0,0,0])
      # cv2.drawContours(img,[cnt],0,(0,255,255),-1)


  cv2.imshow('frame',gray)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

audio.closeAll()
cap.realease()
cv2.destroyAllWindows()