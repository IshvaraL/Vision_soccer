import cv2
import numpy as np

from Localisation import Localise
from Calibration import Calibration

#https://medium.com/@kananvyas/player-and-football-detection-using-opencv-python-in-fifa-match-6fd2e4e373f0

CropOffset = 40


class Vision:

    def __init__(self, stream_pipe=None, comm_pipe=None):
        self.stream_pipe = stream_pipe
        self.comm_pipe = comm_pipe
        self.cal = Calibration()
        self.greenfilter = {'LowHue': 30, 'LowSaturation': 0, 'LowValue': 0, 'HighHue': 90, 'HighSaturation': 255, 'HighValue': 255}
        self.redfilter = {'LowHue': 0, 'LowSaturation': 60, 'LowValue': 70, 'HighHue': 35, 'HighSaturation': 180, 'HighValue': 180}
        self.bluefilter = {'LowHue': 70, 'LowSaturation': 40, 'LowValue': 40, 'HighHue': 140, 'HighSaturation': 255, 'HighValue': 255}

    def totuple(self, a):
        try:
            return tuple(self.totuple(i) for i in a)
        except TypeError:
            return a

    def run(self):
        print("Starting process vision")
        if self.stream_pipe is None:
            print("There is no pipe\nExiting now...")
            return

        cv2.namedWindow('greenfilter', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('redfilter', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('bluefilter', cv2.WINDOW_AUTOSIZE)

        for idx in range(0, 6, 1):
            cv2.createTrackbar(list(self.greenfilter.items())[idx][0], 'greenfilter', list(self.greenfilter.items())[idx][1], 255, self.callback)
            cv2.createTrackbar(list(self.redfilter.items())[idx][0], 'redfilter', list(self.redfilter.items())[idx][1], 255, self.callback)
            cv2.createTrackbar(list(self.bluefilter.items())[idx][0], 'bluefilter', list(self.bluefilter.items())[idx][1], 255, self.callback)

        # self.main_program()

        self.test()

        self.stream_pipe.close()
        self.comm_pipe.close()
        cv2.destroyAllWindows()
        return

    def callback(self, x):
        print('Green:', self.greenfilter)
        print('Red:', self.redfilter)
        print('Blue:', self.bluefilter)

    def test(self):
        loc = Localise()
        frame = self.stream_pipe.recv()
        ref = cv2.imread('../pics/soccerfield_2d.png')
        height, width, cols = ref.shape
        self.h = None
        pts_src = None
        refClean = ref.copy()

        try:
            pts_src = np.load("../calibration_data/calibrated_3D.npy")
            pts_dst = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
            self.h, status = cv2.findHomography(pts_src, pts_dst)
        except Exception as e:
            print(e)
            self.coords_3d = self.cal.manual_calibrate(frame)
            if len(self.coords_3d) is 4:
                pts_dst = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
                pts_src = np.float32(self.coords_3d)
                self.h, status = cv2.findHomography(pts_src, pts_dst)
                np.save("../calibration_data/calibrated_3D", pts_src)

        while True:
            frame = self.stream_pipe.recv()
            for idx in range(0, 6, 1):
                self.greenfilter[list(self.greenfilter.items())[idx][0]] = cv2.getTrackbarPos(list(self.greenfilter.items())[idx][0], 'greenfilter')
                self.redfilter[list(self.redfilter.items())[idx][0]] = cv2.getTrackbarPos(list(self.redfilter.items())[idx][0], 'redfilter')
                self.bluefilter[list(self.bluefilter.items())[idx][0]] = cv2.getTrackbarPos(list(self.bluefilter.items())[idx][0], 'bluefilter')

            x,y,w,h = cv2.boundingRect(pts_src)
            frame = frame[y-CropOffset:y+h, x:x+w].copy()

            img, coordsR, coordsB = loc.recognize_players(frame, self.greenfilter, self.redfilter, self.bluefilter)

            dstRed = []
            dstBlue = []

            ref = refClean.copy()
            for coord in coordsR:
                a = np.array([[coord[0]+x, coord[1]+y-CropOffset]], dtype='float32')
                a = np.array([a])
                dstR = cv2.perspectiveTransform(a, self.h)
                dstRed.append((dstR[0][0][0]/width, dstR[0][0][1]/height))

                cv2.circle(ref, self.totuple(dstR[0][0]), 10, (0, 0, 255), -1)

            for coord in coordsB:
                a = np.array([[coord[0]+x, coord[1]+y-CropOffset]], dtype='float32')
                a = np.array([a])
                dstB = cv2.perspectiveTransform(a, self.h)
                dstBlue.append((dstB[0][0][0]/width, dstB[0][0][1]/height))

                cv2.circle(ref, self.totuple(dstB[0][0]), 10, (255, 0, 0), 4)

            cv2.imshow("transform", ref)
            cv2.imshow("found_players", img)

            team_coords = {0: dstBlue, 1: dstRed}

            self.comm_pipe.send(team_coords)

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
        frame = self.stream_pipe.recv()
        height, width, cols = frame.shape
        self.coords_3d = self.cal.manual_calibrate(frame)
        while True:
            frame = self.stream_pipe.recv()
            # self.coords_3d = get_calibration_coords(frame)

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

            gframe = loc.filter_out_green(dst, self.greenfilter)
            rframe, coordsRed = loc.filter_out_red(dst, self.redfilter)
            bframe, coordsBlue = loc.filter_out_blue(dst, self.bluefilter)

            img = cv2.bitwise_or(rframe, bframe)
            # img = cv2.bitwise_or(img, img_no_green)

            img = cv2.bitwise_or(rframe, bframe)

            cv2.imshow('total', img)

            cv2.imshow('greenfilter', gframe)
            cv2.imshow('redfilter', rframe)
            cv2.imshow('bluefilter', bframe)

            team_coords = {0: coordsBlue, 1: coordsRed}

            self.comm_pipe.send(team_coords)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        return
