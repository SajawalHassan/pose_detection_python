import cv2 as cv
import mediapipe as mp
import time
import pose_tracker_module as pose_tracker

# Capturing vid (cange filename to 0 if need webcam)
capture = cv.VideoCapture(0)

pTime = 0

while True:
    # Reading currunt frame
    success, img = capture.read()

    # If can't read currunt frame, break loop
    if not success:
          break

    detector = pose_tracker.PoseTracker()

    detector.trackPose(img)

    # Calculate fps
    Ctime = time.time()
    fps = 1/(Ctime - pTime)
    pTime = Ctime

    # Display fps
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

    cv.imshow("Video", img)
    key = cv.waitKey(1)

    if key==27:
        break # If key is pressed, break loop

capture.release()
cv.destroyAllWindows()
