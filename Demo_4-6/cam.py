import numpy as np
import cv2.cv as cv
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

#    if(found):
#      volume=getVolume(cnt,leftOrRight)

  return found,volume

while(True):
  ret,frame = cap.read()

  frame1 = frame[0:300, 0:len(frame[0])]
  frame2 = frame[0:len(frame), 0:300]

  frame1 = cv2.medianBlur(frame1,5)
  frame2 = cv2.medianBlur(frame2,5)

  gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
  gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

  #http://stackoverflow.com/questions/11424002/how-to-detect-simple-geometric-shapes-using-opencv

  ret1,thresh1 = cv2.threshold(gray1,127,255,1)
  ret2,thresh2 = cv2.threshold(gray2,127,255,1)
#  x = [100,100,100,100]
#  y = [100,100,100,100]
#  width = [100,100,100,100]
#  height = [100,100,100,100]
  leftOrRight1 = True
  cups = [0,0,0,0]
  #for i in xrange(4):
  #  contours,h = cv2.findContours(thresh[y[i]:height[i], x[i]:width[i]],1,2)
  #  found, volume = getSoundAndVolume(contours,leftOrRight)
  #  leftOrRight= not leftOrRight
  #  cups[i]= 1 if (found) else 0
  detector = cv2.SimpleBlobDetector()
  keypoints = detector.detect(frame1)

  im_with_keypoints = cv2.drawKeypoints(gray1, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
  contours1,h1 = cv2.findContours(thresh1,1,2)
  contours2,h2 = cv2.findContours(thresh2,1,2)

  cv2.drawContours(gray1,contours1,-1,(0,255,0),3)


  circles = cv2.HoughCircles(gray1,cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)

  circles = np.uint16(np.around(circles))

  for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(gray1,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(gray1,(i[0],i[1]),2,(0,0,255),3)



#  found1, volume1 = getSoundAndVolume(contours1,True)
#  found2, volume2 = getSoundAndVolume(contours1,True)#

#  cups[0]= 0 if (found1) else 1
#  cups[1]= 0 if (found2) else 0

  audio.setAllCups(cups)

  cv2.imshow('frame',gray1)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

audio.closeAll()
cap.realease()
cv2.destroyAllWindows()