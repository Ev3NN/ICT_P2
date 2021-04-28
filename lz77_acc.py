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

def lz77_trial(look_ahead_buffer):
    for L in range(10, 11):
        search_buffer = ' ' * L

        codewords = lz77(search_buffer, look_ahead_buffer, L)
        filename = 'LZ77_STD/LZ77_L={}.txt'.format(L)
        f = open(filename,'w')
            
        for el in codewords:
            f.write(str(el) + '\n')

        f.close()
        print('Done')
    


def main():
    file = open('genome.txt', 'r')
    look_ahead_buffer = file.read()
    look_ahead_buffer = look_ahead_buffer.replace('\n', '')
    
    print(lz77_trial(look_ahead_buffer))

if __name__ == "__main__":
    main()