import string

def count_lines(src):
    file = open(src, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()

    return line_count


def launch_samples(dest):
    file = open(dest, 'w')
    

    for i in range(1, 1001):
        filename = 'LZ77_STD/LZ77_L={}.txt'.format(i)
        bin_length = len(bin(i)[2:])   

        line_count = count_lines(filename)
        std = (2 * bin_length + 8) * line_count
        adv = (2 * bin_length + 2) * line_count
        sample = str(i) + ', ' + str(std) + ', ' + str(adv) + ', ' + \
            str(7668456 / std) + ', ' + str(7668456 / adv) + '\n'
        file.write(sample)

    file.close()


def main():
    launch_samples('LZ77_points.csv')

if __name__ == "__main__":
    main()