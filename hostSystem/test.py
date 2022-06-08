import cv2
import time
from arucoFind import Tracker
# open the camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
tracker = Tracker(marker_width=0.114, aruco_type="DICT_4X4_1000")
# read the cap frame by frame and track then display the processed frame
prevFrameTime = time.process_time()
while True:
    ret, frame = cap.read()
    if ret:
        rederedFrame = tracker.find_markerPos(frame)
        newFrameTime = time.process_time()
        fps = 1 / (newFrameTime - prevFrameTime)
        # add frame rate to the rendered frame
        cv2.putText(rederedFrame, "FPS: " + format(fps, '.2f'), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("frame", rederedFrame)
        prevFrameTime = newFrameTime
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# release the camera
cap.release()
cv2.destroyAllWindows()
