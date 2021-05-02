"testfile for lempelziv implementation"

import unittest as u
import numpy as np
import lempelziv as lz


class TestLempelZiv(u.TestCase):
    "handles some tests for the LempelZiv compression"

    def test_bin_repr(self):
        "tests lempelziv.binary_repr"

        self.assertEqual(0, lz.binary_repr(0, 1)[0])
        self.assertEqual(1, lz.binary_repr(1, 1)[0])

        self.assertEqual(5, len(lz.binary_repr(0, 5)))
        self.assertEqual(5, len(lz.binary_repr(1, 5)))

    def test_random_bits_check(self):
        "checks the decoder (binary)"

        for _ in range(100):
            size = np.random.randint(500, 600, size=(1,))
            msg = (np.random.random(size) < 0.5).view(np.uint8)

            encoded, _ = lz.encode_bits(msg)
            decoded = lz.decode_bits(encoded)

            self.assertFalse((msg != decoded).any())

    def test_random_uint_check(self):
        "checks the decoder (uint8)"

        for _ in range(100):
            size = np.random.randint(500, 600, size=(1,))
            msg = np.random.randint(256, size=size, dtype=np.uint8)

            encoded, _ = lz.encode_uint(msg)
            decoded = lz.decode_uint(encoded)

            self.assertFalse((msg != decoded).any())

    def test_example(self):
        "reproduces the theoretical example"
        msg = np.array([1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0], dtype=np.uint8)
        expected = np.array([1, 0, 0, 0, 1, 1, 1, 0, 1, 1,
                             0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], dtype=np.uint8)
        encoded, _ = lz.encode_bits(msg)

        self.assertFalse((encoded != expected).any())

    def compress_bin_genome(self):
        "compress the genome and prints the compression ratio (about 2s)"

        symbols = ['A', 'T', 'C', 'G']
        genome_file = open('genome.txt')
        genome_txt = ''.join(genome_file.read().split('\n'))
        genome_file.close()
        # 0,1,2,3
        genome_int = np.array([symbols.index(a)
                               for a in genome_txt], dtype=np.uint8)
        # get the two lowest bits
        genome_int_bits = np.unpackbits(genome_int)
        genome_int_bit0 = genome_int_bits[7::8]
        genome_int_bit1 = genome_int_bits[6::8]
        # join them
        genome_int_bit_stacked = np.stack([genome_int_bit1, genome_int_bit0])
        genome_bits = genome_int_bit_stacked.transpose().reshape((-1,))

        print(f'{len(genome_bits)=}   ')

        genome_encoded, _ = lz.encode_bits(genome_bits)

        print(f'{len(genome_encoded)=}')
        print(f'compression ratio = {len(genome_bits)}/{len(genome_encoded)}')
        print(f'                  = {len(genome_bits) / len(genome_encoded)}')
        # 1917114 / 2095205 = 0.9150006801243792

    def compress_uint_genome(self):
        "compress the ASCII version of the genome (about 6s)"

        genome_file = open('genome.txt')
        genome_txt = ''.join(genome_file.read().split('\n'))
        genome_file.close()
        # 0,1,2,3
        genome_int = np.frombuffer(genome_txt.encode(), dtype=np.uint8)
        genome_encoded, _ = lz.encode_uint(genome_int)

        print(f'compression ratio = {8*len(genome_int)}/{len(genome_encoded)}')
        print(f'                  = {8*len(genome_int) / len(genome_encoded)}')
        # 7668456 / 3243053 = 2.3645793022809065

    def compress_ascii_genome(self):
        "compress the ASCII version of the genome (about 0.5s)"

        genome_file = open('genome.txt')
        genome_txt = ''.join(genome_file.read().split('\n'))
        genome_file.close()

        _, _, bin_size = lz.encode_str(genome_txt)
        print(f'compression ratio = {8*len(genome_txt)}/{bin_size}')
        print(f'                  = {8*len(genome_txt) / bin_size}')
        # compression ratio = 7668456 / 2697854
        #                   = 2.8424280928471295


if __name__ == "__main__":
    u.main()
