"lempelziv: implements the online Lempel-Ziv compression algorithm"

# TODO: what representation should the encoding have?

from typing import Sequence, Tuple

class LempelZivDict:

    def __init__(self) -> None:
        self.store = dict()
        self.words = []
        self.max_value = 0
    
    def contains(self, key: str) -> bool:
        return key in self.store
    
    def add(self, key: str) -> int:
        self.store[key] = self.max_value
        self.max_value += 1
        self.words.append(key)
        return self.max_value - 1
    
    def get_value(self, key: str) -> int:
        return self.store[key]

    def get_word(self, value: int) -> str:
        return self.words[value]

def encode(sequence: str) -> Tuple[Sequence[int], LempelZivDict]:
    """encode
    """

    mapping = LempelZivDict()
    encoded = list()

    if not sequence:
        return mapping, encoded

    # pass a buffer over the input
    lo = 0
    for hi in range(len(sequence)+1):
        current = sequence[lo:hi]

        # wait until the word is not in the mapping and add it
        if not mapping.contains(current):
            val = mapping.add(current)
            encoded.append(val)
            lo = hi

    # empty the buffer
    val = mapping.get_value(sequence[lo:])
    encoded.append(val)

    return mapping, encoded
    

def decode(mapping: LempelZivDict, encoded: Sequence[int]) -> str:
    """decode
    """
    return ''.join(mapping.get_word(n) for n in encoded)

