import imutils
import cv2
import sys
import numpy as np

NUMMARKERS = 4


class Tracker:
    npfile = np.load("calibration.npz")
    mtx = npfile["mtx"]
    dist = npfile["dist"]
    Corners = dict.fromkeys([10, 21, 22, 23])
    IDS = [10, 21, 22, 23]
    pos = np.zeros((NUMMARKERS, 4))
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

    def fixAngle(angle):
        # return an angle to -pi and pi
        while(angle > np.pi):
            angle -= 2*np.pi
        while(angle < -np.pi):
            angle += 2*np.pi
        return angle

    def find_markerPos(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (corners, ids, rejectedImgPoints) = cv2.aruco.detectMarkers(gray, self.arucoDict, parameters=self.arucoParams)
        if len(corners) > 0:
            # flatten the ArUco IDs list
            ids = ids.flatten()
            # loop over the detected ArUCo corners
            for (markerCorner, markerID) in zip(corners, ids):
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
        for i in range(len(ids)):
            self.Corners[ids[i]] = corners[i]
        originR, originT, markerpos = cv2.aruco.estimatePoseSingleMarkers(self.Corners[10], self.markerWidth, self.mtx, self.dist)
        rodrigues = cv2.Rodrigues(originR[0][0])[0]
        self.pos[0] = [0, 0, 0, np.pi/2]
        for i in range(1, NUMMARKERS):
            rvec, tvec, markerpos = cv2.aruco.estimatePoseSingleMarkers(self.Corners[self.IDS[i]], self.markerWidth, self.mtx, self.dist)
            position = np.matmul(rodrigues, tvec[0][0]-originT[0][0])
            Rod = cv2.Rodrigues(rvec[0][0])[0]
            heading = cv2.Rodrigues(np.matmul(Rod, rodrigues))[0][2]
            self.pos[i] = [position[0], position[1], position[2], self.fixAngle(self.pos[0][3]+heading[2])]
        return frame
