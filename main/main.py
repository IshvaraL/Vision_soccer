import multiprocessing as mp
import time
from Stream import Stream
from Vision import Vision
from Communication import Comm


class Main:

    def __init__(self):
        self.stream_parent_conn, self.stream_child_conn = mp.Pipe()

        self.comm_parent_conn, self.comm_child_conn = mp.Pipe()

        self.stream = Stream(self.stream_child_conn)
        self.vision = Vision(self.stream_parent_conn, self.comm_child_conn)

        self.comm = Comm()

        self.str = mp.Process(target=self.stream.run, args=())
        self.vis = mp.Process(target=self.vision.run, args=())

        self.team_coords = None

    def start(self):
        self.str.start()
        time.sleep(1)
        self.vis.start()

        while True:
            if not self.vis.is_alive():
                print("vis died")
                self.str.terminate()
                self.str.join()
                break

            if not self.str.is_alive():
                print("str died")
                self.vis.terminate()
                self.vis.join()
                break
            #
            if self.comm_parent_conn.poll(1):
                self.team_coords = self.comm_parent_conn.recv()
            # #
            # if self.team_coords is not None:
            #     self.msg = self.team_coords
            #     print(self.msg)
            #     self.comm.open()
            #     self.comm.send(self.msg)
            #     self.comm.close()
            # #     # time.sleep(0.5)


if __name__ == "__main__":
    main = Main()
    main.start()




