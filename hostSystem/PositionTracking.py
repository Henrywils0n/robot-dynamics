from tracker import Tracker
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
# declares the aruco tracker
tracker = Tracker(marker_width=0.1585, aruco_type="DICT_4X4_1000", address=address)
# starts threads for reading frames, outputing frames, processing frames, and sending data to the server
tracker.startThreads()
