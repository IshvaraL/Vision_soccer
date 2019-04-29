import threading as th
from multiprocessing import RLock
import cv2
import time
import datetime

save = True


class Stream:

    def __init__(self, pipe=None):
        self.pipe = pipe
        self.out = None
        self.lock = RLock()
        self.videoframe = None

    def run(self):
        print("Starting process stream")
        if self.pipe is None:
            print("There is no pipe\n exiting now...")
            return

        # self.cap = cv2.VideoCapture('../rec/stream_2019-04-29_10-10-03.avi')
        self.cap = cv2.VideoCapture('http://root:pass@10.28.40.98/axis-cgi/mjpg/video.cgi?streamprofile=Soccer&videokeyframeinterval=')
        if self.cap.isOpened() is False:
            return

        self.showFrame = th.Thread(target=self.show, name="show")
        self.sendFrame = th.Thread(target=self.send, name="send")
        self.sendFrame.start()
        self.showFrame.start()

        while True:
            _, frame = self.cap.read()

            self.lock.acquire()
            self.videoframe = frame
            self.lock.release()

            if not self.sendFrame.is_alive() or not self.showFrame.is_alive():
                break

        self.sendFrame.join()
        self.showFrame.join()
        self.cap.release()
        self.out.release()
        self.pipe.close()
        cv2.destroyAllWindows()
        return

    def show(self):
        time.sleep(0.5)
        lasttime = 0
        update = 31
        strfps = 0
        now = datetime.datetime.now()

        if save:
            self.out = cv2.VideoWriter('../rec/stream_' + now.strftime("%Y-%m-%d_%H-%M-%S") + ".avi",
                                   cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 60,
                                   (int(self.cap.get(3)), int(self.cap.get(4))))

        while True:
            try:
                fps = int(1000000000.0 / (time.time_ns() - lasttime))
            except Exception:
                fps = 0
            lasttime = time.time_ns()

            self.lock.acquire()
            frame = self.videoframe.copy()
            self.lock.release()

            if save:
                save_frame = frame.copy()

            if update > 30:
                update = 0
                strfps = str(fps)
            update += 1

            if frame is not None:
                cv2.putText(frame, strfps, (10, 80), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 4, 2)
                if save:
                    self.out.write(save_frame)
                cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def send(self):
        time.sleep(0.5)
        while True:
            self.lock.acquire()
            frame = self.videoframe
            self.lock.release()

            self.pipe.send(frame)

            if not self.showFrame.is_alive():
                break

# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/