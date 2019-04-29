import cv2
import numpy as np


class Localise:

    def __init__(self):
        pass

    def filter_out_green(self, img, greenfilter):

        # lower_green = np.array([20, 50, 50])
        # upper_green = np.array([85, 255, 220])

        lower_green = np.array([greenfilter['LowHue'], greenfilter['LowSaturation'], greenfilter['LowValue']])
        upper_green = np.array([greenfilter['HighHue'], greenfilter['HighSaturation'], greenfilter['HighValue']])

        # cv2.imwrite('test.jpeg', im)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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

    def filter_out_red(self, img, redfilter):
        # lower_red = np.array([0, 60, 70])
        # upper_red = np.array([35, 180, 180])

        lower_red = np.array([redfilter['LowHue'], redfilter['LowSaturation'], redfilter['LowValue']])
        upper_red = np.array([redfilter['HighHue'], redfilter['HighSaturation'], redfilter['HighValue']])

        lower_pink = np.array([166, 197, 169])
        upper_pink = np.array([183, 255, 255])

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        maskr = cv2.inRange(hsv, lower_red, upper_red)
        maskp = cv2.inRange(hsv, lower_pink, upper_pink)

        mask = cv2.bitwise_or(maskr, maskp)

        # mask = cv2.bitwise_not(mask)
        img = cv2.bitwise_and(img, img, mask=mask)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, None, iterations=2)
        # cv2.imshow("red3", mask)
        # cv2.waitKey(0)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=5)
        # cv2.imshow("red4", mask)
        # cv2.waitKey(0)
        mask = cv2.Canny(mask, 100, 200)
        # cv2.imshow("red5", mask)
        # cv2.waitKey(0)
        kernel = np.ones((1, 1), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        # cv2.imshow('red6', mask)

        cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        coords = []

        # loop over the contours
        for c in cnts:
            # compute the center of the contour
            M = cv2.moments(c)
            try:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                coords.insert(0, (cX, cY))

            except Exception as e:
                break

        if len(coords) < 4 :
            for x in range(len(coords), 4, 1):
                coords.append((0, 0))

        return img, coords

    def filter_out_blue(self, img, bluefilter):
        # lower_blue = np.array([70, 40, 40])
        # upper_blue = np.array([140, 255, 255])

        lower_blue = np.array([bluefilter['LowHue'], bluefilter['LowSaturation'], bluefilter['LowValue']])
        upper_blue = np.array([bluefilter['HighHue'], bluefilter['HighSaturation'], bluefilter['HighValue']])

        # img = cv2.blur(img,(10,10))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # mask = cv2.bitwise_not(mask)
        img = cv2.bitwise_and(img, img, mask=mask)
        # cv2.imshow("blue1", mask)

        kernel = np.ones((6, 6), np.uint8)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
        # mask = cv2.erode(mask, kernel, iterations=3)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow('blue3', mask)

        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # cv2.imshow("blue4", mask)

        # cv2.waitKey(0)
        kernel = np.ones((5, 5), np.uint8)
        # mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
        # cv2.imshow("blue5", mask)

        # cv2.waitKey(0)
        mask = cv2.Canny(mask, 100, 200)
        # cv2.imshow("blue6", mask)
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
                coords.append((cX, cY))

            except Exception as e:
                break

        if len(coords) < 4:
            for x in range(len(coords), 4, 1):
                coords.append((0, 0))

        return img, coords
