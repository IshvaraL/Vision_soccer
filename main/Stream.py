import multiprocessing as mp
from time import sleep

class Stream:

    def __init__(self, pipe=None):
        self.pipe = pipe
        pass

    def run(self):
        print("Starting process stream")
        if self.pipe is None:
            print("There is no pipe\n exiting now...")
            return

        while True:
            self.pipe.send("Hello")
            sleep(1)
