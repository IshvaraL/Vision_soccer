import multiprocessing as mp
import cv2
from time import sleep

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

        while True:

            ret, frame = cap.read()
            self.pipe.send(frame)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            sleep(0.02)
        cap.release()
        cv2.destroyAllWindows()
        return
