"""
Code authored by Keegan Kelly
"""
import cv2
import numpy as np
import time
import asyncio
import aiohttp
import requests
from ast import Pass
from threading import Thread
from webcamvideostream import WebcamVideoStream


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

    def __init__(self, marker_width, aruco_type, address, fps=60):
        self.markerWidth = marker_width
        self.arucoDict = cv2.aruco.Dictionary_get(self.ARUCO_DICT[aruco_type])
        self.arucoParams = cv2.aruco.DetectorParameters_create()
        self.arucoParams.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
        self.startTime = time.perf_counter()
        self.address = address
        self.frameRate = fps

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
        self.endTime = time.perf_counter()
        dt = (self.endTime - self.startTime)
        self.startTime = self.endTime
        # preventing division by zero error
        if dt != 0:
            cv2.putText(frame, "FPS: " + format(1/dt, '.2f'), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # prints data
        LINE_UP = '\033[1A'
        LINE_CLEAR = '\x1b[2K'
        print(LINE_UP + LINE_CLEAR + "(" + format(self.pos[1][0], '.2f') + ", " + format(self.pos[1][1], '.2f') + ", " + format(self.pos[1][2], '.2f') + ")" + "(" + format(self.pos[2][0], '.2f') + ", " +
              format(self.pos[2][1], '.2f') + ", " + format(self.pos[2][2], '.2f') + ")" + "(" + format(self.pos[3][0], '.2f') + ", " + format(self.pos[3][1], '.2f') + ", " + format(self.pos[3][2], '.2f') + ")")
        return frame

    # generates task list of put requests for the asyc function
    def get_tasks(self, session, data):
        tasks = []
        for i in range(0, 3):
            tasks.append(session.put(self.address + 'agents/' + str(i+1), json=data[i]))
        return tasks

    # async function that sends the data to the server

    async def put_data(self, data):
        # put the data to the server
        async with aiohttp.ClientSession() as session:
            tasks = self.get_tasks(session, data)
            try:
                await asyncio.gather(*tasks)
            except:
                Pass

    def startThreads(self):
        # starts threads for reading in new frames, displaying frames, processing frames, and sending data to the server
        self.Stop = False
        self.runGetFrame(frameRate=self.frameRate)
        t2 = Thread(target=self.runProcessFrame)
        t2.daemon = False
        t2.start()
        t3 = Thread(target=self.runShowFrame)
        t3.daemon = False
        t3.start()
        t1 = Thread(target=self.runPutThread)
        t1.daemon = False
        t1.start()
        t4 = Thread(target=self.checkReady)
        t4.daemon = False
        t4.start()
        return self

    # ends the thread for put requests

    def stopThread(self):
        # stops all threads
        self.Stop = True
        self.vs.stop()
        self.vs.stream.release()
        cv2.destroyAllWindows()

    # calls the async function infinitely in a thread to constantly update the server

    def runPutThread(self):
        data = [{'id': 1, 'position': self.pos[1].tolist()}, {'id': 2, 'position': self.pos[2].tolist()}, {'id': 3, 'position': self.pos[3].tolist()}]
        asyncio.run(self.put_data(data))
        prevtime = time.perf_counter()
        while(True):
            if self.Stop:
                return
            # threshold on difference in positions to stop excess put requests (the 3cm/0.03rad is just above the noise level)
            # time given to prevent needing to compute the difference in positions every time since the ptu requests take about than 0.08 seconds to compute
            if (time.perf_counter() - prevtime > 0.07):
                data = [{'id': 1, 'position': self.pos[1].tolist()}, {'id': 2, 'position': self.pos[2].tolist()}, {'id': 3, 'position': self.pos[3].tolist()}]
                prevtime = time.perf_counter()
                asyncio.run(self.put_data(data))

    def runProcessFrame(self):
        # finds markers in the most recent frame in a loop
        while(True):
            if self.Stop:
                return
            if self.vs.grabbed:
                self.outFrame = self.find_markerPos(self.vs.frame)

    def runGetFrame(self, frameRate):
        # initializes the video stream
        self.vs = WebcamVideoStream(src=0, fps=frameRate).start()
        self.vs.start()
        # sets an initial outframe to prevent crashing before the first frame is processed
        self.outFrame = self.vs.frame

    def runShowFrame(self):
        prevTime = time.time()
        frameDelta = 1/self.frameRate
        while(True):
            # stops loop if thread is stopped
            if self.Stop:
                return
            # shows frame
            if self.vs.grabbed:
                prevTime = time.time()
                cv2.imshow('frame', self.outFrame)
            # stops all threads when q is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stopThread()
                break
            # reloads the origin position if r is pressed
            if cv2.waitKey(1) & 0xFF == ord('r'):
                self.originFound = False
            sleepTime = frameDelta - (time.time() - prevTime)
            time.sleep(sleepTime*(sleepTime > 0))
        return self

    # checks if all 3 agents are ready and then sets the start flag to true
    def checkReady(self):
        prevTime = time.time()
        while True:
            if (time.time() - prevTime) > 1:
                prevTime = time.time()
                req = requests.get(self.address+"agentReady")
                DATA = req.json()
                SUM = 0
                for i in range(3):
                    SUM += DATA[i]["ready"]
                if SUM == 3:
                    requests.put(self.address+"agentGo/1", json={'ready': 1})
                    break
