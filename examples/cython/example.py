"""Send and receive messages with Cython or Python

runs a test with Cython and Python implementation,
comparing results
"""
from multiprocessing import Process

import array
import time

import zmq

from cyzmq_example import cython_sender, mixed_receiver


def python_sender(url, n):
    """Use entirely high-level Python APIs to send messages"""
    ctx = zmq.Context()
    s = ctx.socket(zmq.PUSH)
    s.connect(url)
    buf = array.array('i', [1])
    start = time.perf_counter()
    for i in range(n):
        buf[0] = i
        s.send(buf)
    stop = time.perf_counter()
    # send a final message with the timer measurement
    buf = array.array('d', [stop - start])
    s.send(buf)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="send & recv messages with Cython & Python")
    parser.add_argument("--url", default='tcp://127.0.0.1:5555')
    parser.add_argument("-n", default=10, type=int)
    opts = parser.parse_args()
    n = opts.n
    url = opts.url

    ctx = zmq.Context()
    pull = ctx.socket(zmq.PULL)
    pull.bind(url)
    for label, sender in [("Cython", cython_sender), ("Python", python_sender)]:
        print(f"Sending {n} messages on {url} with {label}")
        background = Process(target=sender, args=(url, n))
        background.start()
        mixed_receiver(pull, n)
        background.join()
        timer_buf = pull.recv()
        # unpack timer message
        a = array.array('d')
        a.frombytes(timer_buf)
        seconds = a[0]
        msgs_per_sec = n / seconds
        print(f"{label}: {msgs_per_sec:10.0f} msgs/sec")


if __name__ == "__main__":
    main()
