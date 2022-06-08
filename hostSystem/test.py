import cv2
import time
from arucoFind import Tracker
# open the camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
focus = 0  # min: 0, max: 255, increment:5
cap.set(28, focus)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
tracker = Tracker(marker_width=0.114, aruco_type="DICT_4X4_1000")
# read the cap frame by frame and track then display the processed frame

while True:
    ret, frame = cap.read()
    if ret:
        rederedFrame = tracker.find_markerPos(frame)
        # add frame rate to the rendered frame
        cv2.imshow("frame", rederedFrame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# release the camera
cap.release()
cv2.destroyAllWindows()
