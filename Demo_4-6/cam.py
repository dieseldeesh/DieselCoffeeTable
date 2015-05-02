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

def getSoundAndVolume(contours, leftOrRight, img):
  found = False
  volume = 0
  for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    #print len(approx)
    if len(approx)==5:
      #print "pentagon"
      found = True
      # cv2.drawContours(img,[cnt],0,255,-1)
    elif len(approx)==3:
      #print "triangle"
      found = True
      # cv2.drawContours(img,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
      #print "square"
      found = True
      # cv2.drawContours(img,[cnt],0,(0,0,255),-1)
    elif len(approx) == 9:
      #print "half-circle"
      found = True
      # cv2.drawContours(img,[cnt],0,(255,255,0),-1)
    elif len(approx) > 10:
      #print "circle"
      cv2.drawContours(img,[cnt],0,(0,255,255),-1)

#    if(found):
#      volume=getVolume(cnt,leftOrRight)

  return found,volume,img

while(True):
  ret,frame = cap.read()

  xlen = len(frame)
  ylen = len(frame[0])

  frame1 = frame[0:200, 0:ylen]
  frame2 = frame[0:xlen, 0:200]
  frame3 = frame[xlen-400:xlen-200, 0:ylen]
  frame4 = frame[0:xlen, ylen-400:ylen-200]

  frame = cv2.medianBlur(frame,5)
  frame1 = cv2.medianBlur(frame1,5)
  frame2 = cv2.medianBlur(frame2,5)
  frame3 = cv2.medianBlur(frame3,5)
  frame4 = cv2.medianBlur(frame4,5)

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
  gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
  gray3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
  gray4 = cv2.cvtColor(frame4, cv2.COLOR_BGR2GRAY)

  ret,thresh = cv2.threshold(gray,45,255,1)
  ret1,thresh1 = cv2.threshold(gray1,45,255,1)
  ret2,thresh2 = cv2.threshold(gray2,45,255,1)
  ret3,thresh3 = cv2.threshold(gray3,45,255,1)
  ret4,thresh4 = cv2.threshold(gray4,45,255,1)

  cups = [0,0,0,0]


  dp = 1
  res = 400
  p1 = 200
  p2 = 10.0
  minR = 2
  maxR = 200

  circles1 = cv2.HoughCircles(thresh1,cv.CV_HOUGH_GRADIENT,dp,res,param1=p1,param2=p2,minRadius=minR,maxRadius=maxR)#
# 
  found1 = 0
  if circles1 != None:
    circles1 = np.uint16(np.around(circles1))#

    for i in circles1[0,:]:
      # draw the outer circle
      cv2.circle(thresh1,(i[0],i[1]),i[2],(0,255,0),2)
      # draw the center of the circle
      cv2.circle(thresh1,(i[0],i[1]),2,(0,0,255),3)
      xc = i[0]
      yc = i[1]
      found1 = 1
  else:
    found1 = 0

  circles2 = cv2.HoughCircles(thresh2,cv.CV_HOUGH_GRADIENT,dp,res,param1=p1,param2=p2,minRadius=minR,maxRadius=maxR)#
# 
  found2 = 0
  if circles2 != None:
    circles2 = np.uint16(np.around(circles2))

    for i in circles2[0,:]:
      # draw the outer circle
      cv2.circle(thresh2,(i[0],i[1]),i[2],(0,255,0),2)
      # draw the center of the circle
      cv2.circle(thresh2,(i[0],i[1]),2,(0,0,255),3)
      xc2 = i[0]
      yc2 = i[1]
      found2 = 1
  else:
    found2 = 0

  circles3 = cv2.HoughCircles(thresh3,cv.CV_HOUGH_GRADIENT,dp,res,param1=p1,param2=p2,minRadius=minR,maxRadius=maxR)#
# 
  found3 = 0
  if circles3 != None:
    circles3 = np.uint16(np.around(circles3))

    for i in circles3[0,:]:
      # draw the outer circle
      cv2.circle(thresh3,(i[0],i[1]),i[2],(0,255,0),2)
      # draw the center of the circle
      cv2.circle(thresh3,(i[0],i[1]),2,(0,0,255),3)
      xc3 = i[0]
      yc3 = i[1]
      found3 = 1
  else:
    found3 = 0

  circles4 = cv2.HoughCircles(thresh4,cv.CV_HOUGH_GRADIENT,dp,res,param1=p1,param2=p2,minRadius=minR,maxRadius=maxR)#
# 
  found4 = 0
  if circles4 != None:
    circles4 = np.uint16(np.around(circles4))

    for i in circles4[0,:]:
      # draw the outer circle
      cv2.circle(thresh4,(i[0],i[1]),i[2],(0,255,0),2)
      # draw the center of the circle
      cv2.circle(thresh4,(i[0],i[1]),2,(0,0,255),3)
      xc4 = i[0]
      yc4 = i[1]
      found4 = 1
  else:
    found4 = 0
  #found1, volume1, thresh1 = getSoundAndVolume(contours1, True, thresh1)
  cups[0]= 1 if (found1) else 0
  cups[1]= 1 if (found2) else 0
  cups[2]= 1 if (found3) else 0
  cups[3]= 1 if (found4) else 0
#  cups[1]= 0 if (found2) else 0

  audio.setAllCups(cups)

  #print"Thresh yo ", thresh1
  #cv2.imshow('whole', thresh)
  #cv2.imshow('frame1',thresh1)
  cv2.imshow('frame2',thresh2)
  #cv2.imshow('frame3',thresh3)
  #cv2.imshow('frame4',thresh4)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

audio.closeAll()
cap.realease()
cv2.destroyAllWindows()