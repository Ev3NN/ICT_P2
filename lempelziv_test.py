import lempelziv

def match(sequence: str, expected):
    _, encoded = lempelziv.encode(sequence)
    assert(', '.join(encoded) == expected)

def test(sequence: str):
    import sys

    mapping, encoded = lempelziv.encode(sequence)
    res = lempelziv.decode(mapping, encoded)

    assert(sequence == res)

    source_size = sys.getsizeof(sequence)
    encoded_size = sys.getsizeof(encoded) + sys.getsizeof(mapping)
    print(f"total size ratio: {encoded_size}/{source_size} = {encoded_size/source_size}")



if __name__ == "__main__":
    test(''.join(open('genome.txt').read().split('\n')))
    test('1011010100010')
    match('1011010100010', '1, 00, 011, 101, 1000, 0100, 0010')
