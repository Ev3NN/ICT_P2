"sound: handle the sound.wav manipulation (decoding, reencoding, plotting)"

import sys

import wave

from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np

import channel
import hamming

def eye(x):
    return x

def read(filename: str) -> Tuple[np.ndarray, float]:
    file = wave.open(filename, 'rb')
    buffer = file.readframes(-1)
    framerate = file.getframerate()
    file.close()
    return np.frombuffer(buffer, dtype=np.uint8), framerate

def write(filein: str, fileout: str, transform=eye) -> None:
    with wave.open(filein, 'rb') as fin:
        with wave.open(fileout, 'wb') as fout:
            fout.setparams(fin.getparams())

            buffer = fin.readframes(-1)
            data_in = np.frombuffer(buffer, dtype=np.uint8)
            data_out = transform(data_in)
            fout.writeframesraw(data_out)

def plot(filename: str) -> None:
    values, framerate = read(filename)
    time_end = len(values) / framerate
    plt.plot(np.linspace(0, time_end, len(values)), values)
    plt.show()

def compare_plot(filename: str, transform=eye) -> None:
    values, framerate = read(filename)
    time_end = len(values) / framerate
    time_vals = np.linspace(0, time_end, len(values))

    altered = transform(values)
    
    _, [ax1, ax2] = plt.subplots(2, 1, sharex=True)

    ax1.plot(time_vals, values)
    ax2.plot(time_vals, altered)

    plt.show()

    
if __name__ == "__main__":
    compare_plot(sys.argv[1], channel.alter_uint)
    compare_plot(sys.argv[1], lambda x: hamming.decode_uint(channel.alter_bits(hamming.encode_uint(x))))
