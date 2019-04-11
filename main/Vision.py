import cv2
import numpy as np
# import imutilss
import multiprocessing as mp
from time import sleep

from Localisation import Localise
from Calibration import get_calibration_coords


class Vision:

    def __init__(self, stream_pipe=None, comm_pipe=None):
        self.stream_pipe = stream_pipe
        self.comm_pipe = comm_pipe

        # self.greenfilter = {'LowHue': 27, 'LowSaturation': 50, 'LowValue': 50, 'HighHue': 50, 'HighSaturation': 255, 'HighValue': 220}
        # self.redfilter = {'LowHue': 0, 'LowSaturation': 200, 'LowValue': 0, 'HighHue': 25, 'HighSaturation': 255, 'HighValue': 255}
        # self.bluefilter = {'LowHue': 87, 'LowSaturation': 62, 'LowValue': 64, 'HighHue': 150, 'HighSaturation': 255, 'HighValue': 255}

        self.greenfilter = {'LowHue': 36, 'LowSaturation': 23, 'LowValue': 47, 'HighHue': 48, 'HighSaturation': 153, 'HighValue': 203}
        # self.redfilter = {'LowHue': 0, 'LowSaturation': 100, 'LowValue': 79, 'HighHue': 19, 'HighSaturation': 255, 'HighValue': 255}
        # self.redfilter = {'LowHue': 0, 'LowSaturation': 179, 'LowValue': 0, 'HighHue': 179, 'HighSaturation': 255, 'HighValue': 217}
        # self.bluefilter = {'LowHue': 92, 'LowSaturation': 155, 'LowValue': 0, 'HighHue': 126, 'HighSaturation': 255, 'HighValue': 255}

        self.redfilter = {'LowHue': 0, 'LowSaturation': 213, 'LowValue': 226, 'HighHue': 11, 'HighSaturation': 255,
              'HighValue': 255}
        self.bluefilter = {'LowHue': 88, 'LowSaturation': 179, 'LowValue': 110, 'HighHue': 120, 'HighSaturation': 255,
               'HighValue': 175}

    def run(self):
        print("Starting process vision")
        if self.stream_pipe is None:
            print("There is no pipe\nExiting now...")
            return

        cv2.namedWindow('greenfilter')
        cv2.namedWindow('redfilter')
        cv2.namedWindow('bluefilter')

        for idx in range(0, 6, 1):
            cv2.createTrackbar(list(self.greenfilter.items())[idx][0], 'greenfilter', list(self.greenfilter.items())[idx][1], 255, self.callback)
            cv2.createTrackbar(list(self.redfilter.items())[idx][0], 'redfilter', list(self.redfilter.items())[idx][1], 255, self.callback)
            cv2.createTrackbar(list(self.bluefilter.items())[idx][0], 'bluefilter', list(self.bluefilter.items())[idx][1], 255, self.callback)

        # self.main_program()

        self.test()

        cv2.destroyAllWindows()
        return

    def callback(self, x):
        print('Green:', self.greenfilter)
        print('Red:', self.redfilter)
        print('Blue:', self.bluefilter)

    def test(self):
        loc = Localise()
        while True:
            frame = self.stream_pipe.recv()

            for idx in range(0, 6, 1):
                self.greenfilter[list(self.greenfilter.items())[idx][0]] = cv2.getTrackbarPos(list(self.greenfilter.items())[idx][0], 'greenfilter')
                self.redfilter[list(self.redfilter.items())[idx][0]] = cv2.getTrackbarPos(list(self.redfilter.items())[idx][0], 'redfilter')
                self.bluefilter[list(self.bluefilter.items())[idx][0]] = cv2.getTrackbarPos(list(self.bluefilter.items())[idx][0], 'bluefilter')

            gframe = loc.filter_out_green(frame, self.greenfilter)
            rframe, _ = loc.filter_out_red(gframe, self.redfilter)
            bframe, _ = loc.filter_out_blue(gframe, self.bluefilter)

            img = cv2.bitwise_or(rframe, bframe)

            cv2.imshow('total', img)

            cv2.imshow('greenfilter', gframe)
            cv2.imshow('redfilter', rframe)
            cv2.imshow('bluefilter', bframe)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def calibrate_colors(self):
        for idx in range(0, 6, 1):
            self.greenfilter[list(self.greenfilter.items())[idx][0]] = cv2.getTrackbarPos(
                list(self.greenfilter.items())[idx][0], 'greenfilter')
            self.redfilter[list(self.redfilter.items())[idx][0]] = cv2.getTrackbarPos(
                list(self.redfilter.items())[idx][0], 'redfilter')
            self.bluefilter[list(self.bluefilter.items())[idx][0]] = cv2.getTrackbarPos(
                list(self.bluefilter.items())[idx][0], 'bluefilter')

    def max_rgb_filter(self, image):
        # split the image into its BGR components
        (B, G, R) = cv2.split(image)

        # find the maximum pixel intensity values for each
        # (x, y)-coordinate,, then set all pixel values less
        # than M to zero
        M = np.maximum(np.maximum(R, G), B)
        R[R < M] = 0
        G[G < M] = 0
        B[B < M] = 0

        # merge the channels back together and return the image
        return cv2.merge([B, G, R])

    def main_program(self):
        loc = Localise()
        img2d = cv2.imread('../pics/soccerfield_2d.png', 1)
        img2d = cv2.resize(img2d, (0, 0), fx=2, fy=2)
        cv2.imshow("field", img2d)
        height, width, cols = img2d.shape
        while True:
            frame = self.stream_pipe.recv()
            self.coords_3d = get_calibration_coords(frame)

            if len(self.coords_3d) is 4:
                pts_dst = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
                pts_src = np.float32(self.coords_3d)
                self.matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        while True:
            frame = self.stream_pipe.recv()
            for c in self.coords_3d:
                cv2.circle(frame, c, 20, (0, 0, 0), -1)

            dst = cv2.warpPerspective(frame, self.matrix, (width, height))
            self.calibrate_colors()

            dst = cv2.bilateralFilter(dst, 9, 75, 75)

            cv2.imshow("warp", dst)

            # gframe = loc.filter_out_green(dst, self.greenfilter)
            rframe, coordsRed = loc.filter_out_red(dst, self.redfilter)
            bframe, coordsBlue = loc.filter_out_blue(dst, self.bluefilter)

            img = cv2.bitwise_or(rframe, bframe)
            # img = cv2.bitwise_or(img, img_no_green)

            # cv2.imshow('greenfilter', gframe)
            cv2.imshow('redfilter', rframe)
            cv2.imshow('bluefilter', bframe)

            cv2.imshow("Total", img)

            team_coords = {0: coordsBlue, 1: coordsRed}

            self.comm_pipe.send(team_coords)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        return

