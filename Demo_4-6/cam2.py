import numpy as np
import cv2
import time


cap = cv2.VideoCapture(0)
SENSITVITY = 20

while(True):
    # Capture frame-by-frame
    diffImage = []
    ret1, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    ret2, frame2 = cap.read()
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diffImage = cv2.absdiff(gray1, gray2)

    ret3, threshImage = cv2.threshold(diffImage, SENSITVITY, 255, cv2.THRESH_BINARY)

    blurImage = cv2.blur(threshImage, (10,10))
    ret4, threshImage = cv2.threshold(blurImage, SENSITVITY, 255, cv2.THRESH_BINARY)    

    # Display the resulting frame
    cv2.imshow('frame', threshImage)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
