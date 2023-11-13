#goals
#detect the video feed from the camera
#create the sliders
#apply the color mask based on the slider values
#print out the current slider state

import cv2 as cv
import numpy as np
import os
import utils
from utils import get_hsv

camera_index = utils.camera_index
cap = cv.VideoCapture(camera_index)
cv.namedWindow("frame")
cv.createTrackbar('H min', 'frame', 0, 179, get_hsv)
cv.createTrackbar('H max', 'frame', 179, 179, get_hsv)
cv.createTrackbar('S min', 'frame', 0, 255, get_hsv)
cv.createTrackbar('S max', 'frame', 255, 255, get_hsv)
cv.createTrackbar('V min', 'frame', 0, 255, get_hsv)
cv.createTrackbar('V max', 'frame', 255, 255, get_hsv)

if not cap.isOpened():
    print("cannot access camera!")
    exit()

while True:
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    h_min = cv.getTrackbarPos('H min', 'frame')
    h_max = cv.getTrackbarPos('H max', 'frame')
    s_min = cv.getTrackbarPos('S min', 'frame')
    s_max = cv.getTrackbarPos('S max', 'frame')
    v_min = cv.getTrackbarPos('V min', 'frame')
    v_max = cv.getTrackbarPos('V max', 'frame')

    lower_limit = np.array([h_min, s_min, v_min])
    upper_limit = np.array([h_max, s_max, v_max])

    mask = cv.inRange(hsv, lower_limit, upper_limit)
    result = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('result', result)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    print(f'H min: {h_min}, H max: {h_max}, S min: {s_min}, S max: {s_max}, V min: {v_min}, V max: {v_max}')

cap.release()
cv.destroyAllWindows()
