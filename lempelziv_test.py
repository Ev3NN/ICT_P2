import lempelziv

def test():
    import sys
    sequence = ''.join(open('genome.txt').read().split('\n'))
    # sequence = "ABCD"

    mapping, encoded = lempelziv.encode(sequence)
    res = lempelziv.decode(mapping, encoded)

    if sequence != res:
        print(f'comparison:\n\t{sequence}\n\t{res}')
    else:
        source_size = sys.getsizeof(sequence)
        encoded_size = sys.getsizeof(encoded) + sys.getsizeof(mapping)
        print(f"total size ratio: {encoded_size}/{source_size} = {encoded_size/source_size}")

if __name__ == "__main__":
    test()