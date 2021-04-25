"hamming: implements Hamming (7, 4) code"

import numpy as np

from typing import Tuple

__MATRIX__ = np.array([
    [1, 0, 0, 0, 1, 0, 1],
    [0, 1, 0, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 1]], dtype=np.uint8)

__MASK__ = np.array([
    np.dot(np.unpackbits(np.array([i], dtype=np.uint8))[-4:], __MATRIX__) % 2 for i in range(8)
])

def encode(message: np.ndarray) -> np.ndarray:
    """encodes a message vector into a vector of bits

    params
    ======
    - message: np.ndarray(dtype=np.uint8) vector of uin8 values

    returns
    =======
    - np.ndarray(dtype=np.uint8) vector of bits

    """

    unpacked = np.unpackbits(message)

    return np.concatenate([
        np.dot(unpacked[i:i+4], __MATRIX__)%2 for i in range(0, len(unpacked), 4)
    ])

def check(part: np.ndarray) -> np.ndarray:
    "part: np.ndarray(shape=(7,), dtype=np.uint8)"

    # compute the hamming distance with all known codes
    res = (__MASK__ - part) % 2
    dist = res.sum(axis=1)

    # get the closest one
    idx = dist.argmin()

    if dist[idx] < 2:
        return __MASK__[idx], 0
    return np.zeros((0,)), 1

def main():
    msg = np.random.random((4,)) < 0.5
    msg = msg.view(np.uint8)

    enc = np.dot(msg, __MATRIX__)%2
    print(f'{enc=}')

    dec = np.dot(enc, __CTRL__)%2
    print(f'{dec=}')

    for i in range(7):
        err = np.zeros((7,), dtype=np.uint8)
        err[i] = 1
        dec = np.dot(err, __CTRL__) % 2
        print(f'{i}: {dec}')

if __name__ == "__main__":
    print(f'{__MASK__=}')
