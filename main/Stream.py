import threading as th
from multiprocessing import RLock
import cv2
import time
import datetime

save = False


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
        self.cap = cv2.VideoCapture('../rec/stream_2019-05-07_12-54-17_Trim.mp4')
        # self.cap = cv2.VideoCapture('../rec/stream_2019-05-07_12-54-17.avi')
        # self.cap = cv2.VideoCapture('http://root:pass@10.42.80.102/axis-cgi/mjpg/video.cgi?streamprofile=Soccer&videokeyframeinterval=')
        if self.cap.isOpened() is False:
            return

        self.showFrame = th.Thread(target=self.show, name="show")
        self.sendFrame = th.Thread(target=self.send, name="send")
        self.sendFrame.start()
        self.showFrame.start()

        while True:
            _, frame = self.cap.read()

            if frame is not None:
                self.lock.acquire()
                self.videoframe = frame
                self.lock.release()
            else:
                break

            if not self.sendFrame.is_alive() or not self.showFrame.is_alive():
                break
            time.sleep(0.010)
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
                cv2.imshow('live', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def increase_brightness(self, img, value=-30):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def decrease_brightness(self, img, value=10):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] -= value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def decrease_saturation(self, img, value=30):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        s[s > lim] = 255
        s[s <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def send(self):
        time.sleep(0.5)
        while True:
            self.lock.acquire()
            frame = self.videoframe
            self.lock.release()

            # frame = self.decrease_brightness(frame)
            # frame = self.decrease_saturation(frame)

            # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert it to hsv
            #
            # h, s, v = cv2.split(hsv)
            # v -= 10
            # h += 20
            # final_hsv = cv2.merge((h, s, v))
            #
            # frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

            self.pipe.send(frame)

            if not self.showFrame.is_alive():
                break

# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/