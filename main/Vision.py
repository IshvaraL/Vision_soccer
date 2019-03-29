import cv2
import numpy as np
# import imutilss
import multiprocessing as mp
from time import sleep

from Localisation import Localise
from Calibration import get_calibration_coords


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
        img2d = cv2.imread('../pics/soccerfield_2d.png', 1)
        img2d = cv2.resize(img2d, (0,0), fx=1.5, fy=1.5)
        height, width, cols = img2d.shape
        img2d_clean = img2d.copy()
        while True:
            frame = self.pipe.recv()
            self.coords_3d = get_calibration_coords(frame)

            if len(self.coords_3d ) is 4:
                pts_dst = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
                pts_src = np.float32(self.coords_3d)
                self.matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
                break

        while True:
            frame = self.pipe.recv()
            dst = cv2.warpPerspective(frame, self.matrix, (width, height))

            cv2.imshow("warp", dst)

            # img_no_green = loc.filter_out_green(frame)
            img_no_red, coordsRed = loc.filter_out_red(dst)
            img_no_blue, coordsBlue = loc.filter_out_blue(dst)

            img2d = img2d_clean.copy()
            for c in coordsRed:

                cv2.circle(img2d, c, 6, (0, 0, 255), -1)

            for c in coordsBlue:

                cv2.circle(img2d, c, 6, (255, 0, 0), -1)

            cv2.imshow('soccer field', img2d)
            img = cv2.bitwise_or(img_no_red, img_no_blue)
            # img = cv2.bitwise_or(img, img_no_green)

            # cv2.imshow('img no green', img_no_green)
            # cv2.imshow('img no red', img_no_red)
            # cv2.imshow('img no blue', img_no_blue)

            cv2.imshow("Total", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        return





