import cv2
import numpy as np

img = 0
cal_coords = []

def draw_circle3d(event, x, y, flags, param):
    global ix, iy
    global cal_coords
    global img
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
        ix, iy = x, y
        cal_coords.append((ix, iy))

def get_calibration_coords(img):

    lower = np.array([153, 147, 0])
    upper = np.array([194, 255, 255])

    # cv2.imwrite('test.jpeg', im)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("test1", hsv)
    # cv2.waitKey(0)
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)
    img = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("test2", img)
    # cv2.waitKey(0)
    kernel = np.ones((6, 6), np.uint8)
    mask = cv2.erode(mask, None, iterations=2)
    cv2.imshow("test3", mask)
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
            # coords.append((cX,cY))

        except Exception as e:
            break
    return coords

def manual_calibrate(frame):
    global cal_coords
    cal_coords = []
    global img
    img = frame
    cv2.namedWindow('3d image')
    cv2.setMouseCallback('3d image', draw_circle3d)
    cv2.imshow("3d image", img)
    while len(cal_coords) < 4:
        cv2.imshow("3d image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return cal_coords

# img3d = cv2.imread('../pics/soccerfield_3d.png', 1)
# print(get_calibration_coords(img3d))