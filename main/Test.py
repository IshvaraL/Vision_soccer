import multiprocessing as mp
import time
from Stream import Stream
from Vision import Vision
from Communication import Comm

if __name__ == "__main__":

    parent_conn, child_conn = mp.Pipe()

    stream = Stream(child_conn)
    vision = Vision(parent_conn)

    comm = Comm()

    str = mp.Process(target=stream.run, args = ())
    vis = mp.Process(target=vision.run, args = ())
    vis.start()
    str.start()

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

        comm.send(msg)

        time.sleep(1)

        if vis.is_alive() is False:
            print("vis died")
            str.terminate()
            str.join()
            break

        if str.is_alive() is False:
            print("str died")
            vis.terminate()
            vis.join()
            break

