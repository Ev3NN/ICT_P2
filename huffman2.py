"huffman2: huffman encoding"

import heapq
from typing import Dict, Any, Sequence, Tuple


def __finilize(tree: Tuple, representation: Sequence[str], prefix: str = '') -> None:
    """given a tree as a pair (prob, subtree), a representation as a list of 
    representation per index and a prefix as a string; updates the
    representation such that representation[i] is the binary representation of
    the value for the i-th node (as a str object)"""

    if isinstance(tree, int):
        # tree is the index
        representation[tree] = prefix
        return

    left, right = tree

    __finilize(left[1], representation, prefix+'0')
    __finilize(right[1], representation, prefix+'1')


def build_list(table: Sequence[float]) -> Sequence[str]:
    """given a list of probabilities, return a list of representation using the
    same index for each value"""

    if len(table) == 0:
        return []
    elif len(table) == 1:
        return ['0']

    heap = []
    for i, prob in enumerate(table):
        heapq.heappush(heap, (prob, i))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        heapq.heappush(heap, (left[0] + right[0], (left, right)))

    tree = heapq.heappop(heap)
    representation = len(table) * ['']

    __finilize(tree[1], representation)
    return representation


def build_dict(table: Dict[Any, float]) -> Dict[Any, str]:
    """given a mapping from keys to probabilities, returns a mapping from keys
    to the huffman encoding for these object base of the probabilities"""

    probabilities = table.values()
    return dict(zip(table.keys(), build_list(probabilities)))


if __name__ == "__main__":
    print(build_list([0.1, 0.2, 0.2, 0.3, 0.2]))
    print(build_dict({'A': 0.05, 'B': 0.1, 'C': 0.15,
                      'D': 0.15, 'E': 0.2, 'F': 0.35}))
    print(build_dict({}))
    print(build_dict({'A': 1.0}))
