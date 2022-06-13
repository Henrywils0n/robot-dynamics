import cv2
from tracker import Tracker
import requests
import pandas as pd
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
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
# lower focus focuses further away from the camera
focus = 0  # min: 0, max: 255, increment:5
cap.set(28, focus)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)
# declares the aruco tracker
tracker = Tracker(marker_width=0.114, aruco_type="DICT_4X4_1000")
# reads the cap frame by frame and track then display the processed frame
makeframe = True
while True:
    ret, frame = cap.read()
    if ret:
        rederedFrame = tracker.find_markerPos(frame, makeframe)
        for i in range(1, 4):
            # puts the positions onto the server for each agent
            data = {'id': i, 'position': tracker.pos[i]}
            r = requests.put(address + 'agents/' + str(i), data=data)
        # add frame rate to the rendered frame
        if makeframe:
            cv2.imshow("frame", rederedFrame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
# release the camera
cap.release()
cv2.destroyAllWindows()
