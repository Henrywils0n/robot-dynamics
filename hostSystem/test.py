import cv2
import numpy as np
import time
from arucoFind import Tracker
frame = cv2.imread("hostSystem/all4.jpg")
startTime = time.perf_counter()
tracker = Tracker(marker_width=0.114, aruco_type="DICT_4X4_1000")
endTime = time.perf_counter()
print(endTime-startTime)
fps = 1/(endTime-startTime)
print(fps)
rederedFrame = tracker.find_markerPos(frame)
# show the frame
cv2.imshow("Frame", rederedFrame)
cv2.waitKey(0)
cv2.destroyAllWindows()
