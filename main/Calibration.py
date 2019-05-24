import cv2

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
