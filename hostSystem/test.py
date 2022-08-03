import cv2
import numpy as np
# import the mtx from fisheyeCalibration.npz and then correct the image from the webcam
mtx = np.load('fisheyeCalibration.npz')['mtx']
dist = np.load('fisheyeCalibration.npz')['dist']
# import the image from the webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
# set focus to 30
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 30)
# set res to 720p
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # undistort the image
    undistorted = cv2.undistort(frame, mtx, dist, None, mtx)
    # Display the resulting frame
    cv2.imshow('frame', undistorted)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
