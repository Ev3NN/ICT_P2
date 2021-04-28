"channel: simulates a binary symmetric channel"

import numpy as np


def alter_uint(data: np.ndarray, prob=0.01) -> np.ndarray:
    """flip random bits of the input with probability `prob`

    - data: an array of uint8 encoded in np.uint8 type
    - prob: a float number

    - returns: an array of uint8 of the same length as the input
    """

    return np.packbits(alter_bits(np.unpackbits(data), prob))


def alter_bits(data: np.ndarray, prob=0.01) -> np.ndarray:
    """flip random bits of the input with probability `prob`

    - data: an array of bit (0 or 1) encoded in np.uint8 type
    - prob: a float number

    - returns: an array  of bit of the same length as the input
    """

    # 1 -> should be flipped
    flip = np.random.random((len(data))) < prob
    # mask to XOR with
    mask = flip

    return np.bitwise_xor(data, mask)
