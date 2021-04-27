"hamming: implements Hamming (7, 4) code"

import numpy as np

__MATRIX__ = np.array([
    [1, 0, 0, 0, 1, 0, 1],
    [0, 1, 0, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 1]], dtype=np.uint8)


def encode_uint(message: np.ndarray) -> np.ndarray:
    """encodes a message of uint8 to a binary format with Hamming (7, 4) code

    - message: a np.ndarray(shape=(n,), dtype=np.uint8) the message to encode
    - returns: a np.ndarray(shape=(14*n,), dtype=np.uint8) containing binary \
        values at each element
    """
    return encode_bits(np.unpackbits(message))


def encode_bits(message: np.ndarray) -> np.ndarray:
    """encodes a message of bits to a binary format with Hamming (7, 4) code

    - message: a np.ndarray(shape=(4*n,), dtype=np.uint8) the bits of the \
        message to encode
    - returns: a np.ndarray(shape=(7*n,), dtype=np.uint8) containing binary \
        values at each element
    """

    return np.concatenate([
        np.dot(message[i:i+4], __MATRIX__) % 2 for i in range(0, len(message), 4)
    ])


def __check(part: np.ndarray) -> np.ndarray:
    "part: np.ndarray(shape=(7,), dtype=np.uint8)"

    recomputed = encode_bits(part[:4])
    diff = (part - recomputed) % 2

    syndrome_err = np.sum(diff[-3:])

    # either no detectable error, or
    # only one error detected in the syndrome
    if syndrome_err < 2:
        return recomputed[:4]

    # 2 or 3 error bits in the syndrome
    # change the data bits for the parity bits to agree

    if syndrome_err == 3:
        # flip third bit
        recomputed[2] ^= 1
    elif diff[4] == 0:  # first parity
        recomputed[3] ^= 1
    elif diff[5] == 0:  # second parity
        recomputed[0] ^= 1
    elif diff[6] == 0:  # third parity
        recomputed[1] ^= 1

    return recomputed[:4]


def decode_bits(message: np.ndarray) -> np.ndarray:
    """decodes a message of bits with Hamming (7, 4) code to a binary format.

    - message: a np.ndarray(shape=(7*n,), dtype=np.uint8) the bits of the \
        encoded message with Hamming (7, 4) correction code
    - returns: a np.ndarray(shape=(4*n,), dtype=np.uint8) containing binary \
        values at each element for the most likely message
    """

    parts = []
    for i in range(0, len(message), 7):
        decoded = __check(message[i:i+7])
        parts.append(decoded)
    return np.concatenate(parts)


def decode_uint(message: np.ndarray) -> np.ndarray:
    """decodes a message of bits with Hamming (7, 4) code to a uint8 format.

    - message: a np.ndarray(shape=(14*n,), dtype=np.uint8) the bits of the \
        encoded message with Hamming (7, 4) correction code
    - returns: a np.ndarray(shape=(n,), dtype=np.uint8) containing uint8 \
        values at each element for the most likely message that was encoded
    """
    return np.packbits(decode_bits(message))
