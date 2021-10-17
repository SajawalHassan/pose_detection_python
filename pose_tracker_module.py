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
        results = self.pose.process(imgRgb)

        if draw:
            if results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        else:
            print(results.pose_landmarks)

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
