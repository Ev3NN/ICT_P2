"sound: handle the sound.wav manipulation (decoding, reencoding, plotting)"

import wave

from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np

import channel
import hamming


def eye(arg):
    "returns its argument without modification"
    return arg


def read(filename: str) -> Tuple[np.ndarray, float]:
    "read a .wav file, returns a buffer to its value and the framerate"
    file = wave.open(filename, 'rb')
    buffer = file.readframes(-1)
    framerate = file.getframerate()
    file.close()
    return np.frombuffer(buffer, dtype=np.uint8), framerate


def write(filein: str, fileout: str, transform=eye) -> None:
    """reads a .wav file, transform its content and write the result.

    - filein: path to the input file
    - fileout: path to the output file
    - transform: transformation to apply to the buffer: this function must take\
        a np.array(shape=(n,), dtype=np.uint8) and returns an array of the same\
        type and shape
    """

    with wave.open(filein, 'rb') as fin:
        with wave.open(fileout, 'wb') as fout:
            fout.setparams(fin.getparams())

            buffer = fin.readframes(-1)
            data_in = np.frombuffer(buffer, dtype=np.uint8)
            data_out = transform(data_in)
            fout.writeframesraw(data_out)


def plot(filename: str) -> None:
    "reads a .wav file and plot its content"
    values, framerate = read(filename)
    time_end = len(values) / framerate
    plt.plot(np.linspace(0, time_end, len(values)), values)
    plt.show()


def compare_plot(filename: str, title='', transform=eye) -> None:
    """reads a .wav file, transform its content and plot a comparison of the \
        content before and after the transformation.

    - filename: path to the input file
    - transform: transformation to apply to the buffer: this function must take\
        a np.array(shape=(n,), dtype=np.uint8) and returns an array of the same\
        type and shape
    """
    values, framerate = read(filename)
    time_end = len(values) / framerate
    time_vals = np.linspace(0, time_end, len(values))

    altered = transform(values)


    _, [ax1, ax2] = plt.subplots(2, 1, sharex=True)

    ax1.set_title(title)
    ax2.set_xlabel('time (s)')

    ax1.plot(time_vals, values)
    ax1.set_ylabel('original values')

    ax2.plot(time_vals, altered)
    ax2.set_ylabel('altered values')

    plt.show()


if __name__ == "__main__":
    compare_plot('sound.wav', 'Alteration from the channel', channel.alter_uint)
    compare_plot('sound.wav', 'Alteration from the channel with Hamming (4, 7)', lambda x: hamming.decode_uint(
        channel.alter_bits(hamming.encode_uint(x))))
    write('sound.wav', 'sound_altered.wav', channel.alter_uint)
    write('sound.wav', 'sound_hamming_altered.wav', lambda x: hamming.decode_uint(
        channel.alter_bits(hamming.encode_uint(x))))
