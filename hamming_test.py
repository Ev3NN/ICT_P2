"test cases for hamming.py"

import unittest as u

from numpy import array, uint8, random, unpackbits
from hamming import decode_uint, encode_uint, encode_bits, decode_bits


class TestHamming(u.TestCase):
    "handles testing hamming function"

    def check_bit_pair(self, msg: array, exp: array):
        enc = encode_bits(msg)
        diff = enc != exp

        self.assertFalse(
            diff.any(), msg=f'\n\t{enc}=encode_bits({msg})\n\t{exp}')

        dec = decode_bits(enc)
        diff = dec != msg

        self.assertFalse(
            diff.any(), msg=f'\n\t{dec}=decode_bits({dec})\n\t{msg}')

    def test_bit_pairs(self):
        pairs = {
            '0000': '0000000',
            '0001': '0001011',
            '0010': '0010111',
            '0011': '0011100',
            '0100': '0100110',
            '0101': '0101101',
            '0110': '0110001',
            '0111': '0111010',
            '1000': '1000101',
            '1001': '1001110',
            '1010': '1010010',
            '1011': '1011001',
            '1100': '1100011',
            '1101': '1101000',
            '1110': '1110100',
            '1111': '1111111',
        }

        for message, encoded in pairs.items():
            msg = array([int(val) for val in message], dtype=uint8)
            exp = array([int(val) for val in encoded], dtype=uint8)

            self.check_bit_pair(msg, exp)

    def check_uint_pair(self, msg: array, exp: array):
        enc = encode_uint(msg)
        diff = enc != exp

        self.assertFalse(
            diff.any(), msg=f'\n\t{enc}=encode_uint({msg})\n\t{exp}')

        dec = decode_uint(enc)
        diff = dec != msg

        self.assertFalse(
            diff.any(), msg=f'\n\t{dec}=decode_uint({dec})\n\t{msg}')

    def test_uint_pairs(self):
        pairs = {
            0*8+0*4+0*2+0: '0000000',
            0*8+0*4+0*2+1: '0001011',
            0*8+0*4+1*2+0: '0010111',
            0*8+0*4+1*2+1: '0011100',
            0*8+1*4+0*2+0: '0100110',
            0*8+1*4+0*2+1: '0101101',
            0*8+1*4+1*2+0: '0110001',
            0*8+1*4+1*2+1: '0111010',
            1*8+0*4+0*2+0: '1000101',
            1*8+0*4+0*2+1: '1001110',
            1*8+0*4+1*2+0: '1010010',
            1*8+0*4+1*2+1: '1011001',
            1*8+1*4+0*2+0: '1100011',
            1*8+1*4+0*2+1: '1101000',
            1*8+1*4+1*2+0: '1110100',
            1*8+1*4+1*2+1: '1111111',
        }

        for message, encoded in pairs.items():
            msg = array([message], dtype=uint8)
            # prefix by 4 0 bit for the encoding
            exp = array([int(val) for val in '0000000'+encoded], dtype=uint8)

            self.check_uint_pair(msg, exp)

    def test_recovery(self):
        pairs = {
            '0101111': '0101',
            '0101110': '0100',
        }

        for encoded, message in pairs.items():
            enc = array([int(val) for val in encoded], dtype=uint8)
            exp = array([int(val) for val in message], dtype=uint8)

            diff = decode_bits(enc) != exp
            self.assertFalse(diff.any())

    def test_random_bits(self):
        msg = random.random((256,)) < 0.5
        msg = msg.view(uint8)

        encoded = encode_bits(msg)
        decoded = decode_bits(encoded)

        diff = decoded != msg

        self.assertFalse(diff.any())

    def test_random_uints(self):
        msg = random.randint(0, 256, size=(256,), dtype=uint8)

        encoded = encode_uint(msg)
        decoded = decode_uint(encoded)

        diff = decoded != msg

        self.assertFalse(diff.any())

    def test_single_error_recovery(self):

        for value in range(16):
            expected = unpackbits(array([value], dtype=uint8))[-4:]
            encoded = encode_bits(expected)

            for i in range(7):
                body = encoded.copy()
                body[i] ^= 1 # flip 1 bit
                actual = decode_bits(body)
                
                diff = expected != actual
                self.assertFalse(diff.any())


if __name__ == "__main__":
    u.main()
