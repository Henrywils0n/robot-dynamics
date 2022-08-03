import numpy as np
import cv2
import glob
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND + cv2.fisheye.CALIB_FIX_SKEW
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*4, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:4].T.reshape(-1, 2)
# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
images = glob.glob("*.png")
goodImages = 0
for fname in images:
    img = cv2.imread(fname)
    if img is None:
        print("Check file path")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 4), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        goodImages += 1
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        #cv2.drawChessboardCorners(img, (7, 4), corners2, ret)
        #cv2.imshow('img', img)
        # cv2.waitKey(500)
cv2.destroyAllWindows()
N_imm = goodImages
K = np.zeros((3, 3))
D = np.zeros((4, 1))
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_imm)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_imm)]
retval, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
    objpoints,
    imgpoints,
    gray.shape[::-1],
    K,
    D,
    rvecs,
    tvecs,
    calibration_flags,
    (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6))
# estimateNewCameraMatrixForUndistortRectify
newK = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, gray.shape[::-1], np.eye(3), balance=1.0)
np.savez('fisheyeCalibration.npz', mtx=K, dist=D, newMtx=newK, R=np.eye(3))
