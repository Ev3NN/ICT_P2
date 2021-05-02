"lempelziv: implements the online Lempel-Ziv compression algorithm"

import math
from typing import Tuple, Dict

import numpy as np


def binary_repr(value: int, width: int) -> np.ndarray:
    "represent an unsigned integer < 2**32 in width bitss"
    return np.unpackbits(np.array([value], dtype='>u8').view(np.uint8))[-width:]


def from_bin(bits: np.ndarray) -> int:
    "returns the value of a binary representation"
    factors = 2 ** np.arange(len(bits))[::-1]
    return np.dot(bits, factors)


def encode_uint(sequence: np.ndarray) -> Tuple[np.ndarray, Dict[bytes, int]]:
    """encode a sequence of uint8 (char), returns the encoded message and the dictionary
    """
    return encode_bits(np.unpackbits(sequence))


def encode_str(msg: str) -> Tuple[str, Dict[str, int], int]:
    """encode an ASCII str, returns the encoded message, the dictionay and the
    size in bits"""

    dictionary = {'': 0}

    next_addr = 1

    prefix_key = ''
    key = ''
    total_size = 0

    encoded = ''

    start = 0
    for end in range(len(msg)+1):
        key = msg[start:end]

        new_word = key not in dictionary
        if new_word or end == len(msg):
            prefix_addr = dictionary[prefix_key]
            if new_word:
                dictionary[key] = next_addr

            if next_addr != 1:
                addr_len = math.ceil(math.log2(next_addr))
                encoded += f'{prefix_addr:0{addr_len}b}'
                total_size += addr_len

            encoded += msg[end-1:end]
            total_size += 8  # an ASCII character

            next_addr += 1

            start = end
            prefix_key = ''
        else:
            prefix_key = key

    return encoded, dictionary, total_size


def encode_bits(sequence: np.ndarray) -> Tuple[np.ndarray, Dict[bytes, int]]:
    """encode a sequence of bits, returns the encoded message and the dictionary
    """
    dictionary = {b'': 0}

    next_addr = 1

    prefix_key = b''
    key = b''

    parts = []

    start = 0
    for end in range(len(sequence)+1):
        key = sequence[start:end].tobytes()

        new_word = key not in dictionary

        if new_word or end == len(sequence):
            prefix_addr = dictionary[prefix_key]
            if new_word:
                dictionary[key] = next_addr

            # first address is skipped
            if next_addr != 1:
                addr_len = math.ceil(math.log2(next_addr))
                parts.append(binary_repr(prefix_addr, addr_len))
            parts.append(sequence[end-1:end])

            next_addr += 1

            start = end
            prefix_key = b''
        else:
            prefix_key = key

    return np.concatenate(parts), dictionary


def decode_bits(encoded: np.ndarray) -> np.ndarray:
    "given a compressed sequence returns the original bit sequence"

    # reverse of Dict[bytes, int] can be list[bytes]
    reverse_dict = [b'']
    decoded = []

    reverse_dict.append(encoded[:1].tobytes())
    decoded.append(np.frombuffer(encoded[:1].tobytes(), dtype=np.uint8))

    length = 1
    count_bkp = 1

    # 1* 1 bits address
    # 2* 2 bits
    # 4* 3 buts
    # ...

    start = 1
    count = count_bkp
    while start != len(encoded):
        if count == 0:
            count_bkp *= 2
            count = count_bkp
            length += 1

        addr = from_bin(encoded[start:start+length])

        start += length
        symbol = encoded[start]
        start += 1

        word = np.frombuffer(reverse_dict[addr], dtype=np.uint8)
        word = np.concatenate([word, np.array([symbol], dtype=np.uint8)])

        decoded.append(word)
        reverse_dict.append(word.tobytes())

        count -= 1

    return np.concatenate(decoded)


def decode_uint(encoded: np.ndarray) -> np.ndarray:
    "given a compressed sequence returns the original uint8 sequence"
    return np.packbits(decode_bits(encoded))


def compress_text_file(path):
    "load an UTF-8 file and compress its content, prints the compression ratio"
    with open(path) as file:
        content = file.read()
        _, _, total_size = encode_str(content)
        print(f'compression ratio: {8*len(content)/total_size}')


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        compress_text_file(sys.argv[1])
