import cv2
import numpy as np
# import imutilss
import multiprocessing as mp
from time import sleep

from Localisation import localise

class Vision:

    def __init__(self, pipe=None):
        self.pipe = pipe
        pass

    def run(self):
        print("Starting process vision")
        if self.pipe is None:
            print("There is no pipe\nExiting now...")
            return

        loc = localise()

        while True:
            frame = self.pipe.recv()

            img = loc.get_calibration_coords(frame)

            cv2.imshow('img', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        return





