import multiprocessing as mp
import time
from Stream import Stream
from Vision import Vision
from Communication import Comm

if __name__ == "__main__":

    stream_parent_conn, stream_child_conn = mp.Pipe()

    comm_parent_conn, comm_child_conn = mp.Pipe()

    stream = Stream(stream_child_conn)
    vision = Vision(stream_parent_conn, comm_child_conn)

    # comm = Comm()

    str = mp.Process(target=stream.run, args=())
    vis = mp.Process(target=vision.run, args=())
    vis.start()
    str.start()



    while True:
        team_coords = comm_parent_conn.recv()

        msg = team_coords
        # comm.send(msg)

        # time.sleep(1)

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

