import time
from contextlib import contextmanager


@contextmanager
def tictoc(measured_in="s"):
    start_time = time.time()
    yield
    end_time = time.time()
    elapsed_time = end_time - start_time

    if measured_in == "ms":
        elapsed_time *= 1000  # Convert to milliseconds

    print(f"The block took {elapsed_time:.5f} {measured_in} to execute.")
