import cv2
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
focus = 0  # min: 0, max: 255, increment:5
cap.set(28, focus)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)
# show the camera and increment the focus every 2 seconds
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("frame", frame)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
    cap.set(28, focus)
