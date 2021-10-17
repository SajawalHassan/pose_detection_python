import cv2 as cv
import mediapipe as mp
import time

class PoseTracker():
    def __init__(self, static_img=False, model_comp=1, landmarks=True, enable_segmentation=False,
     segmentation=True, detection_con=0.5, tracking_con=0.5):

        self.static_img = static_img
        self.model_comp = model_comp
        self.landmarks = landmarks
        self.enable_segmentation = enable_segmentation
        self.segmentation = segmentation
        self.detection_con = detection_con
        self.tracking_con = tracking_con

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
        self.mpDraw = mp.solutions.drawing_utils

    def trackPose(self, img, draw=True):
        # Convert to rgb
        imgRgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        # Process results
        self.results = self.pose.process(imgRgb)

        if draw:
            if self.results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        else:
            print(self.results.pose_landmarks)

    def findPos(self, img, draw=True):

        self.lmList = []

        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape # Get w, h
                cx, cy = int(lm.x * w), int(lm.y * h) # Convert w, h to pixels
                self.lmList.append([id, cx, cy]) # Add updates values to lmList

                if draw:
                    cv.circle(img, (cx, cy), 10, (0, 255, 0), cv.FILLED)

        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):

        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255,255,255), 3)
            cv.line(img, (x2, y2), (x3, y3), (255,255,255), 3)
            cv.circle(img, (x1, y1), 10, (0,0,255), -1)
            cv.circle(img, (x1, y1), 15, (0,0,255), 2)
            cv.circle(img, (x2, y2), 10, (0,0,255), -1)
            cv.circle(img, (x2, y2), 15, (0,0,255), 2)
            cv.circle(img, (x3, y3), 10, (0,0,255), -1)
            cv.circle(img, (x3, y3), 15, (0,0,255), 2)

        

# FOR TESTING PURPOSES!
def main():
    # Capturing vid (cange filename to 0 if need webcam)
    capture = cv.VideoCapture("videos/vid_test_body.3gp")

    pTime = 0

    while True:
        # Reading currunt frame
        success, img = capture.read()

        # If can't read currunt frame, break loop
        if not success:
            break

        detector = PoseTracker()

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


if __name__ == "__main__":
    main()
