from webcamvideostream import WebcamVideoStream
import cv2
from chArucoTracker import Tracker
#from tracker import Tracker
import requests
import pandas as pd
import numpy as np

targets = False
filename = 'testData.xlsx'
address = 'http://192.168.0.181:3000/'


# puts the data onto the server
if targets:
    df = pd.read_excel(filename)
    for i in range(1, 4):
        data = {'id': i, 't': df['t'].to_list(), 'x': df['x'+str(i)].to_list(), 'y': df['y'+str(i)].to_list()}
        r = requests.put(address + 'targets/' + str(i), data=data)
# open the camera and sets the resolution, frame rate, and focus
vs = WebcamVideoStream(src=0).start()
vs.start()

# declares the aruco tracker
tracker = Tracker(marker_width=0.0685, square_width=0.073, aruco_type="DICT_4X4_1000", address=address)
tracker.startPutThread()
# reads the cap frame by frame and track then display the processed frame
while True:
    ret = vs.grabbed
    frame = vs.frame
    if ret:
        rederedFrame = tracker.find_markerPos(frame)
        # add frame rate to the rendered frame

        cv2.imshow("frame", rederedFrame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print("(" + format(tracker.pos[1][0], '.2f') + ", " + format(tracker.pos[1][1], '.2f') + ", " + format(tracker.pos[1][2], '.2f') + ")" + "(" + format(tracker.pos[2][0], '.2f') + ", " + format(tracker.pos[2]
              [1], '.2f') + ", " + format(tracker.pos[2][2], '.2f') + ")" + "(" + format(tracker.pos[3][0], '.2f') + ", " + format(tracker.pos[3][1], '.2f') + ", " + format(tracker.pos[3][2], '.2f') + ")", end='\r')
# release the camera
vs.stop()
vs.stream.release()
tracker.stopPutThread()
cv2.destroyAllWindows()
