import huffman as huf
import lz77 as lz
import string

def lz77_genome(src, dest):
    file = open(src, 'r')

    look_ahead_buffer = file.read()
    look_ahead_buffer = look_ahead_buffer.replace('\n', '')
    search_buffer = ' ' * 7
    codewords = lz.lz77(search_buffer, look_ahead_buffer)

    f = open(dest,'w')
        
    for el in codewords:
        f.write(str(el) + '\n')
    f.close()

def compute_freq(filename):
    file = open(filename, 'r')
    
    text = file.read()
    text = text.replace('\n', '')
    
    count_a = text.count('A')
    count_c = text.count('C')
    count_g = text.count('G')
    count_t = text.count('T')
    
    return {'A': count_a, 'C': count_c, 'G': count_g, 'T': count_t}

def main():
    lz77_genome('genome.txt', 'lz77_huffman.txt')

    #--- Computes frequencies and builds tree
    freq = compute_freq('genome.txt')
    huff_dic = huf.build_dict(freq)
        
    #--- Edits lz77-compressed files
    file = open('lz77_huffman.txt', 'r')
    text = file.read()
    
    # Replaces all occurrences of the required string
    for base, code in huff_dic.items():
        text = text.replace(base, code)
    file.close()

    file = open('lz77_huffman.txt', 'w')
    file.write(text)
    file.close()

if __name__ == "__main__":
    main()