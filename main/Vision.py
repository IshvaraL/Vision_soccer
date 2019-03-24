import cv2
import numpy as np
# import imutilss
import multiprocessing as mp
from time import sleep

class Vision:

    def __init__(self, pipe=None):
        self.pipe = pipe
        pass

    def run(self):
        print("Starting process vision")
        if self.pipe is None:
            print("There is no pipe\nExiting now...")
            return

        while True:
            print(self.pipe.recv())
            sleep(1)



