from ast import Pass
from webcamvideostream import WebcamVideoStream
import aiohttp
import cv2
from tracker import Tracker
import requests
import pandas as pd
import asyncio
import numpy as np
import aiohttp
targets = False
filename = 'testData.xlsx'
address = 'http://192.168.0.181:3000/'


def get_tasks(session, data):
    tasks = []
    for i in range(0, 3):
        tasks.append(session.put(address + 'agents/' + str(i+1), data=data[i]))
    return tasks


async def put_data(data):
    # put the data in r1, r2, and r3 into the server
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, data)
        try:
            await asyncio.gather(*tasks)
        except:
            Pass

        # puts the data onto the server
if targets:
    df = pd.read_excel(filename)
    for i in range(1, 4):
        data = {'id': i, 't': df['t'].to_list(), 'x': df['x'+str(i)].to_list(), 'y': df['y'+str(i)].to_list()}
        r = requests.put(address + 'targets/' + str(i), data=data)
# open the camera and sets the resolution, frame rate, and focus
vs = WebcamVideoStream(src=0)
vs.start()

# declares the aruco tracker
tracker = Tracker(marker_width=0.114, aruco_type="DICT_4X4_1000")
# reads the cap frame by frame and track then display the processed frame
makeframe = True
while True:
    ret = vs.grabbed
    frame = vs.frame
    if ret:
        rederedFrame = tracker.find_markerPos(frame, makeframe)
        # puts the positions onto the server for each agent
        data = [{'id': 1, 'position': tracker.pos[1].tolist()}, {'id': 2, 'position': tracker.pos[2].tolist()}, {'id': 3, 'position': tracker.pos[3].tolist()}]
        asyncio.run(put_data(data))
        # add frame rate to the rendered frame
        if makeframe:
            cv2.imshow("frame", rederedFrame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
# release the camera
vs.stop()
vs.stream.release()
cv2.destroyAllWindows()
