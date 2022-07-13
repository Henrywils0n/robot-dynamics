from tracker import Tracker
import requests
import pandas as pd
import numpy as np
from math import ceil

sendPath = False
filename = 'testData.xlsx'
address = 'http://192.168.0.181:3000/'

# puts the target positions onto the server
if sendPath:
    df = pd.read_excel('testData.xlsx')
    allPos = df.to_numpy()
    dt = allPos[1, 0] - allPos[0, 0]
    # split the arrays into chunks of size 15
    numChunks = ceil(len(allPos) / 15)
    allPos = np.array(np.array_split(allPos, numChunks), dtype=object)

    for i in range(3):
        # needs a temp array because the splicing gets screwed up because the split doesnt ensure constant size
        temp = allPos[i]
        for j in range(numChunks):
            # posts the sub array
            # format of the json is id (index of the chunk), total (total number of chunks), dt (time between positions), and pos (the position of the target)
            data = {'id': j+1, 'total': numChunks, 'dt': dt, 'path': temp[:, j+1:j+3].tolist()}
            resp = requests.put(address+"goal"+str(i+1)+"/"+str(j+1), json=data)
            # sends a post if there is a 404 because there isnt one with the id
            if resp.status_code == 404:
                requests.post(address+"goal"+str(i+1)+"/", json=data)

    # checks if there is data on the server beyond the last chunk and then deletes it
    for i in range(3):
        j = numChunks
        while True:
            # HEAD request returns the header from if a GET request is made. If it the code is 404 then there is no data on the server
            resp = requests.head(address+"goal"+str(i+1)+"/"+str(j+1))
            if resp.status_code == 404:
                break
            # code wasnt 404 so there is data in that slot so delete it and increment j to check next id
            else:
                requests.delete(address+"goal"+str(i+1)+"/"+str(j+1))
                j += 1

# declares the aruco tracker class
tracker = Tracker(marker_width=0.1585, aruco_type="DICT_4X4_1000", address=address)
# starts threads for reading frames, outputing frames, processing frames, and sending data to the server
tracker.startThreads()
