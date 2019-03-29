import cv2
import numpy as np


class Calibrate:

    def __init__(self):
        self.ix, self.iy = -1, -1
        self.img2d, self.img3d = 0, 0
        self.coords_2d = []
        self.coords_3d = []

    def get_calibration_coords(self, img):
        lower_purple = np.array([145, 80, 60])
        upper_purple = np.array([160, 255, 255])

        # cv2.imwrite('test.jpeg', im)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # cv2.imshow("test1", hsv)
        # cv2.waitKey(0)
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_purple, upper_purple)
        # cv2.imshow("test2", mask)
        # cv2.waitKey(0)
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.erode(mask, None, iterations=1)
        # cv2.imshow("test3", mask)
        # cv2.waitKey(0)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        # cv2.imshow("test4", mask)
        # cv2.waitKey(0)
        mask = cv2.Canny(mask, 100, 200)
        # cv2.imshow("test5", mask)
        # cv2.waitKey(0)
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)
        # cv2.imshow("test7", mask)
        # cv2.waitKey(0)

        cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        coords = []

        # loop over the contours
        for c in cnts:
            # compute the center of the contour
            M = cv2.moments(c)
            try:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                coords.insert(0,(cX,cY))

            except Exception as e:
                break
        return coords

    def totuple(self, a):
        try:
            return tuple(self.totuple(i) for i in a)
        except TypeError:
            return a

    def draw_circle3d(self, event, x, y, flags, param):
        # global ix,iy
        # global coords_3d
        # if event == cv2.EVENT_LBUTTONDBLCLK:
        #     cv2.circle(img3d,(x,y),3,(255,0,0),-1)
        #     ix,iy = x,y
        #     coords_3d.append((ix, iy))
        pass

    def warp(self, img):
        try:
            pts_src = np.load("../calibration_data/calibrated_3D.npy")
            pts_dst = np.load("../calibration_data/calibrated_2D.npy")

            # h, status = cv2.findHomography(pts_src, pts_dst)
            matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
            dst = cv2.warpPerspective(img, matrix, (500, 500))

            return dst

        except FileNotFoundError as e:
            print("Error")


# print("Starting....")
# cv2.namedWindow('3d image')
# cv2.setMouseCallback('3d image', draw_circle3d)
#
# img2d = cv2.imread('../pics/soccerfield_2d.png', 1)
# height, width, cols = img2d.shape
#
# img3d = cv2.imread('../pics/soccerfield_3d.png', 1)
#
# print("Images loaded")
#
# pts_src, pts_dst = 0, 0
#
# try:
#     print("Step 1")
#     pts_src = np.load("../calibration_data/calibrated_3D.npy")
#     pts_dst = np.load("../calibration_data/calibrated_2D.npy")
#
# except FileNotFoundError as e:
#     print("Step 2")
#     while(1):
#         cv2.imshow('2d image', img2d)
#         cv2.imshow('3d image', img3d)
#         k = cv2.waitKey(20) & 0xFF
#         if k == 27:
#             break
#         elif k == ord('a'):
#             coords_3d = get_calibration_coords(img3d)
#             print("3D:", coords_3d)
#             break
#         elif k == ord('d'):
#             print("3D:", coords_3d)
#             break
#
#     cv2.destroyAllWindows()
#
#     pts_dst = np.float32([[0,0],[width,0],[0,height],[width,height]])
#     pts_src = np.float32(coords_3d)
#
#     np.save("../calibration_data/calibrated_3D", pts_src)
#     np.save("../calibration_data/calibrated_2D", pts_dst)
#
#
# print("Step 3")
# h, status = cv2.findHomography(pts_src, pts_dst)
# matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
# dst = cv2.warpPerspective(img3d, matrix, (width, height))
#
# x, y = 70, 128
# img2d_clean = img2d.copy()
# img3d_clean = dst.copy()
#
# print("Step 4")
# while(1):
#     cv2.imshow('2d image', img2d)
#     cv2.imshow('3d image', img3d)
#     k = cv2.waitKey(20) & 0xFF
#     if k == 255:
#         pass
#     else:
#         img2d = img2d_clean.copy()
#         img3d = img3d_clean.copy()
#         if k == 27:
#             break
#         elif k == ord('w'):
#             y = y - 1
#         elif k == ord('a'):
#             x = x - 1
#         elif k == ord('s'):
#             y = y + 1
#         elif k == ord('d'):
#             x = x + 1
#
#         cv2.circle(img2d, (x,y), 2, (0, 0, 255), -1)
#         cv2.circle(img3d, (x,y), 2, (0, 0, 255), -1)
#
# cv2.destroyAllWindows()
# print("Closing")
