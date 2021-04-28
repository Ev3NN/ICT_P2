import lempelziv
import numpy as np


if __name__ == "__main__":
    msg, _ = lempelziv.encode_bits(np.array([1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0], dtype=np.uint8))
    expected = np.array([1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], dtype=np.uint8)
    
    if (msg != expected).any():
        print("failed!")
    
    #genome = np.fromfile('genome.txt', dtype=np.uint8)
    # ''.join(open('genome.txt').read().split('\n'))
    try:
        genome_sl = np.fromfile('genome_sl.txt', dtype=np.uint8)
    except FileNotFoundError as e:
        fout = open('genome_sl.txt', 'w')
        fout.write(''.join(open('genome.txt').read().split('\n')))
        fout.close()
        genome_sl = np.fromfile('genome_sl.txt', dtype=np.uint8)
    
    genome_sl_enc, _ = lempelziv.encode_uint(genome_sl)

    print('compression ratio (ignoring non ACTG characters, input encoded with 8 bits per symbol)')
    print(f'\t{len(genome_sl) * 8 / len(genome_sl_enc)}')
    print(f'{len(genome_sl):7} = number of characters')
    print(f'{len(genome_sl_enc):7} = number of encoded bits')

