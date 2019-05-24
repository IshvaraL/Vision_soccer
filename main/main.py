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
    str.start()
    time.sleep(1)
    vis.start()
    team_coords = None
    while True:
        if not vis.is_alive():
            print("vis died")
            str.terminate()
            str.join()
            break

        if not str.is_alive():
            print("str died")
            vis.terminate()
            vis.join()
            break

        if comm_parent_conn.poll(1):
            team_coords = comm_parent_conn.recv()
        #
        if team_coords is not None:
            msg = team_coords
            print(msg)
        #     comm.open()
        #     comm.send(team_coords)
        #     comm.close()
        #     # time.sleep(0.5)


