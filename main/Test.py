import multiprocessing as mp
from Stream import Stream
from Vision import Vision

if __name__ == "__main__":

    parent_conn, child_conn = mp.Pipe()

    stream = Stream(child_conn)
    vision = Vision(parent_conn)


    str = mp.Process(target=stream.run, args = ())
    vis = mp.Process(target=vision.run, args = ())
    vis.start()
    str.start()
