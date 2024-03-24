import multiprocessing
import time
from datetime import datetime


def separate_process():
    # This code will run in a separate process
    print("Separate process started", datetime.now())
    time.sleep(1)
    print("Separate process ended", datetime.now())

    # Your code logic goes here


if __name__ == '__main__':

    for i in (1,2):
        # Create a new process
        process = multiprocessing.Process(target=separate_process)
        # Start the process
        process.start()

    # The main process continues running independently
    print("Main process continuing", datetime.now())