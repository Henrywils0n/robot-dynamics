import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
# lower focus focuses further away from the camera
focus = 0  # min: 0, max: 255, increment:5
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, focus)
cap.set(cv2.CAP_PROP_FPS, 60)

while 1:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # get input from user and set the focus
    focus = input("Enter the focus: ")
    cap.set(cv2.CAP_PROP_FOCUS, focus)
    print("Focus is set to: " + str(focus))
