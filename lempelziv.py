"lempelziv: implements the online Lempel-Ziv compression algorithm"

from typing import List, Sequence, Tuple
import math

class LempelZivDict:
    """dictionary implementing fast access to both key and values
    both keys and values must be unique"""

    def __init__(self) -> None:
        # base dict has the empty string at value 0
        self.store = {'': 0}
        self.words = ['']
        self.max_value = 1
    
    def contains(self, key: str) -> bool:
        "returns weither a certain key is present in the dictionary"
        return key in self.store
    
    def add(self, key: str) -> int:
        "add a new word to the dictionary and returns its value"
        self.store[key] = self.max_value
        self.max_value += 1
        self.words.append(key)
        return self.max_value - 1
    
    def get_value(self, key: str) -> int:
        "get the value of a word in the dictionary"
        return self.store[key]

    def get_word(self, value: int) -> str:
        "get the word of a value in the dictionary"
        return self.words[value]

def encode(sequence: str) -> Tuple[List[str], LempelZivDict]:
    """encode:
        - create a sequence encoding the sequence using the LempelZiv algorithm
    
    returns:
        - an encoded sequence as a list of item
        - a dictionary usable to make the decoding
    """

    mapping = LempelZivDict()
    encoded = list()

    if not sequence:
        return mapping, encoded

    # pass a buffer over the input
    lo = 0
    for hi in range(len(sequence)+1):
        current = sequence[lo:hi]

        new_word = not mapping.contains(current)

        # wait until the word is not in the mapping and add it
        if new_word or hi == len(sequence):
            prefix_addr = mapping.get_value(sequence[lo:(hi-1)])
            if new_word:
                current_addr = mapping.add(current)

            if current_addr == 1:
                # encode in 0 bits
                encoded.append(current[-1])
            else:
                addr_len = math.ceil(math.log2(current_addr))
                encoded.append(f"{prefix_addr:0{addr_len}b}{current[-1]}")

            lo = hi

    return mapping, encoded
    

def decode(mapping: LempelZivDict, encoded: Sequence[str]) -> str:
    """decode
        - mapping: the dictionary that was returned with the encoding
        - encoded: the list of encoded value from the LempelZiv algorithm

    returns:
        - the original sequence
    """

    decoded = ''
    for s in encoded:
        # empty address means 0 which is mapped to the empty string
        if len(s) == 1:
            decoded += s
            continue
        # get the address of the prefix
        val = int(s[:-1], 2)
        decoded += mapping.get_word(val) + s[-1]
    return decoded

