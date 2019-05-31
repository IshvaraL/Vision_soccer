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
        self.wait_timer = time.time_ns()
        try:
            self.s.connect((HOST, PORT))
        except:
            print("Could not connect to game")
        time.sleep(0.5)

    def send(self, message):
        data = str(message)
        print(data)
        try:
            self.s.send(data.encode())
            self.s.send(b'<EOF>')
        except:
            self.open()

    def close(self):
        self.s.close()
        self.s = None

    def open(self):
        if self.s is None:
          self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.s.settimeout(1)
          try:
              if time.time_ns() > self.wait_timer:
                  self.s.connect((HOST, PORT))
                  print("Connected")
          except:
                self.wait_timer = time.time_ns() + 5000000000
                print("Could not connect")


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

    while True:
        comm.open()
        comm.send(msg)
        comm.close()
        time.sleep(2)
        print(msg)