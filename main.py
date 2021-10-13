import cv2 as cv
import mediapipe as mp
import time

# Capturing vid (cange filename to 0 if need webcam)
capture = cv.VideoCapture("videos/vid_test_body.3gp")

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

pTime = 0

while True:
    # Reading currunt frame
    success, frame = capture.read()

    # If can't read currunt frame, break loop
    if not success:
          break

    # Convert to rgb
    imgRgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Process results
    results = pose.process(imgRgb)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

    # Calculate fps
    Ctime = time.time()
    fps = 1/(Ctime - pTime)
    pTime = Ctime

    # Display fps
    cv.putText(frame, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

    cv.imshow("Video", frame)
    key = cv.waitKey(1)

    if key==27:
        break # If key is pressed, break loop

capture.release()
cv.destroyAllWindows()
