import cv2
import numpy as np


class Localise:

    def __init__(self):
        self.firstFrame = None
        pass

    def recognize_players(self, img, greenfilter, redfilter, bluefilter):

        if self.firstFrame is None:
            self.firstFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        lower_green = np.array([30, 0, 0])
        upper_green = np.array([95, 255, 255])

        count = 0
        idx = 0

        lower_green = np.array([greenfilter['LowHue'], greenfilter['LowSaturation'], greenfilter['LowValue']])
        upper_green = np.array([greenfilter['HighHue'], greenfilter['HighSaturation'], greenfilter['HighValue']])

        lower_red = np.array([redfilter['LowHue'], redfilter['LowSaturation'], redfilter['LowValue']])
        upper_red = np.array([redfilter['HighHue'], redfilter['HighSaturation'], redfilter['HighValue']])

        lower_blue = np.array([bluefilter['LowHue'], bluefilter['LowSaturation'], bluefilter['LowValue']])
        upper_blue = np.array([bluefilter['HighHue'], bluefilter['HighSaturation'], bluefilter['HighValue']])

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_green, upper_green)

        res = cv2.bitwise_and(img, img, mask=mask)

        # res = cv2.blur(res, (3,3))
        res = cv2.medianBlur(res, 5)
        # res = cv2.GaussianBlur(res,(5,5),0)

        res_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("res grey", res_gray)
        # cv2.imshow("res", res)


        kernel = np.ones((15, 15), np.uint8)
        thresh = cv2.threshold(res_gray, 10, 255, cv2.THRESH_BINARY_INV)[1]
        # cv2.imshow("thresh1", thresh)
        thresh = cv2.erode(thresh, None, iterations=2)
        # cv2.imshow('erode', thresh)
        thresh = cv2.dilate(thresh, kernel, iterations=1)
        # cv2.imshow("thresh2", thresh)

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # frameDelta = cv2.absdiff(self.firstFrame, gray)
        # # frameDelta = cv2.blur(frameDelta, (3, 3))
        # cv2.imshow("test", frameDelta)
        # thresh = cv2.threshold(frameDelta, 60, 150, cv2.THRESH_BINARY)[1]
        # thresh = cv2.dilate(thresh, None, iterations=2)
        # cv2.imshow("test2", thresh)
        # # self.firstFrame = gray

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        prev = 0
        font = cv2.FONT_HERSHEY_SIMPLEX

        coordsRed = []
        coordsBlue = []

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            # Detect players
            if (h >= (1.2) * w):
                if (w > 10 and h >= 35):
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 3)
                    red_player_posX = x + int(w / 2)
                    red_player_posY = y + h
                    coordsRed.append((red_player_posX, red_player_posY))
                    idx = idx + 1
                    player_img = img[y:y + h, x:x + w]
                    # cv2.imshow("players", player_img)
                    player_hsv = cv2.cvtColor(player_img, cv2.COLOR_BGR2HSV)
                    # If player has blue jersy
                    mask1 = cv2.inRange(player_hsv, lower_blue, upper_blue)
                    res1 = cv2.bitwise_and(player_img, player_img, mask=mask1)
                    cv2.imshow('bluefilter', res1)
                    res1 = cv2.cvtColor(res1, cv2.COLOR_HSV2BGR)
                    res1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
                    nzCountBlue = cv2.countNonZero(res1)
                    # print("blue", nzCount)
                    # If player has red jersy
                    mask2 = cv2.inRange(player_hsv, lower_red, upper_red)
                    res2 = cv2.bitwise_and(player_img, player_img, mask=mask2)
                    cv2.imshow('redfilter', res2)
                    res2 = cv2.cvtColor(res2, cv2.COLOR_HSV2BGR)
                    res2 = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
                    nzCountRed = cv2.countNonZero(res2)
                    # print("red", nzCountred)

                    # if nzCountBlue >= 60 and nzCountBlue > nzCountRed:
                    #     # Mark blue jersy players as france
                    #     # cv2.putText(img, 'France', (x - 2, y - 2), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
                    #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    #     blue_player_posX = x + int(w / 2)
                    #     blue_player_posY = y + h
                    #     cv2.circle(img, (blue_player_posX, blue_player_posY), 2, (0, 0, 0), 2)
                    #     coordsBlue.append((blue_player_posX, blue_player_posY))
                    # else:
                    #     pass
                    # if nzCountRed >= 60 and nzCountRed > nzCountBlue:
                    #     # Mark red jersy players as belgium
                    #     # cv2.putText(img, 'Belgium', (x - 2, y - 2), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    #     red_player_posX = x + int(w/2)
                    #     red_player_posY = y + h
                    #     cv2.circle(img, (red_player_posX, red_player_posY), 2, (0, 0, 0), 2)
                    #     coordsRed.append((red_player_posX, red_player_posY))
                    # else:
                    #     pass

        return img, coordsRed, coordsBlue
