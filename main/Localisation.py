import cv2
import numpy as np

class localise:

    def __init__(self):
        pass

    def get_calibration_coords(self, img):

        lower_green = np.array([20, 40, 50])
        upper_green = np.array([85, 255, 220])

        # cv2.imwrite('test.jpeg', im)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # cv2.imshow("test1", hsv)
        # cv2.waitKey(0)
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_green, upper_green)
        # cv2.imshow("test2", mask)
        # cv2.waitKey(0)
        # kernel = np.ones((2, 2), np.uint8)
        # mask = cv2.erode(mask, None, iterations=1)
        # cv2.imshow("test3", mask)
        # cv2.waitKey(0)
        # kernel = np.ones((5, 5), np.uint8)
        # mask = cv2.dilate(mask, kernel, iterations=2)
        # cv2.imshow("test4", mask)
        # cv2.waitKey(0)
        # mask = cv2.Canny(mask, 100, 200)
        # cv2.imshow("test5", mask)
        # cv2.waitKey(0)
        # kernel = np.ones((2, 2), np.uint8)
        # mask = cv2.dilate(mask, kernel, iterations=1)
        # cv2.imshow("test7", mask)
        # cv2.waitKey(0)

        mask = cv2.bitwise_not(mask)

        img = cv2.bitwise_and(img, img, mask = mask)

        # cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # coords = []
        #
        # # loop over the contours
        # for c in cnts:
        #     # compute the center of the contour
        #     M = cv2.moments(c)
        #     try:
        #         cX = int(M["m10"] / M["m00"])
        #         cY = int(M["m01"] / M["m00"])
        #         coords.insert(0, (cX, cY))
        #
        #     except Exception as e:
        #         break
        # return coords
        return img