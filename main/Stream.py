import multiprocessing as mp
import cv2
from time import sleep
from Calibration import Calibrate

class Stream:

    def __init__(self, pipe=None):
        self.pipe = pipe
        pass

    def run(self):
        print("Starting process stream")
        if self.pipe is None:
            print("There is no pipe\n exiting now...")
            return

        cap = cv2.VideoCapture('../res/test.mkv')
        # cap = cv2.VideoCapture('http://root:pass@10.28.40.98/axis-cgi/mjpg/video.cgi?streamprofile=Soccer&videokeyframeinterval=')
        # cap = cv2.VideoCapture('rtsp://10.28.40.98/axis-media/media.amp?streamprofile=Soccer')
        # cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        cal = Calibrate()

        while True:

            ret, frame = cap.read()
            frame = cal.warp(frame)
            self.pipe.send(frame)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            sleep(0.03)
        cap.release()
        cv2.destroyAllWindows()
        return
