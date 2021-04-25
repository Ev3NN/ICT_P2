"channel: simulates a binary symmetric channel"

import numpy as np

def alter_uint(data: np.ndarray, prob=0.01) -> np.ndarray:
    """
    """

    # 1 -> should be flipped
    flip = np.random.random((8*len(data))) < prob
    # mask to XOR with
    mask = np.packbits(flip)

    return np.bitwise_xor(data, mask)

def alter_bits(data: np.ndarray, prob=0.01) -> np.ndarray:
    """
    """

    # 1 -> should be flipped
    flip = np.random.random((len(data))) < prob
    # mask to XOR with
    mask = flip

    return np.bitwise_xor(data, mask)