import cv2
import numpy as np
from Calibration import get_calibration_coords

ix,iy = -1,-1
img2d, img3d = 0,0
coords_2d = []
coords_3d = []


def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a


def draw_circle3d(event,x,y,flags,param):
    global ix,iy
    global coords_3d
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img3d,(x,y),3,(255,0,0),-1)
        ix,iy = x,y
        coords_3d.append((ix, iy))


print("Starting....")
cv2.namedWindow('3d image')
cv2.setMouseCallback('3d image', draw_circle3d)

img2d = cv2.imread('../pics/soccerfield_2d.png', 1)
height, width, cols = img2d.shape

img3d = cv2.imread('../pics/soccerfield_3d.png', 1)

print("Images loaded")

pts_src, pts_dst = 0, 0

try:
    print("Step 1")
    pts_src = np.load("../calibration_data/calibrated_3D.npy")
    pts_dst = np.load("../calibration_data/calibrated_2D.npy")

except FileNotFoundError as e:
    print("Step 2")
    while(1):
        cv2.imshow('2d image', img2d)
        cv2.imshow('3d image', img3d)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == ord('a'):
            coords_3d = get_calibration_coords(img3d)
            print("3D:", coords_3d)
            break
        elif k == ord('d'):
            print("3D:", coords_3d)
            break

    cv2.destroyAllWindows()

    pts_dst = np.float32([[0,0],[width,0],[0,height],[width,height]])
    pts_src = np.float32(coords_3d)

    np.save("../calibration_data/calibrated_3D", pts_src)
    np.save("../calibration_data/calibrated_2D", pts_dst)


print("Step 3")
h, status = cv2.findHomography(pts_src, pts_dst)
matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
dst = cv2.warpPerspective(img3d, matrix, (width, height))

x, y = 70, 128
img2d_clean = img2d.copy()
img3d_clean = dst.copy()

print("Step 4")
while(1):
    cv2.imshow('2d image', img2d)
    cv2.imshow('3d image', img3d)
    k = cv2.waitKey(20) & 0xFF
    if k == 255:
        pass
    else:
        img2d = img2d_clean.copy()
        img3d = img3d_clean.copy()
        if k == 27:
            break
        elif k == ord('w'):
            y = y - 1
        elif k == ord('a'):
            x = x - 1
        elif k == ord('s'):
            y = y + 1
        elif k == ord('d'):
            x = x + 1

        cv2.circle(img2d, (x,y), 2, (0, 0, 255), -1)
        cv2.circle(img3d, (x,y), 2, (0, 0, 255), -1)

cv2.destroyAllWindows()
print("Closing")
