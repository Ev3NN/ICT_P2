import huffman as huf
import lz77 as lz
import string

def compute_codeword(s_buffer, la_buffer, L):
    """
    Finds the longest prefix in la_buffer that begins in s_buffer,
    and computes the appropriate codeword (d, l, c)

    Parameters
    ----------
    s_buffer: str
        Search buffer containing the past occurrences of
        the message.
    la_buffer: str
        Look-Ahead Buffer containing (a part of) the message
        to encode.
    """
    prefix = la_buffer[0]
    codeword = [0, 0, prefix]
    
    while (idx := s_buffer.rfind(prefix)) != -1:
        d = L - idx
        l = len(prefix)

        if len(prefix) < len(la_buffer):
            c = la_buffer[l]
            codeword = [d, l, c]
            prefix = la_buffer[0:l+1]
        else:
            c = ''
            codeword = [d, l, c]
            break
    
    return tuple(codeword)

def lz77(s_buffer, la_buffer, L):
    """
    Encodes a sequence using the LZ77 Algorithm. 

    Parameters
    ----------
    s_buffer: str
        Search buffer containing the past occurrences of
        the message.
    la_buffer: str
        Look-Ahead Buffer containing (a part of) the message
        to encode.
    """
    codewords = []
    while la_buffer:
        code = compute_codeword(s_buffer, la_buffer, L)
        codewords.append(code)

        l = code[1]
        la_buffer, prefix = la_buffer[l+1:], la_buffer[0:l+1]
        s_buffer += prefix

        s_buffer = s_buffer[-L:]
    
    return codewords

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
    print('Done')

def compute_freq(filename):
    file = open(filename, 'r')
    
    text = file.read()
    text = text.replace('\n', '')
    
    count_a = text.count('A')
    count_c = text.count('C')
    count_g = text.count('G')
    count_t = text.count('T')
    
    return {'A': count_a, 'C': count_c, 'G': count_g, 'T': count_t}

def huffman_genome(src, dest):
    #--- Computes frequencies and builds tree
    freq = compute_freq(src)
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    nodes = huf.build_tree(freq)
    huffmanCode = huf.huffman_code_tree(nodes[0][0])

    huff_dic = {}
    print(' Char | Huffman code ')
    print('----------------------')
    for char, p in freq:
        print(' %-4r |%12s' % (char, huffmanCode[char]))
        huff_dic[char] = huffmanCode[char]
        
    #--- Edits lz77-compressed files
    
    #read input file
    file = open(dest, 'r')
    #read file contents to string
    text = file.read()
    
    #replace all occurrences of the required string
    for base, code in huff_dic.items():
        text = text.replace(base, code)

    #close the input file
    file.close()
    #open the input file in write mode
    file = open(dest, 'w')
    #overwrite the input file with the resulting data
    file.write(text)
    #close the file
    file.close()
    print('Done')

def lz77_trial(look_ahead_buffer):
    for L in range(1, 1001):
        search_buffer = ' ' * L

        codewords = lz77(search_buffer, look_ahead_buffer, L)
        filename = 'LZ77_ENC/LZ77_L={}.txt'.format(L)
        f = open(filename,'w')
            
        for el in codewords:
            f.write(str(el) + '\n')

        f.close()
        print('Done')

def main():
    file = open('genome.txt', 'r')
    look_ahead_buffer = file.read()
    look_ahead_buffer = look_ahead_buffer.replace('\n', '')
    
    lz77_trial(look_ahead_buffer)

if __name__ == "__main__":
    main()