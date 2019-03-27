import cv2
import numpy as np
# import imutilss
import multiprocessing as mp
from time import sleep

from Localisation import Localise

class Vision:

    def __init__(self, pipe=None):
        self.pipe = pipe
        pass

    def run(self):
        print("Starting process vision")
        if self.pipe is None:
            print("There is no pipe\nExiting now...")
            return

        loc = Localise()

        while True:
            frame = self.pipe.recv()

            img_no_green = loc.filter_out_green(frame)
            img_no_red = loc.filter_out_red(frame)
            img_no_blue = loc.filter_out_blue(frame)

            img = cv2.bitwise_or(img_no_red, img_no_blue)
            img = cv2.bitwise_or(img, img_no_green)

            cv2.imshow('img no green', img_no_green)
            cv2.imshow('img no red', img_no_red)
            cv2.imshow('img no blue', img_no_blue)

            cv2.imshow("Total", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        return





