#goals
#1. choose either live measurement or .mp4 playback
#2. detect center point on the fidget spinner
#3. detect measurement point on the fidget spinner
#4. calculate angular speed
#5. save values as omega against time

import cv2 as cv
import numpy as np
import utils

fps = 40
x_moving = 0
y_moving = 0
point_center = 0
point_moving = 0
prev_moving_x = 0
prev_moving_y = 0
camera_index = utils.camera_index
kernel = np.ones((5, 5), np.uint8)
a = 0

#color HSV boundaries
lower_blue = np.array([95, 50, 50])
upper_blue = np.array([135, 255, 255])
lower_green = np.array([25, 50, 50])
upper_green = np.array([90, 255, 255])

cap = cv.VideoCapture(camera_index)

if not cap.isOpened():
    print("cannot open camera!")
    exit()



#main loop
while True:
    a += 1
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)




    #BLUE - stationary
    #preprocessing
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    res = cv.bitwise_and(frame, frame, mask=mask_blue)
    gaussian_blur = cv.GaussianBlur(res, (7, 7), 1.5)
    h, s, grayscale = cv.split(gaussian_blur)
    closing = cv.morphologyEx(grayscale, cv.MORPH_CLOSE, kernel)
    circles = cv.HoughCircles(closing, cv.HOUGH_GRADIENT, 0.9, 20, param1 = 50, param2 = 30, minRadius = 30, maxRadius = 60)

    #calculating coordinates
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            point_center = (i[0], i[1])

            #set the center point to be the origin
            x_center = float(point_center[0]) - float(point_center[0])
            y_center = float(point_center[1]) - float(point_center[1]) 
            cv.circle(frame, point_center, 2, (0, 0, 255), 3)
            cv.putText(frame, f'point_center: {x_center}, {y_center}', (0, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)




    #GREEN - moving
    #preprocessing
    mask_green = cv.inRange(hsv, lower_green, upper_green)
    res = cv.bitwise_and(frame, frame, mask=mask_green)
    gaussian_blur = cv.GaussianBlur(res, (7, 7), 1.5)
    h, s, grayscale = cv.split(gaussian_blur)
    closing = cv.morphologyEx(grayscale, cv.MORPH_CLOSE, kernel)
    circles = cv.HoughCircles(closing, cv.HOUGH_GRADIENT, 0.9, 20, param1 = 50, param2 = 30, minRadius = 30, maxRadius = 60)

    #calculating coordinates
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            point_moving = (i[0], i[1])

            #set according to the center point (origin)
            x_moving = float(point_moving[0]) - float(point_center[0])
            y_moving = float(point_moving[1]) - float(point_center[1])
            cv.circle(frame, point_moving, 2, (0, 0, 255), 3)
            cv.putText(frame, f'point_moving: {x_moving}, {y_moving}', (0, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    

    #saving and choose coordinates (when a is odd: save, when a is even: find difference)
    if x_moving and y_moving:
        if a % 2 != 0:
            prev_moving_x = x_moving
            prev_moving_y = y_moving

        if a % 2 == 0:
        #calculate the angle between the hor axis (first coord: initial, second coord: final)
            if point_center and point_moving:
                velocity = utils.get_velocity(prev_moving_x, x_moving, prev_moving_y, y_moving, r=(np.sqrt((y_moving - y_center)**2 + (x_moving - x_center)**2)), fps=fps)
                cv.putText(frame, f'velocity: {velocity}', (0, 90), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)        



    if not ret:
        print("cannot receive frame!")
        break

    cv.imshow(f'processed - source:{camera_index}', frame)

    esc_key = cv.waitKey(1)
    if esc_key == 27:
        break

cap.release()
cv.destroyAllWindows()

