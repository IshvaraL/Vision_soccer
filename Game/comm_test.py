import socket
import pickle
import cv2

HOST = "127.0.0.1"
PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

img2d = cv2.imread('../pics/soccerfield_2d.png', 1)
img2d = cv2.resize(img2d, (0, 0), fx=1.5, fy=1.5)
height, width, cols = img2d.shape
img2d_clean = img2d.copy()

while True:
    s.listen()
    conn, addr = s.accept()

    with conn:
        print("Connected by", addr)
        while True:

            try:
                data = conn.recv(1024)
            except Exception as e:
                break

            if not data:
                break
            else:
                message = pickle.loads(data)
                print(message)
                print("")
                img2d = img2d_clean.copy()
                for data in message:
                    print("Team", data[0])
                    for coords in data[1]:
                        print("Coords", coords)
                        if data[0] is 0:
                            cv2.circle(img2d, coords, 20, (255, 0, 0), -1)
                        elif data[0] is 1:
                            cv2.circle(img2d, coords, 20, (0, 0, 255), -1)

                print("")
                cv2.imshow("test", img2d)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break



