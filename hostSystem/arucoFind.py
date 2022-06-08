import imutils
import cv2
import sys
import numpy as np

NUMMARKERS = 4


class Tracker:
    npfile = np.load("calibration.npz")
    mtx = npfile["mtx"]
    dist = npfile["dist"]
    Corners = {10: tuple(), 11: tuple(), 12: tuple(), 13: tuple()}
    IDS = [10, 11, 12, 13]
    pos = np.zeros((NUMMARKERS, 4))
    numFrames = 0
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

    def __init__(self, marker_width, aruco_type):
        self.markerWidth = marker_width
        self.arucoDict = cv2.aruco.Dictionary_get(self.ARUCO_DICT[aruco_type])
        self.arucoParams = cv2.aruco.DetectorParameters_create()

    def fixAngle(self, angle):
        # return an angle to -pi and pi
        while(angle > np.pi):
            angle -= 2*np.pi
        while(angle < -np.pi):
            angle += 2*np.pi
        return angle

    def find_markerPos(self, frame, makeframe=True):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (corners, ids, rejectedImgPoints) = cv2.aruco.detectMarkers(gray, self.arucoDict, parameters=self.arucoParams)
        if len(corners) > 0:
            ids.flatten()
            for i in range(len(ids)):
                self.Corners[ids[i][0]] = corners[i]
        if len(self.Corners[10]) != 0:

            if self.numFrames == 0:
                self.originR, self.originT, markerpos = cv2.aruco.estimatePoseSingleMarkers(self.Corners[10], self.markerWidth, self.mtx, self.dist)
                self.rodrigues = cv2.Rodrigues(self.originR[0][0])[0]
            # draw axis on the marker
            cv2.aruco.drawAxis(frame, self.mtx, self.dist, self.rodrigues, self.originT[0][0], self.markerWidth * 5)
            self.pos[0] = [0, 0, 0, np.pi/2]
            for i in range(1, NUMMARKERS):
                if len(self.Corners[10+i]) != 0:
                    rvec, tvec, markerpos = cv2.aruco.estimatePoseSingleMarkers(self.Corners[self.IDS[i]], self.markerWidth, self.mtx, self.dist)
                    position = np.matmul(self.rodrigues, tvec[0][0]-self.originT[0][0])
                    Rod = cv2.Rodrigues(rvec[0][0])[0]
                    heading = cv2.Rodrigues(np.matmul(Rod, self.rodrigues))[0][2] + self.pos[0][3]
                    self.pos[i] = [position[0], position[1], position[2], self.fixAngle(heading)]
            self.numFrames += 1
        if makeframe:
            # loop over the detected ArUCo corners
            keys = self.Corners.keys()
            values = self.Corners.values()
            for (markerID, markerCorner) in zip(keys, values):
                if(len(markerCorner) != 0):
                    # extract the marker corners (which are always returned in
                    # top-left, top-right, bottom-right, and bottom-left order)
                    corners = markerCorner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners
                    # convert each of the (x, y)-coordinate pairs to integers
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))
                    # draw the bounding box of the ArUCo detection
                    cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
                    cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
                    cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
                    cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
                    # compute and draw the center (x, y)-coordinates of the ArUco
                    # marker
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
                    # draw the ArUco marker ID on the image
                    cv2.putText(frame, str(markerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    i = markerID-10
                    if i > 4 or i < 0:
                        continue
                    # add position to the frame
                    cv2.putText(frame, "(" + format(self.pos[i][0], '.3f') + ", " + format(self.pos[i][1], '.3f') + ", " + format(self.pos[i][2], '.3f') + ", " + format(self.pos[i][3], '.3f')+")", (topLeft[0], topLeft[1] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame
