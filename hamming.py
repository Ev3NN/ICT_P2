"hamming: implements Hamming (7, 4) code"

import numpy as np

from typing import Tuple

__MATRIX__ = np.array([
    [1, 0, 0, 0, 1, 0, 1],
    [0, 1, 0, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 1]], dtype=np.uint8)

__MASK__ = np.array([
    np.dot(np.unpackbits(np.array([i], dtype=np.uint8))[-4:], __MATRIX__) % 2 for i in range(256)
])

def encode_uint(message: np.ndarray) -> np.ndarray:
    return encode_bits(np.unpackbits(message))

def encode_bits(message: np.ndarray) -> np.ndarray:
    """encodes a message vector into a vector of bits

    params
    ======
    - message: np.ndarray(dtype=np.uint8) vector of uin8 values

    returns
    =======
    - np.ndarray(dtype=np.uint8) vector of bits

    """

    return np.concatenate([
        np.dot(message[i:i+4], __MATRIX__)%2 for i in range(0, len(message), 4)
    ])

def check(part: np.ndarray) -> Tuple[np.ndarray, int]:
    "part: np.ndarray(shape=(7,), dtype=np.uint8)"

    # compute the hamming distance with all known codes
    res = (__MASK__ - part) % 2
    dist = res.sum(axis=1)

    # get the closest one
    idx = dist.argmin()

    return __MASK__[idx], dist[idx]

def decode_bits(message: np.ndarray) -> np.ndarray:

    parts = []
    for i in range(0, len(message), 7):
        decoded, dist = check(message[i:i+7])
        if dist > 1:
            raise Exception(f'unable to decode {message[i:i+7]=}')
        parts.append(decoded[:4])
    return np.concatenate(parts)

def decode_uint(message: np.ndarray) -> np.ndarray:
    return np.packbits(decode_bits(message))

