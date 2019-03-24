import cv2  # import the OpenCV library
import numpy as np  # import the numpy library

def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a

ix,iy = -1,-1
img2d, img3d = 0,0

coords_2d = []
coords_3d = []

# mouse callback function
# def draw_circle2d(event,x,y,flags,param):
#     global ix,iy
#     global coords_2d
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         cv2.circle(img2d,(x,y),3,(255,0,0),-1)
#         ix,iy = x,y
#         coords_2d.append((ix,iy))

# mouse callback function
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
# cv2.namedWindow('2d image')
# cv2.setMouseCallback('2d image', draw_circle2d)

img2d = cv2.imread('../pics/soccerfield_2d.png', 1)
height, width, cols = img2d.shape

img3d = cv2.imread('../pics/soccerfield_3d.png', 1)

print("Images loaded")

pts_src, pts_dst = 0, 0

try:
    print("Step 1")
    pts_src = np.load("calibrated_3D.npy")
    pts_dst = np.load("calibrated_2D.npy")
    print("3D:", pts_src)
    print("2D:", pts_dst)

except FileNotFoundError as e:
    print("Step 2")
    while(1):
        cv2.imshow('2d image', img2d)
        cv2.imshow('3d image', img3d)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == ord('a'):
            print("3D:", coords_3d)
            print("2D:", coords_2d)
        elif k == ord('d'):
            print("3D:", coords_3d)
            print("2D:", coords_2d)
            break

    cv2.destroyAllWindows()

    # pts_src = np.array([(228, 197), (195, 228), (33, 99), (228, 34)])
    # pts_dst = np.array([(223, 118), (181, 127), (116, 36), (259, 43)])

    # pts_src = np.array([(227, 229), (0, 261), (33, 33), (259, 1)])
    # pts_dst = np.array([(212, 138), (21, 92), (138, 19), (286, 40)])

    pts_dst = np.float32([[0,0],[width,0],[0,height],[width,height]])

    # provide points from image 1
    pts_src = np.float32(coords_3d)
    # corresponding points from image 2
    # pts_dst = np.float32(coords_2d)

    np.save("calibrated_3D", pts_src)
    np.save("calibrated_2D", pts_dst)

# pts_src = np.float32([[295, 94], [473, 126], [123, 136], [327, 228]])
# pts_dst = np.float32([[0,0],[width,0],[0,height],[width,height]])

print("Step 3")
# calculate matrix H
h, status = cv2.findHomography(pts_src, pts_dst)

#550,413
matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
dst = cv2.warpPerspective(img3d, matrix, (width,height))
cv2.imshow("test", dst)

# finally, get the mapping

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

        # provide a point you wish to map from image 1 to image 2
        # a = np.array([[x, y]], dtype='float32')
        # a = np.array([a])

        # pointsOut = cv2.perspectiveTransform(a, h)

        # cv2.circle(img2d, totuple(a[0][0]), 2, (0, 0, 255), -1)
        # cv2.circle(img3d, totuple(pointsOut[0][0]), 2, (0, 0, 255), -1)

        cv2.circle(img2d, (x,y), 2, (0, 0, 255), -1)
        cv2.circle(img3d, (x,y), 2, (0, 0, 255), -1)

cv2.destroyAllWindows()
print("Closing")
