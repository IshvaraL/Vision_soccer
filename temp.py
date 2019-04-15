# import the necessary packages
from imutils.video import FPS
import numpy as np
import cv2
import imutils

stream = cv2.VideoCapture('http://root:pass@10.28.40.98/axis-cgi/mjpg/video.cgi?streamprofile=Soccer&videokeyframeinterval=')
fps = FPS().start()

# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video file stream
    grabbed, frame = stream.read()

    # if the frame was not grabbed, then we have reached the end
    # of the stream
    if not grabbed:
        break

    # resize the frame and convert it to grayscale (while still
    # retaining 3 channels)
    # frame = imutils.resize(frame, width=450)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = np.dstack([frame, frame, frame])

    # display a piece of text to the frame (so we can benchmark
    # fairly against the fast method)
    # cv2.putText(frame, "Slow Method", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # show the frame and update the FPS counter
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
    fps.update()


# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()



# def max_rgb_filter(image):
#     # split the image into its BGR components
#     (B, G, R) = cv2.split(image)
#
#     # find the maximum pixel intensity values for each
#     # (x, y)-coordinate,, then set all pixel values less
#     # than M to zero
#     M = np.maximum(np.maximum(R, G), B)
#     R[R < M] = 0
#     G[G < M] = 0
#     B[B < M] = 0
#
#     # merge the channels back together and return the image
#     return cv2.merge([B, G, R])
#
#
# # load the image, apply the max RGB filter, and show the
# # output images
# image = cv2.imread('./test.jpg')
# filtered = max_rgb_filter(image)
# cv2.imshow("Images", np.hstack([image, filtered]))
# cv2.waitKey(0)