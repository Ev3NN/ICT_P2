import lempelziv
import numpy as np


if __name__ == "__main__":
    msg, _ = lempelziv.encode(
        np.array([1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0], dtype=np.uint8))
    expected = np.array([1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], dtype=np.uint8)
    
    if (msg - expected).any():
        print("failed!")
    
    genome = np.fromfile('genome.txt', dtype=np.uint8)
    # ''.join(open('genome.txt').read().split('\n'))
    genome_sl = np.fromfile('genome_sl.txt', dtype=np.uint8)
    
    genome_enc, _ = lempelziv.encode(genome)
    genome_sl_enc, _ = lempelziv.encode(genome_sl)

    print('compression ratio: input supposed as uint8')
    print(f'\t{len(genome) * 8 / len(genome_enc)}')

    print('compression ratio: input supposed as ACTG')
    print(f'\t{len(genome_sl) * 2 / len(genome_sl_enc)}')

