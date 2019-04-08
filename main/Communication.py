import socket
import time
import pickle

HOST = "127.0.0.1"
# PORT = 5005
PORT = 11000


class Comm:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(10)
        self.s.connect((HOST, PORT))
        time.sleep(0.5)

    def send(self, message):
        # data = pickle.dumps(message)
        data = str(message)
        # print(data)
        self.s.send(data.encode())
        self.s.send(b'<EOF>')


if __name__ == "__main__":

    comm = Comm()

    msg = [
        # Header
        # Teams, size per team, total_data
        [["Teams", 0, 1], 3, ["Dynamic: fixed", 6]],

        # Data
        # Team id, coordinates
        [0, [24, 62], ["Old coords"]],
        [0, [44, 22], ["Old coords"]],
        [0, [64, 92], ["Old coords"]],
        [1, [163, 953], ["Old coords"]],
        [1, [545, 439], ["Old coords"]],
        [1, [362, 112], ["Old coords"]]
    ]

    comm.send(msg)