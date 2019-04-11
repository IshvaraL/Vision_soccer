import multiprocessing as mp
import cv2
import time
import datetime

class Stream:

    def __init__(self, pipe=None):
        self.pipe = pipe
        self.out = None
        self.lasttime = 0
        pass

    def run(self):
        print("Starting process stream")
        if self.pipe is None:
            print("There is no pipe\n exiting now...")
            return

        # cap = cv2.VideoCapture('../res/test.mkv')
        cap = cv2.VideoCapture('http://root:pass@10.28.40.98/axis-cgi/mjpg/video.cgi?streamprofile=Soccer&videokeyframeinterval=')
        # cap = cv2.VideoCapture('rtsp://10.28.40.98/axis-media/media.amp?streamprofile=Soccer')
        # cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if cap.isOpened() is False:
            return
        now = datetime.datetime.now()
        self.out = cv2.VideoWriter('../rec/stream_' + now.strftime("%Y-%m-%d_%H-%M-%S") + ".avi" , cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 12, (int(cap.get(3)), int(cap.get(4))))
        while True:
            ret, frame = cap.read()

            fps = 1000000000.0 / (time.time_ns() - self.lasttime)
            self.lasttime = time.time_ns()
            print("Fps:", fps)

            resized = cv2.resize(frame, None, fx=0.6, fy=0.6)

            self.pipe.send(resized)
            cv2.imshow('frame', resized)

            self.out.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.03)
        cap.release()
        self.out.release()
        cv2.destroyAllWindows()
        return
