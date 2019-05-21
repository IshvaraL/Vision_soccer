import cv2
import numpy as np


class Localise:

    def __init__(self):
        pass

    def filter_out_green(self, img, greenfilter):

        # lower_green = np.array([20, 50, 50])
        # upper_green = np.array([85, 255, 220])

        lower_green = np.array([35, 15, 15])
        upper_green = np.array([90, 255, 255])

        lower_green = np.array([30, 0, 0])
        upper_green = np.array([95, 255, 255])

        lower_red = np.array([0, 60, 70])
        upper_red = np.array([35, 180, 180])

        lower_blue = np.array([70, 40, 40])
        upper_blue = np.array([140, 255, 255])

        count = 0
        idx = 0

        # lower_green = np.array([greenfilter['LowHue'], greenfilter['LowSaturation'], greenfilter['LowValue']])
        # upper_green = np.array([greenfilter['HighHue'], greenfilter['HighSaturation'], greenfilter['HighValue']])

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

        res = cv2.bitwise_and(img, img, mask=mask)

        res = cv2.blur(res, (2,2))

        res_bgr = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
        res_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        cv2.imshow("res grey", res_gray)
        cv2.imshow("res", res)

        kernel = np.ones((2, 2), np.uint8)
        thresh = cv2.threshold(res_gray, 10, 255, cv2.THRESH_BINARY_INV)[1]
        cv2.imshow("thresh1", thresh)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cv2.imshow("thresh2", thresh)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        prev = 0
        font = cv2.FONT_HERSHEY_SIMPLEX

        coordsRed = []
        coordsBlue = []

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 3)
            # Detect players
            if (h >= (1.2) * w):
                if (w > 10 and h >= 40):
                    idx = idx + 1
                    player_img = img[y:y + h, x:x + w]
                    cv2.imshow("players", player_img)
                    player_hsv = cv2.cvtColor(player_img, cv2.COLOR_BGR2HSV)
                    # If player has blue jersy
                    mask1 = cv2.inRange(player_hsv, lower_blue, upper_blue)
                    res1 = cv2.bitwise_and(player_img, player_img, mask=mask1)
                    res1 = cv2.cvtColor(res1, cv2.COLOR_HSV2BGR)
                    res1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
                    nzCount = cv2.countNonZero(res1)
                    # print("blue", nzCount)
                    # If player has red jersy
                    mask2 = cv2.inRange(player_hsv, lower_red, upper_red)
                    res2 = cv2.bitwise_and(player_img, player_img, mask=mask2)
                    res2 = cv2.cvtColor(res2, cv2.COLOR_HSV2BGR)
                    res2 = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
                    nzCountred = cv2.countNonZero(res2)
                    # print("red", nzCountred)

                    if (nzCount >= 60):
                        # Mark blue jersy players as france
                        # cv2.putText(img, 'France', (x - 2, y - 2), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        blue_player_posX = x + int(w / 2)
                        blue_player_posY = y + h
                        cv2.circle(img, (blue_player_posX, blue_player_posY), 2, (0, 0, 0), 3)
                        coordsBlue.append((blue_player_posX, blue_player_posY))
                    else:
                        pass
                    if (nzCountred >= 40):
                        # Mark red jersy players as belgium
                        # cv2.putText(img, 'Belgium', (x - 2, y - 2), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                        red_player_posX = x + int(w/2)
                        red_player_posY = y + h
                        cv2.circle(img, (red_player_posX, red_player_posY), 2, (0, 0, 0), 2)
                        coordsRed.append((red_player_posX, red_player_posY))
                    else:
                        pass

        return img, coordsRed, coordsBlue

    def filter_out_red(self, img, redfilter):
        # lower_red = np.array([0, 60, 70])
        # upper_red = np.array([35, 180, 180])
        height, width, cols = img.shape
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
                if len(coords) > 4:
                    break
                coords.insert(0, (cX/width, cY/height))

            except Exception as e:
                break

        if len(coords) < 4 :
            for x in range(len(coords), 4, 1):
                coords.append((0, 0))

        return img, coords

    def filter_out_blue(self, img, bluefilter):
        # lower_blue = np.array([70, 40, 40])
        # upper_blue = np.array([140, 255, 255])
        height, width, cols = img.shape
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
                if len(coords) > 4:
                    break
                coords.insert(0, (cX/width, cY/height))

            except Exception as e:
                break

        if len(coords) < 4:
            for x in range(len(coords), 4, 1):
                coords.append((0, 0))

        return img, coords
