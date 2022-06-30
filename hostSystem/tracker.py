import cv2
import sys
import numpy as np
import datetime
import asyncio
import aiohttp
from ast import Pass
from threading import Thread


class Tracker:
    # importing the camera matrix and distortion coefficients
    # if the file path is working get rid of the folder or add a non relative path
    npfile = np.load("calibration.npz")
    mtx = npfile["mtx"]
    dist = npfile["dist"]
    # declaring the dictionary that will store the corners of the markers at a specific id
    # marker 10 is the origin and then each agent is id 10 + agent number
    Corners = {10: tuple(), 11: tuple(), 12: tuple(), 13: tuple()}
    NUMMARKERS = 4
    # positions of each marker
    pos = np.zeros((NUMMARKERS, 3))
    pos[0] = [0, 0, np.pi/2]
    # bool used to only determine the position of the origin once to eliminate a bit of noise
    originFound = False
    # dictionary of aruco types
    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }
    # constructor that takes the marker width and the aruco type

    def __init__(self, marker_width, aruco_type, address):
        self.markerWidth = marker_width
        self.arucoDict = cv2.aruco.Dictionary_get(self.ARUCO_DICT[aruco_type])
        self.arucoParams = cv2.aruco.DetectorParameters_create()
        self.arucoParams.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
        self.startTime = datetime.datetime.now()
        self.address = address

    def fixAngle(self, angle):
        # return an angle to -pi and pi
        while(angle > np.pi):
            angle -= 2*np.pi
        while(angle < -np.pi):
            angle += 2*np.pi
        return angle

    def find_markerPos(self, frame):
        # accepts a frame and locates markers and updates their positions and draws their position and info onto the frame
        # converts to gray scale and finds the aruco markers
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (corners, ids, rejectedImgPoints) = cv2.aruco.detectMarkers(gray, self.arucoDict, parameters=self.arucoParams)
        # ads the corners to the dictionary if they are detected
        if len(corners) > 0:
            ids.flatten()
            for i in range(len(ids)):
                self.Corners[ids[i][0]] = corners[i]
        # only calculates position if the origin is found. Backup condition if the origin id has found markers because the origin will be marked as found inside the loop (second condition isn't checked if first condition is true)
        if self.originFound or len(self.Corners[10]) != 0:
            # locates the position of the origin marker only once to eliminate a bit of noise (if camera is not rigid and it moves this should be changed)
            if not self.originFound:
                # gets the rotation and translation vector of the origin marker
                self.originR, self.originT, markerpos = cv2.aruco.estimatePoseSingleMarkers(self.Corners[10], self.markerWidth, self.mtx, self.dist)
                # calculates rotation matrix from the rotation vector
                self.rodrigues = cv2.Rodrigues(self.originR[0][0])[0]
                self.originFound = True
            # calculates position of all other markers
            for i in range(1, self.NUMMARKERS):
                # checks if there is a marker found at the specific id
                if len(self.Corners[10+i]) != 0:
                    # finds marker position in the camera reference frame
                    rvec, tvec, markerpos = cv2.aruco.estimatePoseSingleMarkers(self.Corners[i+10], self.markerWidth, self.mtx, self.dist)
                    # finds the difference in position between the origin and the marker and rotates it to the origin reference frame
                    position = np.matmul(self.rodrigues, tvec[0][0]-self.originT[0][0])
                    # rotation matrix of the marker
                    Rod = cv2.Rodrigues(rvec[0][0])[0]
                    # multiply the rotation matrix of the marker with the rotation matrix of the origin and convert it back to a rotation vector. R_Z is the heading and the heading of the origin marker is added to the heading
                    heading = cv2.Rodrigues(np.matmul(self.rodrigues, Rod))[0][2] + np.pi/2
                    # updates the position of the marker
                    self.pos[i] = [position[0], position[1], self.fixAngle(heading)]
                    # drawing axis on the markers
                    cv2.aruco.drawAxis(frame, self.mtx, self.dist, Rod, tvec, self.markerWidth)
        # draws the marker outlines, ids, and position onto the frame

        if self.originFound:
            # draws the axis on the origin marker
            cv2.aruco.drawAxis(frame, self.mtx, self.dist, self.rodrigues, self.originT[0][0], self.markerWidth * 5)
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        # calculating FPS and drawing it onto the frame
        self.endTime = datetime.datetime.now()
        dt = (self.endTime - self.startTime).total_seconds()
        self.startTime = self.endTime
        # preventing division by zero error
        if dt != 0:
            cv2.putText(frame, "FPS: " + format(1/dt, '.2f'), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame

    # generates task list of put requests for the asyc function
    def get_tasks(self, session, data):
        tasks = []
        for i in range(0, 3):
            tasks.append(session.put(self.address + 'agents/' + str(i+1), data=data[i]))
        return tasks

    # async function that sends the data to the server

    async def put_data(self, data):
        # put the data in r1, r2, and r3 into the server
        async with aiohttp.ClientSession() as session:
            tasks = self.get_tasks(session, data)
            try:
                await asyncio.gather(*tasks)
            except:
                Pass

    # starts the thread for put requests

    def startPutThread(self):
        # start the thread that puts the data to the server
        self.Stop = False
        t = Thread(target=self.runPutThread)
        t.daemon = False
        t.start()
        return self

    # ends the thread for put requests

    def stopPutThread(self):
        # stop the thread that puts the data to the server
        self.Stop = True

    # calls the async function infinitely in a thread to constantly update the server

    def runPutThread(self):
        prevSentPos = np.copy(self.pos)
        data = [{'id': 1, 'position': self.pos[1]}, {'id': 2, 'position': self.pos[2]}, {'id': 3, 'position': self.pos[3]}]
        asyncio.run(self.put_data(data))
        while(True):
            if self.Stop:
                return
            # threshold on difference in positions to stop excess put requests (the 3cm/0.03rad is just above the noise level)
            if (np.absolute(self.pos - prevSentPos) > 0.02).any():
                prevSentPos = np.copy(self.pos)
                data = [{'id': 1, 'position': self.pos[1]}, {'id': 2, 'position': self.pos[2]}, {'id': 3, 'position': self.pos[3]}]
                asyncio.run(self.put_data(data))
