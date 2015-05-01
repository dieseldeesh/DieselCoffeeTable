import numpy as np
import cv2
import time
import audio

print "starting cam.py..."
audio.initAll()

cap = cv2.VideoCapture(0)

def getVolume(img,leftOrRight):
  M = cv2.moments(img)
  if(leftOrRight):
    #y centroid
    return int(M['m01']/M['m00'])
  else:
    #x centroid
    return int(M['m10']/M['m00'])

def getSoundAndVolume(contours, leftOrRight):
  found = False
  volume = 0
  for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print len(approx)
    if len(approx)==5:
      print "pentagon"
      found = True
      # cv2.drawContours(img,[cnt],0,255,-1)
    elif len(approx)==3:
      print "triangle"
      found = True
      # cv2.drawContours(img,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
      print "square"
      # cv2.drawContours(img,[cnt],0,(0,0,255),-1)
    elif len(approx) == 9:
      print "half-circle"
      found = True
      # cv2.drawContours(img,[cnt],0,(255,255,0),-1)
    elif len(approx) > 15:
      print "circle"

      # cv2.drawContours(img,[cnt],0,(0,255,255),-1)

    if(found):
      volume=getVolume(cnt,leftOrRight)

  return found,volume

while(True):
  ret,frame = cap.read()

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  #http://stackoverflow.com/questions/11424002/how-to-detect-simple-geometric-shapes-using-opencv
  img = frame

  ret,thresh = cv2.threshold(gray,127,255,1)
  x = [100,100,100,100]
  y = [100,100,100,100]
  width = [100,100,100,100]
  height = [100,100,100,100]
  leftOrRight = True
  cups = [0,0,0,0]
  for i in xrange(4):
    contours,h = cv2.findContours(thresh[y[i]:height[i], x[i]:width[i]],1,2)
    found, volume = getSoundAndVolume(contours,leftOrRight)
    leftOrRight= not leftOrRight
    cups[i]= 1 if (found) else 0

  audio.setAllCups(cup)

  cv2.imshow('frame',gray)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

audio.closeAll()
cap.realease()
cv2.destroyAllWindows()